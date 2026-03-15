---
prompt_name: Long-Form Content Draft Generation
agent: Content
trigger: brief_processed_longform
description: Instructions for drafting longer-form content (Discord announcements, detailed analyses, blog-style posts). Different structure from X threads.
---

# Long-Form Content Draft Writing Instructions

## Overview

When Scout provides a brief recommending long-form format (e.g., Discord announcements, detailed ecosystem analysis, blog-style posts), this prompt guides the Content Agent to write substantive content that educates and engages the community at depth.

## Important Note

**Long-form content is disabled for Milestone 1.** This prompt is provided for future reference and will be activated after Milestone 1 completion. Do not use this prompt until explicitly enabled via governance update.

## Prerequisites

- Brief has been read and analyzed
- Brief's `status` has been updated to `acknowledged`
- Brief recommends long-form format (not thread/single-post)
- `long_form_enabled` flag in governance is set to `true`
- Content exceeds X's 280-character limit and benefits from depth

## When to Use Long-Form

**Recommended use cases**:

1. **Discord announcements** (500-800 words)
   - Major ecosystem partnership
   - Community call to action (governance vote, feedback request)
   - Educational announcement (protocol feature, upgrade)

2. **Detailed analyses** (1000-2000 words)
   - Deep-dive on DeFi trend relevant to Mantle
   - Thought-leadership on L2 scaling or ecosystem design
   - Post-mortem analysis of market event

3. **Blog posts** (1500-3000 words)
   - Technical deep-dives (only if non-confidential)
   - Quarterly ecosystem report
   - Strategic roadmap explanation

## Step 1: Set Up Draft Metadata

Generate unique draft ID:
```
draft-{YYYYMMDD}T{HHMM}-{sequence}
```

Create draft file:

**Location**: `handoffs/content-to-distribution/drafts/{YYYY}-{MM}-{DD}T{HH}{MM}-{sequence}-longform-draft.md`

## Step 2: Write Frontmatter

```yaml
---
id: draft-{YYYYMMDD}T{HHMM}-{sequence}
from: content
to: distribution
timestamp: {ISO 8601 UTC}
cycle: {current cycle number}
priority: {normal | high | urgent}
status: pending
expires: {ISO 8601 UTC, 6 hours from now}
brief_id: {Scout brief ID}
format: long-form
content_type: {discord-announcement | analysis | blog-post}
word_count: {approximate}
confidence: {0-100, your self-score}
review_recommended: {true if "approved with caution" topic, false}
---
```

## Step 3: Plan Content Structure

Determine content type and structure:

### Type 1: Discord Announcement (500-800 words)

**Structure**:
1. Hook (1 paragraph): What happened? Why should readers care?
2. Key facts (3-4 paragraphs): Details, background, importance
3. What it means (2 paragraphs): Implications for Mantle community
4. Call-to-action (1 paragraph): What should readers do?

**Example outline for partnership announcement**:
- Hook: "Mantle just announced partnership with [Protocol]"
- Facts: Why they partnered, what they're building, expected benefits
- Implications: What this means for users, for ecosystem
- CTA: "Join us in Discord discussion" or "Support this initiative"

### Type 2: Detailed Analysis (1000-2000 words)

**Structure**:
1. Executive summary (2 paragraphs)
2. Context (3-4 paragraphs): Background, market conditions
3. Deep analysis (5-8 paragraphs): Detailed examination
4. Implications (3-4 paragraphs): What it means for Mantle
5. Call-to-action or closing (1-2 paragraphs)

**Example outline for DeFi trend analysis**:
- Summary: "The rise of intent-based architectures is reshaping DeFi"
- Context: Historical DeFi design patterns, current limitations
- Analysis: How intent-based systems work, benefits, risks
- Implications: How Mantle can leverage this trend
- CTA: "Learn more / join discussion"

### Type 3: Blog Post (1500-3000 words)

**Structure**:
1. Introduction (2-3 paragraphs): Hook, thesis, preview
2. Background sections (3-5 paragraphs each): Deep context
3. Main analysis (8-15 paragraphs): Core content
4. Implications (3-4 paragraphs): Significance
5. Conclusion (2-3 paragraphs): Summary and forward-looking statement

## Step 4: Research and Outline

1. **Extract key points** from Scout brief's supporting data
2. **Identify authoritative sources** (DeFiLlama, explorer data, official announcements)
3. **Create detailed outline** (3-5 sentences per section)
4. **Verify all claims** against source documents

