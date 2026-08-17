from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "current_jd": "Job Title: Backend Developer\n\nResponsibilities:\n- Build APIs",
    "custom_prompt": "Make it more concise and emphasize Python.",
}


@patch("app.services.jd_service.generate_completion")
def test_successful_modification(mock_completion):
    mock_completion.return_value = "Job Title: Backend Developer (Python-focused)\n..."
    response = client.post("/api/jd/modify", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["job_description"]) > 0


def test_empty_custom_prompt():
    payload = {**VALID_PAYLOAD, "custom_prompt": ""}
    response = client.post("/api/jd/modify", json=payload)
    assert response.status_code == 422


def test_empty_current_jd():
    payload = {**VALID_PAYLOAD, "current_jd": ""}
    response = client.post("/api/jd/modify", json=payload)
    assert response.status_code == 422


@patch("app.services.jd_service.generate_completion")
def test_llm_failure_on_modify(mock_completion):
    from app.core.exceptions import LLMTimeoutError
    mock_completion.side_effect = LLMTimeoutError("timed out")
    response = client.post("/api/jd/modify", json=VALID_PAYLOAD)
    assert response.status_code == 504


def test_modify_response_schema():
    with patch("app.services.jd_service.generate_completion", return_value="Revised JD text"):
        response = client.post("/api/jd/modify", json=VALID_PAYLOAD)
    data = response.json()
    assert set(data.keys()) == {"success", "job_description"}
