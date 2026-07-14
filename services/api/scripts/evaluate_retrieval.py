from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import chromadb

from services.api.app.contracts import SearchRequest
from services.api.app.domain import SearchService
from services.api.app.rag import (
    ChromaVectorStore,
    DeterministicTestEmbeddingProvider,
    SourceIndexer,
)
from services.api.scripts.index_sources import load_records

ROOT = Path(__file__).resolve().parents[3]


def recall_at_k(service: SearchService, cases: list[dict[str, Any]], top_k: int = 5) -> float:
    relevant = 0
    retrieved_relevant = 0
    for case in cases:
        response = service.search(SearchRequest(query=case["query"], top_k=top_k))
        retrieved = {
            result.source_id for group in response.groups for result in group.results[:top_k]
        }
        expected = set(case["expectedSourceIds"])
        relevant += len(expected)
        retrieved_relevant += len(expected & retrieved)
    return retrieved_relevant / relevant if relevant else 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure retrieval Recall@5 on synthetic fixtures."
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=(
            ROOT
            / "services"
            / "api"
            / "tests"
            / "fixtures"
            / "sprint03"
            / "retrieval_eval.json"
        ),
    )
    parser.add_argument(
        "--sources",
        type=Path,
        default=ROOT / "services" / "api" / "tests" / "fixtures" / "sprint02",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records, _ = load_records(args.sources)
    provider = DeterministicTestEmbeddingProvider()
    store = ChromaVectorStore(
        client=chromadb.EphemeralClient(), collection_name="retrieval_evaluation"
    )
    SourceIndexer(store, provider).index(records)
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    recall = recall_at_k(SearchService(store, provider), cases, top_k=5)
    print(json.dumps({"metric": "Recall@5", "value": recall, "cases": len(cases)}))
    return 0 if recall >= 0.85 else 1


if __name__ == "__main__":
    raise SystemExit(main())
