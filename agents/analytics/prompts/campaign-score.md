---
prompt_name: Campaign Performance Scoring
agent: Analytics
trigger: monitoring_window_closes
description: Instructions for scoring published content after the 48-hour monitoring window, calculating weighted engagement scores, and generating feedback for Scout and Content agents.
---

# Campaign Performance Scoring Instructions

## Overview

When a published campaign completes its 48-hour monitoring window, Analytics Agent scores its performance using a weighted rubric. The score becomes feedback for Scout Agent (on narrative effectiveness) and Content Agent (on format/tone effectiveness).

## Prerequisites

- Receipt has been received from Distribution Agent
- 48-hour monitoring window has closed (or is closing)
- Engagement data has been collected via X API, Discord API, DeFiLlama, and Mantle explorer
- Campaign is ready for scoring

## Step 1: Set Up Scoring Session

### 1.1 Identify Campaign

From `handoffs/distribution-to-analytics/receipts/`:
- Find receipt with `status: pending` (unscored)
- Extract: brief_id, draft_id, published_at, monitoring_window_end

### 1.2 Load Campaign Data

From internal campaign tracking (populated when receipt was received):
```
campaign_{brief_id} = {
    brief_id: string
    draft_id: string
    published_at: ISO 8601
    published_to: [channels]
    post_ids: {x: string, discord: string, ...}
    monitoring_until: ISO 8601
    collected_data: {...}  // snapshots from polling
}
```

### 1.3 Verify Monitoring Window Closed

```
if current_time >= campaign.monitoring_until:
    PROCEED_TO_STEP_2()
else:
    DEFER_UNTIL(campaign.monitoring_until + 30_minutes)
```

## Step 2: Aggregate Engagement Metrics

### 2.1 Compile X/Twitter Metrics

For each post/tweet in the thread (if multi-post):

**Collect**:
- Impressions (total reach)
- Likes (count)
- Retweets (count)
- Replies (count)
- Click-through rate (if available from link tracker)
- Engagement rate = (likes + retweets + replies) / impressions

**Sample top replies** (20-30):
- Classify sentiment: positive / neutral / negative
- Count: positive_replies, negative_replies, neutral_replies

**Example data structure**:
```
x_metrics = {
    impressions: 8420,
    likes: 234,
    retweets: 89,
    replies: 45,
    engagement_rate: 0.0408,  // (234+89+45)/8420
    click_throughs: 340,
    ctr: 0.0404,
    reply_sentiment: {
        positive: 28,
        neutral: 12,
        negative: 5
    }
}
```

### 2.2 Compile Discord Metrics

For each message published to Discord:

**Collect**:
- Reactions (count by emoji)
- Reply threads (count, if applicable)
- Total reaction count

**Example data**:
```
discord_metrics = {
    reactions_total: 45,
    reactions_emoji: {
        thumbs_up: 20,
        rocket: 15,
        heart: 10
    },
    reply_threads: 3,
    reply_count: 12
}
```

### 2.3 Compile On-Chain Metrics

Compare pre/post publish on-chain activity:

**Collect** (from Mantle explorer):
- New wallets created (baseline vs. 48h window)
- Transaction volume (baseline vs. 48h window)
- New protocol activity (contracts deployed, interactions)

**Collect** (from DeFiLlama):
- TVL at start of window
- TVL at end of window
- TVL change %
- Trading volume at start/end
- Volume change %

**Example data**:
```
onchain_metrics = {
    tvl_start: 450000000,      // $450M
    tvl_end: 460000000,        // $460M
    tvl_change_pct: 2.22,      // +2.22%
    volume_start: 12500000,    // $12.5M
    volume_end: 13800000,      // $13.8M
    volume_change_pct: 10.4,   // +10.4%
    new_wallets: 342,
    baseline_wallets_per_day: 250,
    transaction_count: 4821,
    baseline_txn_per_day: 4000
}
```

## Step 3: Load Benchmark Data

### 3.1 Read Historical Benchmarks

Open `data/engagement-history.md`:

