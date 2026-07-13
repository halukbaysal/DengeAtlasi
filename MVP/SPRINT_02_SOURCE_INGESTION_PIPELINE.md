# Sprint 02 — Source Ingestion Pipeline

## Goal

Build the approved-source ingestion pipeline from registered document text to validated chunks and a reproducible ChromaDB index.

## Why Now

Retrieval and answer generation are meaningless without traceable, reviewed, edition-specific source data.

## Blueprint References

- `docs/blueprint/12_BACKEND_ARCHITECTURE.md`
- `docs/blueprint/14_DATA_MODEL.md`
- `docs/blueprint/33_RAG_AND_SOURCE_GOVERNANCE_SYSTEM.md`
- `docs/blueprint/40_CONTENT_OPERATIONS_MODEL.md`
- `docs/blueprint/41_SOURCE_REVIEW_WORKFLOW.md`
- `docs/blueprint/42_TAXONOMY_AND_METADATA.md`
- `docs/blueprint/60_TESTING_AND_QUALITY_STRATEGY.md`

## ADR References

- `docs/adr/ADR-002_FASTAPI_BACKEND.md`
- `docs/adr/ADR-003_CHROMADB_MVP.md`
- `docs/adr/ADR-008_MARIFETNAME_FIRST_ROUTING.md`
- `docs/adr/ADR-010_EMBEDDING_MODEL.md` if accepted

## Dependencies

- Sprint 01 complete
- At least one approved test source record or synthetic fixture
- Embedding model ADR accepted for production indexing, or mock embedding allowed for test-only work

## In Scope

- SourceRecord Pydantic models
- Metadata validation
- Review-status enforcement
- Normalization
- Semantic chunking strategy
- Chunk metadata
- Duplicate detection
- Embedding adapter
- ChromaDB adapter
- Deterministic indexing command
- Index report
- Test fixtures

## Out of Scope

- User-facing search
- Reranking
- LLM generation
- Temperament analysis
- Mobile source screens
- Automatic OCR
- Source approval decisions by AI

## Architecture Constraints

- Only `APPROVED` sources may enter the production index.
- Original and normalized text must remain distinct.
- Every chunk must map back to source, edition, section, and page.
- The embedding provider must use the approved adapter.
- Re-indexing must be deterministic and idempotent.
- AI may not approve sources.

## Implementation Tasks

1. Implement canonical source and chunk models.
2. Implement validation for required metadata.
3. Implement review-status gate.
4. Implement normalization preserving original text.
5. Implement semantic chunking with controlled overlap.
6. Add separate strategies for prose and poetry/table fixtures where applicable.
7. Generate stable chunk IDs and source hashes.
8. Implement duplicate and re-index handling.
9. Implement `EmbeddingProvider`.
10. Implement ChromaDB adapter.
11. Implement CLI/script for validation and indexing.
12. Produce machine-readable and human-readable index reports.
13. Add fixtures for Marifetname-primary and Ibn-Sina-supplementary records.
14. Add unit and integration tests.

## Acceptance Criteria

- Invalid or incomplete metadata is rejected.
- Non-APPROVED sources are excluded from production indexing.
- Original text remains available.
- Chunks retain page and section traceability.
- Re-indexing the same source does not create duplicates.
- Source updates create predictable replacements or versions.
- ChromaDB collection can be recreated from registered inputs.
- Index report lists accepted, rejected, skipped, and duplicate records.
- Test fixtures do not pretend to be licensed production content.
- No retrieval API or answer generation is implemented.

## Required Tests

- Metadata validation
- Status gate
- Stable source/chunk IDs
- Duplicate detection
- Idempotent re-index
- Page traceability
- ChromaDB integration
- Embedding adapter mock
- Low-quality or invalid fixture rejection

## Manual Testing Steps

1. Index an approved test fixture.
2. Attempt to index an unreviewed fixture.
3. Re-index the approved fixture.
4. Modify a source hash and re-index.
5. Inspect ChromaDB metadata.
6. Verify page and section fields.
7. Review the generated index report.

## Known Risks

- Real source editions may still be unavailable.
- OCR quality is outside this sprint.
- Embedding changes require complete re-indexing.

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

