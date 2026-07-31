# KS-07 — Embedding Pipeline

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Generate reproducible embeddings only for approved chunk datasets using an accepted embedding ADR.

## Dependencies

KS-06 approved chunks. Embedding ADR accepted. Model/license/privacy review complete.

## In scope

- Provider-neutral embedding adapter
- Model/config fingerprint
- Batch/resume behavior
- Deterministic input manifests
- Embedding artifact validation
- Cost/time reports
- Failure recovery
- Local/staging outputs

## Out of scope

- Vector collection publication
- Production RAG switch
- Research agent
- Automatic model selection

## Required architecture

Embeddings are derived artifacts tied to exact chunk dataset and model configuration versions.

## Data and state rules

Embedding records reference chunk ID, model ID, dimensions, configuration fingerprint, and generation timestamp.

## Security and governance

Secrets are not logged. Network providers require explicit authorization. Source content retention policies are documented.

## Required implementation work

Implement adapter interface, approved provider implementation, manifest-driven jobs, validation, and reports.

## Required tests

- Fixture embedding provider
- Resume/idempotency
- Dimension mismatch
- Partial failure
- Manifest mismatch
- Secret redaction
- Unapproved-chunk rejection

## Acceptance criteria

- Only approved chunks are embedded
- Reproduction metadata is complete
- Failed batches do not corrupt completed artifacts
- No production collection changes

## Required evidence

Embedding manifest, validation report, and test artifacts using approved fixtures.

## Stop conditions

Stop if embedding ADR or model permission is missing.

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
