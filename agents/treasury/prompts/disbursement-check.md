---
prompt_name: Disbursement Processing and Approval
agent: Treasury
trigger: disbursement_request
description: Step-by-step instructions for processing a payment request, validating vendor, checking budgets, and deciding approval or escalation to Governance.
---

# Disbursement Processing Instructions

## Overview

When Treasury Agent receives a disbursement request, this prompt guides validation, budget checking, and decision-making (auto-approve, escalate to Governance, or reject).

## Step 1: Request Reception and Initial Validation

### 1.1 Receive Disbursement Request

Disbursement requests arrive via:
- Handoff file in `handoffs/*/to-treasury/` (if agent-initiated)
- Direct form submission (if operator-initiated)
- Internal message queue

### 1.2 Extract Request Details

Open request and extract:

```
disbursement_id: string (e.g., "disbursement-20260312T1400-001")
amount_mnt: integer (no decimals, in MNT tokens)
vendor: string (e.g., "Twitter API Subscription")
reason: string (e.g., "Monthly subscription for February 2026")
requested_by: string (agent name or operator)
requested_at: ISO 8601 timestamp
recipient_address: string (wallet address)
```

### 1.3 Validate Request Format

Check required fields:

| Field | Type | Required | Status |
|-------|------|----------|--------|
| disbursement_id | string | ✓ | [ ] |
| amount_mnt | integer | ✓ | [ ] |
| vendor | string | ✓ | [ ] |
| reason | string | ✓ | [ ] |
| requested_by | string | ✓ | [ ] |
| requested_at | ISO 8601 | ✓ | [ ] |
| recipient_address | address | ✓ | [ ] |

**Action**:
- ✓ All fields present: continue to 1.4
- ✗ Missing field: reject request, ask requester to resubmit
- Log: `[timestamp] disbursement_validation_failed | {id} | missing_field: {field}`

### 1.4 Validate Field Formats

**disbursement_id**:
- Pattern: `disbursement-{YYYYMMDD}T{HHMM}-{sequence}`
- Example: `disbursement-20260312T1400-001`

**amount_mnt**:
- Positive integer (no decimals)
- Example: 500 (valid), 500.5 (invalid)

**recipient_address**:
- Valid Mantle wallet address (0x prefixed, 40 hex chars)
- Example: `0x7f3a8c2d9e1b5a4c6f3d8e1a2b5c7d9e0a1b2c3d`

**Action**:
- ✓ All formats valid: continue to Step 2
- ✗ Invalid format: reject and explain issue
- Log: `[timestamp] format_validation_failed | {id} | {field}: invalid format`

## Step 2: Check Vendor Approval

### 2.1 Open Approved Vendor List

File: `botdao-governance/rulebook/treasury/approved-vendors.md`

**Example structure**:
```markdown
# Approved Vendors

## Tool Subscriptions
- Twitter API — for X/Twitter posting
- Discord API — for Discord messaging
- DeFiLlama API — for TVL/ecosystem data
- Mantle RPC — for on-chain operations

## Service Providers
- [Company Name] — [Service] — Cap: X MNT/month
- [Company Name] — [Service] — Cap: Y MNT/month

## Contractors
- [Name] — [Type of work] — Max per project: Z MNT
```

### 2.2 Search for Vendor

Look for exact match:
- Search vendor name in list
- Check if category matches request type

**Example**:
- Request: "Twitter API Subscription"
- Approved list: "Twitter API — for X/Twitter posting"
- Status: ✓ Found

### 2.3 Determine Vendor Status

**Status options**:
- ✓ **Approved**: Vendor is in the list
- ? **Unknown**: Vendor not in list (need Governance approval)
- ✗ **Explicitly blocked**: Vendor is on a "do not pay" list

**Action**:
- ✓ Approved: continue to Step 3
- ? Unknown: escalate to Governance (Step 5)
- ✗ Blocked: reject request immediately

Log: `[timestamp] vendor_check | {vendor} | {status}`

