from pathlib import Path

import chromadb
from fastapi.testclient import TestClient
from services.api.app.api.search import get_search_service
from services.api.app.domain import SearchService
from services.api.app.main import app
from services.api.app.rag import (
    ChromaVectorStore,
    DeterministicTestEmbeddingProvider,
    SourceIndexer,
)
from services.api.scripts.index_sources import load_records

FIXTURES = Path(__file__).parent / "fixtures" / "sprint02"


def build_service() -> SearchService:
    records, _ = load_records(FIXTURES)
    provider = DeterministicTestEmbeddingProvider()
    store = ChromaVectorStore(client=chromadb.EphemeralClient(), collection_name="api_test")
    SourceIndexer(store, provider).index(records)
    return SearchService(store, provider)


def test_search_endpoint_returns_structured_retrieval_only() -> None:
    app.dependency_overrides[get_search_service] = build_service
    try:
        response = TestClient(app).post(
            "/api/v1/search", json={"query": "invented primary-source chunking", "topK": 5}
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    payload = response.json()
    assert payload["groups"][0]["role"] == "primary"
    assert payload["groups"][0]["results"][0]["sourceId"] == "SRC-MAR-9001"
    assert "correlationId" in payload
    assert "answer" not in payload


def test_search_endpoint_rejects_oversized_and_user_controlled_filters() -> None:
    app.dependency_overrides[get_search_service] = build_service
    try:
        client = TestClient(app)
        oversized = client.post("/api/v1/search", json={"query": "x" * 1001})
        bypass = client.post(
            "/api/v1/search",
            json={
                "query": "valid query",
                "collection": "unapproved",
                "sourcePriority": 99,
            },
        )
    finally:
        app.dependency_overrides.clear()
    assert oversized.status_code == 422
    assert bypass.status_code == 422
