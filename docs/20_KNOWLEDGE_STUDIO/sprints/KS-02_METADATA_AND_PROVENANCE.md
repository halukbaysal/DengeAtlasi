# KS-02 — Metadata and Provenance Workspace

**Product:** Knowledge Studio
**Status:** IMPLEMENTED — AWAITING HUMAN ACCEPTANCE
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Create a controlled workspace for evidence-backed bibliographic metadata and provenance without performing OCR or source approval.

## Dependencies

KS-01 accepted and selectively committed. Registered sources exist.

## In scope

- Metadata candidate schema
- Evidence references by page/file location
- Manual metadata editing workflow
- Provenance records
- Confidence and verification state
- Edition, publisher, translator, editor, year, language, script, page count
- UNKNOWN preservation
- Metadata audit events
- Import/export reports

## Out of scope

- Full OCR
- Legal approval
- Source classification decisions
- Embeddings
- Runtime publication
- Automated web research
- Admin UI beyond minimal CLI or service layer

## Required architecture

Metadata candidates are separate from canonical approved metadata. Every asserted value must reference evidence or be marked `UNVERIFIED`.

## Data and state rules

Suggested states: `NOT_STARTED`, `CANDIDATE_CAPTURED`, `HUMAN_REVIEW_REQUIRED`, `VERIFIED`, `REJECTED`. Metadata verification does not approve legal use.

## Security and governance

Never infer missing bibliographic facts from filenames alone. Do not access the internet automatically. Preserve original evidence and reviewer audit.

## Required implementation work

Build schemas, repository service, evidence references, CLI commands, report generation, and non-destructive updates to the KS registry.

## Required tests

- UNKNOWN handling
- Evidence-required validation
- Conflicting candidate handling
- Audit append tests
- Idempotent import/export
- Registry backward compatibility
- No runtime-source conversion

## Acceptance criteria

- Every metadata value has evidence or explicit UNKNOWN
- Conflicts are preserved, not silently overwritten
- Human verification is required
- Legal status remains untouched
- No OCR or production operation runs

## Required evidence

Metadata report for all registered sources, tests, and a migration-free registry update.

## Stop conditions

Stop if canonical metadata and candidate metadata cannot be cleanly separated.

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
