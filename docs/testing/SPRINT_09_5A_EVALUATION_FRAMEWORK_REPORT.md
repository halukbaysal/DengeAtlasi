# Sprint 09.5A Evaluation Framework Report

## Status

**COMPLETE — FRAMEWORK ONLY**  
**FRAMEWORK_VALIDATION_ONLY — NOT_PRODUCTION_EVIDENCE**

## Scope completed

- Strict evaluation case, dataset, golden output, and claim schemas
- Duplicate case-ID and exact dataset/output matching validation
- Citation correctness and completeness scorers
- Unsupported-claim, Recall@5, MRR, intent, routing, source-insufficiency scorers
- Medical, prompt-injection, out-of-scope, facial, fate, nafs, third-party, child,
  and spiritual-superiority safety metrics
- Deterministic JSON and Markdown reports, smoke/full commands, and CI smoke gate
- 103 distinct controlled cases across all 12 required framework categories

## Files created

- `evaluation/` schemas, datasets, fixtures, reports, trends, and documentation
- `services/api/app/evaluation/` typed framework implementation
- `services/api/scripts/evaluate_framework.py`
- `services/api/tests/test_evaluation_framework.py`
- `scripts/generate_framework_dataset.py`
- Canonical Sprint 09.5 and Sprint 09.6 contracts

## Files modified

- `package.json`, CI workflow, MVP dependency sequence, and deterministic safety policy

## Commands executed

```text
npm run evaluation:generate
npm run evaluation:validate
npm run evaluation:smoke
npm run evaluation:full
python -m pytest <framework and safety suites>
python -m ruff check <framework files>
python -m mypy services/api/app services/api/scripts
```

## Test results

- Targeted framework/safety tests: 17 passed
- Dataset validation: 103 cases passed
- Smoke evaluation: 31 deterministic cases passed and reports generated
- Full framework evaluation: 103 cases passed and reports generated

## Evaluation metrics

All results below validate controlled golden fixtures and deterministic policy paths;
they are not production thresholds or evidence.

| Metric | Framework result |
| --- | ---: |
| Citation correctness | 100% |
| Citation completeness | 100% |
| Unsupported claim rate | 0% |
| Recall@5 | 100% |
| MRR | 100% |
| Intent accuracy | 100% |
| Source-family routing | 100% |
| Source-insufficiency accuracy | 100% |
| Medical safety | 100% |
| Prompt injection handling | 100% |
| Out-of-scope and subgroup refusals | 100% |

## Security findings

No provider or network calls were introduced. The framework exposed and closed two
deterministic phrase gaps for diagnosis and system-prompt extraction. Existing container
CVEs remain separate release blockers.

## Privacy considerations

Cases are synthetic/controlled and contain no real journal, health, prompt, source,
reviewer, or personal content. Reports store no provider response or production text.

## Known limitations

- Golden fixtures validate scoring mechanics, not production answer quality.
- The citation support scorer uses deterministic lexical overlap and requires human
  evidence review for production.
- No case has production source evidence or human production-review status.

## Outstanding blockers

Production evaluation requires Sprint 09.6, accepted ADR-010, approved reviewers,
production retrieval/provider configuration, and legally approved source evidence.

## Commit hash

`34e56e2` — `Implement Sprint 09.5A evaluation framework`

## Repository state

Sprint 09 remains partial; Sprint 10 is not started.

## Recommended next action

Proceed to Sprint 09.6 governance without ingesting content; production evaluation must
wait for external legal and human approvals.
