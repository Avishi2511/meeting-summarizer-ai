#!/usr/bin/env python3
"""
Simple test script to verify the enhanced meeting summarizer works
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all imports work correctly"""
    try:
        print("Testing imports...")
        from services.document_processor import DocumentProcessor
        from services.summarization_chain import SummarizationChain
        from services.prompt_templates import MeetingPromptTemplates
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_document_processor():
    """Test document processor initialization"""
    try:
        print("Testing DocumentProcessor...")
        from services.document_processor import DocumentProcessor
        processor = DocumentProcessor()
        print("✅ DocumentProcessor initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ DocumentProcessor error: {e}")
        return False

def test_summarization_chain():
    """Test summarization chain initialization"""
    try:
        print("Testing SummarizationChain...")
        from services.summarization_chain import SummarizationChain
        
        # Check if API key exists
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️  GROQ_API_KEY not found in environment")
            return False
            
        chain = SummarizationChain(groq_api_key=api_key)
        print("✅ SummarizationChain initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ SummarizationChain error: {e}")
        return False

def test_text_processing():
    """Test basic text processing"""
    try:
        print("Testing text processing...")
        from services.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        
        # Create a test text file
        test_file = "test_meeting.txt"
        test_content = """
        Meeting Notes - Project Alpha
        
        Attendees: John, Sarah, Mike
        
        Discussion Points:
        1. Project timeline review
        2. Budget allocation
        3. Resource planning
        
        Action Items:
        - John to prepare budget report by Friday
        - Sarah to schedule follow-up meeting
        - Mike to review technical specifications
        
        Next meeting: Next Tuesday at 2 PM
        """
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Process the file
        result = processor.process_file(test_file)
        
        # Clean up
        os.remove(test_file)
        
        if result["success"]:
            print("✅ Text processing successful!")
            print(f"   - File type: {result['file_type']}")
            print(f"   - Word count: {result['metadata']['word_count']}")
            print(f"   - Chunks: {len(result['chunks'])}")
            return True
        else:
            print(f"❌ Text processing failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Text processing error: {e}")
        return False

def test_summarization():
    """Test basic summarization"""
    try:
        print("Testing summarization...")
        from services.summarization_chain import SummarizationChain
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️  Skipping summarization test - no API key")
            return True
            
        chain = SummarizationChain(groq_api_key=api_key)
        
        test_transcript = """
        This is a test meeting transcript. We discussed the quarterly budget review.
        John presented the financial report showing a 15% increase in revenue.
        Sarah suggested optimizing our marketing spend for better ROI.
        Action items: John will prepare detailed analysis by Friday.
        Sarah will schedule follow-up meeting next week.
        """
        
        result = chain.process_transcript(test_transcript, "comprehensive")
        
        if result["success"]:
            print("✅ Summarization successful!")
            print(f"   - Analysis type: {result['analysis_type']}")
            print(f"   - Word count: {result['word_count']}")
            return True
        else:
            print(f"❌ Summarization failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Summarization error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Enhanced Meeting Summarizer")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_document_processor,
        test_summarization_chain,
        test_text_processing,
        test_summarization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        print("\nTo start the server, run:")
        print("uvicorn main:app --reload --host 127.0.0.1 --port 8000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        
    return passed == total

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    success = main()
    sys.exit(0 if success else 1)
