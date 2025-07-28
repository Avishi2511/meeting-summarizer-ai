import os
import whisper
from pathlib import Path
from typing import Dict, Any
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class DocumentProcessor:
    def __init__(self):
        self.whisper_model = None  # Lazy loading
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def _get_whisper_model(self):
        """Lazy load Whisper model"""
        if self.whisper_model is None:
            self.whisper_model = whisper.load_model("base")
        return self.whisper_model
    
    def process_file(self, filepath: str) -> Dict[str, Any]:
        """
        Process uploaded file and return structured data
        """
        file_extension = Path(filepath).suffix.lower()
        
        try:
            if file_extension in ['.mp3', '.wav', '.m4a']:
                return self._process_audio(filepath)
            elif file_extension == '.txt':
                return self._process_text(filepath)
            elif file_extension == '.pdf':
                return self._process_pdf(filepath)
            elif file_extension in ['.docx', '.doc']:
                return self._process_docx(filepath)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_type": file_extension
            }
    
    def _process_audio(self, filepath: str) -> Dict[str, Any]:
        """Process audio files using Whisper"""
        model = self._get_whisper_model()
        result = model.transcribe(filepath)
        transcript = result["text"]
        
        # Clean and preprocess the transcript
        cleaned_transcript = self._clean_text(transcript)
        
        # Split into chunks for better processing
        chunks = self._split_text(cleaned_transcript)
        
        return {
            "success": True,
            "file_type": "audio",
            "raw_transcript": transcript,
            "cleaned_transcript": cleaned_transcript,
            "chunks": chunks,
            "metadata": {
                "duration": result.get("duration", 0),
                "language": result.get("language", "unknown")
            }
        }
    
    def _process_text(self, filepath: str) -> Dict[str, Any]:
        """Process text files"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = self._clean_text(content)
        chunks = self._split_text(cleaned_content)
        
        return {
            "success": True,
            "file_type": "text",
            "raw_transcript": content,
            "cleaned_transcript": cleaned_content,
            "chunks": chunks,
            "metadata": {
                "char_count": len(content),
                "word_count": len(content.split())
            }
        }
    
    def _process_pdf(self, filepath: str) -> Dict[str, Any]:
        """Process PDF files"""
        loader = PyPDFLoader(filepath)
        documents = loader.load()
        
        # Combine all pages
        content = "\n\n".join([doc.page_content for doc in documents])
        cleaned_content = self._clean_text(content)
        chunks = self._split_text(cleaned_content)
        
        return {
            "success": True,
            "file_type": "pdf",
            "raw_transcript": content,
            "cleaned_transcript": cleaned_content,
            "chunks": chunks,
            "metadata": {
                "page_count": len(documents),
                "char_count": len(content)
            }
        }
    
    def _process_docx(self, filepath: str) -> Dict[str, Any]:
        """Process DOCX files"""
        loader = Docx2txtLoader(filepath)
        documents = loader.load()
        
        content = "\n\n".join([doc.page_content for doc in documents])
        cleaned_content = self._clean_text(content)
        chunks = self._split_text(cleaned_content)
        
        return {
            "success": True,
            "file_type": "docx",
            "raw_transcript": content,
            "cleaned_transcript": cleaned_content,
            "chunks": chunks,
            "metadata": {
                "char_count": len(content),
                "word_count": len(content.split())
            }
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove common transcription artifacts
        text = text.replace("um,", "").replace("uh,", "").replace("you know,", "")
        
        # Fix common punctuation issues
        text = text.replace(" ,", ",").replace(" .", ".")
        text = text.replace("  ", " ")
        
        return text.strip()
    
    def _split_text(self, text: str) -> list:
        """Split text into semantic chunks"""
        documents = [Document(page_content=text)]
        chunks = self.text_splitter.split_documents(documents)
        
        return [
            {
                "content": chunk.page_content,
                "metadata": chunk.metadata,
                "length": len(chunk.page_content)
            }
            for chunk in chunks
        ]
