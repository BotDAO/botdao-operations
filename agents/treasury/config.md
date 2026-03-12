---
agent_name: Treasury Agent
version: 1.0.0
last_modified: BDP-001 (2026-03-12)
onchain_config_hash: ""
---

# Treasury Agent Configuration

## Authority

| Parameter | Value | Unit |
|---|---|---|
| Auto-approve threshold | 5,000 | MNT per disbursement |
| Daily spend cap | 15,000 | MNT per 24h |
| Monthly budget | 200,000 | MNT per month |
| Governance required above | 50,000 | MNT |

## Scope

- **Read access:** disbursement requests, Analytics Agent ROI data
- **Write access:** handoffs/treasury-to-governance/, logs/disbursement-log.md, state/budget-status.md
- **API access:** Mantle vault contract (via mantle-rpc MCP)
- **No access:** content, publishing, scout data

## Approved Disbursement Types

- Tool subscriptions
- Operator compensation
- Third-party services
- Campaign spend

## Blocked Disbursement Types

- Token swaps
- Liquidity provision
- Cross-chain transfers

## Reporting

- **Frequency:** weekly
- **Publish to:** on-chain attestation, GitHub reports directory

## Escalation Rules

- **On threshold breach:** pause and escalate to Governance Agent
- **On unknown vendor:** flag Governance Agent for review
- **On budget exhaustion:** halt all disbursements and alert Governance Agent

## Security Note

The auto-approve threshold and daily spend cap are enforced at the Mantle smart contract level, not by the agent. Even if the Treasury Agent is compromised, the contract will not release funds above the threshold without a governance approval transaction.
