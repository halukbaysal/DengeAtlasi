from __future__ import annotations

from enum import Enum
from hashlib import sha256

from pydantic import BaseModel, ConfigDict, Field, model_validator

SOURCE_INJECTION_MARKERS = (
    "ignore previous", "ignore all previous", "system prompt",
    "önceki talimatları", "onceki talimatlari", "developer message", "jailbreak",
)


class ReviewStatus(str, Enum):
    UNREVIEWED = "UNREVIEWED"
    OCR_REVIEWED = "OCR_REVIEWED"
    CONTENT_REVIEWED = "CONTENT_REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class SourceCategory(str, Enum):
    PRIMARY = "PRIMARY"
    SUPPLEMENTARY = "SUPPLEMENTARY"
    CULTURAL = "CULTURAL"
    ACADEMIC_COMMENTARY = "ACADEMIC_COMMENTARY"


class CopyrightStatus(str, Enum):
    PENDING = "PENDING"
    CLEARED = "CLEARED"
    RESTRICTED = "RESTRICTED"
    REJECTED = "REJECTED"


class OcrStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    REJECTED = "REJECTED"


class SourcePage(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    page_number: int = Field(ge=1)
    section: str = Field(min_length=1, max_length=300)
    content_type: str = Field(default="prose", pattern="^(prose|poetry|table)$")
    original_text: str = Field(min_length=1)


class SourceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_id: str = Field(pattern=r"^SRC-[A-Z]{3}-\d{4}$")
    work_title: str = Field(min_length=1, max_length=300)
    author: str = Field(min_length=1, max_length=300)
    edition: str = Field(min_length=1, max_length=500)
    publisher: str = Field(min_length=1, max_length=300)
    publication_year: int = Field(ge=1, le=2100)
    language: str = Field(min_length=2, max_length=100)
    category: SourceCategory
    source_priority: int = Field(ge=1)
    review_status: ReviewStatus
    copyright_status: CopyrightStatus
    ocr_status: OcrStatus
    reviewed_by: str = Field(min_length=1, max_length=200)
    reviewed_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    synthetic_fixture: bool = False
    pages: list[SourcePage] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_approved_record(self) -> SourceRecord:
        if self.review_status == ReviewStatus.APPROVED:
            if self.copyright_status != CopyrightStatus.CLEARED:
                raise ValueError("APPROVED sources require CLEARED copyright status")
            if self.ocr_status not in {OcrStatus.COMPLETE, OcrStatus.NOT_APPLICABLE}:
                raise ValueError("APPROVED sources require completed or non-applicable OCR")
            source_text = "\n".join(page.original_text for page in self.pages).casefold()
            if any(marker in source_text for marker in SOURCE_INJECTION_MARKERS):
                raise ValueError("APPROVED source contains instruction-like content")
        return self

    @property
    def source_hash(self) -> str:
        payload = "\n".join(
            (
                self.edition,
                *(f"{page.page_number}:{page.section}:{page.original_text}" for page in self.pages),
            )
        )
        return sha256(payload.encode("utf-8")).hexdigest()


class SourceChunk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    source_id: str
    source_hash: str
    work_title: str
    author: str
    edition: str
    page_number: int
    section: str
    category: SourceCategory
    review_status: ReviewStatus
    source_priority: int
    content_type: str
    original_text: str
    normalized_text: str
    chunk_index: int = Field(ge=0)
