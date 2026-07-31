# KS-04 — Review Workflow Foundation

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Implement independent human review tracks for legal, provenance, OCR, subject content, and safety.

## Dependencies

KS-02 complete; KS-03 available for OCR review. Reviewer roles defined.

## In scope

- Review cases
- Assignment and status
- Evidence and notes
- Approve/reject/request-changes actions
- Independent review tracks
- Append-only review audit
- Conflict and escalation handling
- CLI/service layer

## Out of scope

- Admin web UI
- Automated legal decisions
- Chunk approval
- Embeddings
- Publication

## Required architecture

Review tracks are independent. A source cannot inherit one approval from another track. Final eligibility is computed from all required gates.

## Data and state rules

Each decision records reviewer role, timestamp, evidence, rationale, and prior state. AI-generated suggestions cannot be stored as human approval.

## Security and governance

RBAC-ready interfaces, immutable audit history, no reviewer impersonation, no destructive deletion of prior decisions.

## Required implementation work

Create review schemas, transition rules, repository, service, reports, and controlled commands.

## Required tests

- Valid and invalid transitions
- Independent gate behavior
- Conflict/escalation
- Audit immutability
- Reopen/request-changes
- Unauthorized action rejection at service boundary

## Acceptance criteria

- All review gates are independent and traceable
- Invalid transitions are blocked
- No review can publish a source
- Human identity/role is recorded or explicitly marked local-development reviewer

## Required evidence

State-transition matrix, tests, and review reports using fixtures.

## Stop conditions

Stop if reviewer roles or legal authority are undefined.

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
