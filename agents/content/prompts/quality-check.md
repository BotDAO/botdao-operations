---
prompt_name: Quality Check
agent: content
trigger: before_handoff
description: Pre-handoff checklist for every draft before sending to Distribution
---

# Quality Check

## When to Run
Run this checklist on every draft before writing it to `handoffs/content-to-distribution/drafts/`. No exceptions.

## Checklist

### Brand Compliance
- [ ] Tone matches voice-guidelines.md (data-driven, not hype)
- [ ] No words from the "do not use" list
- [ ] Hashtag usage follows policy
- [ ] Topic is in approved-topics.md (not in "never" list)
- [ ] If topic is "with caution", extra care taken

### Factual Accuracy
- [ ] Every number has a source
- [ ] No claims without supporting data
- [ ] Dates and timestamps are correct
- [ ] Protocol names and ticker symbols are accurate
- [ ] Links (if any) are valid

### Structural Quality
- [ ] Hook tweet grabs attention (for threads)
- [ ] One idea per tweet (for threads)
- [ ] CTA is clear and actionable
- [ ] Thread length within config limit
- [ ] No orphan tweets that do not connect to the narrative

### Technical
- [ ] Frontmatter has all required fields per SCHEMA.md
- [ ] brief_id references the correct source brief
- [ ] confidence_score is calculated and recorded
- [ ] review_recommended flag is set correctly
- [ ] status is set to "pending"

### Final Gate
- If any box unchecked: fix before proceeding
- If confidence score < threshold after fixes: set review_recommended to true
- Log the quality check result in your heartbeat update
