from __future__ import annotations

import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from services.api.app.rag import (
    ChromaVectorStore,
    DeterministicTestEmbeddingProvider,
    SourceIndexer,
)
from services.api.app.sources import SourceRecord

ROOT = Path(__file__).resolve().parents[3]


def load_records(input_directory: Path) -> tuple[list[SourceRecord], list[str]]:
    records: list[SourceRecord] = []
    rejected: list[str] = []
    for path in sorted(input_directory.glob("*.json")):
        try:
            records.append(SourceRecord.model_validate_json(path.read_text(encoding="utf-8")))
        except (ValidationError, ValueError, json.JSONDecodeError):
            rejected.append(path.name)
    return records, rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and index registered source fixtures.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--index", type=Path, default=ROOT / "data" / "index")
    parser.add_argument("--report", type=Path, default=ROOT / "data" / "index-reports")
    parser.add_argument(
        "--test-embedding",
        action="store_true",
        help="Use deterministic synthetic embeddings. Required until ADR-010 is accepted.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.test_embedding:
        raise SystemExit(
            "No production embedding model is approved. Use --test-embedding only for fixtures."
        )
    records, invalid_files = load_records(args.input)
    store = ChromaVectorStore(persist_path=args.index)
    report = SourceIndexer(store, DeterministicTestEmbeddingProvider()).index(records)
    report.rejected.extend(invalid_files)
    report.write(args.report)
    print((args.report / "index-report.json").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
