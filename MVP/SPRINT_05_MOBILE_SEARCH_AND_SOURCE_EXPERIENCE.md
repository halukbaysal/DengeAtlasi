# Sprint 05 — Mobile Search and Source Experience

## Goal

Deliver the first mobile vertical slice for asking a question, receiving a grounded result, opening citations, and handling loading, offline, empty, and error states.

## Why Now

The backend core loop must become a usable mobile experience before adding temperament-specific input and journaling.

## Blueprint References

- `docs/blueprint/11_MOBILE_ARCHITECTURE.md`
- `docs/blueprint/15_API_STANDARDS.md`
- `docs/blueprint/20_UI_UX_DESIGN_SYSTEM.md`
- `docs/blueprint/21_SCREEN_AND_USER_FLOW_SPECIFICATION.md`
- `docs/blueprint/51_ANALYTICS_AND_PRODUCT_METRICS.md`
- `docs/blueprint/60_TESTING_AND_QUALITY_STRATEGY.md`

## ADR References

- `docs/adr/ADR-001_REACT_NATIVE_CLI.md`
- `docs/adr/ADR-004_SQLITE_LOCAL_STORAGE.md`
- `docs/adr/ADR-005_OPENAPI_CONTRACT_SOURCE.md`

## Dependencies

- Sprint 04 complete
- Generated API client available

## In Scope

- Home screen
- Ask/Search screen
- Loading state
- Grounded result screen
- Marifetname section
- Supplementary source section
- Citation list
- Source detail screen
- Source limit notice
- Medical notice component
- Offline state
- Empty state
- Error state
- Accessibility labels
- Minimal allowlisted analytics abstraction

## Out of Scope

- Temperament questionnaire
- Journal persistence
- TTS
- Authentication
- Cloud sync
- Monetization
- Push notifications

## Architecture Constraints

- Use generated API contracts.
- Validate responses with Zod.
- Medical notice must remain visible.
- Citations must be tappable and show edition/page metadata.
- No astrology-style charts or definitive scores.
- No sensitive payloads in analytics.

## Implementation Tasks

1. Implement navigation routes.
2. Build reusable SourceCard and CitationBadge.
3. Build Ask/Search form with validation.
4. Integrate analysis/search endpoint.
5. Implement loading, error, empty, and offline states.
6. Build Grounded Result screen.
7. Build Source Detail screen.
8. Build SourceLimitNotice and MedicalSafetyNotice.
9. Add response Zod validation.
10. Add accessibility labels and focus behavior.
11. Add allowlisted analytics interface with no sensitive payload.
12. Add component, navigation, and API integration tests.

## Acceptance Criteria

- User can submit a question.
- User sees a validated grounded result.
- Marifetname appears before supplementary sources.
- User can open citation details.
- Page, section, edition, and author are visible.
- Source limitations are visible.
- Medical notice is visible when present.
- Invalid API responses are handled safely.
- Offline state blocks new analysis but does not crash.
- No sensitive query text is sent to analytics.
- Screens work with large text and screen readers.
- No future sprint features appear.

## Required Tests

- Form validation
- API success
- API error
- Invalid Zod response
- Offline state
- Citation navigation
- Medical notice visibility
- Accessibility queries
- Analytics payload allowlist

## Manual Testing Steps

1. Submit a valid question.
2. Open each citation.
3. Test a source-limited result.
4. Test a medical-adjacent result.
5. Disable network and retry.
6. Simulate malformed API data.
7. Increase device text size.
8. Use screen reader navigation.

## Known Risks

- UI may need later visual refinement.
- Network-state libraries require native validation.
- Citation content length may require truncation and expansion behavior.

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