**For narrative type** (from brief):
- Average impressions: X
- Average engagement rate: Y%
- Average positive reply ratio: Z%

**For format** (from draft):
- Thread vs single-post historical averages
- Average performance by format

**Example from engagement-history**:
```
## DeFi Protocol Launches

### Historical Benchmarks (10 campaigns)

| Metric | Average | Std Dev |
|--------|---------|---------|
| Impressions | 6500 | 1200 |
| Engagement Rate | 4.2% | 0.8% |
| Positive Reply % | 82% | 8% |
| Retweet Ratio | 28% | 5% |
| CTR | 3.5% | 1.2% |
| On-Chain TVL Correlation | +1.5% | 0.8% |

### Format Performance (within this type)

Thread: Avg 7200 impressions, 4.8% engagement
Single-post: Avg 5800 impressions, 3.6% engagement
```

### 3.2 Load Draft-Specific Metadata

From the draft file:
- Format (thread, single-post, etc.)
- Confidence score (how good Content Agent thought it was)
- Priority level

## Step 4: Calculate Scoring Metrics

### 4.1 Impressions Score

```
impressions_benchmark = benchmark_for_narrative_type
impressions_observed = x_metrics.impressions

impressions_normalized = (impressions_observed / impressions_benchmark) * 100
impressions_capped = min(impressions_normalized, 150)  // cap at 150% (avoid outlier inflation)

// Scale to 0-100
impressions_score = impressions_capped / 1.5
```

**Example**:
```
Observed: 8,420 impressions
Benchmark: 6,500 impressions
Normalized: (8420 / 6500) * 100 = 129.5
Capped: 129.5 (under 150 cap)
Score: 129.5 / 1.5 = 86.3
```

### 4.2 Engagement Rate Score

```
engagement_benchmark = benchmark_for_narrative_type  // e.g., 4.2%
engagement_observed = x_metrics.engagement_rate * 100  // convert to percentage

engagement_normalized = (engagement_observed / engagement_benchmark) * 100
engagement_capped = min(engagement_normalized, 150)

engagement_score = engagement_capped / 1.5
```

**Example**:
```
Observed: 4.08%
Benchmark: 4.2%
Normalized: (4.08 / 4.2) * 100 = 97.1
Capped: 97.1
Score: 97.1 / 1.5 = 64.7
```

### 4.3 Reply Sentiment Score

```
positive_replies = reply_sentiment.positive
negative_replies = reply_sentiment.negative
total_replies = positive_replies + negative_replies + neutral_replies

sentiment_ratio = (positive_replies - negative_replies) / total_replies
sentiment_normalized = (sentiment_ratio + 1.0) * 50  // shift from [-1,1] to [0,100]

reply_sentiment_score = sentiment_normalized
```

**Example**:
```
Positive: 28, Negative: 5, Neutral: 12 (total: 45)
Ratio: (28 - 5) / 45 = 0.511
Normalized: (0.511 + 1.0) * 50 = 75.5
Score: 75.5
```

### 4.4 Retweet Ratio Score

```
retweet_ratio = retweets / (retweets + likes)

retweet_benchmark = benchmark_for_narrative_type  // e.g., 0.28 (28%)
retweet_normalized = (retweet_ratio / retweet_benchmark) * 100
retweet_capped = min(retweet_normalized, 150)

retweet_score = retweet_capped / 1.5
```

**Example**:
```
Retweets: 89, Likes: 234
Ratio: 89 / (89 + 234) = 0.275
Benchmark: 0.28
Normalized: (0.275 / 0.28) * 100 = 98.2
Capped: 98.2
Score: 98.2 / 1.5 = 65.5
```

### 4.5 Click-Through Rate Score

```
ctr_benchmark = benchmark_for_narrative_type  // e.g., 3.5%
ctr_observed = x_metrics.ctr * 100

ctr_normalized = (ctr_observed / ctr_benchmark) * 100
ctr_capped = min(ctr_normalized, 150)

ctr_score = ctr_capped / 1.5
```

