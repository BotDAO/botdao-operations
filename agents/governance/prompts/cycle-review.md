---
prompt_name: End-of-Cycle Review and State Update
agent: Governance
trigger: cycle_completion
description: Instructions for reviewing agent health at end of each operational cycle, verifying config compliance, and updating cycle state for the next cycle.
---

# End-of-Cycle Review Instructions

## Overview

At the end of each operational cycle (after all agents have taken their turns), Governance Agent performs a comprehensive review: checking agent health, verifying operational constraints, detecting anomalies, and updating state for the next cycle.

**Trigger**: When all agents (Scout → Content → Distribution → Analytics → Treasury → Governance) have completed their turns.

## Step 1: Gather Cycle Data

### 1.1 Read Current Cycle State

File: `state/current-cycle.md`

Extract:
```yaml
cycle_number: integer
cycle_started_at: ISO 8601
agent_turn: string (currently should be "governance")
expected_completion: ISO 8601
```

### 1.2 Read Agent Heartbeats

File: `state/agent-health.md`

Extract heartbeat timestamps for each agent:
```yaml
scout: ISO 8601 timestamp
content: ISO 8601 timestamp
distribution: ISO 8601 timestamp
analytics: ISO 8601 timestamp
treasury: ISO 8601 timestamp
governance: ISO 8601 timestamp
```

### 1.3 Check Pause Status

From same file, check if any agents are paused:
```yaml
paused:
  scout: false
  content: false
  distribution: false
  analytics: false
  treasury: false
```

## Step 2: Verify Agent Health

### 2.1 Check Heartbeat Freshness

For each agent, calculate time elapsed since last heartbeat:

```
time_since_heartbeat = now - agent_heartbeat_timestamp
stale_threshold = 4 hours  (from config)

if time_since_heartbeat > stale_threshold:
    HEARTBEAT_STALE = true
else:
    HEARTBEAT_STALE = false
```

**Create health status table**:

| Agent | Last Heartbeat | Time Since | Status | Paused? |
|-------|---|---|---|---|
| Scout | 2026-03-12T16:45:00Z | 2h 15m | Healthy | No |
| Content | 2026-03-12T16:40:00Z | 2h 20m | Healthy | No |
| Distribution | 2026-03-12T16:38:00Z | 2h 22m | Healthy | No |
| Analytics | 2026-03-12T16:35:00Z | 2h 25m | Healthy | No |
| Treasury | 2026-03-12T16:32:00Z | 2h 28m | Healthy | No |
| Governance | 2026-03-12T16:30:00Z | 2h 30m | Healthy | No |

### 2.2 Assess Agent Activity

For each agent, verify they completed expected work:

**Scout**:
- ✓ Generated briefs? (should be 1-3 per cycle)
- ✓ Updated narrative-tracker.md?
- Check: count new entries in `handoffs/scout-to-content/briefs/` since cycle start

**Content**:
- ✓ Processed briefs? (should match Scout briefs)
- ✓ Generated drafts? (count files in `handoffs/content-to-distribution/drafts/`)
- ✓ Updated brief status? (briefs should be marked "completed")

**Distribution**:
- ✓ Published drafts? (count receipts in `handoffs/distribution-to-analytics/receipts/`)
- ✓ Published within constraints? (check logs for timing violations)
- ✓ Generated receipts? (one per publish)

**Analytics**:
- ✓ Scored campaigns? (count files in `handoffs/analytics-to-scout/scores/`)
- ✓ Detected anomalies? (check `handoffs/analytics-to-governance/reports/`)
- ✓ Updated engagement history?

**Treasury**:
- ✓ Processed disbursements? (check logs)
- ✓ Maintained budget status?
- ✓ No constraint violations?

**Governance**:
- ✓ Reviewed escalations?
- ✓ Updated cycle state?

### 2.3 Create Agent Health Report

