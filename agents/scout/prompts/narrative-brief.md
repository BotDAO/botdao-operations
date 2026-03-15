---
prompt_name: Narrative Brief Generation
agent: Scout
trigger: signal_detected
description: Detailed instructions for writing a comprehensive handoff brief from a single scored signal, structured per scout-to-content SCHEMA.md.
---

# Narrative Brief Writing Instructions

## Overview

When Scout detects a signal that scores above the relevance threshold, this prompt guides the generation of a structured handoff brief. The brief packages the signal with context, recommendations, and data so Content Agent can quickly draft publication-ready content.

## Prerequisites

Before using this prompt:
- Signal has been scored and exceeds `relevance_threshold`
- Signal has passed cooldown and deduplication checks
- Priority level has been assigned (normal/high/urgent)
- Crisis signals have been routed to Governance (NOT Content)

## Step 1: Set Up Brief Metadata

Generate a unique brief ID:
```
brief-{YYYYMMDD}T{HHMM}-{sequence}
```

Example: `brief-20260312T1430-001`

Set current timestamp (ISO 8601 UTC).

## Step 2: Create Brief File

**Location**: `handoffs/scout-to-content/briefs/{YYYY}-{MM}-{DD}T{HH}{MM}-{sequence}-brief.md`

**Example filename**: `2026-03-12T1430-001-brief.md`

## Step 3: Write Frontmatter

```yaml
---
id: brief-{YYYYMMDD}T{HHMM}-{sequence}
from: scout
to: content
timestamp: {ISO 8601 UTC, current time}
cycle: {current cycle number from state/current-cycle.md}
priority: {normal | high | urgent}
status: pending
expires: {ISO 8601 UTC, 6 hours from now}
---
```

### Priority Guidance

- **urgent**: Security incident, negative sentiment spike >5%, TVL drop >15%, major ecosystem partnership
- **high**: Protocol launch, TVL move 5-10%, governance change, ecosystem announcement
- **normal**: General updates, community news, minor metrics, technical developments

## Step 4: Write Signal Summary

**Purpose**: Explain what happened in language a Content Agent (writing for general audience) can immediately understand.

**Structure** (3-4 paragraphs):

### Paragraph 1: What Happened
- What is the event/announcement/metric change?
- When did it happen (timestamp)?
- Which entity is involved (protocol, user, Mantle)?

Example:
"Agni Finance announced a partnership with Mantle Network on March 12 at 14:30 UTC. The partnership includes marketing collaboration and potential liquidity incentives to boost Mantle's DeFi ecosystem."

### Paragraph 2: Why It Matters
- What is the narrative significance?
- How does it position Mantle (positive/neutral/defensive)?
- What is the broader implication for the ecosystem?

Example:
"This partnership strengthens Mantle's position as an attractive platform for top-tier DeFi protocols. Agni Finance is a tier-1 liquidity provider with 50M+ TVL; their endorsement signals confidence in Mantle's technical foundation and community."

### Paragraph 3: Suggested Engagement Angle
- How should Content Agent frame this?
- What story should we tell?
- What emotion/reaction should we aim for (bullish, informational, celebratory)?

Example:
"Frame this as evidence that Mantle is winning the L2 DeFi competition. Emphasize that top protocols choose Mantle for partnership. Tone: celebratory and factual."

## Step 5: Write Source Signals

Create **one subsection per data source** that contributed to this brief.

### Source Subsection Template

```markdown
### [Source Name]

**Platform**: [X/Twitter | Discord | Telegram | DeFiLlama | Mantle Explorer | etc.]

**Signal Description**: [What was detected]

**Signal Score**: [0-100 confidence]

**Detection Timestamp**: [ISO 8601]

**URL** (if applicable): [link to post, message, or data]

**Metrics** (if applicable):
- Engagement: X likes, Y retweets, Z replies
- OR TVL: $X million
- OR Volume: $X million
```

### Example: X/Twitter Source

