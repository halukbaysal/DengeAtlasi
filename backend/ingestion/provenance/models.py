from __future__ import annotations

from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.ingestion.registry.models import UNKNOWN


class MetadataField(str, Enum):
    TITLE = "title"
    AUTHOR = "author"
    EDITOR = "editor"
    TRANSLATOR = "translator"
    PUBLISHER = "publisher"
    EDITION = "edition"
    PUBLICATION_YEAR = "publication_year"
    LANGUAGE = "language"
    SCRIPT = "script"
    PAGE_COUNT = "page_count"
    SECTION_TITLE = "section_title"
    SECTION_LOCATOR = "section_locator"


CandidateState = Literal[
    "CANDIDATE_CAPTURED",
    "HUMAN_REVIEW_REQUIRED",
    "VERIFIED",
    "REJECTED",
]
EvidenceKind = Literal[
    "PAGE",
    "FILE_LOCATION",
    "BIBLIOGRAPHIC_RECORD",
    "MANUAL_NOTE",
]


class EvidenceReference(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    evidence_id: str = Field(pattern=r"^KS-EVD-[a-f0-9]{24}$")
    source_id: str = Field(pattern=r"^KS-SRC-[a-f0-9]{20}$")
    kind: EvidenceKind
    locator: str = Field(min_length=1, max_length=1000)
    description: str = Field(min_length=1, max_length=2000)
    artifact_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    page: Optional[int] = Field(default=None, ge=1)
    visibility: Literal["LOCAL_RESTRICTED"] = "LOCAL_RESTRICTED"

    @model_validator(mode="after")
    def require_page_for_page_evidence(self) -> EvidenceReference:
        if self.kind == "PAGE" and self.page is None:
            raise ValueError("PAGE evidence requires page")
        return self


class MetadataCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    candidate_id: str = Field(pattern=r"^KS-MDC-[a-f0-9]{24}$")
    source_id: str = Field(pattern=r"^KS-SRC-[a-f0-9]{20}$")
    field_name: MetadataField
    value: str = Field(min_length=1, max_length=4000)
    evidence: list[EvidenceReference] = Field(default_factory=list)
    confidence: Optional[float] = Field(default=None, ge=0, le=1)
    state: CandidateState
    created_at: str = Field(min_length=1)
    created_by: str = Field(min_length=1, max_length=200)
    supersedes_candidate_id: Optional[str] = Field(
        default=None, pattern=r"^KS-MDC-[a-f0-9]{24}$"
    )
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = Field(default=None, max_length=200)
    review_reason: Optional[str] = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def enforce_evidence_and_review(self) -> MetadataCandidate:
        if self.value == UNKNOWN:
            if self.evidence:
                raise ValueError("UNKNOWN must not claim supporting evidence")
            if self.state == "VERIFIED":
                raise ValueError("UNKNOWN cannot be verified as a bibliographic fact")
        elif not self.evidence:
            raise ValueError("non-UNKNOWN metadata requires explicit evidence")
        if any(item.source_id != self.source_id for item in self.evidence):
            raise ValueError("evidence source_id must match candidate source_id")
        reviewed = self.state in {"VERIFIED", "REJECTED"}
        if reviewed and not (self.reviewed_at and self.reviewed_by and self.review_reason):
            raise ValueError("reviewed candidates require reviewer, time, and reason")
        if not reviewed and any((self.reviewed_at, self.reviewed_by, self.review_reason)):
            raise ValueError("unreviewed candidates cannot contain review decisions")
        return self


class ProvenanceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    provenance_id: str = Field(pattern=r"^KS-PRV-[a-f0-9]{24}$")
    source_id: str = Field(pattern=r"^KS-SRC-[a-f0-9]{20}$")
    statement: str = Field(min_length=1, max_length=4000)
    evidence: list[EvidenceReference] = Field(min_length=1)
    recorded_at: str = Field(min_length=1)
    recorded_by: str = Field(min_length=1, max_length=200)
    supersedes_provenance_id: Optional[str] = Field(
        default=None, pattern=r"^KS-PRV-[a-f0-9]{24}$"
    )

    @model_validator(mode="after")
    def keep_evidence_on_same_source(self) -> ProvenanceRecord:
        if any(item.source_id != self.source_id for item in self.evidence):
            raise ValueError("provenance evidence must belong to the same source")
        return self


class MetadataWorkspaceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(pattern=r"^KS-SRC-[a-f0-9]{20}$")
    registry_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    version: int = Field(default=0, ge=0)
    candidates: list[MetadataCandidate] = Field(default_factory=list)
    provenance: list[ProvenanceRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_duplicate_ids_and_invalid_supersession(
        self,
    ) -> MetadataWorkspaceRecord:
        candidate_ids = [item.candidate_id for item in self.candidates]
        provenance_ids = [item.provenance_id for item in self.provenance]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("duplicate metadata candidate ID")
        if len(provenance_ids) != len(set(provenance_ids)):
            raise ValueError("duplicate provenance ID")
        known_candidates: set[str] = set()
        for candidate in self.candidates:
            if candidate.source_id != self.source_id:
                raise ValueError("candidate source_id mismatch")
            if (
                candidate.supersedes_candidate_id is not None
                and candidate.supersedes_candidate_id not in known_candidates
            ):
                raise ValueError("candidate supersedes an unknown or future candidate")
            known_candidates.add(candidate.candidate_id)
        known_provenance: set[str] = set()
        for provenance in self.provenance:
            if provenance.source_id != self.source_id:
                raise ValueError("provenance source_id mismatch")
            if (
                provenance.supersedes_provenance_id is not None
                and provenance.supersedes_provenance_id not in known_provenance
            ):
                raise ValueError("provenance supersedes an unknown or future record")
            known_provenance.add(provenance.provenance_id)
        return self


class MetadataWorkspaceDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    records: list[MetadataWorkspaceRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_duplicate_sources(self) -> MetadataWorkspaceDocument:
        source_ids = [item.source_id for item in self.records]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("duplicate source workspace")
        return self


class MetadataAuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(pattern=r"^KS-MEV-[a-f0-9]{24}$")
    event_type: Literal[
        "METADATA_CANDIDATE_ADDED",
        "METADATA_CANDIDATE_REVIEWED",
        "PROVENANCE_RECORDED",
        "METADATA_IMPORT_APPLIED",
        "METADATA_EXPORT_CREATED",
    ]
    occurred_at: str = Field(min_length=1)
    actor: str = Field(min_length=1, max_length=200)
    source_id: Optional[str] = Field(
        default=None, pattern=r"^KS-SRC-[a-f0-9]{20}$"
    )
    workspace_version: Optional[int] = Field(default=None, ge=0)
    details: dict[str, str] = Field(default_factory=dict)
