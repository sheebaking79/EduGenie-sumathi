"""
EduGenie FastAPI Main Application
Exposes RESTful endpoints for Question Answering, Concept Explanations,
Quiz Generation, Text Summarization, and Learning Recommendations.
"""

import os
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, Query, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from config import get_app_status, HOST, PORT, IS_DEMO_MODE
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

logger = logging.getLogger("EduGenie.App")

app = FastAPI(
    title="EduGenie API",
    description="Google Gemini Powered AI Learning Assistant with Deterministic Fallbacks and Local Inference Options",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths for Templates and Static Files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# Pydantic Request Models
class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500, description="Topic to explain")
    backend: Optional[str] = Field(default="gemini", description="AI backend ('gemini' or 'local')")

    @field_validator("topic")
    def topic_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Topic cannot be empty or whitespace only.")
        return v.strip()


class QuizRequest(BaseModel):
    text: Optional[str] = Field(default=None, description="Passage or topic for quiz")
    topic: Optional[str] = Field(default=None, description="Alternative topic key")

    @field_validator("text", "topic")
    def check_non_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Provided text/topic cannot be whitespace only.")
        return v.strip() if v is not None else None


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Text passage to summarize")

    @field_validator("text")
    def text_not_empty(cls, v):
        if not v or not v.strip() or len(v.strip()) < 5:
            raise ValueError("Passage to summarize must be at least 5 characters.")
        return v.strip()


# Routes

@app.get("/", response_class=HTMLResponse, summary="EduGenie Single Page Application")
async def render_ui(request: Request):
    """Renders the EduGenie interactive web dashboard."""
    status_info = get_app_status()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "status": status_info,
            "is_demo_mode": status_info["is_demo_mode"]
        }
    )


@app.get("/health", summary="System Health & Mode Check")
async def health_check():
    """Returns application status, active runtime mode, and model configurations."""
    return JSONResponse(content=get_app_status(), status_code=status.HTTP_200_OK)


@app.get("/qa", summary="Smart Question Answering")
async def handle_qa(question: str = Query(..., min_length=1, description="Question to answer")):
    """
    Answers a general knowledge or academic question concisely.
    """
    cleaned_q = question.strip()
    if not cleaned_q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question query parameter cannot be empty."
        )
    try:
        result = answer_question(cleaned_q)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in /qa: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/explain", summary="Concept Simplification")
async def handle_explain(payload: ExplainRequest):
    """
    Explains complex topics in student-friendly language with analogies.
    """
    try:
        result = explain_topic(payload.topic, backend=payload.backend)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in /explain: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/quiz", summary="Interactive Quiz Generator")
async def handle_quiz(payload: QuizRequest):
    """
    Generates 3 multiple-choice questions (4 options each) from a passage or topic.
    """
    input_content = payload.text or payload.topic
    if not input_content or not input_content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'text' or 'topic' must be provided and non-empty."
        )
    try:
        result = generate_quiz(input_content)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in /quiz: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/summarize", summary="Text Summarizer")
async def handle_summarize(payload: SummarizeRequest):
    """
    Summarizes long educational text into key takeaways and bullet points.
    """
    try:
        result = summarize_text(payload.text)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in /summarize: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/learn/recommendations", summary="Personalized Learning Path")
async def handle_learning_recommendations(topic: str = Query(..., min_length=1, description="Subject or Topic")):
    """
    Returns a structured learning roadmap from beginner to advanced with time estimates and resources.
    """
    cleaned_t = topic.strip()
    if not cleaned_t:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic query parameter cannot be empty."
        )
    try:
        result = get_learning_recommendations(cleaned_t)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in /learn/recommendations: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
