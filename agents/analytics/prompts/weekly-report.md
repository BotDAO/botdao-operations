---
prompt_name: Weekly Analytics Report Generation
agent: Analytics
trigger: weekly_schedule
description: Instructions for compiling the weekly performance summary across all campaigns completed in the past 7 days, including swarm health metrics and recommendations.
---

# Weekly Analytics Report Generation

## Overview

Every 7 days (or on schedule from config), Analytics Agent generates a comprehensive report summarizing all campaigns from the past week, their performance, anomalies detected, and recommendations for optimization.

**Report generated**: Weekly, typically on Monday morning (in UTC)

**Location**: `reports/weekly/analytics-{YYYY}-{MM}-{DD}.md`

## Step 1: Define Report Scope

### 1.1 Set Reporting Period

Define 7-day window:
- **End date**: Today (UTC midnight)
- **Start date**: 7 days ago (UTC midnight)

### 1.2 Gather Campaign List

From `data/engagement-history.md` (or internal campaign tracking):

List all campaigns completed (scored) in the reporting period.

**Example scope**:
```
Reporting Period: March 5-11, 2026 (UTC)
Campaigns Completed: 12
Campaign Brief IDs:
- brief-20260305T1400-001
- brief-20260305T1600-001
- brief-20260306T1200-001
... (9 more)
```

### 1.3 Organize by Category

Group campaigns by narrative type:
- DeFi protocol launches
- Partnership announcements
- Governance updates
- Ecosystem milestones
- Other

## Step 2: Compile Campaign Statistics

### 2.1 Overall Performance

```markdown
## Campaign Performance Summary (Past 7 Days)

**Period**: March 5-11, 2026 (UTC)

### Volume

| Metric | Count |
|--------|-------|
| Campaigns completed | 12 |
| Campaigns Good (>75) | 4 |
| Campaigns Average (50-75) | 7 |
| Campaigns Poor (<50) | 1 |

**Performance Distribution**:
- Good: 33% (above expectations)
- Average: 58% (typical)
- Poor: 8% (below expectations)
```

### 2.2 Aggregate Metrics

```markdown
### Aggregate Engagement Metrics

| Metric | Total | Average | Std Dev |
|--------|-------|---------|---------|
| Impressions (all X posts) | 92,450 | 7,704 | 2,100 |
| Total Engagement | 4,120 | 343 | 120 |
| Average Engagement Rate | 4.46% | 4.46% | 0.8% |
| Positive Replies | 187 | 15.6 | 8 |
| Reply Sentiment Score (avg) | 77.2 | 77.2 | 5.3 |

### On-Chain Correlation

| Metric | Average | Correlation |
|--------|---------|---|
| TVL Change | +1.8% | Moderate (0.65) |
| Volume Change | +7.2% | Moderate (0.62) |
| New Wallets | +285/day | Weak (0.42) |
```

## Step 3: Break Down by Narrative Type

For each narrative type with campaigns in the reporting period:

### 3.1 Create Subsection

```markdown
## Performance by Narrative Type

### DeFi Protocol Launches

**Campaigns**: 3
**Scores**: 78, 82, 71 (average: 77)
**Classification**: Mostly Good

**Top performer**: brief-20260308T1400-001 (score: 82)
- Strong impressions: 9,500
- High engagement rate: 5.2%
- Positive sentiment: 88%

**Underperformer**: brief-20260310T1500-001 (score: 71)
- Moderate impressions: 7,200
- Lower engagement: 3.8%
- Possible reason: Published during market volatility

**Trend**: DeFi protocol launches continue to perform well. Consistent strength across all 3 campaigns.

**Recommendation**: Maintain current weighting in Scout signal detection. Consider if timing improvements could boost the underperformer next time.

---

### Partnership Announcements

**Campaigns**: 4
**Scores**: 73, 68, 75, 69 (average: 71.25)
**Classification**: Average

**Top performer**: brief-20260307T1300-001 (score: 75)
- Excellent engagement: 4.8%
- Strong sentiment: 82%
- High CTR: 4.2%

**Consistent**: All 4 partnerships performed in average range (68-75)
- Impressions ranged 6,200-8,100
- Engagement rate 3.8-4.8%
- Sentiment positive but less enthusiastic than DeFi launches

**Recommendation**: Partnerships are reliable performers but lack the viral potential of DeFi launches. Consider stronger hooks or unique angles to boost engagement.

---

[Repeat for other narrative types...]
```

## Step 4: Identify Anomalies

### 4.1 Summarize Anomalies Detected

