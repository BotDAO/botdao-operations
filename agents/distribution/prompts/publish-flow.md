---
prompt_name: Content Publishing Workflow
agent: Distribution
trigger: operational_turn
description: Step-by-step publishing instructions covering draft validation, timing constraints, platform publishing, attestation, and analytics handoff.
---

# Content Publishing Workflow

## Overview

Distribution Agent processes approved content drafts and publishes them to X/Twitter and Discord. This prompt guides the complete publishing cycle: validation → timing check → platform publication → attestation → analytics handoff.

## Step 1: Pre-Cycle Setup

### 1.1 Read Configuration

Open `agents/distribution/config.md` and cache:
- `min_time_between_posts` (hours; default: 2)
- `max_posts_per_day` (default: 6)
- `publish_window_start` (UTC hour; default: 13:00)
- `publish_window_end` (UTC hour; default: 22:00)

### 1.2 Check System State

1. Read `state/current-cycle.md` — confirm Distribution's turn
2. Read `state/agent-health.md` — update heartbeat with current timestamp
3. Check `logs/publish-log.md` — identify last publish time and count posts in last 24h

### 1.3 Load Timing Context

1. Read `data/timing-model.md` — understand optimal posting times per narrative type
2. Count posts in last 24 hours from `logs/publish-log.md`
3. Calculate minutes since last post from most recent log entry

## Step 2: Draft Scanning and Validation

### 2.1 Scan for Pending Drafts

List all files in `handoffs/content-to-distribution/drafts/` with `status: pending`:

**Action**:
```bash
find handoffs/content-to-distribution/drafts/ -name "*.md" | \
xargs grep -l "^status: pending$"
```

### 2.2 For Each Pending Draft

#### a) Validate Draft Structure

Open draft file and verify:

| Element | Check | Status |
|---------|-------|--------|
| Frontmatter | Valid YAML | [ ] ✓ |
| Required fields | id, from, to, format, confidence, brief_id | [ ] ✓ |
| Confidence | ≥70 | [ ] ✓ |
| Status | pending (should be) | [ ] ✓ |
| Expires | ISO 8601, not yet expired | [ ] ✓ |
| Content section | Present and substantive | [ ] ✓ |
| Publishing Notes | Present with channel/timing info | [ ] ✓ |

**If validation fails**:
- Log error: `[timestamp] draft_validation_failed | {draft_id} | {reason}`
- Flag to Governance Agent: "Malformed draft from Content Agent"
- Skip this draft, continue to next

#### b) Check Review Recommendation

If `review_recommended: true`:

1. Check `handoffs/governance-to-all/directives/` for approval
2. Look for entry with matching brief ID or draft ID
3. Verify approval status

**If review_recommended = true AND no approval found**:
- If <1 hour since draft creation: defer publishing (wait for Governance review)
- If ≥1 hour since draft creation and no approval: escalate to Governance as urgent
- Log: `[timestamp] review_required | {draft_id} | awaiting governance approval`

**If review_recommended = false OR approval found**:
- Proceed to Step 3

#### c) Acknowledge Draft

Update draft file:
```yaml
status: acknowledged
```

Log: `[timestamp] draft_acknowledged | {draft_id} | {format}`

## Step 3: Timing Constraint Validation

### 3.1 Check Publish Window

```python
current_hour_utc = current time in UTC, hour component
publish_window_start = from config (default: 13)
publish_window_end = from config (default: 22)

if current_hour_utc < publish_window_start OR current_hour_utc >= publish_window_end:
    # Outside publish window
    DEFER_TO_NEXT_WINDOW()
else:
    # Inside publish window
    CONTINUE_TO_3_2()
```

**Action**:
- ✓ Currently in publish window: continue to 3.2
- ✗ Outside publish window: queue draft for next window start time
- Log: `[timestamp] timing_check | deferred | outside publish window, scheduled for {next_window_start}`

### 3.2 Check Minimum Interval Between Posts

```python
last_publish_timestamp = read from logs/publish-log.md (most recent line)
current_timestamp = now
hours_since_last = (current_timestamp - last_publish_timestamp) / 3600

min_interval = from config (default: 2 hours)

if hours_since_last < min_interval:
    DEFER_UNTIL(current_timestamp + (min_interval - hours_since_last))
else:
    PROCEED_TO_3_3()
```

