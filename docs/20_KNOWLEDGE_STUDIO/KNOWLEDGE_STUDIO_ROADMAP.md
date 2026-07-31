# Knowledge Studio Roadmap

**Classification:** AUTHORITATIVE

Each sprint is one focused implementation session. Common exclusions until explicitly
listed are production publication, DA behavior changes, and future sprint scope. Every
sprint updates architecture/audit evidence and reports exact commands and Git state.

## KS-00 — Product and Architecture Baseline

**Status:** APPROVED_COMPLETE

- **Objective/dependency:** Establish approved KS scope and boundaries; depends on human
  approval of project control.
- **In scope/deliverables:** product definition, lifecycle, threat/data-flow model,
  canonical schemas decision and repository package boundary.
- **Out of scope:** operational code, file import, OCR, admin surfaces.
- **Acceptance/tests:** document link/ID validation; no conflicting statuses; architecture,
  security, privacy, and content owners approve.
- **Security/docs/evidence:** RBAC and trust boundaries documented; signed decision record.

## KS-01 — Source Registry and Local File Intake

**Status:** VERIFIED_COMPLETE / COMMITTED

Commit `2b9471124dbdb44b55bb3c28b96b36e3f23fdd32`; eight unique sources registered,
zero exact duplicates, all eight `REGISTERED / UNTRUSTED`, publication blocked 8/8.

- **Objective/dependency:** Register untrusted local files safely; KS-00.
- **In scope/deliverables:** durable registry, source IDs, filename normalization,
  SHA-256 duplicates, MIME/size limits, immutable-original abstraction, intake CLI,
  audit events, migration of current prototype/layout.
- **Out of scope:** metadata inference, OCR, classification, approvals.
- **Acceptance/tests:** duplicate/collision, tampered checksum, unsupported type,
  idempotency, path traversal and interrupted-copy tests; originals never enter Git.
- **Security/docs/evidence:** least-privilege local storage and intake threat update;
  test log plus sample non-sensitive manifest.

## KS-02 — Metadata and Provenance

**Status:** IMPLEMENTED / AWAITING HUMAN ACCEPTANCE

- **Objective/dependency:** Capture evidence-backed bibliography; KS-01.
- **In scope/deliverables:** versioned metadata/provenance schema, UNKNOWN semantics,
  evidence references, edition/section records, manual correction history.
- **Out of scope:** legal decision, OCR, automatic trust.
- **Acceptance/tests:** required fields, evidence validation, concurrency/version and
  no-fabrication tests; reviewed schema migration.
- **Security/docs/evidence:** provenance visibility controls; metadata QA report.

## KS-03 — OCR Orchestration

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Produce reviewable text artifacts; KS-02 and OCR decision.
- **In scope/deliverables:** sandboxed job adapter, page images/text/confidence, original
  versus normalized text, retries/failures, artifact versions.
- **Out of scope:** OCR approval, chunking, embeddings.
- **Acceptance/tests:** page boundaries, low-confidence/failure, malicious PDF, timeout,
  reproducibility and artifact-hash tests.
- **Security/docs/evidence:** worker isolation, resource/network limits; benchmark and
  operator runbook.

## KS-04 — Review and Approval Workflow

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Record independent human decisions; KS-02, optionally KS-03.
- **In scope/deliverables:** assignments, legal/OCR/subject decisions, changes requested,
  evidence, expiry, separation of duties, immutable audit history.
- **Out of scope:** automatic approval, embeddings, admin UI.
- **Acceptance/tests:** authorization matrix, invalid transition, expiry/revoke, dual-role
  separate-decision, optimistic-lock and audit tests.
- **Security/docs/evidence:** future identity/RBAC contract; reviewer workflow report.

## KS-05 — Safety and Source Classification

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Classify source role and restrictions; KS-02/04.
- **In scope/deliverables:** Marifetname/Ibn Sina hierarchy, lexicon-only role,
  historical-astrology restrictions, safety labels and human override.
- **Out of scope:** user personality/fate/medical conclusions or publication.
- **Acceptance/tests:** unknown/default-deny, astrology, lexicon, medical, third-party,
  child and injection fixtures; human review remains mandatory.
- **Security/docs/evidence:** poisoned-content controls; signed classification report.

## KS-06 — Chunk Preparation and Review

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Create page-traceable candidate chunks; cleared inputs from
  KS-03–05.
- **In scope/deliverables:** versioned normalization/chunking, paragraph/heading/page
  boundaries, duplicate/artifact QA, chunk review decisions.
- **Out of scope:** embeddings and collections.
- **Acceptance/tests:** boundary, quotation, poetry/table, duplicate, merged-edition,
  missing metadata and deterministic-ID tests.
- **Security/docs/evidence:** instruction-like source remains data; chunk QA report.

