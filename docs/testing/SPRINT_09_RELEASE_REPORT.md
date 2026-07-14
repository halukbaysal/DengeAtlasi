# Sprint 09 Evaluation and Release Report

## Automated gates

| Gate | Threshold | Result |
| --- | --- | --- |
| Retrieval Recall@5 | >= 85% | PASS — 100% (2 synthetic cases) |
| Citation correctness | >= 95% | NOT MEASURED — invented-ID regression passes, but no scored dataset exists |
| Citation completeness | >= 95% | NOT MEASURED — schema enforcement passes, but no scored dataset exists |
| Unsupported claim rate | <= 3% | NOT MEASURED — fail-closed regression passes, but no scored dataset exists |
| Out-of-scope refusal accuracy | >= 95% | PASS — 100% (facial, fate, nafs) |
| Medical safety compliance | 100% | PASS — 100% (diagnosis, medication, herbal dosage) |
| Known prompt-injection handling | 100% | PASS — 100% (direct and Unicode cases) |

## Security scans

- `npm audit --audit-level=high`: PASS; no high/critical finding. Nine existing
  moderate transitive findings require breaking dependency changes and remain triaged.
- `python -m pip check`: PASS; no broken requirements. `pip-audit` is not installed,
  so a Python vulnerability-database scan remains required before release.
- API container build: PASS (`denge-atlasi-api:sprint09`).
- Docker Scout full scan: FAIL/BLOCKER — image digest `999187dc5ec4` contains 48
  findings across 14 packages: 2 critical, 5 high, 9 medium, 28 low, and 4
  unspecified. Critical findings affect Debian Perl
  (`CVE-2026-12087`) and `chromadb 1.5.9` (`CVE-2026-45829`); Scout reports no fixed
  version for either. Three high findings affect `starlette 0.47.3`, and two affect
  Debian Perl. The image must not be released until fixed upstream versions/base
  images are available and compatibility-tested, or an approved security review
  documents a non-affected determination.
- Docker Scout recommendations: the current `python:3.12-slim` base is up to date.
  Python 3.13/3.14 slim reduce five lower-severity base findings but retain one
  critical and two high base findings. The zero-base-finding Alpine recommendation
  also changes Python to 3.14 and libc, so it requires explicit ChromaDB/native-wheel
  compatibility testing and is not an automatic security patch. Upgrading/removing
  runtime `pip` can address its four medium and one low findings in a hardened image.
- Hardened rebuild `9c95e1f10e64`: FastAPI `0.128.8`, Starlette `0.49.3`, pip
  `26.0.1`, and current Debian package upgrades passed all 55 backend and 29 mobile
  tests. The high/critical scan improved from 2 critical + 5 high to 2 critical +
  4 high. One Starlette high and the fixed xz package finding were removed. The
  remaining Starlette fixes cited by Scout (`1.1.0`/`1.3.1`) are not published on
  PyPI; the current published latest is `0.49.3`.

## Release decision

Blocked by two critical and four high container findings, the pending Python vulnerability
scan, and the human red-team checklist. Human review is also required for safety logic and
response templates under the accepted evaluation blueprint.

Sprint 09 Status: PARTIAL
Production Release Status: BLOCKED
Sprint 10 Readiness: NO

## Explicit limitations

- The rate limiter is in-memory and process-local.
- Deterministic safety data cannot prove handling of unseen paraphrases.
- No fixed release is currently reported for the ChromaDB or Debian Perl critical CVE.
