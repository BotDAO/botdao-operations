---
prompt_name: Escalation Response Drafting
agent: Governance
trigger: escalation_received
description: Instructions for reading an escalation from Treasury, Analytics, or another agent, and drafting a response (approval, rejection, or guidance).
---

# Escalation Response Drafting Instructions

## Overview

When Governance Agent receives an escalation from Treasury, Analytics, Content, or Scout, this prompt guides crafting a response that either approves, rejects, or requests changes.

## Prerequisites

- Escalation file has been received in a `handoffs/*/to-governance/` channel
- Escalation has been classified (type, priority)
- Governance Agent is ready to respond

## Step 1: Read and Classify Escalation

### 1.1 Open Escalation File

Location: `handoffs/{agent}-to-governance/`

Example paths:
- `handoffs/treasury-to-governance/escalations/{id}.md`
- `handoffs/analytics-to-governance/reports/{id}.md`
- `handoffs/content-to-governance/{id}.md`
- `handoffs/scout-to-governance/{id}.md`

### 1.2 Extract Key Information

From frontmatter:
```yaml
id: escalation ID
from: agent name
to: governance
timestamp: creation time
priority: normal | high | urgent
status: pending
```

From body:
- What is the issue/request?
- What action is recommended?
- What context/data supports the request?

### 1.3 Classify Escalation Type

**Treasury escalations**:
- Above-threshold disbursement (amount > 5,000 MNT)
- Constraint violation (daily cap or monthly budget exceeded)
- Unknown vendor approval request
- Budget concern (running low)

**Analytics escalations**:
- Anomaly report (positive or negative)
- Threshold breach (engagement too high/low)
- Data quality issue

