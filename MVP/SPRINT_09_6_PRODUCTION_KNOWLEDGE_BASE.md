# Sprint 09.6 — Production Knowledge Base

## Dependency

Requires Sprint 09.5A complete. Sprint 09.5B follows this sprint.

## Goal

Prepare a legally approved, human-reviewed, edition-specific Marifetname-primary and
Ibn Sina-supplementary production corpus without adding product features.

## Entry gate

Production content cannot be ingested without exact edition, publisher, publication
year, rights holder and usage decision, digital provenance, page-number confidence,
OCR suitability, and assigned human reviewers. Missing approval permits governance,
validation tooling, empty lifecycle directories, and clearly non-production samples
only. Legal, public-domain, OCR, human-review, or production status must never be
fabricated.

## Required workflow

```text
acquire → legal review → register edition → OCR/transcribe → OCR review
→ content review → metadata completion → chunk QA → APPROVED
→ staging index → retrieval evaluation → production approval
```

Production collections must be versioned and record source/chunk counts, source and
embedding hashes, model/chunking versions, creation time, snapshot, backup, restore,
and rollback procedures. ADR-010 remains proposed until a representative approved
mini-corpus and human-reviewed candidate benchmark exist.

## Completion rule

Complete only after exact editions and usage rights are approved, human review and
metadata are complete, ADR-010 is accepted, real embeddings and a versioned collection
exist, snapshot/backup/restore are verified, and real-corpus retrieval evaluation runs
without synthetic data. Otherwise report `BLOCKED` with exact missing approvals.
