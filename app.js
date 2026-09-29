/**
 * EduGenie Frontend Application Logic
 * Interactive handlers for Q&A, Explain, Summarize, Quiz, and Learning Path.
 */

// Sample Industrial Revolution passage for quick testing
const INDUSTRIAL_REVOLUTION_SAMPLE = 
  "The Industrial Revolution began in Great Britain in the late 18th century and quickly transformed human society from an agrarian handicraft economy to one dominated by industry and machine manufacturing. Technological innovations such as James Watt's improved steam engine, James Hargreaves' Spinning Jenny, and Richard Arkwright's water frame dramatically increased textile production efficiency. As factories centralized production, millions of agricultural workers migrated from rural areas to burgeoning urban industrial centers like Manchester, Birmingham, and Leeds. This massive demographic shift gave rise to new social classes, including the industrial working class and the wealthy bourgeoisie, while revolutionizing global transportation through steam locomotives and steamships. Despite fostering unprecedented economic growth and technological innovation, early industrialization also caused severe social challenges, including grueling 14-hour workdays, dangerous working conditions, child labor, and intense urban pollution.";

document.addEventListener("DOMContentLoaded", () => {
  initHealthCheck();
  initSampleButtons();
  initQnA();
  initExplain();
  initSummarize();
  initQuiz();
  initLearningPath();
});

