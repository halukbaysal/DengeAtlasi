from __future__ import annotations

import re
from collections.abc import Iterable
from hashlib import sha256

from services.api.app.rag.normalization import normalize_text
from services.api.app.sources import SourceChunk, SourcePage, SourceRecord


def _prose_units(text: str) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    if len(paragraphs) > 1:
        return paragraphs
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def _page_units(page: SourcePage) -> list[str]:
    if page.content_type in {"poetry", "table"}:
        return [line.strip() for line in page.original_text.splitlines() if line.strip()]
    return _prose_units(page.original_text)


def _group_units(units: Iterable[str], max_words: int, overlap_units: int) -> list[str]:
    grouped: list[str] = []
    current: list[str] = []
    current_words = 0
    for unit in units:
        unit_words = len(unit.split())
        if current and current_words + unit_words > max_words:
            grouped.append("\n".join(current))
            current = current[-overlap_units:] if overlap_units else []
            current_words = sum(len(item.split()) for item in current)
        current.append(unit)
        current_words += unit_words
    if current:
        grouped.append("\n".join(current))
    return grouped


def _chunk_id(record: SourceRecord, page: SourcePage, index: int, text: str) -> str:
    identity = "|".join(
        (
            record.source_id,
            record.source_hash,
            str(page.page_number),
            page.section,
            str(index),
            text,
        )
    )
    return f"CHK-{sha256(identity.encode('utf-8')).hexdigest()[:24]}"


def chunk_source(
    record: SourceRecord, *, max_words: int = 120, overlap_units: int = 1
) -> list[SourceChunk]:
    chunks: list[SourceChunk] = []
    index = 0
    for page in sorted(record.pages, key=lambda item: item.page_number):
        for text in _group_units(_page_units(page), max_words, overlap_units):
            chunks.append(
                SourceChunk(
                    chunk_id=_chunk_id(record, page, index, text),
                    source_id=record.source_id,
                    source_hash=record.source_hash,
                    work_title=record.work_title,
                    author=record.author,
                    edition=record.edition,
                    page_number=page.page_number,
                    section=page.section,
                    category=record.category,
                    review_status=record.review_status,
                    source_priority=record.source_priority,
                    content_type=page.content_type,
                    original_text=text,
                    normalized_text=normalize_text(text),
                    chunk_index=index,
                )
            )
            index += 1
    return chunks
