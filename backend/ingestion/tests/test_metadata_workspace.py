from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from backend.ingestion.provenance import (
    EvidenceReference,
    MetadataField,
    MetadataWorkspace,
)
from backend.ingestion.provenance.service import MetadataConflictError
from backend.ingestion.publication_boundary import (
    PublicationBoundaryError,
    to_runtime_source_record,
)
from backend.ingestion.registry import SourceRegistry
from backend.ingestion.registry.models import SourceRegistryDocument
from backend.ingestion.registry.service import sha256_file


def pdf(path: Path, payload: bytes = b"controlled") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"%PDF-1.7\n" + payload)
    return path


def registered(library: Path, name: str = "source.pdf", payload: bytes = b"one"):
    return SourceRegistry(library).register_file(pdf(library.parent / name, payload)).record


def evidence(source_id: str, label: str = "catalog") -> EvidenceReference:
    digest = hashlib.sha256(label.encode()).hexdigest()
    return EvidenceReference(
        evidence_id=f"KS-EVD-{digest[:24]}",
        source_id=source_id,
        kind="BIBLIOGRAPHIC_RECORD",
        locator=f"local-catalog:{label}",
        description="Human-provided catalog evidence",
        artifact_sha256=digest,
    )


def test_initialize_is_migration_free_and_preserves_registry_and_original(
    tmp_path: Path,
) -> None:
    library = tmp_path / "library"
    source = registered(library)
    registry_before = SourceRegistryDocument.model_validate_json(
        (library / "manifests/source_registry.json").read_text()
    )
    registry_bytes = (library / "manifests/source_registry.json").read_bytes()
    original = library / source.original_relative_path
    original_hash = sha256_file(original)

    workspace = MetadataWorkspace(library)
    first = workspace.initialize()
    second = workspace.initialize()

    assert first == second
    assert first.records[0].source_id == source.source_id
    assert first.records[0].registry_sha256 == source.sha256
    assert first.records[0].version == 0
    assert (library / "manifests/source_registry.json").read_bytes() == registry_bytes
    assert sha256_file(original) == original_hash
    assert registry_before.records[0].intake_status.value == "REGISTERED"
    assert registry_before.records[0].trust_status.value == "UNTRUSTED"


def test_unknown_is_explicit_and_requires_no_evidence(tmp_path: Path) -> None:
    library = tmp_path / "library"
    source = registered(library)
    workspace = MetadataWorkspace(library)
    workspace.initialize()

    candidate = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.TITLE,
        value="UNKNOWN",
        evidence=[],
        actor="metadata-operator",
        expected_version=0,
    )

    assert candidate.value == "UNKNOWN"
    assert candidate.evidence == []
    assert candidate.state == "CANDIDATE_CAPTURED"


def test_non_unknown_value_requires_explicit_evidence(tmp_path: Path) -> None:
    library = tmp_path / "library"
    source = registered(library)
    workspace = MetadataWorkspace(library)
    workspace.initialize()

    with pytest.raises(ValidationError, match="explicit evidence"):
        workspace.add_candidate(
            source_id=source.source_id,
            field_name=MetadataField.TITLE,
            value="A claimed title",
            evidence=[],
            actor="metadata-operator",
            expected_version=0,
        )


def test_conflicting_candidates_are_preserved_and_not_overwritten(
    tmp_path: Path,
) -> None:
    library = tmp_path / "library"
    source = registered(library)
    workspace = MetadataWorkspace(library)
    workspace.initialize()
    first = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.PUBLISHER,
        value="Publisher A",
        evidence=[evidence(source.source_id, "a")],
        actor="operator-a",
        expected_version=0,
    )
    second = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.PUBLISHER,
        value="Publisher B",
        evidence=[evidence(source.source_id, "b")],
        actor="operator-b",
        expected_version=1,
    )

    record = workspace.load().records[0]
    assert [item.value for item in record.candidates] == ["Publisher A", "Publisher B"]
    assert first.candidate_id != second.candidate_id
    assert all(item.state == "HUMAN_REVIEW_REQUIRED" for item in record.candidates)