```markdown
## Agent Health Summary (Cycle 47)

| Agent | Heartbeat Age | Status | Output | Issues |
|-------|---|---|---|---|
| Scout | 2h 15m | Healthy | 2 briefs | None |
| Content | 2h 20m | Healthy | 2 drafts | None |
| Distribution | 2h 22m | Healthy | 2 publishes | None |
| Analytics | 2h 25m | Healthy | 2 scores | None |
| Treasury | 2h 28m | Healthy | 0 escalations | None |
| Governance | 2h 30m | Healthy (self) | — | None |

Overall: All agents healthy, no stale heartbeats, no paused agents.
```

## Step 3: Verify Operational Constraints

### 3.1 Check Distribution Timing Constraints

From `logs/publish-log.md`, verify all publishes respected constraints:

**Constraint 1: Publish Window (13:00-22:00 UTC)**
```
For each publish in logs:
    publish_hour = extract hour from timestamp
    if publish_hour < 13 OR publish_hour >= 22:
        VIOLATES_WINDOW = true
    else:
        VIOLATES_WINDOW = false
```

**Constraint 2: Min Time Between Posts (2 hours)**
```
For each sequential publish pair:
    time_diff = publish_timestamp_2 - publish_timestamp_1
    if time_diff < 2 hours:
        VIOLATES_INTERVAL = true
```

**Constraint 3: Daily Cap (6 posts per 24h)**
```
For each 24-hour window:
    posts_in_window = count posts in that 24h
    if posts_in_window > 6:
        VIOLATES_DAILY_CAP = true
```

**Create constraint check table**:

| Constraint | Expected | Actual | Status |
|---|---|---|---|
| Publish window (13:00-22:00 UTC) | All posts in window | 2 posts: 14:30, 16:15 | ✓ Pass |
| Min interval (2h) | All 2h+ apart | Closest pair: 2.5h | ✓ Pass |
| Daily cap (6 posts/24h) | ≤6 per day | Day 1: 1 post, Day 2: 1 post | ✓ Pass |

### 3.2 Check Treasury Constraints

From `logs/disbursement-log.md` and `state/budget-status.md`, verify spending constraints:

**Constraint 1: Daily Cap (15,000 MNT/day)**
```
Query vault contract: spent_today
if spent_today > 15,000:
    VIOLATES_DAILY = true
```

**Constraint 2: Monthly Budget (200,000 MNT/month)**
```
Query vault contract: spent_this_month
if spent_this_month > 200,000:
    VIOLATES_MONTHLY = true
```

**Create spending check table**:

| Constraint | Limit | Current | % Used | Status |
|---|---|---|---|---|
| Daily spend | 15,000 MNT | 6,200 MNT | 41% | ✓ OK |
| Monthly budget | 200,000 MNT | 186,000 MNT | 93% | ⚠ HIGH |

## Step 4: Review Escalations

### 4.1 Scan All Escalation Channels

Check for unresolved escalations:

```
channels = [
    "handoffs/scout-to-governance/",
    "handoffs/content-to-governance/",
    "handoffs/treasury-to-governance/escalations/",
    "handoffs/analytics-to-governance/reports/"
]

for each channel:
    list files with status: pending
    count = number of pending files
```

**Escalation summary**:

| Channel | Pending | High Priority | Action Required |
|---|---|---|---|
| Scout | 0 | — | None |
| Content | 0 | — | None |
| Treasury | 1 | Yes | Approve disbursement >50k |
| Analytics | 1 | Normal | Review anomaly report |

### 4.2 Process Escalations (per cycle-review-dependent prompt)

For each pending escalation, determine status:
- If <24h old: still awaiting response period
- If 24-48h old: escalate to human if urgent
- If >48h old: create GitHub issue for team

## Step 5: Check Configuration Compliance

### 5.1 Verify Agent Configs Match Current Governance Rules

For each agent, read their config file:
- `agents/scout/config.md`
- `agents/content/config.md`
- `agents/distribution/config.md`
- `agents/analytics/config.md`
- `agents/treasury/config.md`
- `agents/governance/config.md`

**Verify** parameters match rulebook:
- Thresholds (relevance, confidence, etc.)
- Limits (max briefs, max posts, budget, etc.)
- Time windows (publish window, scan interval, etc.)

**Create compliance table**:

