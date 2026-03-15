---
prompt_name: Monthly Treasury Report
agent: Treasury
trigger: monthly_schedule
description: Instructions for compiling the monthly treasury report with spend breakdown, budget analysis, and projections for the next month.
---

# Monthly Treasury Report Instructions

## Overview

On the first day of each month (or end of previous month), Treasury Agent generates a comprehensive report of all spending from the previous month, including breakdown by category, budget analysis, and forward-looking projections.

**Report generated**: End of month or 1st of month (UTC)

**Location**: `reports/monthly/treasury-{YYYY}-{MM}.md`

Example: `reports/monthly/treasury-2026-03.md` (for March 2026)

## Step 1: Define Reporting Period

### 1.1 Identify Month

Current month for reporting: previous calendar month

Example (if today is April 1, 2026):
- Reporting month: March 2026
- Period: March 1 - March 31, 2026 (UTC)

### 1.2 Retrieve Disbursement Log

File: `logs/disbursement-log.md`

Extract all entries matching the reporting period.

**Example entries**:
```
[2026-03-01T08:30:00Z] disbursement-20260301T0830-001 | Twitter API | 500 MNT | approved | 0x7f3a...
[2026-03-05T14:00:00Z] disbursement-20260305T1400-001 | Design Contractor | 8000 MNT | approved | 0x9c2e...
[2026-03-10T16:15:00Z] disbursement-20260310T1615-001 | Operator Salary | 50000 MNT | approved | 0x2b8d...
...
[2026-03-31T23:45:00Z] disbursement-20260331T2345-001 | Mantle RPC | 300 MNT | approved | 0x5a1e...
```

### 1.3 Compile Complete Transaction List

Create internal list:
```
transactions_this_month = [
  {
    date: ISO 8601,
    disbursement_id: string,
    vendor: string,
    amount: integer,
    category: string,
    status: approved | rejected | escalated,
    tx_hash: string
  },
  ...
]
```

## Step 2: Aggregate Spending by Category

### 2.1 Categorize Transactions

Use category from rulebook (`botdao-governance/rulebook/treasury/`):

**Categories**:
- Tool Subscriptions (Twitter API, Discord API, RPC, etc.)
- Operator Compensation (salaries, bounties)
- Third-Party Services (design, development, analytics)
- Campaign Spend (advertising, promotional)
- Other

### 2.2 Calculate Totals by Category

```
spending_by_category = {
  "Tool Subscriptions": sum of all tool costs,
  "Operator Compensation": sum of salaries/bounties,
  "Third-Party Services": sum of service costs,
  "Campaign Spend": sum of advertising,
  "Other": remaining
}

total_spent = sum of all categories
```

**Example**:
```
Tool Subscriptions: 2,500 MNT
  - Twitter API: 500
  - Discord API: 400
  - Mantle RPC: 300
  - Other tools: 1,300

Operator Compensation: 120,000 MNT
  - Salaries: 100,000
  - Bounties: 20,000

Third-Party Services: 45,000 MNT
  - Design: 20,000
  - Development: 25,000

Campaign Spend: 15,000 MNT
  - Advertising: 15,000

Other: 3,500 MNT

Total Spent: 186,000 MNT
```

## Step 3: Calculate Budget Analysis

### 3.1 Compare to Budget

```
monthly_budget = 200,000 MNT  (from config)
total_spent = {calculated above}
remaining = monthly_budget - total_spent
percentage_used = (total_spent / monthly_budget) * 100
```

**Example**:
```
Budget: 200,000 MNT
Spent: 186,000 MNT
Remaining: 14,000 MNT
Percentage: 93%
```

### 3.2 Daily Average

```
days_in_month = number of days in the reporting month
daily_average = total_spent / days_in_month
```

**Example** (March has 31 days):
```
Daily average: 186,000 / 31 = 6,000 MNT/day
```

## Step 4: Compile Spending Breakdown

### 4.1 Create Summary Table

