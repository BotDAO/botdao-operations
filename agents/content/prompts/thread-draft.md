---
prompt_name: X Thread Draft Generation
agent: Content
trigger: brief_processed
description: Instructions for drafting a multi-tweet thread from a Scout brief. Includes brand compliance, self-scoring, and handoff to Distribution.
---

# X Thread Draft Writing Instructions

## Overview

When Scout provides a brief recommending thread format, this prompt guides the Content Agent to write a compelling, on-brand multi-tweet thread. The output is a draft file ready for Distribution Agent to publish.

## Prerequisites

- Brief has been read and analyzed by Content Agent
- Brief's `status` has been updated to `acknowledged`
- Brief recommends thread format
- Brand guidelines have been read (tone, approved topics)
- Thread length does not exceed `max_thread_length` from config

## Step 1: Set Up Draft Metadata

Generate unique draft ID:
```
draft-{YYYYMMDD}T{HHMM}-{sequence}
```

Example: `draft-20260312T1510-001`

Set current timestamp (ISO 8601 UTC).

## Step 2: Create Draft File

**Location**: `handoffs/content-to-distribution/drafts/{YYYY}-{MM}-{DD}T{HH}{MM}-{sequence}-thread-draft.md`

**Example filename**: `2026-03-12T1510-001-thread-draft.md`

## Step 3: Write Frontmatter

```yaml
---
id: draft-{YYYYMMDD}T{HHMM}-{sequence}
from: content
to: distribution
timestamp: {ISO 8601 UTC, current time}
cycle: {current cycle number}
priority: {normal | high | urgent}
status: pending
expires: {ISO 8601 UTC, 6 hours from now}
brief_id: {Scout brief's ID}
format: thread
confidence: {0-100, your self-score}
review_recommended: {true if "approved with caution" topic, false otherwise}
---
```

## Step 4: Analyze Brief for Thread Structure

Read the Scout brief and extract:

1. **Core message**: What is the single headline idea? (1 sentence)
   - Example: "Agni Finance partners with Mantle to bring top-tier DeFi to our network"

2. **Key supporting points**: List 3-5 facts/angles that reinforce the core message
   - Agni's credibility (TVL, market position)
   - Benefits to Mantle users
   - Timeline or next steps
   - Call-to-action

3. **Tone cues**: From brief's "Recommended Tone"
   - Celebratory? Thought-leadership? Informational?

4. **Engagement window**: From brief's "Optimal Engagement Window"
   - When should this be published?

## Step 5: Plan Thread Structure

Determine thread length (2-10 tweets, respecting `max_thread_length`):

**Length guidance**:
- **2-3 tweets** ("short thread"): Simple announcement, quick reactions
- **4-6 tweets** ("medium thread"): Partnership, ecosystem update, announcement with context
- **7-10 tweets** ("long thread"): Deep analysis, educational content, thought-leadership

### Check Bybit Conversion Angle

Before planning structure, check the Scout brief's `bybit_conversion_angle` field:
- If `ecosystem-gateway`, `trading-opportunity`, or `promo-amplify` → use the matching Bybit CTA template below for the final tweet
- If `none` → use a generic ecosystem CTA (no affiliate link)
- Rule: **never lead with the CTA** — provide value first, Bybit link is always the natural next step

### Structure Template A: Ecosystem Gateway

Use when brief's conversion angle is `ecosystem-gateway` — Mantle ecosystem news where Bybit is the on-ramp.

1. **Tweet 1 (Hook)**: "[Emoji] [Ecosystem development]. Here's what this means for Mantle 🧵"
2. **Tweet 2-3 (Context)**: What happened, why it matters, credibility signals
3. **Tweet 4 (User Impact)**: Concrete benefits for Mantle users
4. **Tweet 5 (How to Participate)**: Steps to get involved
5. **Tweet 6 (Bybit CTA)**: "Want in? Grab $MNT on Bybit to get started → [affiliate link]"

