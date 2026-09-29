"""
EduGenie Quiz Generation Module
Generates exactly 3 MCQs with 4 options each in strict JSON format.
Validates that the answer string exactly matches one of the 4 options.
"""

import json
import logging
import re
from typing import Dict, Any, List
from config import IS_DEMO_MODE, GEMINI_MODEL, get_gemini_client
from demo_generator import generate_demo_quiz

logger = logging.getLogger("EduGenie.Quiz")

def clean_json_block(text: str) -> str:
    """
    Strips Markdown code fences (e.g. ```json ... ```) and leading/trailing whitespace.
    """
    cleaned = text.strip()
    # Match ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        cleaned = match.group(1).strip()
    return cleaned

def validate_quiz_data(quiz_data: Any) -> bool:
    """
    Validates that quiz_data is a list of exactly 3 questions,
    each with a non-empty question, exactly 4 unique options,
    and an answer that matches one of the options.
    """
    if not isinstance(quiz_data, list) or len(quiz_data) != 3:
        return False

    for item in quiz_data:
        if not isinstance(item, dict):
            return False
        if "question" not in item or not isinstance(item["question"], str) or not item["question"].strip():
            return False
        if "options" not in item or not isinstance(item["options"], list) or len(item["options"]) != 4:
            return False
        if not all(isinstance(opt, str) and opt.strip() for opt in item["options"]):
            return False
        if "answer" not in item or not isinstance(item["answer"], str):
            return False
        # Ensure answer is in options
        if item["answer"].strip() not in [opt.strip() for opt in item["options"]]:
            return False

    return True

def generate_quiz(text_or_topic: str) -> Dict[str, Any]:
    """
    Generates 3 multiple-choice questions for a given text or topic.
    Returns structured quiz items with options and answers.
    """
    cleaned_input = text_or_topic.strip()
    if not cleaned_input:
        raise ValueError("Quiz topic or passage cannot be empty.")

    if IS_DEMO_MODE:
        logger.info(f"[Demo Mode] Generating quiz for: '{cleaned_input[:50]}'")
        quiz = generate_demo_quiz(cleaned_input)
        return {
            "topic_or_text": cleaned_input,
            "quiz": quiz,
            "mode": "demo",
            "model": "offline-deterministic"
        }

    client = get_gemini_client()
    if not client:
        logger.warning("[Fallback] Gemini client unavailable. Using offline quiz.")
        quiz = generate_demo_quiz(cleaned_input)
        return {
            "topic_or_text": cleaned_input,
            "quiz": quiz,
            "mode": "fallback",
            "model": "offline-deterministic"
        }

    prompt = (
        "You are an educational assessment creator. Generate exactly 3 multiple choice questions (MCQs) "
        f"based on the following topic or passage:\n\n{cleaned_input}\n\n"
        "RULES:\n"
        "1. Return ONLY valid raw JSON array containing exactly 3 question objects.\n"
        "2. Each object must have keys: 'question' (string), 'options' (list of 4 distinct strings), and 'answer' (string).\n"
        "3. CRITICAL: The 'answer' field MUST BE THE EXACT STRING OF ONE OF THE OPTIONS, not a letter or index.\n"
        "4. Do not include any explanations or text outside the JSON array.\n\n"
        "Example format:\n"
        "[\n"
        "  {\n"
        '    "question": "What is 2 + 2?",\n'
        '    "options": ["3", "4", "5", "6"],\n'
        '    "answer": "4"\n'
        "  }\n"
        "]"
    )

    for attempt in range(2):
        try:
            if hasattr(client, "models") and hasattr(client.models, "generate_content"):
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )
                raw_text = response.text if hasattr(response, "text") else str(response)
            else:
                model = client.GenerativeModel(GEMINI_MODEL)
                response = model.generate_content(prompt)
                raw_text = response.text

            json_str = clean_json_block(raw_text)
            quiz_data = json.loads(json_str)

            if validate_quiz_data(quiz_data):
                return {
                    "topic_or_text": cleaned_input,
                    "quiz": quiz_data,
                    "mode": "live",
                    "model": GEMINI_MODEL
                }
            else:
                logger.warning(f"Attempt {attempt + 1}: Quiz validation failed for generated JSON.")
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}: Quiz JSON parse error: {e}")

    logger.warning("Quiz generation failed after 2 attempts. Falling back to deterministic generator.")
    fallback_quiz = generate_demo_quiz(cleaned_input)
    return {
        "topic_or_text": cleaned_input,
        "quiz": fallback_quiz,
        "mode": "fallback",
        "model": "offline-deterministic",
        "fallback_notice": "Live model generated invalid JSON schema. Switched to verified offline quiz."
    }
