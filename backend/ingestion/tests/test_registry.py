from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from backend.ingestion.publication_boundary import (
    PublicationBoundaryError,
    to_runtime_source_record,
)
from backend.ingestion.registry import SourceRegistry
from backend.ingestion.registry.models import SourceRegistryDocument
from backend.ingestion.registry.service import normalize_filename, sha256_file


def pdf(path: Path, payload: bytes = b"controlled") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"%PDF-1.7\n" + payload)
    return path


def test_registers_untrusted_record_and_immutable_original(tmp_path: Path) -> None:
    source = pdf(tmp_path / "drop" / "İbn Sina - Şifa.pdf")
    library = tmp_path / "library"
    result = SourceRegistry(library).register_file(source)

    assert not result.exact_duplicate
    assert result.record.intake_status.value == "REGISTERED"
    assert result.record.trust_status.value == "UNTRUSTED"
    assert result.record.original_filename == "İbn Sina - Şifa.pdf"
    assert result.record.normalized_filename == "ibn_sina_sifa.pdf"
    assert result.record.title == "UNKNOWN"
    original = library / result.record.original_relative_path
    assert original.read_bytes() == source.read_bytes()
    assert sha256_file(original) == result.record.sha256


def test_exact_duplicate_is_idempotent_and_preserves_one_record(tmp_path: Path) -> None:
    first = pdf(tmp_path / "one.pdf", b"same")
    second = pdf(tmp_path / "nested" / "renamed.pdf", b"same")
    registry = SourceRegistry(tmp_path / "library")

    initial = registry.register_file(first)
    duplicate = registry.register_file(second)
    document = SourceRegistryDocument.model_validate_json(
        registry.registry_path.read_text(encoding="utf-8")
    )

    assert duplicate.exact_duplicate
    assert duplicate.record.source_id == initial.record.source_id
    assert len(document.records) == 1
    events = registry.audit_path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(event)["event_type"] for event in events] == [
        "SOURCE_REGISTERED",
        "EXACT_DUPLICATE_SKIPPED",
    ]


def test_normalized_filename_collision_does_not_overwrite_original(tmp_path: Path) -> None:
    first = pdf(tmp_path / "Book Name.pdf", b"first")
    second = pdf(tmp_path / "Book-Name.pdf", b"second")
    registry = SourceRegistry(tmp_path / "library")

    first_result = registry.register_file(first)
    second_result = registry.register_file(second)

    assert first_result.record.normalized_filename == "book_name.pdf"
    assert second_result.record.normalized_filename == "book_name.pdf"
    assert first_result.record.original_relative_path != second_result.record.original_relative_path
    assert len(list(registry.originals_root.rglob("*.pdf"))) == 2


@pytest.mark.parametrize(
    ("name", "content", "message"),
    [
        ("not-pdf.txt", b"%PDF-1.7\ntext", "only .pdf"),
        ("fake.pdf", b"not a pdf", "invalid PDF header"),
        ("empty.pdf", b"", "empty files"),
    ],
)
def test_rejects_unsupported_or_invalid_files(
    tmp_path: Path, name: str, content: bytes, message: str
) -> None:
    source = tmp_path / name
    source.write_bytes(content)
    with pytest.raises(ValueError, match=message):
        SourceRegistry(tmp_path / "library").register_file(source)


def test_rejects_oversized_file(tmp_path: Path) -> None:
    source = pdf(tmp_path / "large.pdf", b"x" * 32)
    with pytest.raises(ValueError, match="byte limit"):
        SourceRegistry(tmp_path / "library", max_file_bytes=16).register_file(source)


def test_interrupted_atomic_copy_leaves_no_record_or_partial_original(tmp_path: Path) -> None:
    source = pdf(tmp_path / "source.pdf")
    registry = SourceRegistry(tmp_path / "library")

    with patch("backend.ingestion.registry.service.os.replace", side_effect=OSError("stop")):
        with pytest.raises(OSError, match="stop"):
            registry.register_file(source)

    assert not registry.registry_path.exists()
    assert not list(registry.originals_root.rglob("*.pdf"))
    assert not list(registry.originals_root.rglob(".intake-*.tmp"))


def test_folder_import_is_deterministic_and_ignores_non_pdf(tmp_path: Path) -> None:
    folder = tmp_path / "drop"
    second = pdf(folder / "b.pdf", b"b")
    first = pdf(folder / "a.pdf", b"a")
    (folder / "notes.txt").write_text("not input", encoding="utf-8")
    registry = SourceRegistry(tmp_path / "library")

    results = registry.register_folder(folder)

    assert [item.record.original_filename for item in results] == [first.name, second.name]
    assert len(SourceRegistryDocument.model_validate_json(
        registry.registry_path.read_text(encoding="utf-8")
    ).records) == 2


def test_registry_detects_manifest_tampering(tmp_path: Path) -> None:
    registry = SourceRegistry(tmp_path / "library")
    result = registry.register_file(pdf(tmp_path / "source.pdf"))
    payload = json.loads(registry.registry_path.read_text(encoding="utf-8"))
    payload["records"].append(payload["records"][0])
    registry.registry_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate source_id"):
        registry.register_file(pdf(tmp_path / "other.pdf", b"other"))
    assert result.record.source_id.startswith("KS-SRC-")


def test_ks01_record_cannot_cross_runtime_publication_boundary(tmp_path: Path) -> None:
    record = SourceRegistry(tmp_path / "library").register_file(
        pdf(tmp_path / "source.pdf")
    ).record
    with pytest.raises(PublicationBoundaryError, match="REGISTERED and UNTRUSTED"):
        to_runtime_source_record(record)


def test_filename_normalization_never_uses_parent_components() -> None:
    assert normalize_filename("../../Üçüncü Kitap.PDF") == "ucuncu_kitap.pdf"
