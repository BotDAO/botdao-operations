# Schema: Governance → All Agents (Directives)

## Channel

Governance Agent writes directives here that apply to one or more agents. All agents should check this channel at the start of every cycle.

## File Location

`handoffs/governance-to-all/directives/{timestamp}-directive.md`

## Required Frontmatter

| Field | Type | Description |
|---|---|---|
| id | string | `dir-{timestamp}-{sequence}` |
| from | string | `governance` |
| to | string | `all` or specific agent name(s) comma-separated |
| timestamp | ISO 8601 | When the directive was issued |
| cycle | integer | Current operational cycle number |
| priority | enum | `normal`, `high`, `urgent` |
| status | enum | `active`, `superseded`, `expired` |
| directive_type | enum | `pause`, `resume`, `config-update`, `halt-all`, `notice` |
| expires | ISO 8601 | When this directive expires (if applicable) |

## Required Body Sections

1. **Directive** — Clear, unambiguous instruction
2. **Reason** — Why this directive was issued (link to escalation, governance vote, or emergency)
3. **Affected Agents** — Which agents must act on this directive
4. **Expected Response** — What the affected agent(s) should do
5. **Authority** — Reference to the governance vote, emergency power, or rule that authorizes this directive

## Directive Types

- **pause** — Target agent must stop processing at end of current step
- **resume** — Target agent may resume normal operations
- **config-update** — Agents must re-read their config.md (governance repo was updated)
- **halt-all** — All agents stop immediately (catastrophic scenario only)
- **notice** — Informational, no action required (e.g., weekly governance summary)
