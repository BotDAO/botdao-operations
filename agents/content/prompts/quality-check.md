---
prompt_name: Content Draft Quality Assurance
agent: Content
trigger: pre_handoff
description: Self-review checklist that Content Agent runs on every draft before sending to Distribution. Validates confidence scoring, brand compliance, and technical requirements.
---

# Quality Assurance Checklist for Content Drafts

## Overview

Before Content Agent sends any draft to Distribution, this checklist ensures the draft meets minimum quality and compliance standards. This is the final gate before content is published to the world.

**Important**: Every draft must pass this checklist before entering the `handoffs/content-to-distribution/drafts/` channel. Low-confidence drafts should be escalated to Governance instead.

## Section 1: Confidence Score Validation

### 1.1 Verify Confidence Calculation

Open the draft file and check the confidence score calculation:

**For X threads**:
```
confidence = (
  (brand_alignment × 0.25) +
  (clarity × 0.20) +
  (engagement × 0.20) +
  (accuracy × 0.15) +
  (timing × 0.10) +
  (compliance × 0.10)
)
```

**For long-form**:
Same formula (weights are identical).

**For single-posts**:
Same formula (weights are identical).

**Action**:
- ✓ Recalculate manually if any dimension seems off
- ✓ If calculation error found, correct it
- ✓ If corrected score is <70, do not proceed to Distribution
- ✓ If calculation is correct, proceed

### 1.2 Verify Confidence ≥ 70

Check draft's frontmatter:

```yaml
confidence: {your_score}
```

**Action**:
- ✓ If confidence ≥70: continue to Section 2
- ✗ If confidence <70: do NOT proceed
  - Option A: Revise draft to improve score (if not at revision limit)
  - Option B: Escalate to Governance (if at revision limit)

## Section 2: Frontmatter Validation

### 2.1 Check Required Fields

Verify all required fields are present and correctly formatted:

| Field | Expected | Status |
|-------|----------|--------|
| `id` | `draft-{YYYYMMDD}T{HHMM}-{sequence}` | [ ] ✓ |
| `from` | `content` | [ ] ✓ |
| `to` | `distribution` | [ ] ✓ |
| `timestamp` | ISO 8601 UTC | [ ] ✓ |
| `cycle` | integer | [ ] ✓ |
| `priority` | normal \| high \| urgent | [ ] ✓ |
| `status` | `pending` | [ ] ✓ |
| `expires` | ISO 8601 UTC (6h from now) | [ ] ✓ |
| `brief_id` | Valid brief ID | [ ] ✓ |
| `format` | thread \| single-post \| discord-announcement \| long-form | [ ] ✓ |
| `confidence` | 0-100 integer, ≥70 | [ ] ✓ |
| `review_recommended` | true \| false | [ ] ✓ |

**Action**:
- ✓ All fields present and valid: continue to Section 3
- ✗ Missing field or invalid value: fix and re-check

### 2.2 Verify YAML Syntax

Parse the frontmatter as YAML:

**Action**:
- ✓ No syntax errors: continue to Section 3
- ✗ Syntax error (missing colon, bad indentation, etc.): fix it

## Section 3: Content Validation

### 3.1 Verify Draft Has All Required Sections

**For thread drafts**:
- [ ] ✓ Content section (numbered tweets)
- [ ] ✓ Publishing Notes section
- [ ] ✓ Brief Reference section

**For single-post drafts**:
- [ ] ✓ Content section (single tweet)
- [ ] ✓ Publishing Notes section
- [ ] ✓ Brief Reference section

**For long-form drafts**:
- [ ] ✓ Content section (full formatted text)
- [ ] ✓ Publishing Notes section
- [ ] ✓ Brief Reference section

**Action**:
- ✓ All sections present: continue to Section 4
- ✗ Missing section: add it before proceeding

### 3.2 Verify Content Accuracy

For each factual claim in the draft:

1. **Find source** in the Scout brief
2. **Verify match** between draft and brief
3. **Check for exaggeration** (is claim accurately portrayed?)
4. **Check for misquoting** (if quoting announcement, is it word-for-word?)

**Example verification**:
- Draft: "Agni Finance manages $50M in TVL"
- Brief source: "DeFiLlama: Agni TVL = $50M (timestamp)"
- Status: ✓ Verified

**Action**:
- ✓ All claims verified: continue to Section 4
- ✗ Claim not in brief: remove or flag as uncertain
- ✗ Claim contradicts brief: correct immediately
- ✗ Exaggeration detected: tone down

