from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import whisper
import os
from pathlib import Path
import shutil

app = FastAPI()

# Set up folders
UPLOAD_FOLDER = "uploads"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Groq API setup
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# ✅ Load Whisper model
model = whisper.load_model("base")

# ✅ Homepage route
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Route for transcription
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if filename.endswith((".mp3", ".wav")):
        result = model.transcribe(filepath)
        transcript = result["text"]
    elif filename.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            transcript = f.read()
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    return {"transcript": transcript}

# ✅ Route for summarizing transcript
@app.post("/summarize")
async def summarize(data: dict):
    transcript = data.get("transcript", "")

    if not transcript:
        return JSONResponse(status_code=400, content={"error": "Transcript not provided"})

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{
                "role": "system", "content": "You're an assistant that summarizes meeting transcripts in a structured way, with bullet points and clear headings."
            }, {
                "role": "user", "content": f"Summarize this meeting:\n{transcript}"
            }],
            temperature=0.7
        )
        summary = response.choices[0].message.content

        # Return the summary as a Markdown string
        return {"summary": summary}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