## Step 5: Write the Content

### Writing Guidelines

**Tone** (should match brand guidelines for longer content):
- Professional but accessible (explain jargon for non-experts)
- Authoritative but conversational (not academic or robotic)
- Celebratory when appropriate (avoid hype, maintain credibility)

**Structure within body**:
- Use headers to break up sections (H2 or H3)
- Keep paragraphs to 3-4 sentences max
- Use bullet points for lists or complex ideas
- Use bold text to highlight key terms

**Word count management**:
- Discord announcement: 500-800 words (tight, scannable)
- Analysis: 1000-2000 words (thorough but not exhaustive)
- Blog post: 1500-3000 words (comprehensive, editorial)

### Example Discord Announcement

```markdown
## 🎉 Agni Finance Partners with Mantle: What This Means for You

### Why This Matters

Agni Finance, one of the top DeFi protocols in the industry, just announced a strategic partnership with Mantle Network. This is a major validation of Mantle's infrastructure and opens new opportunities for our community.

### What They Bring

Agni manages over $50M in TVL across multiple chains and serves thousands of traders daily. Their routing algorithms and liquidity pools are top-tier. With this partnership, you'll get access to deeper markets and better execution on Mantle.

### What You Get

- **Better swaps**: Agni's routing optimizes your execution price
- **Lower slippage**: More liquidity = smoother trades
- **Incentives**: Agni is bootstrapping liquidity with rewards for early adopters
- **More protocols**: This opens the door for additional tier-1 protocols to build on Mantle

### Timeline

Launching [date]. Full details in the announcement post below.

### Join the Conversation

Have questions? Let's discuss in #ecosystem-partnerships. Want to get started? See #getting-started for instructions.
```

## Step 6: Self-Score the Draft

Use same 6-dimension rubric as thread drafts, but calibrate for longer content:

### Dimension 1: Brand Alignment (25% weight)
- Does the piece maintain consistent voice over longer format?
- Does tone match brand guidelines for educational/thought-leadership?
- Are messaging pillars reinforced throughout?

### Dimension 2: Clarity (20% weight)
- Is the main thesis clear within first 2 paragraphs?
- Are technical concepts explained for non-experts?
- Do section headers guide the reader?

### Dimension 3: Engagement Potential (20% weight)
- Would community members want to share this?
- Does it provoke thoughtful discussion (not just reactions)?
- Is there a clear call-to-action?

### Dimension 4: Accuracy (15% weight)
- Is every claim verifiable from brief's supporting data?
- Are quotes attributed?
- Are statistics sourced?

### Dimension 5: Timing Fit (10% weight)
- Does content fit the engagement window?
- Is timing-sensitive information current?

### Dimension 6: Compliance (10% weight)
- No financial advice or promises
- No disparagement of competitors
- No unverified technical claims
- Approved topics only

**Calculate confidence** using same weighted formula as threads.

## Step 7: Brand Compliance Check

Before finalizing:

### Voice Alignment
- ✓ Tone is professional and authoritative
- ✓ Language is accessible (explains jargon)
- ✓ Matches brand guidelines for longer writing

### Topic Approval
- ✓ Topic is in `brand/approved-topics.md`
- ✓ If "approved with caution": set `review_recommended: true`

### Prohibited Content
- ✗ No financial advice ("You should invest X% in Mantle")
- ✗ No promises of returns ("This will generate 10x")
- ✗ No disparagement ("Arbitrum's design is flawed")
- ✗ No unverified claims ("Mantle can process 1M TPS")

## Step 8: Revision Loop

If confidence < 70:

1. Identify lowest-scoring dimension
2. Rewrite that section to improve score
3. Re-score all dimensions
4. Repeat up to `revision_limit` times

If still below 70 after revisions:
- Do NOT send
- Create escalation to Governance

## Step 9: Write Body Sections

### Body Section 1: Content

The full long-form text. Organize with headers:

```markdown
## Content

## 🎉 Agni Finance Partners with Mantle: What This Means for You

### Why This Matters

[Content here...]

### What They Bring

[Content here...]

### What You Get

[Content here...]

### Timeline

[Content here...]

### Join the Conversation

[Content here...]
```

### Body Section 2: Publishing Notes