### 3.3 Verify Character/Word Limits

**For X threads**:
Each tweet must be ≤280 characters.

**Action**:
- Count characters in each tweet (including spaces, hashtags, URLs)
- If any tweet >280 chars: edit to reduce length
- Acceptable length reductions: abbreviate, remove adjectives, use links instead of text

**Example**:
```
Original (295 chars): "Agni Finance, which is one of the leading DeFi aggregators in the ecosystem, just announced..."
Shortened (276 chars): "Agni Finance, a leading DeFi aggregator, just announced..."
```

**For long-form**:
Check draft's frontmatter for `word_count`:
- Discord announcement: 500-800 words
- Analysis: 1000-2000 words
- Blog post: 1500-3000 words

**Action**:
- Use word processor to count actual words
- If under target: add substance to weak sections
- If over target: cut least essential content

**For single-post**:
Must be ≤280 characters (same as thread tweets).

## Section 4: Brand Compliance Check

### 4.1 Tone Alignment

Read `brand/voice-guidelines.md` and check:

**Tone elements**:
- [ ] ✓ Language level is appropriate (not too technical, not condescending)
- [ ] ✓ Attitude matches brand (confident, professional, celebratory when appropriate)
- [ ] ✓ No contradictions with organizational messaging
- [ ] ✓ Vocabulary matches Mantle's brand (confident, technical but accessible)

**Action**:
- ✓ Tone matches: continue to 4.2
- ✗ Tone mismatch: rewrite relevant sections

**Examples of tone issues**:
| Issue | Example | Fix |
|-------|---------|-----|
| Too technical | "XVM opcodes enable gas optimization" | "Lower gas fees through technical improvements" |
| Too casual | "Agni is gonna moon bro" | "Agni is poised to drive ecosystem growth" |
| Condescending | "For those new to DeFi..." | "For the DeFi community..." |
| Arrogant | "Mantle is superior to all other L2s" | "Mantle offers distinct advantages for DeFi" |

### 4.2 Topic Approval

Open `brand/approved-topics.md`:

1. **Is the topic listed?**
   - [ ] ✓ Yes, in approved list
   - [ ] ✓ Yes, in "approved with caution" list
   - [ ] ✗ No, topic is not listed

**Action**:
- ✓ Topic is approved: continue to 4.3
- ✓ Topic is approved with caution: verify `review_recommended: true` is set in frontmatter, then continue to 4.3
- ✗ Topic is not approved: DO NOT SEND. Escalate to Governance instead.

### 4.3 Prohibited Content Check

Scan draft for any of these:

**Financial Advice Prohibited**:
- ✗ "You should buy Mantle" / "Invest X% in this"
- ✗ "This will make you money" / "Guaranteed returns"
- ✗ "This is a safe investment"

**Investment Promises Prohibited**:
- ✗ "This will 10x" / "Moon incoming"
- ✗ "You'll make your money back in 3 months"
- ✗ "Stake here for yields" (if promising specific returns)

**Competitor Disparagement Prohibited**:
- ✗ "Arbitrum is inferior"
- ✗ "Optimism's design is flawed"
- ✗ Comparative claims that frame competitors negatively

**False/Unverified Technical Claims Prohibited**:
- ✗ "Mantle can process 1M TPS" (if not verified in brief)
- ✗ "Mantle is completely decentralized" (if not confirmed)
- ✗ Claims about security if not audit-verified

**Action**:
- ✓ No prohibited content found: continue to 4.4
- ✗ Prohibited content found: remove it immediately and re-verify compliance

### 4.4 Hashtag and Mention Check

**For X posts**:

Verify hashtags are on-brand:
- [ ] ✓ #Mantle (primary)
- [ ] ✓ #DeFi, #L2, #Ethereum (contextual)
- [ ] ✗ #Crypto (avoid generic tags)
- [ ] ✗ Hashtags from brief that don't align with brand

**For mentions**:
- [ ] ✓ @MantleNetwork (primary account)
- [ ] ✓ @MantleDevs (if development-related)
- [ ] ✓ Partner handles if relevant (e.g., @AgniFinance for partnership announcement)
- [ ] ✗ Mentions not verified in brief

**Action**:
- ✓ Hashtags/mentions verified: continue to Section 5
- ✗ Incorrect hashtags: revise to on-brand set
- ✗ Unverified mentions: remove or verify in brief

## Section 5: Format-Specific Checks

### 5.1 If Format = Thread

