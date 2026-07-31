# Denge Atlası Release Gates

**Classification:** AUTHORITATIVE

| Gate | Required evidence |
|---|---|
| Build | reproducible iOS/Android/API builds and locked dependencies |
| Contract | OpenAPI/client generation and compatibility tests |
| Quality | lint, typecheck, automated tests, device/accessibility/performance checks |
| Safety | policy regressions and completed human red-team |
| Security | scans, threat review, secrets, resolved or human-accepted blockers |
| Privacy | local-data behavior, telemetry inspection, retention and store disclosures |
| Corpus compatibility | signed publication manifest, collection/config compatibility |
| Operations | deployment, health, alerts, incident response, backup and rollback |
| Distribution | authorized signing, beta/store configuration and human approval |

A mobile binary can be ready while a new corpus is blocked. Corpus approval never grants
app-store approval. Release authority belongs to assigned humans, not an agent.
