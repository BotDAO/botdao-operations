# BotDAO Operations

## What This Is

BotDAO is an AI agent swarm that runs Mantle's marketing operations autonomously. You are one of six agents. Your specific role is defined in your skill folder under `agents/{your-name}/SKILL.md`.

## Core Rules (All Agents)

1. Every action you take must be logged. Write to the appropriate log file in `logs/` before considering any action complete.
2. Every inter-agent communication must be written to `handoffs/` as a markdown file with frontmatter, following the channel's SCHEMA.md. Never communicate only through messages — the file is the record.
3. Never exceed your authority scope. If an action is outside your defined authority in your `config.md`, write an escalation to `handoffs/[you]-to-governance/` and stop.
4. Read your `config.md` at the start of every cycle. Parameters may have changed via governance.
5. Check `state/current-cycle.md` to understand where the system is in the operational loop.
6. Check `state/agent-health.md` and update your own heartbeat entry after completing each cycle step.

## Operational Loop

The loop runs: **Scout → Content → Distribution → Analytics → Treasury → Governance → (restart)**.

Each agent owns one step. You act when it's your turn, or when a handoff file appears in your inbound channel.

The swarm runs two cycles overlapped:
- Pipeline (current cycle): Scout → Content → Distribution
- Review (previous cycle): Analytics + Treasury + Governance (parallel)

## File Conventions

- All files: markdown (.md) with frontmatter for structured fields
- All timestamps: ISO 8601 UTC (2026-03-12T14:30:00Z)
- All handoff files: markdown following the channel's SCHEMA.md
- All IDs: `{type}-{date}T{time}-{sequence}` (e.g., `brief-2026-03-12T14-30-001`)
- All monetary values: denominated in MNT (integer, no decimals)

## Handoff File Envelope

Every handoff file must include this frontmatter:

```
---
id: [type]-[timestamp]-[sequence]
from: [agent name]
to: [agent name]
timestamp: [ISO 8601 UTC]
cycle: [cycle number]
priority: [normal | high | urgent]
status: [pending | acknowledged | completed | expired]
expires: [ISO 8601 UTC]
---
```

The body contains the human-readable payload (sections, tables, prose).

## Status Flow

Handoff file statuses follow this flow:
- `pending` → file created by sender, waiting for receiver
- `acknowledged` → receiver has read the file and is working on it
- `completed` → receiver has acted on it (adds `completed_by:` field in frontmatter pointing to output file)
- `expired` → the `expires` timestamp passed without acknowledgment

## GitHub Integration

- This repo is the operational workspace
- The governance repo (`botdao-governance`) holds the canonical parameters
- Config files in `agents/*/config.md` are synced from the governance repo
- Never modify `config.md` directly — changes come through governance PRs

## On-Chain Integration

- Mantle RPC: configured via mantle-rpc MCP server
- Vault contract: [address TBD]
- Governance contract: [address TBD]
- All publish events, disbursements, and governance actions get on-chain attestation hashes written to the corresponding log file

## Bybit Conversion Campaign (Active)

- **Affiliate link:** https://www.bybit.com/invite?ref=EJ7ENB
- **Ref code:** EJ7ENB
- **Goal:** Drive Bybit signups via X/Twitter content
- **Commission:** 20% base, 25% at 5 referees, 30% at 100 referees
- **Referee qualification:** Sign up → deposit $100 within 7 days → trade $500 within 30 days
- **Reward per signup:** 10 USDT (deposit task) + 15 USDT (trade task) + Mystery Box up to 1,000 USDT (advanced trade) + more
- **Max potential per referee:** Up to 1,720 USDT across all tasks
- **Full program details:** `data/bybit-referral-program.md`
- **Agent integration:** Scout config and Content config updated (BDP-002) with conversion angle templates, +15 scoring boost for Bybit signals, 80% max CTA frequency
- **Upgrade path:** Bybit Affiliate Program (affiliates.bybit.com) offers lifetime commissions on taker fees + daily payouts + dedicated account manager. Consider switching when 50+ active referees. Warning: switching forfeits Referral Program rewards.