## KS-07 — Embedding Pipeline

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Generate candidate embeddings; KS-06 plus accepted ADR-010.
- **In scope/deliverables:** pinned provider/model/config, approved-chunk eligibility,
  batching, hashes, cost/latency records, failure/re-index/rollback plans.
- **Out of scope:** vector publication or model selection without evidence.
- **Acceptance/tests:** blocked unapproved input, dimensions/counts, retry/idempotency,
  provider privacy/failure and reproducibility tests.
- **Security/docs/evidence:** secret/data-retention controls; accepted ADR and run report.

## KS-08 — Vector Collection Builder

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Build isolated versioned candidates; KS-07.
- **In scope/deliverables:** allowlisted-source collection builder, manifests, snapshot,
  backup, restore, integrity and rollback preparation.
- **Out of scope:** DA activation.
- **Acceptance/tests:** count/hash/filter, mixed-source rejection, snapshot and isolated
  restore tests.
- **Security/docs/evidence:** no arbitrary collection selection; restore evidence.

## KS-09 — Production Corpus Evaluation

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Assess exact candidate quality; KS-08 and approved reviewers.
- **In scope/deliverables:** 100-case first dataset, retrieval/citation/unsupported/safety/
  latency metrics, failure taxonomy and regression queue.
- **Out of scope:** framework scores as production proof or silent thresholds.
- **Acceptance/tests:** dataset/evidence/duplicate validation, scorer regressions, exact
  collection binding and threshold report.
- **Security/docs/evidence:** injection/red-team cases protected; reviewer-approved report.

## KS-10 — Controlled Publication

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Promote a passing candidate atomically; KS-09 and all gates.
- **In scope/deliverables:** signed publication/rollback manifests, dual control, DA
  compatibility handshake, revocation and rollback.
- **Out of scope:** DA/store release.
- **Acceptance/tests:** missing signature/evidence, tamper, compatibility, atomic switch,
  rollback and disaster drill.
- **Security/docs/evidence:** publication least privilege; signed release record.

## KS-11 — Admin API

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Expose stable workflows; KS-04–10 domain stability.
- **In scope/deliverables:** authenticated, versioned, role-scoped admin contracts,
  pagination, jobs, audit queries.
- **Out of scope:** public endpoints or consumer access.
- **Acceptance/tests:** authn/authz, object-level access, CSRF/rate/size, audit, OpenAPI.
- **Security/docs/evidence:** threat model and API security review.

## KS-12 — Admin Web Interface

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Usable reviewer console; KS-11.
- **In scope/deliverables:** queues, evidence comparison, accessible decision controls,
  status/audit visibility and safe file preview.
- **Out of scope:** automatic decisions or public UI.
- **Acceptance/tests:** role journeys, accessibility, unsafe rendering/XSS, stale-write,
  explicit confirmation and browser matrix.
- **Security/docs/evidence:** CSP/session/privacy review; usability evidence.

## KS-13 — Research Agent

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Assist discovery only; KS-01/02/04/05/11 controls stable.
- **In scope/deliverables:** allowlisted research connectors, citations/provenance,
  discovery records, budgets, human registration handoff.
- **Out of scope:** downloads/approval/OCR/embedding/publication without workflow.
- **Acceptance/tests:** prompt injection, poisoned page, missing citation, duplicate,
  egress/domain, budget and direct-publication denial.
- **Security/docs/evidence:** untrusted-agent threat review; discovery audit samples.

## KS-14 — Security Hardening and Production Operations

**Status:** PLANNED / NOT_STARTED

- **Objective/dependency:** Close cross-system security and operational gaps; stable KS
  product and controlled publication workflow.
- **In scope/deliverables:** penetration/red-team, dependency/container hardening, secrets,
  audit integrity, retention, incident response, backups, restore/failover, monitoring,
  SLOs, deployment readiness, capacity/cost, on-call and production runbooks.
- **Out of scope:** feature expansion.
- **Acceptance/tests:** vulnerability gates, manual role/worker/publication attacks,
  backup/restore, failover, rollback, alert, incident and runbook drills, log/privacy
  inspection.
- **Security/docs/evidence:** human security and production-readiness sign-off, updated
  risk register, recovery evidence and assigned operational owners.

## Legacy migration map

| Legacy scope | New roadmap |
|---|---|
| Sprint 02 ingestion primitives | Shared candidates reviewed in KS-01/06/07/08 |
| Sprint 09.5A framework | DA-08 and shared Phase A evaluation |
| Proposed Sprint 09.55 admin/research | KS-01/02/04/05/11/12/13 |
| Sprint 09.6 production knowledge base | KS-01 through KS-10 |
| Sprint 09.5B | KS-09 |
| Sprint 09 final closure | separate DA-08 and KS-10 gates |
