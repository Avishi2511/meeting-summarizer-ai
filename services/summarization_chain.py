import os
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from services.prompt_templates import MeetingPromptTemplates

class GeminiLLM:
    """Simple Gemini API wrapper"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        self._client = None
        # Configure the API key
        genai.configure(api_key=api_key)
    
    @property
    def client(self):
        """Lazy initialization of Gemini client"""
        if self._client is None:
            self._client = genai.GenerativeModel(self.model)
        return self._client
    
    def generate(self, prompt: str) -> str:
        """Generate response from Gemini API"""
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2000,
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

class SummarizationChain:
    """Multi-stage summarization pipeline"""
    
    def __init__(self, gemini_api_key: str):
        self.llm = GeminiLLM(api_key=gemini_api_key)
        self.templates = MeetingPromptTemplates()
    
    def process_transcript(self, transcript: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Process transcript through the summarization pipeline
        
        Args:
            transcript: The meeting transcript text
            analysis_type: Type of analysis to perform
                - "comprehensive": Full structured summary
                - "topics": Topic extraction only
                - "actions": Action items only
                - "sentiment": Sentiment analysis only
                - "all": All types of analysis
        """
        
        try:
            results = {
                "success": True,
                "analysis_type": analysis_type,
                "input_length": len(transcript),
                "word_count": len(transcript.split())
            }
            
            if analysis_type == "comprehensive" or analysis_type == "all":
                results["comprehensive_summary"] = self._generate_comprehensive_summary(transcript)
            
            if analysis_type == "topics" or analysis_type == "all":
                results["topic_analysis"] = self._extract_topics(transcript)
            
            if analysis_type == "actions" or analysis_type == "all":
                results["action_items"] = self._extract_action_items(transcript)
            
            if analysis_type == "sentiment" or analysis_type == "all":
                results["sentiment_analysis"] = self._analyze_sentiment(transcript)
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis_type": analysis_type
            }
    
    def process_chunks(self, chunks: List[Dict], analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Process multiple text chunks and combine results
        """
        try:
            # For long documents, process chunks separately and then combine
            if len(chunks) == 1:
                return self.process_transcript(chunks[0]["content"], analysis_type)
            
            # Process each chunk
            chunk_results = []
            for i, chunk in enumerate(chunks):
                chunk_result = self.process_transcript(chunk["content"], "topics")
                chunk_result["chunk_index"] = i
                chunk_results.append(chunk_result)
            
            # Combine all chunks for final comprehensive analysis
            combined_text = "\n\n".join([chunk["content"] for chunk in chunks])
            
            # Limit combined text to avoid token limits
            if len(combined_text) > 15000:  # Rough token limit
                combined_text = combined_text[:15000] + "\n\n[Content truncated for processing]"
            
            final_result = self.process_transcript(combined_text, analysis_type)
            final_result["chunk_results"] = chunk_results
            final_result["total_chunks"] = len(chunks)
            
            return final_result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis_type": analysis_type
            }
    
    def _generate_comprehensive_summary(self, transcript: str) -> str:
        """Generate comprehensive structured summary"""
        prompt = self.templates.get_comprehensive_summary_prompt().format(transcript=transcript)
        return self.llm.generate(prompt)
    
    def _extract_topics(self, transcript: str) -> str:
        """Extract key topics from transcript"""
        prompt = self.templates.get_topic_extraction_prompt().format(transcript=transcript)
        return self.llm.generate(prompt)
    
    def _extract_action_items(self, transcript: str) -> str:
        """Extract action items from transcript"""
        prompt = self.templates.get_action_items_prompt().format(transcript=transcript)
        return self.llm.generate(prompt)
    
    def _analyze_sentiment(self, transcript: str) -> str:
        """Analyze sentiment and tone of transcript"""
        prompt = self.templates.get_sentiment_analysis_prompt().format(transcript=transcript)
        return self.llm.generate(prompt)
    
    def get_summary_types(self) -> List[str]:
        """Return available summary types"""
        return ["comprehensive", "topics", "actions", "sentiment", "all"]
