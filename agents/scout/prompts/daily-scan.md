---
prompt_name: Daily Narrative Scan Cycle
agent: Scout
trigger: operational_turn
description: Regular monitoring cycle that scans all data sources for narrative signals and generates priority-ranked signal briefs.
---

# Daily Scan Cycle Instructions

## Overview

Execute a complete scan of all monitored data sources (X/Twitter, Discord, Telegram, DeFiLlama, Mantle explorer) and compile ranked signals into narrative briefs. This prompt runs continuously during each Scout operational turn.

## Step 1: Pre-Scan Setup

1. Read config parameters from `agents/scout/config.md`:
   - `scan_interval` (hours since last scan)
   - `relevance_threshold` (0-100 scoring floor)
   - `narrative_cooldown` (hours before re-covering same narrative)
   - `max_briefs_per_cycle` (output limit)

2. Check operational state:
   - Read `state/current-cycle.md` — confirm Scout turn
   - Read `state/agent-health.md` — update heartbeat with current timestamp

3. Load context data:
   - Read `data/narrative-tracker.md` — which narratives were covered and when
   - Read `data/engagement-history.md` — which signal types perform well
   - Scan `handoffs/analytics-to-scout/scores/` (last 3 files) — identify high-performing narrative types

## Step 2: Data Source Scanning

For each monitored source below, fetch signals no older than `scan_interval`:

### X/Twitter Monitoring
- Fetch posts from monitored accounts: `@0xMantle`, `@MantleDevs`, `@MantleTreasury`, `@Bybit_Official`, `@Bybit_Web3`, `@BybitAnnouncements`
- Fetch posts with monitored hashtags: `#Mantle`, `#MantleNetwork`, `#MantleL2`, `#Bybit`, `#BybitWeb3`
- Extract: post text, engagement metrics (replies, retweets, likes), timestamp
- **Flag Bybit conversion signals**: any post about Bybit promotions, MNT listings, trading campaigns, deposit bonuses, or Mantle-Bybit integrations

### Discord Monitoring
- Scan monitored channels for new messages (announcements, dev updates, ecosystem news)
- Extract: message text, channel, timestamp

### Telegram Monitoring
- Scan monitored groups for signals
- Extract: message text, timestamp

### DeFiLlama API
- Query Mantle TVL (total and by protocol)
- Query 24h trading volume
- Check for new protocol listings or major TVL movements (>5%)
- Extract: TVL amount, volume, change %, protocols affected, timestamp

### Mantle Explorer
- Check for major on-chain events: new smart contracts deployed, protocol launches, security incidents
- Check new user wallet creation rate
- Extract: event type, details, timestamp

## Step 3: Signal Scoring

For each signal detected, calculate a relevance score (0-100):

**Scoring factors:**
- **Engagement metrics** (if social): replies + retweets + likes normalized against benchmark
- **On-chain impact** (if blockchain): TVL movement %, new contracts, transaction spike
- **Topic alignment** (all): does signal match `brand/approved-topics.md`?
- **Freshness** (all): newer signals score higher (within scan window)
- **Previous performance** (all): if narrative type has strong Analytics scores, increase weighting
- **Bybit conversion potential** (all): +15 score boost if signal has a natural Bybit signup angle. Triggers: Bybit promotions, MNT trading opportunities, Mantle ecosystem entry points that funnel through Bybit, new Bybit listings related to Mantle, fee discounts, deposit bonuses

**Example rubric:**
- 80-100: Major ecosystem announcement, security incident, 10%+ TVL move, viral engagement (1000+ interactions)
- 60-80: Protocol launch, governance update, significant TVL move (5-10%), strong engagement (200-1000)
- 40-60: Feature update, partnership announcement, moderate TVL move (2-5%), modest engagement (50-200)
- 0-40: General ecosystem update, minor metrics, low engagement

## Step 4: Deduplication & Clustering

1. **Check narrative cooldown:**
   - For each signal, search `data/narrative-tracker.md` for the same narrative topic
   - If found and last cover was <`narrative_cooldown` hours ago: skip signal (unless marked `urgent`)
   - Exception: security incidents, negative sentiment spikes (>5%), TVL drops >10% — skip cooldown

2. **Cluster related signals:**
   - Group signals that describe the same underlying narrative
   - Example: if 3 posts mention "Agni Finance partnership", treat as 1 clustered signal
   - Use the highest-scoring post as representative

## Step 5: Priority Classification

For each signal scoring above `relevance_threshold`:

Assign priority level:
- **urgent**: Security incidents, negative sentiment spikes >5%, TVL drops >15%, major partnership with competing L2
- **high**: Protocol launches, TVL moves 5-10%, governance changes, ecosystem announcements from major protocols
- **normal**: General updates, community highlights, minor TVL moves <5%, technical developments

## Step 6: Brief Generation

For the top `max_briefs_per_cycle` signals (ranked by score):

### Create brief file

Location: `handoffs/scout-to-content/briefs/{YYYY}-{MM}-{DD}T{HH}{MM}-{sequence}-brief.md`

Example: `2026-03-12T1430-001-brief.md`

### Frontmatter

```yaml
---
id: brief-{YYYYMMDD}T{HHMM}-{sequence}
from: scout
to: content
timestamp: {ISO 8601 UTC, now}
cycle: {current cycle number from state/current-cycle.md}
priority: {urgent | high | normal}
status: pending
expires: {ISO 8601 UTC, 6 hours from now}
---
```

### Body Sections