**Example**:
```
Observed: 4.04%
Benchmark: 3.5%
Normalized: (4.04 / 3.5) * 100 = 115.4
Capped: 115.4
Score: 115.4 / 1.5 = 76.9
```

### 4.6 On-Chain Attribution Score

Track whether on-chain activity spiked during the 48h window:

```
tvl_change = onchain_metrics.tvl_change_pct
volume_change = onchain_metrics.volume_change_pct
new_wallets_delta = onchain_metrics.new_wallets - (baseline_wallets_per_day * 2)

// Normalize each component
tvl_score = (tvl_change / 2.0) * 50 + 50  // scale to 0-100 around 2% change
volume_score = (volume_change / 10.0) * 50 + 50  // scale around 10% change
wallets_score = min((new_wallets_delta / baseline_wallets_per_day) * 50 + 50, 100)

// Average on-chain component
onchain_score = (tvl_score + volume_score + wallets_score) / 3
```

**Example**:
```
TVL change: +2.22%
TVL score: (2.22 / 2.0) * 50 + 50 = 105.5 → capped at 100

Volume change: +10.4%
Volume score: (10.4 / 10.0) * 50 + 50 = 102 → capped at 100

New wallets: 342 observed, 250 baseline for 2 days = 500 expected
Delta: 342 - 500 = -158 (below baseline)
Wallets score: (-158 / 250) * 50 + 50 = 18.4

On-chain score: (100 + 100 + 18.4) / 3 = 72.8
```

## Step 5: Calculate Weighted Campaign Score

```
campaign_score = (
  (impressions_score × 0.15) +
  (engagement_rate_score × 0.25) +
  (reply_sentiment_score × 0.20) +
  (retweet_ratio_score × 0.15) +
  (ctr_score × 0.15) +
  (onchain_score × 0.10)
)
```

**Example calculation**:
```
Impressions: 86.3 (×0.15 = 12.95)
Engagement: 64.7 (×0.25 = 16.18)
Sentiment: 75.5 (×0.20 = 15.10)
Retweet: 65.5 (×0.15 = 9.83)
CTR: 76.9 (×0.15 = 11.54)
On-chain: 72.8 (×0.10 = 7.28)
Total: 72.88 → rounded to 73
```

## Step 6: Classify Performance

```
if campaign_score > 75:
    classification = "Good"
elif campaign_score >= 50:
    classification = "Average"
else:
    classification = "Poor"
```

## Step 7: Detect Anomalies

### 7.1 Positive Anomaly

```
if any metric > benchmark * 1.2:  // 20% above benchmark
    positive_anomaly = true
    anomaly_magnitude = metric_observed - benchmark
```

**Example**: Impressions 8,420 vs benchmark 6,500 = +1,920 impressions (29.5% above)

### 7.2 Negative Anomaly

```
if any metric < benchmark * 0.8:  // 20% below benchmark
    negative_anomaly = true
    anomaly_magnitude = benchmark - metric_observed
```

**Example**: Engagement 4.08% vs benchmark 4.2% = -0.12% (2.9% below) — minor, below anomaly threshold

### 7.3 Create Anomaly Report (If Needed)

If any anomaly detected, create separate report:

File: `handoffs/analytics-to-governance/reports/{timestamp}-anomaly.md`

```yaml
---
id: anomaly-{timestamp}-{sequence}
from: analytics
to: governance
timestamp: {ISO 8601 UTC}
cycle: {current cycle}
priority: {high if negative, normal if positive}
status: pending
deviation: {+35% | -15% | etc.}
direction: {over | under}
---

## Anomaly Report

**Campaign**: {brief_id}
**Narrative Type**: {type}
**Anomaly Type**: {type of metric that deviated}
**Metric**: {metric name}
**Benchmark**: {value}
**Observed**: {value}
**Deviation**: {+X% | -X%}

**Possible Causes**:
- [List hypotheses]

**Recommended Action**:
- [What should change? Should we replicate or avoid this pattern?]
```

## Step 8: Generate Scout Feedback

File: `handoffs/analytics-to-scout/scores/{timestamp}-scout-score.md`

### 8.1 Frontmatter

