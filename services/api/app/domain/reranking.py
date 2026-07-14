from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RetrievalCandidate:
    chunk_id: str
    document: str
    metadata: dict[str, object]
    score: float


class Reranker(Protocol):
    @property
    def provider_id(self) -> str: ...

    def rerank(
        self, query: str, candidates: Sequence[RetrievalCandidate], top_k: int
    ) -> list[RetrievalCandidate]: ...


class LexicalReranker:
    @property
    def provider_id(self) -> str:
        return "lexical-default-v1"

    def rerank(
        self, query: str, candidates: Sequence[RetrievalCandidate], top_k: int
    ) -> list[RetrievalCandidate]:
        query_tokens = set(query.casefold().split())

        def rank(candidate: RetrievalCandidate) -> tuple[int, float, str]:
            document_tokens = set(candidate.document.casefold().split())
            return (len(query_tokens & document_tokens), candidate.score, candidate.chunk_id)

        return sorted(candidates, key=rank, reverse=True)[:top_k]
