---
prompt_name: Timing Model Consultation
agent: distribution
trigger: before_publish
description: Decide optimal publish time using historical data
---

# Timing Model Consultation

## When to Run
Before every publish action, consult this to decide if now is the right time.

## Steps

### 1. Read Current Model
Open `data/timing-model.md`. Note:
- Best performing time windows by day of week
- Confidence level of each window (low/medium/high)
- Any blackout periods

### 2. Check Constraints
From `agents/distribution/config.md`:
- publish_window: allowed hours (e.g., 13:00-22:00 UTC)
- min_spacing: minimum hours between posts
- max_posts_per_day: daily cap

From `logs/publish-log.md`:
- When was the last post published?
- How many posts today?

### 3. Decision Matrix
- If inside a high-confidence optimal window AND constraints pass: publish now
- If inside publish_window but not optimal: publish if draft is urgent priority
- If outside publish_window: hold until next window opens
- If spacing constraint not met: calculate when it clears and hold

### 4. Urgency Override
If the draft's source brief had `priority: high` or urgency "urgent":
- Override timing optimization
- Publish as soon as constraints allow (ignore optimal window, respect hard constraints only)

## Output
Return a decision: publish_now, hold_until (with timestamp), or hold_next_day.