| Agent | Parameter | Config Value | Rulebook Value | Match? |
|---|---|---|---|---|
| Scout | relevance_threshold | 60 | 60 | ✓ |
| Scout | narrative_cooldown | 24 | 24 | ✓ |
| Content | min_confidence_to_send | 70 | 70 | ✓ |
| Distribution | publish_window_start | 13:00 | 13:00 | ✓ |
| Distribution | publish_window_end | 22:00 | 22:00 | ✓ |
| Treasury | monthly_budget | 200,000 | 200,000 | ✓ |

**Status**: All configs match rulebook. Compliance: GREEN ✓

### 5.2 Check for Unauthorized Changes

Verify no config files were modified outside of governance process:

**Action**:
- Check git history of config files (if git-tracked)
- Verify all changes went through GitHub PR process
- If unauthorized change detected: **escalate as CRITICAL**

## Step 6: Compile Cycle Summary

### 6.1 Create Cycle Report

```markdown
## Cycle 47 Summary

**Period**: 2026-03-12T14:00:00Z to 2026-03-12T16:30:00Z (2.5 hours)

### Cycle Progression

1. **Scout Turn** ✓ Completed
   - Briefs generated: 2
   - Escalations: 0
   - Status: Healthy

2. **Content Turn** ✓ Completed
   - Drafts created: 2
   - Escalations: 0
   - Status: Healthy

3. **Distribution Turn** ✓ Completed
   - Publishes: 2
   - Constraint violations: 0
   - Status: Healthy

4. **Analytics Turn** ✓ Completed
   - Campaigns scored: 2
   - Anomalies detected: 1
   - Status: Healthy

5. **Treasury Turn** ✓ Completed
   - Disbursements processed: 3
   - Escalations: 1 (normal: above-threshold)
   - Status: Healthy

6. **Governance Turn** (current)
   - Review in progress...

### Key Metrics

| Metric | Value |
|--------|-------|
| Cycle duration | 2.5 hours |
| Briefed narratives | 2 |
| Published pieces | 2 |
| Engagement events | 2 campaigns monitored |
| Disbursements processed | 3 |
| Budget remaining | 14,000 MNT (7%) |

### Constraint Status

- Distribution timing: All green ✓
- Treasury spending: Yellow (93% of budget) ⚠
- Agent health: All green ✓
- Escalations: Normal (1 treasury approval) ✓

### Anomalies

- **Analytics**: Positive anomaly detected in brief-20260312T1400-001 (TVL correlation)
  - Status: Noted for future reference
  - Recommendation: Continue monitoring this pattern

### Overall Assessment

Cycle 47 completed successfully. All agents operational, no critical issues, one normal treasury escalation (above-threshold disbursement awaiting governance approval).

**Status**: GREEN ✓ — Ready for Cycle 48
```

## Step 7: Update Cycle State

### 7.1 Prepare Cycle 48 State

File: `state/current-cycle.md`

Update for next cycle:

```yaml
---
cycle_number: 48
cycle_started_at: 2026-03-12T16:35:00Z
agent_turn: scout  # Reset to Scout to begin new cycle
expected_completion: 2026-03-12T18:35:00Z  # 2 hours later
last_cycle_summary: completed_ok
---
```

### 7.2 Update Heartbeat

Update own heartbeat:

File: `state/agent-health.md`

```yaml
governance: 2026-03-12T16:35:00Z
```

### 7.3 Archive Cycle Data

Optionally create cycle summary file:

File: `logs/cycle-47-summary.md`

Document:
- Cycle number, dates
- Agent completions
- Output counts (briefs, drafts, publishes, scores)
- Escalations
- Constraint status
- Anomalies
- Health assessment

## Step 8: Log Cycle Completion

Append to governance log:

```
[{timestamp}] cycle_complete | cycle-{N} | {duration} | all_agents_ok | {N} escalations
[{timestamp}] cycle_progressed | cycle-{N} → cycle-{N+1} | agent_turn: scout
[{timestamp}] heartbeat_update | governance | success | governance: {timestamp}
```

Examples:
```
[2026-03-12T16:35:00Z] cycle_complete | cycle-47 | 2h 35m | all_agents_ok | 1 escalation (normal)
[2026-03-12T16:35:05Z] cycle_progressed | cycle-47 → cycle-48 | agent_turn: scout
[2026-03-12T16:35:10Z] heartbeat_update | governance | success | governance: 2026-03-12T16:35:10Z
```

