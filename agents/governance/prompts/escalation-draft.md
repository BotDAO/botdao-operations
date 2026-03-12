---
prompt_name: Escalation Draft
agent: governance
trigger: escalation_received
description: Draft a response to an escalation from Analytics or Treasury
---

# Escalation Draft

## When to Run
When processing an escalation during cycle-review, or when an urgent escalation arrives mid-cycle.

## Steps

### 1. Read the Escalation
Open the escalation file. Identify:
- Source agent (Analytics or Treasury)
- Escalation type (anomaly, budget, violation)
- Severity (from priority field)
- What action is being requested

### 2. Assess Impact
- Which agents are affected?
- Is this time-sensitive?
- Does this require a config change (governance proposal) or just a one-time decision?

### 3. Decision Framework

**For budget escalations (from Treasury):**
- Is the amount reasonable given current budget status?
- Does it align with BotDAO objectives?
- Is the vendor approved?
- Decision: approve, reject, or request more info

**For anomaly reports (from Analytics):**
- Is the anomaly positive (outperformance) or negative (underperformance)?
- Positive: note for future strategy, no action needed
- Negative: investigate cause. Options:
  - Adjust agent config (issue directive)
  - Pause the relevant agent
  - Flag for governance proposal if systemic

**For violation reports:**
- How severe is the violation?
- Was it a one-time error or pattern?
- Decision: warning directive, config tightening, or agent pause

### 4. Write Response
- Log the decision in `logs/governance-log.md`
- If action needed: write directive to `handoffs/governance-to-all/directives/`
- If budget approved: notify Treasury to proceed
- Mark the original escalation as `status: completed`

### 5. Follow-up
If the escalation requires a governance proposal:
- Draft a proposal using the appropriate template from the governance repo
- Note this in the governance log for the operator to review
