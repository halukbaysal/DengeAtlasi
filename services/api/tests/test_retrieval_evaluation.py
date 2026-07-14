import json
from pathlib import Path

import chromadb
from services.api.app.domain import SearchService
from services.api.app.rag import (
    ChromaVectorStore,
    DeterministicTestEmbeddingProvider,
    SourceIndexer,
)
from services.api.scripts.evaluate_retrieval import recall_at_k
from services.api.scripts.index_sources import load_records

FIXTURES = Path(__file__).parent / "fixtures"


def test_synthetic_retrieval_recall_at_five_meets_gate() -> None:
    records, _ = load_records(FIXTURES / "sprint02")
    provider = DeterministicTestEmbeddingProvider()
    store = ChromaVectorStore(client=chromadb.EphemeralClient(), collection_name="eval_test")
    SourceIndexer(store, provider).index(records)
    cases = json.loads((FIXTURES / "sprint03" / "retrieval_eval.json").read_text())
    assert recall_at_k(SearchService(store, provider), cases) >= 0.85