def test_manual_correction_appends_history_and_requires_current_version(
    tmp_path: Path,
) -> None:
    library = tmp_path / "library"
    source = registered(library)
    workspace = MetadataWorkspace(library)
    workspace.initialize()
    first = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.PUBLICATION_YEAR,
        value="1901",
        evidence=[evidence(source.source_id, "year-a")],
        actor="operator",
        expected_version=0,
    )
    corrected = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.PUBLICATION_YEAR,
        value="1902",
        evidence=[evidence(source.source_id, "year-b")],
        actor="operator",
        expected_version=1,
        supersedes_candidate_id=first.candidate_id,
    )

    assert corrected.supersedes_candidate_id == first.candidate_id
    assert len(workspace.load().records[0].candidates) == 2
    with pytest.raises(MetadataConflictError, match="version conflict"):
        workspace.add_candidate(
            source_id=source.source_id,
            field_name=MetadataField.LANGUAGE,
            value="Turkish",
            evidence=[evidence(source.source_id, "language")],
            actor="stale-operator",
            expected_version=1,
        )


def test_review_requires_human_role_and_does_not_approve_source(
    tmp_path: Path,
) -> None:
    library = tmp_path / "library"
    source = registered(library)
    registry_bytes = (library / "manifests/source_registry.json").read_bytes()
    workspace = MetadataWorkspace(library)
    workspace.initialize()
    candidate = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.LANGUAGE,
        value="Turkish",
        evidence=[evidence(source.source_id, "language")],
        actor="operator",
        expected_version=0,
    )

    with pytest.raises(PermissionError, match="HUMAN_METADATA_REVIEWER"):
        workspace.review_candidate(
            source_id=source.source_id,
            candidate_id=candidate.candidate_id,
            decision="VERIFIED",
            actor="automation",
            actor_role="SYSTEM",
            reason="not allowed",
            expected_version=1,
        )
    reviewed = workspace.review_candidate(
        source_id=source.source_id,
        candidate_id=candidate.candidate_id,
        decision="VERIFIED",
        actor="human-reviewer-1",
        actor_role="HUMAN_METADATA_REVIEWER",
        reason="Evidence inspected manually",
        expected_version=1,
    )

    assert reviewed.state == "VERIFIED"
    assert (library / "manifests/source_registry.json").read_bytes() == registry_bytes
    registry = SourceRegistryDocument.model_validate_json(registry_bytes)
    assert registry.records[0].trust_status.value == "UNTRUSTED"
    with pytest.raises(PublicationBoundaryError):
        to_runtime_source_record(registry.records[0])


def test_unknown_cannot_be_verified_even_by_metadata_reviewer(
    tmp_path: Path,
) -> None:
    library = tmp_path / "library"
    source = registered(library)
    workspace = MetadataWorkspace(library)
    workspace.initialize()
    candidate = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.AUTHOR,
        value="UNKNOWN",
        evidence=[],
        actor="operator",
        expected_version=0,
    )

    with pytest.raises(ValidationError, match="UNKNOWN cannot be verified"):
        workspace.review_candidate(
            source_id=source.source_id,
            candidate_id=candidate.candidate_id,
            decision="VERIFIED",
            actor="human-reviewer",
            actor_role="HUMAN_METADATA_REVIEWER",
            reason="UNKNOWN is not a fact",
            expected_version=1,
        )
    assert workspace.load().records[0].version == 1