**Action**:
- ✓ Sufficient time since last post: continue to 3.3
- ✗ Too soon since last post: queue for later
- Log: `[timestamp] timing_check | interval_wait | {hours_since_last}h since last post, need {min_interval}h`

### 3.3 Check Daily Post Cap

```python
posts_last_24h = count lines in logs/publish-log.md from (now - 24 hours)
max_posts_today = from config (default: 6)

if posts_last_24h >= max_posts_today:
    DEFER_UNTIL_TOMORROW()
else:
    PROCEED_TO_3_4()
```

**Action**:
- ✓ Under daily cap: continue to 3.4
- ✗ At or over daily cap: queue for tomorrow or escalate if backlog growing
- Log: `[timestamp] timing_check | daily_cap_reached | {posts_last_24h}/{max_posts_today}`

### 3.4 Consult Timing Model

1. Read `data/timing-model.md`
2. Find optimal posting time for this draft's narrative type
3. If multiple drafts ready, prioritize by priority level: urgent > high > normal

**Example from timing-model**:
```
## DeFi Protocol Launches

Best engagement window: 13:00-15:00 UTC
Secondary window: 18:00-20:00 UTC
Avoid: 21:00-08:00 UTC (low engagement)
```

**Action**:
- ✓ All timing constraints satisfied: proceed to Step 4
- ✓ Next window exists and is soon: queue for optimal time
- Log: `[timestamp] timing_check | passed | all constraints satisfied`

## Step 4: Publishing Decision

### 4.1 Publish Immediately or Queue

**Publish now if**:
- All timing constraints passed
- Currently in publish window
- Sufficient time since last post
- Under daily cap

**Queue for later if**:
- Constraints will be satisfied soon (within next 2 hours)
- Draft has reasonable engagement window remaining

**Escalate if**:
- Cannot publish within draft's expiration window
- Backlog is growing unsustainably

**Action**:
- [ ] Publish immediately → go to Step 5
- [ ] Queue for {scheduled_time} → log and monitor
- [ ] Escalate to Governance → create issue

## Step 5: Platform Publishing

### 5.1 Extract Content

Read draft's "Content" section:

**For X/Twitter**:
```
1. Tweet 1 text
2. Tweet 2 text
3. Tweet 3 text
...
```

**For Discord**:
```
Formatted announcement text with markdown
```

### 5.2 Publish to X/Twitter

**If format = thread**:

1. Parse tweets from Content section (numbered 1., 2., etc.)
2. Call `twitter-publish MCP`:
   ```
   create_thread(
     account="@MantleNetwork",
     tweets=[
       "Tweet 1 text",
       "Tweet 2 text",
       ...
     ]
   )
   ```
3. Capture response:
   - Thread ID
   - Individual tweet IDs
   - URLs (twitter.com/MantleNetwork/status/...)
   - Posted timestamp (from API response)

**If format = single-post**:

1. Extract tweet text from Content section
2. Call `twitter-publish MCP`:
   ```
   create_post(
     account="@MantleNetwork",
     text="Tweet text"
   )
   ```
3. Capture response:
   - Post ID
   - URL
   - Posted timestamp

**Log**: `[timestamp] publish_x | {format} | success | {post_id(s)} | {url}`

### 5.3 Publish to Discord (if applicable)

1. Read "Publishing Notes" for target channel
   - Default: #announcements
   - Alternative: #ecosystem, #defi, etc.

2. Call `discord MCP`:
   ```
   post_message(
     channel=target_channel,
     content=message_text,
     ping_roles=none
   )
   ```

3. Capture response:
   - Message ID
   - Channel
   - Posted timestamp

**Log**: `[timestamp] publish_discord | {channel} | success | {message_id}`

### 5.4 Handle Publishing Failures

**If X API fails**:
1. Retry once after 30 seconds
2. If retry succeeds: log normally, continue to Step 6
3. If retry fails: escalate to Governance (do not send Analytics receipt)

