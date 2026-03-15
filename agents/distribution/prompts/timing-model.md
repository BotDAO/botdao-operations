---
prompt_name: Optimal Publish Timing Model Consultation
agent: Distribution
trigger: draft_received
description: Instructions for consulting the timing model data and determining optimal publish time for a draft based on narrative type, historical performance, and current constraints.
---

# Timing Model Consultation

## Overview

The timing model (`data/timing-model.md`) is a reference document that captures historical patterns in when different content types and narrative topics receive peak engagement. This prompt guides Distribution Agent to consult the model and use it to select optimal publish times.

## Important Note

**The timing model is built incrementally**: The first 5-10 campaigns will not have sufficient historical data. Early cycles will use default windows. As campaigns complete and Analytics scores arrive, the model will be populated with real performance data.

## Step 1: Access the Timing Model

File location: `data/timing-model.md`

### 1.1 Check Model Structure

The timing model is organized by narrative type. Expected sections:

```markdown
# Timing Model — Optimal Publishing Times

## DeFi Protocol Launches

**Historical Performance**:
- Average engagement peak: 14:00-16:00 UTC
- Secondary peak: 18:00-20:00 UTC
- Lowest engagement: 21:00-08:00 UTC
- Best day of week: Tuesday-Thursday

**Sample Size**: 5 campaigns
**Confidence Level**: Low (insufficient data)

---

## Partnership Announcements

**Historical Performance**:
- Average engagement peak: 13:00-15:00 UTC
- Secondary peak: 17:00-19:00 UTC
- Lowest engagement: 22:00-07:00 UTC
- Best day of week: Monday, Wednesday

**Sample Size**: 3 campaigns
**Confidence Level**: Very low (minimal data)

---

## Ecosystem Updates

**Historical Performance**:
- Average engagement peak: 14:00-17:00 UTC
- Secondary peak: 19:00-21:00 UTC
- Lowest engagement: 22:00-06:00 UTC
- Best day of week: All days (consistent)

**Sample Size**: 2 campaigns
**Confidence Level**: Very low (minimal data)

---
```

## Step 2: Identify Draft's Narrative Type

From the draft's brief reference, determine what narrative type this is:

**Common narrative types**:
- DeFi protocol launch
- Partnership announcement
- Governance update
- Staking/incentive announcement
- Ecosystem milestone (TVL, volume, user growth)
- Security incident response
- Technical upgrade
- Community call-to-action

### 2.1 Map Draft to Model Section

Open `data/timing-model.md` and find the section matching the draft's narrative type.

**Example**:
- Draft brief: Partnership with Agni Finance
- Narrative type: Partnership Announcements
- Model section: "## Partnership Announcements"

### 2.2 Read Historical Data

From the model section, extract:
- **Average engagement peak window** (UTC hours)
- **Secondary window** (fallback)
- **Worst times to publish** (avoid)
- **Best day of week**
- **Sample size** (how many campaigns this is based on)
- **Confidence level** (based on sample size)

## Step 3: Evaluate Confidence in Model Data

### 3.1 Assess Sample Size

| Sample Size | Confidence Level | How to Use |
|---|---|---|
| 0-2 campaigns | Very Low | Use as reference only; prioritize current constraints |
| 3-5 campaigns | Low | Consider alongside default windows; may deviate |
| 6-10 campaigns | Medium | Good guidance; follow unless overridden by constraints |
| 11+ campaigns | High | Strong signal; optimize for these windows when possible |
| 20+ campaigns | Very High | Trust this data; only deviate if constraints force it |

**Action**:
- Very Low/Low confidence: Use model as suggestion, but don't force timing if constraints conflict
- Medium+ confidence: Prioritize model times when feasible

### 3.2 Check "Best Day of Week"

The model may recommend specific days:
- Example: "Partnership announcements perform best Tuesday-Thursday"

**Action**:
- If today is a recommended day: prioritize publishing
- If today is not recommended: defer if engagement window allows, or publish anyway if expiration is soon

## Step 4: Apply Distribution Constraints

Overlay timing model recommendations against Distribution Agent's operational constraints:

### 4.1 Constraint 1: Publish Window (UTC)

From config: `publish_window_start` and `publish_window_end` (default: 13:00-22:00 UTC)

**Rule**: Can only publish between these hours.

**Action**:
1. Check if model's optimal window falls within publish window
2. If yes: aim for model's optimal window
3. If no: use the overlap between model window and publish window

**Example**:
```
Model optimal: 13:00-15:00 UTC
Publish window: 13:00-22:00 UTC
Action: Publish between 13:00-15:00 (overlap)
```

