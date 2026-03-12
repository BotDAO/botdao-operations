# Schema: Content → Distribution (Drafts)

## Channel

Content Agent writes approved drafts here. Distribution Agent reads from this channel and publishes.

## File Location

`handoffs/content-to-distribution/drafts/{timestamp}-{format}-draft.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `draft-{timestamp}-{sequence}` |
| from | string | `content` |
| to | string | `distribution` |
| timestamp | ISO 8601 | When the draft was finalized |
| cycle | integer | Current operational cycle number |
| priority | enum | `normal`, `high`, `urgent` |
| status | enum | `pending`, `acknowledged`, `completed`, `expired` |
| expires | ISO 8601 | End of engagement window |
| brief_id | string | ID of the originating Scout brief |
| format | enum | `thread`, `single-post`, `discord-announcement`, `long-form` |
| confidence | integer | Self-score 0-100 (must be ≥70 to send) |
| review_recommended | boolean | True if topic is in "approved with caution" list |

## Required Body Sections

1. **Content** — The exact text to publish (Distribution cannot modify this)
2. **Publishing Notes** — Target channel(s), any timing preferences, hashtags
3. **Brief Reference** — Link to the originating Scout brief

## Rules

- Drafts with `confidence` below 70 must not be sent to this channel
- Drafts with `review_recommended: true` should be flagged for Governance Agent review before Distribution publishes
- Distribution Agent publishes the content exactly as written — no modifications
