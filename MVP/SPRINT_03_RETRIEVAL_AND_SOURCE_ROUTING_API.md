# Sprint 03 — Retrieval and Source Routing API

## Goal

Implement query processing, Marifetname-first source routing, metadata-filtered retrieval, reranking abstraction, and a structured retrieval API.

## Why Now

The system must prove it can locate the right approved passages before any model-generated answer is allowed.

## Blueprint References

- `docs/blueprint/10_SYSTEM_ARCHITECTURE.md`
- `docs/blueprint/12_BACKEND_ARCHITECTURE.md`
- `docs/blueprint/13_TEMPERAMENT_AND_SOURCE_ROUTING_ENGINE.md`
- `docs/blueprint/15_API_STANDARDS.md`
- `docs/blueprint/30_AI_ARCHITECTURE.md`
- `docs/blueprint/33_RAG_AND_SOURCE_GOVERNANCE_SYSTEM.md`
- `docs/blueprint/34_MODEL_ROUTING_AND_PROVIDER_STRATEGY.md`

## ADR References

- `docs/adr/ADR-003_CHROMADB_MVP.md`
- `docs/adr/ADR-005_OPENAPI_CONTRACT_SOURCE.md`
- `docs/adr/ADR-008_MARIFETNAME_FIRST_ROUTING.md`

## Dependencies

- Sprint 02 complete
- Test index available

## In Scope

- Query validation and normalization
- Intent classification contract
- Deterministic source routing
- Marifetname-first retrieval
- Metadata filters
- Top-K retrieval
- Reranker interface and mock/default implementation
- Empty and insufficient result behavior
- Retrieval endpoint
- OpenAPI update
- Retrieval evaluation fixtures

## Out of Scope

- LLM answer generation
- Citation prose formatting
- Medical recommendation logic
- Mobile search screens
- Journal
- TTS

## Architecture Constraints

- Source routing is deterministic and server-controlled.
- Marifetname is queried first for relevant intents.
- Supplementary sources are separate result groups.
- Only approved-source chunks are returned.
- User input cannot choose arbitrary collections or priorities.
- Reranker is provider-independent.

## Implementation Tasks

1. Define retrieval request/response contracts.
2. Implement input limits and normalization.
3. Implement intent labels from taxonomy.
4. Implement source-routing matrix.
5. Query Marifetname first where applicable.
6. Query supplementary collections only when configured criteria are met.
7. Implement metadata-filtered ChromaDB retrieval.
8. Implement reranker interface.
9. Return structured result groups with score and source metadata.
10. Implement no-result and insufficient-result states.
11. Add `/api/v1/search` or canonical retrieval endpoint.
12. Regenerate OpenAPI and mobile client.
13. Add retrieval test dataset and metrics command.

## Acceptance Criteria

- Relevant temperament queries search Marifetname first.
- Ibn Sina results are labeled supplementary.
- Only approved chunks appear.
- Page, section, edition, and source ID are returned.
- User input cannot bypass source priorities.
- Empty results return a stable response, not an exception.
- Retrieval endpoint validates payload size.
- OpenAPI client generation still passes.
- Retrieval Recall@5 can be measured.
- No generative answer is returned.

## Required Tests

- Intent classification
- Routing matrix
- Marifetname-first order
- Supplement fallback
- Approved-only filtering
- Metadata integrity
- Empty results
- Oversized input rejection
- Reranker adapter
- Recall@5 evaluation command

## Manual Testing Steps

1. Search a known Marifetname fixture topic.
2. Search a topic requiring an Ibn Sina supplement.
3. Search an unsupported topic.
4. Attempt to request an unapproved source.
5. Inspect result order and metadata.
6. Run retrieval evaluation.

## Known Risks

- Small corpora can inflate retrieval metrics.
- Intent classification may initially use deterministic rules.
- Reranker provider may remain mock until later evaluation.

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

