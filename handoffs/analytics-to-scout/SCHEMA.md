# Schema: Analytics → Scout (Narrative Performance Scores)

## Channel

Analytics Agent writes performance scores here after each campaign's monitoring window. Scout Agent reads these to adjust signal weighting.

## File Location

`handoffs/analytics-to-scout/scores/{timestamp}-narrative-score.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `navscore-{timestamp}-{sequence}` |
| from | string | `analytics` |
| to | string | `scout` |
| timestamp | ISO 8601 | When the score was finalized |
| cycle | integer | Cycle of the scored campaign |
| priority | enum | `normal` |
| status | enum | `pending`, `acknowledged` |
| brief_id | string | ID of the originating Scout brief |
| narrative | string | Short description of the narrative |
| overall_score | integer | 0-100 composite score |

## Required Body Sections

1. **Score Breakdown** — Table of individual metrics (impressions, engagement rate, reply quality, etc.) with scores and weights
2. **Narrative Assessment** — Did this narrative topic perform above or below benchmark? Why?
3. **Recommendation** — Should Scout weight this narrative type higher or lower in future scans?
