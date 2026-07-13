# Sprint 09 — Security, Safety, and Evaluation

## Goal

Harden the complete system against prompt injection, unsupported claims, false citations, unsafe medical output, sensitive logging, and operational abuse.

## Why Now

The core product exists. It must not proceed to beta without measurable safety, retrieval, citation, privacy, and security evidence.

## Blueprint References

- `docs/blueprint/16_SECURITY_AND_PRIVACY_ARCHITECTURE.md`
- `docs/blueprint/31_PROMPT_AND_CONTEXT_SYSTEM.md`
- `docs/blueprint/32_EVALUATION_AND_SAFETY_SYSTEM.md`
- `docs/blueprint/51_ANALYTICS_AND_PRODUCT_METRICS.md`
- `docs/blueprint/60_TESTING_AND_QUALITY_STRATEGY.md`
- `docs/blueprint/62_OBSERVABILITY_AND_INCIDENT_MANAGEMENT.md`
- `docs/blueprint/73_PRODUCTION_READINESS_CHECKLIST.md`

## ADR References

- `docs/adr/ADR-007_NO_CAMERA_OR_FACIAL_ANALYSIS.md`
- `docs/adr/ADR-009_MANDATORY_MEDICAL_SAFETY_LAYER.md`

## Dependencies

- Sprint 08 complete
- End-to-end core loop available

## In Scope

- Full AI evaluation suite
- Prompt injection tests
- Source poisoning tests
- Citation correctness and completeness
- Unsupported claim measurement
- Medical safety tests
- Facial-inference refusal tests
- Fate/nafs-ranking refusal tests
- Rate limiting
- Payload limits
- Dependency and container scans
- Log-redaction verification
- Analytics allowlist enforcement
- Threat model
- Incident runbooks
- Release report

## Out of Scope

- New product features
- Monetization
- Accounts
- Cloud sync
- Large UI redesign
- New source families unless needed as test fixtures

## Architecture Constraints

- Any medical safety failure blocks release.
- Any invented citation blocks release.
- Sensitive user content must not enter logs or analytics.
- Security fixes must not bypass validation or source controls.
- Evaluation thresholds come from the blueprint unless changed by accepted ADR.

## Implementation Tasks

1. Build automated eval runner.
2. Add retrieval, citation, unsupported-claim, and safety datasets.
3. Add direct and indirect prompt injection cases.
4. Add source-poisoning fixtures.
5. Add medical, medication, herbal, facial, fate, and nafs cases.
6. Add rate limiting and payload limits.
7. Add log-redaction tests.
8. Add analytics payload validation.
9. Run dependency and container scans.
10. Create threat model.
11. Create incident runbooks.
12. Produce evaluation and release-blocker report.
13. Fix critical failures within sprint scope.

## Acceptance Criteria

- Retrieval Recall@5 meets threshold.
- Citation correctness and completeness meet thresholds.
- Unsupported claim rate is within threshold.
- Medical safety compliance is 100%.
- Known prompt injection cases are safely handled.
- Facial, diagnosis, treatment, medication, fate, and nafs-ranking requests do not produce prohibited outputs.
- Logs and analytics contain no sensitive content.
- Rate limits and payload limits work.
- Critical dependency/container findings are resolved or explicitly block release.
- Threat model and incident runbooks exist.
- No unrelated features are added.

## Required Tests

- Full automated eval suite
- Security integration tests
- Rate limit
- Payload limit
- Log redaction
- Analytics allowlist
- Dependency scan
- Container scan
- Manual red-team pass

## Manual Testing Steps

1. Run the complete evaluation suite.
2. Review every failure.
3. Attempt direct and indirect prompt injection.
4. Submit medical and medication requests.
5. Submit facial and fate requests.
6. Inspect production-style logs.
7. Inspect analytics payloads.
8. Trigger rate limits.
9. Review threat model and runbooks.

## Known Risks

- Thresholds may expose source or prompt weaknesses requiring rework.
- Provider updates can change safety performance.
- Security tools may report non-exploitable findings that still require documented triage.

## Agent Instructions

- Start immediately when instructed to begin this sprint.
- Do not ask follow-up questions.
- Read all referenced documents before modifying code.
- Inspect the current repository and preserve existing working behavior.
- Use the smallest complete implementation that satisfies this sprint.
- Do not implement future sprint scope.
- Do not silently alter accepted architecture.
- If a minor detail is unspecified, use the safest convention already established by the blueprint and repository.
- If genuinely blocked, return a precise `BLOCKED` completion report instead of asking an open-ended question.
- Run all required tests and report actual results.


## Completion Report Format

```text
SPRINT XX COMPLETION REPORT

Status:
- COMPLETE
- PARTIAL
- BLOCKED

Summary:

Files created:

Files modified:

Files deleted:

Dependencies added or changed:

Implementation details:

Tests added:

Commands executed:

Command results:

Acceptance criteria:
- PASS/FAIL — criterion

Manual testing steps:

Security considerations:

Privacy considerations:

Architecture decisions or concerns:

Known limitations:

Deferred items:

Recommended next action:
```

