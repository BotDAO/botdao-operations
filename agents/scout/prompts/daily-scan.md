---
prompt_name: Daily Narrative Scan
agent: scout
trigger: cycle_start
description: Regular scanning cycle to find Mantle ecosystem narratives
---

# Daily Narrative Scan

## When to Run
Load this prompt at the start of every operational cycle when `state/current-cycle.md` shows it is your turn.

## Steps

### 1. Load Parameters
Read `agents/scout/config.md` and note:
- scan_interval (hours between scans)
- relevance_threshold (minimum score to flag)
- narrative_cooldown (hours before re-covering same topic)
- max_briefs_per_cycle (cap on briefs per cycle)

### 2. Check Narrative History
Read `data/narrative-tracker.md`. Note any narratives still in cooldown. Do not re-scan topics that were covered within the cooldown window.

### 3. Check Analytics Feedback
Read any pending files in `handoffs/analytics-to-scout/scores/` with `status: pending`. These contain performance scores from previous content. Use them to adjust which signal types to prioritize:
- High-scoring narratives: increase weight for similar signals
- Low-scoring narratives: decrease weight, consider cooling off that topic type

### 4. Scan Sources
Check each monitored source in order:
1. X/Twitter: search monitored accounts and hashtags for Mantle-related activity
2. DeFiLlama API: check Mantle TVL changes, protocol launches, volume spikes
3. Mantle explorer: new contract deployments, large transactions, governance activity
4. Discord: monitored channels for community sentiment and announcements
5. Telegram: monitored groups for ecosystem chatter

For each signal found, record:
- Source (platform and specific account/channel)
- Raw content or data point
- Timestamp
- Initial relevance estimate (0-100)

### 5. Score and Rank
For each signal, calculate a relevance score based on:
- Timeliness: how recent is this? (weight: 30%)
- Impact: how significant for Mantle ecosystem? (weight: 25%)
- Novelty: has this been covered before? (weight: 20%)
- Engagement potential: will the community care? (weight: 15%)
- Data availability: can we back this with numbers? (weight: 10%)

Filter out any signal below the relevance_threshold from config.

### 6. Deduplicate
Compare remaining signals against each other. If two signals cover the same underlying event, keep only the highest-scoring one.

### 7. Generate Briefs
For each signal that passes filtering (up to max_briefs_per_cycle), write a narrative brief using the `narrative-brief.md` prompt. Save each brief to `handoffs/scout-to-content/briefs/`.

### 8. Update State
- Update `data/narrative-tracker.md` with all narratives found this cycle
- Update `state/agent-health.md` with your heartbeat timestamp
- Mark any processed analytics feedback files as `status: completed`

## Error Handling
- If a source is unreachable, skip it and note the failure in your heartbeat
- If no signals pass the threshold, write a brief noting "no actionable narratives" so Content knows the cycle was not skipped
- If you exceed max_briefs_per_cycle, keep only the highest-scored briefs
