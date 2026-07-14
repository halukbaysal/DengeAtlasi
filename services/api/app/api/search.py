from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from services.api.app.contracts import SearchRequest, SearchResponse
from services.api.app.domain import SearchService
from services.api.app.rag import ChromaVectorStore, DeterministicTestEmbeddingProvider

router = APIRouter(prefix="/api/v1", tags=["retrieval"])


@lru_cache
def get_search_service() -> SearchService:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=(
            "No production embedding model is approved; configure a SearchService "
            "dependency explicitly."
        ),
    )


@router.post("/search", response_model=SearchResponse, operation_id="searchApprovedSources")
def search(
    request: SearchRequest,
    service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponse:
    return service.search(request)


def create_test_search_service(index_path: Path) -> SearchService:
    """Explicit local fixture helper; never selected implicitly in production."""

    return SearchService(
        ChromaVectorStore(persist_path=index_path), DeterministicTestEmbeddingProvider()
    )
