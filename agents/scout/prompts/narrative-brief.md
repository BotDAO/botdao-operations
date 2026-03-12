---
prompt_name: Narrative Brief
agent: scout
trigger: signal_above_threshold
description: Write a structured handoff brief from a scored signal
---

# Narrative Brief

## When to Run
After daily-scan.md produces a signal that passes the relevance threshold, use this prompt to write the formal brief that Content will use.

## Output Location
Write to `handoffs/scout-to-content/briefs/` as a timestamped file, e.g. `2026-03-12T14-00-scout-brief.md`

## Brief Format
Follow the schema defined in `handoffs/scout-to-content/SCHEMA.md`. The file must include:

### Frontmatter
```
---
id: scout-{ISO timestamp}
from: scout
to: content
type: brief
status: pending
created: {ISO 8601 timestamp}
priority: {high|medium|low}
narrative_id: {short slug like "mantle-tvl-milestone"}
---
```

### Body Sections

**Narrative Summary**: 2-3 sentences describing what happened and why it matters for Mantle.

**Source Data**: List each source with links or data points. Include numbers where possible (TVL figures, percentage changes, transaction counts).

**Suggested Angles**: Provide 2-3 content angles Content could take:
- Data-driven angle (lead with numbers)
- Community angle (lead with ecosystem impact)
- Technical angle (lead with how it works)

**Supporting Context**: Any background Content needs to write well. Recent related events, key players involved, relevant metrics for comparison.

**Urgency Rating**: How time-sensitive is this?
- Urgent: publish within 2 hours (breaking event)
- Standard: publish within current cycle (notable development)
- Evergreen: publish anytime within 48 hours (trend or analysis)

## Quality Checks Before Saving
- All frontmatter fields filled in
- At least one data point with a specific number
- At least two suggested angles
- Narrative is not in cooldown (check `data/narrative-tracker.md`)
- Priority level matches urgency rating
