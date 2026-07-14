import logging
from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.api.app.security import SecurityMiddleware


def guarded_app(*, body_limit: int = 128, request_limit: int = 2) -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        SecurityMiddleware,
        max_body_bytes=body_limit,
        rate_limit_requests=request_limit,
        rate_limit_window_seconds=60,
    )

    @app.post("/api/v1/echo")
    def echo() -> dict[str, bool]:
        return {"ok": True}

    return app


def test_payload_limit_rejects_oversized_content() -> None:
    response = TestClient(guarded_app()).post("/api/v1/echo", content=b"x" * 129)
    assert response.status_code == 413
    assert response.json()["detail"] == "PAYLOAD_TOO_LARGE"


def test_rate_limit_is_enforced_per_client() -> None:
    client = TestClient(guarded_app())
    assert client.post("/api/v1/echo").status_code == 200
    assert client.post("/api/v1/echo").status_code == 200
    response = client.post("/api/v1/echo")
    assert response.status_code == 429
    assert response.json()["detail"] == "RATE_LIMITED"


def test_logs_contain_metadata_but_not_sensitive_body(caplog: Any) -> None:
    sensitive = "private-journal-health-value"
    with caplog.at_level(logging.INFO, logger="denge_atlasi.http"):
        response = TestClient(guarded_app()).post(
            "/api/v1/echo", json={"journal": sensitive}
        )
    assert response.status_code == 200
    assert sensitive not in caplog.text
    assert "endpoint=/api/v1/echo" in caplog.text
    assert response.headers["x-correlation-id"]
