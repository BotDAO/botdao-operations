---
agent_name: Scout Agent
version: 1.0.0
last_modified: BDP-002 (2026-03-15) — Bybit conversion campaign
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
- @Bybit_Official (Mantle parent — PRIMARY conversion target)
- @Bybit_Web3
- @BybitAnnouncements

## Monitored Keywords

### Mantle Ecosystem
- mantle, $MNT, mantle network, mantle L2
- mantle TVL, mantle DeFi, mantle ecosystem
- agni finance, merchant moe, lendle, aurelius
- mantle staking, mETH, cmETH

### Bybit Conversion Signals
- bybit, bybit web3, bybit wallet
- bybit promo, bybit bonus, bybit campaign, bybit rewards
- bybit listing, bybit launchpad, bybit earn
- bybit MNT, MNT trading, MNT/USDT
- bybit deposit bonus, bybit fee discount
- bybit mantle, mantle on bybit

## Monitored Channels

- Discord: mantle-general, mantle-defi, mantle-dev
- Telegram: MantleNetwork, MantleDevs

## Bybit Campaign Configuration

- **Affiliate link**: https://www.bybit.com/invite?ref=EJ7ENB
- **Conversion goal**: Bybit signups via affiliate referral
- **Signal priority boost**: +15 score for signals with natural Bybit conversion angle
- **Content angles** (blend all):
  - Mantle ecosystem gateway (Bybit as the on-ramp to Mantle DeFi)
  - Trading opportunities (Scout finds alpha, Content frames as Bybit trade)
  - Bybit promotions (promos, bonuses, campaigns — amplify with Mantle context)

## Escalation Rules

- Crisis signals (security incidents, negative sentiment spikes) go directly to handoffs/scout-to-governance/ with priority: urgent
- Crisis signals are never passed to Content Agent