**Checklist**:
- [ ] ✓ Each tweet ≤280 characters
- [ ] ✓ Tweets are numbered (1/, 2/, etc.)
- [ ] ✓ Thread flows logically (tweet N → tweet N+1)
- [ ] ✓ Hook tweet (1st) is compelling
- [ ] ✓ Final tweet has clear CTA or closing
- [ ] ✓ Total tweets ≤ max_thread_length from config
- [ ] ✓ Thread can be read as standalone (context clear without external knowledge)

**Action**:
- ✓ All checks pass: continue to Section 6
- ✗ Tweet exceeds 280 chars: edit
- ✗ Logic broken: reorder or rewrite tweets
- ✗ No CTA: add to final tweet
- ✗ Too long: cut weakest tweets

### 5.2 If Format = Single-Post

**Checklist**:
- [ ] ✓ Text ≤280 characters
- [ ] ✓ Hook is strong (first sentence grabs attention)
- [ ] ✓ All necessary context in one tweet
- [ ] ✓ Clear CTA or next step
- [ ] ✓ Includes relevant hashtags

**Action**:
- ✓ All checks pass: continue to Section 6
- ✗ Text exceeds 280: edit ruthlessly
- ✗ No hook: rewrite opening
- ✗ Missing context: convert to thread instead
- ✗ No CTA: add one

### 5.3 If Format = Discord Announcement

