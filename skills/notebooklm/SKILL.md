---
name: notebooklm
description: "Interface with Google NotebookLM to create notebooks, add sources (URLs, files), run analysis, and generate deliverables (infographics, mind maps, audio overviews, flashcards). Uses notebooklm-py CLI. Free RAG system — analysis happens on Google's servers."
triggers: ["notebooklm", "notebook", "analyze sources", "generate infographic", "mind map", "audio overview"]
version: 1.0.0
dependencies: ["notebooklm-py"]
---

# NotebookLM Skill

## Overview

Google NotebookLM is a free RAG (Retrieval-Augmented Generation) system. This skill lets BotDAO agents create notebooks, load sources (YouTube URLs, web pages, PDFs, text), run analysis queries, and generate deliverables — all from the command line via `notebooklm-py`.

**Why this matters for BotDAO:** Analysis happens on Google's servers at zero token cost. Claude Code orchestrates, NotebookLM thinks. This is how Scout Agent does deep research without burning through API credits.

## Prerequisites

```bash
pip install notebooklm-py
notebooklm login  # Opens browser for Google OAuth — one-time setup
```

## Core Commands

### Authentication

```bash
notebooklm login
# Opens browser → sign in with Google → token saved locally
```

### Create a Notebook

```bash
notebooklm create "Mantle Ecosystem Research"
# Returns: notebook_id (save this)

notebooklm use <notebook_id>
# Sets as active notebook for subsequent commands
```

### Add Sources

```bash
# Add YouTube videos (NotebookLM extracts transcripts automatically)
notebooklm source add "https://youtube.com/watch?v=abc123"
notebooklm source add "https://youtube.com/watch?v=def456"

# Add web pages
notebooklm source add "https://www.mantle.xyz/blog/some-article"

# Add local files
notebooklm source add "./data/mantle-research.pdf"
notebooklm source add "./data/tvl-report.md"

# Add up to 50 sources per notebook
```

### Query / Analyze

```bash
# Ask questions grounded in loaded sources
notebooklm ask "What are the main DeFi protocols on Mantle and how do they compare?"
notebooklm ask "What trading opportunities are mentioned across these videos?"
notebooklm ask "Summarize the key themes across all sources"
```

### Generate Deliverables

```bash
# Infographic (blueprint/handwritten style)
notebooklm generate infographic --orientation portrait

# Mind map
notebooklm generate mind-map

# Audio overview (podcast-style summary)
notebooklm generate audio "make it engaging" --wait

# Flashcards
notebooklm generate flashcards --quantity more

# Slide deck
notebooklm generate slide-deck

# Data table
notebooklm generate data-table "compare key protocols"
```

### Download Outputs

```bash
notebooklm download audio ./outputs/podcast.mp3
notebooklm download infographic ./outputs/infographic.png
notebooklm download mind-map ./outputs/mindmap.png
```

## BotDAO Integration Workflows

### Workflow 1: Scout Research Pipeline

Scout Agent uses yt-search + notebooklm to do deep research on a topic before generating a brief.

```bash
# 1. Search YouTube for recent Mantle content
python skills/yt-search/scripts/search.py "mantle network defi" \
  --max-results 10 --max-age 30 --output json > /tmp/yt-results.json

# 2. Create a NotebookLM notebook
notebooklm create "Scout Research: Mantle DeFi $(date +%Y-%m-%d)"
notebooklm use <notebook_id>

# 3. Load top video URLs as sources
# (parse URLs from yt-results.json and add each one)
cat /tmp/yt-results.json | python -c "
import json, sys, subprocess
data = json.load(sys.stdin)
for v in data['results'][:10]:
    subprocess.run(['notebooklm', 'source', 'add', v['url']])
"

# 4. Ask research questions
notebooklm ask "What are the top trending narratives about Mantle DeFi?"
notebooklm ask "What trading opportunities or catalysts are mentioned?"
notebooklm ask "What is the community sentiment toward Mantle?"

# 5. Generate deliverables
notebooklm generate infographic --orientation portrait
notebooklm download infographic ./data/research-infographic.png
```

### Workflow 2: Content Research (Single Prompt)

One prompt that chains everything together:

```
"Use the yt-search skill to find the latest videos about Mantle DeFi.
Load the top 10 into NotebookLM. Ask it to identify the top 3 narratives
and trading opportunities. Generate an infographic summarizing the findings.
Use the output to write a Scout brief."
```

### Workflow 3: Competitive Analysis

```bash
# Research what other L2s are doing
python skills/yt-search/scripts/search.py "arbitrum vs optimism vs mantle 2026" \
  --max-results 15 --sort views --output json > /tmp/l2-comparison.json

notebooklm create "L2 Competitive Analysis"
# Load sources, then:
notebooklm ask "How does Mantle compare to Arbitrum and Optimism in these videos?"
notebooklm ask "What advantages does Mantle have that other L2s don't?"
notebooklm generate data-table "compare L2 features, TVL, ecosystem size"
```

### Workflow 4: Bybit Content Research

```bash
# Find Bybit-related content for Content Agent
python skills/yt-search/scripts/search.py "bybit trading tutorial 2026" \
  --max-results 10 --sort views

notebooklm create "Bybit Content Research"
# Load sources, then:
notebooklm ask "What are the most common reasons people sign up for Bybit?"
notebooklm ask "What features do creators highlight as Bybit's best?"
# Use insights to improve Content Agent's Bybit CTA messaging
```

## Token Economics

| Component | Token Cost | Who Pays |
|-----------|-----------|----------|
| yt-dlp search | 0 | Nobody (scraping) |
| NotebookLM source loading | 0 | Google |
| NotebookLM analysis | 0 | Google |
| NotebookLM deliverables | 0 | Google |
| Claude Code orchestration | Minimal | You (prompt tokens only) |

This is why the workflow is powerful — the expensive RAG analysis is offloaded to Google's free tier.

## Limitations

- NotebookLM requires Google account authentication (one-time browser login)
- Max 50 sources per notebook
- notebooklm-py is unofficial — API may change if Google updates NotebookLM
- Some deliverables (audio, video) take 1-3 minutes to generate
- Source loading from YouTube requires the video to have captions/transcripts
