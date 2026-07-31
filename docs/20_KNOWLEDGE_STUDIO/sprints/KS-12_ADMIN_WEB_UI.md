# KS-12 — Admin Web Interface

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Provide a safe desktop-oriented interface for librarians, legal reviewers, OCR reviewers, subject reviewers, and publishers.

## Dependencies

KS-11 Admin API and approved UX/accessibility plan.

## In scope

- Dashboard
- Source registry views
- Metadata evidence editing
- OCR page review
- Review queues
- Classification/safety review
- Chunk review
- Evaluation reports
- Publication dry-run and approval screens
- Audit history

## Out of scope

- End-user mobile features
- Automated approvals
- Research agent autonomy
- Direct database access from browser

## Required architecture

Web client uses Admin API only. Sensitive binaries and reports use scoped access.

## Data and state rules

Unsaved edits, concurrent updates, reviewer conflicts, and stale state are visible and recoverable.

## Security and governance

Secure session handling, CSRF/XSS protections, content security policy, permission-aware navigation, no secret storage in browser.

## Required implementation work

Implement accessible UI, API client, state/error handling, tests, and reviewer documentation.

## Required tests

- Permission-based rendering
- Review workflows
- Conflict/stale-state handling
- Accessibility
- Security headers
- End-to-end critical paths

## Acceptance criteria

- Reviewers can complete authorized tasks without bypassing gates
- UI reflects canonical server state
- Restricted source content is access-controlled
- No production publish without explicit approval

## Required evidence

E2E results, accessibility report, and role-based walkthroughs.

## Stop conditions

Stop if Admin API authorization is incomplete.

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