### 2.4 Check Vendor Spending Cap (if applicable)

Some vendors may have monthly spending caps in the rulebook:

**Example**:
```
Twitter API — Cap: 1,000 MNT/month
```

**Action**:
1. Check approved-vendors.md for cap
2. If no cap listed: no constraint
3. If cap exists: verify request doesn't exceed it
4. Query vault contract: `queryVendorSpendingThisMonth(vendor)`
5. Compare: `current_spending + request_amount <= cap`

**If exceeds cap**:
- Escalate to Governance (vendor limit exceeded)
- Log: `[timestamp] vendor_cap_check | {vendor} | exceeded_cap: {cap}, requested: {amount}`

## Step 3: Check Spending Constraints

### 3.1 Query Vault Smart Contract

Read current vault state:

```solidity
struct VaultState {
    uint256 monthlyBudget;        // 200,000 MNT
    uint256 spent_this_month;     // cumulative
    uint256 spent_today;          // resets at 00:00 UTC
    uint256 autoApproveThreshold; // 5,000 MNT
    uint256 dailySpendCap;        // 15,000 MNT
}
```

Call via `mantle-rpc MCP`:
```
vault_state = mantle_rpc.queryVaultState()
```

**Capture values**:
```
monthly_budget: {value}
spent_this_month: {value}
spent_today: {value}
auto_approve_threshold: {value}
daily_spend_cap: {value}
```

### 3.2 Check Daily Spend Cap

```
spent_today = vault_state.spent_today
daily_cap = vault_state.dailySpendCap  // default: 15,000 MNT
request_amount = disbursement.amount_mnt

if (spent_today + request_amount) > daily_cap:
    VIOLATES_DAILY_CAP = true
else:
    VIOLATES_DAILY_CAP = false
```

**Example**:
```
Spent today: 12,000 MNT
Daily cap: 15,000 MNT
Request: 5,000 MNT
Status: (12,000 + 5,000) > 15,000? YES → VIOLATES CAP
```

**Action**:
- ✗ Violates daily cap: escalate to Governance
- Log: `[timestamp] spending_check | daily_cap_exceeded | spent: {spent_today}, request: {amount}, cap: {daily_cap}`

### 3.3 Check Monthly Budget

```
spent_this_month = vault_state.spent_this_month
monthly_budget = vault_state.monthlyBudget  // default: 200,000 MNT
request_amount = disbursement.amount_mnt

if (spent_this_month + request_amount) > monthly_budget:
    VIOLATES_MONTHLY_BUDGET = true
else:
    VIOLATES_MONTHLY_BUDGET = false
```

**Example**:
```
Spent this month: 185,000 MNT
Monthly budget: 200,000 MNT
Request: 20,000 MNT
Status: (185,000 + 20,000) > 200,000? YES → VIOLATES BUDGET
```

**Action**:
- ✗ Violates monthly budget: escalate to Governance
- Log: `[timestamp] spending_check | monthly_budget_exceeded | spent: {spent_this_month}, request: {amount}, budget: {monthly_budget}`

### 3.4 Decision Tree for Constraints

```
if daily_cap_violated OR monthly_budget_violated:
    ESCALATE_TO_GOVERNANCE()
else:
    PROCEED_TO_3_5()
```

### 3.5 Check Auto-Approve Threshold

```
auto_approve_threshold = vault_state.autoApproveThreshold  // default: 5,000 MNT
request_amount = disbursement.amount_mnt

if request_amount <= auto_approve_threshold:
    AUTO_APPROVE = true
else:
    AUTO_APPROVE = false
```

**Example**:
```
Auto-approve threshold: 5,000 MNT
Request: 2,500 MNT
Status: 2,500 <= 5,000? YES → AUTO APPROVE
```

**Action**:
- ✓ Under threshold: proceed to auto-approval (Step 4)
- ✗ Over threshold: proceed to governance escalation (Step 5)

