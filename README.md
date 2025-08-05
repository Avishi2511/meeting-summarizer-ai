# AI Meeting Summarizer - Enhanced with LangChain

An intelligent meeting summarizer that processes audio files, documents, and text to generate comprehensive meeting summaries using LangChain and advanced AI analysis.

## Features

### Enhanced Document Processing with LangChain
- **Multi-format Support**: Supports MP3, WAV, TXT, PDF, and DOCX files
- **Intelligent Text Splitting**: Uses LangChain's RecursiveCharacterTextSplitter for semantic chunking
- **Text Preprocessing**: Automatic cleaning and normalization of transcripts
- **Metadata Extraction**: Extracts file metadata including duration, language, word count, etc.

### Intelligent Summarization Pipeline
- **Multi-stage Processing**: Structured analysis pipeline with multiple specialized prompts
- **Analysis Types**:
  - **Comprehensive Summary**: Full structured meeting report with all sections
  - **Topic Analysis**: Key topics and themes extraction
  - **Action Items**: Tasks and assignments identification
  - **Sentiment Analysis**: Meeting tone and engagement analysis
  - **All Types**: Combined analysis with tabbed interface

### Professional Summary Templates
- **Executive Summary**: High-level overview with key outcomes
- **Key Discussion Points**: Main topics with context
- **Decisions Made**: Documented decisions with responsible parties
- **Action Items**: Specific tasks with assignments and deadlines
- **Next Steps**: Follow-up actions and milestones
- **Participants & Roles**: Key attendees and their contributions

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Avishi2511/meeting-summarizer-ai.git
cd meeting-summarizer-ai
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

4. **Run the application**:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

5. **Access the application**:
Open your browser and go to `http://127.0.0.1:8000`

## 🎯 Usage

1. **Upload a file**: Drag and drop or select MP3, WAV, TXT, PDF, or DOCX files
2. **Choose analysis type**: Select from comprehensive, topics, actions, sentiment, or all
3. **Get results**: View structured summaries with professional formatting

## 🔍 Analysis Types

- **Comprehensive**: Complete meeting summary with all sections
- **Topics**: Key discussion points and themes
- **Actions**: Action items, tasks, and assignments
- **Sentiment**: Meeting tone and engagement analysis
- **All**: Combined analysis with tabbed interface

## 🔧 Technical Stack

- **Backend**: FastAPI, LangChain, OpenAI/Groq API
- **Document Processing**: Whisper, PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI Models**: LLaMA 3 70B via Groq API

## 🚀 Future Enhancements

The current implementation provides a solid foundation for:
- Vector database integration for meeting history and search
- RAG (Retrieval-Augmented Generation) for context-aware summaries
- Real-time meeting assistance
- Integration with calendar systems
- Multi-language support
- Advanced analytics and insights
