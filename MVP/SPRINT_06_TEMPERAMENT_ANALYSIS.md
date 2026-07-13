# Sprint 06 — Temperament Analysis

## Goal

Implement the Marifetname-first temperament analysis flow with clearly separated Ibn Sina supplements, safe uncertainty language, reflection themes, and mandatory medical safety behavior.

## Why Now

This is the product’s primary differentiated feature and must be built only after source retrieval, citation validation, and the mobile result experience are stable.

## Blueprint References

- `docs/blueprint/01_PROJECT_VISION.md`
- `docs/blueprint/03_PHILOSOPHY_AND_DESIGN_PRINCIPLES.md`
- `docs/blueprint/13_TEMPERAMENT_AND_SOURCE_ROUTING_ENGINE.md`
- `docs/blueprint/20_UI_UX_DESIGN_SYSTEM.md`
- `docs/blueprint/21_SCREEN_AND_USER_FLOW_SPECIFICATION.md`
- `docs/blueprint/32_EVALUATION_AND_SAFETY_SYSTEM.md`
- `docs/blueprint/71_MVP_SCOPE_AND_RELEASE_PLAN.md`

## ADR References

- `docs/adr/ADR-008_MARIFETNAME_FIRST_ROUTING.md`
- `docs/adr/ADR-009_MANDATORY_MEDICAL_SAFETY_LAYER.md`

## Dependencies

- Sprint 05 complete
- Approved temperament-related source fixtures or production sources

## In Scope

- Temperament input flow
- Consent and educational disclaimer
- Input validation
- Marifetname-first backend routing
- Ibn Sina supplementary section
- Optional other approved supporting sources
- Uncertainty/source-limit language
- Safe general wellbeing suggestions
- Reflection questions
- Mandatory doctor notice for health-adjacent content
- Temperament evaluation dataset
- Mobile result presentation

## Out of Scope

- Definitive temperament scoring
- Personality tests
- Clinical psychology
- Disease prediction
- Medication or treatment
- Facial analysis
- Birth-chart astrology
- Nafs ranking
- Child analysis
- Third-party analysis

## Architecture Constraints

- Temperament output is thematic, not deterministic.
- Marifetname remains primary.
- Ibn Sina is visibly supplementary.
- Health advice is limited to low-risk general wellbeing language.
- Any symptom or condition triggers stronger medical guidance.
- The model cannot suppress the doctor notice.
- No numeric “truth score” for personality or temperament.

## Implementation Tasks

1. Define temperament input contract.
2. Build consent/disclaimer screen.
3. Build temperament input form.
4. Implement backend temperament route and source routing.
5. Implement safe response language templates.
6. Implement Ibn Sina supplement reason field.
7. Implement safe wellbeing suggestion allowlist/policy.
8. Implement medical-adjacent escalation.
9. Build temperament result screen sections.
10. Add reflection questions.
11. Add eval dataset for deterministic language, medical advice, and source routing.
12. Add unit, integration, component, and end-to-end tests.

## Acceptance Criteria

- User can complete the temperament input flow.
- Marifetname is always queried first.
- Ibn Sina appears only as a separately labeled supplement.
- Output uses “may,” “can be associated,” or equivalent uncertainty language.
- Output never claims a definitive personality or disease.
- Health-adjacent responses include the mandatory doctor notice.
- Symptoms, medication, or illness input does not produce personalized treatment advice.
- Citations are visible and valid.
- Source-limited cases remain honest.
- No modern personality test or astrology framework is introduced.

## Required Tests

- Input validation
- Consent requirement
- Marifetname-first routing
- Ibn Sina supplement labeling
- Deterministic-language rejection
- Safe suggestion policy
- Symptom escalation
- Medical notice enforcement
- Citation validation
- Source insufficiency
- End-to-end mobile flow

## Manual Testing Steps

1. Complete a normal temperament flow.
2. Inspect primary and supplementary sections.
3. Enter health symptoms.
4. Ask for a diet, medicine, or herbal dosage.
5. Test a source-limited profile.
6. Verify all citations.
7. Verify no numeric or definitive personality score appears.
8. Test accessibility.

## Known Risks

- Users may over-interpret historical temperament categories.
- Safe language must remain prominent, not buried.
- Source coverage may be uneven across temperament themes.

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

