# Knowledge Publication Contract

**Classification:** AUTHORITATIVE

One immutable publication package contains:

- registry export and exact approved metadata
- source, page, chunk, OCR, and configuration fingerprints
- approved chunk dataset and citation/page metadata
- embedding model ID/version/license and configuration
- vector collection name/version/counts/checksum
- legal, OCR, subject, safety, chunk, and publication decision references
- production evaluation and safety reports
- publication manifest, compatibility version, created time, and authority signature
- backup/snapshot/restore evidence and rollback manifest

DA validates schema version, signatures/hashes, source allowlist, collection identity,
embedding compatibility, evaluation status, and rollback target before activation.
Publication is atomic. DA never accepts filesystem paths into KS working directories.
Revocation publishes a new manifest or activates a prior verified rollback manifest.
