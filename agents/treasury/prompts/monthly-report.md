---
prompt_name: Monthly Report
agent: treasury
trigger: end_of_month
description: Compile monthly treasury report with spend breakdown and projections
---

# Monthly Report

## When to Run
At the end of each calendar month.

## Steps

### 1. Gather Data
Read:
- `logs/disbursement-log.md` for all payments this month
- `state/budget-status.md` for current balances
- `rulebook/treasury/budget-caps.md` for allocated vs actual

### 2. Spend Breakdown
Calculate and report:
- Total spent this month
- Spend by category (agent operations, vendor payments, campaigns, operator compensation)
- Spend by agent (how much each agent's operations cost)
- Largest single disbursement
- Number of payments processed
- Number of escalations to Governance

### 3. Budget Analysis
- Allocated budget vs actual spend (percentage)
- Per-agent allocation vs actual (identify over/under spenders)
- Daily spending pattern (any spikes?)
- Comparison to previous month (if data available)

### 4. Projections
Based on current trends:
- Projected next month spend
- Will any caps need adjustment?
- Any budget risks (approaching limits)?

### 5. Output
Write full report to `logs/governance-log.md` as a monthly treasury entry. Also write summary to `handoffs/treasury-to-governance/escalations/` with type "monthly-report" so Governance reviews it.

Update `state/budget-status.md` to roll over to the new month.
