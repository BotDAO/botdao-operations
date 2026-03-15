# BotDAO Content Pipeline - GitHub Integration

## How it works

The content pipeline runs as 4 GitHub Actions workflows that chain together automatically:

```
Scout (scheduled)
  |
  | writes briefs to handoffs/scout-to-content/briefs/
  | creates GitHub Issue for urgent/high priority
  |
  v
Content (triggered by push to briefs/)
  |
  | reads pending briefs
  | drafts threads, scores them
  | opens a PR for human review
  |
  v
[Human Review] - approve/edit/reject the PR
  |
  v
Distribution (triggered by PR merge)
  |
  | publishes approved drafts to @bo7dao
  | copies to published/ for tracking
  | creates Analytics tracking issue
  |
  v
Analytics (daily schedule)
  |
  | pulls engagement metrics from Twitter API
  | writes performance scores to handoffs/analytics-to-scout/scores/
  | Scout reads these on next scan to improve signal ranking
```

## Workflows

| Workflow | Trigger | Agent | Output |
|----------|---------|-------|--------|
| `scout-scan.yml` | Every 6h + manual | Scout | Briefs + Issues |
| `content-draft.yml` | Push to briefs/ + manual | Content | Drafts + PR |
| `distribution-publish.yml` | PR merge + manual | Distribution | Published threads |
| `analytics-report.yml` | Daily midnight UTC + manual | Analytics | Engagement scores |

## Human checkpoints

The pipeline has one mandatory human review point: the Content PR. When Content generates a draft, it opens a pull request. You review the thread copy, check the claims, and merge to publish. Nothing goes live without your approval.

For breaking news, you can also trigger any workflow manually from the Actions tab.

## Required secrets

Add these in your repo Settings > Secrets and variables > Actions:

| Secret | Required | Description |
|--------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key for Scout + Content agents |
| `TWITTER_BEARER_TOKEN` | Yes | Twitter API v2 bearer token (read access for Scout + Analytics) |
| `TWITTER_API_KEY` | For Distribution | Twitter API key (write access for posting) |
| `TWITTER_API_SECRET` | For Distribution | Twitter API secret |
| `TWITTER_ACCESS_TOKEN` | For Distribution | OAuth access token for @bo7dao |
| `TWITTER_ACCESS_SECRET` | For Distribution | OAuth access secret for @bo7dao |

## Required Python scripts

The workflows call these scripts which need to be created:

| Script | Agent | Purpose |
|--------|-------|---------|
| `scripts/scout-scan.py` | Scout | Scans data sources, generates briefs |
| `scripts/content-draft.py` | Content | Reads briefs, drafts threads via Claude |
| `scripts/distribution-publish.py` | Distribution | Posts threads to Twitter via Tweepy |
| `scripts/analytics-report.py` | Analytics | Pulls engagement metrics, writes scores |

## Required labels

Create these labels in your repo (Settings > Labels):

| Label | Color | Description |
|-------|-------|-------------|
| `scout-brief` | #1d76db | Scout-generated signal brief |
| `priority-urgent` | #d73a4a | Urgent priority signal |
| `priority-high` | #e99695 | High priority signal |
| `awaiting-content` | #fbca04 | Brief waiting for Content agent |
| `content-drafted` | #0e8a16 | Content has drafted a response |
| `content-draft` | #c5def5 | PR contains content draft |
| `awaiting-review` | #fbca04 | Draft needs human review |
| `content-escalation` | #d93f0b | Low-confidence draft |
| `governance-review` | #b60205 | Needs Governance review |
| `crisis` | #d73a4a | Crisis escalation |
| `analytics-tracking` | #0075ca | Awaiting engagement analysis |
| `awaiting-analytics` | #fbca04 | Published, waiting for metrics |

## Getting started

1. Push the `botdao-operations` folder to a GitHub repo
2. Add the required secrets (at minimum: `ANTHROPIC_API_KEY`)
3. Create the labels listed above
4. Build the Python scripts (or run the pipeline manually while developing)
5. Trigger the Scout workflow manually from Actions tab to test

## Manual operation (current mode)

Until the Python scripts are built, you can run the pipeline manually:

1. Write a brief by hand (or have Claude generate one) and commit to `handoffs/scout-to-content/briefs/`
2. Content workflow triggers, but without the script it won't auto-draft. Instead, draft manually and open a PR.
3. Merge the PR when the thread looks good.
4. Distribution workflow triggers. Use `dry_run: true` to preview, or post manually to @bo7dao.
5. Track engagement manually and log to `handoffs/analytics-to-scout/scores/`.

## Crisis handling

If Scout detects a crisis signal, it writes to `handoffs/scout-to-governance/` (NOT content) and creates a GitHub Issue tagged `crisis` + `governance-review`. The content pipeline pauses automatically since no brief is written to the Content handoff folder.
