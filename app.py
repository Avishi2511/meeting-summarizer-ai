import streamlit as st
import whisper
from openai import OpenAI
import os

# Optionally use environment variable or hardcode
client = OpenAI(api_key="sk-abcdef1234567890abcdef1234567890abcdef12")

# Load Whisper model
model = whisper.load_model("base")

st.title("AI Meeting Note Assistant")
st.write("Upload an audio file or transcript to get meeting notes!")

uploaded_file = st.file_uploader("Upload Audio (.mp3/.wav) or Text (.txt)", type=["mp3", "wav", "txt"])

def summarize_transcript(transcript_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're an assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Summarize this meeting:\n{transcript_text}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

if uploaded_file:
    file_type = uploaded_file.type

    if file_type.startswith("audio"):
        # Save and transcribe audio
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.read())
        st.info("Transcribing audio...")
        result = model.transcribe("temp_audio.wav")
        transcript = result["text"]

    elif file_type == "text/plain":
        transcript = uploaded_file.read().decode("utf-8")

    else:
        st.error("Unsupported file type.")
        st.stop()

    st.success("Transcript ready!")
    st.text_area("Transcript", transcript, height=200)

    if st.button("Summarize"):
        st.info("Summarizing...")
        try:
            summary = summarize_transcript(transcript)
            st.subheader("📌 Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"Error: {e}")
