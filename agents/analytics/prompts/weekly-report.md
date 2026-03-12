---
prompt_name: Weekly Report
agent: analytics
trigger: end_of_week
description: Compile weekly performance summary across all campaigns
---

# Weekly Report

## When to Run
At the end of each 7-day period. Check `state/current-cycle.md` for cycle count to determine if a week has passed.

## Steps

### 1. Gather Data
Read all entries in `data/engagement-history.md` from the past 7 days. Also read:
- `logs/publish-log.md` for total posts published
- `state/budget-status.md` for spend this period
- `state/agent-health.md` for any downtime or errors

### 2. Compile Metrics
Calculate for the week:
- Total posts published (by platform)
- Average engagement score
- Best performing post (highest score) with link
- Worst performing post (lowest score) with link
- Narrative types covered (count by category)
- Anomalies detected (count and summaries)
- Week-over-week trend (improving, declining, stable)

### 3. Insights
Write 3-5 bullet points:
- What narrative type performed best this week?
- What content format drove the most engagement?
- What timing patterns emerged?
- Any concerning trends?
- Recommended adjustments for next week

### 4. Agent Health Summary
For each agent, note:
- Uptime percentage
- Number of handoffs processed
- Any errors or escalations

### 5. Output
Write the report to `logs/governance-log.md` as a weekly entry. Also write a summary to `handoffs/analytics-to-governance/reports/` so Governance has it for review.
