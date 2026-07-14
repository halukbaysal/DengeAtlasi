# Source Inventory

**Status:** ACTIVE
**Last reviewed:** 2026-07-13

This registry tracks candidate editions. A work's place in the approved product
hierarchy does not approve a particular edition for retrieval. Only an edition
whose `Review Status` is `APPROVED` and whose `Approved` value is `YES` may enter
staging or production retrieval.

## Allowed Values

- Category: `PRIMARY`, `SUPPLEMENTARY`, `CULTURAL`, `ACADEMIC_COMMENTARY`
- Review Status: `UNREVIEWED`, `OCR_REVIEWED`, `CONTENT_REVIEWED`, `APPROVED`, `REJECTED`
- Copyright Status: `PENDING`, `CLEARED`, `RESTRICTED`, `REJECTED`
- OCR Status: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `NOT_APPLICABLE`, `REJECTED`
- Approved: `YES`, `NO`

## Inventory

| Source ID | Title | Author | Edition | Publisher | Publication Year | Language | Category | Source Priority | Review Status | Copyright Status | OCR Status | Approved | Notes |
|---|---|---|---|---|---:|---|---|---:|---|---|---|---|---|
| `SRC-MAR-0001` | Marifetname | Erzurumlu İbrahim Hakkı | TBD — edition not selected | TBD | TBD | Ottoman Turkish / Turkish | PRIMARY | 1 | UNREVIEWED | PENDING | NOT_STARTED | NO | Candidate source family only. Edition, rights, completeness, and digitization quality require human review. |
| `SRC-IBS-0001` | Canon of Medicine / El-Kanun fi't-Tıb | Ibn Sina | TBD — edition not selected | TBD | TBD | Arabic / Turkish | SUPPLEMENTARY | 2 | UNREVIEWED | PENDING | NOT_STARTED | NO | Candidate source family only. Historical medical content requires the mandatory medical notice and may never become treatment advice. |

## Approved Source Hierarchy

The following hierarchy is approved for future routing, subject to edition-level
approval:

1. Primary: Marifetname
2. Secondary: Ibn Sina

Future sources, not implemented and not approved for retrieval:

- Abu Zayd al-Balkhi
- Miskawayh
- Ghazali
- Kutadgu Bilig

No other source is admitted by this Sprint 00 decision.

## Current Blockers

- `TBD-SRC-001`: Select and legally review a Marifetname edition.
- `TBD-SRC-002`: Select and legally review an Ibn Sina edition.
- `TBD-SRC-003`: Assess scan completeness and OCR quality for each selected edition.
- `TBD-SRC-004`: Record reviewer identities and approval dates after human review.
