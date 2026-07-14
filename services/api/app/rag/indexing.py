from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path

from services.api.app.rag.chunking import chunk_source
from services.api.app.rag.embeddings import EmbeddingProvider
from services.api.app.rag.vector_store import ChromaVectorStore
from services.api.app.sources import ReviewStatus, SourceRecord


@dataclass
class IndexReport:
    accepted: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    duplicates: list[str] = field(default_factory=list)
    replaced: list[str] = field(default_factory=list)
    chunk_count: int = 0
    embedding_provider: str = ""

    def write(self, output_directory: Path) -> None:
        output_directory.mkdir(parents=True, exist_ok=True)
        (output_directory / "index-report.json").write_text(
            json.dumps(asdict(self), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        rows = [
            "# Source Index Report",
            "",
            f"- Embedding provider: `{self.embedding_provider}`",
            f"- Accepted: {len(self.accepted)}",
            f"- Rejected: {len(self.rejected)}",
            f"- Skipped: {len(self.skipped)}",
            f"- Duplicates: {len(self.duplicates)}",
            f"- Replaced: {len(self.replaced)}",
            f"- Chunks written: {self.chunk_count}",
            "",
            "## Record IDs",
            "",
            f"- Accepted: {', '.join(self.accepted) or 'none'}",
            f"- Rejected: {', '.join(self.rejected) or 'none'}",
            f"- Skipped: {', '.join(self.skipped) or 'none'}",
            f"- Duplicates: {', '.join(self.duplicates) or 'none'}",
            f"- Replaced: {', '.join(self.replaced) or 'none'}",
        ]
        (output_directory / "index-report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


class SourceIndexer:
    def __init__(self, vector_store: ChromaVectorStore, embeddings: EmbeddingProvider) -> None:
        self._vector_store = vector_store
        self._embeddings = embeddings

    def index(self, records: Sequence[SourceRecord], *, production: bool = True) -> IndexReport:
        report = IndexReport(embedding_provider=self._embeddings.provider_id)
        observed_hashes: set[str] = set()
        for record in sorted(records, key=lambda item: (item.source_priority, item.source_id)):
            if production and record.review_status != ReviewStatus.APPROVED:
                report.rejected.append(record.source_id)
                continue
            if record.source_hash in observed_hashes:
                report.duplicates.append(record.source_id)
                continue
            observed_hashes.add(record.source_hash)
            existing_hashes = self._vector_store.source_hashes(record.source_id)
            if existing_hashes == {record.source_hash}:
                report.skipped.append(record.source_id)
                continue
            chunks = chunk_source(record)
            embeddings = self._embeddings.embed([chunk.normalized_text for chunk in chunks])
            self._vector_store.replace_source(chunks, embeddings)
            if existing_hashes:
                report.replaced.append(record.source_id)
            else:
                report.accepted.append(record.source_id)
            report.chunk_count += len(chunks)
        return report
