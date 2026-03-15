---
prompt_name: Governance Proposal Impact Analysis
agent: Governance
trigger: proposal_pr_submitted
description: Instructions for analyzing a GitHub PR proposing changes to governance rules, agent configs, or operational parameters. Assess impact on affected agents and estimate risk.
---

# Governance Proposal Impact Analysis Instructions

## Overview

When a GitHub PR is submitted proposing changes to governance rules, agent configurations, or operational parameters, Governance Agent analyzes the impact before recommending approval, request for changes, or rejection.

## Step 1: Receive and Classify Proposal

### 1.1 Identify PR

GitHub PR submitted to:
- `botdao-operations/` (agent configs, operational rules)
- `botdao-governance/rulebook/` (governance rules)

PR contains:
- Title describing change
- Description explaining motivation
- Files changed (diffs visible)
- May include: proposed implementation, test cases, rollback plan

### 1.2 Classify Proposal Type

**Types**:

- **Parameter change**: Thresholds, limits, time windows (low risk)
  - Example: `relevance_threshold: 60 → 65`
  - Risk: Low (easy to rollback)

- **Config change**: Agent configuration like `max_drafts_per_cycle: 3 → 5`
  - Example: Distribution max_posts_per_day increased
  - Risk: Low-Medium (operational impact)

- **Rule addition/removal**: New spending category, new escalation type
  - Example: New vendor type added to approved list
  - Risk: Medium

- **Process change**: Workflow modification, new agent, changed order
  - Example: Add new "quality-review" step before publishing
  - Risk: High (touches all agents)

- **Constitutional amendment**: Changes to Governance Agent itself
  - Example: Modify Governance Agent's emergency powers
  - Risk: Very High (requires supermajority vote per rulebook)

### 1.3 Extract Key Metadata

From PR:

```
title: [PR title]
number: [PR#]
author: [GitHub user]
created_at: [ISO 8601]
proposed_by: [Human person or agent]
target_files: [list of files changed]
type: [parameter | config | rule | process | constitutional]
```

## Step 2: Impact Analysis

### 2.1 Identify Affected Agents

For each file changed, determine which agents are impacted:

**Example**:
```
PR changes: agents/scout/config.md

Impact:
- Scout Agent: HIGH (directly affected)
- Content Agent: LOW (may use Scout's outputs differently)
- Distribution Agent: NONE
- Analytics Agent: MEDIUM (may need to recalibrate benchmarks)
- Treasury Agent: NONE
- Governance Agent: NONE
```

### 2.2 Analyze Change Details

For each affected agent, answer:

1. **What specifically changes?**
   - Config parameter name and old → new value
   - Reason for change
   - Expected effect

2. **How does agent behavior change?**
   - What will the agent do differently?
   - Will outputs change?
   - Will operational speed/throughput change?

3. **Are there interdependencies?**
   - Does this agent's change affect other agents?
   - What downstream effects are expected?

**Example**:
```
Change: relevance_threshold: 60 → 65

Scout Agent impact:
- Harder for signals to pass threshold
- Fewer briefs generated (fewer high-quality signals = higher bar)
- Scout may need to scan more sources to hit output targets

Content Agent impact:
- Receives fewer briefs (maybe 2 per cycle instead of 3)
- Less workload, faster cycle time
- No behavior change, just volume change

Analytics Agent impact:
- Fewer campaigns to score (fewer publishes due to fewer briefs)
- May need more cycles to build statistical confidence
- Timing model will take longer to develop
```

### 2.3 Create Impact Assessment Table

```markdown
## Impact Assessment

| Agent | Impact Level | Effect | Rollback Difficulty |
|-------|---|---|---|
| Scout | HIGH | Threshold raised; fewer briefs | Easy (1 config change) |
| Content | LOW | Fewer drafts to process | Easy (automatic result) |
| Distribution | LOW | Fewer publishes | Easy (automatic result) |
| Analytics | MEDIUM | Slower model development | Medium (need more cycles) |
| Treasury | NONE | — | — |
| Governance | LOW | Slightly less activity | Easy |

**Overall Impact**: MEDIUM (affects Scout directly, ripples downstream)
```

