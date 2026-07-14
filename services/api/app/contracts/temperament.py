from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from services.api.app.contracts.search import API_MODEL_CONFIG, RetrievalResult, to_camel


class TemperamentStatus(str, Enum):
    THEMES_FOUND = "THEMES_FOUND"
    SOURCE_LIMITED = "SOURCE_LIMITED"
    MEDICAL_REDIRECT = "MEDICAL_REDIRECT"
    SAFETY_REDIRECT = "SAFETY_REDIRECT"


class TemperamentRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    observations: str = Field(min_length=2, max_length=1000)
    consent_accepted: bool
    confirms_adult: bool
    confirms_self_report: bool
    include_lifestyle_context: bool = False

    @model_validator(mode="after")
    def require_eligible_consent(self) -> "TemperamentRequest":
        if not self.consent_accepted:
            raise ValueError("Educational and safety consent is required.")
        if not self.confirms_adult:
            raise ValueError("Temperament reflection is available only to adults.")
        if not self.confirms_self_report:
            raise ValueError("Only self-reflection input is allowed.")
        return self


class TemperamentFinding(BaseModel):
    model_config = API_MODEL_CONFIG

    text: str
    citation_ids: list[str] = Field(min_length=1)


class TemperamentResponse(BaseModel):
    model_config = API_MODEL_CONFIG

    status: TemperamentStatus
    primary_source_findings: list[TemperamentFinding] = Field(default_factory=list)
    supplementary_findings: list[TemperamentFinding] = Field(default_factory=list)
    supplement_reason: Optional[str] = None  # noqa: UP045
    symbolic_themes: list[str] = Field(default_factory=list)
    safe_wellbeing_suggestions: list[str] = Field(default_factory=list)
    reflection_questions: list[str] = Field(default_factory=list)
    citations: list[RetrievalResult] = Field(default_factory=list)
    source_limit_note: Optional[str] = None  # noqa: UP045
    medical_safety_notice: Optional[str] = None  # noqa: UP045
    educational_disclaimer: str
    correlation_id: str
