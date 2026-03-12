---
prompt_name: Impact Analysis
agent: governance
trigger: proposal_pr_opened
description: Analyze a governance proposal PR and write an impact report
---

# Impact Analysis

## When to Run
When the `impact-analysis.yml` GitHub Action fires on a new PR in the governance repo, signaling a new proposal needs review.

## Steps

### 1. Read the Proposal
Examine the PR diff. Identify:
- Which files in `rulebook/` are being changed?
- What parameters are being modified?
- What are the old values vs proposed new values?
- What type of proposal is this? (parameter change, budget, new agent, emergency, constitutional)

### 2. Identify Affected Agents
Map each changed file to the agents it affects:
- `rulebook/agents/scout.md` changes affect Scout
- `rulebook/brand/*` changes affect Content and Distribution
- `rulebook/treasury/*` changes affect Treasury
- `rulebook/system/*` changes can affect all agents
- `rulebook/agents/governance.md` is self-modification (constitutional constraint applies)

### 3. Risk Assessment
For each affected agent, evaluate:
- Will this change break current operations? (high/medium/low risk)
- Does it require agent restart or just config reload?
- Are there cascading effects on other agents?
- Does it conflict with any other current config?

### 4. Estimate Impact
- Operational impact: how much does this change day-to-day behavior?
- Financial impact: does this affect budget, caps, or spend patterns?
- Brand impact: does this change how BotDAO presents itself?
- Security impact: does this change access controls or authority scopes?

### 5. Write Report
Post the impact analysis as a comment on the PR (via GitHub API). Include:
- Summary of changes
- Affected agents list
- Risk level (low/medium/high)
- Recommendation (approve, request changes, or flag for extended review)
- Any conditions for safe deployment

Also save the report to `reports/impact-analyses/` in the governance repo.

### 6. Constitutional Check
If the proposal modifies `rulebook/agents/governance.md`:
- Flag as constitutional amendment
- Requires 75% supermajority and 14-day voting period
- Governance Agent cannot approve changes to its own config
