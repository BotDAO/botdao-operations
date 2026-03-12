---
prompt_name: Disbursement Check
agent: treasury
trigger: payment_request
description: Process a payment request by verifying budget, caps, and vendor approval
---

# Disbursement Check

## When to Run
When a payment or disbursement needs processing. This can be triggered by:
- Operator compensation schedule
- Campaign budget request
- Vendor invoice
- Governance directive

## Steps

### 1. Read Current Budget
Open `state/budget-status.md`. Note:
- Current period (month)
- Total budget for period
- Amount spent so far
- Remaining balance

### 2. Check Caps
From `agents/treasury/config.md`:
- auto_approve_limit: max amount that can be approved without governance vote
- daily_cap: maximum disbursement per day
- monthly_cap: maximum disbursement per month

From `rulebook/treasury/budget-caps.md` (via local copy):
- Per-agent monthly allocations
- Total monthly budget

Calculate:
- Would this payment exceed the daily cap?
- Would this payment exceed the monthly cap?
- Would this payment exceed the requesting agent's allocation?
- Is the amount within auto_approve_limit?

### 3. Verify Vendor
Check `rulebook/treasury/approved-vendors.md`:
- Is the recipient an approved vendor?
- If not, escalate to Governance

### 4. Decision

**Auto-approve if ALL true:**
- Amount <= auto_approve_limit
- Daily cap not exceeded
- Monthly cap not exceeded
- Agent allocation not exceeded
- Vendor is approved

**Escalate to Governance if ANY true:**
- Amount > auto_approve_limit
- Any cap would be exceeded
- Vendor not approved
- Unusual payment pattern detected

### 5. Execute or Escalate

**If approved:**
- Process payment via Mantle vault contract
- Record in `logs/disbursement-log.md`
- Update `state/budget-status.md`
- Update heartbeat

**If escalated:**
- Write escalation to `handoffs/treasury-to-governance/escalations/` per SCHEMA.md
- Include amount, reason for escalation, and recommendation
- Do NOT process payment until Governance responds
