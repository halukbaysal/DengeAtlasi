# Risk Register

**Classification:** AUTHORITATIVE

| ID | Risk | Product | Likelihood | Impact | Mitigation | Owner | Status | Blocking |
|---|---|---|---|---|---|---|---|---|
| R-001 | Unlicensed edition enters corpus | KS/DA | High | Critical | independent legal gate and immutable provenance | Legal reviewer | OPEN | Yes |
| R-002 | OCR changes historical meaning | KS/DA | High | High | original/normalized separation and page review | OCR review role | OPEN | Yes |
| R-003 | Astrology used deterministically | KS/DA | Medium | Critical | admin-only default, safety labels, routing exclusions | Safety review role | OPEN | Yes |
| R-004 | Unsupported or mismatched citation | DA | Medium | Critical | claim-level validator and production evaluation | Evaluation owner | OPEN | Yes |
| R-005 | Vulnerable dependencies exploited | Both | High | Critical | targeted upgrades, scans, human risk decision | Security owner | OPEN | Yes |
| R-006 | Missing reviewers become implicit approval | KS | High | Critical | fail-closed states and RBAC-separated decisions | Product owner | OPEN | Yes |
| R-007 | Model performs poorly on historical Turkish | KS/DA | Medium | High | approved benchmark and rollback | AI platform owner | OPEN | Yes |
| R-008 | Collection cannot be restored | KS/DA | Medium | Critical | snapshot, isolated restore drill, manifest checks | Operations owner | OPEN | Yes |
| R-009 | Admin compromise publishes unsafe corpus | KS | Medium | Critical | MFA/RBAC, dual control, audit, signed manifests | Security owner | OPEN | Yes |
| R-010 | Journal/private text leaks | DA | Low | Critical | local-first, explicit send, allowlisted telemetry | Privacy owner | MONITORED | Yes |
| R-011 | Documentation diverges from code | Both | High | High | current-state audit and roadmap IDs in changes | Technical program owner | ACTIVE | No |
| R-012 | Research agent self-publishes | KS | Medium | Critical | discovery-only output and mandatory human pipeline | KS product owner | OPEN | Yes |

Roles are ownership placeholders; assignments are currently UNASSIGNED unless separately
recorded by authorized humans.
