// 🔹 Summarization API call
async function summarize() {
  const text = document.getElementById("userInput").value.trim();
  if (!text) {
    alert("Please enter some text.");
    return;
  }

  document.getElementById("resultBox").style.display = "block";
  document.getElementById("summaryOutput").innerText = "⏳ Loading summary...";

  try {
    const response = await fetch("/summary/summary-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: text })
    });

    const data = await response.json();
    console.log(data);
    if (data && data.length>0) {
      document.getElementById("summaryOutput").innerText = data[0];
    } else {
      document.getElementById("summaryOutput").innerText =
        "❌ Error: Could not generate summary.";
    }
  } catch (error) {
    console.error(error);
    document.getElementById("summaryOutput").innerText =
      "⚠️ API request failed.";
  }
}

// 🔹 Loader
let phraseIndex = 0;
let phraseInterval = null;
const loader = document.getElementById("loader");
const loaderText = document.getElementById("loaderText");

const phraseStatic = [
  "⚡ Cooking something cool...",
  "🤖 AI is dangerous... or is it?",
  "🔮 Calibrating brainwaves...",
  "🚀 Launching your experience...",
  "☕ Brewing some digital coffee..."
];

function setupPhrases(action) {
  const phrases = [];
  if (action) {
    phrases.push(action);
  }
  return [...phrases, ...phraseStatic]; // cleaner spread
}

function waiting(action = null) {
  const phrases = setupPhrases(action);

  loader.classList.add("active");

  // Clear any old interval
  clearInterval(phraseInterval);

  phraseIndex = 0;
  loaderText.textContent = phrases[phraseIndex];

  phraseInterval = setInterval(() => {
    phraseIndex = (phraseIndex + 1) % phrases.length;
    loaderText.textContent = phrases[phraseIndex];
  }, 3000);
}

function endWaiting() {
  loader.classList.remove("active");
  clearInterval(phraseInterval);
  phraseInterval = null;
  phraseIndex = 0;
}
