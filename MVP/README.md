# Denge Atlası — MVP Sprint Execution System

**Status:** SUPERSEDED AS PROJECT-CONTROL AUTHORITY
**Purpose:** Canonical execution entry point for sprint-by-sprint implementation.

> Historical note: this file remains as evidence of the original single-product sprint
> sequence. Future work must begin at
> [`docs/00_PROJECT_CONTROL/MASTER_PROJECT_BLUEPRINT.md`](../docs/00_PROJECT_CONTROL/MASTER_PROJECT_BLUEPRINT.md)
> and use separate DA/KS roadmap identifiers. Existing sprint files are not deleted.

---

## 1. Operating Model

```text
Blueprint documents = Product and architecture constitution
ADR documents = Accepted technical decisions
Sprint document = Implementation contract
Agent document = Worker rules
Completion report = Evidence of work
```

No agent may invent the product while coding.

---

## 2. Mandatory Read Order

For every sprint, read in this order:

```text
1. AGENTS/CODEX_AGENT.md or AGENTS/GEMINI_AGENT.md
2. AGENTS/SECURITY_RULES.md
3. MVP/README.md
4. Active MVP/SPRINT_XX_<NAME>.md
5. Blueprint documents listed in the active sprint
6. ADR documents listed in the active sprint
7. Existing repository code and tests
```

---

## 3. Direct Start Rule

When the user says:

```text
Sprint 01 başla
Sprint 02 başla
Start Sprint 03
Implement Sprint 04
```

the agent must:

1. Start immediately.
2. Ask no follow-up questions.
3. Inspect the repository.
4. Implement only the named sprint.
5. Run required checks.
6. Return the completion report.

Minor implementation details must be resolved using:

```text
active sprint
→ accepted ADR
→ blueprint
→ existing repository convention
→ safest minimal implementation
```

---

## 4. Blocker Rule

The agent may stop only for:

- Missing required repository or files
- Direct contradiction between accepted documents
- Missing mandatory legal/source approval
- Inaccessible build environment
- Unsatisfied safety requirement

The agent must not ask an open-ended question.

It must return:

```text
Status: BLOCKED
Exact blocker:
Files or decisions involved:
Work completed:
Safest resolution:
```

---

## 5. Sprint Sequence

```text
Sprint 00 — Product and Source Decisions
Sprint 01 — Engineering Foundation
Sprint 02 — Source Ingestion Pipeline
Sprint 03 — Retrieval and Source Routing API
Sprint 04 — Grounded Answer and Citation Engine
Sprint 05 — Mobile Search and Source Experience
Sprint 06 — Temperament Analysis
Sprint 07 — Reflection Journal
Sprint 08 — Native TTS
Sprint 09 — Security, Safety, and Evaluation
Sprint 09.5A — Evaluation Framework
Sprint 09.6 — Production Knowledge Base
Sprint 09.5B — Production Evaluation
Sprint 09 Final Closure
Sprint 10 — Beta Hardening and Release Readiness
```

Sprint numbers are dependency order, not duration.

---

## 6. Global Architecture Constraints

```text
Mobile: React Native CLI + TypeScript
State: Zustand
Validation: Zod
Local database: SQLite
Backend: Python + FastAPI
Backend validation: Pydantic
Vector database: ChromaDB
API contract: OpenAPI
Containerization: Docker
Authentication: none in MVP
Cloud sync: none in MVP
Camera/facial analysis: prohibited
```

---

## 7. Global Safety Constraints

Never implement:

- Facial character or personality inference
- Emotion recognition
- Medical diagnosis
- Treatment or medication advice
- Herbal prescriptions or dosage
- Deterministic personality classification
- Nafs ranking
- Fate or future prediction
- Unsupported citations
- Unapproved sources

Historical health content must include the mandatory doctor notice.

---

## 8. Definition of Done

A sprint is complete only when:

- All acceptance criteria pass.
- Required tests are added.
- Required commands run successfully.
- Skipped or unavailable commands are reported.
- Documentation is updated.
- No future sprint scope is included.
- Security and privacy implications are reported.
- Completion report is provided.

---

## 9. Standard Execution Prompt

```text
Read:

AGENTS/CODEX_AGENT.md
AGENTS/SECURITY_RULES.md
MVP/README.md
MVP/SPRINT_XX_<NAME>.md
All blueprint and ADR files referenced by the sprint.

Inspect the existing project.

Implement Sprint XX only.

Do not ask follow-up questions.
Begin immediately.
Follow all acceptance criteria.
Do not implement future sprints.
Do not silently change architecture.

After implementation provide the required completion report.
```
