# BotDAO Skills — Local Setup Guide

## Prerequisites

- Python 3.10+
- Google account (for NotebookLM)
- Claude Code (for orchestration)

## Step 1: Install Dependencies

```bash
pip install yt-dlp notebooklm-py
```

## Step 2: Authenticate NotebookLM

```bash
notebooklm login
```

This opens your browser. Sign in with a Google account. The token is saved locally — you only do this once.

## Step 3: Test YouTube Search

```bash
python skills/yt-search/scripts/search.py "mantle network" --max-results 5
```

You should see a table of 5 YouTube videos about Mantle.

## Step 4: Test NotebookLM

```bash
notebooklm create "Test Notebook"
notebooklm source add "https://www.mantle.xyz"
notebooklm ask "What is Mantle?"
```

You should get an answer grounded in Mantle's website content.

## Step 5: Run the Full Pipeline

```bash
python skills/notebooklm/scripts/research-pipeline.py "mantle defi ecosystem" \
  --max-results 10 \
  --max-age 30 \
  --questions "What are the top Mantle DeFi protocols?" \
              "What trading opportunities are emerging?" \
              "How does Mantle compare to other L2s?" \
  --deliverables infographic mind-map \
  --output-dir ./data/research
```

This will:
1. Search YouTube for "mantle defi ecosystem"
2. Create a NotebookLM notebook
3. Load the top 10 videos as sources
4. Ask your 3 questions (analyzed by Google's RAG)
5. Generate an infographic and mind map
6. Save a research report to `data/research/`

## Using with Claude Code

From Claude Code, you can run the full pipeline with a single prompt:

```
Use the yt-search skill to find the latest videos about Mantle DeFi.
Load the top 10 into NotebookLM using the research pipeline.
Ask it to identify the top narratives and trading opportunities.
Generate an infographic. Save the report to data/research/.
```

Or use the individual skills separately:

```
/yt-search mantle network defi
```

```
Create a NotebookLM notebook, add these 5 URLs as sources,
and ask: "What are the key themes across these sources?"
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `yt-dlp: command not found` | `pip install yt-dlp` |
| `notebooklm: command not found` | `pip install notebooklm-py` |
| NotebookLM auth fails | `notebooklm login` — re-authenticate in browser |
| YouTube search returns 0 results | Try broader query, increase `--max-age` |
| NotebookLM source loading fails | Video may not have captions; try a different URL |
| Timeout on deliverable generation | Some outputs (audio, video) take 1-3 min; use `--wait` flag |
