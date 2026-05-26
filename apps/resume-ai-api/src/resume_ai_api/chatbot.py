from __future__ import annotations

from resume_ai_api.analyzer import analyze_resume


def answer_question(message: str, resume_text: str | None, job_description: str | None) -> tuple[str, list[str]]:
    question = message.lower()

    if resume_text and job_description:
        analysis = analyze_resume(resume_text, job_description)
        if "score" in question or "match" in question:
            return (
                f"Your current match score is {analysis.score}/100. {analysis.verdict}",
                analysis.improvements[:3],
            )
        if "missing" in question or "keyword" in question:
            missing = ", ".join(analysis.missing_keywords[:8]) or "no major missing keywords"
            return (
                f"The most important missing keywords are: {missing}. Only add them if they are true.",
                analysis.improvements[:3],
            )
        if "summary" in question:
            return analysis.suggested_summary, ["Place this near the top of your resume.", "Customize it per job."]

    if "fastapi" in question or "api" in question:
        return (
            "FastAPI is the Python web framework used here. A route like POST /api/v1/analyze "
            "receives resume text, runs the analyzer, and returns JSON to the frontend or user.",
            ["Open /docs locally to try the API.", "Read docs/beginner-guide.md for the request flow."],
        )

    if "docker" in question:
        return (
            "Docker packages the app and its dependencies into a container so it runs the same locally, "
            "in staging, and on AWS EKS.",
            ["Run docker compose up --build locally.", "Use the Terraform EKS guide for production."],
        )

    return (
        "I can help improve your resume for a job. Ask about match score, missing keywords, summary, "
        "projects, Docker, FastAPI, or AWS deployment.",
        ["Send resume_text and job_description for personalized advice.", "Try POST /api/v1/analyze first."],
    )
