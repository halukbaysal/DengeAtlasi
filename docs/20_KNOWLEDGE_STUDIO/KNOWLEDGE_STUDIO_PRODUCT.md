# Knowledge Studio Product

**Classification:** AUTHORITATIVE

Knowledge Studio controls discovery, intake, immutable originals, duplicate checks,
bibliographic/provenance records, OCR, legal/subject/safety/chunk review, embedding,
collection building, evaluation, publication, rollback, and audit.

Personas are intake operator, bibliographic researcher, OCR reviewer, legal reviewer,
subject reviewer, safety reviewer, evaluation reviewer, publication authority, security
administrator, and auditor. Assignments are currently UNASSIGNED.

It requires future authentication, role-based authorization, separation of duties,
tamper-evident audit events, job isolation, protected originals and review evidence,
versioned artifacts, backup/restore, and dual-control publication.

Research agents may discover candidates and bibliography but cannot approve or publish.
Their output always follows:

```text
DISCOVERY → REGISTRATION → STAGING → HUMAN REVIEW
→ APPROVAL → EVALUATION → PUBLICATION
```

KS hands immutable publication packages to DA. It is never required for normal DA
end-user runtime and contains no user journal or behavioral data.
