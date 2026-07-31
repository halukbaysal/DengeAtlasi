# KS-02 Metadata and Provenance Workspace

**Classification:** AUTHORITATIVE IMPLEMENTATION NOTE
**Status:** IMPLEMENTED — AWAITING HUMAN ACCEPTANCE
**Date:** 2026-07-31

## Architecture

KS-02 extends the committed KS-01 boundary without changing its canonical
`KnowledgeSourceRecord`, registry schema, source IDs, checksums, intake/trust states, or
publication rejection. Candidate bibliography is stored separately in
`manifests/metadata_workspace.json`, with append-only events in
`manifests/metadata_audit.jsonl`. Both remain local and excluded from Git.

Each workspace record binds to a registered `source_id` and its immutable registry
SHA-256. Initialization is migration-free: it creates an empty version-zero workspace
record for every registered source and writes nothing into `source_registry.json`.

## Metadata schema

Supported candidate fields are:

- title, author, editor, translator, publisher, edition, publication year;
- language, script, page count;
- section title and section locator.

Each `MetadataCandidate` contains a stable candidate ID, source ID, field, value,
evidence references, optional confidence, state, actor/time, optional superseded
candidate, and optional human review decision. Candidates are never merged by field.

`UNKNOWN` is an explicit value with no claimed evidence and cannot be verified as a
bibliographic fact. Every non-`UNKNOWN` candidate requires at least one evidence
reference with source ID, evidence kind, locator, description, artifact SHA-256, optional
page, and local-restricted visibility.

## Provenance and corrections

`ProvenanceRecord` stores an evidence-backed statement, actor/time, and optional
superseded record. Corrections append a new candidate or provenance record pointing to
the earlier record. Earlier values remain intact.

Per-source optimistic versions reject stale updates. Atomic replacement and a local POSIX
lock prevent partial workspace writes and concurrent lost updates.

## Human verification boundary

New non-unknown values enter `HUMAN_REVIEW_REQUIRED`; unknowns enter
`CANDIDATE_CAPTURED`. Only an explicit service/CLI call with actor role
`HUMAN_METADATA_REVIEWER` may mark a candidate `VERIFIED` or `REJECTED`. Metadata
verification does not alter registry trust/intake fields or create legal, subject,
safety, OCR, chunk, embedding, evaluation, or publication decisions.

## Audit and reports

Append-only event types are:

- `METADATA_CANDIDATE_ADDED`;
- `METADATA_CANDIDATE_REVIEWED`;
- `PROVENANCE_RECORDED`;
- `METADATA_EXPORT_CREATED`.

The JSON export covers every registered source, preserves all conflicting candidates and
provenance, lists unresolved fields, repeats registry intake/trust states, and explicitly
sets all approval flags false. No filename-derived bibliography is emitted.

## CLI

```bash
python -m backend.ingestion.metadata_workspace --help
```

Commands: `initialize`, `add-candidate`, `add-provenance`, `review`,
`import-workspace`, and `export`. Workspace import validates registry fingerprints,
rejects imported review decisions, preserves ID/content conflicts, and is idempotent.
Evidence must be supplied by a human/operator; the CLI performs no PDF content reading,
OCR, filename inference, web access, classification, or approval.

## Storage impact

The local implementation created:

- `data/source-library/manifests/metadata_workspace.json`;
- `data/source-library/manifests/metadata_audit.jsonl`;
- `data/source-library/manifests/.metadata.lock`;
- `data/source-library/reports/ks02_metadata_report.json`.

These are ignored local artifacts. The report covers eight registered sources with no
asserted bibliographic candidates; every field remains unresolved. Registry and all eight
immutable-original checksums matched before and after initialization/export.

## Explicit exclusions

KS-03 OCR, classification, legal/subject/safety approval, chunking, embeddings,
ChromaDB/vector operations, publication, runtime API changes, and mobile changes were not
implemented or executed.
