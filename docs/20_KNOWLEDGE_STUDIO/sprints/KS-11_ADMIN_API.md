# KS-11 — Admin API

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Expose governed Knowledge Studio operations through an authenticated administrator/reviewer API.

## Dependencies

Core workflows KS-01 through KS-10 stable enough for service contracts. Identity/RBAC design approved.

## In scope

- Authenticated admin endpoints
- Role/permission model
- Registry and artifact reads
- Review actions
- Job submission/status
- Report access
- Publication dry-run and approval requests
- OpenAPI contracts

## Out of scope

- Public API
- Mobile integration
- Web UI
- Research agent
- Anonymous access

## Required architecture

API delegates to existing domain services and does not duplicate lifecycle logic.

## Data and state rules

Every mutation records authenticated actor, request ID, timestamp, reason, and resulting state.

## Security and governance

Strong authentication, least privilege, CSRF strategy where applicable, rate limits, audit logging, body limits, and no raw-source leakage by default.

## Required implementation work

Create API module, auth/RBAC adapters, schemas, handlers, OpenAPI, and tests.

## Required tests

- Authentication
- Permission matrix
- Invalid transitions
- Audit identity
- Rate/body limits
- Sensitive response filtering
- OpenAPI compatibility

## Acceptance criteria

- Unauthorized actions are blocked
- API cannot bypass domain gates
- All mutations are attributable
- No public runtime endpoint changes

## Required evidence

Permission matrix, OpenAPI diff, tests, and security review.

## Stop conditions

Stop if identity provider or role model is unresolved.

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
