# Production Collection, Backup, and Restore Runbook

**Status:** NOT EXECUTED — no approved production corpus exists.

Before indexing, freeze a manifest containing collection version, source/page/chunk
counts, source hash, embedding model and dimension, chunking version, and creation time.
Index into staging first and bind every retrieval report to that manifest hash.

For each release:

1. Create a read-only collection snapshot and record its checksum and storage reference.
2. Copy the snapshot to the approved backup location and record retention and encryption.
3. Restore the backup into an isolated collection with a new name.
4. compare manifest, counts, IDs, source hashes, and sampled vectors.
5. Run collection-integrity and retrieval smoke tests against the restored collection.
6. Record operator, timestamps, tool versions, logs, result, and rollback target.

A path, command, or unexecuted procedure is not backup or restore verification.