**Example 2**:
```
Model optimal: 12:00-14:00 UTC
Publish window: 13:00-22:00 UTC
Action: Publish at 13:00 (earliest in publish window, closest to model optimal)
```

### 4.2 Constraint 2: Minimum Time Between Posts (hours)

From config: `min_time_between_posts` (default: 2 hours)

**Rule**: Cannot publish within N hours of the last publish.

**Action**:
1. Check time since last publish from `logs/publish-log.md`
2. If enough time has passed: timing model applies
3. If not enough time: defer until interval is satisfied, then apply model

**Example**:
```
Last publish: 15:30 UTC
Current time: 16:00 UTC
min_time_between_posts: 2 hours
Status: Cannot publish until 17:30 UTC
Model optimal: 13:00-15:00 UTC (already passed)
Action: Publish at 17:30 (first allowed time) or defer to next optimal window
```

### 4.3 Constraint 3: Daily Post Cap

From config: `max_posts_per_day` (default: 6)

**Rule**: Cannot exceed N posts in 24 hours.

**Action**:
1. Count posts in last 24 hours from logs
2. If under cap: timing model applies
3. If at/over cap: must defer to tomorrow

**Example**:
```
Posts in last 24h: 6
max_posts_per_day: 6
Status: At cap, cannot publish today
Model optimal: 13:00-15:00 UTC today (not possible)
Action: Defer to tomorrow, aim for optimal window tomorrow
```

### 4.4 Constraint 4: Draft Expiration Window

From draft's frontmatter: `expires` (ISO 8601)

**Rule**: Must publish before draft expires or it's no longer timely.

**Action**:
1. Check hours until expiration
2. If >6 hours until expiration: timing model is primary (use it)
3. If <6 hours until expiration: publish ASAP (expiration takes priority over model)
4. If <0 (expired): do not publish, flag to Governance

**Example**:
```
Model optimal: 14:00-16:00 UTC
Draft expires: 16:30 UTC
Current time: 13:00 UTC
Status: Within expiration window, model applies
Action: Publish at 14:00-16:00 UTC
```

**Example 2**:
```
Model optimal: 14:00-16:00 UTC
Draft expires: 14:15 UTC
Current time: 13:00 UTC
Status: Expiration before model optimal window ends
Action: Publish immediately (13:00) to catch engagement before expiration
```

## Step 5: Calculate Optimal Publish Time

### 5.1 Decision Tree

```
Is model data available for this narrative type?
├─ NO → Use default window (13:00 UTC, middle of publish window)
├─ YES → Is model confidence Medium or higher?
    ├─ NO (Low/Very Low) → Use default, check model as reference
    └─ YES → Does model optimal window overlap publish window?
        ├─ NO → Use edge of publish window closest to model
        ├─ YES → Can we publish at model optimal without violating constraints?
            ├─ NO (interval/cap constraints) → Find earliest allowed time
            ├─ YES → Schedule for model optimal
```

### 5.2 Calculate Specific Time

Once optimal window is determined, select specific hour:

**If early in window**: Publish at window start (e.g., if optimal is 13:00-15:00, publish at 13:00)

**If late in window**: Check constraints; publish as soon as allowed, but before expiration

**If multiple drafts queued**: Use priority level to break tie
- Urgent > High > Normal

### 5.3 Handle Time Zone Differences

**Important**: All times in this system are UTC.

**Action**:
- Model times are UTC
- Config times are UTC
- Log times are UTC
- All calculations in UTC
- When communicating to humans, note "UTC" explicitly

## Step 6: Consult Model Examples

### Example 1: Partnership Announcement

```
Draft: Partnership with Agni Finance
Narrative type: Partnership Announcements
Model data:
  - Optimal: 13:00-15:00 UTC (High confidence, 8 campaigns)
  - Secondary: 17:00-19:00 UTC
  - Avoid: 22:00-07:00 UTC
  - Best day: Monday, Wednesday

Current status:
  - Time: Today 12:45 UTC (Wednesday)
  - Last publish: 3 hours ago ✓ (meets min interval)
  - Posts today: 2/6 ✓ (under cap)
  - Expires: 18:30 UTC ✓ (5h 45m window)
  - Priority: High

Decision: Publish at 13:00 UTC (optimal window, constraints satisfied)
```

### Example 2: Protocol Update (Low Confidence Model)

