# BotDAO Operations

Operational infrastructure for BotDAO's 6-agent system. This is where agents do their actual work — scanning narratives, drafting content, publishing, scoring performance, managing treasury, and governing the loop.

## How It Works

Agents communicate through **handoff files** — timestamped markdown documents dropped into channel directories. Each channel has a `SCHEMA.md` that defines the expected format. This file-first pattern means the system works identically whether agents run as Claude Agent Teams teammates or as independent Operators on separate machines.

## Operational Loop

```
Scout → Content → Distribution → Analytics → Treasury → Governance
  ↑                                                         |
  └─────────────────────────────────────────────────────────┘
```

Two cycles overlap at any time. Each cycle takes ~4-6 hours from narrative scan to published content with performance tracking.

## Repository Structure

```
CLAUDE.md               Master context loaded by all agents
agents/                 Per-agent operational files
  {agent}/
    SKILL.md            Full operational instructions
    config.md           Parameters (synced from governance repo)
    prompts/            Reusable prompt templates
handoffs/               Inter-agent communication channels
  {sender}-to-{receiver}/
    SCHEMA.md           Format specification
    briefs|drafts|...   Timestamped handoff files
state/                  Live system state
  current-cycle.md      Active cycle tracker
  agent-health.md       Heartbeat and status
  active-campaigns.md   Running campaign log
  budget-status.md      Current period spend
logs/                   Append-only event logs
  publish-log.md        Every published post
  disbursement-log.md   Every treasury payment
  governance-log.md     Every governance action
data/                   Persistent operational data
  engagement-history.md Campaign performance history
  timing-model.md       Optimal posting windows
  narrative-tracker.md  Tracked narratives and cooldowns
brand/                  Brand assets (synced from governance repo)
  voice-guidelines.md   Tone and style rules
  approved-topics.md    Topic guardrails
  templates/            Content format templates
```

## Agents

| Agent | Role | Upstream | Downstream |
|---|---|---|---|
| Scout | Monitors Mantle ecosystem for narratives | Analytics | Content |
| Content | Drafts threads, posts, and long-form | Scout | Distribution |
| Distribution | Publishes to X and Discord | Content | Analytics |
| Analytics | Scores performance, detects anomalies | Distribution | Scout, Content, Governance |
| Treasury | Manages MNT vault, processes payments | Governance | Governance |
| Governance | Reviews proposals, enforces rules | Analytics, Treasury | All agents |

## Handoff Flow

Every inter-agent message follows the same envelope format:

```markdown
---
id: {sender}-{timestamp}
from: {agent}
to: {agent}
type: {brief|draft|score|receipt|directive|...}
status: pending
created: {ISO 8601}
---

{Body content per SCHEMA.md}
```

Receiving agents process files with `status: pending`, update to `status: processing`, then `status: completed`.

## Config Sync

Agent configs in `agents/*/config.md` are copies from the governance repo's `rulebook/agents/`. When a governance proposal merges, updated configs are pulled into this repo. Agents always read from their local `config.md`.

**Canonical source:** [botdao-governance](https://github.com/BotDAO/botdao-governance)

## Quick Links

- [Master context (CLAUDE.md)](CLAUDE.md)
- [Agent skills](agents/)
- [Handoff schemas](handoffs/)
- [System state](state/)
- [Governance repo](https://github.com/BotDAO/botdao-governance)

---

*BotDAO: six agents, zero human employees, fully on-chain. Built on Mantle.*
