"""
EduGenie Configuration Module
Manages API keys, model selections, runtime modes, and fallbacks.
"""

import os
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("EduGenie.Config")

# Environment Variables & Settings
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", os.getenv("GEMINI_FLASH_MODEL", "gemini-1.5-flash")).strip()
GEMINI_PRO_MODEL: str = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro").strip()
EXPLAIN_BACKEND: str = os.getenv("EXPLAIN_BACKEND", "gemini").strip().lower()
LOCAL_MODEL_NAME: str = os.getenv("LOCAL_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M").strip()
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))

# Determine if running in Demo Mode
PLACEHOLDER_KEYS = ["", "your_api_key_here", "YOUR_GEMINI_API_KEY", "placeholder", "demo"]
IS_DEMO_MODE: bool = (GEMINI_API_KEY == "" or GEMINI_API_KEY in PLACEHOLDER_KEYS or len(GEMINI_API_KEY) < 10)

if IS_DEMO_MODE:
    logger.info("⚡ Running in DEMO MODE (Offline Deterministic AI Generators active)")
else:
    logger.info(f"✨ Running in LIVE MODE (Gemini API configured with model: {GEMINI_MODEL})")

# Cache for Gemini client to prevent multiple instantiations
_gemini_client = None

def get_gemini_client():
    """
    Returns an initialized Gemini client if API key is present and SDK is available.
    Supports both google-genai and google.generativeai gracefully.
    """
    global _gemini_client
    if IS_DEMO_MODE:
        return None

    if _gemini_client is not None:
        return _gemini_client

    try:
        # First try modern google-genai SDK
        from google import genai
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("Initialized Google GenAI client successfully.")
        return _gemini_client
    except Exception as e:
        logger.warning(f"Failed to initialize google-genai Client: {e}. Attempting fallback wrapper.")
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=GEMINI_API_KEY)
            _gemini_client = legacy_genai
            logger.info("Initialized google.generativeai legacy client successfully.")
            return _gemini_client
        except Exception as e2:
            logger.error(f"Could not initialize any Gemini SDK: {e2}")
            return None

def get_app_status() -> Dict[str, Any]:
    """Returns application health and configuration metadata."""
    return {
        "status": "healthy",
        "app_name": "EduGenie",
        "version": "1.0.0",
        "mode": "demo" if IS_DEMO_MODE else "live",
        "is_demo_mode": IS_DEMO_MODE,
        "default_model": GEMINI_MODEL,
        "pro_model": GEMINI_PRO_MODEL,
        "explain_backend": EXPLAIN_BACKEND,
        "local_model_name": LOCAL_MODEL_NAME,
        "host": HOST,
        "port": PORT
    }