## Step 4: Auto-Approve Disbursement

Used for requests ≤ auto_approve_threshold with all constraints satisfied.

### 4.1 Call Smart Contract

Via `mantle-rpc MCP`, submit disbursement:

```solidity
function disburse(
    address recipient,
    uint256 amountMNT,
    string memory reason,
    bool requiresGovernance
) external returns (bool success, bytes32 transactionHash)
```

**Call parameters**:
```
recipient: disbursement.recipient_address
amountMNT: disbursement.amount_mnt
reason: disbursement.reason
requiresGovernance: false  // auto-approve, no governance needed
```

**Call**:
```
result = mantle_rpc.disburse(
  recipient: "{recipient_address}",
  amountMNT: {amount},
  reason: "{reason}",
  requiresGovernance: false
)
```

### 4.2 Handle Response

**If success = true**:
- Capture transactionHash
- Proceed to Step 6 (logging)
- Log: `[timestamp] disbursement_approved | {id} | success | tx: {tx_hash}`

**If success = false**:
- Capture error message
- If error = "insufficient_balance": escalate to Governance (budget issue)
- If error = "network_error": retry once after 5 min
- Log: `[timestamp] disbursement_failed | {id} | error: {message}`

## Step 5: Escalate to Governance Agent

Used when amount > auto_approve_threshold OR constraints violated.

### 5.1 Create Escalation File

Location: `handoffs/treasury-to-governance/escalations/{timestamp}-esc.md`

Naming: `{YYYY}{MM}{DD}T{HHMM}{SS}-esc-{sequence}.md`

Example: `20260312T140030-esc-001.md`

### 5.2 Write Frontmatter

```yaml
---
id: esc-treasury-{timestamp}-{sequence}
from: treasury
to: governance
timestamp: {ISO 8601 UTC}
cycle: {current cycle number}
priority: {normal | high}
status: pending
---
```

**Priority determination**:
- `normal`: Amount between 5,001-50,000 MNT OR minor constraint
- `high`: Amount >50,000 MNT OR constraint violation (daily cap/monthly budget)

### 5.3 Write Body Sections

#### Section 1: Disbursement Request

```markdown
## Disbursement Request

**Disbursement ID**: {id}
**Amount**: {amount} MNT
**Vendor**: {vendor}
**Reason**: {reason}
**Requested By**: {requester}
**Requested At**: {timestamp}
**Recipient Address**: {address}
```

#### Section 2: Spending Context

```markdown
## Spending Context

**Daily Spending**:
- Spent today: {amount} MNT
- Daily cap: {cap} MNT
- Available today: {remaining} MNT
- This request: {request} MNT
- Status: OK / WARNING / WOULD EXCEED

**Monthly Budget**:
- Spent this month: {amount} MNT
- Monthly budget: {budget} MNT
- Available this month: {remaining} MNT
- This request: {request} MNT
- Status: OK / WARNING / WOULD EXCEED

**Percentage of Month**: {percent}% spent ({days} days into month)
```

#### Section 3: Vendor Assessment

```markdown
## Vendor Assessment

**Vendor**: {vendor}
**Approval Status**: {approved | unknown | blocked}
**Category**: {category from rulebook}
**Vendor Cap** (if any): {cap} / {period}
**Status vs Cap**: {current} / {cap} (would be {new} / {cap})
```

#### Section 4: ROI Analysis (if applicable)

```markdown
## ROI Analysis

[Only if relevant; e.g., tool subscriptions with known impact]

**Expected ROI**:
- Tool: Twitter API
- Monthly cost: {amount} MNT
- Historical value delivered: [engagement impact, if measured]
- Estimated engagement lift: +X%

**Recommendation**:
- Cost is justified / Cost seems high / No historical data
```

#### Section 5: Recommendation