```markdown
## Spending Summary (March 2026)

| Category | Amount | % of Total | vs. Budget |
|----------|--------|-----------|-----------|
| Tool Subscriptions | 2,500 MNT | 1.3% | Planned |
| Operator Compensation | 120,000 MNT | 64.5% | Planned |
| Third-Party Services | 45,000 MNT | 24.2% | Planned |
| Campaign Spend | 15,000 MNT | 8.1% | Planned |
| Other | 3,500 MNT | 1.9% | Unplanned |
| **TOTAL** | **186,000 MNT** | **100%** | **93% of budget** |

## Budget Analysis

| Metric | Value | Status |
|--------|-------|--------|
| Monthly Budget | 200,000 MNT | — |
| Total Spent | 186,000 MNT | OK |
| Remaining | 14,000 MNT | LOW |
| Percentage Used | 93% | HIGH |
| Daily Average | 6,000 MNT | Normal |
```

### 4.2 Create Detailed Vendor Breakdown

```markdown
## Vendor Breakdown

| Vendor | Amount | Count | Avg Per | Category |
|--------|--------|-------|---------|----------|
| [Salary Fund] | 100,000 MNT | 1 | — | Operator Comp |
| [Bounties Paid] | 20,000 MNT | 4 | 5,000 | Operator Comp |
| [Design Firm] | 20,000 MNT | 2 | 10,000 | Services |
| [Dev Contractor] | 25,000 MNT | 3 | 8,333 | Services |
| [Advertising Partner] | 15,000 MNT | 1 | — | Campaign |
| Twitter API | 500 MNT | 1 | — | Tools |
| Discord API | 400 MNT | 1 | — | Tools |
| Mantle RPC | 300 MNT | 1 | — | Tools |
| [Other vendors] | 5,900 MNT | — | — | Mixed |
```

## Step 5: Analyze Spending Patterns

### 5.1 Trend Analysis

Compare to previous months (if data available):

```markdown
## Trend Analysis

### Comparison to Previous Months

| Category | Jan | Feb | Mar | Trend |
|----------|-----|-----|-----|-------|
| Tool Subscriptions | 2,000 | 2,300 | 2,500 | ↑ Slight increase |
| Operator Comp | 115,000 | 120,000 | 120,000 | → Stable |
| Services | 40,000 | 42,000 | 45,000 | ↑ Increasing |
| Campaign Spend | 10,000 | 12,000 | 15,000 | ↑ Increasing |
| Other | 3,000 | 5,000 | 3,500 | ↓ Decreasing |
| **TOTAL** | **170,000** | **181,300** | **186,000** | ↑ +3% MoM |

### Key Observations

- Tool spending increasing slightly (due to increased RPC load?)
- Operator compensation stable (good predictability)
- Services increasing (more contractors? or higher rates?)
- Campaign spend up (Q2 marketing push?)
- Overall trend: gradual increase month-over-month
```

### 5.2 Identify Anomalies

```markdown
## Anomalies

**Unusually High Vendor Costs**:
- Design Firm: 20,000 MNT in March vs. 15,000 avg in Feb
  - Reason: Large UI redesign project (expected)
  - Status: Within bounds, approved

**New Vendors**:
- None this month

**Spike in Category**:
- Campaign Spend: +3,000 MNT vs. Feb (15,000 vs 12,000)
  - Reason: Q2 marketing push (planned)
  - Status: Within budget

**Concerns**:
- Monthly budget utilization at 93% (little buffer)
- Trend shows +3% growth MoM
- If trend continues: June might exceed budget
```

## Step 6: Daily Spending Analysis

### 6.1 Identify High-Spending Days

```markdown
## Daily Spending Pattern

### Highest Spending Days

| Date | Amount | Vendors | Reason |
|------|--------|---------|--------|
| Mar 1 | 25,000 | Salary fund + 2 services | Month start (salary payout) |
| Mar 10 | 20,000 | Design firm | Major deliverable |
| Mar 15 | 18,000 | Bounties (4 payouts) | Mid-month contributor payouts |
| Mar 28 | 22,000 | Dev contractor + other | End-of-cycle payments |

### Daily Average

- Average daily spend: 6,000 MNT
- Highest day: 25,000 MNT (417% of average)
- Lowest day: 500 MNT (8% of average)
- Volatility: High (salary/payment cycles cause spikes)

**Pattern**: Spending spikes at month-start (salary) and mid/end-cycle (contractor payouts). Normal pattern; within constraints.
```

