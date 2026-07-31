# Source Library Structure

**Classification:** AUTHORITATIVE

Canonical logical layout:

```text
data/source-library/
  incoming/       transient local drop, untrusted
  originals/      immutable checksum-addressed local/object artifacts
  manifests/      intake and artifact inventories
  artifacts/      future versioned OCR/review/chunk/embedding artifacts
  reports/        future generated non-sensitive reports
```

Lifecycle is represented by registry and artifact state, never by moving source binaries
through workflow-named directories. The CLI creates or validates required local paths;
workflow folder markers are not authoritative. Binary sources, local manifests, registry
data, audit logs, immutable originals, OCR text, vectors, reviewer PII, and legal evidence
remain outside Git. Only reviewed, non-sensitive schemas and redacted reports may be
committed under a separately approved scope.

Filenames use lowercase safe ASCII where practical, underscores, `.pdf`, and collision
suffixes. Source IDs derive from a registry sequence/UUID, never the filename. SHA-256
identifies exact duplicates; a duplicate creates an audited reference rather than another
original. Backups preserve encrypted originals, registry, audit log, and manifests; restore
tests verify hashes and access controls.
