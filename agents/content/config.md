---
agent_name: Content Agent
version: 1.0.0
last_modified: BDP-002 (2026-03-15) — Bybit conversion campaign
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

## Bybit Conversion Campaign

| Parameter | Value | Notes |
|---|---|---|
| Affiliate link | https://www.bybit.com/invite?ref=EJ7ENB | Include in CTA tweets when brief has conversion angle |
| CTA placement | Final tweet of thread | Never in tweet 1 (hook) — always at the end |
| CTA style | Soft sell | Provide value first, CTA feels like a natural next step |
| Max CTA frequency | 80% of threads | Not every post needs a Bybit CTA — 1 in 5 should be pure ecosystem content |
| Disclosure | Include "link" or context | Don't hide that it's a referral — trust > clicks |

### Conversion Angle Templates
When Scout brief includes a `bybit_conversion_angle`, Content must weave it into the thread:
- `ecosystem-gateway`: Frame Bybit as the starting point to access Mantle DeFi
- `trading-opportunity`: Frame the signal as actionable alpha tradeable on Bybit
- `promo-amplify`: Lead with the value of the promotion, CTA to claim it
- `none`: Skip Bybit CTA entirely — publish as pure ecosystem content
