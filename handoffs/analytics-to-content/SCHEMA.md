# Schema: Analytics → Content (Format Performance Scores)

## Channel

Analytics Agent writes format performance scores here. Content Agent reads these to optimize draft strategy.

## File Location

`handoffs/analytics-to-content/scores/{timestamp}-format-score.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `fmtscore-{timestamp}-{sequence}` |
| from | string | `analytics` |
| to | string | `content` |
| timestamp | ISO 8601 | When the score was finalized |
| cycle | integer | Cycle of the scored campaign |
| priority | enum | `normal` |
| status | enum | `pending`, `acknowledged` |
| draft_id | string | ID of the originating Content draft |
| format | string | Format type (thread, single-post, etc.) |
| overall_score | integer | 0-100 composite score |

## Required Body Sections

1. **Score Breakdown** — Table of individual metrics with scores
2. **Format Assessment** — How did this format perform compared to historical averages for the same format type?
3. **Tone Assessment** — Did the tone land? Evidence from reply sentiment.
4. **Recommendation** — Specific suggestions for Content Agent (length, structure, tone adjustments)
