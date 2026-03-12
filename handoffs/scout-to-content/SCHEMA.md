# Schema: Scout → Content (Narrative Briefs)

## Channel

Scout Agent writes briefs here when it detects a narrative worth covering. Content Agent reads from this channel.

## File Location

`handoffs/scout-to-content/briefs/{timestamp}-brief.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `brief-{timestamp}-{sequence}` |
| from | string | `scout` |
| to | string | `content` |
| timestamp | ISO 8601 | When the brief was created |
| cycle | integer | Current operational cycle number |
| priority | enum | `normal`, `high`, or `urgent` |
| status | enum | `pending`, `acknowledged`, `completed`, `expired` |
| expires | ISO 8601 | Deadline for Content to act (engagement window) |

## Required Body Sections

1. **Signal Summary** — What was detected, in plain language
2. **Source Signals** — Subsections per source (X/Social, On-Chain, Discord, etc.) with platform, signal description, and detection timestamp
3. **Recommendation** — Suggested format, tone, and engagement window
4. **Supporting Data** — Table of relevant metrics (TVL, volume, change %, etc.)
5. **Context** — Related previous briefs and analytics references

## Status Updates

- Content Agent updates frontmatter to `status: acknowledged` when it begins drafting
- Content Agent updates to `status: completed` and adds `completed_by: [draft filename]` when the draft is written
