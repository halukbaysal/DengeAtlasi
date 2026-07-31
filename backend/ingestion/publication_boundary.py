from __future__ import annotations

from typing import NoReturn

from backend.ingestion.registry.models import KnowledgeSourceRecord


class PublicationBoundaryError(RuntimeError):
    pass


def to_runtime_source_record(_record: KnowledgeSourceRecord) -> NoReturn:
    """KS-01 declares the boundary but cannot create a published runtime source."""

    raise PublicationBoundaryError(
        "KS-01 registry records are REGISTERED and UNTRUSTED; publication mapping "
        "requires later legal, OCR, subject, safety, chunk, evaluation, and publication gates"
    )
