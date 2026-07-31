from __future__ import annotations

import hashlib
import json
import os
import tempfile
from fcntl import LOCK_EX, LOCK_UN, flock
from pathlib import Path
from typing import Callable, Literal, TypeVar

from backend.ingestion.provenance.models import (
    EvidenceReference,
    MetadataAuditEvent,
    MetadataCandidate,
    MetadataField,
    MetadataWorkspaceDocument,
    MetadataWorkspaceRecord,
    ProvenanceRecord,
)
from backend.ingestion.registry.models import UNKNOWN, SourceRegistryDocument
from backend.ingestion.registry.service import utc_now

T = TypeVar("T")


class MetadataConflictError(RuntimeError):
    pass


class MetadataWorkspace:
    """Evidence-backed KS-02 workspace separate from the immutable KS-01 registry."""

    def __init__(self, library_root: Path) -> None:
        self.library_root = library_root
        self.manifests_root = library_root / "manifests"
        self.reports_root = library_root / "reports"
        self.registry_path = self.manifests_root / "source_registry.json"
        self.workspace_path = self.manifests_root / "metadata_workspace.json"
        self.audit_path = self.manifests_root / "metadata_audit.jsonl"
        self.lock_path = self.manifests_root / ".metadata.lock"

    def initialize(self) -> MetadataWorkspaceDocument:
        return self._mutate(self._initialize_locked)

    def add_candidate(
        self,
        *,
        source_id: str,
        field_name: MetadataField,
        value: str,
        evidence: list[EvidenceReference],
        actor: str,
        expected_version: int,
        confidence: float | None = None,
        supersedes_candidate_id: str | None = None,
    ) -> MetadataCandidate:
        def operation() -> MetadataCandidate:
            workspace = self._initialize_locked()
            record = self._record(workspace, source_id)
            self._expect_version(record, expected_version)
            now = utc_now()
            identity = json.dumps(
                {
                    "source_id": source_id,
                    "field": field_name.value,
                    "value": value,
                    "evidence": [item.model_dump(mode="json") for item in evidence],
                    "actor": actor,
                    "created_at": now,
                },
                sort_keys=True,
            )
            candidate = MetadataCandidate(
                candidate_id=f"KS-MDC-{self._fingerprint(identity)[:24]}",
                source_id=source_id,
                field_name=field_name,
                value=value,
                evidence=evidence,
                confidence=confidence,
                state=(
                    "CANDIDATE_CAPTURED"
                    if value == UNKNOWN
                    else "HUMAN_REVIEW_REQUIRED"
                ),
                created_at=now,
                created_by=actor,
                supersedes_candidate_id=supersedes_candidate_id,
            )
            updated_record = MetadataWorkspaceRecord.model_validate(
                {
                    **record.model_dump(mode="json"),
                    "version": record.version + 1,
                    "candidates": [
                        *[item.model_dump(mode="json") for item in record.candidates],
                        candidate.model_dump(mode="json"),
                    ],
                }
            )
            updated = self._replace_record(workspace, updated_record)
            self._write_workspace(updated)
            self._append_audit(
                event_type="METADATA_CANDIDATE_ADDED",
                actor=actor,
                source_id=source_id,
                workspace_version=updated_record.version,
                details={
                    "candidate_id": candidate.candidate_id,
                    "field_name": field_name.value,
                    "state": candidate.state,
                },
            )
            return candidate

        return self._mutate(operation)

    def review_candidate(
        self,
        *,
        source_id: str,
        candidate_id: str,
        decision: str,
        actor: str,
        actor_role: str,
        reason: str,
        expected_version: int,
    ) -> MetadataCandidate:
        if actor_role != "HUMAN_METADATA_REVIEWER":
            raise PermissionError("metadata review requires HUMAN_METADATA_REVIEWER")
        if decision not in {"VERIFIED", "REJECTED"}:
            raise ValueError("decision must be VERIFIED or REJECTED")

        def operation() -> MetadataCandidate:
            workspace = self._initialize_locked()
            record = self._record(workspace, source_id)
            self._expect_version(record, expected_version)
            current = next(
                (item for item in record.candidates if item.candidate_id == candidate_id),
                None,
            )
            if current is None:
                raise KeyError(f"unknown candidate: {candidate_id}")
            if current.state in {"VERIFIED", "REJECTED"}:
                raise MetadataConflictError("candidate already has a review decision")
            reviewed = MetadataCandidate.model_validate(
                {
                    **current.model_dump(mode="json"),
                    "state": decision,
                    "reviewed_at": utc_now(),
                    "reviewed_by": actor,
                    "review_reason": reason,
                }
            )
            candidates = [
                reviewed if item.candidate_id == candidate_id else item
                for item in record.candidates
            ]
            updated_record = MetadataWorkspaceRecord.model_validate(
                {
                    **record.model_dump(mode="json"),
                    "version": record.version + 1,
                    "candidates": [
                        item.model_dump(mode="json") for item in candidates
                    ],
                }
            )
            updated = self._replace_record(workspace, updated_record)
            self._write_workspace(updated)
            self._append_audit(
                event_type="METADATA_CANDIDATE_REVIEWED",
                actor=actor,
                source_id=source_id,
                workspace_version=updated_record.version,
                details={
                    "candidate_id": candidate_id,
                    "decision": decision,
                    "metadata_only": "true",
                },
            )
            return reviewed

        return self._mutate(operation)

    def add_provenance(
        self,
        *,
        source_id: str,
        statement: str,
        evidence: list[EvidenceReference],
        actor: str,
        expected_version: int,
        supersedes_provenance_id: str | None = None,
    ) -> ProvenanceRecord:
        def operation() -> ProvenanceRecord:
            workspace = self._initialize_locked()
            record = self._record(workspace, source_id)
            self._expect_version(record, expected_version)
            now = utc_now()
            identity = json.dumps(
                {
                    "source_id": source_id,
                    "statement": statement,
                    "evidence": [item.model_dump(mode="json") for item in evidence],
                    "actor": actor,
                    "recorded_at": now,
                },
                sort_keys=True,
            )
            provenance = ProvenanceRecord(
                provenance_id=f"KS-PRV-{self._fingerprint(identity)[:24]}",
                source_id=source_id,
                statement=statement,
                evidence=evidence,
                recorded_at=now,
                recorded_by=actor,
                supersedes_provenance_id=supersedes_provenance_id,
            )
            updated_record = MetadataWorkspaceRecord.model_validate(
                {
                    **record.model_dump(mode="json"),
                    "version": record.version + 1,
                    "provenance": [
                        *[item.model_dump(mode="json") for item in record.provenance],
                        provenance.model_dump(mode="json"),
                    ],
                }
            )
            updated = self._replace_record(workspace, updated_record)
            self._write_workspace(updated)
            self._append_audit(
                event_type="PROVENANCE_RECORDED",
                actor=actor,
                source_id=source_id,
                workspace_version=updated_record.version,
                details={"provenance_id": provenance.provenance_id},
            )
            return provenance

        return self._mutate(operation)

    def export_report(self, destination: Path, *, actor: str) -> Path:
        workspace = self.initialize()
        registry = self._load_registry()
        by_source = {item.source_id: item for item in workspace.records}
        sources: list[dict[str, object]] = []
        report: dict[str, object] = {
            "schema_version": 1,
            "generated_at": utc_now(),
            "metadata_only": True,
            "legal_approval": False,
            "subject_approval": False,
            "safety_approval": False,
            "publication_approval": False,
            "sources": sources,
        }
        for source in registry.records:
            record = by_source[source.source_id]
            values: dict[str, list[dict[str, object]]] = {}
            for candidate in record.candidates:
                values.setdefault(candidate.field_name.value, []).append(
                    candidate.model_dump(mode="json")
                )
            sources.append(
                {
                    "source_id": source.source_id,
                    "registry_sha256": source.sha256,
                    "intake_status": source.intake_status.value,
                    "trust_status": source.trust_status.value,
                    "workspace_version": record.version,
                    "metadata_candidates": values,
                    "provenance": [
                        item.model_dump(mode="json") for item in record.provenance
                    ],
                    "unresolved_fields": [
                        field.value
                        for field in MetadataField
                        if not values.get(field.value)
                    ],
                }
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        self._atomic_write(
            destination,
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        )
        self._append_audit(
            event_type="METADATA_EXPORT_CREATED",
            actor=actor,
            source_id=None,
            workspace_version=None,
            details={
                "destination": str(destination.relative_to(self.library_root)),
                "source_count": str(len(registry.records)),
            },
        )
        return destination

    def import_workspace(self, source: Path, *, actor: str) -> int:
        """Idempotently import validated candidate/provenance records, never approvals."""

        imported = MetadataWorkspaceDocument.model_validate_json(
            source.read_text(encoding="utf-8")
        )

        def operation() -> int:
            current = self._initialize_locked()
            current_by_source = {item.source_id: item for item in current.records}
            changed = 0
            replacements: dict[str, MetadataWorkspaceRecord] = {}
            for incoming in imported.records:
                source_changed = 0
                target = current_by_source.get(incoming.source_id)
                if target is None:
                    raise KeyError(
                        f"import references unknown registered source: {incoming.source_id}"
                    )
                if incoming.registry_sha256 != target.registry_sha256:
                    raise RuntimeError("import registry fingerprint mismatch")
                candidates = {item.candidate_id: item for item in target.candidates}
                provenance = {item.provenance_id: item for item in target.provenance}
                for candidate in incoming.candidates:
                    existing_candidate = candidates.get(candidate.candidate_id)
                    if (
                        existing_candidate is not None
                        and existing_candidate != candidate
                    ):
                        raise MetadataConflictError(
                            "candidate ID collision with different content"
                        )
                    if existing_candidate is None:
                        if candidate.state in {"VERIFIED", "REJECTED"}:
                            raise PermissionError(
                                "imports cannot introduce review decisions"
                            )
                        candidates[candidate.candidate_id] = candidate
                        changed += 1
                        source_changed += 1
                for record in incoming.provenance:
                    existing_provenance = provenance.get(record.provenance_id)
                    if (
                        existing_provenance is not None
                        and existing_provenance != record
                    ):
                        raise MetadataConflictError(
                            "provenance ID collision with different content"
                        )
                    if existing_provenance is None:
                        provenance[record.provenance_id] = record
                        changed += 1
                        source_changed += 1
                if source_changed:
                    replacements[incoming.source_id] = MetadataWorkspaceRecord(
                        source_id=target.source_id,
                        registry_sha256=target.registry_sha256,
                        version=target.version + 1,
                        candidates=list(candidates.values()),
                        provenance=list(provenance.values()),
                    )
            if replacements:
                updated = MetadataWorkspaceDocument(
                    records=[
                        replacements.get(item.source_id, item)
                        for item in current.records
                    ]
                )
                self._write_workspace(updated)
            self._append_audit(
                event_type="METADATA_IMPORT_APPLIED",
                actor=actor,
                source_id=None,
                workspace_version=None,
                details={
                    "input_sha256": self._fingerprint(source.read_text(encoding="utf-8")),
                    "records_added": str(changed),
                },
            )
            return changed

        return self._mutate(operation)

    def load(self) -> MetadataWorkspaceDocument:
        if not self.workspace_path.exists():
            return MetadataWorkspaceDocument()
        return MetadataWorkspaceDocument.model_validate_json(
            self.workspace_path.read_text(encoding="utf-8")
        )

    def _initialize_locked(self) -> MetadataWorkspaceDocument:
        registry = self._load_registry()
        workspace = self.load()
        existing = {item.source_id: item for item in workspace.records}
        changed = False
        records: list[MetadataWorkspaceRecord] = []
        for source in registry.records:
            current = existing.pop(source.source_id, None)
            if current is None:
                current = MetadataWorkspaceRecord(
                    source_id=source.source_id,
                    registry_sha256=source.sha256,
                )
                changed = True
            elif current.registry_sha256 != source.sha256:
                raise RuntimeError("workspace registry fingerprint mismatch")
            records.append(current)
        if existing:
            raise RuntimeError("workspace references source absent from registry")
        initialized = MetadataWorkspaceDocument(records=records)
        if changed or not self.workspace_path.exists():
            self._write_workspace(initialized)
        return initialized

    def _load_registry(self) -> SourceRegistryDocument:
        if not self.registry_path.exists():
            raise FileNotFoundError("KS-01 source registry does not exist")
        return SourceRegistryDocument.model_validate_json(
            self.registry_path.read_text(encoding="utf-8")
        )

    @staticmethod
    def _record(
        workspace: MetadataWorkspaceDocument, source_id: str
    ) -> MetadataWorkspaceRecord:
        record = next(
            (item for item in workspace.records if item.source_id == source_id),
            None,
        )
        if record is None:
            raise KeyError(f"unknown registered source: {source_id}")
        return record

    @staticmethod
    def _expect_version(record: MetadataWorkspaceRecord, expected: int) -> None:
        if record.version != expected:
            raise MetadataConflictError(
                f"workspace version conflict: expected {expected}, actual {record.version}"
            )

    @staticmethod
    def _replace_record(
        workspace: MetadataWorkspaceDocument, replacement: MetadataWorkspaceRecord
    ) -> MetadataWorkspaceDocument:
        return MetadataWorkspaceDocument(
            records=[
                replacement if item.source_id == replacement.source_id else item
                for item in workspace.records
            ]
        )

    def _write_workspace(self, workspace: MetadataWorkspaceDocument) -> None:
        self.manifests_root.mkdir(parents=True, exist_ok=True)
        self._atomic_write(
            self.workspace_path,
            workspace.model_dump_json(indent=2) + "\n",
        )

    @staticmethod
    def _atomic_write(path: Path, payload: str) -> None:
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                prefix=f".{path.name}-",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temporary = Path(handle.name)
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()

    def _append_audit(
        self,
        *,
        event_type: Literal[
            "METADATA_CANDIDATE_ADDED",
            "METADATA_CANDIDATE_REVIEWED",
            "PROVENANCE_RECORDED",
            "METADATA_IMPORT_APPLIED",
            "METADATA_EXPORT_CREATED",
        ],
        actor: str,
        source_id: str | None,
        workspace_version: int | None,
        details: dict[str, str],
    ) -> None:
        occurred_at = utc_now()
        identity = json.dumps(
            {
                "event_type": event_type,
                "occurred_at": occurred_at,
                "actor": actor,
                "source_id": source_id,
                "details": details,
            },
            sort_keys=True,
        )
        event = MetadataAuditEvent(
            event_id=f"KS-MEV-{self._fingerprint(identity)[:24]}",
            event_type=event_type,
            occurred_at=occurred_at,
            actor=actor,
            source_id=source_id,
            workspace_version=workspace_version,
            details=details,
        )
        descriptor = os.open(
            self.audit_path,
            os.O_APPEND | os.O_CREAT | os.O_WRONLY,
            0o600,
        )
        try:
            os.write(descriptor, (event.model_dump_json() + "\n").encode())
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _mutate(self, operation: Callable[[], T]) -> T:
        self.manifests_root.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            flock(descriptor, LOCK_EX)
            return operation()
        finally:
            flock(descriptor, LOCK_UN)
            os.close(descriptor)

    @staticmethod
    def _fingerprint(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