```markdown
## Recommendation

**Treasury Agent Assessment**:
- Amount: {amount} MNT exceeds auto-approve threshold (threshold: {threshold})
- Vendor: {approved | needs approval}
- Budget impact: {manageable | concerning | violates constraints}
- Risk level: {low | medium | high}

**Recommended Action**:
1. APPROVE — Amount is reasonable, vendor is approved, budget is healthy
2. APPROVE WITH CONDITIONS — Approve, but note budget is getting tight (X% used)
3. REQUEST CHANGES — Approve only if amount reduced to {amount}
4. REJECT — Vendor not approved / constraints violated / risk too high

**Reasoning**: [Explain why Treasury recommends this action]
```

### 5.4 File the Escalation

Write escalation file to `handoffs/treasury-to-governance/escalations/{filename}.md`

Log: `[timestamp] escalation_created | {id} | amount: {amount}, {reason_code}`

## Step 6: Logging and State Updates

### 6.1 Log to Disbursement Log

File: `logs/disbursement-log.md`

Format (one line per transaction):
```
[{ISO 8601}] {disbursement_id} | {vendor} | {amount_mnt} MNT | {status} | {tx_hash or reason}
```

Examples:
```
[2026-03-12T14:00:00Z] disbursement-20260312T1400-001 | Twitter API | 500 MNT | approved | 0x7f3a...
[2026-03-12T14:15:00Z] disbursement-20260312T1415-001 | Design Consultant | 45000 MNT | escalated | governance review required
[2026-03-12T14:30:00Z] disbursement-20260312T1430-001 | Unknown Vendor | 2000 MNT | rejected | vendor not approved
```

### 6.2 Update Budget Status

File: `state/budget-status.md`

After any approved disbursement, update budget tracking:

```yaml
---
timestamp: {ISO 8601 UTC}
---

## Monthly Budget (March 2026)

| Metric | Amount | Status |
|--------|--------|--------|
| Total budget | 200,000 MNT | |
| Spent to date | {updated} MNT | |
| Remaining | {updated} MNT | |
| Percentage used | {updated}% | OK / WARNING |

## Daily Spending (Today UTC)

| Metric | Amount | Limit | Status |
|--------|--------|-------|--------|
| Spent today | {updated} MNT | 15,000 MNT | OK / WARNING / EXCEEDED |
| Remaining today | {updated} MNT | | |

## Recent Transactions (Last 5)

| Timestamp | Vendor | Amount | Status | TX Hash |
|-----------|--------|--------|--------|---------|
| {ts} | {vendor} | {amt} | {status} | {hash} |
| ... | ... | ... | ... | ... |
```

### 6.3 Update Heartbeat

File: `state/agent-health.md`

```
treasury: {current ISO 8601 timestamp}
```

## Step 7: Handle Governance Response (if escalated)

### 7.1 Monitor for Response

Governance Agent writes approval/rejection to:
`handoffs/governance-to-treasury/approvals/{filename}.md`

**Action**:
- Check this directory regularly (every hour)
- Look for file with matching disbursement_id

### 7.2 If Approval Received

1. Execute disbursement (Step 4, auto-call smart contract)
2. Log: `[timestamp] disbursement_approved | {id} | governance approved | tx: {hash}`
3. Update budget status

### 7.3 If Rejection Received

1. Log: `[timestamp] disbursement_rejected | {id} | governance decision | reason: {reason}`
2. Mark as rejected in budget tracking
3. Notify requester (if applicable)

### 7.4 If No Response After 24h

1. Create urgent escalation to Governance Agent
2. Log: `[timestamp] escalation_timeout | {id} | no governance response in 24h`

## Summary: Decision Tree

```
┌─ Request received
├─ Format validation
│  └─ Invalid? → Reject
├─ Vendor check
│  ├─ Unknown? → Escalate (Governance approval needed)
│  └─ Blocked? → Reject
├─ Spending constraints
│  ├─ Daily cap violated? → Escalate (constraint)
│  └─ Monthly budget violated? → Escalate (constraint)
├─ Auto-approve threshold
│  ├─ Amount ≤ 5,000 MNT? → Auto-approve → Log → Done
│  └─ Amount > 5,000 MNT? → Escalate (Governance decision needed)
└─ Escalation
   ├─ Governance approves? → Execute → Log
   ├─ Governance rejects? → Reject → Log
   └─ No response >24h? → Escalate as urgent
```