## Step 3: Risk Assessment

### 3.1 Evaluate Risk by Category

#### Breaking Changes
- Will this break existing workflows?
- Are there compatibility issues?
- Will data be lost?

```
Risk: Low (parameter change is backward-compatible)
No breaking changes expected.
```

#### Performance Impact
- Will agent throughput change?
- Could this cause bottlenecks?
- What's the worst-case scenario?

```
Risk: Low-Medium
If threshold is too high, Scout may struggle to find enough signals
(worst case: 0 briefs per cycle, content pipeline stalls)
Mitigation: Set threshold thoughtfully, monitor first cycle
```

#### Financial Impact
- Does this affect spending?
- Could this cause budget overruns?
- What are financial implications?

```
Risk: None (parameter change, not spending change)
```

#### Governance/Compliance
- Does this violate any rules?
- Does it need a vote?
- Are there Constitutional concerns?

```
Risk: None (pre-approved parameter change)
Governance Agent can merge directly (if within pre-approved list)
```

#### Operational/System Risk
- Could this break the operational cycle?
- What if something goes wrong?
- Is there a rollback plan?

```
Risk: Low
Rollback: Simply revert commit and redeploy config
Estimated recovery time: <5 minutes
```

### 3.2 Rank Overall Risk

```
Risk Level: LOW-MEDIUM

Factors:
+ Low breaking change risk (parameter change)
+ Easy to rollback (single config file)
+ No financial impact
- Could affect Scout Agent output (depending on threshold value)
- May need monitoring in first cycle
- Could slow Analytics model development if threshold too high
```

## Step 4: Evaluate Change Quality

### 4.1 Check Change Completeness

**Does the PR include**:
- [ ] ✓ Clear description of what's changing
- [ ] ✓ Rationale/motivation for the change
- [ ] ✓ Examples or test cases
- [ ] ✓ Rollback plan (if applicable)
- [ ] ✓ Impact on agents (if known)
- [ ] ✓ Timeline/when to deploy

**If missing**:
- Request additional information from PR author
- Ask for test cases or examples

### 4.2 Check Alignment with Rulebook

**Is the proposal consistent with**:
- [ ] ✓ Approved spending policies (if financial change)
- [ ] ✓ Governance rules (if process change)
- [ ] ✓ Agent constraints (if config change)
- [ ] ✓ Constitutional rules (if governance change)

**If misaligned**:
- Request changes before approval
- Explain which rule conflicts

### 4.3 Assess Proposal Justification

**Is the reasoning sound?**
- Is the motivation clear?
- Are benefits explained?
- Are trade-offs acknowledged?
- Is data provided (if applicable)?

**Example good justification**:
```
Current relevance_threshold: 60
Problem: Generating too many low-quality briefs (2-3 per cycle)
Most have engagement <50, suggest quality issue
Proposed change: 65
Expected result: Higher bar, fewer but better briefs (1-2 per cycle)
Risk: Might miss some narratives; mitigation = monitor first cycle
Data: Analysis of past 20 briefs shows X% would be filtered
Rollback: Easy (single parameter)
```

## Step 5: Draft GitHub Comment

### 5.1 Comment Format

Post comment on the PR with:

1. **Analysis summary**: 1 paragraph
2. **Affected agents table**: Summary of impact
3. **Risk assessment**: Overall risk level + factors
4. **Completeness check**: Any missing info requested
5. **Recommendation**: Approve, Request Changes, or Reject
6. **Conditions** (if any): What must be done before merging

### 5.2 Example Comment

