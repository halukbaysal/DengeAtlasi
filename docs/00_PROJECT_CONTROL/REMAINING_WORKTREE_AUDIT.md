# Remaining Worktree Audit

**Audit date:** 2026-07-31
**Repository:** DengeAtlasi
**Branch:** `main`
**Baseline:** `2b9471124dbdb44b55bb3c28b96b36e3f23fdd32`
**Disposition:** SUPERSEDED HISTORICAL AUDIT SNAPSHOT; final resolution is in section 18

> All inventory, “uncommitted,” KS-15, and proposed-decision statements in sections 1–17
> describe the historical worktree at audit capture time. They are not active roadmap or
> current-status claims.

## 1. Executive summary

The pre-report worktree contained exactly **82 Git-visible remaining files**: 4 modified
tracked files and 78 untracked files. Creating this required, deliberately untracked audit
report brings the final worktree to **83 files**: 4 modified and 79 untracked. The final
set divides into 32 KS-00 governance documents (including this report), 15 sprint
documents, 22 legacy/prototype ingestion files, 8 source-library folder markers, 5
root/shared configuration files, and 1 local intake manifest.

The documentation set is substantial rather than empty or placeholder-only, and its
relative Markdown links resolve. It is not ready for an authoritative commit unchanged:

- `CURRENT_STATE_AUDIT.md`, `KNOWLEDGE_STUDIO_ROADMAP.md`, and the already committed
  KS-01 acceptance report contain pre-commit/pre-acceptance status claims.
- The roadmap defines a separate KS-15 Production Operations sprint, while the supplied
  sprint set ends at KS-14 and combines security and production operations.
- `MASTER_PROJECT_BLUEPRINT.md` still labels `backend/ingestion/` uncommitted, despite
  the canonical KS-01 boundary now being committed.
- The prototype ingestion tree implements OCR, classification, chunking, embeddings,
  indexing, and report generation outside the accepted registry architecture. It is
  internally referenced only by its own tests and by the uncommitted root scripts.

No remaining file should be committed until the human decisions in section 17 are made.

## 2. Exact inventory totals

| Category | Count |
|---|---:|
| A. KS-00 project governance | 32 |
| B. Knowledge Studio sprint documents | 15 |
| C. Legacy or prototype ingestion code | 22 |
| D. Source-library scaffolding | 8 |
| E. Root or shared configuration | 5 |
| F. Local or generated artifacts | 1 |
| G. Unknown or unsafe | 0 |
| **Total** | **83** |

Ignored local binaries and generated registry artifacts are not part of the 83-file
Git-visible inventory, but are recorded in section 8 because they must remain local.

## 3. Complete file inventory and classification

### A. KS-00 project governance — 32 files

Evidence code `A1` means an untracked Markdown governance/product/control document under
the proposed authoritative documentation hierarchy. These files are candidate KS-00
material, subject to the conflicts in section 12.

