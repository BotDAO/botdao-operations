---
prompt_name: X Thread Draft
agent: content
trigger: brief_received
description: Draft an X thread from a Scout brief following brand guidelines
---

# X Thread Draft

## When to Run
When a new brief appears in `handoffs/scout-to-content/briefs/` with `status: pending`.

## Before Writing
1. Read the brief fully
2. Read `brand/voice-guidelines.md` for tone and style rules
3. Read `brand/approved-topics.md` to confirm the topic is allowed
4. Read `brand/templates/x-thread.md` for thread structure
5. Read `data/engagement-history.md` for what thread formats perform well

## Writing Process

### Step 1: Choose Angle
Pick the best angle from the brief's suggestions. Consider:
- Which angle has the strongest data?
- Which matches recent high-performing content?
- Which is most timely?

### Step 2: Draft Thread
Follow the thread template structure:
- Tweet 1 (Hook): Bold claim or surprising data point. Must grab attention.
- Tweets 2-7 (Body): Build the argument with data, context, and insight. One idea per tweet.
- Final Tweet (CTA): Call to action. Drive to Mantle, invite discussion, or link to source.

Rules from brand guidelines:
- Data-driven, not hype. Every claim needs a number or source.
- No rocket emojis, no "to the moon" language
- Professional but accessible. Write for smart people, not insiders.
- Max 10 tweets per thread (check config for exact limit)

### Step 3: Self-Score Confidence
Rate your draft on 6 dimensions (0-100 each):
- Brand compliance: does it match voice guidelines?
- Factual accuracy: are all claims supported?
- Engagement potential: will people interact?
- Clarity: is it easy to follow?
- Originality: does it add something new?
- Completeness: does it cover the narrative fully?

Average score = confidence score.

### Step 4: Decision
- If confidence >= min_confidence_to_send (from config, default 70): proceed to handoff
- If confidence < threshold: revise and re-score (up to revision_limit from config)
- If still below after max revisions: flag `review_recommended: true` in handoff

## Output
Write draft to `handoffs/content-to-distribution/drafts/` following the schema in `handoffs/content-to-distribution/SCHEMA.md`.

Mark the original brief as `status: completed`.
