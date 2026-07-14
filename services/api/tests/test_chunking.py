from pathlib import Path

from services.api.app.rag import chunk_source, normalize_text
from services.api.app.sources import SourceRecord

FIXTURE = Path(__file__).parent / "fixtures" / "sprint02" / "marifetname_approved.json"


def load_source() -> SourceRecord:
    return SourceRecord.model_validate_json(FIXTURE.read_text(encoding="utf-8"))


def test_normalization_preserves_original_source_text() -> None:
    original = "İnsan\t  dengesi\r\n korunur."
    assert normalize_text(original) == "İnsan dengesi\nkorunur."
    assert original == "İnsan\t  dengesi\r\n korunur."


def test_chunks_have_stable_ids_and_page_traceability() -> None:
    source = load_source()
    first = chunk_source(source, max_words=12)
    second = chunk_source(source, max_words=12)

    assert [chunk.chunk_id for chunk in first] == [chunk.chunk_id for chunk in second]
    assert all(chunk.source_id == source.source_id for chunk in first)
    assert {(chunk.page_number, chunk.section) for chunk in first} == {
        (1, "Synthetic balance prose"),
        (2, "Synthetic verse"),
    }
    assert all(chunk.original_text for chunk in first)
    assert all(chunk.normalized_text for chunk in first)


def test_poetry_units_are_not_merged_when_chunk_limit_is_small() -> None:
    poetry_chunks = [
        chunk for chunk in chunk_source(load_source(), max_words=4) if chunk.page_number == 2
    ]
    assert len(poetry_chunks) == 2
