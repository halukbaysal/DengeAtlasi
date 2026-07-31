# KS-06 — Text Normalization, Chunk Preparation, and Chunk Review

**Product:** Knowledge Studio
**Status:** PLANNED — NOT_STARTED
**Owner:** UNASSIGNED
**Last updated:** 2026-07-31
**Authoritative roadmap:** `../KNOWLEDGE_STUDIO_ROADMAP.md`

## Purpose

Create citation-preserving candidate chunks from approved OCR/text artifacts and require human review before embedding.

## Dependencies

Verified metadata, reviewed OCR artifacts, source classification, required source approvals.

## In scope

- Text normalization with reversible mappings
- Heading/page-aware segmentation
- Candidate chunks
- Token counts
- Page and section provenance
- Lexicon-assisted normalization suggestions
- Chunk review workflow
- Rejection/revision
- Chunk dataset manifests

## Out of scope

- Embeddings
- Vector indexing
- Runtime publication
- LLM-generated claims

## Required architecture

Raw OCR, normalized text, and candidate chunks are separate layers. Every chunk must trace back to source pages and artifact versions.

## Data and state rules

Chunk IDs are deterministic from source/version/location/content. Approved chunks are immutable within a dataset version.

## Security and governance

Prompt-injection-like source text is preserved as source content but labeled; it must never become an instruction to build agents or answers.

## Required implementation work

Build normalization adapters, chunk builder, manifests, review integration, reports, and export format.

## Required tests

- Page boundary preservation
- Heading-aware chunks
- Deterministic IDs
- Reversible normalization
- Ottoman-term suggestion behavior
- Injection-text labeling
- Review transitions

## Acceptance criteria

- Every chunk has source/page provenance
- No unreviewed chunk is embedding-eligible
- Lexicon content is excluded from direct-answer chunk sets unless explicitly configured for lookup collections

## Required evidence

Reviewed fixture chunk dataset and validation report.

## Stop conditions

Stop if citation provenance is lost or chunk IDs are unstable.

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
