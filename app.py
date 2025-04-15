from flask import Flask, request, jsonify, render_template
import whisper
from openai import OpenAI
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Groq API setup
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# Load Whisper model once
model = whisper.load_model("base")

@app.route('/')
def index():
    return render_template('index.html')

# ✅ Route for transcription only
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    if filename.endswith(('.mp3', '.wav')):
        result = model.transcribe(filepath)
        transcript = result["text"]
    elif filename.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            transcript = f.read()
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({"transcript": transcript})

# ✅ Separate route for summarizing transcript
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    transcript = data.get("transcript", "")

    if not transcript:
        return jsonify({"error": "Transcript not provided"}), 400

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You're an assistant that summarizes meeting transcripts in a structured way, with bullet points and clear headings."},
                {"role": "user", "content": f"Summarize this meeting:\n{transcript}"}
            ],
            temperature=0.7
        )
        summary = response.choices[0].message.content

        # Format summary into bullet points
        formatted_summary = "<ul>"
        for line in summary.strip().split('\n'):
            if line.strip():  # ignore empty lines
                formatted_summary += f"<li>{line.strip()}</li>"
        formatted_summary += "</ul>"

        return jsonify({"summary": formatted_summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
