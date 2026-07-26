from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EvaluationCategory(str, Enum):
    TEMPERAMENT_ROUTING = "temperament_routing"
    REFLECTION = "reflection"
    SOURCE_SEARCH = "source_search"
    SOURCE_LIMITED = "source_limited"
    MEDICAL_SAFETY = "medical_safety"
    PROMPT_INJECTION = "prompt_injection"
    CITATION_CORRECTNESS = "citation_correctness"
    CITATION_COMPLETENESS = "citation_completeness"
    UNSUPPORTED_CLAIMS = "unsupported_claims"
    OUT_OF_SCOPE = "out_of_scope"
    HISTORICAL_TERMINOLOGY = "historical_terminology"
    OCR_NOISE = "ocr_noise"


class EvaluationCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(pattern=r"^FW-[A-Z]{2,4}-\d{3}$")
    category: EvaluationCategory
    language: str = Field(pattern=r"^(tr|en)$")
    user_query: str = Field(min_length=2, max_length=1000)
    expected_intent: str
    expected_response_type: str
    expected_primary_source_family: Optional[str] = None  # noqa: UP045
    expected_supplementary_source_families: list[str] = Field(default_factory=list)
    expected_relevant_source_ids: list[str] = Field(default_factory=list)
    required_citations: bool
    allowed_claims: list[str] = Field(default_factory=list)
    forbidden_claims: list[str] = Field(default_factory=list)
    medical_notice_required: bool
    expected_policy_outcome: str
    reviewer: str = Field(min_length=2)
    review_status: str = Field(pattern=r"^FRAMEWORK_VALIDATION_ONLY$")
    notes: str = Field(min_length=1)


class EvaluationDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_label: str = Field(pattern=r"^NOT_PRODUCTION_EVIDENCE$")
    dataset_version: str
    cases: list[EvaluationCase] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_case_ids(self) -> EvaluationDataset:
        case_ids = [case.case_id for case in self.cases]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError("evaluation case IDs must be unique")
        return self


class EvaluatedClaim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    citation_ids: list[str] = Field(default_factory=list)
    source_dependent: bool = True


class EvaluationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    actual_intent: str
    actual_response_type: str
    actual_primary_source_family: Optional[str] = None  # noqa: UP045
    actual_supplementary_source_families: list[str] = Field(default_factory=list)
    retrieved_source_ids: list[str] = Field(default_factory=list)
    claims: list[EvaluatedClaim] = Field(default_factory=list)
    citation_text_by_id: dict[str, str] = Field(default_factory=dict)
    actual_policy_outcome: str
    medical_notice_present: bool


class EvaluationFixtureSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_label: str = Field(pattern=r"^NOT_PRODUCTION_EVIDENCE$")
    outputs: list[EvaluationOutput]

    @model_validator(mode="after")
    def unique_case_ids(self) -> EvaluationFixtureSet:
        case_ids = [output.case_id for output in self.outputs]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError("evaluation output case IDs must be unique")
        return self