#### Signal Summary
- Plain-language description of what was detected
- Why it matters to Mantle's narrative (e.g., "strengthens Mantle position as leading L2 DeFi platform")
- Suggested engagement angle (e.g., "celebrate partnership with top DeFi protocol")

#### Source Signals
Create a subsection for each data source that contributed to this brief:

**X/Twitter Sources** (if applicable)
- URLs to relevant posts
- Combined engagement: X replies, Y retweets, Z likes
- Dominant sentiment: bullish/neutral/bearish
- Reach estimate

**On-Chain Signals** (if applicable)
- TVL changes: "$X moved, Y% change"
- Protocol: [name] TVL now [amount]
- New contracts deployed: [count]
- Transaction spike: yes/no

**Discord Signals** (if applicable)
- Channel(s) where mentioned
- Community sentiment

**DeFiLlama Signals** (if applicable)
- TVL snapshot: [amount]
- Volume snapshot: [amount]
- Benchmark comparison: [X% above/below average]

#### Recommendation

- **Suggested format**: thread | single-post | discord-announcement
- **Suggested tone**: informational | celebratory | thought-leadership | defensive
- **Optimal engagement window**: "publish within 2 hours for peak engagement"
- **Suggested hashtags**: #Mantle, #DeFi, etc.
- **Account tags**: @0xMantle, @MantleDevs, etc. (if relevant)
- **Bybit conversion angle**: Describe how this signal can naturally lead to a Bybit signup CTA. Options:
  - `ecosystem-gateway`: "Get $MNT on Bybit to participate in [this opportunity]"
  - `trading-opportunity`: "Trade $MNT on Bybit — [catalyst] is driving momentum"
  - `promo-amplify`: "Bybit is running [promo] — sign up to claim [bonus]"
  - `none`: Signal has no natural Bybit conversion angle (still publish, just skip affiliate CTA)

#### Supporting Data

Create a metrics table:

| Metric | Value | Source | Timestamp |
|--------|-------|--------|-----------|
| Mantle TVL | $X million | DeFiLlama | [timestamp] |
| 24h Volume | $X million | DeFiLlama | [timestamp] |
| TVL % Change | +X% | DeFiLlama | [timestamp] |
| [Protocol Name] TVL | $X million | DeFiLlama | [timestamp] |
| [Social Post] Engagement | X interactions | X/Twitter | [timestamp] |

#### Context

- **Related briefs**: "See brief-20260310T1200-001 for previous analysis of this protocol"
- **Performance history**: "DeFi protocol launches have scored 78/100 average engagement in past 3 cycles"
- **Competitive context**: "Other L2s have covered similar announcements; differentiate by emphasizing Mantle's technical advantage"

## Step 7: Update Tracking

1. Append entry to `data/narrative-tracker.md`:
   ```
   | brief-{id} | {timestamp} | {source} | brief-brief | {engagement_window_hours}h |
   ```

2. If this narrative type has strong Analytics scores (>75), note in tracker:
   - "DeFi protocol launches: high performer (avg 78), increase weighting +10%"

## Step 8: Crisis Escalation (Do NOT send to Content)

If you detect **any** of:
- Security incident (contract vulnerability, exploit, hack)
- Negative sentiment spike >5% increase in critical mentions within 1 hour
- Major TVL drop >15% in <1 hour
- Regulatory action or negative news

Then:

1. Create file in `handoffs/scout-to-governance/` (NOT content):
   ```yaml
   ---
   id: crisis-{YYYYMMDD}T{HHMM}-{sequence}
   from: scout
   to: governance
   timestamp: {ISO 8601 UTC}
   cycle: {current cycle}
   priority: urgent
   status: pending
   expires: {ISO 8601 UTC, 1 hour from now}
   ---
   ```

2. Body sections:
   - **Crisis Type**: security | sentiment | market | regulatory
   - **Signal Details**: what was detected, sources, metrics
   - **Recommended Action**: pause publishing | issue statement | monitor
   - **Severity Score**: 0-100

3. Do NOT create a brief for this signal.

## Step 9: Cycle Completion

1. Update heartbeat in `state/agent-health.md`:
   ```
   scout: {current ISO 8601 timestamp}
   ```

2. Log summary to `logs/scout-log.md`:
   ```
   [{timestamp}] scan_complete | signals_scanned: 47, briefs_generated: 2, escalations: 0
   ```

## Error Handling

| Error | Action |
|-------|--------|
| X API unavailable | Log error, retry in 5 min. If persists >30 min, escalate to Governance. |
| DeFiLlama API down | Skip TVL/volume metrics, proceed with social signals. |
| narrative-tracker corrupted | Rebuild from `handoffs/scout-to-content/briefs/` directory listing. |
| Heartbeat write fails | Retry once. Log error and continue. |

## Output Summary

This prompt produces:
- **2-3 briefs** (ranked by score, capped at `max_briefs_per_cycle`)
- **0-1 crisis escalations** (if urgent incident detected)
- **Updated tracking files**: `narrative-tracker.md`, `state/agent-health.md`
- **Log entries**: one summary line per scan

## Quality Checklist

Before finalizing briefs:
- ✓ All signals are above `relevance_threshold`
- ✓ Cooldown violations are skipped (unless urgent)
- ✓ Frontmatter is complete and valid YAML
- ✓ Signal Summary is clear to non-technical reader
- ✓ Recommendation matches signal type and sentiment
- ✓ Supporting Data includes sources and timestamps
- ✓ Crisis signals are routed to Governance, NOT Content
