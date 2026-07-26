# Sprint 09.5 — AI Evaluation

## Status and dependency correction

This contract supersedes any interpretation that production evaluation must precede
the production knowledge base. Historical Sprint 09 records remain unchanged.

```text
Sprint 09.5A — Evaluation Framework
→ Sprint 09.6 — Production Knowledge Base
→ Sprint 09.5B — Production Evaluation
→ Sprint 09 Final Closure
```

## Phase A — Evaluation Framework

Build deterministic schemas, validation, scorers, controlled golden fixtures,
JSON/Markdown reporting, CI smoke evaluation, and a local full evaluation. Synthetic
or controlled cases must be labelled `FRAMEWORK_VALIDATION_ONLY` and
`NOT_PRODUCTION_EVIDENCE`. At least 100 distinct cases are required. No provider call,
production threshold claim, prompt change, or product feature is permitted.

Required metrics: citation correctness, citation completeness, unsupported-claim
rate, Recall@5, MRR, intent/routing accuracy, source insufficiency, policy outcome,
medical safety, prompt injection, and out-of-scope refusal.

Phase A is complete when schema/duplicate/scorer/report tests pass, deterministic
smoke/full commands run, and reports explicitly deny production-evidence status.

## Phase B — Production Evaluation

Blocked until Sprint 09.6 is complete, ADR-010 is accepted, production retrieval is
configured, and approved human reviewers and provider configuration exist. Every
case requires source evidence, reviewer/date/status, expected response, and policy
outcome. Blueprint thresholds remain unchanged. Missing metrics are `NOT MEASURED`.

Phase B cannot be completed with framework fixtures or synthetic source content.
