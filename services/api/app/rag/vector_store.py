from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any, Optional

import chromadb

from services.api.app.sources import SourceChunk


class ChromaVectorStore:
    def __init__(
        self,
        *,
        collection_name: str = "denge_atlasi_sources",
        persist_path: Optional[Path] = None,  # noqa: UP045
        client: Optional[Any] = None,  # noqa: UP045
    ) -> None:
        if client is not None:
            self._client = client
        elif persist_path is not None:
            persist_path.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(persist_path))
        else:
            self._client = chromadb.EphemeralClient()
        self._collection = self._client.get_or_create_collection(
            name=collection_name, configuration={"hnsw": {"space": "cosine"}}
        )

    def replace_source(
        self, chunks: Sequence[SourceChunk], embeddings: Sequence[list[float]]
    ) -> None:
        if not chunks:
            return
        if len(chunks) != len(embeddings):
            raise ValueError("chunk and embedding counts must match")
        source_id = chunks[0].source_id
        if any(chunk.source_id != source_id for chunk in chunks):
            raise ValueError("replace_source accepts chunks from one source")
        existing = self._collection.get(where={"source_id": source_id}, include=[])
        if existing["ids"]:
            self._collection.delete(ids=existing["ids"])
        self._collection.add(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.normalized_text for chunk in chunks],
            embeddings=list(embeddings),
            metadatas=[self._metadata(chunk) for chunk in chunks],
        )

    def source_hashes(self, source_id: str) -> set[str]:
        result = self._collection.get(where={"source_id": source_id}, include=["metadatas"])
        return {
            str(metadata["source_hash"])
            for metadata in result["metadatas"] or []
            if metadata is not None
        }

    def count(self) -> int:
        return self._collection.count()

    def metadata_for_source(self, source_id: str) -> list[dict[str, Any]]:
        result = self._collection.get(where={"source_id": source_id}, include=["metadatas"])
        return [dict(metadata) for metadata in result["metadatas"] or [] if metadata is not None]

    def query(
        self,
        query_embedding: list[float],
        *,
        category: str,
        source_priority: int,
        top_k: int,
    ) -> list[dict[str, Any]]:
        result = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={
                "$and": [
                    {"category": category},
                    {"source_priority": source_priority},
                    {"review_status": "APPROVED"},
                ]
            },
            include=["documents", "metadatas", "distances"],
        )
        ids = result["ids"][0] if result["ids"] else []
        documents = result["documents"][0] if result["documents"] else []
        metadatas = result["metadatas"][0] if result["metadatas"] else []
        distances = result["distances"][0] if result["distances"] else []
        return [
            {
                "chunk_id": chunk_id,
                "document": document,
                "metadata": dict(metadata or {}),
                "score": max(0.0, 1.0 - float(distance)),
            }
            for chunk_id, document, metadata, distance in zip(
                ids, documents, metadatas, distances
            )
        ]

    @staticmethod
    def _metadata(chunk: SourceChunk) -> dict[str, Any]:
        return {
            "source_id": chunk.source_id,
            "source_hash": chunk.source_hash,
            "work_title": chunk.work_title,
            "author": chunk.author,
            "edition": chunk.edition,
            "page_number": chunk.page_number,
            "section": chunk.section,
            "category": chunk.category.value,
            "review_status": chunk.review_status.value,
            "source_priority": chunk.source_priority,
            "content_type": chunk.content_type,
            "chunk_index": chunk.chunk_index,
            "original_text": chunk.original_text,
        }
