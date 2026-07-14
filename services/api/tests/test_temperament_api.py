from fastapi.testclient import TestClient
from services.api.app.api.temperament import get_temperament_service
from services.api.app.domain import TemperamentService
from services.api.app.main import app
from services.api.tests.test_analysis_service import build_retrieval


def build_service() -> TemperamentService:
    return TemperamentService(build_retrieval(minimum_score=0.0))


def test_temperament_endpoint_requires_consent_and_returns_themes() -> None:
    app.dependency_overrides[get_temperament_service] = build_service
    try:
        client = TestClient(app)
        invalid = client.post(
            "/api/v1/analyze/temperament",
            json={
                "observations": "denge",
                "consentAccepted": False,
                "confirmsAdult": True,
                "confirmsSelfReport": True,
            },
        )
        valid = client.post(
            "/api/v1/analyze/temperament",
            json={
                "observations": "denge",
                "consentAccepted": True,
                "confirmsAdult": True,
                "confirmsSelfReport": True,
            },
        )
    finally:
        app.dependency_overrides.clear()
    assert invalid.status_code == 422
    assert valid.status_code == 200
    assert valid.json()["status"] == "THEMES_FOUND"
