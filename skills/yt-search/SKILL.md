---
name: yt-search
description: "Search YouTube for videos on a topic, return ranked results with titles, channels, views, dates, and URLs. Use when the Scout Agent needs video intelligence on Mantle ecosystem topics, or when researching competitor content."
triggers: ["youtube search", "find videos", "yt-search", "video research"]
version: 1.0.0
dependencies: ["yt-dlp"]
---

# YouTube Search Skill

## Overview

Search YouTube for videos matching a query. Returns a ranked table of results with video URL, title, channel, view count, duration, and upload date. Useful for Scout Agent research, competitive analysis, and content sourcing.

## Usage

```bash
python skills/yt-search/scripts/search.py "mantle network defi"
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max-results` | 20 | Number of results to return |
| `--max-age` | 180 | Filter out videos older than N days |
| `--sort` | relevance | Sort by: relevance, date, views |
| `--output` | table | Output format: table, json, markdown |

### Examples

```bash
# Search for Mantle ecosystem content
python skills/yt-search/scripts/search.py "mantle network" --max-results 10 --max-age 30

# Find Bybit tutorials (for content ideas)
python skills/yt-search/scripts/search.py "bybit tutorial 2026" --sort views

# Export as markdown for Scout brief
python skills/yt-search/scripts/search.py "mantle L2 defi" --output markdown > data/yt-research.md
```

## Integration with Scout Agent

The Scout Agent can use this skill during Step 2 (Data Source Scanning) to supplement social and on-chain signals with video content intelligence:

1. Run search for Mantle-related topics
2. Identify trending videos (high views + recent upload)
3. Flag videos that could inspire content angles
4. Include video signals in brief's Source Signals section

## Output Format

### Table (default)

```
#  | URL                                    | Title              | Channel        | Views | Length | Date
1  | https://youtube.com/watch?v=abc123     | Mantle DeFi Guide  | CryptoDaily    | 45K   | 12:30  | Mar 10
2  | https://youtube.com/watch?v=def456     | MNT Token Analysis | DeFi Insider   | 22K   | 8:45   | Mar 08
```

### Markdown

```markdown
## YouTube Research: "mantle network defi"
*Searched on 2026-03-15 | 10 results | Filtered to last 30 days*

| # | Title | Channel | Views | Date | Link |
|---|-------|---------|-------|------|------|
| 1 | Mantle DeFi Guide | CryptoDaily | 45K | Mar 10 | [Watch](url) |
```

## Setup

```bash
pip install yt-dlp
```

No API key required — yt-dlp scrapes YouTube search results directly.