| File | State | Evidence/disposition |
|---|---|---|
| `docs/00_PROJECT_CONTROL/AGENT_EXECUTION_RULES.md` | untracked | A1; governance candidate |
| `docs/00_PROJECT_CONTROL/CURRENT_STATE_AUDIT.md` | untracked | A1; stale KS-01 claims must be corrected |
| `docs/00_PROJECT_CONTROL/DECISION_REGISTER.md` | untracked | A1; governance candidate |
| `docs/00_PROJECT_CONTROL/MASTER_PROJECT_BLUEPRINT.md` | untracked | A1; stale “uncommitted ingestion” wording |
| `docs/00_PROJECT_CONTROL/NEXT_ACTION_PLAN.md` | untracked | A1; pre-acceptance next action is stale |
| `docs/00_PROJECT_CONTROL/README.md` | untracked | A1; governance candidate |
| `docs/00_PROJECT_CONTROL/REMAINING_WORKTREE_AUDIT.md` | untracked | A1; required disposition report; review before any later commit |
| `docs/00_PROJECT_CONTROL/RISK_REGISTER.md` | untracked | A1; governance candidate |
| `docs/10_DENGE_ATLASI/DENGE_ATLASI_PRODUCT.md` | untracked | A1; DA product boundary |
| `docs/10_DENGE_ATLASI/DENGE_ATLASI_ROADMAP.md` | untracked | A1; legacy decimal mapping needs human review |
| `docs/10_DENGE_ATLASI/README.md` | untracked | A1; DA documentation index |
| `docs/10_DENGE_ATLASI/RELEASE_GATES.md` | untracked | A1; release governance |
| `docs/20_KNOWLEDGE_STUDIO/KNOWLEDGE_STUDIO_ARCHITECTURE.md` | untracked | A1; architecture candidate |
| `docs/20_KNOWLEDGE_STUDIO/KNOWLEDGE_STUDIO_PRODUCT.md` | untracked | A1; product candidate |
| `docs/20_KNOWLEDGE_STUDIO/KNOWLEDGE_STUDIO_ROADMAP.md` | untracked | A1; KS-14/KS-15 conflict |
| `docs/20_KNOWLEDGE_STUDIO/PUBLISHING_CONTRACT.md` | untracked | A1; publication boundary candidate |
| `docs/20_KNOWLEDGE_STUDIO/README.md` | untracked | A1; KS index candidate |
| `docs/20_KNOWLEDGE_STUDIO/SOURCE_LIBRARY_STRUCTURE.md` | untracked | A1; conflicts with legacy folders |
| `docs/20_KNOWLEDGE_STUDIO/SOURCE_LIFECYCLE.md` | untracked | A1; lifecycle candidate |
| `docs/30_SHARED_PLATFORM/INTEGRATION_BOUNDARIES.md` | untracked | A1; shared-boundary candidate |
| `docs/30_SHARED_PLATFORM/README.md` | untracked | A1; shared-platform index |
| `docs/40_SOURCE_GOVERNANCE/INITIAL_SOURCE_DISPOSITION.md` | untracked | A1; review for source-specific claims |
| `docs/40_SOURCE_GOVERNANCE/README.md` | untracked | A1; governance index |
| `docs/40_SOURCE_GOVERNANCE/SOURCE_POLICY.md` | untracked | A1; source-policy candidate |
| `docs/50_SECURITY_AND_PRIVACY/README.md` | untracked | A1; security/privacy baseline |
| `docs/60_EVALUATION/EVALUATION_STRATEGY.md` | untracked | A1; evaluation baseline |
| `docs/60_EVALUATION/README.md` | untracked | A1; evaluation index |
| `docs/70_RELEASE_ENGINEERING/README.md` | untracked | A1; release index |
| `docs/70_RELEASE_ENGINEERING/RELEASE_STRATEGY.md` | untracked | A1; release baseline |
| `docs/80_ADRS/README.md` | untracked | A1; ADR index |
| `docs/90_ARCHIVE/README.md` | untracked | A1; explicitly maps decimal sprints as superseded |
| `docs/DOCUMENTATION_INDEX.md` | untracked | A1; root documentation index |

### B. Knowledge Studio sprint documents — 15 files

All are untracked, non-empty sprint contracts extracted from the supplied roadmap archive.
They form one documentation unit, but the KS-14/KS-15 mismatch blocks an unchanged commit.