## Error Handling

| Error | Action |
|-------|--------|
| Format validation fails | Reject, ask for resubmission |
| Vendor unknown | Escalate to Governance |
| Vault contract unreachable | Retry in 5 min; if persists >30 min, escalate |
| Recipient address invalid | Reject, ask for correction |
| Transaction reverts (insufficient balance) | Escalate to Governance (budget issue) |
| Governance response timeout >24h | Escalate as urgent |

## Quality Checklist

Before approving:
- [ ] ✓ All required fields present
- [ ] ✓ Field formats valid (ID, amount, address)
- [ ] ✓ Vendor is approved (or Unknown for escalation)
- [ ] ✓ Daily spending cap not violated
- [ ] ✓ Monthly budget not violated
- [ ] ✓ Decision path followed correctly
- [ ] ✓ Logs updated accurately
- [ ] ✓ Budget status file updated

Before escalating:
- [ ] ✓ Reason for escalation is clear
- [ ] ✓ Frontmatter complete and valid
- [ ] ✓ Sections include all context
- [ ] ✓ Recommendation is specific
- [ ] ✓ File saved to correct location

## Examples

### Example 1: Auto-Approve Request

```
Request: "disbursement-20260312T1400-001"
Amount: 500 MNT
Vendor: "Twitter API" (approved)
Recipient: "0x7f3a..."

Checks:
✓ Format valid
✓ Vendor approved
✓ Spent today: 12,000, Request: 500, Cap: 15,000 ✓
✓ Spent month: 185,000, Request: 500, Budget: 200,000 ✓
✓ Amount 500 ≤ threshold 5,000 ✓

Decision: AUTO-APPROVE
Action: Call vault.disburse(..., requiresGovernance: false)
Log: "[2026-03-12T14:00:00Z] disbursement-20260312T1400-001 | Twitter API | 500 MNT | approved | 0x7f3a..."
```

### Example 2: Escalate for Governance Decision

```
Request: "disbursement-20260312T1415-001"
Amount: 45,000 MNT
Vendor: "Design Consultant" (approved)
Recipient: "0x2b8d..."

Checks:
✓ Format valid
✓ Vendor approved
✓ Daily cap OK
✓ Monthly budget OK
✗ Amount 45,000 > threshold 5,000

Decision: ESCALATE
Action: Create escalation to Governance Agent
File: "handoffs/treasury-to-governance/escalations/20260312T141500-esc-001.md"
Log: "[2026-03-12T14:15:00Z] disbursement-20260312T1415-001 | Design Consultant | 45000 MNT | escalated | governance review required"
```

### Example 3: Reject for Unknown Vendor

```
Request: "disbursement-20260312T1430-001"
Amount: 2,000 MNT
Vendor: "Unknown Company XYZ"
Recipient: "0x9c2e..."

Checks:
✓ Format valid
✗ Vendor NOT in approved list

Decision: ESCALATE (Unknown vendor needs Governance approval)
Action: Create escalation to Governance Agent
File: "handoffs/treasury-to-governance/escalations/20260312T143000-esc-002.md"
Log: "[2026-03-12T14:30:00Z] disbursement-20260312T1430-001 | Unknown Company XYZ | 2000 MNT | escalated | vendor not approved"
```

## Integration

This prompt is part of Treasury Agent's operational cycle:

1. Requests arrive continuously (as-needed)
2. Treasury processes each request using this prompt
3. Auto-approvals execute immediately (smart contract calls)
4. Escalations wait for Governance responses (up to 24h)
5. Log is maintained throughout for audit
6. Budget status is updated after each decision

For monthly budget reset and reporting, see `monthly-report.md` prompt.
