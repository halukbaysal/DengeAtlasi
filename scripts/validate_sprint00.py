"""Validate the static Sprint 00 governance deliverables without ingesting data."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SECTIONS: dict[str, tuple[str, ...]] = {
    "docs/source-registry/SOURCE_INVENTORY.md": (
        "Source ID",
        "Edition",
        "Review Status",
        "Copyright Status",
        "Approved Source Hierarchy",
        "Marifetname",
        "Ibn Sina",
    ),
    "docs/source-registry/SOURCE_REVIEW_TEMPLATE.md": (
        "UNREVIEWED",
        "OCR_REVIEWED",
        "CONTENT_REVIEWED",
        "APPROVED",
        "REJECTED",
    ),
    "docs/source-registry/COPYRIGHT_REVIEW_TEMPLATE.md": (
        "Edition",
        "Publisher",
        "Copyright holder",
        "Country / jurisdiction",
        "Evidence",
        "Usage Decision",
        "Reviewer",
        "Date",
    ),
    "docs/source-registry/MANDATORY_MEDICAL_NOTICE.md": (
        "does not diagnose disease",
        "does not prescribe treatment",
        "does not replace qualified healthcare professionals",
        "licensed healthcare professional",
    ),
    "docs/adr/ADR-010_EMBEDDING_MODEL.md": (
        "Status:** PROPOSED",
        "Evaluation Criteria",
        "Benchmarking Process",
        "Acceptance Requirements",
        "does not choose a model",
    ),
    "docs/architecture/DECISION_LOG.md": (
        "Completed Decisions",
        "Pending Decisions",
        "Rationale",
        "2026-07-13",
    ),
}

SOURCE_ID_PATTERN = re.compile(r"`(SRC-[A-Z]{3}-\d{4})`")


def validate_required_content() -> list[str]:
    errors: list[str] = []
    for relative_path, required_text in REQUIRED_SECTIONS.items():
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"missing file: {relative_path}")
            continue
        content = path.read_text(encoding="utf-8")
        for text in required_text:
            if text not in content:
                errors.append(f"{relative_path}: missing required text: {text}")
    return errors


def validate_source_ids() -> list[str]:
    inventory = (ROOT / "docs/source-registry/SOURCE_INVENTORY.md").read_text(
        encoding="utf-8"
    )
    source_ids = SOURCE_ID_PATTERN.findall(inventory)
    duplicates = sorted({source_id for source_id in source_ids if source_ids.count(source_id) > 1})
    return [f"duplicate source ID: {source_id}" for source_id in duplicates]


def validate_data_directories() -> list[str]:
    required = (
        "data/raw/marifetname",
        "data/raw/ibn_sina",
        "data/reviewed",
        "data/normalized",
        "data/chunks",
        "data/embeddings",
    )
    return [f"missing directory: {path}" for path in required if not (ROOT / path).is_dir()]


def main() -> int:
    errors = validate_required_content() + validate_source_ids() + validate_data_directories()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Sprint 00 document validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
