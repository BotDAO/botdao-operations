# Schema: Distribution → Analytics (Publish Receipts)

## Channel

Distribution Agent writes a receipt after every successful publish. Analytics Agent reads from this channel to begin monitoring.

## File Location

`handoffs/distribution-to-analytics/receipts/{timestamp}-publish-receipt.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `receipt-{timestamp}-{sequence}` |
| from | string | `distribution` |
| to | string | `analytics` |
| timestamp | ISO 8601 | When the content was published |
| cycle | integer | Current operational cycle number |
| priority | enum | `normal` |
| status | enum | `pending`, `acknowledged`, `completed` |
| draft_id | string | ID of the originating Content draft |
| brief_id | string | ID of the originating Scout brief |
| content_hash | string | SHA-256 hash of the published content |
| onchain_tx | string | Mantle transaction hash for the publish attestation |

## Required Body Sections

1. **Publish Details** — Table with channel, URL/link to published content, exact publish time
2. **Content Summary** — Brief description of what was published (not the full text)
3. **Monitoring Window** — Start and end timestamps for Analytics to monitor (48h default)

## Rules

- One receipt per publish event (if content is cross-posted to multiple channels, write one receipt per channel)
- The content_hash must match the hash of the draft received from Content Agent