**Checklist**:
- [ ] ✓ Uses proper Discord markdown (bold, italics, code blocks)
- [ ] ✓ Emoji are present but not excessive (2-3 per section)
- [ ] ✓ Sections have headers
- [ ] ✓ Paragraphs are short (2-3 sentences max)
- [ ] ✓ Content is scannable (not wall of text)
- [ ] ✓ Includes channel cross-references (#channel-name)
- [ ] ✓ CTA is clear (e.g., "join discussion in #announcements")

**Action**:
- ✓ All checks pass: continue to Section 6
- ✗ Poor formatting: restructure with headers and whitespace
- ✗ Wall of text: break into paragraphs
- ✗ No CTA: add explicit next step

### 5.4 If Format = Long-Form

**Checklist**:
- [ ] ✓ Word count matches target range
- [ ] ✓ Has clear main thesis (stated in first 2 paragraphs)
- [ ] ✓ Sections have headers (hierarchical: H2 > H3, not H1 > H3)
- [ ] ✓ Paragraphs are 3-4 sentences max
- [ ] ✓ Transitions between sections are smooth
- [ ] ✓ Jargon is explained (accessible to non-experts)
- [ ] ✓ Conclusion summarizes and provides forward-looking statement
- [ ] ✓ CTA is present

**Action**:
- ✓ All checks pass: continue to Section 6
- ✗ Thesis unclear: rewrite opening
- ✗ Headers not hierarchical: fix structure
- ✗ Too much jargon: add plain-language explanations
- ✗ No conclusion: add summary + forward-looking statement

## Section 6: Brief Reference Validation

### 6.1 Verify Brief ID Exists

**Action**:
1. Open the brief file: `handoffs/scout-to-content/briefs/{brief_id}.md`
2. Confirm it exists and is not expired
3. Confirm draft's `brief_id` matches the file's `id` field

**If brief not found**:
- ✗ Do NOT send draft
- Escalate: "Draft references invalid brief ID"

### 6.2 Verify Draft Aligns With Brief

**Action**:
1. Read brief's "Recommendation" section
2. Check: Does draft match recommended format? Tone? Timing window?

| Element | Brief Says | Draft Does | Status |
|---------|-----------|-----------|--------|
| Format | Thread | Draft is thread | ✓ |
| Tone | Celebratory | Tone is celebratory | ✓ |
| Window | Publish by 16:30 UTC | Ready to publish | ✓ |

**If misalignment found**:
- Edit draft to match brief's recommendation, OR
- Document reason for deviation in Publishing Notes

## Section 7: Publishing Notes Check

### 7.1 Verify Publishing Notes Are Complete

**Action**:
Confirm Publishing Notes section includes:
- [ ] ✓ Target channel (e.g., "@MantleNetwork")
- [ ] ✓ Publishing timing preference (ASAP, scheduled, etc.)
- [ ] ✓ Hashtags (if X post)
- [ ] ✓ Mentions/tags (if relevant)
- [ ] ✓ Cross-post instructions (if multi-channel)
- [ ] ✓ Any special notes for Distribution Agent

**If incomplete**:
- Add missing details

## Section 8: Final Review Checklist

Before marking draft as ready for Distribution:

```
DRAFT QUALITY ASSURANCE - FINAL CHECKLIST
==========================================

Confidence & Frontmatter:
[ ] Confidence ≥70
[ ] All required frontmatter fields present
[ ] YAML syntax valid
[ ] Format field matches draft type

Content:
[ ] All required sections present
[ ] All factual claims verified against brief
[ ] No prohibited content
[ ] Character/word limits met

Brand Compliance:
[ ] Tone matches voice guidelines
[ ] Topic is approved (or approved with caution)
[ ] Hashtags/mentions are on-brand
[ ] No financial advice, promises, or disparagement

Format-Specific:
[ ] [If thread] All tweets ≤280 chars, numbered, logical flow
[ ] [If single-post] ≤280 chars, hook strong, CTA present
[ ] [If long-form] Word count correct, headers hierarchical, thesis clear
[ ] [If discord] Markdown proper, scannable, emoji appropriate

Handoff Quality:
[ ] Brief reference is valid
[ ] Draft aligns with brief recommendation
[ ] Publishing Notes are complete
[ ] Ready for Distribution to publish without modification

FINAL DECISION:
[ ] APPROVED - Send to Distribution
[ ] NEEDS REVISION - Revise and re-check
[ ] ESCALATE - Cannot meet confidence threshold; send to Governance
```

## Section 9: Decision Point

### Scenario A: All Checks Pass

**Action**:
1. Mark draft as `status: pending` in frontmatter (already set)
2. Write draft file to `handoffs/content-to-distribution/drafts/{filename}.md`
3. Update brief: `status: completed`, add `completed_by: drafts/{filename}.md`
4. Log: `[timestamp] draft_sent | {draft_id} | confidence: {score} | to distribution`
5. Update heartbeat in `state/agent-health.md`

**Result**: Draft is now in Distribution Agent's queue for publishing.

### Scenario B: Issues Found But Fixable

**Action**:
1. Identify issue(s)
2. Revise draft
3. Re-score confidence (if content changed)
4. Re-run this checklist from Section 1
5. If still <70 or revision limit reached: go to Scenario C

**Result**: Revised draft is ready for Distribution (or escalation).

### Scenario C: Cannot Meet Standards

**Conditions**:
- Confidence <70 after all revisions
- Revision limit reached (config: `revision_limit`)
- Prohibited content cannot be removed
- Topic not in approved list

**Action**:
1. Create escalation file: `handoffs/content-to-governance/esc-{timestamp}-{sequence}.md`
2. Frontmatter:
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
   ```
3. Body:
   ```markdown
   ## Escalation: Content Draft Cannot Meet Quality Threshold

   **Brief ID**: {brief_id}
   **Draft ID**: {draft_id}
   **Confidence Score**: {score}
   **Revision Attempts**: {number}/{revision_limit}

   **Reason for Escalation**:
   [Identify lowest-scoring dimensions or why confidence cannot be improved]

   **Options**:
   1. Approve as-is despite low confidence
   2. Reject brief and request Scout re-signal
   3. Provide guidance on content adjustment
   ```

4. **Do NOT send draft to Distribution**
5. Wait for Governance response

**Result**: Governance Agent decides next action (approve anyway, reject, request revision).

## Quality Assurance Log

After completing QA for a draft, log the result:

```
[{timestamp}] qa_check_complete | {draft_id} | {result} | {notes}
```

Examples:
```
[2026-03-12T15:15:00Z] qa_check_complete | draft-20260312T1510-001 | approved | all checks passed, confidence 87
[2026-03-12T15:20:00Z] qa_check_complete | draft-20260312T1520-001 | revision | tweets exceeded 280 chars, edited and re-scored 82
[2026-03-12T15:30:00Z] qa_check_complete | draft-20260312T1530-001 | escalated | confidence 64 after 2 revisions, beyond recovery
```

## Checklist Summary

This quality assurance process ensures:

✓ Confidence score is accurate and ≥70
✓ Frontmatter is complete and valid
✓ Content sections are present and substantial
✓ All claims are verified against briefs
✓ Brand guidelines are followed
✓ No prohibited content is present
✓ Format-specific requirements are met
✓ Brief reference is valid and draft aligns
✓ Publishing notes enable Distribution Agent to publish without confusion
✓ Every draft is audit-ready (ready for governance review if needed)

If all sections pass, draft is ready for Distribution Agent.
If any section fails, either revise or escalate.

**No draft enters Distribution's queue without passing this QA checklist.**
