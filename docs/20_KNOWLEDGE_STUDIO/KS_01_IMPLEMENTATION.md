# KS-01 Source Registry and Immutable Intake

**Classification:** AUTHORITATIVE IMPLEMENTATION NOTE
**Status:** IMPLEMENTED, validation evidence required with each change

## Architecture decision

Knowledge Studio intake uses `backend.ingestion.registry.KnowledgeSourceRecord`. It accepts
incomplete discovery metadata and fixes every new record at `REGISTERED / UNTRUSTED`.
Denge Atlası retains the strict `services.api.app.sources.SourceRecord` as a downstream
published-source contract. The boundary deliberately has no successful mapping in KS-01.

The earlier `DocumentMetadata` workflow and OCR/classification/chunk/embedding pipeline
are deprecated prototype evidence. They are not called by the KS-01 CLI and must not be
extended. Later sprints may migrate useful algorithms only after canonical-state tests.

## Storage contract

```text
data/source-library/
  incoming/                       local untrusted drop
  originals/aa/<sha256>.pdf       immutable content-addressed original
  manifests/source_registry.json  atomic canonical registry
  manifests/intake_audit.jsonl    append-only events
```

Originals, registry data, audit events, OCR work, review evidence, and reports are ignored
by Git. The local policy file, pre-existing folder markers, and pre-existing intake
checksum manifest remain visible. KS-01 adds no empty placeholder files.

## Intake guarantees

- stable `KS-SRC-<20 checksum chars>` identifier
- streamed SHA-256 and exact duplicate detection
- original and safe normalized filenames recorded separately
- positive size limit, `.pdf`, inferred MIME, and `%PDF-` header validation
- atomic checksum-verified original copy and atomic registry replacement
- exclusive local intake lock prevents concurrent registry lost updates
- append-only `SOURCE_REGISTERED` and `EXACT_DUPLICATE_SKIPPED` events
- deterministic sorted folder intake and idempotent repeated execution
- explicit `UNKNOWN` bibliography; no content inspection or classification

## Layout migration impact

No existing source or generated artifact is moved automatically.

| Existing area | KS disposition |
|---|---|
| `data/source-library/incoming` | retained as untrusted drop |
| legacy workflow-named source-library folders | retained pending audited migration |
| `data/raw`, `normalized`, `reviewed` | legacy production-governance placeholders |
| `data/chunks`, `embeddings`, `index` | legacy/generated downstream artifacts; not KS-01 |
| `data/ingestion` | deprecated prototype output and ignored |

Future cleanup requires a separately authorized migration with checksum verification.

## Explicit exclusions

No OCR, sidecar, metadata inference, source/safety classification, legal/subject approval,
chunking, embeddings, ChromaDB, RAG publication, admin API/UI, research agent, or PDF
import from the current source library was performed by KS-01 implementation.