```yaml
---
id: navscore-{timestamp}-{sequence}
from: analytics
to: scout
timestamp: {ISO 8601 UTC}
cycle: {current cycle}
priority: normal
status: pending
brief_id: {brief_id}
narrative: {narrative type from brief}
overall_score: {0-100}
---
```

### 8.2 Body Sections

#### Section 1: Score Breakdown

```markdown
## Score Breakdown

| Metric | Score | Weight | Contribution |
|--------|-------|--------|---|
| Impressions | 86 | 15% | 12.9 |
| Engagement Rate | 65 | 25% | 16.2 |
| Reply Sentiment | 76 | 20% | 15.1 |
| Retweet Ratio | 66 | 15% | 9.8 |
| Click-Through Rate | 77 | 15% | 11.5 |
| On-Chain Attribution | 73 | 10% | 7.3 |
| **Overall Score** | **73** | 100% | **73** |
```

#### Section 2: Narrative Assessment

```markdown
## Narrative Assessment

**Narrative Type**: DeFi Protocol Partnership

**Performance Classification**: Average (50-75 range)

**Performance vs. Benchmark**:
- This DeFi partnership campaign scored 73, slightly below the type's average of 76
- Impressions were strong (29% above benchmark)
- Engagement rate was slightly below benchmark
- Reply sentiment was positive (75.5 score)
- On-chain correlation was moderate

**What Worked**:
- High impressions indicate broad reach
- Strong positive sentiment in replies shows community likes the partnership
- Good click-through rate suggests interest in learning more

**What Could Improve**:
- Engagement rate (likes + retweets) lagged benchmark
- Could have stronger call-to-action to drive more interactions
```

#### Section 3: Recommendation

```markdown
## Recommendation for Scout

**Narrative Type Weighting**: DeFi partnerships should maintain current weighting in signal detection

**Suggested Action**:
- Continue prioritizing DeFi partnership signals (score 73 is respectable)
- Consider if different hooks or partnership types perform better
- Monitor whether subsequent partnerships improve with Content Agent optimization

**Sample Size**: This is the Nth campaign of this type. [If very few: data is still building. If many: confident in recommendation.]

**Next Steps**: See Analytics-to-Content feedback for Content Agent improvements; they may address the engagement gap in future partnership campaigns.
```

## Step 9: Generate Content Feedback

File: `handoffs/analytics-to-content/scores/{timestamp}-content-score.md`

### 9.1 Frontmatter

```yaml
---
id: fmtscore-{timestamp}-{sequence}
from: analytics
to: content
timestamp: {ISO 8601 UTC}
cycle: {current cycle}
priority: normal
status: pending
draft_id: {draft_id}
format: {format}
overall_score: {0-100}
---
```

### 9.2 Body Sections

#### Section 1: Score Breakdown

Same metrics table as Scout feedback (above).

#### Section 2: Format Assessment

```markdown
## Format Assessment

**Format Used**: Thread (5 tweets)

**Format Performance**:
- Threads (historically) average 72/100 for DeFi partnership narratives
- This thread scored 73, slightly above thread average
- Single-posts for same topic average 68 (thread was better choice)

**Format Effectiveness**:
- Threading allowed detailed explanation of partnership benefits
- 5-tweet length was appropriate (not too long, not too short)
- Each tweet built logically on previous

**Recommendation**: Thread format was effective for this content.
```

#### Section 3: Tone Assessment

```markdown
## Tone Assessment

**Tone Used**: Celebratory + Informational

**Tone Reception**:
- Reply sentiment was 75.5/100 (very positive)
- Comments were substantive (not spam/noise)
- Community responses were engaged and questioning (good sign)

**Tone Effectiveness**:
- Celebratory tone resonated well with audience
- Balance with facts kept it credible (not pure hype)

**Recommendation**: This tone worked well. Replicate for future partnerships.
```

#### Section 4: Recommendation

