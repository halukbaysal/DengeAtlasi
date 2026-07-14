import pytest
from services.api.app.contracts import SearchIntent
from services.api.app.domain import classify_intent, route_intent


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("Mizaç ve denge", SearchIntent.TEMPERAMENT),
        ("Uyku ve mevsim hakkında tarihsel bilgi", SearchIntent.HISTORICAL_HEALTH_LIFESTYLE),
        ("Ahlak ve erdem", SearchIntent.ETHICS_HABITS),
        ("Nefs disiplini", SearchIntent.NAFS_INNER_DISCIPLINE),
        ("Bilinmeyen konu", SearchIntent.GENERAL),
    ],
)
def test_deterministic_intent_classification(query: str, expected: SearchIntent) -> None:
    assert classify_intent(query) == expected


def test_routing_is_server_controlled_and_marifetname_first() -> None:
    route = route_intent(SearchIntent.HISTORICAL_HEALTH_LIFESTYLE)
    assert route.primary_category == "PRIMARY"
    assert route.primary_priority == 1
    assert route.supplementary_category == "SUPPLEMENTARY"
    assert route.supplementary_priority == 2
    assert route.always_supplement is True
