from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=30, description="Plain text copied from a resume.")
    job_description: str = Field(..., min_length=30, description="Target job description.")
    role_title: str | None = Field(default=None, description="Optional role name.")


class SkillMatch(BaseModel):
    skill: str
    found_in_resume: bool


class AnalyzeResponse(BaseModel):
    score: int
    verdict: str
    matched_keywords: list[str]
    missing_keywords: list[str]
    skill_matches: list[SkillMatch]
    strengths: list[str]
    improvements: list[str]
    suggested_summary: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2)
    resume_text: str | None = None
    job_description: str | None = None


class ChatResponse(BaseModel):
    answer: str
    suggested_next_steps: list[str]