### Structure Template B: Trading Opportunity

Use when brief's conversion angle is `trading-opportunity` — market signals, TVL moves, catalysts.

1. **Tweet 1 (Hook)**: "📊 [Data point] just happened on Mantle. Here's what the numbers are saying 🧵"
2. **Tweet 2 (Data)**: TVL, volume, on-chain metrics with sources
3. **Tweet 3 (Context)**: Why this matters — what's driving the move
4. **Tweet 4 (What's Next)**: What to watch for, potential outcomes
5. **Tweet 5 (Bybit CTA)**: "$MNT is moving. Trade it on Bybit → [affiliate link]"

### Structure Template C: Promo Amplify

Use when brief's conversion angle is `promo-amplify` — Bybit promotions, bonuses, campaigns.

1. **Tweet 1 (Hook)**: "🎁 Bybit just dropped [promo type] for Mantle users. Here's how to claim it 🧵"
2. **Tweet 2 (Details)**: What's the promo, how much, duration
3. **Tweet 3 (Why Now)**: Why this is worth it — tie to Mantle momentum
4. **Tweet 4 (How-To)**: Simple steps to claim
5. **Tweet 5 (Bybit CTA)**: "Sign up and claim your bonus → [affiliate link]"

### Structure Template D: Pure Ecosystem (No Bybit CTA)

Use when brief's conversion angle is `none` — or when hitting the 80% CTA frequency cap.

1. **Tweet 1 (Hook)**: "[Emoji] Big news for Mantle: [announcement]. Here's what this means for the ecosystem 🧵"
2. **Tweet 2-3 (Context)**: What happened, credibility, significance
3. **Tweet 4 (User Benefits)**: Concrete impact for users
4. **Tweet 5 (Timeline)**: What's next, when to expect it
5. **Tweet 6 (Generic CTA)**: "Follow us for more Mantle alpha" (no affiliate link)

## Step 6: Write the Thread

### Tweet-by-Tweet Writing

For each tweet in the thread:

1. **Keep under 280 characters** (Twitter limit)
2. **One idea per tweet** (don't overcomplicate)
3. **Use line breaks** for readability (tweets support multi-line)
4. **Add hashtags strategically** (2-3 per thread, placed naturally)
5. **Add mentions** only if relevant and accurate (e.g., @AgniFinance for partnership)
6. **Check tone** against brand guidelines
   - Is it professional? Celebratory? Thought-provoking?
   - Does it match Mantle's voice?

### Brand Compliance During Writing

**Tone check** (read voice-guidelines.md):
- ✓ Not condescending or overly technical
- ✓ Conversational but professional
- ✓ Confident but not arrogant
- ✓ Celebrates wins without dismissing competitors

**Topic check** (read approved-topics.md):
- ✓ Topic is in approved list
- ✓ If "approved with caution": you will flag this later (don't skip)
- ✓ Not prohibited (no financial advice, no disparagement)

**Claim verification**:
- ✓ "Tier-1 DeFi protocol" — confirmed in brief's supporting data?
- ✓ "50M+ TVL" — is this number accurate per DeFiLlama?
- ✓ "Partnership includes X" — is this from official announcement?

### Example Thread A: Ecosystem Gateway (with Bybit CTA)

```
1/ 🚀 Agni Finance is bringing deep liquidity to Mantle. Here's why this partnership is a huge win for both protocols 🧵

2/ Agni is one of the top DeFi aggregators in the industry. They manage 50M+ in TVL across multiple chains and serve thousands of traders daily.

3/ They chose Mantle because of our superior efficiency and EVM compatibility. This validates that top-tier protocols prefer Mantle's infrastructure.

4/ For Mantle users: You'll get access to Agni's best-in-class routing algorithms + massive liquidity pools. Better swaps. Lower slippage. Period.

5/ Launching with incentives to bootstrap liquidity. Expect significantly deeper markets on Mantle starting [date].

6/ Want to LP on Agni when it goes live? You'll need $MNT. Grab it on Bybit → [affiliate link]

#Mantle #DeFi #L2
```

### Example Thread B: Trading Opportunity (with Bybit CTA)

```
1/ 📊 Mantle TVL just crossed $500M — up 12% this week. Here's what's driving it 🧵

2/ Three protocols added $60M in combined TVL over the past 7 days:
• Agni Finance: +$25M
• Merchant Moe: +$20M
• Lendle: +$15M

3/ Why the surge? Mantle's gas costs are a fraction of mainnet, and yield opportunities are outpacing other L2s right now.

4/ When TVL moves this fast, it usually means smart money is positioning. Worth watching how this plays out over the next few weeks.

5/ $MNT is moving with the ecosystem. Trade it on Bybit → [affiliate link]

#Mantle #MNT #L2
```

### Example Thread C: Promo Amplify (with Bybit CTA)

```
1/ 🎁 Bybit just launched a deposit bonus campaign for $MNT. Here's how to claim yours 🧵

2/ New users who sign up and deposit $100+ get a $20 bonus in $MNT. Campaign runs until [date].

3/ Timing is solid — Mantle ecosystem is heating up with 3 new protocol launches this month and TVL trending up 15% week-over-week.

4/ How to claim:
→ Sign up on Bybit
→ Deposit $100+
→ Bonus hits your account within 24h

5/ Sign up and grab your bonus → [affiliate link]

#Mantle #Bybit #MNT
```

## Step 7: Score the Draft

**Self-scoring rubric** (6 dimensions, weighted):

### Dimension 1: Brand Alignment (25% weight)

Score 0-100:
- **90-100**: Perfectly matches voice guidelines, tone is spot-on, messaging aligns with organizational pillars
- **70-89**: Matches guidelines well, minor tone adjustments could improve
- **50-69**: Generally on-brand but has tone inconsistencies or awkward phrasing
- **0-49**: Off-brand, wrong tone, or contradicts guidelines

**Example**: If brief says "celebratory" but your thread is dry and informational, score lower.

### Dimension 2: Clarity (20% weight)

Score 0-100:
- **90-100**: Crystal clear to someone unfamiliar with the signal; no jargon; narrative flows logically
- **70-89**: Clear, but may require 1-2 reads; mostly jargon-free
- **50-69**: Somewhat unclear; too much technical jargon or jumps in logic
- **0-49**: Confusing; contradictory; unclear why this matters

**Example**: If a reader doesn't understand why Agni partnership matters to Mantle, clarity score is low.

### Dimension 3: Engagement Potential (20% weight)

Score 0-100:
- **90-100**: High likelihood of replies, retweets; hooks reader; calls reader to action
- **70-89**: Good engagement potential; engaging tone; some call-to-action
- **50-69**: Moderate engagement; informational but not particularly compelling
- **0-49**: Low engagement potential; dry tone; no call-to-action

**Example**: Historical data shows partnership announcements with CTAs average 78/100 engagement. If your thread has weak CTA, score lower.

### Dimension 4: Accuracy (15% weight)

Score 0-100:
- **90-100**: Every claim verified; no misrepresentations; direct quotes accurate
- **70-89**: Mostly accurate; minor details could be verified better
- **50-69**: Some claims not verified; paraphrasing slightly loosens accuracy
- **0-49**: Multiple inaccuracies; misrepresents facts; false claims

**Example**: If brief says "50M TVL" but you wrote "30M TVL", score 0 for accuracy.

### Dimension 5: Timing Fit (10% weight)

Score 0-100:
- **90-100**: Content perfectly fits engagement window; fresh, timely, relevant
- **70-89**: Fits engagement window reasonably well
- **50-69**: Timely but could be more urgent/reactive
- **0-49**: Doesn't fit timing; stale approach

**Example**: If engagement window is "publish within 2 hours" and your thread has time-bound details, score higher.

### Dimension 6: Compliance (10% weight)

Score 0-100:
- **90-100**: No prohibited content; follows all rules; approved topics only
- **70-89**: Compliant but touches approved-with-caution topic (will flag)
- **50-69**: Borderline compliance; contains borderline claims
- **0-49**: Violates compliance rules; includes prohibited content

**Example**: Financial advice ("This will moon") = fail compliance = 0.

### Calculate Confidence Score

```
confidence = (
  (brand_score × 0.25) +
  (clarity_score × 0.20) +
  (engagement_score × 0.20) +
  (accuracy_score × 0.15) +
  (timing_score × 0.10) +
  (compliance_score × 0.10)
)
```

**Example calculation**:
```
Brand: 85 (×0.25 = 21.25)
Clarity: 92 (×0.20 = 18.4)
Engagement: 78 (×0.20 = 15.6)
Accuracy: 95 (×0.15 = 14.25)
Timing: 85 (×0.10 = 8.5)
Compliance: 90 (×0.10 = 9.0)
Total: 87 → confidence: 87
```

## Step 8: Revision Loop

If confidence < 70:

1. **Identify weakness** (lowest-scoring dimension)
   - Example: "Engagement potential is 58 (lowest)"

2. **Rewrite to improve that dimension**
   - Example: If weak engagement, add stronger hook and CTA

3. **Re-score** (all dimensions again)

4. **Repeat** up to `revision_limit` times (default: 2)

If still below 70 after max revisions:
- **Do NOT send** to Distribution
- **Create escalation** to Governance (see Step 12)

## Step 9: Check Brand Compliance

Before writing to handoff file, verify:

### Voice Alignment
- ✓ Tone matches `brand/voice-guidelines.md`
- ✓ Language level (not too technical, not condescending)
- ✓ Messaging aligns with organizational pillars

### Topic Approval
- ✓ Topic is in `brand/approved-topics.md`
- ✓ If "approved with caution": set `review_recommended: true` (will be reviewed before publishing)
- ✗ If not approved: DO NOT SEND; escalate instead

### Prohibited Content Check
- ✗ Financial advice? "This will moon" / "You'll make 10x"
- ✗ Investment promises? "Guaranteed returns" / "Safe bet"
- ✗ Disparagement? "Arbitrum sucks" / "Optimism is inferior"
- ✗ False claims? Unverified technical capabilities

## Step 10: Write Body Sections

### Body Section 1: Content

The exact tweet text. Format as numbered list:

```markdown
## Content

1. 🚀 Agni Finance is bringing deep liquidity to Mantle. Here's why this partnership is a huge win for both protocols 🧵

2. Agni is one of the top DeFi aggregators in the industry. They manage 50M+ in TVL across multiple chains and serve thousands of traders daily.

3. They chose Mantle because of our superior efficiency and EVM compatibility. This validates that top-tier protocols prefer Mantle's infrastructure.

4. For Mantle users: You'll get access to Agni's best-in-class routing algorithms + massive liquidity pools. Better swaps. Lower slippage. Period.

5. Launching with incentives to bootstrap liquidity. Expect significantly deeper markets on Mantle starting [date].

6. Ready to experience the best DeFi UX on Mantle? Join us 🔗 [link]

#Mantle #DeFi #L2
```

### Body Section 2: Publishing Notes

```markdown
## Publishing Notes

**Target Channel**: @MantleNetwork on X/Twitter

**Publish Timing**: ASAP (within 1 hour of Distribution receiving this draft)

**Hashtags**: #Mantle, #DeFi, #L2

**Mentions**: @AgniFinance (for engagement/RT)

**Cross-post?**: No Discord announcement needed (thread is announcement enough)

**Bybit Conversion**:
- Conversion angle: {ecosystem-gateway | trading-opportunity | promo-amplify | none}
- Affiliate link included: {yes | no}
- CTA tweet number: {N, or "N/A" if no CTA}
```

### Body Section 3: Brief Reference

```markdown
## Brief Reference

**Originating Brief**: brief-20260312T1430-001

**How This Draft Aligns With Brief**:
- Format: Thread (recommended by brief)
- Tone: Celebratory + informational (as recommended)
- Length: 6 tweets (within max_thread_length of 10)
- Timing: Ready to publish during optimal engagement window (14:30-16:30 UTC)
```

## Step 11: Final Checks Before Sending

### Frontmatter Validation
- ✓ ID format correct: `draft-{YYYYMMDD}T{HHMM}-{sequence}`
- ✓ Confidence score ≥70
- ✓ review_recommended is true/false (not null)
- ✓ All required fields present
- ✓ YAML is valid (no syntax errors)

### Content Validation
- ✓ Each tweet is ≤280 characters
- ✓ Thread length (N tweets) ≤ max_thread_length
- ✓ No prohibited content
- ✓ All claims are verified
- ✓ Tone is consistent
- ✓ CTA is clear

### File Validation
- ✓ Filename matches pattern: `{timestamp}-thread-draft.md`
- ✓ All sections present (Content, Publishing Notes, Brief Reference)
- ✓ Markdown is properly formatted

## Step 12: Handle Low-Confidence Drafts

If confidence < 70 after `revision_limit` revisions:

1. **Create escalation file** in `handoffs/content-to-governance/`:

```yaml
---
id: esc-content-{timestamp}-{sequence}
from: content
to: governance
timestamp: {ISO 8601 UTC}
cycle: {current cycle}
priority: normal
status: pending
---
```

2. **Body**:

```markdown
## Low-Confidence Draft Escalation

**Brief ID**: {scout brief ID}

**Draft ID**: {your draft ID}

**Confidence Score**: {your score} (below threshold of 70)

**Problem**: [Identify weakest dimensions]

**Attempted Revisions**: {number}/{revision_limit}

**Request**: Should we:
1. Approve anyway and publish despite low confidence?
2. Reject brief and request Scout to re-signal?
3. Provide guidance on how to improve draft?
```

3. **Do NOT send** this draft to Distribution

## Step 13: Update Brief Status

After writing draft:

1. Go back to the Scout brief file
2. Update frontmatter: `status: completed`
3. Add new field: `completed_by: drafts/{your_draft_filename}.md`

## Step 14: Log and Update Heartbeat

1. Append to logs:
   ```
   [2026-03-12T15:10:00Z] thread_draft_created | draft-20260312T1510-001 | brief-20260312T1430-001 | confidence: 87
   ```

2. Update heartbeat in `state/agent-health.md`:
   ```
   content: {current ISO 8601 timestamp}
   ```

## Step 15: Send to Distribution

If confidence ≥70:

Write draft file to: `handoffs/content-to-distribution/drafts/{filename}-thread-draft.md`

Distribution Agent will pick it up on next cycle.

## Output

This prompt produces one file:

**File**: `handoffs/content-to-distribution/drafts/{timestamp}-thread-draft.md`

**Characteristics**:
- Valid YAML frontmatter (confidence ≥70)
- 6 tweets (numbered, each ≤280 chars)
- On-brand, compliant, accurate
- Ready for Distribution Agent to publish without modification

## Quality Checklist

Before sending:
- ✓ Confidence ≥70
- ✓ All tweets verified for accuracy
- ✓ Tone consistent throughout
- ✓ Each tweet ≤280 characters
- ✓ Call-to-action is clear
- ✓ No prohibited content
- ✓ Brief reference is accurate
- ✓ Publishing notes are specific

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Tweets exceed 280 characters | Edit to remove words; use abbreviations |
| Tone doesn't match guidelines | Rewrite to match voice guidelines |
| Claims not verified in brief | Go back to brief and verify data |
| No call-to-action | Add CTA in final tweet (link or next step) |
| Thread too long | Cut weakest tweets or move to separate thread |
| Confidence calculation wrong | Recalculate using all 6 dimensions |
