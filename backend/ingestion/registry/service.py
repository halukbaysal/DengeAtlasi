from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import shutil
import tempfile
import unicodedata
from fcntl import LOCK_EX, LOCK_UN, flock
from datetime import datetime, timezone
from pathlib import Path

from backend.ingestion.registry.models import (
    IntakeAuditEvent,
    IntakeResult,
    KnowledgeSourceRecord,
    SourceRegistryDocument,
)

PDF_HEADER = b"%PDF-"
DEFAULT_MAX_FILE_BYTES = 512 * 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_filename(filename: str) -> str:
    basename = Path(filename).name
    stem = unicodedata.normalize("NFKD", Path(basename).stem)
    stem = stem.encode("ascii", "ignore").decode("ascii").casefold()
    stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")
    return f"{stem or 'document'}.pdf"


class SourceRegistry:
    def __init__(self, library_root: Path, *, max_file_bytes: int = DEFAULT_MAX_FILE_BYTES) -> None:
        self.library_root = library_root
        self.originals_root = library_root / "originals"
        self.manifests_root = library_root / "manifests"
        self.registry_path = self.manifests_root / "source_registry.json"
        self.audit_path = self.manifests_root / "intake_audit.jsonl"
        self.lock_path = self.manifests_root / ".intake.lock"
        self.max_file_bytes = max_file_bytes

    def register_file(self, source: Path) -> IntakeResult:
        source = source.resolve()
        self._validate_source(source)
        self.manifests_root.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            flock(descriptor, LOCK_EX)
            return self._register_file_locked(source)
        finally:
            flock(descriptor, LOCK_UN)
            os.close(descriptor)

    def _register_file_locked(self, source: Path) -> IntakeResult:
        checksum = sha256_file(source)
        registry = self._load()
        existing = next((item for item in registry.records if item.sha256 == checksum), None)
        if existing is not None:
            self._append_audit("EXACT_DUPLICATE_SKIPPED", existing, source.name)
            return IntakeResult(record=existing, exact_duplicate=True)

        imported_at = utc_now()
        record = KnowledgeSourceRecord(
            source_id=f"KS-SRC-{checksum[:20]}",
            original_filename=source.name,
            normalized_filename=normalize_filename(source.name),
            original_relative_path=f"originals/{checksum[:2]}/{checksum}.pdf",
            sha256=checksum,
            file_size_bytes=source.stat().st_size,
            mime_type="application/pdf",
            imported_at=imported_at,
        )
        self._preserve_original(source, record)
        updated = SourceRegistryDocument(records=[*registry.records, record])
        self._write_registry(updated)
        try:
            self._append_audit("SOURCE_REGISTERED", record, source.name)
        except Exception:
            self._write_registry(registry)
            raise
        return IntakeResult(record=record, exact_duplicate=False)

    def register_folder(self, folder: Path) -> list[IntakeResult]:
        if not folder.is_dir():
            raise ValueError(f"not a directory: {folder}")
        return [self.register_file(path) for path in sorted(folder.glob("*.pdf"))]

    def _validate_source(self, source: Path) -> None:
        if not source.is_file():
            raise ValueError(f"source is not a regular file: {source}")
        size = source.stat().st_size
        if size <= 0:
            raise ValueError("empty files are not accepted")
        if size > self.max_file_bytes:
            raise ValueError(f"file exceeds {self.max_file_bytes} byte limit")
        if source.suffix.casefold() != ".pdf":
            raise ValueError("only .pdf files are accepted")
        guessed, _ = mimetypes.guess_type(source.name)
        if guessed != "application/pdf":
            raise ValueError("file MIME type is not application/pdf")
        with source.open("rb") as handle:
            if handle.read(len(PDF_HEADER)) != PDF_HEADER:
                raise ValueError("invalid PDF header")

    def _load(self) -> SourceRegistryDocument:
        if not self.registry_path.exists():
            return SourceRegistryDocument()
        return SourceRegistryDocument.model_validate_json(
            self.registry_path.read_text(encoding="utf-8")
        )

    def _preserve_original(
        self, source: Path, record: KnowledgeSourceRecord
    ) -> None:
        destination = self.library_root / record.original_relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if sha256_file(destination) != record.sha256:
                raise RuntimeError("immutable original checksum mismatch")
            return
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=destination.parent,
                prefix=".intake-",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temporary = Path(handle.name)
                with source.open("rb") as source_handle:
                    shutil.copyfileobj(source_handle, handle, length=1024 * 1024)
                handle.flush()
                os.fsync(handle.fileno())
            if sha256_file(temporary) != record.sha256:
                raise RuntimeError("atomic copy checksum verification failed")
            os.replace(temporary, destination)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()

    def _write_registry(self, document: SourceRegistryDocument) -> None:
        self.manifests_root.mkdir(parents=True, exist_ok=True)
        payload = document.model_dump_json(indent=2) + "\n"
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.manifests_root,
                prefix=".registry-",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temporary = Path(handle.name)
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.registry_path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()

    def _append_audit(
        self,
        event_type: str,
        record: KnowledgeSourceRecord,
        observed_filename: str,
    ) -> None:
        self.manifests_root.mkdir(parents=True, exist_ok=True)
        occurred_at = utc_now()
        identity = "|".join(
            (event_type, occurred_at, record.source_id, observed_filename)
        )
        event = IntakeAuditEvent(
            event_id=f"KS-EVT-{hashlib.sha256(identity.encode()).hexdigest()[:24]}",
            event_type=event_type,
            occurred_at=occurred_at,
            source_id=record.source_id,
            sha256=record.sha256,
            original_filename=observed_filename,
            details={"intake_status": "REGISTERED", "trust_status": "UNTRUSTED"},
        )
        descriptor = os.open(
            self.audit_path,
            os.O_APPEND | os.O_CREAT | os.O_WRONLY,
            0o600,
        )
        try:
            os.write(descriptor, (event.model_dump_json() + "\n").encode("utf-8"))
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