```markdown
## Anomalies Detected This Week

**Positive Anomalies**: 2

1. **brief-20260306T1400-001**: TVL spike correlation
   - Campaign: "Mantle TVL hits $500M"
   - TVL actually jumped +5.2% during 48h window (benchmark: +2%)
   - Suggests campaign may have driven real ecosystem activity
   - Recommendation: Continue emphasizing TVL milestones

2. **brief-20260309T1600-001**: Viral engagement
   - Campaign: "Developer community milestone"
   - Impressions: 12,800 (97% above benchmark)
   - Engagement rate: 6.3% (50% above benchmark)
   - Recommendation: Analyze what made this resonate; replicate format/tone

**Negative Anomalies**: 1

1. **brief-20260311T1400-001**: Sentiment spike negative
   - Campaign: "Ecosystem update"
   - Negative replies: 15 (baseline: 2-3)
   - Community concerns about roadmap decisions
   - Recommendation: Governance Agent should review for crisis response

---
```

### 4.2 Link to Anomaly Reports

Reference any formal anomaly reports generated:
```
[See: handoffs/analytics-to-governance/reports/20260311T1430-anomaly.md for full analysis]
```

## Step 5: Analyze Performance Trends

### 5.1 Format Performance

```markdown
## Format Performance Analysis

### Thread vs Single-Post

| Format | Count | Avg Score | Avg Impressions | Avg Engagement |
|--------|-------|-----------|---|---|
| Thread | 8 | 74.5 | 8,200 | 4.6% |
| Single-Post | 4 | 68.3 | 6,100 | 3.9% |

**Finding**: Threads consistently outperform single-posts (+6.2 points, +31% impressions)

**Implication**: Content Agent should bias toward thread format for narratives where depth is valuable.

**Exceptions**: Time-sensitive reactions may work better as single-posts (faster turnaround).

---

### Content Length (for threads)

| Length | Count | Avg Score | Engagement |
|--------|-------|-----------|---|
| 3-4 tweets | 2 | 71 | 4.2% |
| 5-6 tweets | 4 | 76 | 4.7% |
| 7-8 tweets | 2 | 72 | 4.4% |

**Finding**: 5-6 tweet threads perform best (sweet spot)

**Implication**: Content Agent should target 5-6 tweets for partnerships/announcements.

---
```

### 5.2 Tone Performance

```markdown
## Tone Performance Analysis

| Tone | Campaigns | Avg Score | Sentiment |
|------|-----------|-----------|---|
| Celebratory | 5 | 76.2 | 82% positive |
| Informational | 4 | 70.1 | 76% positive |
| Thought-Leadership | 3 | 73.4 | 80% positive |

**Finding**: Celebratory tone performs best for announcements/partnerships

**Implication**: Content Agent should default to celebratory for good news; reserve informational for neutral updates.

---
```

### 5.3 Publishing Time Performance

```markdown
## Optimal Publishing Time Analysis

| Time Window | Campaigns | Avg Score | Peak Engagement |
|---|---|---|---|
| 13:00-14:00 UTC | 3 | 74.2 | 14:30 UTC |
| 14:00-15:00 UTC | 4 | 75.8 | 15:15 UTC |
| 15:00-16:00 UTC | 3 | 71.5 | 16:00 UTC |
| 16:00-17:00 UTC | 2 | 68.9 | 17:15 UTC |

**Finding**: 14:00-15:00 UTC publish window shows best performance

**Recommendation**: Update `data/timing-model.md` to prioritize 14:00-15:00 UTC for future campaigns.

---
```

## Step 6: Swarm Health Metrics

### 6.1 Agent Performance

```markdown
## Swarm Agent Performance

### Scout Agent

| Metric | Value | Status |
|--------|-------|--------|
| Briefs generated (week) | 12 | Normal |
| Avg signal quality | 7.3/10 | Good |
| Crisis escalations | 0 | None |
| Heartbeat staleness | <30min | Healthy |

**Assessment**: Scout Agent performing well. Signal quality is consistent.

---

### Content Agent

| Metric | Value | Status |
|--------|-------|--------|
| Drafts created | 12 | Normal (= briefs) |
| Avg confidence score | 78 | Good |
| Low-confidence escalations | 1 | Low frequency |
| Revision rate | 8% | Good (most drafts accepted first-try) |
| Heartbeat staleness | <25min | Healthy |

**Assessment**: Content Agent performing very well. Confidence scores are strong; few escalations.

---

### Distribution Agent

| Metric | Value | Status |
|--------|-------|--------|
| Publishes completed | 12 | Normal (= drafts) |
| Publish failures | 0 | None |
| Timing violations | 0 | All constraints respected |
| Attestation success | 100% | Perfect |
| Heartbeat staleness | <20min | Healthy |

**Assessment**: Distribution Agent is flawless. All publishes successful; all constraints respected.

---

### Analytics Agent

| Metric | Value | Status |
|--------|-------|--------|
| Campaigns scored | 12 | Normal |
| Scoring accuracy | 8.5/10 | Good |
| Report generation | On-schedule | Healthy |
| Heartbeat staleness | <30min | Healthy |

**Assessment**: Analytics Agent keeping pace. Scoring is consistent.

---
```

