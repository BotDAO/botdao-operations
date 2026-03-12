---
prompt_name: Campaign Score
agent: analytics
trigger: monitoring_window_closed
description: Score a published piece after its monitoring window ends
---

# Campaign Score

## When to Run
When a publish receipt in `handoffs/distribution-to-analytics/receipts/` has `status: pending` and its monitoring_window has elapsed.

## Steps

### 1. Collect Metrics
For the published post, gather:
- Impressions (views)
- Engagements (likes, replies, quotes, bookmarks)
- Retweets/shares
- Click-through rate (if link included)
- Sentiment (positive/negative/neutral from replies)
- On-chain attribution (if trackable, wallet connections or transactions after post)

### 2. Calculate Weighted Score
Use weights from `agents/analytics/config.md`:
- Impressions: weight from config (e.g., 15%)
- Engagement rate: weight from config (e.g., 25%)
- Sentiment: weight from config (e.g., 20%)
- Retweets: weight from config (e.g., 15%)
- CTR: weight from config (e.g., 15%)
- On-chain attribution: weight from config (e.g., 10%)

Normalize each metric against benchmarks in `data/engagement-history.md`. Score 0-100.

### 3. Anomaly Detection
Check if any metric deviates more than the anomaly threshold (from config, default 20%) from the rolling average:
- If positive anomaly: flag as outperformer, note what worked
- If negative anomaly: flag as underperformer, note possible causes

### 4. Write Score Handoffs
Write to TWO locations:

**To Scout** (`handoffs/analytics-to-scout/scores/`):
- Narrative performance: which narrative type scored well/poorly
- Helps Scout prioritize future scanning

**To Content** (`handoffs/analytics-to-content/scores/`):
- Format performance: which content format scored well/poorly
- Helps Content choose formats and angles

If anomaly detected, also write to:

**To Governance** (`handoffs/analytics-to-governance/reports/`):
- Anomaly report per SCHEMA.md
- Include deviation percentage and direction

### 5. Update Data
- Update `data/engagement-history.md` with this campaign's results
- Update `state/active-campaigns.md` to mark campaign as scored
- Mark the publish receipt as `status: completed`
- Update heartbeat in `state/agent-health.md`
