# KS-10 — Controlled Publication and Rollback

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Publish a fully approved knowledge artifact to Denge Atlası through an explicit, reversible, audited gate.

## Dependencies

All required source, OCR, subject, safety, chunk, embedding, vector, evaluation, and security gates passed.

## In scope

- Publication eligibility service
- Publication manifest
- Human approval record
- Active-version pointer
- Atomic activation
- Smoke validation
- Rollback command and rehearsal
- Publication audit

## Out of scope

- App Store release
- Admin UI
- Research agent
- New content processing

## Required architecture

Publishing changes only the approved active artifact pointer after all validations pass. Build and activation are separate operations.

## Data and state rules

Manifest includes all upstream fingerprints and approvals. Rollback preserves previous active versions.

## Security and governance

Two-person or explicitly configured human approval is recommended for production. No AI agent may grant publication approval.

## Required implementation work

Implement eligibility checks, manifest validation, activation, rollback, reports, and dry-run mode.

## Required tests

- Missing-gate rejection
- Manifest tampering
- Atomic activation
- Smoke-test failure rollback
- Explicit rollback
- Audit completeness

## Acceptance criteria

- Incomplete sources cannot publish
- Activation is atomic and reversible
- Runtime consumes only the published version
- Publication and application releases remain separate

## Required evidence

Dry-run and controlled staging publication reports; production requires separate human authorization.

## Stop conditions

Stop before production activation unless explicitly authorized.

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