```markdown
### X/Twitter Signal

**Platform**: X/Twitter

**Signal Description**: @AgniFinance posted announcement of partnership with Mantle. Post text discusses liquidity incentives and market expansion.

**Signal Score**: 87 (high relevance)

**Detection Timestamp**: 2026-03-12T14:30:00Z

**URL**: https://x.com/AgniFinance/status/123456789

**Metrics**:
- Engagement: 420 likes, 89 retweets, 34 replies
- Reach (estimated): ~8,000 impressions
- Sentiment: bullish (100% positive replies sampled)
```

### Example: On-Chain Signal

```markdown
### On-Chain Signal

**Platform**: Mantle Explorer

**Signal Description**: Agni Finance deployed new smart contract on Mantle (liquidity pool contract). This is first major contract deployment by the protocol.

**Signal Score**: 78 (confirms partnership is real)

**Detection Timestamp**: 2026-03-12T14:25:00Z

**URL**: https://explorer.mantle.xyz/tx/0x7f3a...

**Metrics**:
- TVL Impact: +$0 (not yet deployed), expected $5M based on announcement
- Gas Cost: [amount]
```

### Example: DeFiLlama Signal

```markdown
### DeFiLlama Signal

**Platform**: DeFiLlama API

**Signal Description**: Mantle TVL increased by 2.3% in the past 24 hours (from $450M to $460M). This follows Agni Finance announcement.

**Signal Score**: 62 (contextual, corroborates partnership impact)

**Detection Timestamp**: 2026-03-12T14:30:00Z

**URL**: https://defillama.com/chain/Mantle

**Metrics**:
- Current Mantle TVL: $460 million
- 24h Change: +$10 million (+2.3%)
- Top Protocol: [name] with [amount]
```

## Step 6: Write Recommendation

**Purpose**: Guide Content Agent on format, tone, and timing.

### Recommended Format

Choose one (or list priority order if multiple are viable):

- **thread** (preferred for announcements with context)
- **single-post** (preferred for time-sensitive reactions)
- **discord-announcement** (for community-focused announcements)

Example:
```
**Recommended Format**: Thread (3-5 tweets)

**Rationale**: Partnership announcement deserves detailed context. A thread allows us to:
1. Announce the partnership
2. Explain why Agni is tier-1
3. Describe expected benefits to Mantle users
4. Call-to-action: "Get started on Mantle + Agni"
```

### Recommended Tone

Choose one or describe mixture:

- **informational**: Facts-driven, neutral
- **celebratory**: Excited, bullish, highlight the win
- **thought-leadership**: Educational, strategic analysis
- **defensive**: Proactive response to negative sentiment

Example:
```
**Recommended Tone**: Celebratory + Informational

**Rationale**: This is clearly a positive win for Mantle. Readers expect bullish framing. However, maintain credibility by including concrete details (Agni's TVL, market position) rather than pure hype.
```

### Engagement Window

Specify the time window when content should be published:

```
**Optimal Engagement Window**: Publish within 2 hours (before 16:30 UTC)

**Rationale**: Announcement was made at 14:30 UTC. Community engagement is highest in the first 2-3 hours after announcement. After 4 hours, momentum drops.
```

### Suggested Hashtags

```
**Hashtags**: #Mantle #DeFi #L2 #Partnership
```

### Suggested Account Tags

```
**Account Tags**: @AgniFinance (for engagement), @MantleDevs (for credibility)
```

## Step 7: Write Supporting Data

Create a table with key metrics and sources:

```markdown
### Supporting Data

| Metric | Value | Source | Timestamp | Notes |
|--------|-------|--------|-----------|-------|
| Agni Finance TVL | $50M | DeFiLlama | 2026-03-12 | Tier-1 protocol |
| Mantle TVL | $460M | DeFiLlama | 2026-03-12T14:30 | Up 2.3% in 24h |
| Tweet Engagement | 543 total | X/Twitter | 2026-03-12T14:30 | Announcement post |
| Partnership Type | Liquidity incentives + marketing | Agni announcement | 2026-03-12T14:30 | Per announcement text |
```