// Simple Markdown to HTML formatter
function formatMarkdown(text) {
  if (!text) return "";
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Headings
  html = html.replace(/^### (.*$)/gim, "<h3>$1</h3>");
  html = html.replace(/^#### (.*$)/gim, "<h4>$1</h4>");
  html = html.replace(/^## (.*$)/gim, "<h2>$1</h2>");

  // Bold & Italic
  html = html.replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>");
  html = html.replace(/\*(.*?)\*/gim, "<em>$1</em>");

  // Inline code
  html = html.replace(/`([^`]+)`/gim, "<code>$1</code>");

  // Bullet points
  html = html.replace(/^[•\-\*]\s+(.*$)/gim, "<li>$1</li>");
  html = html.replace(/(<li>[\s\S]*?<\/li>)/gm, "<ul>$1</ul>");
  // Clean multiple contiguous <ul> tags
  html = html.replace(/<\/ul>\s*<ul>/g, "");

  // Paragraphs
  html = html.replace(/\n\n+/g, "</p><p>");
  html = "<p>" + html + "</p>";
  html = html.replace(/<p><\/p>/g, "");
  html = html.replace(/<p>(<h[234]>)/g, "$1");
  html = html.replace(/(<\/h[234]>)<\/p>/g, "$1");
  html = html.replace(/<p>(<ul>[\s\S]*?<\/ul>)<\/p>/g, "$1");

  return html;
}

// Initial System Health Check
async function initHealthCheck() {
  try {
    const res = await fetch("/health");
    if (res.ok) {
      const data = await res.json();
      const modeBadge = document.getElementById("mode-badge");
      const modeText = document.getElementById("mode-text");
      if (data.mode === "live") {
        modeBadge.className = "badge badge-live";
        modeText.textContent = `Live Gemini (${data.default_model})`;
      } else {
        modeBadge.className = "badge badge-demo";
        modeText.textContent = "Demo Mode (Offline)";
      }
    }
  } catch (err) {
    console.warn("Health check error:", err);
  }
}

// Sample buttons loader
function initSampleButtons() {
  document.querySelectorAll(".btn-sample[data-target]").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const val = btn.getAttribute("data-value");
      const targetInput = document.getElementById(targetId);
      if (targetInput) {
        targetInput.value = val;
        targetInput.focus();
      }
    });
  });

  const btnSampleRev = document.getElementById("btn-sample-revolution");
  if (btnSampleRev) {
    btnSampleRev.addEventListener("click", () => {
      const sumInput = document.getElementById("summarize-input");
      if (sumInput) {
        sumInput.value = INDUSTRIAL_REVOLUTION_SAMPLE;
        sumInput.focus();
      }
    });
  }
}

// Helper to show/hide UI state
function setCardState(cardId, loading, errorMsg = "") {
  const spinner = document.getElementById(`spinner-${cardId}`);
  const submitBtn = document.getElementById(`btn-${cardId}-submit`);
  const errorBanner = document.getElementById(`error-${cardId}`);
  const resultBox = document.getElementById(`result-${cardId}`);

  if (spinner) spinner.style.display = loading ? "inline-block" : "none";
  if (submitBtn) submitBtn.disabled = loading;

  if (errorBanner) {
    if (errorMsg) {
      errorBanner.textContent = errorMsg;
      errorBanner.style.display = "block";
    } else {
      errorBanner.style.display = "none";
    }
  }

  if (loading && resultBox) {
    // Keep visible or clear on new search
  }
}

// 1. Smart Q&A Handler
function initQnA() {
  const form = document.getElementById("form-qa");
  const input = document.getElementById("qa-input");
  const resultBox = document.getElementById("result-qa");
  const content = document.getElementById("content-qa");
  const meta = document.getElementById("meta-qa");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q) {
      setCardState("qa", false, "Please enter a valid question.");
      return;
    }

    setCardState("qa", true, "");
    try {
      const res = await fetch(`/qa?question=${encodeURIComponent(q)}`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to fetch answer");

      content.innerHTML = `<p>${data.answer}</p>`;
      meta.textContent = `Mode: ${data.mode.toUpperCase()} • Model: ${data.model}`;
      resultBox.style.display = "block";
      setCardState("qa", false, "");
    } catch (err) {
      setCardState("qa", false, err.message);
    }
  });
}

// 2. Concept Explainer Handler
function initExplain() {
  const form = document.getElementById("form-explain");
  const input = document.getElementById("explain-input");
  const resultBox = document.getElementById("result-explain");
  const content = document.getElementById("content-explain");
  const meta = document.getElementById("meta-explain");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const topic = input.value.trim();
    if (!topic) {
      setCardState("explain", false, "Please enter a concept or topic.");
      return;
    }

    const backendEl = document.querySelector('input[name="explain-backend"]:checked');
    const backend = backendEl ? backendEl.value : "gemini";

    setCardState("explain", true, "");
    try {
      const res = await fetch("/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, backend })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to generate explanation");

      content.innerHTML = formatMarkdown(data.explanation);
      meta.textContent = `Backend: ${data.backend.toUpperCase()} • Mode: ${data.mode.toUpperCase()}`;
      resultBox.style.display = "block";
      setCardState("explain", false, "");
    } catch (err) {
      setCardState("explain", false, err.message);
    }
  });
}

// 3. Passage Summarizer Handler
function initSummarize() {
  const form = document.getElementById("form-summarize");
  const input = document.getElementById("summarize-input");
  const resultBox = document.getElementById("result-summarize");
  const content = document.getElementById("content-summarize");
  const meta = document.getElementById("meta-summarize");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text || text.length < 5) {
      setCardState("summarize", false, "Please enter at least 5 characters to summarize.");
      return;
    }

    setCardState("summarize", true, "");
    try {
      const res = await fetch("/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to generate summary");

      content.innerHTML = formatMarkdown(data.summary);
      meta.textContent = `Original: ${data.original_length} chars • Mode: ${data.mode.toUpperCase()}`;
      resultBox.style.display = "block";
      setCardState("summarize", false, "");
    } catch (err) {
      setCardState("summarize", false, err.message);
    }
  });
}

// 4. Interactive Quiz Generator & Grader
let currentQuizData = [];

function initQuiz() {
  const form = document.getElementById("form-quiz");
  const input = document.getElementById("quiz-input");
  const resultBox = document.getElementById("result-quiz");
  const quizContainer = document.getElementById("quiz-container");
  const scoreBanner = document.getElementById("quiz-score-banner");
  const quizActions = document.getElementById("quiz-actions");
  const meta = document.getElementById("meta-quiz");
  const btnSubmitAll = document.getElementById("btn-submit-all-quiz");
  const btnResetQuiz = document.getElementById("btn-reset-quiz");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const topic = input.value.trim();
    if (!topic) {
      setCardState("quiz", false, "Please enter a topic or text for the quiz.");
      return;
    }

    setCardState("quiz", true, "");
    scoreBanner.style.display = "none";
    try {
      const res = await fetch("/quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to generate quiz");

      currentQuizData = data.quiz;
      renderQuizQuestions(currentQuizData);

      meta.textContent = `3 Questions • Mode: ${data.mode.toUpperCase()} • Model: ${data.model}`;
      resultBox.style.display = "block";
      quizActions.style.display = "flex";
      setCardState("quiz", false, "");
    } catch (err) {
      setCardState("quiz", false, err.message);
    }
  });

  btnSubmitAll.addEventListener("click", () => {
    evaluateAllQuestions();
  });

  btnResetQuiz.addEventListener("click", () => {
    if (currentQuizData.length > 0) {
      renderQuizQuestions(currentQuizData);
      scoreBanner.style.display = "none";
    }
  });
}

function renderQuizQuestions(quizList) {
  const container = document.getElementById("quiz-container");
  container.innerHTML = "";

  quizList.forEach((qItem, qIdx) => {
    const card = document.createElement("div");
    card.className = "quiz-q-card";
    card.id = `q-card-${qIdx}`;

    let optionsHtml = qItem.options.map((opt, optIdx) => `
      <label class="quiz-option-label" id="opt-label-${qIdx}-${optIdx}">
        <input type="radio" name="quiz-q-${qIdx}" value="${opt.replace(/"/g, "&quot;")}" data-qindex="${qIdx}">
        <span>${opt}</span>
      </label>
    `).join("");

    card.innerHTML = `
      <div class="quiz-q-title">Q${qIdx + 1}. ${qItem.question}</div>
      <div class="quiz-options-group">${optionsHtml}</div>
      <div id="q-feedback-${qIdx}" style="display:none;"></div>
    `;

    container.appendChild(card);
  });
}

function evaluateAllQuestions() {
  let score = 0;
  const total = currentQuizData.length;

  currentQuizData.forEach((qItem, qIdx) => {
    const selectedRadio = document.querySelector(`input[name="quiz-q-${qIdx}"]:checked`);
    const feedbackEl = document.getElementById(`q-feedback-${qIdx}`);
    const correctAnswer = qItem.answer.trim();

    // Reset styles on options
    qItem.options.forEach((opt, optIdx) => {
      const label = document.getElementById(`opt-label-${qIdx}-${optIdx}`);
      label.className = "quiz-option-label";
      if (opt.trim() === correctAnswer) {
        label.classList.add("opt-correct");
      }
    });

    if (selectedRadio) {
      const chosenAnswer = selectedRadio.value.trim();
      const chosenIdx = qItem.options.findIndex(o => o.trim() === chosenAnswer);
      const chosenLabel = document.getElementById(`opt-label-${qIdx}-${chosenIdx}`);

      if (chosenAnswer === correctAnswer) {
        score++;
        feedbackEl.className = "q-feedback-badge badge-success";
        feedbackEl.innerHTML = `✓ Correct! "${correctAnswer}" is the right answer.`;
      } else {
        if (chosenLabel) chosenLabel.classList.add("opt-incorrect");
        feedbackEl.className = "q-feedback-badge badge-danger";
        feedbackEl.innerHTML = `✗ Incorrect. You selected "${chosenAnswer}". The correct answer is <strong>"${correctAnswer}"</strong>.`;
      }
    } else {
      feedbackEl.className = "q-feedback-badge badge-danger";
      feedbackEl.innerHTML = `⚠️ Unanswered. The correct answer is <strong>"${correctAnswer}"</strong>.`;
    }
    feedbackEl.style.display = "block";
  });

  // Show score banner
  const scoreBanner = document.getElementById("quiz-score-banner");
  const scoreText = document.getElementById("score-text");
  const scoreFeedback = document.getElementById("score-feedback");
  const percentage = Math.round((score / total) * 100);

  scoreText.textContent = `Score: ${score}/${total} (${percentage}%)`;
  if (score === total) {
    scoreFeedback.textContent = "🌟 Outstanding! Perfect score!";
  } else if (score >= 2) {
    scoreFeedback.textContent = "👏 Great job! You have a solid grasp of this topic.";
  } else {
    scoreFeedback.textContent = "📚 Keep reviewing the study materials and try again!";
  }
  scoreBanner.style.display = "block";
}

// 5. Learning Path Roadmap Handler
function initLearningPath() {
  const form = document.getElementById("form-learn");
  const input = document.getElementById("learn-input");
  const resultBox = document.getElementById("result-learn");
  const content = document.getElementById("content-learn");
  const meta = document.getElementById("meta-learn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const topic = input.value.trim();
    if (!topic) {
      setCardState("learn", false, "Please enter a subject or skill.");
      return;
    }

    setCardState("learn", true, "");
    try {
      const res = await fetch(`/learn/recommendations?topic=${encodeURIComponent(topic)}`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to generate learning path");

      content.innerHTML = formatMarkdown(data.recommendations);
      meta.textContent = `Topic: ${data.topic} • Mode: ${data.mode.toUpperCase()}`;
      resultBox.style.display = "block";
      setCardState("learn", false, "");
    } catch (err) {
      setCardState("learn", false, err.message);
    }
  });
}
