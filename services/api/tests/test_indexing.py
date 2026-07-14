import json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import chromadb
from services.api.app.rag import (
    ChromaVectorStore,
    DeterministicTestEmbeddingProvider,
    SourceIndexer,
)
from services.api.app.sources import SourceRecord

FIXTURES = Path(__file__).parent / "fixtures" / "sprint02"


def load(name: str) -> SourceRecord:
    return SourceRecord.model_validate_json((FIXTURES / name).read_text(encoding="utf-8"))


def create_indexer() -> tuple[SourceIndexer, ChromaVectorStore]:
    store = ChromaVectorStore(
        client=chromadb.EphemeralClient(), collection_name=f"test_{uuid4().hex}"
    )
    return SourceIndexer(store, DeterministicTestEmbeddingProvider(dimensions=8)), store


def test_mock_embedding_adapter_is_deterministic() -> None:
    provider = DeterministicTestEmbeddingProvider(dimensions=8)
    first = provider.embed(["sentetik metin"])
    assert first == provider.embed(["sentetik metin"])
    assert len(first[0]) == 8


def test_production_index_rejects_unreviewed_and_is_idempotent() -> None:
    indexer, store = create_indexer()
    approved = load("marifetname_approved.json")
    unreviewed = load("marifetname_unreviewed.json")

    first = indexer.index([unreviewed, approved])
    initial_count = store.count()
    second = indexer.index([approved])

    assert first.accepted == [approved.source_id]
    assert first.rejected == [unreviewed.source_id]
    assert second.skipped == [approved.source_id]
    assert store.count() == initial_count


def test_duplicate_hash_is_reported() -> None:
    indexer, _ = create_indexer()
    approved = load("marifetname_approved.json")
    duplicate = approved.model_copy(update={"source_id": "SRC-MAR-9999"})

    report = indexer.index([approved, duplicate])
    assert report.duplicates == [duplicate.source_id]


def test_source_update_replaces_old_chunks_and_metadata_is_traceable() -> None:
    indexer, store = create_indexer()
    source = load("marifetname_approved.json")
    indexer.index([source])
    old_count = store.count()

    payload = deepcopy(source.model_dump(mode="json"))
    payload["pages"] = [payload["pages"][0]]
    payload["pages"][0]["original_text"] = "A corrected, entirely synthetic source paragraph."
    updated = SourceRecord.model_validate(payload)
    report = indexer.index([updated])

    assert report.replaced == [source.source_id]
    assert store.count() < old_count
    metadata = store.metadata_for_source(source.source_id)
    assert {item["source_hash"] for item in metadata} == {updated.source_hash}
    assert {item["page_number"] for item in metadata} == {1}
    assert {item["section"] for item in metadata} == {"Synthetic balance prose"}


def test_index_report_has_machine_and_human_readable_outputs(tmp_path: Path) -> None:
    indexer, _ = create_indexer()
    report = indexer.index([load("marifetname_approved.json")])
    report.write(tmp_path)

    machine = json.loads((tmp_path / "index-report.json").read_text(encoding="utf-8"))
    assert machine["accepted"] == ["SRC-MAR-9001"]
    assert (tmp_path / "index-report.md").read_text(encoding="utf-8").startswith(
        "# Source Index Report"
    )