## Step 7: Budget Forecast & Projections

### 7.1 Project April Budget

Based on March spending:

```markdown
## Forward Projection (April 2026)

### Assumption: Spending continues at March rate

```
March spend: 186,000 MNT (93% of budget)
Projected April: 186,000 MNT (if no changes)
Remaining budget buffer: 14,000 MNT

If April = March: Projected use = 93% (would stay below budget)
If trend continues (+3% MoM): Projected April = 191,580 MNT
- 191,580 / 200,000 = 95.8% of budget (would be tight)
```

### 7.2 Scenario Analysis

```markdown
### Scenario 1: Spending Stable (No Growth)

- April spend: 186,000 MNT
- Budget remaining: 14,000 MNT
- Status: GREEN (safe)

### Scenario 2: +3% Growth (Trend Continues)

- April spend: 191,580 MNT
- Budget remaining: 8,420 MNT
- Status: YELLOW (getting tight)

### Scenario 3: Campaign Ramps Up

- Assume Campaign Spend: +10,000 MNT
- April spend: 196,000 MNT
- Budget remaining: 4,000 MNT
- Status: RED (little buffer, risky)

### Scenario 4: One-Time Spike

- Assume large contractor payment: +30,000 MNT
- April spend: 216,000 MNT
- Budget remaining: -16,000 MNT
- Status: EXCEEDS (would require Governance approval)
```

### 7.3 Recommendations

```markdown
## Budget Recommendations

**For April 2026**:

1. **Monitor Operator Compensation**: At 120,000/month, it's the largest category.
   - If any raises planned, budget impact is substantial
   - Recommend: Verify no unexpected headcount changes

2. **Plan Campaign Spend**: Currently 15,000/month and growing.
   - If Q2 marketing push continues, costs will rise
   - Recommend: Get approval for April budget if >15,000 expected

3. **Services Cost Control**: Increasing from 40,000 (Jan) to 45,000 (Mar).
   - Design/Dev costs are rising
   - Recommend: Evaluate if future projects can be scoped more efficiently

4. **Budget Buffer**: Only 14,000 MNT remaining (7% buffer).
   - If unexpected costs arise, would require Governance approval
   - Recommend: Plan conservatively or request budget increase for May

**Risk Assessment**:
- Green: Spending stable and predictable
- Yellow: Trend toward budget limits; monitor closely
- Red: One-time high costs could trigger escalations
```

## Step 8: Compile Report Sections

### 8.1 Report Frontmatter

```markdown
---
report_type: monthly_treasury
month: March
year: 2026
generated_at: 2026-03-31T18:00:00Z or 2026-04-01T08:00:00Z
total_disbursements: 32
total_approved: 31
total_escalated: 1
total_rejected: 0
---

# Monthly Treasury Report — March 2026

**Generated**: March 31, 2026 or April 1, 2026 (UTC)

---
```

### 8.2 Report Contents (in order)

1. **Frontmatter** — metadata
2. **Executive Summary** — 2-3 paragraph overview
3. **Spending Summary** — categories, totals, budget %
4. **Budget Analysis** — spent vs. budget, remaining, percentage
5. **Vendor Breakdown** — detailed spending per vendor
6. **Trend Analysis** — comparison to previous months, observations
7. **Daily Pattern Analysis** — high-spending days, average, volatility
8. **Anomalies** — unusual costs, new vendors, concerns
9. **Forecast & Projections** — April outlook, scenarios
10. **Recommendations** — actions for Governance/leadership
11. **Appendix** — full transaction log (if detailed)

## Step 9: Handle Month-End Accounting

### 9.1 Reset Daily Counter

At 00:00 UTC on 1st of month, daily spending counter resets.

**Action**:
- Call vault contract: `resetDailySpending()`
- Verify: spent_today = 0
- Log: `[timestamp] daily_spending_reset | new_month_start`

### 9.2 Archive Previous Month Log

Create archive of previous month's transactions:

File: `logs/disbursement-log-{YYYY}-{MM}.md`

Example: `logs/disbursement-log-2026-03.md`

Content: All transactions from March, plus summary:

```markdown
# Disbursement Log — March 2026

