# ruff: noqa: UP045

from __future__ import annotations

from enum import Enum
from hashlib import sha256
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GateDecision(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class UsageEnvironment(str, Enum):
    NONE = "NONE"
    INTERNAL = "INTERNAL"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class HumanDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    status: GateDecision = GateDecision.PENDING
    reviewer: Optional[str] = Field(default=None, min_length=1, max_length=200)
    decided_at: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    evidence_reference: Optional[str] = Field(default=None, min_length=1, max_length=500)

    @model_validator(mode="after")
    def require_evidence_for_final_decision(self) -> HumanDecision:
        if self.status != GateDecision.PENDING:
            if not self.reviewer or not self.decided_at or not self.evidence_reference:
                raise ValueError("final decisions require reviewer, date, and evidence")
        return self


class ProductionEditionRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_id: str = Field(pattern=r"^SRC-[A-Z]{3}-\d{4}$")
    work_title: str = Field(min_length=1, max_length=300)
    author: str = Field(min_length=1, max_length=300)
    edition: Optional[str] = Field(default=None, min_length=1, max_length=500)
    publisher: Optional[str] = Field(default=None, min_length=1, max_length=300)
    publication_year: Optional[int] = Field(default=None, ge=1, le=2100)
    rights_holder: Optional[str] = Field(default=None, min_length=1, max_length=300)
    license_or_legal_basis: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    usage_environment: UsageEnvironment = UsageEnvironment.NONE
    digital_provenance: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    page_number_confidence: Optional[float] = Field(default=None, ge=0, le=1)
    ocr_suitability: Optional[str] = Field(default=None, min_length=1, max_length=500)
    legal_review: HumanDecision
    ocr_review: HumanDecision
    content_review: HumanDecision
    final_approval: HumanDecision

    @property
    def blockers(self) -> list[str]:
        blockers: list[str] = []
        required = {
            "edition": self.edition,
            "publisher": self.publisher,
            "publication_year": self.publication_year,
            "rights_holder": self.rights_holder,
            "license_or_legal_basis": self.license_or_legal_basis,
            "digital_provenance": self.digital_provenance,
            "page_number_confidence": self.page_number_confidence,
            "ocr_suitability": self.ocr_suitability,
        }
        blockers.extend(f"missing_{name}" for name, value in required.items() if value is None)
        if self.usage_environment != UsageEnvironment.PRODUCTION:
            blockers.append("production_usage_not_approved")
        for name in ("legal_review", "ocr_review", "content_review", "final_approval"):
            if getattr(self, name).status != GateDecision.APPROVED:
                blockers.append(f"{name}_not_approved")
        return blockers

    @property
    def production_eligible(self) -> bool:
        return not self.blockers


class ProductionPageMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_id: str = Field(pattern=r"^SRC-[A-Z]{3}-\d{4}$")
    author: str = Field(min_length=1)
    edition: str = Field(min_length=1)
    publisher: str = Field(min_length=1)
    page: int = Field(ge=1)
    chapter: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    keywords: list[str] = Field(min_length=1)
    language: str = Field(min_length=2)
    source_family: str = Field(min_length=1)
    review_status: str = Field(pattern="^APPROVED$")


class ProductionCollectionManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    collection_name: str = Field(pattern=r"^denge_atlasi_prod_v\d+$")
    source_count: int = Field(ge=1)
    page_count: int = Field(ge=1)
    chunk_count: int = Field(ge=1)
    source_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    embedding_model: str = Field(min_length=1)
    embedding_dimension: int = Field(ge=1)
    chunking_version: str = Field(min_length=1)
    created_at: str = Field(min_length=1)
    snapshot_reference: str = Field(min_length=1)
    backup_reference: str = Field(min_length=1)
    restore_test_reference: str = Field(min_length=1)

    @property
    def manifest_hash(self) -> str:
        payload = self.model_dump_json(exclude_none=True)
        return sha256(payload.encode("utf-8")).hexdigest()