### 6.2 System Health

```markdown
## System Health Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Agent heartbeats | ✓ All healthy | No stale agents |
| Handoff channels | ✓ Flowing | No blockages |
| On-chain attestation | ✓ 100% success | All publishes recorded |
| Data integrity | ✓ Clean | No corrupted files |
| Operational cycle | ✓ Normal | On schedule |

**Overall Health**: GREEN 🟢 (system operating nominally)

---
```

## Step 7: Generate Recommendations

### 7.1 For Scout Agent

```markdown
## Recommendations

### Scout Agent

**Observation**: DeFi protocol launches are strong performers (avg 77). Partnership announcements are consistent but lower (avg 71).

**Recommendation**:
- Maintain current focus on DeFi protocol signals
- Continue monitoring partnership opportunities (reliable but not viral)
- Consider increasing weighting on TVL milestone narratives (showed positive on-chain correlation)

**Specific Action Items**:
1. Slightly increase `relevance_threshold` for DeFi launches (already high-performing)
2. Consider scanning for secondary effects of partnerships (e.g., on-chain activity spikes) as signals
3. Monitor competitive L2 ecosystem announcements to catch partnership opportunities early

---
```

### 7.2 For Content Agent

```markdown
### Content Agent

**Observation**: Thread format significantly outperforms single-posts. 5-6 tweet threads are optimal. Celebratory tone drives best sentiment.

**Recommendations**:
- Default to thread format for announcements/partnerships (vs. single-posts)
- Target 5-6 tweets per thread (proven sweet spot)
- Use celebratory tone for positive narratives
- Maintain current confidence scoring discipline (78 avg is strong)

**Specific Action Items**:
1. Update content drafting workflow to bias toward threads
2. Set internal target length at 5-6 tweets
3. A/B test hook variations in future threads to further boost initial engagement

---
```

### 7.3 For Distribution Agent

```markdown
### Distribution Agent

**Observation**: Flawless execution. All publishes successful, all timing constraints respected, 100% attestation success.

**Recommendation**: Continue current operation. No changes needed.

**Note**: Consider exploring optimal timing window 14:00-15:00 UTC if scout and content agents provide flexibility.

---
```

### 7.4 For Governance Agent

```markdown
### Governance Agent

**Observation**: System is operating healthily. No agent issues, no escalations, all constraints respected.

**Recommendation**:
- Monitor anomaly trend (1 negative detected this week; establish pattern?)
- Review sentiment spike in brief-20260311T1400-001 (see Analytics-to-Governance report)
- Consider updating timing model based on new performance data (14:00-15:00 UTC window showing best results)

---
```

## Step 8: Update Timing Model

### 8.1 Incorporate New Data

Based on this week's performance, update `data/timing-model.md` sections:

```markdown
## DeFi Protocol Launches

**Historical Performance** (updated with week of 3/5-3/11):
- Average engagement peak: 14:00-15:00 UTC (confirmed from 3 campaigns)
- Secondary peak: 15:00-16:00 UTC
- Lowest engagement: 22:00-07:00 UTC
- Best day of week: Tuesday-Thursday (all 3 campaigns published on these days)

**Sample Size**: 13 campaigns (up from 10)
**Confidence Level**: Medium (sufficient data for confidence)

**Last Updated**: 2026-03-11

---
```

### 8.2 Note Confidence Increases

If any narrative type has accumulated enough sample size (10+), note confidence increase:

```markdown
## Partnership Announcements

**Historical Performance** (updated with week of 3/5-3/11):
- Average engagement peak: 13:00-14:00 UTC (adjusted from previous 13:00-15:00)
- Secondary peak: 17:00-19:00 UTC
- Best day of week: Monday, Wednesday, Friday

**Sample Size**: 14 campaigns (up from 10)
**Confidence Level**: Medium (entering "medium confidence" range)

**Last Updated**: 2026-03-11

**Note**: Confidence upgraded from "Low" to "Medium" as sample size exceeded 10.

---
```

## Step 9: Create Summary Table

