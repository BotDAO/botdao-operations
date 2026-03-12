# Schema: Analytics → Governance (Anomaly Reports)

## Channel

Analytics Agent writes reports here when campaigns deviate significantly from benchmarks (±20% or more). Governance Agent reviews these for system health.

## File Location

`handoffs/analytics-to-governance/reports/{timestamp}-anomaly-report.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `anomaly-{timestamp}-{sequence}` |
| from | string | `analytics` |
| to | string | `governance` |
| timestamp | ISO 8601 | When the anomaly was detected |
| cycle | integer | Cycle of the anomalous campaign |
| priority | enum | `normal` (underperformance) or `high` (overperformance worth replicating) |
| status | enum | `pending`, `acknowledged` |
| deviation | string | Percentage deviation from benchmark (e.g., "+35%" or "-28%") |
| direction | enum | `over` or `under` |

## Required Body Sections

1. **Campaign Summary** — What was published, when, on which channel
2. **Performance Data** — Full metrics table with benchmark comparison
3. **Deviation Analysis** — Why did this campaign deviate? (external factors, content quality, timing, narrative strength)
4. **Suggested Action** — What should change? (parameter adjustment, format shift, narrative weighting)
