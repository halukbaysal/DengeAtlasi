# Sprint 10 — Beta Hardening and Release Readiness

## Goal

Prepare stable iOS, Android, and backend builds for a controlled adult closed beta with complete privacy, safety, observability, rollback, and operational documentation.

## Why Now

The product must prove operational readiness after feature completion and safety evaluation.

## Blueprint References

- `docs/blueprint/51_ANALYTICS_AND_PRODUCT_METRICS.md`
- `docs/blueprint/60_TESTING_AND_QUALITY_STRATEGY.md`
- `docs/blueprint/61_DEVOPS_AND_DEPLOYMENT_ARCHITECTURE.md`
- `docs/blueprint/62_OBSERVABILITY_AND_INCIDENT_MANAGEMENT.md`
- `docs/blueprint/71_MVP_SCOPE_AND_RELEASE_PLAN.md`
- `docs/blueprint/73_PRODUCTION_READINESS_CHECKLIST.md`

## ADR References

All accepted ADRs.

## Dependencies

- Sprint 09 complete
- No unresolved release blockers

## In Scope

- Release configuration
- Environment validation
- Backend deployment pipeline
- Mobile release builds
- Crash handling
- Privacy-safe metrics
- Alerts
- Backup and restore
- Rollback
- Store privacy disclosures
- Adult-only beta onboarding
- Consent and disclaimers
- Regression testing
- Production-readiness checklist
- Closed-beta release notes

## Out of Scope

- Public launch
- Monetization
- Accounts
- Cloud sync
- New major features
- New AI providers
- New source families
- Marketing campaign

## Architecture Constraints

- Only approved sources in production index.
- No production secrets in repository.
- No sensitive logs or analytics.
- Medical safety and citation validation cannot be bypassed.
- Closed beta remains 18+.
- Release must be rollback-capable.

## Implementation Tasks

1. Finalize local, staging, and production configuration.
2. Validate secret management.
3. Build and test backend deployment pipeline.
4. Build Android release artifact.
5. Build iOS release artifact on macOS.
6. Configure privacy-safe crash reporting and metrics.
7. Configure alerts and dashboards.
8. Test backup/restore of source index and backend state.
9. Test backend and source-index rollback.
10. Finalize consent, source, and medical disclaimer screens.
11. Complete store privacy disclosures.
12. Run full regression.
13. Complete production readiness checklist.
14. Prepare closed-beta release notes and tester instructions.

## Acceptance Criteria

- Backend production image builds and deploys to staging.
- Android release build succeeds.
- iOS release build succeeds on macOS or is honestly reported as environment-blocked.
- Secrets are externally managed.
- Crash reporting excludes user content.
- Alerts work.
- Backup and restore are tested.
- Rollback is tested.
- Consent and disclaimers are visible.
- Production index contains approved sources only.
- Full regression passes.
- All critical production-readiness items are checked.
- Closed-beta documentation exists.
- No public launch or monetization feature is added.

## Required Tests

- Release builds
- Staging smoke test
- Full backend tests
- Full mobile tests
- Full AI eval suite
- Backup/restore
- Rollback
- Alert test
- Privacy payload inspection
- Production readiness review

## Manual Testing Steps

1. Install release builds on physical devices.
2. Complete onboarding and consent.
3. Run the full user loop.
4. Test offline journal.
5. Test TTS.
6. Test medical redirect.
7. Verify citations.
8. Trigger a controlled backend failure.
9. Verify alerts and rollback.
10. Review store disclosures and beta instructions.

## Known Risks

- iOS signing and store configuration require Apple credentials.
- Production hosting choice may remain environment-specific.
- Beta feedback may require scope changes after release.

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

