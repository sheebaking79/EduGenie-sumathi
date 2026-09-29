"""
Automated Screenshot Capture Script for EduGenie
Uses Playwright (Chromium) to execute all scenarios, capture real desktop and mobile screenshots,
and generate captions.json.
"""

import os
import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

CAPTIONS = {}

def capture_all():
    print(f"Starting automated screenshot capture targeting {BASE_URL}...")
    with sync_playwright() as p:
        # 1. Desktop Browser (1366x768)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1366, "height": 768})
        page = context.new_page()

        # Shot 01: Landing Dashboard Initial State
        page.goto(BASE_URL)
        page.wait_for_selector(".navbar")
        time.sleep(1)
        shot_01 = os.path.join(OUTPUT_DIR, "01_dashboard_initial.png")
        page.screenshot(path=shot_01, full_page=False)
        CAPTIONS["01_dashboard_initial.png"] = "EduGenie web dashboard landing state with demo mode badge and five educational feature cards."
        print("Captured 01_dashboard_initial.png")

        # Shot 02: Scenario 1 - Ask "Which is the largest ocean?"
        page.fill("#qa-input", "Which is the largest ocean?")
        page.click("#btn-qa-submit")
        page.wait_for_selector("#result-qa", state="visible")
        time.sleep(0.5)
        # Scroll card into view
        page.locator("#card-qa").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_02 = os.path.join(OUTPUT_DIR, "02_qa_largest_ocean.png")
        page.screenshot(path=shot_02, full_page=False)
        CAPTIONS["02_qa_largest_ocean.png"] = "Smart Q&A response for 'Which is the largest ocean?' providing concise factual answer regarding the Pacific Ocean."
        print("Captured 02_qa_largest_ocean.png")

        # Shot 03: Scenario 2 - Explain "quantum computing"
        page.fill("#explain-input", "quantum computing")
        page.click('input[name="explain-backend"][value="gemini"]')
        page.click("#btn-explain-submit")
        page.wait_for_selector("#result-explain", state="visible")
        time.sleep(0.5)
        page.locator("#card-explain").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_03 = os.path.join(OUTPUT_DIR, "03_explain_quantum_computing.png")
        page.screenshot(path=shot_03, full_page=False)
        CAPTIONS["03_explain_quantum_computing.png"] = "Concept Explainer simplifying Quantum Computing using Qubit analogies and school-level definitions via Gemini backend."
        print("Captured 03_explain_quantum_computing.png")

        # Shot 04: Scenario 2b - Explain "binary search algorithm" with Local Backend
        page.fill("#explain-input", "binary search algorithm")
        page.click('input[name="explain-backend"][value="local"]')
        page.click("#btn-explain-submit")
        page.wait_for_selector("#result-explain", state="visible")
        time.sleep(0.5)
        page.locator("#card-explain").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_04 = os.path.join(OUTPUT_DIR, "04_explain_binary_search_local.png")
        page.screenshot(path=shot_04, full_page=False)
        CAPTIONS["04_explain_binary_search_local.png"] = "Concept Explainer for 'binary search algorithm' with telephone directory analogy and O(log n) analysis via Local LaMini-Flan-T5 option."
        print("Captured 04_explain_binary_search_local.png")

        # Shot 05: Scenario 3 - Summarize Industrial Revolution Paragraph
        page.click("#btn-sample-revolution")
        time.sleep(0.5)
        page.click("#btn-summarize-submit")
        page.wait_for_selector("#result-summarize", state="visible")
        time.sleep(0.5)
        page.locator("#card-summarize").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_05 = os.path.join(OUTPUT_DIR, "05_summarize_industrial_revolution.png")
        page.screenshot(path=shot_05, full_page=False)
        CAPTIONS["05_summarize_industrial_revolution.png"] = "Text Summarizer condensing Industrial Revolution textbook passage into bulleted study notes."
        print("Captured 05_summarize_industrial_revolution.png")

        # Shot 06: Scenario 4 - Generate Quiz on "Pythagoras theorem"
        page.fill("#quiz-input", "Pythagoras theorem")
        page.click("#btn-quiz-submit")
        page.wait_for_selector("#result-quiz", state="visible")
        page.wait_for_selector("#q-card-0", state="visible")
        time.sleep(0.5)
        page.locator("#card-quiz").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_06 = os.path.join(OUTPUT_DIR, "06_quiz_pythagoras_generated.png")
        page.screenshot(path=shot_06, full_page=False)
        CAPTIONS["06_quiz_pythagoras_generated.png"] = "Interactive Quiz Generator displaying 3 structured MCQs on Pythagoras theorem with 4 options each."
        print("Captured 06_quiz_pythagoras_generated.png")

        # Shot 07: Scenario 4b - Answer 1 Wrong and 2 Right on Pythagoras Quiz
        # Q0: Right answer is "a² + b² = c²" -> select option 0
        page.click('#opt-label-0-0')
        # Q1: Right answer is "Right-angled triangle" -> let's intentionally choose WRONG "Equilateral triangle" (opt-label-1-0)
        page.click('#opt-label-1-0')
        # Q2: Right answer is "5 cm" -> select option 0
        page.click('#opt-label-2-0')
        time.sleep(0.5)
        page.click("#btn-submit-all-quiz")
        time.sleep(0.8)
        page.locator("#card-quiz").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_07 = os.path.join(OUTPUT_DIR, "07_quiz_grading_evaluation.png")
        page.screenshot(path=shot_07, full_page=False)
        CAPTIONS["07_quiz_grading_evaluation.png"] = "Quiz grading evaluation showing 2 Correct (green) and 1 Incorrect (red) with score banner 2/3 (66.7%)."
        print("Captured 07_quiz_grading_evaluation.png")

        # Shot 08: Scenario 5 - Learning Path for "SQL"
        page.fill("#learn-input", "SQL")
        page.click("#btn-learn-submit")
        page.wait_for_selector("#result-learn", state="visible")
        time.sleep(0.5)
        page.locator("#card-learn").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_08 = os.path.join(OUTPUT_DIR, "08_learning_path_sql.png")
        page.screenshot(path=shot_08, full_page=False)
        CAPTIONS["08_learning_path_sql.png"] = "Personalized Learning Roadmap for SQL showing 3 structured stages (Beginner to Advanced) with time estimates."
        print("Captured 08_learning_path_sql.png")

        # Shot 09: Input Validation & Error Handling
        page.fill("#qa-input", "")
        page.click("#btn-qa-submit")
        time.sleep(0.5)
        page.locator("#card-qa").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_09 = os.path.join(OUTPUT_DIR, "09_validation_error_state.png")
        page.screenshot(path=shot_09, full_page=False)
        CAPTIONS["09_validation_error_state.png"] = "Input validation and error handling displaying helpful user error notification on empty submission."
        print("Captured 09_validation_error_state.png")

        # Shot 10: OpenAPI / Swagger Documentation
        page.goto(f"{BASE_URL}/docs")
        page.wait_for_selector(".swagger-ui")
        time.sleep(1)
        shot_10 = os.path.join(OUTPUT_DIR, "10_fastapi_swagger_docs.png")
        page.screenshot(path=shot_10, full_page=False)
        CAPTIONS["10_fastapi_swagger_docs.png"] = "FastAPI interactive OpenAPI Swagger documentation for all 5 EduGenie endpoints and /health."
        print("Captured 10_fastapi_swagger_docs.png")

        browser.close()

        # 2. Mobile Browser (390x844 iPhone 14 Viewport)
        mobile_browser = p.chromium.launch(headless=True)
        mobile_context = mobile_browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        )
        mobile_page = mobile_context.new_page()

        # Mobile Shot 1: Mobile Dashboard Landing
        mobile_page.goto(BASE_URL)
        mobile_page.wait_for_selector(".navbar")
        time.sleep(1)
        shot_m1 = os.path.join(OUTPUT_DIR, "11_mobile_dashboard.png")
        mobile_page.screenshot(path=shot_m1, full_page=False)
        CAPTIONS["11_mobile_dashboard.png"] = "Mobile responsive view (390x844) showing EduGenie responsive header and navigation."
        print("Captured 11_mobile_dashboard.png")

        # Mobile Shot 2: Mobile Quiz with Live Grading
        mobile_page.fill("#quiz-input", "Pythagoras theorem")
        mobile_page.click("#btn-quiz-submit")
        mobile_page.wait_for_selector("#result-quiz", state="visible")
        time.sleep(0.5)
        mobile_page.click('#opt-label-0-0')
        mobile_page.click('#opt-label-1-0')
        mobile_page.click('#opt-label-2-0')
        mobile_page.click("#btn-submit-all-quiz")
        time.sleep(0.5)
        mobile_page.locator("#card-quiz").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_m2 = os.path.join(OUTPUT_DIR, "12_mobile_quiz_evaluated.png")
        mobile_page.screenshot(path=shot_m2, full_page=False)
        CAPTIONS["12_mobile_quiz_evaluated.png"] = "Mobile view (390x844) of interactive quiz assessment with instant grading and score tracking."
        print("Captured 12_mobile_quiz_evaluated.png")

        # Mobile Shot 3: Mobile Learning Path
        mobile_page.fill("#learn-input", "SQL")
        mobile_page.click("#btn-learn-submit")
        mobile_page.wait_for_selector("#result-learn", state="visible")
        time.sleep(0.5)
        mobile_page.locator("#card-learn").scroll_into_view_if_needed()
        time.sleep(0.5)
        shot_m3 = os.path.join(OUTPUT_DIR, "13_mobile_learning_path.png")
        mobile_page.screenshot(path=shot_m3, full_page=False)
        CAPTIONS["13_mobile_learning_path.png"] = "Mobile view (390x844) displaying personalized learning roadmap for SQL."
        print("Captured 13_mobile_learning_path.png")

        mobile_browser.close()

    # Save captions.json
    captions_path = os.path.join(OUTPUT_DIR, "captions.json")
    with open(captions_path, "w", encoding="utf-8") as f:
        json.dump(CAPTIONS, f, indent=2)
    print(f"Saved all captions to {captions_path}")
    print("Screenshot capture successfully completed!")

if __name__ == "__main__":
    capture_all()
