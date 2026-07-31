# KS-13 — Admin Research Agent and Source Discovery

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Assist administrators with source discovery and bibliographic research while preventing self-learning into production.

## Dependencies

Admin API/UI, review workflow, source registry, security model, and approved provider policy.

## In scope

- Admin-created research tasks
- Provider-neutral agent adapter
- Search result/candidate registry
- Bibliographic evidence capture
- URL and file candidate registration
- Duplicate hints
- Edition comparison assistance
- Risk flags
- Staging-only output
- Full audit

## Out of scope

- Automatic downloading from arbitrary URLs without policy
- Automatic legal approval
- Automatic OCR/embedding/publication
- Runtime answering from agent memory
- Autonomous continuous crawling

## Required architecture

Agent output is a candidate artifact only. Flow: discovery → registration → staging → human review → later approved pipelines.

## Data and state rules

Every claim stores provider, query, timestamp, source URL/reference, excerpt limits, and confidence. Unsupported claims remain suggestions.

## Security and governance

SSRF protection, domain allow/deny policy, prompt-injection detection in documents, download limits, malware scanning integration point, secret isolation.

## Required implementation work

Build research task model, provider adapter, result normalization, candidate registration, reports, and approval handoff.

## Required tests

- SSRF/private-network rejection
- Malicious document instruction handling
- Duplicate candidates
- Missing provenance
- Provider failure/retry
- No automatic production transition

## Acceptance criteria

- Agent cannot publish or approve
- Results are fully attributable
- Risky or unverifiable results are flagged
- Production RAG is unchanged

## Required evidence

Red-team results, task audit, and sample staging research report.

## Stop conditions

Stop if provider privacy, copyright, or network-security policy is unresolved.

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
