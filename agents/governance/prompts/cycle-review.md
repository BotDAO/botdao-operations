---
prompt_name: Cycle Review
agent: governance
trigger: cycle_end
description: End-of-cycle review of agent health, escalations, and config compliance
---

# Cycle Review

## When to Run
At the end of every operational cycle, after all other agents have completed their turns.

## Steps

### 1. Check Agent Health
Read `state/agent-health.md`. For each agent:
- Is the last heartbeat within the expected interval?
- Are there any error flags?
- Did the agent complete its assigned tasks this cycle?

Flag any agent that:
- Missed its heartbeat by more than the stale_threshold (from config)
- Reported errors
- Did not produce expected output

### 2. Process Escalations
Check all pending items in:
- `handoffs/analytics-to-governance/reports/` (anomaly reports)
- `handoffs/treasury-to-governance/escalations/` (budget escalations)

For each escalation, use `escalation-draft.md` prompt to draft a response.

### 3. Check Config Compliance
For each agent, compare their behavior this cycle against their config:
- Did Scout stay within max_briefs_per_cycle?
- Did Content respect confidence thresholds?
- Did Distribution respect publish windows and spacing?
- Did Analytics complete monitoring within the window?
- Did Treasury respect auto-approve limits?

Note any deviations.

### 4. Review Governance Directives
Check `handoffs/governance-to-all/directives/` for any pending directives that need follow-up.

### 5. Update Cycle State
- Update `state/current-cycle.md` to increment the cycle number
- Log the cycle review in `logs/governance-log.md`
- Update heartbeat in `state/agent-health.md`

### 6. Issue Directives (if needed)
If any agent needs correction:
- Write a directive to `handoffs/governance-to-all/directives/` per SCHEMA.md
- Types: pause, resume, config-update, notice
- Only use "halt-all" for critical system-wide issues
