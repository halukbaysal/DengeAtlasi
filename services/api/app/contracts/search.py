from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def to_camel(value: str) -> str:
    first, *rest = value.split("_")
    return first + "".join(part.capitalize() for part in rest)


API_MODEL_CONFIG = ConfigDict(
    alias_generator=to_camel,
    extra="forbid",
    populate_by_name=True,
)


class SearchIntent(str, Enum):
    TEMPERAMENT = "TEMPERAMENT"
    ETHICS_HABITS = "ETHICS_HABITS"
    NAFS_INNER_DISCIPLINE = "NAFS_INNER_DISCIPLINE"
    HISTORICAL_HEALTH_LIFESTYLE = "HISTORICAL_HEALTH_LIFESTYLE"
    DECISION_SOCIAL_RESPONSIBILITY = "DECISION_SOCIAL_RESPONSIBILITY"
    TURKISH_CULTURAL_VALUES = "TURKISH_CULTURAL_VALUES"
    GENERAL = "GENERAL"


class SearchStatus(str, Enum):
    FOUND = "FOUND"
    INSUFFICIENT = "INSUFFICIENT"
    EMPTY = "EMPTY"


class SearchRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    query: str = Field(min_length=2, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=10)

    @field_validator("query")
    @classmethod
    def reject_control_characters(cls, value: str) -> str:
        if any(ord(character) < 32 and character not in "\n\t" for character in value):
            raise ValueError("query contains unsupported control characters")
        return " ".join(value.split())


class RetrievalResult(BaseModel):
    model_config = API_MODEL_CONFIG

    chunk_id: str
    source_id: str
    work_title: str
    author: str
    edition: str
    page_number: int
    section: str
    category: str
    score: float = Field(ge=0.0, le=1.0)
    excerpt: str


class RetrievalGroup(BaseModel):
    model_config = API_MODEL_CONFIG

    role: str
    label: str
    results: list[RetrievalResult]


class SearchResponse(BaseModel):
    model_config = API_MODEL_CONFIG

    status: SearchStatus
    intent: SearchIntent
    normalized_query: str
    groups: list[RetrievalGroup]
    source_limit_note: Optional[str] = None  # noqa: UP045
    correlation_id: str
