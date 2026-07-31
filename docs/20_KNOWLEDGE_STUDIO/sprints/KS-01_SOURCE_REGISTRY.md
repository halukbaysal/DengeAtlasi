# KS-01 — Source Registry and Immutable Intake

**Product:** Knowledge Studio
**Status:** VERIFIED_COMPLETE — COMMITTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Register untrusted PDF sources without OCR, classification, bibliographic inference, embeddings, vector indexing, or publication.

## Dependencies

KS-00 accepted. Local source-library directory available. Human authorization to register files.

## In scope

- Streaming SHA-256
- Stable checksum-derived source IDs
- Exact duplicate detection
- Content-addressed immutable originals
- Atomic registry persistence
- Append-only intake audit
- Safe filename handling
- PDF/header/size validation
- File and folder CLI
- Runtime publication boundary

## Out of scope

- OCR
- Metadata extraction beyond file facts
- Source classification
- Legal or subject approval
- Chunking
- Embeddings
- ChromaDB
- Admin authentication
- Web UI

## Required architecture

Canonical intake model is `KnowledgeSourceRecord`. Runtime `SourceRecord` remains unchanged. KS-01 records are always `REGISTERED / UNTRUSTED` and publication mapping must reject them.

## Data and state rules

Original binaries are content-addressed under `originals/<sha-prefix>/<sha256>.pdf`. Registry is local JSON; audit is JSONL. Bibliographic fields remain `UNKNOWN`.

## Security and governance

Local artifacts are excluded from Git. Copy and registry writes are atomic. Input size and PDF signature are validated. No file is executed.

## Completion evidence

Committed separately as `2b9471124dbdb44b55bb3c28b96b36e3f23fdd32`.
Eight unique sources were registered, zero exact duplicates were found, all eight remain
`REGISTERED / UNTRUSTED`, and publication is blocked 8/8.

## Required tests

- Registry unit tests
- Duplicate/idempotency tests
- Atomic-copy tests
- Corruption/checksum tests
- CLI help and dry-run tests
- Publication-boundary rejection tests
- Ruff, MyPy, docs validation, secret scan

## Acceptance criteria

- All registered sources have unique IDs and SHA-256 values
- Repeated import is idempotent
- Originals verify against registry checksums
- Registry and audit counts match
- All sources remain `REGISTERED / UNTRUSTED`
- Publication is blocked for every source
- No OCR/classification/chunking/embedding/runtime changes

## Required evidence

`KS_01_IMPLEMENTATION.md`, `KS_01_ACCEPTANCE_REPORT.md`, registry tests, and the selective staging diff.

## Stop conditions

KS-01 is accepted and committed. Later work still requires separate sprint authorization.

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
