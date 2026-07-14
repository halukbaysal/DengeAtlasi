from pathlib import Path

from services.api.scripts.index_sources import load_records

FIXTURES = Path(__file__).parent / "fixtures" / "sprint02"


def test_loader_rejects_invalid_fixture_without_exposing_content() -> None:
    records, rejected = load_records(FIXTURES)
    assert len(records) == 3
    assert rejected == ["invalid_missing_metadata.json"]