```markdown
## Recommendation for Content

**What Worked**:
- Format choice (thread) was effective
- Tone (celebratory + informational) resonated
- Structure flowed well

**What to Improve**:
- Engagement rate (likes + retweets) was 4.08%, slightly below 4.2% benchmark
- Could strengthen hook in first tweet to drive more initial engagement
- Consider testing stronger call-to-action in final tweet

**Suggested Changes for Next Campaign**:
1. Hook: Make opening tweet punchier/more attention-grabbing
2. CTA: Strengthen final-tweet call-to-action (link or action)
3. Tone: Keep celebratory + informational (was successful)
4. Format: Continue with thread for partnership announcements

**Confidence Scoring Note**:
- You scored this draft 85/100
- Actual performance: 73/100
- Discrepancy: -12 points
- Possible reasons: external factors (market sentiment, timing), underestimated difficulty of audience engagement
```

## Step 10: Update Historical Data

### 10.1 Append to Engagement History

File: `data/engagement-history.md`

Add row to the table for this narrative type:

```markdown
| brief-20260312T1430-001 | DeFi Protocol Partnership | thread | 73 | 8420 | 4.08% | +2.22% TVL | {timestamp} |
```

### 10.2 Update Timing Model (Optional)

If Analytics observes a strong pattern in when posts published:
- Log publish time: 15:30 UTC
- Log peak engagement time: 16:45 UTC (example)
- Note for future timing model updates

## Step 11: Update Campaign Tracking

### 11.1 Mark Campaign as Scored

Update internal tracking:
```
campaign_{brief_id}.status = "scored"
campaign_{brief_id}.score = {score}
campaign_{brief_id}.classification = {Good | Average | Poor}
```

### 11.2 Update Receipt Status

Go back to receipt file in `handoffs/distribution-to-analytics/receipts/`:

Update frontmatter:
```yaml
status: completed
score: {0-100}
classification: {Good | Average | Poor}
```

## Step 12: Log Scoring

Append to logs:

```
[{timestamp}] campaign_score_complete | brief-{brief_id} | score: {score} | classification: {classification}
[{timestamp}] scout_feedback_sent | navscore-{id} | {narrative_type}
[{timestamp}] content_feedback_sent | fmtscore-{id} | {format} performance
```

If anomaly detected:
```
[{timestamp}] anomaly_detected | {brief_id} | {anomaly_type} | {metric} {+X% | -X%}
```

## Step 13: Update Heartbeat

Update `state/agent-health.md`:
```
analytics: {current ISO 8601 timestamp}
```

## Output

Scoring cycle produces:
- **Scout feedback file**: `handoffs/analytics-to-scout/scores/{id}.md`
- **Content feedback file**: `handoffs/analytics-to-content/scores/{id}.md`
- **Anomaly report** (if applicable): `handoffs/analytics-to-governance/reports/{id}.md`
- **Updated engagement history**: entry added to `data/engagement-history.md`
- **Log entries**: 3-4 entries documenting scoring and feedback

## Quality Checklist

Before finalizing scores:

- [ ] ✓ All 6 metrics calculated correctly
- [ ] ✓ Weighted average is accurate
- [ ] ✓ Benchmarks retrieved from engagement history
- [ ] ✓ Anomalies identified (if any)
- [ ] ✓ Scout feedback explains narrative performance
- [ ] ✓ Content feedback addresses format/tone
- [ ] ✓ Recommendations are actionable
- [ ] ✓ Files use correct naming convention
- [ ] ✓ YAML frontmatter is valid
- [ ] ✓ Historical data updated

## Integration with Weekly Report

Scores from this prompt feed into the weekly report that Governance Agent generates. See `weekly-report.md` prompt for how individual campaign scores are aggregated.

## Important Notes

- **Anomalies take priority**: If campaign deviates significantly, create anomaly report immediately (escalate to Governance)
- **Sample size matters**: Early campaigns have lower confidence in benchmarks; as more campaigns complete, model becomes more reliable
- **Format/tone feedback is actionable**: Content Agent specifically uses these recommendations to optimize future drafts
- **On-chain correlation is crucial**: If campaign drives on-chain activity despite low social engagement (or vice versa), this is valuable learning