```markdown
## Publishing Notes

**Target Channel**: Discord #announcements

**Alternative Channels**:
- X/Twitter thread (if re-posting)
- Blog (if full blog post)

**Cross-Post?**: Yes, as X thread (Content Agent or Distribution handles this)

**Include in Weekly Summary?**: Yes (include brief paragraph)
```

### Body Section 3: Brief Reference

```markdown
## Brief Reference

**Originating Brief**: brief-20260312T1430-001

**Brief Format Recommendation**: Long-form / Discord announcement

**Alignment**: Provides in-depth explanation of partnership (brief was summary-level)
```

## Step 10: Format for Distribution

### Discord Announcement Format

If publishing to Discord:
- Use Discord markdown (bold, italics, code blocks)
- Include relevant emoji (not excessive)
- Break into scannable sections with headers
- Keep paragraphs short (2-3 sentences)

### Blog Post Format

If publishing to blog:
- Use standard markdown headers (H1, H2, H3)
- Include metadata (author, date, category)
- Add table of contents for long posts (2000+ words)
- Include byline or attribution

### X/Twitter Thread Format

If cross-posting to X:
- Break into tweet-length chunks (280 chars each)
- Number tweets (1/, 2/, 3/, etc.)
- Maintain flow when split into tweets

## Step 11: Final Validation

### Content Validation
- ✓ Word count matches stated range
- ✓ No prohibited content
- ✓ All statistics verified
- ✓ Tone consistent throughout
- ✓ Headers guide reader logic
- ✓ CTA is clear

### Compliance Validation
- ✓ No financial advice
- ✓ No promises or guarantees
- ✓ Approved topics only
- ✓ Brand voice maintained

### Format Validation
- ✓ Proper markdown syntax
- ✓ Headers are hierarchical (H2 > H3, not H1 > H3)
- ✓ Links are properly formatted and verified
- ✓ No broken references

## Step 12: Handle Low-Confidence Drafts

If confidence < 70 after revisions:

Create escalation in `handoffs/content-to-governance/`:

```yaml
---
id: esc-content-{timestamp}-{sequence}
from: content
to: governance
timestamp: {ISO 8601 UTC}
cycle: {current cycle}
priority: normal
status: pending
---

## Low-Confidence Long-Form Draft

**Brief ID**: {brief ID}
**Draft ID**: {your draft ID}
**Confidence Score**: {score}
**Weak Dimensions**: [list]
**Request**: [Approve anyway / Reject / Provide guidance]
```

## Step 13: Update Brief Status & Log

1. Update brief: `status: completed`, add `completed_by: drafts/{filename}`
2. Log: `[timestamp] longform_draft_created | draft-ID | confidence: score`
3. Update heartbeat in `state/agent-health.md`

## Step 14: Send to Distribution

If confidence ≥70:

Write file to: `handoffs/content-to-distribution/drafts/{timestamp}-longform-draft.md`

## Output

One file per long-form draft:

**File**: `handoffs/content-to-distribution/drafts/{timestamp}-longform-draft.md`

**Characteristics**:
- Confidence ≥70
- 500-3000 words (depending on content type)
- On-brand, accurate, compliant
- Properly formatted for target channel (Discord/blog/X)
- Ready for Distribution Agent to publish without modification

## Quality Checklist

Before sending:
- ✓ Confidence ≥70
- ✓ Word count in target range
- ✓ All claims verified
- ✓ Tone consistent
- ✓ No prohibited content
- ✓ Brand guidelines followed
- ✓ CTA is clear
- ✓ Proper markdown formatting
- ✓ Headers are hierarchical
- ✓ Links are valid

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Too much jargon for general audience | Add plain-language explanations |
| No clear main thesis | Rewrite intro to state thesis in first 2 paragraphs |
| Rambling organization | Restructure with clear headers; each section should have topic sentence |
| Missing call-to-action | Add explicit CTA in final section |
| Unverified claims | Go back to brief and source every stat |
| Excessive length | Cut sections that don't advance main thesis |
| Tone inconsistency | Check each paragraph against brand guidelines |

## Disabled Until Milestone 2

This prompt is template-ready but **disabled for Milestone 1**. To enable:

1. Governance Agent must approve via PR to `agents/content/config.md`
2. Add flag: `long_form_enabled: true`
3. Update Content Agent SKILL.md to include long-form workflow
4. Scout and Distribution agents must be updated to handle long-form format

Until then, Content Agent should only draft threads and single-posts.
