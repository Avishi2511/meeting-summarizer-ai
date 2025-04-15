let currentTranscript = "";

document.getElementById("transcribe-btn").addEventListener("click", async function () {
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];
  if (!file) return alert("Please upload a file!");

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("status").innerText = "⏳ Transcribing...";

  const response = await fetch("/upload", {
    method: "POST",
    body: formData
  });

  const data = await response.json();

  if (data.error) {
    document.getElementById("status").innerText = `❌ ${data.error}`;
    return;
  }

  currentTranscript = data.transcript;
  document.getElementById("status").innerText = "✅ Transcript ready!";
  document.getElementById("transcript").innerText = data.transcript;
  document.getElementById("transcript-section").style.display = "block";

  document.getElementById("summarize-btn").disabled = false;
});

document.getElementById("summarize-btn").addEventListener("click", async function () {
  if (!currentTranscript) return;

  document.getElementById("status").innerText = "📝 Summarizing...";

  const response = await fetch("/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transcript: currentTranscript })
  });

  const data = await response.json();

  if (data.error) {
    document.getElementById("status").innerText = `❌ ${data.error}`;
    return;
  }

  document.getElementById("status").innerText = "✅ Summary ready!";

  // ✅ Parse markdown from model into HTML
  const formatted = marked.parse(data.summary);
  document.getElementById("summary").innerHTML = formatted;
  document.getElementById("summary-section").style.display = "block";
});
