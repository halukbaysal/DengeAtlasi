# Sprint 00 — Product and Source Decisions

## Goal

Close all documentation, source, legal, and architecture decisions required before implementation begins.

## Why Now

The RAG system cannot be trustworthy until approved editions, source metadata, safety rules, and provider-independent contracts are fixed.

## Blueprint References

- `docs/blueprint/01_PROJECT_VISION.md`
- `docs/blueprint/02_BUSINESS_STRATEGY.md`
- `docs/blueprint/03_PHILOSOPHY_AND_DESIGN_PRINCIPLES.md`
- `docs/blueprint/32_EVALUATION_AND_SAFETY_SYSTEM.md`
- `docs/blueprint/33_RAG_AND_SOURCE_GOVERNANCE_SYSTEM.md`
- `docs/blueprint/41_SOURCE_REVIEW_WORKFLOW.md`
- `docs/blueprint/42_TAXONOMY_AND_METADATA.md`
- `docs/blueprint/71_MVP_SCOPE_AND_RELEASE_PLAN.md`

## ADR References

- `docs/adr/ADR-001_REACT_NATIVE_CLI.md`
- `docs/adr/ADR-002_FASTAPI_BACKEND.md`
- `docs/adr/ADR-003_CHROMADB_MVP.md`
- `docs/adr/ADR-004_SQLITE_LOCAL_STORAGE.md`
- `docs/adr/ADR-005_OPENAPI_CONTRACT_SOURCE.md`
- `docs/adr/ADR-006_NO_AUTH_IN_MVP.md`
- `docs/adr/ADR-007_NO_CAMERA_OR_FACIAL_ANALYSIS.md`
- `docs/adr/ADR-008_MARIFETNAME_FIRST_ROUTING.md`
- `docs/adr/ADR-009_MANDATORY_MEDICAL_SAFETY_LAYER.md`

## Dependencies

None.

## In Scope

- Confirm source hierarchy.
- Register candidate editions for Marifetname and Ibn Sina.
- Create source inventory template.
- Create copyright review template.
- Create source review checklist.
- Finalize source categories and review statuses.
- Define mandatory medical notice text.
- Define source-grounded response types.
- Create proposed ADR for embedding model selection.
- Document unresolved business decisions as explicit `TBD`, not hidden assumptions.

## Out of Scope

- Application code
- Backend code
- Mobile project creation
- OCR implementation
- Embedding generation
- ChromaDB setup
- LLM provider integration

## Architecture Constraints

- Marifetname remains primary.
- Ibn Sina supplements only when required.
- Only `APPROVED` sources may reach production retrieval.
- No camera or facial analysis.
- Historical health content cannot become treatment advice.

## Implementation Tasks

1. Create `docs/source-registry/SOURCE_INVENTORY.md`.
2. Create `docs/source-registry/SOURCE_REVIEW_TEMPLATE.md`.
3. Create `docs/source-registry/COPYRIGHT_REVIEW_TEMPLATE.md`.
4. Create `docs/source-registry/MANDATORY_MEDICAL_NOTICE.md`.
5. Create `docs/adr/ADR-010_EMBEDDING_MODEL.md` with `Status: Proposed`.
6. Record all unresolved source editions as clearly named blockers or TBD entries.
7. Verify links and references across blueprint documents.
8. Add a Sprint 00 decision log.

## Acceptance Criteria

- Source inventory contains required metadata fields.
- Marifetname and Ibn Sina appear as separate source families.
- Review template supports all review states.
- Copyright template records jurisdiction, edition, rights holder, evidence, and decision.
- Mandatory medical notice is explicit and reusable.
- Embedding model ADR exists but does not invent a final model without evaluation.
- No application code is created.
- All unresolved decisions are visible.

## Required Tests

- Markdown link/path validation
- Required-section validation
- Duplicate source ID check in the source inventory
- Manual review of medical notice language

## Manual Testing Steps

1. Open every created document.
2. Verify source status values match the blueprint.
3. Verify Marifetname and Ibn Sina are not merged.
4. Verify the medical notice explicitly directs users to a doctor or appropriate health professional.
5. Verify no code or future sprint implementation was added.

## Known Risks

- Source editions may not yet be licensed or digitized.
- OCR quality may be unknown.
- Embedding model choice remains pending evaluation.

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

