import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from services.api.app.sources import ReviewStatus, SourceRecord

FIXTURES = Path(__file__).parent / "fixtures" / "sprint02"


def load_fixture(name: str) -> SourceRecord:
    return SourceRecord.model_validate_json((FIXTURES / name).read_text(encoding="utf-8"))


def test_approved_source_requires_complete_metadata() -> None:
    with pytest.raises(ValidationError):
        SourceRecord.model_validate_json(
            (FIXTURES / "invalid_missing_metadata.json").read_text(encoding="utf-8")
        )


def test_approved_source_requires_cleared_copyright() -> None:
    payload = json.loads((FIXTURES / "marifetname_approved.json").read_text(encoding="utf-8"))
    payload["copyright_status"] = "PENDING"
    with pytest.raises(ValidationError, match="CLEARED copyright"):
        SourceRecord.model_validate(payload)


def test_source_hash_is_stable_and_changes_with_source_text() -> None:
    first = load_fixture("marifetname_approved.json")
    second = load_fixture("marifetname_approved.json")
    assert first.source_hash == second.source_hash

    second.pages[0].original_text += " Synthetic correction."
    assert first.source_hash != second.source_hash
    assert first.review_status == ReviewStatus.APPROVED
