---
prompt_name: Long-Form Draft
agent: content
trigger: brief_with_long_form_angle
description: Draft longer content like Discord announcements or detailed analyses
---

# Long-Form Draft

## When to Run
When a Scout brief suggests a narrative better suited for long-form content (Discord announcement, detailed analysis, or blog-style post) rather than an X thread.

## Before Writing
1. Read the brief fully
2. Read `brand/voice-guidelines.md` for tone rules
3. Read `brand/approved-topics.md` to confirm topic is allowed
4. Read `brand/templates/discord-announcement.md` for Discord format
5. Read `data/engagement-history.md` for what long-form formats work

## Writing Process

### Step 1: Pick Format
Based on the narrative:
- Discord announcement: community-facing news, ecosystem updates
- Detailed analysis: data-heavy deep dive, protocol comparison
- Blog-style: thought leadership, trend analysis

### Step 2: Draft Structure
- Title: clear and specific, no clickbait
- Opening paragraph: what happened and why it matters (3-4 sentences)
- Body sections: 2-4 sections with subheadings, each covering one aspect
- Data section: key metrics in a clear format
- Closing: what this means going forward, call to action

### Step 3: Apply Brand Voice
Same rules as thread drafts:
- Data-driven, not hype
- Professional but accessible
- Every claim backed by data
- No prohibited language (check voice guidelines)

### Step 4: Self-Score and Decide
Same 6-dimension scoring as thread-draft.md. Same threshold and revision rules apply.

## Output
Write to `handoffs/content-to-distribution/drafts/` with `content_type: long-form` in frontmatter. Follow `handoffs/content-to-distribution/SCHEMA.md`.
