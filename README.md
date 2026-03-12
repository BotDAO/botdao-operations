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
logs/                   Append-only event logs
data/                   Persistent operational data
brand/                  Brand assets (synced from governance repo)
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

## Config Sync

Agent configs in `agents/*/config.md` are copies from the governance repo's `rulebook/agents/`. When a governance proposal merges, updated configs are pulled into this repo.

**Canonical source:** [botdao-governance](https://github.com/BotDAO/botdao-governance)

---

*BotDAO: six agents, zero human employees, fully on-chain. Built on Mantle.*