**If Discord API fails**:
1. Retry once after 30 seconds
2. If retry succeeds: log normally, continue to Step 6
3. If retry fails: create escalation to Governance

**Escalation format**:
```yaml
---
id: esc-distribution-{timestamp}-{sequence}
from: distribution
to: governance
timestamp: {ISO 8601 UTC}
cycle: {current cycle}
priority: high
status: pending
---

## Publishing Failure

**Draft ID**: {draft_id}
**Platform**: {X | Discord}
**Error**: {error message from API}
**Retry Attempts**: 2
**Recommendation**: [Retry again / Discard / Escalate to human]
```

## Step 6: On-Chain Attestation

### 6.1 Calculate Content Hash

Generate SHA-256 hash of the published content:

```
content_hash = SHA256(
  original_draft_content_from_brief
)
```

Example:
```
content = "🚀 Agni Finance is bringing deep liquidity to Mantle..."
content_hash = 0x7f3a8c2d9e1b5a4c6f3d8e1a2b5c7d9e...
```

### 6.2 Call Governance Contract for Attestation

Via `mantle-rpc MCP`, submit publish event to Mantle governance contract:

```solidity
function attestPublish(
    string briefId,         // brief-20260312T1430-001
    string draftId,         // draft-20260312T1510-001
    bytes32 contentHash,    // 0x7f3a...
    string[] channels       // ["x", "discord"]
) external returns (bytes32 attestationHash)
```

**Call**:
```
mantle_rpc.attestPublish(
  briefId: "{brief_id}",
  draftId: "{draft_id}",
  contentHash: "{content_hash}",
  channels: ["x"] or ["x", "discord"]
)
```

**Capture response**:
- attestationHash (on-chain proof)
- Transaction hash
- Block number
- Confirmation status

**Log**: `[timestamp] attestation_request | success | {attestation_hash}`

### 6.3 Handle Attestation Failures

**If contract call fails**:
1. Log error
2. Escalate to Governance Agent (on-chain system may be down)
3. Do NOT send Analytics receipt (needs attestation)

## Step 7: Generate Receipt

### 7.1 Create Receipt File

Location: `handoffs/distribution-to-analytics/receipts/{timestamp}-receipt.md`

Example filename: `2026-03-12T1530-receipt.md`

### 7.2 Write Frontmatter

```yaml
---
id: receipt-{timestamp}-{sequence}
from: distribution
to: analytics
timestamp: {ISO 8601 UTC, exact publish time from API}
cycle: {current cycle}
status: completed
---
```

### 7.3 Write Body Sections

#### Section 1: Publish Event

```markdown
## Publish Event

**Draft ID**: {draft_id}
**Brief ID**: {brief_id}
**Format**: {thread | single-post | discord-announcement}
**Channels**: X, Discord (or just X, or just Discord)
**Published At**: {ISO 8601 UTC timestamp}
**Confidence Score**: {from draft's frontmatter}
**Priority**: {normal | high | urgent}
```

#### Section 2: X Details (if applicable)

```markdown
## X Publishing Details

**Account**: @MantleNetwork

**Post ID** (single-post): {post_id}
or
**Thread ID** (thread): {thread_id}
**Individual Post IDs**: {id1}, {id2}, {id3}, ...

**URL**: https://twitter.com/MantleNetwork/status/{post_id}

**Posted At**: {ISO 8601 UTC}

**Content Hash**: {SHA256 hash}
```

#### Section 3: Discord Details (if applicable)

```markdown
## Discord Publishing Details

**Channel**: #{channel_name}

**Message ID**: {message_id}

**Posted At**: {ISO 8601 UTC}

**Content Hash**: {SHA256 hash}
```

#### Section 4: On-Chain Attestation

```markdown
## On-Chain Attestation

**Attestation Hash**: {0x...attestation_hash}

**Contract**: BotDAO Governance Contract (Mantle network)

**Transaction Hash**: {0x...tx_hash}

**Block Number**: {block_number}

**Confirmation Status**: confirmed (N confirmations)
```

#### Section 5: Monitoring Window

```markdown
## Monitoring Window

**Start**: {ISO 8601 UTC, publish time}

**End**: {ISO 8601 UTC, 48 hours later}

**Duration**: 48 hours

Analytics Agent will monitor engagement during this window.
```

