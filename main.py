from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from dotenv import load_dotenv
import whisper
import os
import time
from pathlib import Path
import shutil
from services.document_processor import DocumentProcessor
from services.summarization_chain import SummarizationChain
from models.meeting_models import FileUploadResponse, SummaryRequest, SummaryResponse

app = FastAPI()
load_dotenv()

# Set up folders
UPLOAD_FOLDER = "uploads"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-pro")

# ✅ Initialize services
document_processor = DocumentProcessor()
summarization_chain = SummarizationChain(gemini_api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Whisper model (lazy loading for backward compatibility)
model = None

def get_whisper_model():
    global model
    if model is None:
        model = whisper.load_model("base")
    return model

# ✅ Homepage route
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Enhanced route for file processing with LangChain
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Save uploaded file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process file using the enhanced document processor
    result = document_processor.process_file(filepath)
    
    if not result["success"]:
        return JSONResponse(status_code=400, content={"error": result["error"]})
    
    # Return enhanced response with metadata and chunks
    return {
        "transcript": result["cleaned_transcript"],
        "raw_transcript": result["raw_transcript"],
        "file_type": result["file_type"],
        "metadata": result["metadata"],
        "chunks": len(result["chunks"]),
        "processing_info": {
            "text_length": len(result["cleaned_transcript"]),
            "word_count": len(result["cleaned_transcript"].split()),
            "chunk_count": len(result["chunks"])
        }
    }

# ✅ Legacy upload route for backward compatibility
@app.post("/upload-legacy")
async def upload_file_legacy(file: UploadFile = File(...)):
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if filename.endswith((".mp3", ".wav")):
        whisper_model = get_whisper_model()
        result = whisper_model.transcribe(filepath)
        transcript = result["text"]
    elif filename.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            transcript = f.read()
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    return {"transcript": transcript}

# ✅ Enhanced route for intelligent summarization with LangChain
@app.post("/summarize")
async def summarize(data: dict):
    transcript = data.get("transcript", "")
    analysis_type = data.get("analysis_type", "comprehensive")
    
    if not transcript:
        return JSONResponse(status_code=400, content={"error": "Transcript not provided"})

    try:
        start_time = time.time()
        
        # Use the enhanced summarization chain
        result = summarization_chain.process_transcript(transcript, analysis_type)
        
        processing_time = time.time() - start_time
        result["processing_time"] = round(processing_time, 2)
        
        if not result["success"]:
            return JSONResponse(status_code=500, content={"error": result["error"]})
        
        # Return structured response based on analysis type
        if analysis_type == "comprehensive":
            return {"summary": result["comprehensive_summary"], **result}
        else:
            return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ New route for processing with chunks (for large documents)
@app.post("/process")
async def process_document(data: dict):
    """Enhanced processing endpoint that handles chunked documents"""
    transcript = data.get("transcript", "")
    chunks = data.get("chunks", [])
    analysis_type = data.get("analysis_type", "comprehensive")
    
    if not transcript and not chunks:
        return JSONResponse(status_code=400, content={"error": "Transcript or chunks not provided"})

    try:
        start_time = time.time()
        
        if chunks:
            # Process using chunks for better handling of large documents
            result = summarization_chain.process_chunks(chunks, analysis_type)
        else:
            # Process single transcript
            result = summarization_chain.process_transcript(transcript, analysis_type)
        
        processing_time = time.time() - start_time
        result["processing_time"] = round(processing_time, 2)
        
        if not result["success"]:
            return JSONResponse(status_code=500, content={"error": result["error"]})
        
        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ Route to get available analysis types
@app.get("/analysis-types")
async def get_analysis_types():
    """Get available analysis types"""
    return {
        "types": summarization_chain.get_summary_types(),
        "descriptions": {
            "comprehensive": "Full structured summary with all sections",
            "topics": "Key topics and themes extraction",
            "actions": "Action items and tasks extraction",
            "sentiment": "Sentiment and tone analysis",
            "all": "All analysis types combined"
        }
    }

# ✅ Legacy summarize route for backward compatibility
@app.post("/summarize-legacy")
async def summarize_legacy(data: dict):
    transcript = data.get("transcript", "")

    if not transcript:
        return JSONResponse(status_code=400, content={"error": "Transcript not provided"})

    try:
        prompt = f"""You're an assistant that summarizes meeting transcripts in a structured way, with bullet points and clear headings.

Summarize this meeting:
{transcript}"""

        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2000,
            )
        )
        summary = response.text

        # Return the summary as a Markdown string
        return {"summary": summary}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