**Data source rules**:
- Include timestamp for every metric
- Link to data source if possible (DeFiLlama URL, explorer link, etc.)
- Prioritize official sources (Agni's Twitter) over secondary sources
- Include 2-3 supporting metrics (not exhaustive list)

## Step 8: Write Context Section

Link this brief to previous analysis and performance patterns:

### Related Briefs

Search `data/narrative-tracker.md` for related narratives:

```markdown
### Related Briefs

- **brief-20260310T1200-001**: Previous analysis of Mantle's DeFi partnerships (March 10)
  - Status: published as single-post
  - Performance: 65 engagement score (average)

- **brief-20260301T1500-002**: Mantle TVL milestone announcement (March 1)
  - Status: published as thread
  - Performance: 82 engagement score (strong)
```

### Performance History

Reference Analytics scores for this narrative type:

```markdown
### Narrative Type Performance

**Narrative Type**: "DeFi Protocol Partnership"

**Historical Performance** (from analytics-to-scout scores):
- Average engagement score: 78/100
- Format that performs best: thread (avg 82) vs single-post (avg 74)
- Tone that performs best: celebratory
- Best publish window: 13:00-16:00 UTC
- On-chain attribution: 35% correlated with TVL changes within 48h

**Recommendation**: This narrative type is a consistent performer. Prioritize thread format and celebratory tone.
```

### Competitive Context

Research how other L2s might cover similar news:

```markdown
### Competitive Context

Arbitrum and Optimism may cover Agni partnerships with their respective networks. Mantle should move quickly to emphasize unique aspects:
- Mantle's lower gas costs vs Arbitrum/Optimism
- Mantle's EVM compatibility (vs other alternatives)
- Emphasis on "top protocols choose Mantle"
```

## Step 9: Review & Finalize

Before writing the file, check:

### Frontmatter Checklist
- ✓ ID follows pattern: `brief-{YYYYMMDD}T{HHMM}-{sequence}`
- ✓ Timestamp is ISO 8601 UTC
- ✓ Cycle number is correct
- ✓ Priority is one of: normal, high, urgent
- ✓ Status is `pending`
- ✓ Expires is 6 hours from now (ISO 8601)

### Content Checklist
- ✓ Signal Summary is clear to non-technical reader
- ✓ Why It Matters explains significance
- ✓ Engagement Angle is specific and actionable
- ✓ All sources are documented with platform, timestamp, score
- ✓ Recommendation specifies format, tone, timing
- ✓ Supporting Data includes 2-3 metrics with sources
- ✓ Context links to related briefs or performance data
- ✓ No crisis signals in this brief (those go to Governance)

### Quality Checks
- ✓ Frontmatter is valid YAML
- ✓ Markdown is properly formatted
- ✓ URLs are correct
- ✓ Timestamps are consistent
- ✓ No typos in metric values

## Step 10: Track in Narrative Tracker

After writing the brief file, append to `data/narrative-tracker.md`:

```
| brief-20260312T1430-001 | 2026-03-12T14:30:00Z | X/Twitter, On-Chain | Agni Partnership | 2h engagement window |
```

## Output

This prompt produces one file:

**File**: `handoffs/scout-to-content/briefs/{timestamp}-brief.md`

**Contents**:
- Valid YAML frontmatter
- 3-4 section body (Signal Summary, Source Signals, Recommendation, Supporting Data, Context)
- Ready for Content Agent to process

**Next Step**: Content Agent reads the brief, acknowledges it, and drafts publication-ready content.

## Common Pitfalls to Avoid

| Pitfall | Correction |
|---------|-----------|
| Signal Summary is too technical | Rephrase for general audience (non-crypto native) |
| Recommendation is vague | Be specific: "thread, 3-5 tweets, celebratory tone, publish by 16:00 UTC" |
| Missing data source URLs | Always include links to X posts, explorer pages, DeFiLlama URLs |
| Expired brief (too old) | If signal is >6 hours old when brief is written, adjust expires accordingly |
| No performance history | Check analytics scores for this narrative type; if none exist, note "first campaign of this type" |
| Crisis signal mixed in | Crisis signals bypass Content entirely — route to Governance via separate file |