### 9.1 Campaign Summary Table

```markdown
## Detailed Campaign Results (Week of 3/5-3/11)

| Brief ID | Narrative | Format | Published | Score | Classification | Key Insight |
|---|---|---|---|---|---|---|
| brief-20260305T1400-001 | DeFi Launch | Thread | 3/5 14:00 | 78 | Good | Strong impressions |
| brief-20260305T1600-001 | Partnership | Single | 3/5 16:00 | 73 | Average | Reliable performer |
| brief-20260306T1200-001 | Ecosystem | Thread | 3/6 12:00 | 82 | Good | **VIRAL** - Anomaly |
| brief-20260306T1400-001 | TVL Update | Single | 3/6 14:00 | 75 | Good | TVL spike corr. |
| ... (8 more) |

---
```

## Step 10: Compile Report Frontmatter

```markdown
---
report_type: weekly_analytics
period_start: 2026-03-05
period_end: 2026-03-11
generated_at: 2026-03-12T08:00:00Z
cycles_covered: 7 (cycles 42-48)
campaigns_scored: 12
anomalies_detected: 3
---

# Weekly Analytics Report — Week of March 5-11, 2026

**Generated**: March 12, 2026, 08:00 UTC

---
```

## Step 11: Final Report Structure

Complete report includes (in order):

1. **Frontmatter** — metadata
2. **Executive Summary** — 2-3 paragraph overview
3. **Campaign Performance** — volume, metrics, distribution
4. **Performance by Narrative Type** — subsections for each type
5. **Anomalies Detected** — positive and negative
6. **Format/Tone/Timing Analysis** — performance breakdowns
7. **Swarm Agent Health** — each agent's metrics and assessment
8. **Recommendations** — specific action items per agent
9. **Timing Model Updates** — new data incorporated
10. **Detailed Campaign Table** — row per campaign
11. **Next Week Outlook** — expectations and monitoring focus

## Step 12: Write and Publish Report

### 12.1 File Location

`reports/weekly/analytics-{YYYY}-{MM}-{DD}.md`

Example: `reports/weekly/analytics-2026-03-12.md`

### 12.2 Write to File

Generate markdown file with all sections above.

### 12.3 Cross-Reference

Link from main reports directory:
- Create entry in `reports/README.md` pointing to latest report
- Or include link in governance log

## Step 13: Notify Stakeholders

### 13.1 Log Report Generation

Append to logs:

```
[{timestamp}] weekly_report_generated | {filename} | {campaigns} campaigns scored, {anomalies} anomalies detected
```

### 13.2 Create GitHub Issue (Optional)

If using GitHub for tracking:

```markdown
**Title**: Weekly Analytics Report: Week of 3/5-3/11

**Body**:
Report generated and available at: `reports/weekly/analytics-2026-03-12.md`

Key findings:
- 12 campaigns scored
- 33% performed well (>75)
- Threads outperform single-posts by +6.2 points
- Optimal timing: 14:00-15:00 UTC
- 1 negative anomaly detected (sentiment spike)

Next steps: Review recommendations by agent team.
```

## Step 14: Update Heartbeat

```
analytics: {current ISO 8601 timestamp}
```

## Output

Weekly report produces:

- **One comprehensive markdown file**: `reports/weekly/analytics-{date}.md`
- **Updated timing model**: `data/timing-model.md` with new campaign data
- **Updated engagement history**: `data/engagement-history.md` (weekly snapshot)
- **Log entries**: 1-2 entries documenting report generation
- **Optional GitHub issue**: For team visibility

## Quality Checklist

Before finalizing report:

- [ ] ✓ All campaigns from period included
- [ ] ✓ Performance metrics calculated correctly
- [ ] ✓ Narrative type breakdowns complete
- [ ] ✓ Anomalies documented
- [ ] ✓ Recommendations are specific and actionable
- [ ] ✓ Agent assessments accurate and fair
- [ ] ✓ Timing model updated with new sample sizes
- [ ] ✓ Report file uses correct naming
- [ ] ✓ All links and references valid
- [ ] ✓ Tone is professional and data-driven

## Report Examples

Past reports can be referenced:
- `reports/weekly/analytics-2026-03-05.md` (previous week)
- `reports/weekly/analytics-2026-02-26.md` (2 weeks ago)

## Integration

This report is read by:
- **Governance Agent**: For system health assessment and escalation decisions
- **Scout Agent**: For narrative weighting recommendations
- **Content Agent**: For format/tone optimization
- **Human operators**: For swarm performance overview and decision-making

All stakeholders should review weekly to stay aligned on what's working and what needs adjustment.
