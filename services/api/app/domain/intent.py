from services.api.app.contracts import SearchIntent
from services.api.app.rag.normalization import normalize_text

KEYWORDS: tuple[tuple[SearchIntent, frozenset[str]], ...] = (
    (
        SearchIntent.HISTORICAL_HEALTH_LIFESTYLE,
        frozenset({"sağlık", "beden", "uyku", "hareket", "mevsim", "hastalık", "historical"}),
    ),
    (SearchIntent.TEMPERAMENT, frozenset({"mizaç", "mizac", "temperament", "denge"})),
    (
        SearchIntent.NAFS_INNER_DISCIPLINE,
        frozenset({"nefis", "nefs", "nafs", "disiplin", "disiplini"}),
    ),
    (SearchIntent.ETHICS_HABITS, frozenset({"ahlak", "etik", "alışkanlık", "erdem"})),
    (
        SearchIntent.DECISION_SOCIAL_RESPONSIBILITY,
        frozenset({"karar", "sorumluluk", "toplum"}),
    ),
    (SearchIntent.TURKISH_CULTURAL_VALUES, frozenset({"kültür", "kutadgu", "değer"})),
)


def classify_intent(query: str) -> SearchIntent:
    normalized = normalize_text(query).casefold()
    tokens = frozenset(normalized.replace("/", " ").split())
    for intent, keywords in KEYWORDS:
        if tokens & keywords:
            return intent
    return SearchIntent.GENERAL
