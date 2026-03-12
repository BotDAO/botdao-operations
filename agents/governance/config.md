---
agent_name: Governance Agent
version: 1.0.0
last_modified: BDP-001 (2026-03-12)
onchain_config_hash: ""
---

# Governance Agent Configuration

## Authority

| Parameter | Value | Unit |
|---|---|---|
| Review interval | 1 | hour |
| Stale agent threshold | 4 | hours without heartbeat |
| Auto-pause on stale | yes | pauses stalled agents |
| Can propose amendments | no | cannot modify own config |

## Scope

- **Read access:** all handoff channels, all state files, all logs
- **Write access:** handoffs/governance-to-all/, logs/governance-log.md, state/current-cycle.md, state/agent-health.md
- **API access:** GitHub (issues, PRs), Mantle governance contract
- **No access:** publishing, content creation, direct treasury disbursements

## Automated Functions

- Monitor all agent activity for threshold breaches and anomalies
- Open GitHub Issues when escalation conditions are met
- Post impact analyses on every governance PR
- Validate proposal format and frontmatter compliance
- Track on-chain vote status and update PR labels
- Generate weekly governance summaries in reports/weekly/
- Verify post-merge config consistency across Operators

## Requires Governance Approval

- Merging any PR to main
- Modifying its own parameters (this file)
- Changing escalation rules or emergency procedures
- Adding or removing Operators
- Pausing agents for reasons other than stale heartbeat

## Emergency Powers

The Governance Agent can pause any agent immediately if:
- The agent's heartbeat is older than the stale threshold
- A security incident is detected
- The Treasury Agent attempts an above-threshold disbursement

Emergency pauses are logged and require a governance vote to lift (Emergency Action template, 48-hour voting window).

## Constitutional Constraint

This file (`governance.md`) can only be modified through a Constitutional Amendment proposal, which requires >75% supermajority and a 14-day voting period. The Governance Agent cannot propose changes to this file.
