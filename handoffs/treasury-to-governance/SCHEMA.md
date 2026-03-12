# Schema: Treasury → Governance (Escalations)

## Channel

Treasury Agent writes escalations here when a disbursement exceeds its authority threshold or an anomaly is detected.

## File Location

`handoffs/treasury-to-governance/escalations/{timestamp}-escalation.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `tesc-{timestamp}-{sequence}` |
| from | string | `treasury` |
| to | string | `governance` |
| timestamp | ISO 8601 | When the escalation was created |
| cycle | integer | Current operational cycle number |
| priority | enum | `high` (threshold breach) or `urgent` (unknown vendor, budget exhaustion) |
| status | enum | `pending`, `acknowledged`, `resolved` |
| escalation_type | enum | `threshold-breach`, `unknown-vendor`, `budget-exhaustion`, `anomaly` |
| amount | integer | MNT amount involved |

## Required Body Sections

1. **Escalation Summary** — What triggered the escalation, in plain language
2. **Disbursement Details** — Table with recipient, amount, type, and which threshold was breached
3. **Current Budget State** — Snapshot from state/budget-status.md
4. **Recommended Action** — Treasury Agent's suggestion (approve, deny, defer to governance vote)
