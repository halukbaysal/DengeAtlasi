# KS-03 — OCR Orchestration and Text-Layer Assessment

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Assess existing text layers and produce reviewable OCR artifacts while preserving page mapping and immutable originals.

## Dependencies

KS-02 schemas available. OCR tool ADR selected. Human authorization for copyrighted local processing.

## In scope

- Text-layer coverage assessment
- Page sampling
- OCR job orchestration
- Page-level confidence
- Script/language hints
- Original page mapping
- OCR artifact manifests
- Retry/failure states
- Local-only generated outputs

## Out of scope

- Source approval
- Semantic classification
- Chunking
- Embeddings
- Production indexing
- Automatic correction of uncertain historical terms

## Required architecture

OCR artifacts are derived, replaceable, and versioned. Originals remain immutable. OCR engine configuration is recorded in a reproducibility manifest.

## Data and state rules

Page-level status and confidence are mandatory. Low-confidence pages enter a review queue. OCR completion does not imply textual correctness.

## Security and governance

OCR outputs remain outside Git. Resource limits, timeouts, malformed-PDF handling, and subprocess isolation are required.

## Required implementation work

Create OCR adapter interfaces, job manifests, page artifacts, text-layer assessor, CLI/service orchestration, and reports.

## Required tests

- Born-digital PDF path
- Image-only PDF path
- Mixed text-layer path
- Failure/retry behavior
- Page-number preservation
- Resource-limit behavior
- No mutation of originals

## Acceptance criteria

- OCR is reproducible from recorded configuration
- Every page maps to its source page
- Low-confidence pages are flagged
- No source advances to approval automatically
- No chunks or embeddings are generated

## Required evidence

OCR assessment and job reports for authorized test fixtures; production books remain governed by human authorization.

## Stop conditions

Stop if OCR tooling or copyright processing authorization is unresolved.

## Completion report format

Codex must report:

1. Result: `PASS`, `PARTIAL`, `BLOCKED`, or `FAIL`
2. Files created
3. Files modified
4. Data migration impact
5. Commands executed
6. Test results
7. Acceptance-criteria matrix
8. Security and privacy impact
9. Known limitations
10. Human approvals still required
11. Exact Git status
12. Exact recommended next action
13. Confirmation that the next sprint was not started
