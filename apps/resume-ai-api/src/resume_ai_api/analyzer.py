from __future__ import annotations

import re
from collections import Counter

from resume_ai_api.schemas import AnalyzeResponse, SkillMatch


COMMON_SKILLS = [
    "python",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "ec2",
    "s3",
    "lambda",
    "git",
    "github actions",
    "ci/cd",
    "rest api",
    "machine learning",
    "nlp",
    "pandas",
    "react",
    "typescript",
    "javascript",
    "linux",
    "nginx",
    "prometheus",
    "grafana",
]

STOP_WORDS = {
    "and",
    "the",
    "with",
    "for",
    "you",
    "your",
    "are",
    "that",
    "this",
    "will",
    "from",
    "have",
    "has",
    "our",
    "using",
    "work",
    "team",
    "role",
    "experience",
    "candidate",
    "skills",
    "ability",
    "must",
    "should",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9+#./-]{2,}", normalize(text))


def top_keywords(text: str, limit: int = 24) -> list[str]:
    words = [word for word in tokenize(text) if word not in STOP_WORDS]
    counts = Counter(words)
    return [word for word, _ in counts.most_common(limit)]


def sentence_count(text: str) -> int:
    return len([part for part in re.split(r"[.!?]+", text) if part.strip()])


def analyze_resume(resume_text: str, job_description: str, role_title: str | None = None) -> AnalyzeResponse:
    resume = normalize(resume_text)
    job = normalize(job_description)

    job_keywords = top_keywords(job)
    matched_keywords = sorted({keyword for keyword in job_keywords if keyword in resume})
    missing_keywords = sorted({keyword for keyword in job_keywords if keyword not in resume})[:12]

    relevant_skills = [skill for skill in COMMON_SKILLS if skill in job or skill in resume]
    skill_matches = [
        SkillMatch(skill=skill, found_in_resume=skill in resume)
        for skill in relevant_skills[:18]
    ]

    keyword_score = 0 if not job_keywords else int((len(matched_keywords) / len(job_keywords)) * 55)
    skill_score = 0
    if skill_matches:
        skill_score = int(
            (sum(1 for skill in skill_matches if skill.found_in_resume) / len(skill_matches)) * 25
        )
    structure_score = 0
    if len(resume_text) > 800:
        structure_score += 8
    if sentence_count(resume_text) >= 6:
        structure_score += 6
    if any(marker in resume for marker in ["project", "built", "created", "developed", "deployed"]):
        structure_score += 6

    score = min(100, keyword_score + skill_score + structure_score)
    verdict = build_verdict(score)
    strengths = build_strengths(score, matched_keywords, skill_matches)
    improvements = build_improvements(missing_keywords, skill_matches)
    suggested_summary = build_summary(role_title, matched_keywords, skill_matches)

    return AnalyzeResponse(
        score=score,
        verdict=verdict,
        matched_keywords=matched_keywords[:12],
        missing_keywords=missing_keywords,
        skill_matches=skill_matches,
        strengths=strengths,
        improvements=improvements,
        suggested_summary=suggested_summary,
    )


def build_verdict(score: int) -> str:
    if score >= 80:
        return "Strong match. Your resume is closely aligned with the job description."
    if score >= 60:
        return "Good match. Add a few missing keywords and clearer project impact."
    if score >= 40:
        return "Partial match. The resume needs stronger alignment with this role."
    return "Weak match. Rewrite the resume around the target job requirements."


def build_strengths(
    score: int,
    matched_keywords: list[str],
    skill_matches: list[SkillMatch],
) -> list[str]:
    strengths: list[str] = []
    found_skills = [skill.skill for skill in skill_matches if skill.found_in_resume]
    if matched_keywords:
        strengths.append(f"Your resume already includes relevant terms like {', '.join(matched_keywords[:5])}.")
    if found_skills:
        strengths.append(f"Technical skills detected: {', '.join(found_skills[:6])}.")
    if score >= 70:
        strengths.append("The resume has enough role-specific language to pass an initial screening.")
    return strengths or ["The resume has enough text to start improving it for this role."]


def build_improvements(missing_keywords: list[str], skill_matches: list[SkillMatch]) -> list[str]:
    improvements: list[str] = []
    missing_skills = [skill.skill for skill in skill_matches if not skill.found_in_resume]
    if missing_keywords:
        improvements.append(f"Add honest examples for missing keywords: {', '.join(missing_keywords[:6])}.")
    if missing_skills:
        improvements.append(f"Mention these skills if you have used them: {', '.join(missing_skills[:6])}.")
    improvements.append("Use bullet points with action, tool, result. Example: Built X with Y, improving Z.")
    improvements.append("Add numbers where possible, such as users, latency, cost, accuracy, or time saved.")
    return improvements


def build_summary(
    role_title: str | None,
    matched_keywords: list[str],
    skill_matches: list[SkillMatch],
) -> str:
    role = role_title or "software role"
    skills = [skill.skill for skill in skill_matches if skill.found_in_resume]
    highlights = skills[:4] or matched_keywords[:4] or ["problem solving", "project delivery"]
    return (
        f"Motivated candidate targeting a {role}, with hands-on experience in "
        f"{', '.join(highlights)}. Comfortable building practical solutions, learning quickly, "
        "and improving applications through clean implementation and measurable results."
    )

