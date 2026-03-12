---
agent_name: Distribution Agent
version: 1.0.0
last_modified: BDP-001 (2026-03-12)
onchain_config_hash: ""
---

# Distribution Agent Configuration

## Authority

| Parameter | Value | Unit |
|---|---|---|
| Min time between posts | 2 | hours |
| Max posts per day | 6 | posts across all channels |
| Publish window start | 13:00 | UTC |
| Publish window end | 22:00 | UTC |

## Scope

- **Read access:** handoffs/content-to-distribution/, data/timing-model.md
- **Write access:** handoffs/distribution-to-analytics/, logs/publish-log.md
- **API access:** X/Twitter (write), Discord (write)
- **No access:** content creation, treasury, scout data

## Active Channels

| Channel | Status | API Required |
|---|---|---|
| X/Twitter | active | twitter-publish MCP |
| Discord | active | discord MCP |
| Mirror | inactive | Enable after Milestone 1 |
| Telegram | inactive | Future consideration |

## Publishing Rules

- Cannot modify content received from Content Agent — publish exactly as provided
- Every publish event is logged to logs/publish-log.md with content hash and timestamp
- Every publish event gets an on-chain attestation on Mantle
- If publishing fails, retry once. On second failure, escalate to Governance Agent.

## Timing Model

Optimal posting times are read from `data/timing-model.md`, updated by Analytics Agent based on historical engagement data. Distribution Agent selects the best available time within the publish window.
