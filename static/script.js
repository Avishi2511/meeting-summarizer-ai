document.getElementById("upload-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const formData = new FormData();
    const file = document.getElementById("file").files[0];
    formData.append("file", file);
  
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });
  
    const data = await response.json();
    document.getElementById("output").innerHTML = `
      <h2>Transcript</h2><p>${data.transcript}</p>
      <h2>Summary</h2><p>${data.summary}</p>
    `;
  });
  