from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from services.api.app.contracts.search import API_MODEL_CONFIG, RetrievalResult, to_camel


class AnalysisStatus(str, Enum):
    ANSWER = "ANSWER"
    SOURCE_LIMITED = "SOURCE_LIMITED"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    SAFETY_REDIRECT = "SAFETY_REDIRECT"
    MEDICAL_REDIRECT = "MEDICAL_REDIRECT"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    CITATION_VALIDATION_FAILED = "CITATION_VALIDATION_FAILED"


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    query: str = Field(min_length=2, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=10)


class GeneratedClaim(BaseModel):
    model_config = API_MODEL_CONFIG

    text: str = Field(min_length=1, max_length=2000)
    citation_ids: list[str] = Field(min_length=1)


class ProviderAnswer(BaseModel):
    model_config = API_MODEL_CONFIG

    sourced_claims: list[GeneratedClaim]
    general_symbolic_interpretation: Optional[str] = Field(  # noqa: UP045
        default=None, max_length=2000
    )


class AnalysisResponse(BaseModel):
    model_config = API_MODEL_CONFIG

    status: AnalysisStatus
    sourced_claims: list[GeneratedClaim] = Field(default_factory=list)
    general_symbolic_interpretation: Optional[str] = None  # noqa: UP045
    citations: list[RetrievalResult] = Field(default_factory=list)
    source_limit_note: Optional[str] = None  # noqa: UP045
    medical_notice: Optional[str] = None  # noqa: UP045
    message: Optional[str] = None  # noqa: UP045
    prompt_id: Optional[str] = None  # noqa: UP045
    prompt_version: Optional[str] = None  # noqa: UP045
    correlation_id: str