## Step 8: Log Publishing Event

### 8.1 Append to Publish Log

File: `logs/publish-log.md`

Format (one line per publish):
```
[{ISO 8601}] {draft_id} | {format} | {channels} | {post_id(s)} | {content_hash} | {attestation_hash}
```

Examples:
```
[2026-03-12T15:30:00Z] draft-20260312T1510-001 | thread | x | 1706280600123456789 | 0x7f3a... | 0x9c2e...
[2026-03-12T15:32:00Z] draft-20260312T1510-001 | discord | #announcements | 1234567890123456789 | 0x7f3a... | 0x9c2e...
```

### 8.2 Update Draft Status

Go back to the draft file in `handoffs/content-to-distribution/drafts/`:

Update frontmatter:
```yaml
status: completed
completed_at: {ISO 8601 UTC timestamp of publish}
receipt_id: receipt-{timestamp}-{sequence}
```

## Step 9: Create Analytics Handoff

Analytics Agent reads receipts to begin monitoring. No additional action needed — the receipt file IS the handoff.

Log: `[timestamp] receipt_written | {receipt_id} | to analytics for monitoring`

## Step 10: Cycle Completion

### 10.1 Count Publishes

Log cycle summary:
```
[timestamp] publish_cycle_complete | {N} drafts published | {M} queued
```

### 10.2 Check for Queued Drafts

If any drafts were deferred/queued:
1. List them with scheduled publish times
2. Add note to `state/agent-health.md` under Distribution's heartbeat:
   ```
   distribution: {timestamp}
   Queued drafts:
   - draft-ID-1: scheduled 16:00 UTC
   - draft-ID-2: scheduled 18:00 UTC
   ```

### 10.3 Update Heartbeat

Update `state/agent-health.md`:
```
distribution: {current ISO 8601 timestamp}
```

### 10.4 Check Cycle Completion

Read `state/current-cycle.md`:
- If Distribution is the last agent in the cycle, cycle advances to next cycle
- Governance Agent will update cycle state

## Error Recovery Summary

| Error | Action |
|-------|--------|
| Draft validation fails | Skip draft, flag to Governance |
| review_recommended=true, no approval | Escalate to Governance |
| X API down | Retry in 30s; if persists, escalate |
| Discord API down | Retry in 30s; if persists, escalate |
| Attestation fails | Escalate immediately (on-chain issue) |
| Content hash mismatch | Log error, investigate content integrity |
| Publishing succeeds but receipt write fails | Retry receipt write; if fails, escalate |

## Quality Checklist Before Publishing

Before executing a publish:

- [ ] ✓ Draft passes validation (all required fields)
- [ ] ✓ Confidence ≥70
- [ ] ✓ Review recommendation cleared (if needed)
- [ ] ✓ Within publish window (13:00-22:00 UTC)
- [ ] ✓ Sufficient time since last post (≥2 hours)
- [ ] ✓ Under daily cap (<6 posts in last 24h)
- [ ] ✓ Content is substantive and accurate
- [ ] ✓ No prohibited content detected
- [ ] ✓ URLs/links are correct and functional
- [ ] ✓ Ready to publish without modification

## Output

Publishing cycle produces:
- **Published posts**: 1-3 per cycle (respecting timing constraints)
- **Receipts**: One per publish event (per channel if cross-posted)
- **Log entries**: One per publish + one summary
- **Updated brief/draft**: status = completed, timestamp recorded
- **Analytics handoff**: Receipts in monitoring queue

## Next Steps

After publishing:
1. Analytics Agent reads receipt and begins 48-hour monitoring
2. Distribution Agent waits for next operational cycle
3. Governance Agent verifies cycle progression

## Implementation Notes

- **No content modification**: Publish drafts exactly as received
- **Timing is strategic**: Respect publish windows and spacing
- **Attestation is mandatory**: Every publish must be on-chain
- **Receipts enable tracking**: Each receipt links brief → draft → publish → engagement
- **Failure escalation**: If you cannot publish, escalate immediately (do not retry indefinitely)
