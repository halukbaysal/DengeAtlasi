# Source Review Template

Copy this template once per source edition. Do not overwrite prior reviews;
preserve them as an audit trail.

## Source Identity

- Source ID:
- Work title:
- Author or compiler:
- Edition:
- Publisher:
- Publication year:
- Language:
- Page range:
- Source category:
- Source priority:

## Review Record

- Current review status: `UNREVIEWED`
- Reviewer:
- Review date (YYYY-MM-DD):
- OCR confidence (0–100 or N/A):
- Copyright status: `PENDING`
- Evidence references:
- Content notes:
- Rejection reason, if applicable:

## Review Workflow

Use only these states:

1. `UNREVIEWED` — newly registered; prohibited from retrieval.
2. `OCR_REVIEWED` — OCR checked against the scan or trusted transcription.
3. `CONTENT_REVIEWED` — meaning, boundaries, attribution, pages, and metadata checked.
4. `APPROVED` — copyright is cleared and the edition is eligible for staging and production retrieval.
5. `REJECTED` — excluded with a documented reason.

Allowed forward transitions are:

```text
UNREVIEWED → OCR_REVIEWED → CONTENT_REVIEWED → APPROVED
       └──────────────→ REJECTED ←──────────────┘
```

Any material source change creates a new review record and returns the edition to
`UNREVIEWED`. Automation may assist review but cannot grant `APPROVED` status.

## OCR Review Checklist

- [ ] Compared with the scan or a trusted transcription
- [ ] Missing, duplicate, and reordered pages checked
- [ ] Headings, tables, poetry, and marginalia checked
- [ ] Page references preserved
- [ ] OCR confidence recorded

## Content Review Checklist

- [ ] Author, work, edition, publisher, and year verified
- [ ] Section boundaries and original meaning preserved
- [ ] Original and normalized text remain separate
- [ ] Historical claims are not presented as current scientific fact
- [ ] Health-adjacent material is labeled
- [ ] Unsafe derivative commentary is absent

## Approval Checklist

- [ ] Copyright decision is `CLEARED`
- [ ] OCR and content reviews are complete
- [ ] Required metadata is complete
- [ ] Source hash and page traceability can be established
- [ ] Mandatory medical notice applies to health-adjacent use
- [ ] Human approver and date are recorded

## Final Decision

- Final status: `UNREVIEWED | OCR_REVIEWED | CONTENT_REVIEWED | APPROVED | REJECTED`
- Approved for retrieval: `YES | NO`
- Decision rationale:
- Final reviewer:
- Final review date (YYYY-MM-DD):
