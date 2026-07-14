from dataclasses import dataclass
from typing import Optional

from services.api.app.contracts import SearchIntent


@dataclass(frozen=True)
class RetrievalRoute:
    primary_category: str = "PRIMARY"
    primary_priority: int = 1
    supplementary_category: Optional[str] = None  # noqa: UP045
    supplementary_priority: Optional[int] = None  # noqa: UP045
    always_supplement: bool = False


ROUTES: dict[SearchIntent, RetrievalRoute] = {
    SearchIntent.TEMPERAMENT: RetrievalRoute(
        supplementary_category="SUPPLEMENTARY", supplementary_priority=2
    ),
    SearchIntent.HISTORICAL_HEALTH_LIFESTYLE: RetrievalRoute(
        supplementary_category="SUPPLEMENTARY",
        supplementary_priority=2,
        always_supplement=True,
    ),
    SearchIntent.ETHICS_HABITS: RetrievalRoute(),
    SearchIntent.NAFS_INNER_DISCIPLINE: RetrievalRoute(),
    SearchIntent.DECISION_SOCIAL_RESPONSIBILITY: RetrievalRoute(),
    SearchIntent.TURKISH_CULTURAL_VALUES: RetrievalRoute(),
    SearchIntent.GENERAL: RetrievalRoute(),
}


def route_intent(intent: SearchIntent) -> RetrievalRoute:
    return ROUTES[intent]
