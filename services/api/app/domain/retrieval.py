from __future__ import annotations

from typing import Optional
from uuid import uuid4

from services.api.app.contracts import (
    RetrievalGroup,
    RetrievalResult,
    SearchIntent,
    SearchRequest,
    SearchResponse,
    SearchStatus,
)
from services.api.app.domain.intent import classify_intent
from services.api.app.domain.reranking import LexicalReranker, Reranker, RetrievalCandidate
from services.api.app.domain.routing import route_intent
from services.api.app.rag import ChromaVectorStore, EmbeddingProvider, normalize_text


class SearchService:
    def __init__(
        self,
        store: ChromaVectorStore,
        embeddings: EmbeddingProvider,
        reranker: Optional[Reranker] = None,  # noqa: UP045
        *,
        minimum_score: float = 0.05,
    ) -> None:
        self._store = store
        self._embeddings = embeddings
        self._reranker = reranker or LexicalReranker()
        self._minimum_score = minimum_score

    def search(self, request: SearchRequest) -> SearchResponse:
        return self.search_for_intent(request)

    def search_for_intent(
        self,
        request: SearchRequest,
        *,
        intent_override: Optional[SearchIntent] = None,  # noqa: UP045
        force_supplement: bool = False,
    ) -> SearchResponse:
        normalized_query = normalize_text(request.query)
        intent = intent_override or classify_intent(normalized_query)
        route = route_intent(intent)
        query_embedding = self._embeddings.embed([normalized_query])[0]

        primary = self._retrieve(
            normalized_query,
            query_embedding,
            category=route.primary_category,
            priority=route.primary_priority,
            top_k=request.top_k,
        )
        groups: list[RetrievalGroup] = []
        if primary:
            groups.append(RetrievalGroup(role="primary", label="Marifetname", results=primary))

        should_supplement = route.supplementary_category is not None and (
            route.always_supplement or force_supplement or not primary
        )
        supplementary: list[RetrievalResult] = []
        if should_supplement:
            assert route.supplementary_category is not None
            assert route.supplementary_priority is not None
            supplementary = self._retrieve(
                normalized_query,
                query_embedding,
                category=route.supplementary_category,
                priority=route.supplementary_priority,
                top_k=request.top_k,
            )
            if supplementary:
                groups.append(
                    RetrievalGroup(
                        role="supplementary",
                        label="Ibn Sina — supplementary",
                        results=supplementary,
                    )
                )

        status = SearchStatus.FOUND
        source_limit_note = None
        if not primary and not supplementary:
            status = SearchStatus.EMPTY
            source_limit_note = "No sufficiently relevant approved source passages were found."
        elif should_supplement and not supplementary:
            status = SearchStatus.INSUFFICIENT
            source_limit_note = "Approved supplementary source material was insufficient."

        return SearchResponse(
            status=status,
            intent=intent,
            normalized_query=normalized_query,
            groups=groups,
            source_limit_note=source_limit_note,
            correlation_id=str(uuid4()),
        )

    def _retrieve(
        self,
        query: str,
        query_embedding: list[float],
        *,
        category: str,
        priority: int,
        top_k: int,
    ) -> list[RetrievalResult]:
        raw = self._store.query(
            query_embedding,
            category=category,
            source_priority=priority,
            top_k=top_k,
        )
        candidates = [
            RetrievalCandidate(
                chunk_id=str(item["chunk_id"]),
                document=str(item["document"]),
                metadata=dict(item["metadata"]),
                score=float(item["score"]),
            )
            for item in raw
            if float(item["score"]) >= self._minimum_score
        ]
        return [self._to_result(item) for item in self._reranker.rerank(query, candidates, top_k)]

    @staticmethod
    def _to_result(candidate: RetrievalCandidate) -> RetrievalResult:
        metadata = candidate.metadata
        return RetrievalResult(
            chunk_id=candidate.chunk_id,
            source_id=str(metadata["source_id"]),
            work_title=str(metadata["work_title"]),
            author=str(metadata["author"]),
            edition=str(metadata["edition"]),
            page_number=int(str(metadata["page_number"])),
            section=str(metadata["section"]),
            category=str(metadata["category"]),
            score=candidate.score,
            excerpt=candidate.document,
        )
