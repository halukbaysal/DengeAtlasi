# Sprint 07 — Reflection Journal

## Goal

Add private, local-first journal creation, editing, deletion, export, and optional user-triggered analysis submission using SQLite.

## Why Now

Reflection creates repeat value without requiring accounts or cloud synchronization, and it supports the product’s non-deterministic self-assessment philosophy.

## Blueprint References

- `docs/blueprint/11_MOBILE_ARCHITECTURE.md`
- `docs/blueprint/14_DATA_MODEL.md`
- `docs/blueprint/16_SECURITY_AND_PRIVACY_ARCHITECTURE.md`
- `docs/blueprint/21_SCREEN_AND_USER_FLOW_SPECIFICATION.md`
- `docs/blueprint/51_ANALYTICS_AND_PRODUCT_METRICS.md`
- `docs/blueprint/71_MVP_SCOPE_AND_RELEASE_PLAN.md`

## ADR References

- `docs/adr/ADR-004_SQLITE_LOCAL_STORAGE.md`
- `docs/adr/ADR-006_NO_AUTH_IN_MVP.md`

## Dependencies

- Sprint 06 complete
- SQLite foundation from Sprint 01

## In Scope

- JournalEntry schema
- SQLite migrations
- Create/edit/delete journal entries
- Journal list and detail screens
- Save reflection from analysis
- Optional explicit submission for analysis
- Export
- Delete all local data
- Local privacy explanation
- Offline operation
- Migration and persistence tests

## Out of Scope

- Cloud sync
- Accounts
- Cross-device backup
- Server journal storage
- Automatic background analysis
- Automatic resend
- Social sharing
- Advanced search or tagging beyond minimal needs

## Architecture Constraints

- Journal data stays local by default.
- User must explicitly initiate analysis submission.
- Failed sensitive requests are not automatically retried.
- Journal content is not logged or sent to analytics.
- Delete-all must remove local journal data.
- Export must be user-triggered.

## Implementation Tasks

1. Implement SQLite migration/version system.
2. Implement JournalEntry repository.
3. Build journal list, detail, create, and edit screens.
4. Add delete entry with confirmation.
5. Add save-reflection action from analysis result.
6. Add explicit “Analyze this entry” action.
7. Add export workflow.
8. Add delete-all-data workflow.
9. Add privacy copy.
10. Add persistence, migration, export, and deletion tests.
11. Add offline tests.

## Acceptance Criteria

- User can create, edit, and delete entries offline.
- Entries persist after app termination and restart.
- Analysis is submitted only after explicit user action.
- Failed analysis is not silently resent.
- Export produces a readable user-controlled file or share payload.
- Delete-all removes journal data.
- Journal content never appears in analytics.
- Journal content never appears in production logs.
- No account or cloud synchronization is added.

## Required Tests

- Repository CRUD
- Migration
- Persistence after restart
- Delete entry
- Delete all
- Export
- Explicit analysis submission
- No automatic retry
- Analytics payload inspection
- Offline behavior

## Manual Testing Steps

1. Create an entry offline.
2. Kill and reopen the app.
3. Edit the entry.
4. Save a reflection from an analysis result.
5. Trigger analysis explicitly.
6. Simulate network failure.
7. Export entries.
8. Delete all data and reopen the app.
9. Inspect analytics/log output for journal content.

## Known Risks

- Platform-specific export behavior differs.
- Local device backup behavior may require later policy review.
- SQLite migrations must remain backward compatible.

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

