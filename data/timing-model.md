---
last_updated: 2026-03-12T00:00:00Z
data_points: 0
---

# Timing Model

Updated by the Analytics Agent based on observed engagement patterns. Read by the Distribution Agent to select optimal posting times.

## Optimal Posting Times (UTC)

| Day | Best Window | Engagement Index | Confidence |
|---|---|---|---|
| Monday | 14:00–16:00 | — | low (default) |
| Tuesday | 14:00–16:00 | — | low (default) |
| Wednesday | 14:00–16:00 | — | low (default) |
| Thursday | 14:00–16:00 | — | low (default) |
| Friday | 14:00–16:00 | — | low (default) |
| Saturday | 16:00–18:00 | — | low (default) |
| Sunday | 16:00–18:00 | — | low (default) |

These are initial defaults. The model will be updated as engagement data accumulates. Confidence moves from `low` to `medium` after 10 data points per day, and `high` after 30.
