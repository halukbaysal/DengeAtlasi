# Denge Atlası Product

**Classification:** AUTHORITATIVE

## Purpose and users

Denge Atlası is an adult self-reflection and historical-wisdom product. Users ask
source-grounded questions, inspect citations, explore non-deterministic temperament
themes, keep a device-local journal, and optionally use device-native text-to-speech.

## Supported journeys and modules

- Home → source question → grouped result → source detail
- Consent-based adult self-report → temperament themes → source evidence
- Local journal create/edit/delete/export; explicit journal-analysis request
- User-initiated on-device reading of visible text
- FastAPI health, search, grounded reflection analysis, and temperament contracts

## Prohibited capabilities

No facial/emotion inference, third-party or child analysis, deterministic personality,
fate/nafs/spiritual ranking, diagnosis, treatment, medication/herbal advice, hidden
journal upload, unsupported claims/citations, or independent modern personality framework.

## Architecture and ownership

React Native CLI/TypeScript owns presentation, local SQLite, device TTS, client
validation, and privacy-preserving telemetry. FastAPI/Pydantic owns routing, safety,
retrieval, citation validation, provider boundaries, and OpenAPI. DA owns user runtime
data; KS owns source and review data. DA receives only versioned publication artifacts.

## Production dependencies

Published corpus manifest, pinned compatible vector collection, accepted embedding
configuration, approved provider configuration, API deployment, secrets, monitoring,
signing, privacy disclosures, tested rollback, and resolved security gates.

## Privacy boundary

Journal text remains local unless an adult explicitly submits an analysis. Queries,
prompts, source passages, journal/health data, and provider output are prohibited from
analytics and routine logs. No account/cloud sync exists in the current MVP.

## Release blockers and criteria

Blockers are documented in project control and release gates. Release requires tested
mobile/backend artifacts, human red-team, security decision, privacy/store approval,
operational readiness, and an independently approved corpus version or an explicit
source-unavailable release mode.
