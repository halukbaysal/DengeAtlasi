# KS-08 — Vector Collection Builder

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Build immutable, versioned staging vector collections from validated embedding artifacts.

## Dependencies

KS-07 validated embeddings; vector-store ADR and compatible secure version approved.

## In scope

- Collection manifest
- Build staging collection
- Metadata filters
- Source/category restrictions
- Integrity validation
- Version naming
- Rebuild/rollback preparation
- Collection inventory

## Out of scope

- Production activation
- End-user access
- Corpus publication approval
- Research agent

## Required architecture

Collections are immutable per version. A new build creates a new version rather than mutating the active collection.

## Data and state rules

Manifest links source versions, chunk dataset, embedding model, vector-store version, schema, filters, and integrity counts.

## Security and governance

Restricted/admin-only sources must be physically or logically isolated from production-answer collections.

## Required implementation work

Implement builder, validation, inventory, manifest, and staging-only commands.

## Required tests

- Count/integrity checks
- Metadata-filter checks
- Restricted-source isolation
- Rebuild determinism
- Version collision
- Failure rollback

## Acceptance criteria

- Staging collection matches manifest counts and checksums
- Restricted sources are excluded
- Active production collection is untouched
- Rollback target is identifiable

## Required evidence

Staging build report and manifest.

## Stop conditions

Stop if vector-store vulnerabilities or schema incompatibilities remain release-blocking.

## Completion report format

Codex must report:

1. Result: `PASS`, `PARTIAL`, `BLOCKED`, or `FAIL`
2. Files created
3. Files modified
4. Data migration impact
5. Commands executed
6. Test results
7. Acceptance-criteria matrix
8. Security and privacy impact
9. Known limitations
10. Human approvals still required
11. Exact Git status
12. Exact recommended next action
13. Confirmation that the next sprint was not started