def test_provenance_is_evidence_backed_and_append_only(tmp_path: Path) -> None:
    library = tmp_path / "library"
    source = registered(library)
    workspace = MetadataWorkspace(library)
    workspace.initialize()

    first = workspace.add_provenance(
        source_id=source.source_id,
        statement="Acquired from a local institutional catalog export.",
        evidence=[evidence(source.source_id, "provenance-a")],
        actor="metadata-operator",
        expected_version=0,
    )
    second = workspace.add_provenance(
        source_id=source.source_id,
        statement="Catalog export was corrected by the operator.",
        evidence=[evidence(source.source_id, "provenance-b")],
        actor="metadata-operator",
        expected_version=1,
        supersedes_provenance_id=first.provenance_id,
    )

    record = workspace.load().records[0]
    assert len(record.provenance) == 2
    assert second.supersedes_provenance_id == first.provenance_id


def test_audit_events_append_for_metadata_operations(tmp_path: Path) -> None:
    library = tmp_path / "library"
    source = registered(library)
    workspace = MetadataWorkspace(library)
    workspace.initialize()
    candidate = workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.EDITION,
        value="First edition candidate",
        evidence=[evidence(source.source_id, "edition")],
        actor="operator",
        expected_version=0,
    )
    workspace.review_candidate(
        source_id=source.source_id,
        candidate_id=candidate.candidate_id,
        decision="REJECTED",
        actor="human-reviewer",
        actor_role="HUMAN_METADATA_REVIEWER",
        reason="Evidence does not establish edition",
        expected_version=1,
    )

    events = [
        json.loads(line)
        for line in workspace.audit_path.read_text().splitlines()
    ]
    assert [item["event_type"] for item in events] == [
        "METADATA_CANDIDATE_ADDED",
        "METADATA_CANDIDATE_REVIEWED",
    ]
    assert events[-1]["details"]["metadata_only"] == "true"


def test_export_is_repeatable_and_reports_all_registered_sources(
    tmp_path: Path,
) -> None:
    library = tmp_path / "library"
    first = registered(library, "one.pdf", b"one")
    second = registered(library, "two.pdf", b"two")
    workspace = MetadataWorkspace(library)
    workspace.initialize()
    destination = library / "reports/metadata.json"

    workspace.export_report(destination, actor="report-operator")
    first_report = json.loads(destination.read_text())
    workspace.export_report(destination, actor="report-operator")
    second_report = json.loads(destination.read_text())

    assert {item["source_id"] for item in first_report["sources"]} == {
        first.source_id,
        second.source_id,
    }
    assert [
        {key: value for key, value in item.items() if key != "generated_at"}
        for item in [first_report, second_report]
    ][0] == [
        {key: value for key, value in item.items() if key != "generated_at"}
        for item in [first_report, second_report]
    ][1]
    assert all(item["intake_status"] == "REGISTERED" for item in first_report["sources"])
    assert all(item["trust_status"] == "UNTRUSTED" for item in first_report["sources"])
    assert first_report["publication_approval"] is False


def test_workspace_import_is_validated_and_idempotent(tmp_path: Path) -> None:
    source_library = tmp_path / "source-library"
    source = registered(source_library, "same.pdf", b"same-content")
    source_workspace = MetadataWorkspace(source_library)
    source_workspace.initialize()
    source_workspace.add_candidate(
        source_id=source.source_id,
        field_name=MetadataField.SCRIPT,
        value="Arabic script",
        evidence=[evidence(source.source_id, "script")],
        actor="metadata-operator",
        expected_version=0,
    )

    target_library = tmp_path / "target-library"
    target = registered(target_library, "renamed.pdf", b"same-content")
    assert target.source_id == source.source_id
    target_workspace = MetadataWorkspace(target_library)
    target_workspace.initialize()

    first_added = target_workspace.import_workspace(
        source_workspace.workspace_path,
        actor="import-operator",
    )
    second_added = target_workspace.import_workspace(
        source_workspace.workspace_path,
        actor="import-operator",
    )

    assert first_added == 1
    assert second_added == 0
    record = target_workspace.load().records[0]
    assert record.version == 1
    assert [item.value for item in record.candidates] == ["Arabic script"]
