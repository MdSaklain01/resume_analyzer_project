from fastapi.testclient import TestClient

from resume_ai_api.main import app


client = TestClient(app)


def test_health_ready() -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_analyze_resume() -> None:
    response = client.post(
        "/api/v1/analyze",
        json={
            "role_title": "Backend Developer",
            "resume_text": (
                "Python developer built FastAPI REST API projects with Docker, Redis, "
                "PostgreSQL, AWS EKS, Terraform, Argo CD, GitHub Actions CI/CD, Prometheus and Grafana."
            ),
            "job_description": (
                "We need a backend developer with Python, FastAPI, Docker, AWS EKS, Redis, "
                "Terraform, Argo CD, CI/CD, REST API, monitoring, Prometheus and Grafana experience."
            ),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["score"] >= 70
    assert "python" in body["matched_keywords"]


def test_chatbot_answers_api_question() -> None:
    response = client.post("/api/v1/chat", json={"message": "What is FastAPI?"})

    assert response.status_code == 200
    assert "FastAPI" in response.json()["answer"]


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "resume_ai_http_requests_total" in response.text
