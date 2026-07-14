# Architecture Decision Log

## Completed Decisions

| Date | Decision | Status | Rationale / Authority |
|---|---|---|---|
| 2026-07-13 | React Native CLI with TypeScript; no Expo | ACCEPTED | Native control and ADR-001 |
| 2026-07-13 | FastAPI, Pydantic, and Pytest backend | ACCEPTED | Typed API contracts and ADR-002 |
| 2026-07-13 | ChromaDB is the future MVP vector store | ACCEPTED, NOT IMPLEMENTED | Low MVP operational complexity and ADR-003 |
| 2026-07-13 | SQLite is local durable storage | ACCEPTED | Offline local-first storage and ADR-004 |
| 2026-07-13 | FastAPI OpenAPI is the API contract source | ACCEPTED | Prevent contract drift and ADR-005 |
| 2026-07-13 | No authentication or cloud sync in MVP | ACCEPTED | Privacy and delivery scope; ADR-006 |
| 2026-07-13 | Camera, facial analysis, emotion detection, and biometric processing are prohibited | ACCEPTED | Privacy, safety, and ADR-007 |
| 2026-07-13 | Marifetname is primary; Ibn Sina is supplementary | ACCEPTED | Product identity and ADR-008 |
| 2026-07-13 | Health-adjacent responses require a deterministic medical notice | ACCEPTED | Medical safety and ADR-009 |
| 2026-07-13 | Only edition-level `APPROVED` sources may enter production retrieval | ACCEPTED | Source governance blueprints 33 and 41 |

## Pending Decisions

| Date | Decision / Blocker | Status | Rationale / Next Evidence |
|---|---|---|---|
| 2026-07-13 | Exact Marifetname edition, publisher, rights, and digitization | TBD | Human source and copyright review required |
| 2026-07-13 | Exact Ibn Sina edition, publisher, rights, and digitization | TBD | Human source and copyright review required |
| 2026-07-13 | Embedding model and provider | PROPOSED | ADR-010 benchmark and licensing evidence required |
| 2026-07-13 | Post-beta business model and pricing | TBD | Retention, trust, safety, and unit economics must be measured |
| 2026-07-13 | Store category and final privacy disclosures | TBD | Required before public release, not Sprint 00 implementation |

## Source Hierarchy Decision

The currently approved product hierarchy is:

1. Primary: Marifetname
2. Secondary: Ibn Sina

Future, not implemented: Abu Zayd al-Balkhi, Miskawayh, Ghazali, and Kutadgu Bilig.
This is a routing hierarchy, not edition approval. No edition is currently approved
for retrieval.
