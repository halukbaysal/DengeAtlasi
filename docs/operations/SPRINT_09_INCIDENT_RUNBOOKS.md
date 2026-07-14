# Sprint 09 Incident Runbooks

For every incident: assign severity, preserve payload-free evidence, name an incident
commander, record UTC timestamps, communicate impact without user content, and create
a postmortem with owner and due date.

## Provider outage — SEV-2

Confirm provider health using correlation IDs and latency/error metrics; disable the
provider route, preserve deterministic redirects and source-only behavior, communicate
degradation, then restore behind a canary and rerun safety evaluation.

## ChromaDB corruption — SEV-2

Stop indexing and retrieval, retain the affected index read-only, verify source hashes,
rebuild from approved source records, run Recall@5 and citation gates, then switch the
index atomically. Never repair from unreviewed text.

## Source poisoning — SEV-2

Quarantine the source ID and derived chunks, disable affected responses, compare source
hashes and review history, rebuild the index without the source, rerun injection and
citation suites, and require reviewer approval before restoration.

## Sensitive log exposure — SEV-1

Restrict log access, stop the leaking path, preserve access metadata without copying
sensitive content, rotate any exposed credentials, determine affected users/retention,
follow legal notification requirements, purge according to approved policy, and add a
redaction regression test before reopening.

## Unsafe output report — SEV-1

Disable the affected prompt/provider path, retain only correlation ID and policy outcome,
reproduce in an isolated approved environment, add the case to the safety dataset, fix
deterministic controls, obtain required human review, and require 100% medical safety.

## Mobile release rollback — SEV-2

Halt rollout, identify the last verified build, use store rollback/phased-release controls,
communicate affected versions, verify API backward compatibility, and rerun core-loop,
offline journal, deletion, citation, TTS, and safety checks before resubmission.

## Postmortem template

- Severity, commander, UTC timeline, detection, impact, and duration
- Technical/root cause and contributing controls
- What worked/failed, payload-free evidence, corrective actions, owners, due dates
- Dataset/runbook/control updates and verification evidence
