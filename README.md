# 🧞‍♂️ EduGenie — Google Gemini Powered Learning Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B%20%7C%203.13-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Google GenAI](https://img.shields.io/badge/Google%20GenAI-Gemini%20Flash%20%2F%20Pro-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![Pytest](https://img.shields.io/badge/Tests-37%20Passed%20(100%25)-success.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automated%20E2E-2EAD33.svg?logo=playwright&logoColor=white)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**EduGenie** is a lightweight, responsive educational assistant that simplifies learning through generative AI. Designed for students of all academic levels, EduGenie breaks down complex concepts, answers factual questions, condenses dense study passages, generates 3-MCQ interactive quizzes with automated grading, and constructs personalized curriculum roadmaps.

Equipped with a **hybrid AI inference engine** (Google Gemini API + local HuggingFace `MBZUAI/LaMini-Flan-T5-783M`) and a **deterministic offline knowledge generator**, EduGenie guarantees **100% uptime** with zero crashes even during API rate limits or offline classroom use.

---

## 📋 Table of Contents
- [Overview & Problem Statement](#overview--problem-statement)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Installation & Quickstart](#installation--quickstart)
  - [Option A: Offline Demo Mode (No API Key Required)](#option-a-offline-demo-mode-no-api-key-required)
  - [Option B: Live Gemini AI Mode](#option-b-live-gemini-ai-mode)
  - [Option C: Local HuggingFace Transformer Mode](#option-c-local-huggingface-transformer-mode)
- [REST API Reference](#rest-api-reference)
- [Automated Testing & QA Verification](#automated-testing--qa-verification)
- [Screenshots & Visual Evidence](#screenshots--visual-evidence)
- [Video Demonstrations](#video-demonstrations)
- [Phase-Wise Deliverables](#phase-wise-deliverables)
- [Limitations & Future Roadmap](#limitations--future-roadmap)
- [License](#license)

---

## 🔍 Overview & Problem Statement

### The Problem
- **Cognitive Overload:** Students reading dense, multi-page textbooks struggle to extract core takeaways.
- **Abstract STEM Concepts:** Topics in physics, chemistry, and algorithms (e.g., Quantum Computing, Binary Search) are taught using complex jargon without relatable analogies.
- **Lack of Active Recall:** Passive reading results in low retention; students lack instant self-assessment quizzes with feedback.
- **Cloud AI Fragility:** Standard AI applications crash when API quotas or internet connectivity drop.

### The EduGenie Solution
EduGenie provides an on-demand, fault-tolerant AI study companion that combines cloud foundation models with edge determinism. It delivers 5 specialized learning tools in a modern glassmorphism single-page application.

---

## 🎯 Objectives
1. **Asynchronous Backend:** Provide high-speed REST endpoints via FastAPI and Uvicorn on port 8000.
2. **Pedagogical Simplification:** Transform abstract scientific and computing concepts into school-level explanations with intuitive analogies.
3. **Active Recall & Grading:** Synthesize 3-MCQ assessments with strict JSON validation and real-time client-side scoring.
4. **Zero-Downtime Guarantee:** Implement deterministic offline generators for full functionality in demo and fallback modes.
5. **Quality Assurance:** Validate functionality with 37 automated test cases, real Playwright screenshots, and video recordings.

---

## ✨ Key Features

| Feature | Description | Endpoint |
| :--- | :--- | :--- |
| **💬 Smart Q&A** | Instant, concise factual answers (2–4 sentences) to academic and general knowledge questions. | `GET /qa?question=` |
| **💡 Concept Explainer** | Explains complex topics with relatable analogies (e.g., spinning coins for superposition, phonebooks for binary search). Supports Cloud Gemini or Local LaMini. | `POST /explain` |
| **📝 Passage Summarizer** | Condenses lengthy textbook paragraphs into 4 high-yield bullet takeaways. | `POST /summarize` |
| **🎯 Interactive Quiz Generator** | Generates exactly 3 MCQs with 4 options each in strict JSON format. Evaluates answers with color-coded feedback and score tracking. | `POST /quiz` |
| **🗺️ Learning Roadmap** | Builds structured 3-stage curriculum guides (Beginner $\rightarrow$ Intermediate $\rightarrow$ Advanced) with timeframes and resources. | `GET /learn/recommendations` |
| **⚡ Health & Demo Mode** | Dynamic runtime mode detection (`Demo Mode` vs. `Live Gemini`) and model parameter inspection. | `GET /health` |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI (v0.110+) | Asynchronous ASGI RESTful API framework |
| **Server Engine** | Uvicorn (v0.28+) | High-concurrency ASGI server on port 8000 |
| **Frontend UI** | HTML5 • Modern CSS3 • Vanilla JS | Single-Page Application (zero bundle overhead) |
| **Cloud AI Model** | Google Gemini (`gemini-1.5-flash` / `pro`) | Cloud Generative AI reasoning via `google-genai` SDK |
| **Local AI Model** | `MBZUAI/LaMini-Flan-T5-783M` | Local CPU text-to-text generation via HuggingFace |
| **Schema Validation** | Pydantic (v2.6+) | Strict request data validation and sanitization |
| **Automated Testing** | Pytest & Pytest-Cov (v8.0+) | 37 automated tests with 80% total code coverage |
| **E2E Automation** | Playwright (Chromium) | Automated desktop (1366x768) & mobile (390x844) captures |
| **Media Encoding** | FFmpeg (v7.1+) | High-definition MP4 video transcoding and compression |

---

## 🏗️ System Architecture

```
                                  +---------------------------------------+
                                  |         Learner / Web Browser         |
                                  |    (Desktop 1366x768 / Mobile 390x844)|
                                  +-------------------+-------------------+
                                                      |
                                           HTTP / REST (JSON Payloads)
                                                      |
                                  +-------------------v-------------------+
                                  |      FastAPI ASGI Server (:8000)      |
                                  |      Pydantic Request Validation      |
                                  +---------+-------------------+---------+
                                            |                   |
                     +----------------------+                   +----------------------+
                     |                                                                 |
     +---------------v---------------+                                 +---------------v---------------+
     |      Core Feature Modules     |                                 |    System Health & Config     |
     | • qna.py          • quiz.py   |                                 | • config.py    • /health      |
     | • explanation.py  • summary.py|                                 | • Mode Resolution (Demo/Live) |
     | • learning_path.py            |                                 +-------------------------------+
     +---------------+---------------+
                     |
     +---------------+----------------------------------+
     |                                                  |
+----v--------------------+   +-------------------------v-+   +-------------------------+
|    Google Gemini API    |   |   HuggingFace Pipeline    |   | Deterministic Generator |
| (gemini-1.5-flash/pro)  |   | (LaMini-Flan-T5-783M Local|   | (Zero-Downtime Fallback)|
+-------------------------+   +---------------------------+   +-------------------------+
```

---

## 🚀 Installation & Quickstart

### Prerequisites
- Python 3.10 or higher (Tested on Python 3.10, 3.11, 3.12, 3.13)
- `pip` package manager
- Google Chrome or Chromium (for Playwright screenshots)

### 1. Clone & Install Dependencies
```bash
# Navigate to repository root
cd EduGenie

# Install required Python packages
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

---

### Option A: Offline Demo Mode (No API Key Required)
EduGenie includes deterministic offline generators that run without an API key:
```bash
# Start server in Demo Mode
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser at **`http://127.0.0.1:8000`**. The navbar will display `⚡ Demo Mode (Offline)`.

---

### Option B: Live Gemini AI Mode
To connect to live Google Gemini foundation models:
1. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```
2. Insert your Google AI Studio API key in `.env`:
```env
GEMINI_API_KEY=AIzaSy...YourKeyHere...
GEMINI_MODEL=gemini-1.5-flash
GEMINI_PRO_MODEL=gemini-1.5-pro
EXPLAIN_BACKEND=gemini
PORT=8000
```
3. Restart the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The navbar will display `✨ Live Gemini AI (gemini-1.5-flash)`.

---

### Option C: Local HuggingFace Transformer Mode
To run concept explanations using the local `MBZUAI/LaMini-Flan-T5-783M` model:
```bash
pip install transformers torch
```
Set `EXPLAIN_BACKEND=local` in `.env` or select **LaMini-Flan-T5-783M (Local)** on the Concept Explainer card.

---

## 📡 REST API Reference

| Verb | Endpoint | Parameters / Body | Sample Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | None | `{"status": "healthy", "mode": "demo", "default_model": "gemini-1.5-flash"}` |
| `GET` | `/qa` | `?question=Which is the largest ocean?` | `{"question": "...", "answer": "The Pacific Ocean...", "mode": "demo"}` |
| `POST` | `/explain` | `{"topic": "quantum computing", "backend": "gemini"}` | `{"topic": "quantum computing", "explanation": "...", "backend": "gemini"}` |
| `POST` | `/quiz` | `{"topic": "Pythagoras theorem"}` | `{"quiz": [{"question": "...", "options": [...], "answer": "..."}]}` |
| `POST` | `/summarize` | `{"text": "Industrial Revolution paragraph..."}` | `{"summary": "...", "original_length": 842, "mode": "demo"}` |
| `GET` | `/learn/recommendations` | `?topic=SQL` | `{"topic": "SQL", "recommendations": "Stage 1: Beginner...", "mode": "demo"}` |

Access interactive Swagger docs at **`http://127.0.0.1:8000/docs`**.

---

## 🧪 Automated Testing & QA Verification

EduGenie includes an automated test suite with **37 test cases** covering API routes, input sanitization, strict JSON parsing, and AI failure fallbacks.

```bash
# Run full automated test suite with coverage
pytest -v --cov=. tests/
```

### Test Results Summary
- **Total Tests Executed:** 37
- **Passed:** 37 (100% Pass Rate)
- **Failed:** 0
- **Total Codebase Coverage:** 80%
- **Execution Time:** ~0.70 seconds

All terminal outputs are preserved in `docs/evidence/` (`install.txt`, `server_start.txt`, `pytest_run.txt`, `coverage.txt`).

---

## 📸 Screenshots & Visual Evidence

| ID | Description | Preview |
| :--- | :--- | :--- |
| `01` | **Dashboard Landing State** | `docs/screenshots/01_dashboard_initial.png` |
| `02` | **Scenario 1: Smart Q&A** | `docs/screenshots/02_qa_largest_ocean.png` |
| `03` | **Scenario 2: Concept Explainer** | `docs/screenshots/03_explain_quantum_computing.png` |
| `04` | **Scenario 2b: Local Backend** | `docs/screenshots/04_explain_binary_search_local.png` |
| `05` | **Scenario 3: Text Summarizer** | `docs/screenshots/05_summarize_industrial_revolution.png` |
| `06` | **Scenario 4: Quiz Generator** | `docs/screenshots/06_quiz_pythagoras_generated.png` |
| `07` | **Scenario 4b: Grader & Score (2/3)** | `docs/screenshots/07_quiz_grading_evaluation.png` |
| `08` | **Scenario 5: Learning Roadmap** | `docs/screenshots/08_learning_path_sql.png` |
| `09` | **Validation Error Interception** | `docs/screenshots/09_validation_error_state.png` |
| `10` | **FastAPI Swagger Docs** | `docs/screenshots/10_fastapi_swagger_docs.png` |
| `11-13` | **Mobile Responsive Viewports** | `docs/screenshots/11_mobile_dashboard.png` |

Run automated screenshot capture:
```bash
python3 scripts/capture_screenshots.py
```

---

## 🎥 Video Demonstrations

1. **Demonstration Walkthrough:** `media/Demo_Video.mp4`  
   *A 3-minute high-definition video walking through all 5 scenarios with on-screen caption overlays.*
2. **Testing & Verification Walkthrough:** `media/Testing_Video.mp4`  
   *A 1-minute video showing 37 automated pytest cases passing and UI edge-case validation.*
3. **Voiceover Script:** `docs/demo_script.md`  
   *Full scene-by-scene narration text for voice-over recording.*

---

## 📁 Phase-Wise Deliverables

All phase documents are generated in standard OOXML format (`.docx`, `.xlsx`, `.pptx`) with real code metrics and screenshots:

- `Phase_Wise_Submission/01_Brainstorming_Ideation/Phase_01_Brainstorming.docx`
- `Phase_Wise_Submission/02_Requirement_Analysis/Phase_02_Requirements.docx`
- `Phase_Wise_Submission/03_Project_Design/Phase_03_Design.docx` + `diagrams/` (6 PNG diagrams)
- `Phase_Wise_Submission/04_Project_Planning/Phase_04_Planning.docx` + `Gantt_Chart.xlsx`
- `Phase_Wise_Submission/05_Project_Development/Phase_05_Development.docx`
- `Phase_Wise_Submission/06_Project_Testing/Phase_06_Testing.docx` + `Test_Cases.xlsx` + `Traceability_Matrix.xlsx`
- `Phase_Wise_Submission/07_Project_Documentation/Final_Project_Report.docx` (Complete Technical Report)
- `Phase_Wise_Submission/08_Project_Demonstration/Demo_Guide.docx` + `Final_Presentation.pptx` + `Viva_Questions.docx`

---

## ⚖️ Limitations & Future Roadmap

### Current Limitations
- **Stateless Execution:** Queries are evaluated independently without multi-turn chat memory.
- **Offline Corpus Coverage:** Offline generator provides deep coverage for curated academic topics.
- **Monolingual:** Interface and prompts are optimized for English.

### Future Enhancements
1. **Multi-turn Conversational Memory:** Add SQLite / PostgreSQL conversation persistence.
2. **Speech Integration:** Add Whisper STT voice input and Bark/Kokoro TTS audio explanations.
3. **PDF Syllabus Upload:** Enable students to upload textbooks and generate custom test papers.
4. **Multilingual Support:** Add localization for Spanish, Hindi, French, and Mandarin.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
