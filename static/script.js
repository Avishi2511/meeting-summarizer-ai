let currentTranscript = "";
let currentFileData = null;

document.getElementById("transcribe-btn").addEventListener("click", async function () {
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];
  if (!file) return alert("Please upload a file!");

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("status").style.display = "block";
  document.getElementById("status").innerText = "⏳ Processing file...";

  try {
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
    currentFileData = data;
    
    // Display enhanced status with file info
    const fileInfo = `✅ File processed! Type: ${data.file_type.toUpperCase()} | Words: ${data.processing_info.word_count} | Chunks: ${data.processing_info.chunk_count}`;
    document.getElementById("status").innerText = fileInfo;
    
    document.getElementById("transcript").innerText = data.transcript;
    document.getElementById("transcript-section").style.display = "block";

    // Show analysis options and enable summarize button
    document.getElementById("analysis-options").style.display = "block";
    document.getElementById("summarize-btn").disabled = false;

  } catch (error) {
    document.getElementById("status").innerText = `❌ Error: ${error.message}`;
  }
});

document.getElementById("summarize-btn").addEventListener("click", async function () {
  if (!currentTranscript) return;

  const analysisType = document.getElementById("analysis-type").value;
  document.getElementById("status").innerText = `📝 Analyzing (${analysisType})...`;

  try {
    const response = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        transcript: currentTranscript,
        analysis_type: analysisType
      })
    });

    const data = await response.json();

    if (data.error) {
      document.getElementById("status").innerText = `❌ ${data.error}`;
      return;
    }

    // Display processing info
    const processingInfo = `✅ Analysis complete! Processing time: ${data.processing_time}s | Words: ${data.word_count}`;
    document.getElementById("status").innerText = processingInfo;

    // Display results based on analysis type
    displayAnalysisResults(data, analysisType);
    document.getElementById("summary-section").style.display = "block";

  } catch (error) {
    document.getElementById("status").innerText = `❌ Error: ${error.message}`;
  }
});

function displayAnalysisResults(data, analysisType) {
  const summaryDiv = document.getElementById("summary");
  let content = "";

  if (analysisType === "comprehensive") {
    content = marked.parse(data.comprehensive_summary || data.summary);
  } else if (analysisType === "topics") {
    content = `<h3>📋 Topic Analysis</h3>${marked.parse(data.topic_analysis)}`;
  } else if (analysisType === "actions") {
    content = `<h3>✅ Action Items</h3>${marked.parse(data.action_items)}`;
  } else if (analysisType === "sentiment") {
    content = `<h3>😊 Sentiment Analysis</h3>${marked.parse(data.sentiment_analysis)}`;
  } else if (analysisType === "all") {
    content = `
      <div class="analysis-tabs">
        <div class="tab-buttons">
          <button class="tab-btn active" onclick="showTab('comprehensive')">📋 Summary</button>
          <button class="tab-btn" onclick="showTab('topics')">🎯 Topics</button>
          <button class="tab-btn" onclick="showTab('actions')">✅ Actions</button>
          <button class="tab-btn" onclick="showTab('sentiment')">😊 Sentiment</button>
        </div>
        <div id="comprehensive" class="tab-content active">
          ${marked.parse(data.comprehensive_summary || "")}
        </div>
        <div id="topics" class="tab-content">
          ${marked.parse(data.topic_analysis || "")}
        </div>
        <div id="actions" class="tab-content">
          ${marked.parse(data.action_items || "")}
        </div>
        <div id="sentiment" class="tab-content">
          ${marked.parse(data.sentiment_analysis || "")}
        </div>
      </div>
    `;
  }

  summaryDiv.innerHTML = content;
}

function showTab(tabName) {
  // Hide all tab contents
  const tabContents = document.querySelectorAll('.tab-content');
  tabContents.forEach(tab => tab.classList.remove('active'));
  
  // Remove active class from all buttons
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => btn.classList.remove('active'));
  
  // Show selected tab and mark button as active
  document.getElementById(tabName).classList.add('active');
  event.target.classList.add('active');
}
