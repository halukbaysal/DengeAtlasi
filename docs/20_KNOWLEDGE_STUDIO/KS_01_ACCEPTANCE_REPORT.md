# KS-01 Acceptance Report

**Status:** READY FOR HUMAN ACCEPTANCE
**Date:** 2026-07-31
**Scope:** Source Registry and Immutable Local File Intake only

## 1. Executive summary

KS-01 passed architecture, CLI, registry, atomic intake, duplicate, audit, scope, and
publication-boundary verification. Eight PDFs were registered as `REGISTERED / UNTRUSTED`.
No OCR, metadata inference, classification, legal/safety/subject decision, chunking,
embedding, ChromaDB operation, production RAG change, or publication occurred.

## 2. KS-01 verification results

| Control | Result |
|---|---|
| Canonical KS registry separated from runtime `SourceRecord` | PASS |
| Content-addressed immutable originals | PASS |
| Streaming SHA-256 and stable source IDs | PASS |
| Exact duplicate and idempotency tests | PASS |
| Atomic copy/registry persistence and local lock | PASS |
| Append-only intake audit | PASS |
| REGISTERED / UNTRUSTED maximum | PASS |
| No prohibited runtime/mobile/vector behavior | PASS |

## 3. CLI verification

Implemented entry point:

```bash
python -m backend.ingestion.ingest_source
```

Verified command:

```bash
python -m backend.ingestion.ingest_source \
  --folder data/source-library/incoming \
  --library data/source-library
```

`--help` ran before registration and created no registry, audit, or original. The CLI
imports only `backend.ingestion.registry.SourceRegistry`.

## 4. Registry verification

- Registry: `data/source-library/manifests/source_registry.json`
- Audit: `data/source-library/manifests/intake_audit.jsonl`
- Records: 8
- Unique checksums: 8
- Unique source IDs: 8
- `SOURCE_REGISTERED` events: 8
- `EXACT_DUPLICATE_SKIPPED` events: 0
- Every original size and SHA-256 matches its registry record.
- Every bibliographic field remains `UNKNOWN`.

## 5. Registration results

| Original filename | Normalized filename | Source ID | Bytes | Registered at |
|---|---|---|---:|---|
| `111ibrahim_hakki_marifetname_compressed.pdf` | `111ibrahim_hakki_marifetname_compressed.pdf` | `KS-SRC-989ddff615b0efc90e62` | 72,934,397 | `2026-07-31T05:33:03.886091+00:00` |
| `231194.pdf` | `231194.pdf` | `KS-SRC-f65f090fa98f28e68993` | 21,074,552 | `2026-07-31T05:33:04.033797+00:00` |
| `c39012873.pdf` | `c39012873.pdf` | `KS-SRC-1dbb5e193157c9d9f16b` | 573,988 | `2026-07-31T05:33:04.073325+00:00` |
| `ibn_sina_sifa_kitabi_tip_kanunu_felsefe_meseleleri_muzik.pdf` | same | `KS-SRC-3c9f6e8793dc49936569` | 7,628,132 | `2026-07-31T05:33:04.085984+00:00` |
| `kitab-i_yildizname.pdf` | `kitab_i_yildizname.pdf` | `KS-SRC-9f8121d3325ea139a560` | 23,406,833 | `2026-07-31T05:33:04.129784+00:00` |
| `osmanlica_lugat.pdf` | `osmanlica_lugat.pdf` | `KS-SRC-6b92d757f732633f9cac` | 1,315,599 | `2026-07-31T05:33:04.173904+00:00` |
| `the_astrology_of_the_ottoman_empire_by_baris_ilhan.pdf` | same | `KS-SRC-35f50db06d0abce09d59` | 11,239,079 | `2026-07-31T05:33:04.190682+00:00` |
| `yldznameyihuseyn0001su.pdf` | `yldznameyihuseyn0001su.pdf` | `KS-SRC-2fd9f1c5c96360fb8ea4` | 9,136,506 | `2026-07-31T05:33:04.222890+00:00` |

SHA-256 values are recorded in the local registry and intake manifest; source binaries,
registry, audit, and originals remain excluded from Git.

## 6. Publication-boundary verification

Dry-run mapping was attempted for all eight records. Result: **8/8 BLOCKED**.

The boundary rejected each because KS-01 records are untrusted and lack OCR, legal,
subject, safety, chunk, embedding, evaluation, and publication approvals. This is the
required result.

## 7. Repository impact

KS-01 code is isolated under `backend/ingestion/registry`, the intake CLI, tests, and the
explicit publication boundary. No Git-visible change exists under `apps/mobile`,
`services/api`, or `packages/api-client`. Earlier uncommitted prototype and project-control
work remains in the same dirty worktree and must be excluded from a KS-01-only commit.

## 8. Files registered

Eight files were registered; none was moved from incoming, modified, OCR-processed, or
made searchable. Originals were copied to checksum-addressed local paths.

## 9. Duplicate detection

The initial set contained eight unique SHA-256 values. Duplicates skipped: `0`.
Automated tests verify same-content/different-name idempotency and duplicate audit events.

## 10. Known limitations

- Local JSON/JSONL persistence, not multi-host storage
- POSIX file lock; no Windows portability
- Header/MIME checks do not replace malware or full PDF structural scanning
- Application-enforced content-addressed immutability, not WORM storage
- Audit events are not cryptographically signed
- Admin authentication, RBAC, reviewer workflow, and later lifecycle stages are absent
- Deprecated prototype modules remain pending a separately reviewed cleanup

## 11. Human approval checklist

- [ ] Approve KS registry/runtime contract separation.
- [ ] Approve JSON/JSONL local persistence for KS-01 scope.
- [ ] Approve content-addressed original layout and Git exclusion.
- [ ] Accept eight records as REGISTERED / UNTRUSTED only.
- [ ] Confirm no legal, source, safety, OCR, or publication approval is implied.
- [ ] Approve a KS-01-only Git file boundary before commit.

## 12. Recommended next action

Human reviewers accept or reject KS-01 and its file boundary. If accepted, create a
KS-01-only commit without unrelated prototype/project-control changes. Do not begin KS-02
until separately authorized.
