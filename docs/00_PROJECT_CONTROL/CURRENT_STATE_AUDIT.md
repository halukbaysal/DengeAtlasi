# Current State Audit

**Classification:** AUTHORITATIVE
**Evidence cutoff:** 2026-07-31

Code, tests, Git history, and operational reports outrank claimed sprint status.

| Legacy scope | Claimed status | Verified status | Evidence | Gaps / disposition |
|---|---|---|---|---|
| Sprint 00 governance | Complete | VERIFIED_COMPLETE | ADR-001–010, source registry, validation | ADR-010 intentionally proposed |
| Sprint 01 foundation | Complete | VERIFIED_COMPLETE | monorepo, CI, locks, Docker, OpenAPI | Root README status text is stale |
| Sprint 02 ingestion | Complete | VERIFIED_COMPLETE for synthetic API-side flow | `services/api/app/rag`, source tests, tag `v0.2-ingestion` | Not a production/admin ingestion product; map shared pieces to KS |
| Sprint 03 retrieval | Complete | VERIFIED_COMPLETE for test-configured runtime | search API, routing/store tests, tag `v0.3-retrieval` | Production collection/model absent |
| Sprint 04 grounded answer | Complete | VERIFIED_COMPLETE for mock-provider behavior | analysis service, citations, tests | Production LLM/corpus absent |
| Sprint 05 mobile sources | Complete | VERIFIED_COMPLETE automated scope | screens/components/validation/tests | Device/network beta evidence incomplete |
| Sprint 06 temperament | Complete | VERIFIED_COMPLETE automated scope | API/mobile flow and tests | Production source evidence absent |
| Sprint 07 journal | Complete | VERIFIED_COMPLETE automated scope | SQLite repository/service/tests | Store/privacy validation pending |
| Sprint 08 TTS | Complete | VERIFIED_COMPLETE automated scope | adapter/component/tests | Real-device checklist remains human |
| Sprint 09 security | Partial | VERIFIED_PARTIAL | middleware, policies, reports, commit `04e4b81` | red-team and vulnerabilities open |
| Sprint 09.5A | Complete framework | VERIFIED_COMPLETE | schemas, 103 cases, reports, CI smoke | explicitly not production evidence |
| Sprint 09.6 | Blocked | BLOCKED | governance models/report, commit `d306923` | no approved corpus or operations |
| Sprint 09.5B | Blocked | BLOCKED | blocked report | all production metrics unmeasured |
| Sprint 10 | Not started | NOT_STARTED | no implementation commit | depends on DA and corpus gates |
| KS-00 governance | Approved | APPROVED_COMPLETE | authoritative governance, architecture, lifecycle, and KS-00–KS-14 roadmap | committed as one governance baseline |
| KS-01 registry/intake | Implemented and committed | VERIFIED_COMPLETE / COMMITTED | commit `2b9471124dbdb44b55bb3c28b96b36e3f23fdd32`; 8 unique sources registered; 8 REGISTERED / UNTRUSTED; publication blocked 8/8 | zero exact duplicates; later lifecycle remains blocked |
| Legacy ingestion prototype | Previously requested pipeline | SUPERSEDED / DEPRECATED | old workflow modules retained for migration evidence | must not be extended |
| `data/source-library` | Local intake and canonical registry | VERIFIED_PARTIAL, LOCAL DATA | 8 incoming PDFs, 8 immutable originals, canonical registry/audit | all source and generated artifacts remain excluded from Git |
| Knowledge Studio beyond KS-01 | Idea mixed into Sprint 09.x | NOT_STARTED | no auth/admin API/UI/reviewer workflow system | follow KS-02+ only when authorized |
| Research agent / Sprint 09.55 | Referenced by prompt | UNKNOWN | named file absent from repository | map concept to KS-13; do not invent contract |

## Conflicts and drift

- `README.md` introduction says the repository is at Sprint 03 although code reaches
  Sprint 09 work.
- `MVP/README.md` treats one sprint chain as authority for two products.
- Runtime `SourceRecord` and canonical KS registry are separated by an explicit boundary.
  Deprecated prototype workflow enums remain temporarily for migration evidence.
- `data/raw` lifecycle guidance and `data/source-library` use competing layouts.
- ChromaDB is an accepted MVP direction, while the production embedding decision and
  collection are absent; test infrastructure must not be described as production.
- Completion reports accurately document work but are supporting evidence, not authority.

## Existing-document disposition

| Area | Classification |
|---|---|
| This control directory and new product policies | AUTHORITATIVE |
| Accepted ADRs | AUTHORITATIVE technical decisions within their scope |
| `docs/blueprint` | SUPPORTING; superseded where this blueprint sets product control |
| `MVP/SPRINT_00`–`SPRINT_10` | HISTORICAL execution contracts |
| Decimal Sprint 09.5/09.6 sequencing | SUPERSEDED by DA/KS roadmaps |
| Testing/security/operations reports | SUPPORTING evidence with recorded dates |
| Completion claims unsupported by code/tests | HISTORICAL claim only |

## Recommended disposition

The obsolete uncommitted ingestion prototype was archived outside the repository and
removed from the worktree. Treat the committed KS-01 registry as the only canonical
intake implementation. KS-02 through KS-14 remain `PLANNED / NOT_STARTED`.
