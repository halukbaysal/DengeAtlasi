# KS-05 — Source Classification and Safety Labeling

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Produce reviewable source-category and safety-label candidates without allowing automatic trust or publication.

## Dependencies

KS-02 metadata candidates; KS-04 review workflow.

## In scope

- Category taxonomy
- Safety-label taxonomy
- Rule-based candidate generation
- Explainable evidence
- Human confirm/reject flow
- Restricted-source handling
- Lexicon/direct-answer restrictions
- Historical astrology restrictions

## Out of scope

- Deterministic personality or fate features
- Embeddings
- Runtime routing
- Automatic approval
- Research agent

## Required architecture

Classifiers emit candidates, never authoritative decisions. Rules are deterministic and versioned where practical.

## Data and state rules

Categories include `PRIMARY_SOURCE`, `SECONDARY_ACADEMIC`, `LEXICON`, `HISTORICAL_REFERENCE`, `HISTORICAL_ASTROLOGY`, `COMMENTARY`, and `UNKNOWN`.

## Security and governance

Risk labels cannot be removed without audited human review. Restricted materials remain admin-only by default.

## Required implementation work

Implement taxonomy, candidate engine, evidence model, review integration, reports, and tests.

## Required tests

- Marifetname candidate
- Lexicon restrictions
- Academic secondary source
- Yıldızname restriction
- Unknown scan behavior
- Conflicting evidence
- No automatic approval

## Acceptance criteria

- Candidates are explainable
- UNKNOWN is preserved when evidence is weak
- Restricted material cannot become production-eligible
- Lexicons cannot become direct answer authorities

## Required evidence

Classification and safety reports with human-review queues.

## Stop conditions

Stop if taxonomy conflicts with source governance.

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
