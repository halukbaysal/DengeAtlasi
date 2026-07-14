# Architecture Changelog

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
