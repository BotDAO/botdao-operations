---
prompt_name: Publish Flow
agent: distribution
trigger: draft_received
description: Step-by-step publishing workflow from draft to live post
---

# Publish Flow

## When to Run
When a new draft appears in `handoffs/content-to-distribution/drafts/` with `status: pending`.

## Steps

### 1. Validate Draft
- Read the draft file fully
- Confirm all required frontmatter fields are present
- Check `review_recommended` flag. If true, hold for Governance review (write escalation to `handoffs/governance-to-all/`)
- Confirm content_type matches a supported platform

### 2. Check Timing
- Read `data/timing-model.md` for optimal posting windows
- Read `agents/distribution/config.md` for publish_window and min_spacing
- If current time is outside the publish window, hold until next window opens
- If a post was published less than min_spacing ago, wait
- If daily post count has hit max_posts_per_day, hold until tomorrow

### 3. Platform Selection
Based on content_type in the draft:
- thread or single: publish to X/Twitter
- long-form or announcement: publish to Discord
- If draft suggests both: publish to primary platform first, secondary after min_spacing

### 4. Publish
- Format content for the target platform
- Publish via the appropriate MCP tool (twitter-publish for X, discord for Discord)
- Record the published post URL/ID
- Generate content_hash for on-chain attestation (if enabled)

### 5. On-Chain Attestation
If on-chain publishing is enabled:
- Submit content_hash to the Mantle attestation contract
- Record the transaction hash

### 6. Write Analytics Handoff
Create a publish receipt in `handoffs/distribution-to-analytics/receipts/` following the SCHEMA.md:
- Include post URL, platform, content_hash, publish timestamp
- Set monitoring_window per config (default: 48 hours)
- Set status to pending

### 7. Update State
- Mark the original draft as `status: completed`
- Update `logs/publish-log.md` with the new publish event
- Update `state/agent-health.md` with heartbeat

## Error Handling
- If publishing fails: retry once after 60 seconds. If still fails, hold draft and note error in heartbeat.
- If on-chain attestation fails: publish anyway, flag for manual attestation later
- If all daily slots used: queue draft for next day, do not drop it
