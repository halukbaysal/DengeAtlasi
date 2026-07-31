from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from backend.ingestion.provenance import EvidenceReference, MetadataField, MetadataWorkspace


def _evidence(args: argparse.Namespace) -> list[EvidenceReference]:
    if args.value == "UNKNOWN":
        return []
    required = (
        args.evidence_kind,
        args.evidence_locator,
        args.evidence_description,
        args.evidence_sha256,
    )
    if any(value is None for value in required):
        raise ValueError("non-UNKNOWN values require complete evidence arguments")
    identity = json.dumps(
        {
            "source_id": args.source_id,
            "kind": args.evidence_kind,
            "locator": args.evidence_locator,
            "sha256": args.evidence_sha256,
            "page": args.evidence_page,
        },
        sort_keys=True,
    )
    evidence_id = f"KS-EVD-{hashlib.sha256(identity.encode()).hexdigest()[:24]}"
    return [
        EvidenceReference(
            evidence_id=evidence_id,
            source_id=args.source_id,
            kind=args.evidence_kind,
            locator=args.evidence_locator,
            description=args.evidence_description,
            artifact_sha256=args.evidence_sha256,
            page=args.evidence_page,
        )
    ]


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="KS-02 evidence-backed metadata workspace; no OCR or approvals"
    )
    root.add_argument(
        "--library",
        type=Path,
        default=Path("data/source-library"),
        help="Local source-library root",
    )
    subcommands = root.add_subparsers(dest="command", required=True)

    subcommands.add_parser("initialize")

    export = subcommands.add_parser("export")
    export.add_argument("--output", type=Path)
    export.add_argument("--actor", required=True)

    import_workspace = subcommands.add_parser("import-workspace")
    import_workspace.add_argument("--input", type=Path, required=True)
    import_workspace.add_argument("--actor", required=True)

    candidate = subcommands.add_parser("add-candidate")
    candidate.add_argument("--source-id", required=True)
    candidate.add_argument("--field", choices=[item.value for item in MetadataField], required=True)
    candidate.add_argument("--value", required=True)
    candidate.add_argument("--actor", required=True)
    candidate.add_argument("--expected-version", type=int, required=True)
    candidate.add_argument("--confidence", type=float)
    candidate.add_argument("--supersedes")
    candidate.add_argument(
        "--evidence-kind",
        choices=["PAGE", "FILE_LOCATION", "BIBLIOGRAPHIC_RECORD", "MANUAL_NOTE"],
    )
    candidate.add_argument("--evidence-locator")
    candidate.add_argument("--evidence-description")
    candidate.add_argument("--evidence-sha256")
    candidate.add_argument("--evidence-page", type=int)

    review = subcommands.add_parser("review")
    review.add_argument("--source-id", required=True)
    review.add_argument("--candidate-id", required=True)
    review.add_argument("--decision", choices=["VERIFIED", "REJECTED"], required=True)
    review.add_argument("--actor", required=True)
    review.add_argument("--actor-role", required=True)
    review.add_argument("--reason", required=True)
    review.add_argument("--expected-version", type=int, required=True)

    provenance = subcommands.add_parser("add-provenance")
    provenance.add_argument("--source-id", required=True)
    provenance.add_argument("--statement", required=True)
    provenance.add_argument("--actor", required=True)
    provenance.add_argument("--expected-version", type=int, required=True)
    provenance.add_argument("--supersedes")
    provenance.add_argument(
        "--evidence-kind",
        choices=["PAGE", "FILE_LOCATION", "BIBLIOGRAPHIC_RECORD", "MANUAL_NOTE"],
        required=True,
    )
    provenance.add_argument("--evidence-locator", required=True)
    provenance.add_argument("--evidence-description", required=True)
    provenance.add_argument("--evidence-sha256", required=True)
    provenance.add_argument("--evidence-page", type=int)
    return root


def main() -> int:
    args = parser().parse_args()
    workspace = MetadataWorkspace(args.library)
    if args.command == "initialize":
        document = workspace.initialize()
        print(f"metadata workspace initialized for {len(document.records)} sources")
        return 0
    if args.command == "export":
        destination = args.output or args.library / "reports" / "ks02_metadata_report.json"
        print(workspace.export_report(destination, actor=args.actor))
        return 0
    if args.command == "import-workspace":
        added = workspace.import_workspace(args.input, actor=args.actor)
        print(f"metadata workspace import added {added} records")
        return 0
    if args.command == "add-candidate":
        candidate = workspace.add_candidate(
            source_id=args.source_id,
            field_name=MetadataField(args.field),
            value=args.value,
            evidence=_evidence(args),
            actor=args.actor,
            expected_version=args.expected_version,
            confidence=args.confidence,
            supersedes_candidate_id=args.supersedes,
        )
        print(f"{candidate.candidate_id} / {candidate.state}")
        return 0
    if args.command == "review":
        candidate = workspace.review_candidate(
            source_id=args.source_id,
            candidate_id=args.candidate_id,
            decision=args.decision,
            actor=args.actor,
            actor_role=args.actor_role,
            reason=args.reason,
            expected_version=args.expected_version,
        )
        print(f"{candidate.candidate_id} / {candidate.state} / metadata-only")
        return 0
    if args.command == "add-provenance":
        args.value = args.statement
        provenance = workspace.add_provenance(
            source_id=args.source_id,
            statement=args.statement,
            evidence=_evidence(args),
            actor=args.actor,
            expected_version=args.expected_version,
            supersedes_provenance_id=args.supersedes,
        )
        print(provenance.provenance_id)
        return 0
    raise RuntimeError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
