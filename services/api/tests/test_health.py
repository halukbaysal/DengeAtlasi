from datetime import datetime

from fastapi.testclient import TestClient
from services.api.app.contracts import HealthResponse
from services.api.app.main import app

client = TestClient(app)


def test_health_returns_structured_response() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    parsed = HealthResponse.model_validate(payload)
    assert parsed.status == "ok"
    assert parsed.service == "denge-atlasi-api"
    assert parsed.version == "0.1.0"
    assert isinstance(parsed.timestamp, datetime)


def test_health_contract_rejects_unknown_fields() -> None:
    schema = HealthResponse.model_json_schema()
    assert schema["additionalProperties"] is False