```markdown
## Governance Impact Analysis

**Summary**:
This PR proposes raising the `relevance_threshold` from 60 to 65 for Scout Agent.
The change aims to reduce low-quality briefs and improve downstream content quality.

### Affected Agents

| Agent | Impact | Notes |
|-------|--------|-------|
| Scout | HIGH | Threshold raised; expect fewer briefs |
| Content | LOW | Fewer input briefs |
| Analytics | MEDIUM | Slower model development |
| Others | NONE | — |

### Risk Assessment

**Risk Level**: LOW-MEDIUM

✅ Low breaking change risk (parameter change)
✅ Easy rollback (single config file)
✅ No financial impact
⚠️ Could affect Scout output volume (depends on signal distribution)
⚠️ Monitor first cycle for feasibility

### Completeness

- [x] Clear description of change
- [x] Motivation provided
- [ ] No test cases / example impacts shown → **Request**: Can you provide analysis of how many briefs would be filtered under new threshold?
- [x] Rollback plan is simple

### Recommendation

**Status**: REQUEST CHANGES

**Reasoning**:
- Proposal is sound, but I'd like to see data on impact (how many of past 20 briefs would be filtered?)
- This will help Scout Agent assess feasibility
- Once data is provided, I recommend approval (low risk parameter change)

**Conditions**:
1. Provide impact data (number of briefs filtered from past campaigns)
2. Confirm Scout Agent can still meet `max_briefs_per_cycle` targets with new threshold
3. Once confirmed, request approval from Scout Agent (affected agent)

### Merge Authority

If approved by Scout Agent: Governance Agent can merge directly (this is a pre-approved parameter change)
If Scout concerns: escalate to human governance vote (requires simple majority)
```

## Step 6: Determine Merge Authority

### 6.1 Check If Pre-Approved

From rulebook (`botdao-governance/rulebook/agents/`):

**Parameter changes** (low-risk, can merge directly):
- `relevance_threshold` ±5 points
- `scan_interval` ±1 hour
- `max_drafts_per_cycle` ±1 draft
- Similar low-impact adjustments

**Example pre-approved list**:
```markdown
# Pre-Approved Governance Changes

Governance Agent can merge directly (no vote required):
- Scout: relevance_threshold (±5 points), scan_interval (±1 hour)
- Content: max_drafts_per_cycle (±1), revision_limit (±1)
- Distribution: min_time_between_posts (±30 min), max_posts_per_day (±2)
- Analytics: monitoring_window (±6 hours), anomaly_threshold (±5%)
- Treasury: auto_approve_threshold (±1,000 MNT), daily_spend_cap (±2,000 MNT)

All other changes require: simple majority vote (>50%), 7-day voting period
Constitutional amendments require: supermajority vote (>75%), 14-day voting period
```

### 6.2 Classify This Proposal

**If pre-approved**:
```
Decision: APPROVE
Authority: Governance Agent
Action: Merge directly (no vote needed)
Notification: Create issue "Parameter updated: {change}"
```

**If requires vote**:
```
Decision: REQUEST GOVERNANCE VOTE
Authority: DAO members
Action: Create on-chain voting proposal
Voting period: [N days]
Threshold: [simple majority / supermajority]
Notification: Post voting link on GitHub PR
```

**If constitutional amendment**:
```
Decision: REQUEST CONSTITUTIONAL VOTE
Authority: DAO members (supermajority)
Action: Follow Constitutional Amendment process
Voting period: 14 days minimum
Threshold: >75% approval
Notification: Alert community via announcement
```

## Step 7: Provide Governance Guidance

### 7.1 If Approving

Comment should include:

```markdown
## Governance Approval

**Decision**: APPROVED

This is a pre-approved parameter change (within Scout config bounds).

**Implementation**:
1. Awaiting approval from Scout Agent (see link to escalation/approval channel)
2. Once Scout approves, Governance Agent will merge PR
3. Config change deploys within next cycle

**Timeline**:
- Scout approval: expected within 2 hours
- Deployment: next cycle start
- Monitoring: First cycle will show impact; report any issues

**Rollback**:
If issues arise: Revert commit, takes <5 minutes
```

