"""
EduGenie Explanation Module
Explains complex academic and technical concepts simply for school students.
Supports EXPLAIN_BACKEND=gemini or EXPLAIN_BACKEND=local (LaMini-Flan-T5-783M).
"""

import logging
from typing import Dict, Any, Optional
from config import IS_DEMO_MODE, GEMINI_MODEL, EXPLAIN_BACKEND, LOCAL_MODEL_NAME, get_gemini_client
from demo_generator import generate_demo_explanation

logger = logging.getLogger("EduGenie.Explanation")

# Cache for local pipeline if loaded
_local_pipeline = None

def _get_local_pipeline():
    """Attempts to load local huggingface pipeline if installed."""
    global _local_pipeline
    if _local_pipeline is not None:
        return _local_pipeline

    try:
        from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
        logger.info(f"Loading local model '{LOCAL_MODEL_NAME}' on CPU...")
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_MODEL_NAME)
        _local_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
        return _local_pipeline
    except Exception as e:
        logger.warning(f"Local model '{LOCAL_MODEL_NAME}' could not be loaded ({e}). Falling back to generator.")
        return None

def explain_topic(topic: str, backend: Optional[str] = None) -> Dict[str, Any]:
    """
    Explains a concept simply for school students.
    Selects backend based on parameter or environment config.
    """
    cleaned_topic = topic.strip()
    if not cleaned_topic:
        raise ValueError("Topic cannot be empty.")

    resolved_backend = (backend or EXPLAIN_BACKEND).strip().lower()

    # Local HuggingFace backend option
    if resolved_backend == "local":
        logger.info(f"Running explanation via LOCAL backend for topic: '{cleaned_topic}'")
        pipe = _get_local_pipeline()
        if pipe:
            try:
                prompt = f"Explain the concept of {cleaned_topic} simply for a school student with analogies:"
                res = pipe(prompt)
                generated_text = res[0]["generated_text"] if res else ""
                return {
                    "topic": cleaned_topic,
                    "explanation": generated_text,
                    "backend": "local",
                    "model": LOCAL_MODEL_NAME,
                    "mode": "live-local"
                }
            except Exception as e:
                logger.error(f"Error during local inference: {e}")
        
        # If local inference or download fails, deterministic fallback
        exp = generate_demo_explanation(cleaned_topic, backend="local")
        return {
            "topic": cleaned_topic,
            "explanation": exp,
            "backend": "local",
            "model": f"{LOCAL_MODEL_NAME} (Offline Fallback)",
            "mode": "fallback",
            "fallback_notice": "Local PyTorch model not downloaded in sandbox. Using offline generator."
        }

    # Gemini backend
    if IS_DEMO_MODE:
        logger.info(f"[Demo Mode] Explaining topic: '{cleaned_topic}'")
        exp = generate_demo_explanation(cleaned_topic, backend="gemini")
        return {
            "topic": cleaned_topic,
            "explanation": exp,
            "backend": "gemini",
            "mode": "demo",
            "model": "offline-deterministic"
        }

    client = get_gemini_client()
    if not client:
        logger.warning("[Fallback] Gemini client unavailable. Using offline explanation.")
        exp = generate_demo_explanation(cleaned_topic, backend="gemini")
        return {
            "topic": cleaned_topic,
            "explanation": exp,
            "backend": "gemini",
            "mode": "fallback",
            "model": "offline-deterministic"
        }

    prompt = (
        "You are an inspiring, friendly teacher explaining concepts to a school student. "
        f"Explain '{cleaned_topic}' in simple, engaging language. "
        "Include:\n"
        "1. What is it? (Simple definition)\n"
        "2. A relatable real-world analogy\n"
        "3. Step-by-step how it works\n"
        "4. Why it matters in the real world\n"
        "Format with clear Markdown headings and bullet points."
    )

    try:
        if hasattr(client, "models") and hasattr(client.models, "generate_content"):
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            explanation_text = response.text if hasattr(response, "text") else str(response)
        else:
            model = client.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(prompt)
            explanation_text = response.text

        return {
            "topic": cleaned_topic,
            "explanation": explanation_text.strip(),
            "backend": "gemini",
            "mode": "live",
            "model": GEMINI_MODEL
        }
    except Exception as e:
        logger.error(f"Gemini API error during explanation: {e}. Falling back.")
        exp = generate_demo_explanation(cleaned_topic, backend="gemini")
        return {
            "topic": cleaned_topic,
            "explanation": exp,
            "backend": "gemini",
            "mode": "fallback",
            "model": "offline-deterministic",
            "fallback_notice": f"Live API unavailable ({str(e)[:50]}...). Switched to offline response."
        }
