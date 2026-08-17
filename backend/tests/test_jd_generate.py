from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "job_title": "Backend Developer",
    "experience_required": "2-3 years",
    "required_skills": ["Python", "FastAPI", "PostgreSQL", "REST APIs"],
    "employment_type": "Full-time",
}


@patch("app.services.jd_service.generate_completion")
def test_successful_generation(mock_completion):
    mock_completion.return_value = "Job Title: Backend Developer\n\nJob Overview...\n"
    response = client.post("/api/jd/generate", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Backend Developer" in data["job_description"]


def test_missing_job_title():
    payload = {**VALID_PAYLOAD, "job_title": ""}
    response = client.post("/api/jd/generate", json=payload)
    assert response.status_code == 422


def test_missing_experience():
    payload = {**VALID_PAYLOAD, "experience_required": ""}
    response = client.post("/api/jd/generate", json=payload)
    assert response.status_code == 422


def test_missing_required_skills():
    payload = {**VALID_PAYLOAD, "required_skills": []}
    response = client.post("/api/jd/generate", json=payload)
    assert response.status_code == 422


def test_missing_employment_type():
    payload = {**VALID_PAYLOAD, "employment_type": ""}
    response = client.post("/api/jd/generate", json=payload)
    assert response.status_code == 422


@patch("app.services.jd_service.generate_completion")
def test_llm_failure(mock_completion):
    from app.core.exceptions import LLMProviderError
    mock_completion.side_effect = LLMProviderError("boom")
    response = client.post("/api/jd/generate", json=VALID_PAYLOAD)
    assert response.status_code == 502
    assert "boom" not in response.text  # no internal details leaked


def test_response_schema():
    with patch("app.services.jd_service.generate_completion", return_value="Some JD text"):
        response = client.post("/api/jd/generate", json=VALID_PAYLOAD)
    data = response.json()
    assert set(data.keys()) == {"success", "job_description"}
    assert isinstance(data["job_description"], str)
