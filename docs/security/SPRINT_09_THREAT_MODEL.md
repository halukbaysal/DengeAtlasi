# Sprint 09 Threat Model

## Scope and assets

The mobile client, API, approved-source index, provider boundary, local journal, logs,
analytics metadata, citations, prompts, and release artifacts are in scope. Journal,
health, birth, prompt, source-excerpt, and provider-output text are sensitive.

## Trust boundaries and controls

| Boundary | Threat | Preventive and detective controls |
| --- | --- | --- |
| Mobile → API | oversized payload, abuse, schema attack | 16 KiB body limit, per-client rate limit, Pydantic `extra=forbid`, control-character rejection |
| User/source → prompt | direct or indirect injection | deterministic refusal markers, machine-owned boundaries, source poisoning rejection, prompt hierarchy |
| Provider → API | invalid schema, invented citation, unsupported claim | strict provider schema, retrieved-ID allowlist, lexical support check, fail-closed response |
| API → logs | journal/health/prompt leakage | metadata-only middleware logs and redaction regression tests |
| Mobile → analytics | sensitive payload or unknown event | runtime event/property/value allowlist; analytics disabled by default |
| Source ingestion → index | malicious or unreviewed content | approval/copyright/OCR gates, instruction-like content rejection, source hashes |
| Supply chain/container | vulnerable dependency or image | pinned Python lock, npm/pip audit, container scan gate and documented triage |

## Abuse cases and release blockers

Medical diagnosis, treatment, medication and dosage requests must redirect with the
mandatory doctor notice. Facial inference, fate prediction, and nafs ranking must be
refused. Any medical failure, invented citation, prompt disclosure, sensitive log,
or critical supply-chain finding blocks release.

## Residual risks

Keyword controls do not cover every paraphrase and require human red-team review.
The in-memory limiter is per process and must be replaced by a shared gateway/store
before horizontally scaled production. Approved-source review remains a human control.
