# Architecture Changelog

## 2026-07-13 — Sprint 09 Security, Safety, and Evaluation

- Added API payload/rate guards and metadata-only correlation logging.
- Added analytics allowlist enforcement, poisoning/injection gates, safety evaluation data,
  threat model, incident runbooks, red-team checklist, and release report.
- Preserved provider, source-governance, medical-safety, and no-biometric boundaries.

## 2026-07-13 — Sprint 08 Device-Native TTS

### Added

- Platform-neutral TTS interface and `react-native-tts` 4.1.1 native adapter.
- Explicit play/resume, pause-with-stop-fallback, stop, and bounded rate controls.
- Turkish offline-voice selection, unsupported-voice fallback, and visible-text
  preservation on errors.
- Navigation cleanup and background lifecycle stop behavior.
- Accessible controls for grounded results, temperament output, source detail, and
  local reflection content, plus a device validation checklist.

### Boundary

- No cloud TTS, network speech voice, audio generation/upload, voice cloning,
  autoplay, background programming, music, or therapeutic claim was added.

## 2026-07-13 — Sprint 07 Local Reflection Journal

### Added

- Versioned SQLite migration with a constrained `journal_entries` schema and index.
- Parameterized local repository CRUD, persistence, readable export, single-entry
  deletion, and delete-all behavior.
- Journal list, create/edit, detail, export, privacy copy, and destructive-action
  confirmation screens that remain available offline.
- User-triggered save-from-analysis and explicit analyze-entry actions with no retry
  queue or background submission.
- Regression tests for migrations, restart behavior, CRUD, export, deletion, payload
  limits, single-attempt network failure, and analytics payload boundaries.

### Boundary

- No account, cloud sync, server journal storage, automatic analysis, background
  resend, social sharing, or new native dependency was added.

## 2026-07-13 — Sprint 06 Temperament Analysis

### Added

- Adult, consented, self-report-only temperament request and response contracts.
- Server-controlled temperament retrieval that always queries Marifetname first and
  optionally labels Ibn Sina lifestyle context as a separate, reasoned supplement.
- Deterministic uncertainty templates, reflection questions, and low-risk wellbeing
  suggestion allow-list without personality scoring or definitive classification.
- Medical escalation and notice enforcement for symptoms, medication, treatment,
  and dosage input.
- Mobile consent, observations, thematic result, citation, source-limit, and medical
  safety presentation with generated-contract-backed Zod validation.

### Boundary

- No child or third-party analysis, modern personality framework, astrology, nafs
  ranking, facial inference, disease prediction, or treatment advice was added.

## 2026-07-13 — Sprint 05 Mobile Search and Source Experience

### Added

- Home, Ask, Grounded Result, and Source Detail mobile navigation flow.
- Generated-contract-backed API integration with strict Zod response validation.
- Accessible source cards, tappable citations, source-limit notice, medical notice,
  loading, offline, empty, and error states.
- Primary-source-first citation ordering and edition/page/section/author details.
- Compile-time analytics allow-list that cannot carry query, prompt, health, or
  source-excerpt payloads.

### Boundary

- No temperament questionnaire, journal persistence, TTS, authentication, sync,
  monetization, push notification, or new native dependency was added.

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
