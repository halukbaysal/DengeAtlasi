from services.api.app.domain.reranking import LexicalReranker, RetrievalCandidate


def test_lexical_reranker_is_provider_independent_and_stable() -> None:
    reranker = LexicalReranker()
    candidates = [
        RetrievalCandidate("b", "unrelated words", {}, 0.9),
        RetrievalCandidate("a", "known balance topic", {}, 0.4),
    ]
    ranked = reranker.rerank("balance topic", candidates, top_k=1)
    assert reranker.provider_id == "lexical-default-v1"
    assert [candidate.chunk_id for candidate in ranked] == ["a"]
