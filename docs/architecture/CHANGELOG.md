# Architecture Changelog

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
