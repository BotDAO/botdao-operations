---
agent_name: Content Agent
version: 1.0.0
last_modified: BDP-001 (2026-03-12)
onchain_config_hash: ""
---

# Content Agent Configuration

## Authority

| Parameter | Value | Unit |
|---|---|---|
| Min confidence to send | 70 | score (0-100) |
| Max drafts per cycle | 3 | drafts |
| Max thread length | 10 | tweets |
| Revision limit | 2 | self-revisions before escalation |

## Scope

- **Read access:** handoffs/scout-to-content/, handoffs/analytics-to-content/, brand/
- **Write access:** handoffs/content-to-distribution/
- **No access:** publishing, treasury, scout data sources

## Content Types

| Type | Enabled | Notes |
|---|---|---|
| X thread | yes | Primary format |
| X single post | yes | For quick reactions |
| Discord announcement | yes | Cross-posted from X content |
| Long-form (Mirror) | no | Enable after Milestone 1 |
| Image/visual | no | Enable when visual pipeline exists |

## Quality Gate

Every draft is self-scored before handoff:
- Drafts scoring below the confidence threshold are flagged as `confidence: low` in frontmatter
- Low-confidence drafts are not sent to Distribution
- Two consecutive low-confidence drafts trigger an escalation to Governance Agent

## Brand Compliance

All content must comply with `brand/voice-guidelines.md` and `brand/approved-topics.md`. The Content Agent reads these files at the start of every cycle.
