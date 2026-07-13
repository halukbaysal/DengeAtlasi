# Sprint 08 — Native TTS

## Goal

Add accessible device-native text-to-speech for source-grounded results and reflection content.

## Why Now

TTS improves accessibility and usability without introducing cloud audio, voice cloning, or additional sensitive data processing.

## Blueprint References

- `docs/blueprint/11_MOBILE_ARCHITECTURE.md`
- `docs/blueprint/20_UI_UX_DESIGN_SYSTEM.md`
- `docs/blueprint/21_SCREEN_AND_USER_FLOW_SPECIFICATION.md`
- `docs/blueprint/71_MVP_SCOPE_AND_RELEASE_PLAN.md`

## ADR References

- `docs/adr/ADR-001_REACT_NATIVE_CLI.md`
- `docs/adr/ADR-007_NO_CAMERA_OR_FACIAL_ANALYSIS.md`

## Dependencies

- Sprint 07 complete

## In Scope

- Native TTS adapter
- Play
- Pause where supported
- Stop
- Speech rate
- TTS reader UI
- Screen-reader compatibility
- Lifecycle handling
- Error fallback to visible text
- Device tests

## Out of Scope

- Voice cloning
- Cloud TTS
- Audio file generation
- Audio upload
- Background sleep programming
- Health or therapy claims
- Automatic playback
- Music

## Architecture Constraints

- TTS runs on device.
- No audio or text is uploaded for speech.
- Playback starts only after user action.
- Visible text remains available if TTS fails.
- The feature must not claim treatment or subconscious programming.

## Implementation Tasks

1. Implement platform-neutral TTS interface.
2. Add native dependency if required and document it.
3. Build TTS reader controls.
4. Add play, pause/stop, and rate behavior.
5. Handle navigation and app lifecycle.
6. Handle unsupported voices/languages.
7. Add accessibility labels.
8. Add tests with a mock TTS adapter.
9. Add manual device test checklist.

## Acceptance Criteria

- User can start and stop reading.
- Pause works where platform support allows; otherwise behavior is documented.
- User can adjust supported speech rate.
- No automatic playback occurs.
- No audio file is generated or uploaded.
- TTS failure does not hide the text.
- Controls are accessible.
- App background/foreground transitions do not leave uncontrolled playback.

## Required Tests

- Adapter contract
- Play
- Stop
- Rate
- Unsupported platform behavior
- Navigation cleanup
- App lifecycle
- Accessibility labels
- No network call for TTS

## Manual Testing Steps

1. Play a grounded result.
2. Stop playback.
3. Change speech rate.
4. Navigate away during playback.
5. Background and foreground the app.
6. Disable or remove a matching voice.
7. Use screen reader controls.
8. Confirm no network call is made by the feature.

## Known Risks

- Pause behavior differs by platform.
- Turkish voice availability depends on device configuration.
- Long text may require chunked speech.

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