| File | Classification/evidence |
|---|---|
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-00_PRODUCT_FOUNDATION.md` | B; claims `VERIFIED_COMPLETE`; review acceptance evidence |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-01_SOURCE_REGISTRY.md` | B; pre-commit wording needs reconciliation |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-02_METADATA_AND_PROVENANCE.md` | B; planned only; KS-02 not started |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-03_OCR_PIPELINE.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-04_REVIEW_WORKFLOW.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-05_SOURCE_CLASSIFICATION.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-06_CHUNK_PIPELINE.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-07_EMBEDDING_PIPELINE.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-08_VECTOR_COLLECTIONS.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-09_EVALUATION_FRAMEWORK.md` | B; planned production-corpus scope |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-10_PUBLICATION_PIPELINE.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-11_ADMIN_API.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-12_ADMIN_WEB_UI.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-13_RESEARCH_AGENT.md` | B; planned only |
| `docs/20_KNOWLEDGE_STUDIO/sprints/KS-14_PRODUCTION_OPERATIONS.md` | B; combines roadmap KS-14 and KS-15 |

### C. Legacy or prototype ingestion code — 22 files

Evidence code `C1` means the file belongs to a self-contained deprecated pipeline rooted
in `DocumentMetadata`. Repository search found no import from `apps/mobile`,
`services/api`, `packages/api-client`, CI, or the KS-01 CLI. The only code consumers are
other C1 files and `test_ingestion.py`. The uncommitted `package.json` would newly add
this tree to root lint/typecheck/test commands. These files duplicate or prematurely
implement later KS-02 through KS-08 responsibilities and are **unsafe to commit now**.

| File | Role and later disposition |
|---|---|
| `backend/ingestion/chunking/__init__.py` | C1; prototype export; archive/cleanup candidate |
| `backend/ingestion/chunking/chunker.py` | C1; KS-06-like chunker; migration evidence only |
| `backend/ingestion/classifiers/__init__.py` | C1; prototype export |
| `backend/ingestion/classifiers/source.py` | C1; KS-05-like filename/text heuristics; unsafe authority |
| `backend/ingestion/embeddings/__init__.py` | C1; prototype export |
| `backend/ingestion/embeddings/service.py` | C1; KS-07-like embedding helper; no accepted ADR |
| `backend/ingestion/metadata/__init__.py` | C1; prototype export |
| `backend/ingestion/metadata/extractor.py` | C1; KS-02-like inference; conflicts with no-fabrication workflow |
| `backend/ingestion/ocr/__init__.py` | C1; prototype export |
| `backend/ingestion/ocr/engine.py` | C1; sidecar OCR abstraction; not canonical KS-03 |
| `backend/ingestion/pipeline/__init__.py` | C1; prototype export |
| `backend/ingestion/pipeline/indexer.py` | C1; writes vector index; conflicts with KS-01 scope |
| `backend/ingestion/pipeline/service.py` | C1; executes metadata/classification/OCR/chunk/report operations |
| `backend/ingestion/reports/__init__.py` | C1; prototype export |
| `backend/ingestion/reports/writer.py` | C1; generated prototype reports |
| `backend/ingestion/reviewers/__init__.py` | C1; prototype export |
| `backend/ingestion/reviewers/rules.py` | C1; non-human workflow heuristics; later review required |
| `backend/ingestion/schemas/__init__.py` | C1; old schema export |
| `backend/ingestion/schemas/models.py` | C1; overloaded deprecated lifecycle, duplicates KS registry concepts |
| `backend/ingestion/tests/__init__.py` | C1; only needed by prototype test package |
| `backend/ingestion/tests/test_ingestion.py` | C1; sole external consumer of most prototype modules |
| `backend/ingestion/utils/__init__.py` | C1; empty package placeholder; obsolete |

### D. Source-library scaffolding — 8 files

All are empty untracked folder markers. They describe the earlier workflow layout, not the
authoritative KS-01 content-addressed `originals/` plus `manifests/` layout. `incoming/`
remains a valid local drop; `approved/`, `copyright-review/`, `discovered/`, `downloaded/`,
`human-review/`, `ocr-pending/`, and `rejected/` encode lifecycle in directories and
overlap the planned record/artifact state model. Commit only after an explicit migration
decision.

| File | Disposition |
|---|---|
| `data/source-library/approved/.gitkeep` | D; obsolete/duplicate convention candidate |
| `data/source-library/copyright-review/.gitkeep` | D; obsolete/duplicate convention candidate |
| `data/source-library/discovered/.gitkeep` | D; obsolete/duplicate convention candidate |
| `data/source-library/downloaded/.gitkeep` | D; obsolete/duplicate convention candidate |
| `data/source-library/human-review/.gitkeep` | D; obsolete/duplicate convention candidate |
| `data/source-library/incoming/.gitkeep` | D; valid local-drop marker candidate |
| `data/source-library/ocr-pending/.gitkeep` | D; obsolete/duplicate convention candidate |
| `data/source-library/rejected/.gitkeep` | D; obsolete/duplicate convention candidate |

### E. Root or shared configuration — 5 files

| File | State | Evidence/disposition |
|---|---|---|
| `.gitignore` | modified | Adds `data/ingestion/`; prior prototype-output protection, not required by canonical KS-01 paths |
| `MVP/README.md` | modified | KS-00 governance change; marks legacy sprint authority superseded |
| `README.md` | modified | KS-00 governance links; corrects stale Sprint 03 framing without deleting historical text |
| `package.json` | modified | Mixes KS-01 checks with unsafe prototype checks; must be split/reviewed |
| `backend/__init__.py` | untracked | Shared Python package marker; potentially supports KS imports, but KS-01 tests already passed without committing it |

`MVP/README.md` and `README.md` logically belong with a corrected KS-00 governance commit.
`.gitignore`, `package.json`, and `backend/__init__.py` require separate human review.

### F. Local or generated artifacts — 1 Git-visible file

| File | State | Disposition |
|---|---|---|
| `data/source-library/incoming/source_manifest.json` | untracked by explicit negation rule | Contains filenames, sizes, checksums, and import timestamps for eight local PDFs; keep local and exclude from every commit unless a separately approved sanitized-manifest policy is adopted |

### G. Unknown or unsafe — 0 files

Every Git-visible file could be classified from repository evidence. “Unsafe to commit”
prototype files remain in category C rather than being duplicated here.

## 4. Documentation quality verification

- Empty files: none among the 46 remaining documentation files.
- Placeholder-only documents: none; short README files are indexes, not empty stubs.
- Markdown links: 48 files inspected (including two committed KS-01 documents), 0 broken
  relative links.
- Duplicate documents: no byte-for-byte duplicate was identified. There is intentional
  subject overlap between the master blueprint, product documents, roadmap, sprint
  contracts, and indexes; authority labels must remain explicit.
- Obsolete decimal Sprint 09 references: retained in `CURRENT_STATE_AUDIT.md`,
  `DENGE_ATLASI_ROADMAP.md`, `KNOWLEDGE_STUDIO_ROADMAP.md`, and
  `docs/90_ARCHIVE/README.md` as migration/history mappings. They must not be interpreted
  as active sequencing.
- Incorrect status claims:
  - `CURRENT_STATE_AUDIT.md` says KS-01 is uncommitted, current PDFs were not imported,
    and the registry is not populated. All three are stale.
  - `KNOWLEDGE_STUDIO_ROADMAP.md` says KS-01 is uncommitted and no repository PDF was
    imported. Both are stale.
  - `MASTER_PROJECT_BLUEPRINT.md` calls all `backend/ingestion/` uncommitted, although
    the KS-01 registry boundary is committed.
  - `NEXT_ACTION_PLAN.md`, `KS-01_SOURCE_REGISTRY.md`, and the committed
    `KS_01_ACCEPTANCE_REPORT.md` contain pre-commit/pre-human-acceptance actions.
- Roadmap conflict: `KNOWLEDGE_STUDIO_ROADMAP.md` defines KS-14 Security Hardening and
  KS-15 Production Operations. The requested archive and sprint directory define only
  KS-00 through KS-14, with `KS-14_PRODUCTION_OPERATIONS.md` combining both scopes.
- The KS-00 sprint file claims `VERIFIED_COMPLETE`, while its own acceptance criteria
  include human agreement and a signed decision record; repository evidence does not
  prove those human approvals.

## 5. Prototype code dependency analysis

Searches covered `backend.ingestion`, explicit prototype module names, `from
backend.ingestion`, and `import backend.ingestion`.

| Consumer | Result |
|---|---|
| KS-01 CLI | imports only `backend.ingestion.registry.SourceRegistry`; independent |
| Runtime API (`services/api`) | no prototype imports found |
| Mobile application | no prototype imports found |
| API client | no prototype imports found |
| CI/scripts | no direct prototype references found |
| Prototype tests | `test_ingestion.py` imports and exercises the prototype tree |
| Root package scripts | uncommitted `package.json` would add all ingestion tests/checks |
| Documentation | accepted KS-01 docs explicitly label prototypes deprecated |

Archiving/removing category C later would not break known runtime, mobile, or KS-01 CLI
code. It would require removing or archiving `test_ingestion.py` and reconsidering the
uncommitted `package.json` changes in the same dedicated cleanup. No such action is
authorized by this audit.

## 6. Files safe to commit

No remaining file is proven safe to commit **unchanged** as an isolated, authoritative
unit. Conditional candidates after corrections and human review are:

1. Category A plus the KS-00 portions of `README.md` and `MVP/README.md`.
2. Category B after resolving KS-14 versus KS-15 and stale KS-01 status language.
3. `data/source-library/incoming/.gitkeep` only, if humans approve tracking that local
   drop-point structure.

## 7. Files requiring review

- All 32 category A governance documents: authority and stale status review.
- All 15 category B sprint documents: roadmap-numbering and acceptance review.
- All 22 category C files: archive versus later selective migration decision.
- All 8 category D markers: directory-state versus record-state architecture decision.
- All 5 category E files: mixed provenance and root-tooling impact.

## 8. Files that must remain local

The Git-visible `incoming/source_manifest.json` must remain local under current policy.
Repository inspection also confirmed these ignored artifacts:

- eight `data/source-library/incoming/*.pdf` source documents;
- eight content-addressed `data/source-library/originals/**/*.pdf` immutable copies;
- `data/source-library/manifests/source_registry.json`;
- `data/source-library/manifests/intake_audit.jsonl`;
- `data/source-library/manifests/.intake.lock`.

PDFs, registry data, audit data, originals, OCR output, vectors, caches, build output,
environment files, and secrets are excluded from every proposed commit.

## 9. Files that appear obsolete

- The 21 functional prototype pipeline/schema/test files in category C are superseded
  migration evidence, not canonical implementation.
- `backend/ingestion/utils/__init__.py` is an empty obsolete placeholder.
- Seven workflow-named `.gitkeep` markers other than `incoming/.gitkeep` conflict with
  record-based lifecycle design.
- The source manifest is an older intake manifest duplicated in function by the canonical
  local registry, though it must be preserved locally until an authorized migration.

## 10. Files that conflict with KS-01

- `backend/ingestion/schemas/models.py` defines a second intake/workflow model and
  overloaded ready states.
- `metadata/extractor.py`, `classifiers/source.py`, `ocr/engine.py`,
  `chunking/chunker.py`, `embeddings/service.py`, and `pipeline/indexer.py` implement
  operations explicitly outside KS-01.
- `pipeline/service.py` composes those operations without the canonical registry.
- `package.json` would make these deprecated tests part of the root default test command.
- Workflow-named source-library folders compete with registry/artifact state.
- Governance documents containing “uncommitted/unpopulated/not imported” claims conflict
  with the accepted and committed KS-01 state.

## 11. Proposed commit sequence

No commits were created. After resolving section 17:

1. **Governance baseline** — corrected category A documents plus only the governance
   hunks in `README.md` and `MVP/README.md`.
2. **Sprint roadmap** — corrected category B documents after a single KS-00–KS-14 or
   KS-00–KS-15 decision.
3. **Source-library scaffolding** — only approved non-sensitive `.gitkeep` structure;
   likely just `incoming/.gitkeep`. Do not include the local manifest.

Do not include category C in these commits. If humans later decide it is obsolete,
perform a separately authorized cleanup/archive change with dependency validation.

## 12. Proposed commit messages and exact candidate contents

### Commit 1

`docs(knowledge-studio): establish KS-00 governance baseline`

Candidate contents after correction: all 32 category A files, `README.md`, and
`MVP/README.md`. Exclude `.gitignore`, `package.json`, `backend/__init__.py`, all sprint
files, source-library files, and prototype code.

### Commit 2

`docs(knowledge-studio): formalize KS-00 through KS-14 roadmap`

Candidate contents after numbering reconciliation: the 15 category B files. If KS-15 is
retained, change the message and add an explicitly approved KS-15 sprint contract rather
than silently folding it into KS-14.

### Commit 3

`chore(source-library): align local source-library scaffolding`

Candidate content after architecture approval:
`data/source-library/incoming/.gitkeep`. Other category D markers may be included only if
the authoritative structure is revised to retain them. Never include the manifest or
source/generated data.

## 13. Files excluded from every proposed commit

- All 22 category C prototype files.
- `data/source-library/incoming/source_manifest.json`.
- All ignored PDFs, immutable originals, registry/audit/lock files, and generated output.
- `.gitignore`, `package.json`, and `backend/__init__.py` until their provenance and
  intended tooling boundary are separately approved.

## 14. Human decisions required

1. Choose KS-00–KS-14 with combined final hardening/operations, or KS-00–KS-15 with
   separate KS-14 Security and KS-15 Operations.
2. Confirm whether KS-00 has received the human approvals required by its own contract.
3. Authorize correction of all stale KS-01 status and next-action statements.
4. Decide whether category C should remain local migration evidence, be archived, or be
   removed in a later dedicated change.
5. Decide whether lifecycle stages are directories or registry/artifact states.
6. Decide whether root lint/typecheck/test should cover only canonical KS-01 or also
   deprecated prototype code.
7. Decide whether a sanitized intake manifest may ever be tracked; current recommendation
   is no.

## 15. Validation commands

Inventory and evidence commands used:

```text
git status --short --branch --untracked-files=all
git diff --name-status
git diff --stat
git ls-files --others --exclude-standard
git log --oneline --decorate origin/main..main
rg "backend\.ingestion"
rg "ingestion\.(ocr|metadata|classifiers|chunking|embeddings|pipeline|reports|reviewers|schemas|utils)"
rg "from backend.ingestion"
rg "import backend.ingestion"
```

Final validation results:

| Command | Result |
|---|---|
| `npm run docs:validate` | PASS — Sprint 00 document validation passed |
| `npm run secrets:check` | PASS — secret scan passed |
| `git diff --check` | PASS — no whitespace errors |
| `git status --short --branch --untracked-files=all` | PASS — final inventory 83 files |
| `git diff --cached --name-only` | PASS — empty; nothing staged |

## 16. Git safety confirmation

- Nothing was staged.
- No commit was created.
- No push or fetch was attempted.
- No file was deleted, reset, cleaned, stashed, overwritten, or discarded.
- KS-02 was not started.

## 17. Exact recommended next command

Human review should begin by reading this untracked report:

```bash
sed -n '1,420p' docs/00_PROJECT_CONTROL/REMAINING_WORKTREE_AUDIT.md
```

## 18. Final disposition after human decisions

All seven decisions were resolved on 2026-07-31:

1. The active roadmap is exactly KS-00 through KS-14. KS-14 combines security hardening,
   operational readiness, backups/recovery, monitoring, deployment readiness, incident
   response, and production operations. There is no active KS-15.
2. KS-00 is `APPROVED_COMPLETE`.
3. KS-01 is `VERIFIED_COMPLETE / COMMITTED` at
   `2b9471124dbdb44b55bb3c28b96b36e3f23fdd32`: eight unique sources registered, zero
   exact duplicates, eight `REGISTERED / UNTRUSTED`, publication blocked 8/8.
4. The obsolete prototype was archived outside the repository, verified, and its 23
   untracked implementation files removed. It was not committed.
5. Registry and artifact state is canonical. Eight obsolete workflow-directory markers
   were removed; source binaries were not moved.
6. Root `package.json` and `.gitignore` prototype-only changes were restored to HEAD.
7. The superseded local source manifest was backed up separately outside the repository,
   verified, and removed from the intake directory. It was not included in the shareable
   prototype archive.

Source PDFs, immutable originals, canonical registry, audit log, lock, OCR/vector output,
and local backups remain outside Git. The committed KS-01 historical acceptance report
was not rewritten. KS-02 through KS-14 remain `PLANNED / NOT_STARTED`.
