from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from resume_ai_api.analyzer import analyze_resume
from resume_ai_api.cache import cache, cache_key
from resume_ai_api.chatbot import answer_question
from resume_ai_api.metrics import MetricsMiddleware, prometheus_response
from resume_ai_api.schemas import AnalyzeRequest, AnalyzeResponse, ChatRequest, ChatResponse
from resume_ai_api.settings import settings


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="FastAPI backend for resume analysis and beginner-friendly AI chatbot help.",
)
app.add_middleware(MetricsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "AI Resume Analyzer API is running",
        "docs": "/docs",
        "health": "/health/ready",
    }


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "environment": settings.environment}


@app.get("/metrics")
def metrics():
    return prometheus_response()


@app.post(f"{settings.api_prefix}/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    key = cache_key("analysis", payload.resume_text, payload.job_description, payload.role_title or "")
    cached = cache.get_json(key)
    if cached:
        return AnalyzeResponse.model_validate(cached)

    result = analyze_resume(payload.resume_text, payload.job_description, payload.role_title)
    cache.set_json(key, result.model_dump())
    return result


@app.post(f"{settings.api_prefix}/analyze/file", response_model=AnalyzeResponse)
async def analyze_file(
    job_description: str = Form(...),
    role_title: str | None = Form(default=None),
    file: UploadFile = File(...),
) -> AnalyzeResponse:
    raw = await file.read()
    try:
        resume_text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Please upload a plain .txt resume for this starter project.",
        ) from exc

    payload = AnalyzeRequest(
        resume_text=resume_text,
        job_description=job_description,
        role_title=role_title,
    )
    return analyze(payload)


@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    answer, next_steps = answer_question(
        payload.message,
        payload.resume_text,
        payload.job_description,
    )
    return ChatResponse(answer=answer, suggested_next_steps=next_steps)