### 7.2 If Requesting Changes

Comment should include:

```markdown
## Governance Request for Changes

**Decision**: REQUEST CHANGES

Before this can be approved, I need:

1. **Impact Data**: Analysis of how many past briefs would be filtered
2. **Scout Agent Input**: Confirm feasibility with new threshold
3. **Risk Mitigation**: Plan if Scout can't meet output targets

**Timeline**:
- Changes requested by: [date]
- Once provided, I'll re-review
- Expected approval: 1-2 days after changes submitted

Please comment here when you've addressed these items.
```

### 7.3 If Rejecting

Comment should include:

```markdown
## Governance Rejection

**Decision**: REJECT

**Reason**:
[Specific reason, e.g., violates rule, contradicts another proposal, high risk]

**Recommendation**:
- [Alternative approach, if applicable]
- [When to resubmit with changes]
- [Process to follow for appeals]

**Questions?**: Escalate to human governance team (see links in rulebook)
```

## Step 8: Log Analysis

Append to governance log:

```
[{timestamp}] impact_analysis_complete | PR#{number} | {title} | decision: {approve|request_changes|reject}
```

Example:
```
[2026-03-12T16:40:00Z] impact_analysis_complete | PR#47 | "Scout: Raise relevance threshold" | decision: request_changes
```

## Step 9: Follow Up

### 9.1 If Approval Granted

1. Monitor PR for Scout Agent approval
2. When Scout approves, merge PR
3. Log merge: `PR#{number} merged by Governance Agent`
4. Create GitHub issue: "Config deployed: {change}"

### 9.2 If Changes Requested

1. Monitor PR for updates
2. When author responds, re-review
3. Request additional changes or approve

### 9.3 If Rejected

1. Close PR (with comment explaining why)
2. Invite resubmission when ready
3. Monitor for new PR on similar topic

## Quality Checklist

Before posting impact analysis:

- [ ] ✓ Proposal type identified correctly
- [ ] ✓ All affected agents listed
- [ ] ✓ Impact on each agent explained
- [ ] ✓ Overall risk assessed
- [ ] ✓ Completeness check done
- [ ] ✓ Alignment with rules verified
- [ ] ✓ Merge authority determined
- [ ] ✓ Recommendation is clear
- [ ] ✓ Comment is professional and data-driven
- [ ] ✓ Logged in governance log

## Examples

### Example 1: Pre-Approved Parameter Change

**PR**: Raise Scout relevance_threshold from 60 to 65

Analysis:
- Impact: Scout generates fewer briefs (higher bar)
- Risk: LOW (pre-approved, easy rollback)
- Recommendation: APPROVE (within bounds)
- Authority: Governance Agent can merge

Decision: APPROVE

### Example 2: Requires Voting

**PR**: Add new spending category "Research & Development" with 20,000 MNT/month allocation

Analysis:
- Impact: Treasury Agent processes new category; monthly budget increases
- Risk: MEDIUM (changes budget rules)
- Recommendation: REQUEST VOTE (not pre-approved)
- Authority: DAO members (simple majority)

Decision: REQUEST GOVERNANCE VOTE

### Example 3: Constitutional Amendment

**PR**: Modify Governance Agent's emergency powers (expand auto-pause conditions)

Analysis:
- Impact: Governance Agent can pause any agent for additional reasons
- Risk: VERY HIGH (changes Governance Agent itself)
- Recommendation: CONSTITUTIONAL AMENDMENT (supermajority)
- Authority: DAO members (>75%, 14 days)

Decision: REQUEST CONSTITUTIONAL AMENDMENT VOTE

---

This prompt ensures governance changes are thoroughly analyzed before implementation, minimizing risk and maintaining system integrity.
