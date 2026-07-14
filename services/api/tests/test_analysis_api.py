from fastapi.testclient import TestClient
from services.api.app.api.analysis import get_analysis_service
from services.api.app.domain import AnalysisService
from services.api.app.main import app
from services.api.tests.test_analysis_service import ContextAwareProvider, build_retrieval


def build_analysis_service() -> AnalysisService:
    return AnalysisService(build_retrieval(), ContextAwareProvider())


def test_analysis_endpoint_returns_structured_grounded_response() -> None:
    app.dependency_overrides[get_analysis_service] = build_analysis_service
    try:
        response = TestClient(app).post(
            "/api/v1/analyze/reflection", json={"query": "mizaç ve denge", "topK": 5}
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ANSWER"
    assert payload["citations"]
    assert "hiddenReasoning" not in payload
    assert "rawProviderOutput" not in payload
