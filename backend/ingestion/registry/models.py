from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

UNKNOWN = "UNKNOWN"


class IntakeStatus(str, Enum):
    REGISTERED = "REGISTERED"


class TrustStatus(str, Enum):
    UNTRUSTED = "UNTRUSTED"


class KnowledgeSourceRecord(BaseModel):
    """Canonical KS registry record for incomplete, unreviewed intake."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_id: str = Field(pattern=r"^KS-SRC-[a-f0-9]{20}$")
    original_filename: str = Field(min_length=1, max_length=500)
    normalized_filename: str = Field(pattern=r"^[a-z0-9][a-z0-9_.-]*\.pdf$")
    original_relative_path: str = Field(pattern=r"^originals/[a-f0-9]{2}/[a-f0-9]{64}\.pdf$")
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    file_size_bytes: int = Field(gt=0)
    mime_type: str = Field(pattern=r"^application/pdf$")
    imported_at: str = Field(min_length=1)
    intake_status: IntakeStatus = IntakeStatus.REGISTERED
    trust_status: TrustStatus = TrustStatus.UNTRUSTED
    title: str = UNKNOWN
    author: str = UNKNOWN
    editor: str = UNKNOWN
    translator: str = UNKNOWN
    publisher: str = UNKNOWN
    edition: str = UNKNOWN
    publication_year: str = UNKNOWN
    language: str = UNKNOWN
    original_language: str = UNKNOWN

    @model_validator(mode="after")
    def enforce_fail_closed_intake(self) -> KnowledgeSourceRecord:
        if self.intake_status != IntakeStatus.REGISTERED:
            raise ValueError("KS-01 records may only be REGISTERED")
        if self.trust_status != TrustStatus.UNTRUSTED:
            raise ValueError("KS-01 records must remain UNTRUSTED")
        return self


class SourceRegistryDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1)
    records: list[KnowledgeSourceRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_duplicate_identifiers(self) -> SourceRegistryDocument:
        source_ids = [record.source_id for record in self.records]
        checksums = [record.sha256 for record in self.records]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("duplicate source_id in registry")
        if len(checksums) != len(set(checksums)):
            raise ValueError("duplicate sha256 in registry")
        return self


class IntakeAuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(pattern=r"^KS-EVT-[a-f0-9]{24}$")
    event_type: str = Field(pattern=r"^(SOURCE_REGISTERED|EXACT_DUPLICATE_SKIPPED)$")
    occurred_at: str = Field(min_length=1)
    actor: str = Field(default="LOCAL_CLI", pattern=r"^[A-Z0-9_-]+$")
    source_id: str = Field(pattern=r"^KS-SRC-[a-f0-9]{20}$")
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    original_filename: str = Field(min_length=1, max_length=500)
    details: dict[str, str] = Field(default_factory=dict)


class IntakeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record: KnowledgeSourceRecord
    exact_duplicate: bool
