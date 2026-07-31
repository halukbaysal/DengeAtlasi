# KS-09 — Evaluation Framework and Production Corpus Evaluation

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Measure retrieval, citation support, unsupported claims, routing, safety, injection resistance, and latency before publication.

## Dependencies

Framework fixtures may begin earlier; production evaluation requires KS-08 staging collection and approved corpus.

## In scope

- Phase A framework validation
- Phase B production corpus evaluation
- Case schema
- Expected-source/citation fields
- Recall@5 and MRR
- Citation correctness/completeness
- Unsupported-claim rate
- Routing accuracy
- Safety and injection suites
- Reports and release thresholds

## Out of scope

- Automatic release approval
- Model fine-tuning
- New product features

## Required architecture

Synthetic results are labeled `FRAMEWORK_VALIDATION_ONLY / NOT_PRODUCTION_EVIDENCE`. Production claims require reviewed production cases.

## Data and state rules

Progression target: 100 curated, 300 reviewed, then 1000 production cases. Threshold changes are versioned and human-approved.

## Security and governance

Evaluation prompts and expected answers must not leak restricted source content. Failures are retained as evidence.

## Required implementation work

Create evaluation schema, scorers, runners, reports, CI smoke suite, and human-review workflow.

## Required tests

- Scorer unit tests
- Known-good/known-bad citation cases
- Unsupported claim examples
- Routing cases
- Medical/fate/child/third-party safety cases
- Prompt-injection cases

## Acceptance criteria

- Framework and production evidence are clearly separated
- Metrics are reproducible
- Failed thresholds block publication
- Human-reviewed cases and reviewer metadata are recorded

## Required evidence

Versioned evaluation report and threshold decision.

## Stop conditions

Stop if production evaluation lacks approved cases or citation ground truth.

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