[All individual transaction lines from March]

## Monthly Summary

| Metric | Value |
|--------|-------|
| Total transactions | 32 |
| Total spent | 186,000 MNT |
| Approved | 31 |
| Escalated | 1 |
| Rejected | 0 |
| Budget used | 93% |
```

### 9.3 Replenish Budget

Vault contract automatically replenishes budget at month start.

**Action** (automatic):
- Vault resets: spent_this_month = 0
- Vault replenishes: monthlyBudget = 200,000 MNT
- Verify: new_budget_available = 200,000 MNT

## Step 10: Write Report File

### 10.1 File Location and Naming

Directory: `reports/monthly/`

Naming: `treasury-{YYYY}-{MM}.md`

Example: `reports/monthly/treasury-2026-03.md`

### 10.2 Generate Markdown

Write complete report using sections from Step 8.

### 10.3 Include Links

Reference related documents:
- `logs/disbursement-log-2026-03.md` (archived month log)
- `state/budget-status.md` (current budget)
- `botdao-governance/rulebook/treasury/` (spending rules)

## Step 11: Log Report Generation

Append to logs:

```
[{timestamp}] monthly_report_generated | {filename} | {month} {year} | spent: {amount} ({pct}% of budget)
```

Example:
```
[2026-04-01T08:00:00Z] monthly_report_generated | treasury-2026-03.md | March 2026 | spent: 186,000 (93% of budget)
```

## Step 12: Create GitHub Issue (Optional)

If using GitHub for communication:

```markdown
**Title**: Monthly Treasury Report: March 2026

**Body**:
Report generated and available at: `reports/monthly/treasury-2026-03.md`

Key findings:
- Total spent: 186,000 MNT (93% of budget)
- Operator compensation: 120,000 MNT (65% of spending)
- Budget buffer: 14,000 MNT (7% remaining)
- Trend: +3% spending growth month-over-month
- Risk: Budget tightening; monitor April spending carefully

Recommendations:
1. Verify no unexpected headcount changes
2. Plan for Q2 marketing spend
3. Consider budget increase for May if trend continues

Next steps: Governance Agent to review and approve April budget.
```

## Step 13: Update Heartbeat

```
treasury: {current ISO 8601 timestamp}
```

## Output

Monthly report produces:

- **One comprehensive markdown file**: `reports/monthly/treasury-{YYYY}-{MM}.md`
- **Archived disbursement log**: `logs/disbursement-log-{YYYY}-{MM}.md`
- **Updated budget status**: `state/budget-status.md` (with next month's figures)
- **Log entries**: 2-3 entries documenting report and month-end actions
- **Optional GitHub issue**: For team visibility

## Quality Checklist

Before finalizing report:

- [ ] ✓ All transactions from month included
- [ ] ✓ Categories accurate and complete
- [ ] ✓ Spending totals match log
- [ ] ✓ Budget percentages calculated correctly
- [ ] ✓ Vendor breakdown includes all vendors
- [ ] ✓ Trend analysis compares to previous months (if available)
- [ ] ✓ Anomalies identified and explained
- [ ] ✓ Forecast scenarios are realistic
- [ ] ✓ Recommendations are specific and actionable
- [ ] ✓ Report file uses correct naming
- [ ] ✓ All links and references valid
- [ ] ✓ Tone is professional and data-driven

## Integration

This report is reviewed by:
- **Governance Agent**: For budget oversight and planning
- **Leadership/Board**: For financial accountability and forecasting
- **Future Treasury Agents**: For historical context and benchmarking

Reports from all months form a historical treasury record for audit purposes.
