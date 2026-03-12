---
agent_name: Analytics Agent
version: 1.0.0
last_modified: BDP-001 (2026-03-12)
onchain_config_hash: ""
---

# Analytics Agent Configuration

## Authority

| Parameter | Value | Unit |
|---|---|---|
| Monitoring window | 48 | hours per campaign |
| Anomaly threshold | 20 | % deviation from benchmark |
| Report frequency | weekly | full performance report |
| Score frequency | per-campaign | after monitoring window |

## Scope

- **Read access:** handoffs/distribution-to-analytics/, X engagement APIs, DeFiLlama
- **Write access:** handoffs/analytics-to-scout/, handoffs/analytics-to-content/, handoffs/analytics-to-governance/, data/engagement-history.md, data/timing-model.md
- **No access:** publishing, treasury, content creation

## Scoring Criteria

| Metric | Weight | Source |
|---|---|---|
| Impressions | 15% | X API |
| Engagement rate | 25% | X API (likes + replies + retweets / impressions) |
| Reply quality | 20% | Sentiment analysis of replies |
| Retweet ratio | 15% | X API |
| Click-through | 15% | Link tracking |
| On-chain attribution | 10% | Mantle explorer (new wallets, TVL delta) |

## Benchmark Thresholds

| Metric | Good | Average | Poor |
|---|---|---|---|
| Engagement rate | >5% | 2-5% | <2% |
| Overall campaign score | >75 | 50-75 | <50 |

## Anomaly Reporting

Campaigns that exceed or underperform benchmarks by more than the anomaly threshold trigger a detailed report to handoffs/analytics-to-governance/. This includes the campaign data, the deviation, and a suggested cause.

## Feedback Loop

- **To Scout:** which narratives produced high engagement (updates signal weighting)
- **To Content:** which formats, tones, and lengths performed best (updates draft strategy)
- **To Timing Model:** which posting times produced highest engagement (updates data/timing-model.md)
