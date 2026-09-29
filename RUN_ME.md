# 🚀 EduGenie — Quick Execution & Verification Guide

This guide provides the exact single-run commands to install, run, test, capture screenshots, and generate all deliverables for **EduGenie**.

---

## ⚡ 1. Complete One-Shot Setup & Run

```bash
# 1. Navigate to project root
cd /home/user/EduGenie

# 2. Install all Python dependencies
pip install -r requirements.txt

# 3. Install Playwright browser binaries and system libraries
playwright install chromium
playwright install-deps

# 4. Start FastAPI server in background (or separate terminal)
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# 5. Verify server is healthy
curl -s http://127.0.0.1:8000/health
```

---

## 🧪 2. Run Automated Pytest Suite

```bash
cd /home/user/EduGenie
pytest -v --cov=. tests/
```
*Expected Output: 37 passed, 100% pass rate, 80% coverage in ~0.70s.*

---

## 📸 3. Capture Real Automated Screenshots

```bash
python3 /home/user/EduGenie/scripts/capture_screenshots.py
```
*Generates 13 real screenshots (10 desktop + 3 mobile) and `docs/screenshots/captions.json`.*

---

## 🎥 4. Record Demo & Testing Videos

```bash
# Record 3-minute Demo Video with on-screen captions
python3 /home/user/EduGenie/scripts/record_demo.py

# Record 1-minute Testing & Verification Video
python3 /home/user/EduGenie/scripts/record_testing.py
```
*Outputs `media/Demo_Video.mp4` and `media/Testing_Video.mp4`.*

---

## 📊 5. Generate Diagrams, Spreadsheets & Phase Docs

```bash
# Generate 6 design diagrams (PNG)
python3 /home/user/EduGenie/scripts/generate_diagrams.py

# Generate Gantt Chart, Test Cases, Traceability Matrix & PowerPoint presentation
python3 /home/user/EduGenie/scripts/generate_excel_pptx.py

# Generate Phase Word documents (Phases 1 to 6, Demo Guide, Viva Questions)
python3 /home/user/EduGenie/scripts/generate_all_phases.py

# Generate Complete Final Project Report (15-25 pages)
python3 /home/user/EduGenie/scripts/generate_final_report.py
```

---

## 📦 6. Package Repository as Zip

```bash
cd /home/user
zip -r EduGenie.zip EduGenie/ -x "EduGenie/__pycache__/*" "EduGenie/*/__pycache__/*" "EduGenie/.pytest_cache/*"
```
