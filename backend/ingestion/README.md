# Knowledge Studio KS-01 Source Intake

This package implements only the canonical KS-01 source registry and immutable local file
intake. It does not expose an application API. Every accepted PDF ends at:

```text
intake_status = REGISTERED
trust_status = UNTRUSTED
```

The strict Denge Atlası runtime `SourceRecord` remains a separate published-source
contract. `publication_boundary.py` intentionally rejects mapping a KS-01 record into
that contract. Legacy OCR, classification, chunk, embedding, and report prototype modules
remain deprecated for migration evidence and are not invoked by this CLI.

## Commands

```bash
python -m backend.ingestion.ingest_source path/to/book.pdf
python -m backend.ingestion.ingest_source --folder books/
python -m backend.ingestion.ingest_source book.pdf --library /safe/local/source-library
```

The registry is atomically written to `manifests/source_registry.json`; append-only intake
events use `manifests/intake_audit.jsonl`. Originals use the content-addressed immutable
path `originals/<sha-prefix>/<sha256>.pdf`. Repeated imports are exact-checksum duplicates
and do not create another registry record or original.

KS-01 validates size, `.pdf`, MIME inference, and `%PDF-` header. It preserves the
original filename, records a safe normalized display filename, captures checksum/size/time,
and leaves all bibliographic fields `UNKNOWN`. It does not read PDF content beyond the
header, OCR, classify, decide copyright, chunk, embed, index, or publish.
