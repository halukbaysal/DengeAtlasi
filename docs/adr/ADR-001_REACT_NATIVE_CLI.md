# ADR-001 — React Native CLI

**Status:** Accepted

## Decision
Use React Native CLI with TypeScript. Do not use Expo.

## Reason
The project requires direct native control, predictable builds, and long-term access to platform capabilities.

## Consequences
Native iOS and Android setup must be maintained. Native packages require explicit review.
