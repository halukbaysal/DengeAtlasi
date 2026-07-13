# Sprint 04 — Grounded Answer and Citation Engine

## Goal

Generate structured, source-grounded answers with validated citations, explicit source limits, safety outcomes, and mandatory medical notices.

## Why Now

The product cannot expose AI-generated interpretation until unsupported claims and false citations are actively blocked.

## Blueprint References

- `docs/blueprint/03_PHILOSOPHY_AND_DESIGN_PRINCIPLES.md`
- `docs/blueprint/12_BACKEND_ARCHITECTURE.md`
- `docs/blueprint/15_API_STANDARDS.md`
- `docs/blueprint/30_AI_ARCHITECTURE.md`
- `docs/blueprint/31_PROMPT_AND_CONTEXT_SYSTEM.md`
- `docs/blueprint/32_EVALUATION_AND_SAFETY_SYSTEM.md`
- `docs/blueprint/60_TESTING_AND_QUALITY_STRATEGY.md`

## ADR References

- `docs/adr/ADR-005_OPENAPI_CONTRACT_SOURCE.md`
- `docs/adr/ADR-008_MARIFETNAME_FIRST_ROUTING.md`
- `docs/adr/ADR-009_MANDATORY_MEDICAL_SAFETY_LAYER.md`

## Dependencies

- Sprint 03 complete
- Approved LLM provider or mock provider
- Prompt registry foundation

## In Scope

- Structured AnalysisResponse model
- LLMProvider adapter
- Mock provider
- Prompt registry and versioning
- Context assembly
- Answer composer
- Citation validator
- Unsupported-claim safeguards
- Source insufficiency handling
- Out-of-scope handling
- Medical safety classifier/policy
- Mandatory doctor notice
- Analysis endpoint
- Evaluation fixtures

## Out of Scope

- Mobile result UI
- Full temperament questionnaire
- Journal
- TTS
- Multi-provider routing
- Monetization

## Architecture Constraints

- Model output is untrusted until validated.
- Citation IDs come only from retrieved context.
- Invalid citations block the answer.
- General symbolic interpretation must be separate from sourced claims.
- Medical notice is appended deterministically and cannot be removed by the model.
- Hidden reasoning is never requested or returned.
- Full prompts and responses are not logged.

## Implementation Tasks

1. Implement response models and enums.
2. Implement prompt registry with versioned prompt metadata.
3. Implement context builder with source boundaries.
4. Implement `LLMProvider` and mock provider.
5. Implement structured generation.
6. Implement citation validator.
7. Implement source sufficiency policy.
8. Implement out-of-scope policy.
9. Implement medical-adjacent detection.
10. Implement mandatory doctor notice.
11. Implement safe error/fallback responses.
12. Add analysis endpoint.
13. Regenerate OpenAPI and mobile client.
14. Add eval fixtures for unsupported claims, fake citations, health advice, and prompt injection.

## Acceptance Criteria

- Every sourced claim maps to a retrieved source.
- Invented citation IDs are rejected.
- Source-limited answers clearly state limitations.
- General symbolic content is separately labeled.
- Health-adjacent answers include the doctor notice.
- Diagnosis, treatment, medication, dosage, and herbal prescription requests do not produce advice.
- Out-of-scope prompts return a stable refusal.
- Prompt injection does not expose internal instructions.
- Structured output validation is enforced.
- No raw prompt or model output is logged.

## Required Tests

- Structured response validation
- Citation correctness
- Invented citation rejection
- Source insufficiency
- General-symbolic separation
- Medical notice enforcement
- Medication and treatment refusal
- Prompt injection
- Provider timeout
- Invalid provider JSON
- Log redaction

## Manual Testing Steps

1. Ask a source-supported question.
2. Ask a source-limited question.
3. Ask for medication advice.
4. Ask for an herbal dosage.
5. Attempt prompt injection.
6. Force a fake citation from the mock provider.
7. Inspect logs for sensitive content.
8. Verify response structure in OpenAPI.

## Known Risks

- Unsupported claim detection is imperfect and requires evals.
- Medical-adjacent classification must prioritize safety.
- Real provider behavior may differ from mock behavior.

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

