# ADR-010 — Embedding Model Evaluation

**Status:** PROPOSED

## Context

The MVP needs an embedding model, but selecting one without evaluation would risk
poor Turkish/Ottoman-language retrieval, unsafe source mixing, provider lock-in,
and unmeasured operating cost. This ADR intentionally does not choose a model.

## Proposed Decision

Select an embedding model only after a reproducible, provider-neutral benchmark
using approved or legally usable evaluation material. Record the final choice in a
new accepted ADR or an accepted revision of this ADR.

## Evaluation Criteria

- Turkish semantic retrieval quality
- Ottoman Turkish and transliterated-text behavior where evaluation data permits
- Marifetname-first ranking preservation
- Separation of primary and supplementary sources
- Citation/page traceability after chunk retrieval
- Robustness to spelling, diacritics, OCR noise, and short queries
- Vector dimensions, latency, throughput, memory, storage, and cost
- Offline/reproducible test support and deterministic version pinning
- Data residency, privacy, licensing, and provider-retention terms
- Provider portability and batch-processing support
- Model/version lifecycle and migration risk

## Benchmarking Process

1. Freeze a versioned evaluation dataset with human-reviewed relevance labels.
2. Include Marifetname, Ibn Sina supplement, source-insufficient, OCR-noise, and
   adversarial cross-source queries.
3. Apply identical normalization and chunking inputs to every candidate.
4. Measure retrieval metrics, latency, cost, and failure behavior independently.
5. Review errors for unsafe medical retrieval and incorrect source priority.
6. Repeat the benchmark on the pinned candidate version.
7. Document results, licensing review, rollback plan, and migration implications.

## Acceptance Requirements

- Recall@5 is at least 85% on the approved evaluation set.
- Marifetname-first routing tests pass for all applicable benchmark cases.
- No unapproved source can enter the benchmark's production-eligible results.
- Medical safety and known prompt-injection handling remain 100% compliant.
- Model version, license, privacy terms, dimensions, and costs are documented.
- The benchmark is reproducible in CI or a documented controlled environment.
- Human reviewers approve representative Turkish and OCR-noise results.
- No release blocker defined by the evaluation and safety blueprint is present.

## Deferred Decision

Model name, provider, dimensions, hosting mode, and production configuration remain
`TBD` until benchmarking is complete. No embedding generation is authorized by
this proposed ADR.
