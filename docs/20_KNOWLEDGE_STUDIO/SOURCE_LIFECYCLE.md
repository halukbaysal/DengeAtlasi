# Canonical Source Lifecycle

**Classification:** AUTHORITATIVE

Each dimension changes independently and records actor role, time, reason, evidence, and
artifact fingerprint.

| Dimension/state | Entry | Permitted | Prohibited | Exit | Role | Reversible |
|---|---|---|---|---|---|---|
| Intake DISCOVERED | candidate found | record locator | OCR/publish | checksum intake | intake operator | Yes |
| REGISTERED | checksum/source ID fixed | metadata research | mutate original | provenance recorded | registrar | Yes |
| ORIGINAL_PRESERVED | immutable copy verified | downstream jobs | replace bytes | archive/reject | registrar | No mutation |
| OCR PENDING | eligible original | schedule sandbox job | claim reviewed text | extracted/failed | OCR operator | Yes |
| OCR EXTRACTED | outputs + confidence exist | compare/correct | approve silently | human-reviewed/rework | OCR reviewer | Yes |
| OCR HUMAN_REVIEWED | page evidence signed | subject review | rewrite original | revoke with audit | OCR reviewer | Yes |
| LEGAL PENDING | exact edition known | collect evidence | embed/publish | cleared/restricted/rejected | legal reviewer | Yes |
| LEGAL CLEARED | signed scoped decision | permitted processing | exceed license | expiry/review | legal reviewer | Yes |
| SUBJECT PENDING | readable scope | assess metadata/content | publish | approved/changes/rejected | subject reviewer | Yes |
| SAFETY PENDING | content available | label/restrict | route to users | approved/restricted/rejected | safety reviewer | Yes |
| CHUNK GENERATED | approved input version | QA/edit proposal | embed before review | reviewed/rejected | chunk reviewer | Yes |
| CHUNK HUMAN_REVIEWED | QA signed | embedding eligibility | mutate in place | new version/revoke | chunk reviewer | Yes |
| EMBEDDING ELIGIBLE | all gates + accepted ADR | generate candidate | publish directly | generated/failed | platform operator | Yes |
| EMBEDDING VERIFIED | count/hash/config pass | evaluate | change vectors | evaluation/rebuild | platform operator | Yes |
| EVALUATION PASSED | exact candidate tested | publication review | reuse for new hash | expire/fail | evaluation reviewer | Yes |
| PUBLICATION CANDIDATE | all evidence bundled | dual-control review | DA access | published/rejected | publication authority | Yes |
| PUBLISHED | signed atomic promotion | DA read | mutation | supersede/rollback | publication authority | Via version |
| REJECTED | human gate failed | preserve evidence/archive | downstream use | audited reopen/archive | responsible reviewer | Yes |
| ARCHIVED | retention decision | audit/restore per policy | active use | authorized restore | records owner | Yes |

`PUBLISHED`, `REJECTED`, and `ARCHIVED` are terminal for an artifact version. A new version
or explicit audited reopen is required; history is never overwritten.
