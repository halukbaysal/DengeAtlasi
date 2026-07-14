from pathlib import Path
from typing import Any

import chromadb
from services.api.app.contracts import SearchIntent, SearchRequest, SearchStatus
from services.api.app.domain import SearchService
from services.api.app.rag import (
    ChromaVectorStore,
    DeterministicTestEmbeddingProvider,
    SourceIndexer,
)
from services.api.app.sources import ReviewStatus, SourceCategory, SourceChunk
from services.api.scripts.index_sources import load_records

SOURCE_FIXTURES = Path(__file__).parent / "fixtures" / "sprint02"


def indexed_service() -> tuple[SearchService, ChromaVectorStore]:
    records, _ = load_records(SOURCE_FIXTURES)
    provider = DeterministicTestEmbeddingProvider()
    store = ChromaVectorStore(
        client=chromadb.EphemeralClient(), collection_name="search_service_tests"
    )
    SourceIndexer(store, provider).index(records)
    return SearchService(store, provider), store


def test_historical_query_returns_primary_then_labeled_supplement() -> None:
    service, _ = indexed_service()
    response = service.search(
        SearchRequest(query="historical invented supplement alpha beta", topK=5)
    )
    assert response.intent == SearchIntent.HISTORICAL_HEALTH_LIFESTYLE
    assert [group.role for group in response.groups] == ["primary", "supplementary"]
    assert response.groups[1].label == "Ibn Sina — supplementary"
    assert response.groups[1].results[0].source_id == "SRC-IBS-9001"


def test_result_metadata_is_complete_and_contains_no_generated_answer() -> None:
    service, _ = indexed_service()
    response = service.search(SearchRequest(query="invented primary-source chunking", topK=2))
    result = response.groups[0].results[0]
    assert result.source_id == "SRC-MAR-9001"
    assert result.page_number >= 1
    assert result.section
    assert result.edition
    assert "answer" not in response.model_dump()


class EmptyStore:
    def query(self, *_: object, **__: object) -> list[dict[str, Any]]:
        return []


def test_empty_results_return_stable_response() -> None:
    service = SearchService(EmptyStore(), DeterministicTestEmbeddingProvider())  # type: ignore[arg-type]
    response = service.search(SearchRequest(query="unsupported query", topK=5))
    assert response.status == SearchStatus.EMPTY
    assert response.groups == []
    assert response.source_limit_note


def test_metadata_filter_excludes_unapproved_chunks() -> None:
    provider = DeterministicTestEmbeddingProvider()
    store = ChromaVectorStore(
        client=chromadb.EphemeralClient(), collection_name="approved_filter_test"
    )
    chunk = SourceChunk(
        chunk_id="CHK-unapproved",
        source_id="SRC-MAR-9998",
        source_hash="hash",
        work_title="Synthetic",
        author="Synthetic",
        edition="Synthetic",
        page_number=1,
        section="Synthetic",
        category=SourceCategory.PRIMARY,
        review_status=ReviewStatus.UNREVIEWED,
        source_priority=1,
        content_type="prose",
        original_text="unapproved content",
        normalized_text="unapproved content",
        chunk_index=0,
    )
    store.replace_source([chunk], provider.embed([chunk.normalized_text]))
    results = store.query(
        provider.embed(["content"])[0], category="PRIMARY", source_priority=1, top_k=5
    )
    assert results == []