```
Draft: New RPC node announcement
Narrative type: Technical Updates
Model data:
  - Optimal: 14:00-16:00 UTC (Very Low confidence, 1 campaign)
  - Secondary: not available
  - Avoid: not enough data

Current status:
  - Time: Today 13:30 UTC
  - Last publish: 1.5 hours ago ✗ (min interval = 2h, need 0.5h more)
  - Posts today: 2/6 ✓
  - Expires: 19:30 UTC ✓
  - Priority: Normal

Decision: Defer until 15:30 UTC (min interval satisfied), close to model optimal
Note: Model confidence is low, so don't force timing; practical constraints are primary
```

### Example 3: Emergency Security Response

```
Draft: Security incident response
Narrative type: Security incident (no historical model yet)
Model data:
  - No prior campaigns of this type
  - No model available

Current status:
  - Time: Today 21:45 UTC (outside publish window 13:00-22:00)
  - Last publish: 30m ago
  - Posts today: 5/6
  - Expires: 22:45 UTC (1h window remaining)
  - Priority: Urgent

Decision: Cannot publish tonight (outside window, at cap)
Action: Escalate to Governance — security response needs immediate approval to override constraints
```

## Step 7: Log Timing Decision

After selecting optimal time, log the reasoning:

```
[{timestamp}] timing_decision | {draft_id} | scheduled {scheduled_time} UTC | reason: {reason}
```

Examples:
```
[2026-03-12T13:00:00Z] timing_decision | draft-20260312T1510-001 | scheduled 13:00 UTC | reason: model optimal for partnerships (confidence high, 8 samples)
[2026-03-12T13:30:00Z] timing_decision | draft-20260312T1520-001 | scheduled 15:30 UTC | reason: model optional, interval constraint (1.5h/2h satisfied at 15:30)
[2026-03-12T21:45:00Z] timing_decision | draft-20260312T1530-001 | escalate_governance | reason: urgent security, outside publish window + at daily cap
```

## Step 8: Update Timing Model (After Publishing)

**Note**: Distribution Agent does NOT write to timing model. Analytics Agent updates it after campaigns complete.

However, Distribution Agent can log publishing time for Analytics to reference:
- Log publish time to `logs/publish-log.md` (already done in publish flow)
- Analytics uses these timestamps to correlate with engagement peaks

## Timing Model Maintenance (For Governance/Analytics)

As campaigns complete, Analytics Agent will update `data/timing-model.md`:

1. **After 5 campaigns** of a narrative type: Model section gets initial confidence bump
2. **After 10 campaigns**: Model becomes "Medium" confidence
3. **After 20 campaigns**: Model becomes "High" confidence

Template for Analytics to add model sections:

```markdown
## [Narrative Type]

**Historical Performance** (from {N} published campaigns):
- Average engagement peak: {HH:00}-{HH:00} UTC
- Secondary peak: {HH:00}-{HH:00} UTC
- Lowest engagement: {HH:00}-{HH:00} UTC
- Best day of week: {Days}
- Best timezone window: {description if applicable}

**Sample Size**: {N} campaigns
**Confidence Level**: {Very Low / Low / Medium / High / Very High}

**Last Updated**: {ISO 8601 date}

**Notes**: [Any caveats or patterns observed]
```

## Default Timing (When Model Unavailable)

If no model data exists for a narrative type:

**Default window**: 14:00 UTC (middle of publish window 13:00-22:00)

**Rationale**: Mid-window provides buffer for constraint violations, matches US East Coast business hours (9 AM EST).

## Key Principles

1. **Model is guidance, not law**: Use it to optimize, but constraints take priority
2. **Confidence matters**: Low-confidence data is a suggestion; high-confidence data should be followed when feasible
3. **Constraints are hard limits**: Publish window, interval, and daily cap are non-negotiable (unless Governance overrides)
4. **Expiration is urgent**: If draft will expire before optimal time, publish earlier
5. **Sequential improvement**: The more campaigns we run, the better the timing model becomes

## Troubleshooting

| Situation | Action |
|-----------|--------|
| No model data for narrative type | Use default 14:00 UTC; publish when constraints allow |
| Model data very old (>30 days) | Note in log that data may be stale; use with caution |
| Multiple optimal windows available | Pick earliest (within expiration window) to meet engagement window sooner |
| Constraints prevent any publish today | Defer to tomorrow; note reason in heartbeat comment |
| Urgent draft expires too soon for optimal window | Override timing, publish ASAP (escalate if constraints violated) |

## Integration with Publish Flow

The timing model consultation is Step 3.4 of the publish-flow prompt. After following this timing-model prompt:

1. Return to publish-flow Step 4 (Publishing Decision)
2. Proceed with publish immediately OR queue for scheduled time
3. Continue through publish, attestation, and receipt generation

This prompt is standalone reference; always return to publish-flow for the complete publishing workflow.
