---
agent_name: Scout Agent
version: 1.0.0
last_modified: BDP-001 (2026-03-12)
onchain_config_hash: ""
---

# Scout Agent Configuration

## Authority

| Parameter | Value | Unit |
|---|---|---|
| Scan interval | 2 | hours |
| Relevance threshold | 60 | score (0-100) |
| Narrative cooldown | 24 | hours before re-covering |
| Max briefs per cycle | 3 | briefs |

## Scope

- **Read access:** X/Twitter, Discord, Telegram, DeFiLlama API, Mantle explorer
- **Write access:** handoffs/scout-to-content/, state/narrative-tracker.md
- **No access:** publishing, treasury, other agents' files

## Monitored Accounts

- @0xMantle
- @MantleDevs
- @MantleTreasury
- @Bybit_Official (Mantle parent)

## Monitored Keywords

- mantle, $MNT, mantle network, mantle L2
- mantle TVL, mantle DeFi, mantle ecosystem
- agni finance, merchant moe, lendle, aurelius
- mantle staking, mETH, cmETH

## Monitored Channels

- Discord: mantle-general, mantle-defi, mantle-dev
- Telegram: MantleNetwork, MantleDevs

## Escalation Rules

- Crisis signals (security incidents, negative sentiment spikes) go directly to handoffs/scout-to-governance/ with priority: urgent
- Crisis signals are never passed to Content Agent
