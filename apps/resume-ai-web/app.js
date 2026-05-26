const API_BASE = window.API_BASE_URL || "";

const form = document.querySelector("#analyze-form");
const score = document.querySelector("#score");
const verdict = document.querySelector("#verdict");
const matched = document.querySelector("#matched");
const missing = document.querySelector("#missing");
const improvements = document.querySelector("#improvements");
const chatButton = document.querySelector("#chat-button");
const chatAnswer = document.querySelector("#chat-answer");

let lastPayload = null;

function chips(node, values) {
  node.innerHTML = "";
  values.forEach((value) => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = value;
    node.appendChild(chip);
  });
}

function list(node, values) {
  node.innerHTML = "";
  values.forEach((value) => {
    const item = document.createElement("li");
    item.textContent = value;
    node.appendChild(item);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const submit = form.querySelector("button");
  submit.disabled = true;
  submit.textContent = "Analyzing...";

  lastPayload = {
    role_title: document.querySelector("#role-title").value,
    resume_text: document.querySelector("#resume-text").value,
    job_description: document.querySelector("#job-description").value,
  };

  try {
    const response = await fetch(`${API_BASE}/api/v1/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastPayload),
    });
    const data = await response.json();
    score.textContent = data.score;
    verdict.textContent = data.verdict;
    chips(matched, data.matched_keywords);
    chips(missing, data.missing_keywords);
    list(improvements, data.improvements);
  } catch (error) {
    verdict.textContent = "Could not reach the API. Check that the backend is running.";
  } finally {
    submit.disabled = false;
    submit.textContent = "Analyze Resume";
  }
});

chatButton.addEventListener("click", async () => {
  chatAnswer.textContent = "Thinking...";
  const payload = {
    message: document.querySelector("#chat-message").value,
    resume_text: lastPayload?.resume_text,
    job_description: lastPayload?.job_description,
  };

  try {
    const response = await fetch(`${API_BASE}/api/v1/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    chatAnswer.textContent = data.answer;
  } catch (error) {
    chatAnswer.textContent = "Could not reach the chatbot endpoint.";
  }
});