**Content escalations**:
- Low-confidence draft (can't reach 70)
- Topic not approved
- Backlog exceeded

**Scout escalations**:
- Crisis signal (security, negative sentiment, TVL drop)
- System error or data unavailable

## Step 2: Evaluate Request

### 2.1 For Treasury Escalations (Disbursement Approval)

**If above-threshold amount (>5,000 MNT)**:

Evaluate:
1. **Vendor legitimacy**: Is vendor in approved list?
2. **Amount reasonableness**: Is amount proportional to service?
3. **Budget health**: What % of budget remains?
4. **Priority**: Is work high-value or essential?

**Decision framework**:
```
if vendor_approved AND amount_reasonable AND budget_healthy:
    RECOMMEND_APPROVE()
elif vendor_approved AND amount_reasonable AND budget_tight:
    APPROVE_WITH_CAUTION()  # note budget impact
elif vendor_unknown:
    REQUEST_VENDOR_APPROVAL()
elif amount_seems_high:
    REQUEST_COST_JUSTIFICATION()
```

### 2.2 For Analytics Escalations (Anomaly Reports)

**If positive anomaly** (engagement above benchmark):

Evaluate:
1. **Confidence**: How strong is the signal? (multiple metrics agree?)
2. **Reproducibility**: Can we replicate this pattern?
3. **Actionability**: What should we do differently?

**Decision framework**:
```
if strong_signal AND actionable:
    RECOMMEND_REPLICATE()  # guidance to Scout/Content
else if interesting_but_unclear:
    REQUEST_INVESTIGATION()  # ask for deeper analysis
```

**If negative anomaly** (engagement below benchmark):

Evaluate:
1. **Severity**: How far below benchmark?
2. **Cause**: External factors or content issue?
3. **Action**: Should we pause, adjust, or investigate?

**Decision framework**:
```
if severe_AND_content_caused:
    RECOMMEND_PAUSE_SIMILAR()  # guidance to Content/Scout
else if external_factors:
    MONITOR()  # expect recovery
else if unclear:
    REQUEST_INVESTIGATION()
```

### 2.3 For Content Escalations (Low Confidence Drafts)

**If confidence <70 after revisions**:

Evaluate:
1. **Brief quality**: Was the scout brief clear?
2. **Content difficulty**: Is the topic inherently hard to write?
3. **Content capability**: Should we improve Content Agent's ability?

**Decision framework**:
```
if brief_unclear:
    REJECT_BRIEF()  # ask Scout to re-signal
else if content_difficult:
    APPROVE_ANYWAY()  # or request revision
else if content_agent_struggling:
    PROVIDE_GUIDANCE()  # coaching on how to improve
```

### 2.4 For Scout Escalations (Crisis Signals)

**If crisis signal** (security, negative sentiment, TVL drop):

Evaluate:
1. **Severity**: How urgent is this?
2. **Scope**: What part of ecosystem affected?
3. **Action**: What should we do immediately?

**Decision framework**:
```
if security_incident:
    PAUSE_DISTRIBUTION_IMMEDIATELY()
    CREATE_GITHUB_ISSUE_URGENT()
else if negative_sentiment:
    RECOMMEND_MONITORING()
    CREATE_GITHUB_ISSUE()
else if tvl_drop:
    RECOMMEND_STATEMENT_OR_RESPONSE()
```

## Step 3: Draft Response

### 3.1 Response Format

**File location**: `handoffs/governance-to-{agent}/`

**Naming**: `{timestamp}-response-{agent}-{id-suffix}.md`

Example: `20260312T163500-response-treasury-20260312T1415-001.md`

### 3.2 Frontmatter

```yaml
---
id: response-{timestamp}-{sequence}
from: governance
to: {agent name}
timestamp: {ISO 8601 UTC, now}
cycle: {current cycle}
in_response_to: {escalation ID}
decision: {approve | reject | request_info | request_revision}
priority: {normal | high}
status: pending
---
```

### 3.3 Body: Decision Section

```markdown
## Governance Decision

**Response to**: {escalation ID}
**Escalation Type**: {type}
**Original Request**: [Brief summary]

**Decision**: {APPROVE | REJECT | REQUEST INFORMATION | REQUEST REVISION}

**Reasoning**:
[1-3 sentences explaining why]

[Rest of body depends on decision type...]
```

### 3.4 Decision-Specific Response Bodies

#### If APPROVE (Treasury Disbursement)

```markdown
## Decision: APPROVE

**Amount**: {amount} MNT
**Vendor**: {vendor}
**Recipient**: {wallet address}

**Reasoning**:
- Vendor is approved and legitimate
- Amount is reasonable for service
- Current budget status: {X}% used, adequate buffer remaining
- Work is [essential | high-value]

**Conditions** (if any):
- [List any conditions, e.g., "Please confirm this is final payment for the project"]

**Next Steps**:
Treasury Agent should execute disbursement via smart contract.
```

#### If REJECT (Content Draft or Treasury)

```markdown
## Decision: REJECT

**Escalation ID**: {id}
**Reason for Rejection**: [Brief but clear explanation]

**Reasoning**:
- [Specific reason 1]
- [Specific reason 2]

**Recommended Next Steps**:
- [Guidance on how to resubmit or alternative action]

**Contact**: If questions, escalate again with additional context.
```

#### If REQUEST INFORMATION (Analytics Anomaly)

```markdown
## Decision: REQUEST ADDITIONAL INVESTIGATION

**Escalation ID**: {id}
**Need**: [What additional information/analysis is needed?]

**Specifics**:
- [Specific question 1]
- [Specific question 2]

**Context**:
[Why this information matters]

**Timeline**:
Please respond within [N hours] so we can [action].

**Reassessment**:
Once we have this information, we'll make a final decision.
```

#### If REQUEST REVISION (Content Agent)

```markdown
## Decision: REQUEST REVISION

**Draft ID**: {id}
**Issue**: [Specific problem with the draft]

**Recommendation**:
[Specific guidance on how to improve]

**Resubmission**:
Once revised, please resubmit to Governance for approval before sending to Distribution.

**Timeline**: Please revise within [N hours].
```

#### If APPROVE WITH CAUTION (Budget Tight)

```markdown
## Decision: APPROVE WITH CAUTION

**Amount**: {amount} MNT
**Vendor**: {vendor}
**Decision**: Approved

**Budget Impact**:
- Current budget usage: {X}%
- After this disbursement: {Y}%
- Remaining buffer: {Z}%

**Caution**:
Budget is running tight. If additional high-value opportunities arise this month, we may be unable to fund them. Monitor closely.

**Recommendation for Treasury**:
Begin planning for next month's budget allocation now.
```

#### If PAUSE SIMILAR CONTENT (Negative Anomaly)

```markdown
## Decision: TEMPORARY HOLD ON SIMILAR CONTENT

**Anomaly Detected**: [Narrative type] underperforming significantly

**Metrics**:
- Expected engagement: X
- Actual engagement: Y
- Deviation: -Z%

**Action**:
Scout Agent: Reduce weighting on [narrative type] for next 2 cycles
Content Agent: Lower priority for [narrative type] drafts
Distribution Agent: No action needed; respond to any pending drafts

**Reason**:
[Explanation of why this content isn't resonating]

**Timeline**: Review decision after 2 cycles for potential course correction.

**Monitoring**:
If one more campaign of this type underperforms, escalate for deeper review.
```

## Step 4: Include Supporting Context

### 4.1 Reference Relevant Data

If rejecting or requesting info, include:
- Links to relevant files (brief, draft, logs)
- Data points that inform decision
- Historical context (how similar cases were handled)

### 4.2 Example Inclusive Response

```markdown
## Decision: APPROVE

**Amount**: 5,500 MNT
**Vendor**: Design Contractor (approved)

**Supporting Data**:
- Monthly budget remaining: 14,000 MNT (7%)
- Spent today: 6,200 MNT / 15,000 MNT cap
- This is the 3rd design contract this month (trend: increasing design spend)

**Approval**:
Vendor is approved, amount is reasonable, budget permits.

**Note**:
Monitor design spending going forward—trending upward. Consider if April needs budget for additional design work.

**Reference**:
- Escalation: handoffs/treasury-to-governance/escalations/{id}.md
- Current budget: state/budget-status.md
- Spending trend: reports/monthly/treasury-2026-03.md
```

## Step 5: Address Precedent and Consistency

### 5.1 Reference Prior Decisions

If this is similar to a past escalation, reference it:

```markdown
**Precedent**:
Similar request was submitted on [date] for [vendor/type].
We approved/rejected because: [reasoning]
This case is [identical | similar | different] because: [explanation]
Therefore, consistent decision is: [decision]
```

### 5.2 Document if Changing Previous Guidance

If this decision differs from past approach:

```markdown
**Policy Note**:
Previous similar requests were [handled differently].
This time we're [changing approach] because: [new information | changed circumstances]
This new approach will apply going forward [unless circumstances change].
```

## Step 6: Set Expectations for Next Steps

### 6.1 What Happens Now

```markdown
## Next Steps

**Immediate** (within 1 hour):
- [Agent] should [action]

**Follow-up** (within 24 hours):
- [Agent] should [action]

**Monitoring** (ongoing):
- [Watch for X, report if Y happens]
```

### 6.2 Timeline for Response

If escalation is from treasury and requires quick action:

```markdown
**Timeline**:
- This approval is valid until [date/time]
- If not executed by then, requires re-approval
- Expected execution: within [N hours]
```

## Step 7: Write to File and Notify Agent

### 7.1 Save Response File

File: `handoffs/governance-to-{agent}/[response_filename].md`

### 7.2 Log the Response

Append to governance log:

```
[{timestamp}] escalation_response | {agent} | {escalation_id} | decision: {approve|reject|request_info}
```

Example:
```
[2026-03-12T16:37:00Z] escalation_response | treasury | esc-treasury-20260312T1415-001 | decision: approve
```

### 7.3 Notify Agent (if system supports)

Send notification to agent:
- "New governance response for escalation {id}"
- Link to response file

## Error Handling

| Scenario | Action |
|----------|--------|
| Insufficient information to decide | Request additional investigation |
| Conflicting constraints (e.g., budget vs strategy) | Escalate to human team or create GitHub issue |
| Never seen this type of escalation before | Research past decisions, use judgment, document reasoning |
| Decision impacts multiple agents | Create separate responses or one response with multi-agent directions |

## Quality Checklist

Before finalizing response:

- [ ] ✓ Decision clearly stated (approve/reject/request)
- [ ] ✓ Reasoning is clear and data-driven
- [ ] ✓ Frontmatter is complete and valid YAML
- [ ] ✓ If approving: conditions and next steps are clear
- [ ] ✓ If rejecting: guidance on how to resubmit is provided
- [ ] ✓ If requesting info: specific questions are listed
- [ ] ✓ Supporting context included (links, data)
- [ ] ✓ Timeline is realistic
- [ ] ✓ File saved to correct location
- [ ] ✓ Logged in governance log

## Integration

Responses go to agent via `handoffs/governance-to-{agent}/` channel:

1. Treasury reads response from `handoffs/governance-to-treasury/approvals/`
2. Analytics reads response (if applicable)
3. Content reads response (if applicable)
4. Scout reads response (if applicable)

Each agent checks their channel regularly and acts on responses.

Governance maintains these channels as ONE-WAY communication (G → Agent).
Agents escalate back via their escalation channels (Agent → G).

This creates a conversation loop for iterative decision-making.
