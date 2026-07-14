# Architecture Changelog

## 2026-07-13 — Sprint 04 Grounded Answer and Citation Engine

### Added

- Structured grounded-analysis contracts and `/api/v1/analyze/reflection` endpoint.
- Versioned prompt metadata, isolated untrusted context boundaries, and LLM provider
  abstraction with a controlled mock implementation.
- Citation allow-list, lexical support check, and answer-blocking validation failures.
- Stable source-limited, provider-unavailable, out-of-scope, injection, and medical
  redirect outcomes with a deterministic doctor notice.
- Safety fixtures and regression coverage for fake citations, unsupported claims,
  provider failures, prompt injection, medical advice, and log redaction.

### Boundary

- No production LLM provider, mobile result UI, questionnaire, journal, TTS, or
  multi-provider routing was added.

## 2026-07-13 — Sprint 03 Retrieval and Source Routing API

### Added

- Validated `/api/v1/search` contracts with stable empty and insufficient states.
- Deterministic intent classification and server-controlled Marifetname-first routing.
- Approved-only ChromaDB metadata filtering and separated supplementary results.
- Provider-neutral reranker boundary and a deterministic lexical implementation.
- Synthetic retrieval fixtures and a Recall@5 evaluation command.

### Boundary

- No generative answer, medical recommendation, citation prose, mobile search UI,
  journal, or TTS behavior was added.
- Production retrieval remains unavailable until an embedding model is approved and
  explicitly configured under ADR-010.

## 2026-07-13 — Sprint 02 Source Ingestion Pipeline

### Added

- Canonical validated source, page, and chunk contracts with stable hashes and IDs.
- Original-text-preserving normalization and prose/poetry/table chunking strategies.
- Approved-only production indexing, duplicate detection, idempotent replacement,
  ChromaDB persistence, and JSON/Markdown index reports.
- Provider-neutral embedding boundary with a deterministic synthetic test adapter.
- Synthetic primary and supplementary fixtures; no licensed source content.

### Boundary

- ADR-010 remains proposed, so no production embedding model was selected.
- No retrieval API, reranking, answer generation, or other Sprint 03 behavior was added.

## 2026-07-13 — Sprint 00 and Sprint 01 Foundation

### Added

- Source inventory, source-review workflow, copyright-review record, and mandatory
  medical notice.
- Proposed embedding-model evaluation ADR without selecting a provider or model.
- Explicit decision log and unresolved source/legal blockers.
- React Native CLI and FastAPI monorepo foundation, generated OpenAPI contracts,
  SQLite initialization shell, tests, Dockerfile, and CI quality gates.
- Pre-commit checks, dependency locks, repository templates, secret scanning, and
  empty data lifecycle directories.

### Boundaries Preserved

- No ingestion, embeddings, ChromaDB collection, retrieval, RAG, LLM provider,
  source routing, search, journal, or TTS implementation was added.