## Step 9: Check for Issues to Create

### 9.1 Identify Issues Needing Escalation

If any constraint violation or critical issue:
- Create GitHub issue
- Assign to operations lead
- Add labels: cycle-review, {issue-type}

**Example issue** (if monthly budget exceeded):
```markdown
**Title**: Governance | Budget Alert | Monthly spend exceeded

**Body**:
Monthly budget exceeded in cycle 47. Current spend: 203,000 MNT (101.5% of budget).

Actions required:
1. Review Treasury escalations
2. Approve emergency fund transfer or
3. Pause non-essential spending

See: logs/governance-log.md
```

### 9.2 Create GitHub Issue for Anomalies

If analytics detected anomaly:
```markdown
**Title**: Analytics | Anomaly Report | [Narrative Type]

**Body**:
Analytics Agent detected [positive|negative] anomaly in campaign [brief-id].

Details:
- Metric: [metric name]
- Deviation: [+X% | -X%]
- Assessment: [finding]

See: handoffs/analytics-to-governance/reports/[filename]
```

## Step 10: Check if Weekly Report is Due

If today is Sunday (or report day per config):

**Action**:
- Instruct Analytics Agent to generate weekly report (if not already done)
- Link weekly report in governance log

## Step 11: Prepare Handoff for Next Cycle

### 11.1 Create Scout Briefing (if applicable)

If Scout should start immediately:
- Leave any context/notes in `state/current-cycle.md` comments
- Example: "High market volatility expected; monitor social sentiment closely"

### 11.2 Document Known Issues

If any known issues for next cycle:
```yaml
---
cycle_number: 48
known_issues:
  - Monthly budget at 93%; monitor April spending
  - One treasury escalation pending governance approval
  - Analytics anomaly pattern emerging; investigate further
---
```

## Output

Cycle review produces:

- **Updated cycle state**: `state/current-cycle.md` (incremented cycle number, reset agent_turn)
- **Updated heartbeat**: `state/agent-health.md` (governance timestamp)
- **Cycle summary** (optional): `logs/cycle-47-summary.md`
- **Log entries**: 3-4 entries documenting review and progression
- **GitHub issues** (if issues detected): 0-3 issues
- **Governance log updated**: Records all findings

## Quality Checklist

Before finalizing cycle review:

- [ ] ✓ All agent heartbeats checked (all <4h old)
- [ ] ✓ All agent outputs verified (briefs, drafts, publishes, scores)
- [ ] ✓ All constraints checked (distribution timing, treasury spending)
- [ ] ✓ All escalations counted and summarized
- [ ] ✓ All configs verified for compliance
- [ ] ✓ Cycle summary is complete and accurate
- [ ] ✓ Next cycle state is initialized
- [ ] ✓ Logs are updated
- [ ] ✓ GitHub issues created (if needed)
- [ ] ✓ Heartbeat is updated

## Integration

End-of-cycle review triggers next cycle:

1. Governance completes review
2. `state/current-cycle.md` is updated with cycle N+1
3. `agent_turn` is reset to "scout"
4. Scout Agent picks up its turn
5. New cycle begins

This continuous loop repeats indefinitely, with Governance Agent overseeing the entire swarm.

## Example Cycle Timeline

```
Cycle 47 Start: 2026-03-12T14:00:00Z
  ├─ Scout: 14:00-14:30 (generates 2 briefs)
  ├─ Content: 14:30-15:00 (drafts 2 pieces)
  ├─ Distribution: 15:00-15:30 (publishes 2)
  ├─ Analytics: 15:30-16:00 (scores 2 campaigns)
  ├─ Treasury: 16:00-16:30 (processes 3 disbursements)
  └─ Governance: 16:30-16:35 (reviews cycle, updates state)
Cycle 47 End: 2026-03-12T16:35:00Z

Cycle 48 Start: 2026-03-12T16:35:00Z (immediately)
  └─ [Repeat for next cycle]
```

This ensures continuous operation without gaps between cycles.
