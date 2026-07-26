# Evaluation System

The Sprint 09.5A framework validates schemas, scorers, deterministic execution, and
report generation. Everything under `framework_validation` and `fixtures` is:

```text
FRAMEWORK_VALIDATION_ONLY
NOT_PRODUCTION_EVIDENCE
```

Commands:

```bash
npm run evaluation:validate
npm run evaluation:smoke
npm run evaluation:full
```

`evaluation:smoke` is deterministic and suitable for pull requests. The full command
is local/nightly and writes both JSON and Markdown reports. Neither command calls a
paid provider. Production datasets remain empty until legally approved sources,
human reviewers, ADR-010, and production retrieval are available.

Structure:

```text
schemas/                 generated JSON schemas
datasets/framework_validation/ controlled cases
datasets/production/     blocked/empty until approval
fixtures/                controlled golden outputs
reports/                 generated framework reports
scorers/                 scorer documentation; implementation lives in backend
trends/                  append-only report history format
```
