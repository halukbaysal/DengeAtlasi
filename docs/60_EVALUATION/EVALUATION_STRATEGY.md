# Evaluation Strategy

**Classification:** AUTHORITATIVE

## Phase A — Framework validation

Synthetic or controlled fixtures validate schemas, scorers, reports, CI, citation and
unsupported-claim mechanics, routing scoring, and safety scoring. Every artifact says
`FRAMEWORK_VALIDATION_ONLY` and `NOT_PRODUCTION_EVIDENCE`. The current 103-case suite is
Phase A.

## Phase B — Production corpus evaluation

Only approved, manifest-bound corpus versions and human-reviewed expected evidence qualify.
Start with 100 curated cases, grow to 300 mixed reviewed cases, then 1,000+ production
cases. Dataset version, reviewers/dates, collection/model/chunk hashes, limitations, and
failures are mandatory.

Measure Recall@5, MRR, source routing, citation correctness/completeness, unsupported
claims, insufficiency, out-of-scope refusal, medical safety, prompt injection, latency,
errors, and human findings. Existing thresholds remain unchanged unless an accepted
decision changes them. Failures retain inputs/outputs/evidence classification and enter
regression coverage. Phase A scores never fill a Phase B `NOT MEASURED` field.
