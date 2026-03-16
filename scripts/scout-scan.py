#!/usr/bin/env python3
"""
BotDAO Scout Agent — Signal Scanner

Scans Twitter (via API v2), DeFiLlama, and uses Claude to score signals
and generate narrative briefs for the Content Agent.

Usage (called by .github/workflows/scout-scan.yml):
    python scripts/scout-scan.py \
        --config agents/scout/config.md \
        --output-dir handoffs/scout-to-content/briefs \
        --priority-override "" \
        --focus-topic ""

Required env vars:
    ANTHROPIC_API_KEY   — Claude API key
    TWITTER_BEARER_TOKEN — Twitter API v2 bearer token
    DEFILLAMA_API       — DeFiLlama base URL (default: https://api.llama.fi)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

import anthropic
import requests

# ---------------------------------------------------------------------------
# Config parsing
# ---------------------------------------------------------------------------

def parse_config(path: str) -> dict:
    """Read Scout config.md and extract key parameters."""
    with open(path) as f:
        text = f.read()

    def _table_val(label: str) -> str:
        m = re.search(rf"\|\s*{re.escape(label)}\s*\|\s*([^|]+)\|", text)
        return m.group(1).strip().replace(",", "") if m else ""

    # Extract monitored accounts
    accounts = re.findall(r"- (@\w+)", text)

    # Extract monitored keywords from "Mantle Ecosystem" and "Bybit Conversion Signals" sections
    keywords = []
    in_keywords_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("### Mantle Ecosystem") or stripped.startswith("### Bybit Conversion Signals"):
            in_keywords_section = True
            continue
        if stripped.startswith("##"):
            in_keywords_section = False
            continue
        if in_keywords_section and stripped.startswith("- "):
            kws = [k.strip() for k in stripped.lstrip("- ").split(",") if k.strip()]
            keywords.extend(kws)

    # Extract affiliate link
    aff_match = re.search(r"Affiliate link\S*:\s*(https://\S+)", text)
    affiliate_link = aff_match.group(1) if aff_match else ""

    return {
        "scan_interval": int(_table_val("Scan interval") or 2),
        "relevance_threshold": int(_table_val("Relevance threshold") or 60),
        "narrative_cooldown": int(_table_val("Narrative cooldown") or 24),
        "max_briefs_per_cycle": int(_table_val("Max briefs per cycle") or 3),
        "monitored_accounts": accounts,
        "monitored_keywords": keywords,
        "affiliate_link": affiliate_link,
    }


# ---------------------------------------------------------------------------
# Data source fetchers
# ---------------------------------------------------------------------------

def fetch_twitter_signals(bearer_token: str, accounts: list[str],
                          keywords: list[str], hours: int) -> list[dict]:
    """Fetch recent tweets from monitored accounts and keyword searches."""
    if not bearer_token:
        print("WARNING: TWITTER_BEARER_TOKEN not set, skipping Twitter", file=sys.stderr)
        return []

    headers = {"Authorization": f"Bearer {bearer_token}"}
    base = "https://api.twitter.com/2"
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    signals = []

    # Search for tweets from monitored accounts + keywords
    # Combine into one query to conserve rate limits
    account_query = " OR ".join(f"from:{a.lstrip('@')}" for a in accounts[:6])
    keyword_sample = keywords[:10]  # API query length limit
    kw_query = " OR ".join(f'"{k}"' for k in keyword_sample)
    query = f"({account_query}) OR ({kw_query}) -is:retweet"

    # Truncate to Twitter search max (1024 chars for Essential)
    if len(query) > 1024:
        query = f"({account_query}) -is:retweet"

    params = {
        "query": query,
        "start_time": since,
        "max_results": 50,
        "tweet.fields": "created_at,public_metrics,author_id,text",
        "user.fields": "username",
        "expansions": "author_id",
    }

    try:
        r = requests.get(f"{base}/tweets/search/recent", headers=headers,
                         params=params, timeout=30)
        if r.status_code == 429:
            print("WARNING: Twitter rate limited, skipping", file=sys.stderr)
            return []
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print(f"WARNING: Twitter API error: {e}", file=sys.stderr)
        return []

    # Build author lookup
    authors = {}
    for user in data.get("includes", {}).get("users", []):
        authors[user["id"]] = user["username"]

    for tweet in data.get("data", []):
        metrics = tweet.get("public_metrics", {})
        signals.append({
            "source": "twitter",
            "author": f"@{authors.get(tweet.get('author_id'), 'unknown')}",
            "text": tweet["text"],
            "url": f"https://x.com/i/status/{tweet['id']}",
            "timestamp": tweet.get("created_at", ""),
            "likes": metrics.get("like_count", 0),
            "retweets": metrics.get("retweet_count", 0),
            "replies": metrics.get("reply_count", 0),
            "engagement": (metrics.get("like_count", 0)
                           + metrics.get("retweet_count", 0) * 2
                           + metrics.get("reply_count", 0) * 3),
        })

    print(f"Twitter: fetched {len(signals)} tweets", file=sys.stderr)
    return signals


def fetch_defillama_signals(base_url: str) -> list[dict]:
    """Fetch Mantle TVL and protocol data from DeFiLlama."""
    base_url = base_url.rstrip("/")
    signals = []
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Chain TVL
    try:
        r = requests.get(f"{base_url}/v2/chains", timeout=15)
        r.raise_for_status()
        chains = r.json()
        mantle = next((c for c in chains if c.get("name", "").lower() == "mantle"), None)
        if mantle:
            tvl = mantle.get("tvl", 0)
            signals.append({
                "source": "defillama",
                "type": "chain_tvl",
                "text": f"Mantle TVL: ${tvl / 1e6:.1f}M",
                "tvl": tvl,
                "timestamp": now_iso,
            })
    except requests.RequestException as e:
        print(f"WARNING: DeFiLlama chains error: {e}", file=sys.stderr)

    # Protocol-level data for Mantle
    try:
        r = requests.get(f"{base_url}/protocols", timeout=15)
        r.raise_for_status()
        protocols = r.json()
        mantle_protocols = []
        for p in protocols:
            chains = p.get("chains", [])
            if "Mantle" in chains:
                mantle_tvl = p.get("chainTvls", {}).get("Mantle", {})
                if isinstance(mantle_tvl, (int, float)):
                    tvl_val = mantle_tvl
                elif isinstance(mantle_tvl, dict):
                    tvl_val = mantle_tvl.get("tvl", 0)
                else:
                    tvl_val = 0
                change_1d = p.get("change_1d", 0) or 0
                mantle_protocols.append({
                    "name": p.get("name", "Unknown"),
                    "tvl": tvl_val,
                    "change_1d": change_1d,
                })

        # Sort by TVL and flag big movers
        mantle_protocols.sort(key=lambda x: abs(x.get("change_1d", 0)), reverse=True)
        for mp in mantle_protocols[:10]:
            if abs(mp["change_1d"]) >= 5:
                signals.append({
                    "source": "defillama",
                    "type": "protocol_move",
                    "text": f"{mp['name']} on Mantle: {mp['change_1d']:+.1f}% 24h change (TVL: ${mp['tvl'] / 1e6:.1f}M)",
                    "protocol": mp["name"],
                    "change_pct": mp["change_1d"],
                    "tvl": mp["tvl"],
                    "timestamp": now_iso,
                })

        print(f"DeFiLlama: {len(mantle_protocols)} Mantle protocols tracked, "
              f"{len([s for s in signals if s.get('type') == 'protocol_move'])} big movers",
              file=sys.stderr)
    except requests.RequestException as e:
        print(f"WARNING: DeFiLlama protocols error: {e}", file=sys.stderr)

    return signals


# ---------------------------------------------------------------------------
# Claude-powered scoring and brief generation
# ---------------------------------------------------------------------------

SCORING_SYSTEM = """You are the Scout Agent for BotDAO, a crypto marketing swarm focused on Mantle Network.

You will receive raw signals (tweets, DeFiLlama data). Your job:
1. Cluster related signals into distinct narratives
2. Score each narrative 0-100 based on: engagement, on-chain impact, topic alignment with Mantle ecosystem, freshness, Bybit conversion potential (+15 boost if natural signup angle exists)
3. Classify priority: urgent (security incidents, >15% TVL drop, negative sentiment spike), high (protocol launches, 5-10% TVL moves, ecosystem announcements), normal (general updates)
4. For top narratives, determine Bybit conversion angle: ecosystem-gateway | trading-opportunity | promo-amplify | none

Respond in JSON:
{
  "narratives": [
    {
      "title": "short narrative title",
      "summary": "2-3 sentence summary of what happened and why it matters to Mantle",
      "score": 85,
      "priority": "high",
      "bybit_angle": "ecosystem-gateway",
      "bybit_cta_suggestion": "one-liner CTA if angle is not none",
      "suggested_format": "thread",
      "suggested_tone": "thought-leadership",
      "hashtags": ["#Mantle", "#MNT"],
      "account_tags": ["@0xMantle"],
      "engagement_window_hours": 6,
      "sources": [
        {"platform": "twitter", "author": "@handle", "text": "...", "url": "...", "engagement": 500}
      ],
      "metrics": [
        {"metric": "Mantle TVL", "value": "$X", "source": "DeFiLlama", "timestamp": "..."}
      ]
    }
  ],
  "crisis_signals": []
}

Only include narratives scoring above THRESHOLD. Maximum MAX_BRIEFS narratives.
If you detect a crisis signal (security exploit, >15% TVL crash, regulatory action), put it in crisis_signals instead."""

BRIEF_TEMPLATE = """---
id: brief-{id}
from: scout
to: content
timestamp: {timestamp}
cycle: {cycle}
priority: {priority}
status: pending
expires: {expires}
---

# Signal Summary

{summary}

**Why it matters to Mantle**: {why_it_matters}

**Suggested engagement angle**: {engagement_angle}

## Source Signals

{sources_section}

### Key Data Points

| Metric | Value | Source | Timestamp |
|--------|-------|--------|-----------|
{metrics_rows}

## Recommendation

- **Suggested format**: {format}
- **Suggested tone**: {tone}
- **Optimal engagement window**: Publish within {window}h for peak engagement
- **Suggested hashtags**: {hashtags}
- **Account tags**: {tags}
- **Bybit conversion angle**: `{bybit_angle}`{bybit_cta}

## Context

- **Related briefs**: {related}
- **Competitive context**: {competitive}
"""


def score_and_cluster(signals: list[dict], config: dict) -> dict:
    """Send signals to Claude for scoring and clustering."""
    client = anthropic.Anthropic()

    # Build signals summary for Claude
    signal_text = json.dumps(signals, indent=2, default=str)

    # Truncate if too long (keep under ~80k chars for context window)
    if len(signal_text) > 80000:
        signal_text = signal_text[:80000] + "\n... (truncated)"

    system = SCORING_SYSTEM.replace("THRESHOLD", str(config["relevance_threshold"]))
    system = system.replace("MAX_BRIEFS", str(config["max_briefs_per_cycle"]))

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system,
        messages=[{
            "role": "user",
            "content": f"Here are the raw signals from this scan cycle. Today is {datetime.now(timezone.utc).strftime('%Y-%m-%d')}. Analyze, cluster, score, and return JSON.\n\n{signal_text}"
        }],
    )

    # Extract JSON from response
    response_text = message.content[0].text
    # Try to find JSON block
    json_match = re.search(r"\{[\s\S]*\}", response_text)
    if not json_match:
        print(f"ERROR: Claude did not return valid JSON:\n{response_text[:500]}", file=sys.stderr)
        return {"narratives": [], "crisis_signals": []}

    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse Claude JSON: {e}", file=sys.stderr)
        return {"narratives": [], "crisis_signals": []}


def generate_brief(narrative: dict, sequence: int, cycle: int,
                   config: dict) -> tuple[str, str]:
    """Generate a brief markdown file from a scored narrative. Returns (filename, content)."""
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y-%m-%dT%H%M")
    brief_id = f"{now.strftime('%Y%m%dT%H%M')}-{sequence:03d}"
    filename = f"{now.strftime('%Y-%m-%dT%H%M')}-{sequence:03d}-brief.md"
    expires = (now + timedelta(hours=narrative.get("engagement_window_hours", 6)))

    # Build sources section
    sources_lines = []
    twitter_sources = [s for s in narrative.get("sources", []) if s.get("platform") == "twitter"]
    defi_sources = [s for s in narrative.get("sources", []) if s.get("platform") == "defillama"]

    if twitter_sources:
        sources_lines.append("### X/Twitter Sources")
        for s in twitter_sources:
            author = s.get("author", "unknown")
            text_preview = s.get("text", "")[:120]
            url = s.get("url", "")
            eng = s.get("engagement", 0)
            sources_lines.append(f"- {author}: {text_preview}{'...' if len(s.get('text', '')) > 120 else ''}")
            if url:
                sources_lines.append(f"  - URL: {url}")
            sources_lines.append(f"  - Engagement: {eng}")
        sources_lines.append("")

    if defi_sources:
        sources_lines.append("### DeFiLlama Signals")
        for s in defi_sources:
            sources_lines.append(f"- {s.get('text', s.get('metric', 'data point'))}")
        sources_lines.append("")

    # Build metrics rows
    metrics_rows = []
    for m in narrative.get("metrics", []):
        metrics_rows.append(
            f"| {m.get('metric', '')} | {m.get('value', '')} | {m.get('source', '')} | {m.get('timestamp', now.isoformat())} |"
        )
    if not metrics_rows:
        metrics_rows.append(f"| Signal Score | {narrative.get('score', 0)}/100 | Scout Agent | {now.isoformat()} |")

    # Bybit CTA line
    bybit_angle = narrative.get("bybit_angle", "none")
    bybit_cta = ""
    if bybit_angle != "none" and narrative.get("bybit_cta_suggestion"):
        bybit_cta = f' — "{narrative["bybit_cta_suggestion"]}"'

    # Summary split — use Claude's summary directly
    summary = narrative.get("summary", "Signal detected.")
    title = narrative.get("title", "Untitled Signal")

    content = BRIEF_TEMPLATE.format(
        id=brief_id,
        timestamp=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        cycle=cycle,
        priority=narrative.get("priority", "normal"),
        expires=expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
        summary=f"**{title}**\n\n{summary}",
        why_it_matters=summary.split(". ")[-1] if ". " in summary else summary,
        engagement_angle=f"{narrative.get('suggested_tone', 'informational')} — {title}",
        sources_section="\n".join(sources_lines) if sources_lines else "No source details available.",
        metrics_rows="\n".join(metrics_rows),
        format=narrative.get("suggested_format", "thread"),
        tone=narrative.get("suggested_tone", "informational"),
        window=narrative.get("engagement_window_hours", 6),
        hashtags=", ".join(narrative.get("hashtags", ["#Mantle", "#MNT"])),
        tags=", ".join(narrative.get("account_tags", ["@0xMantle"])),
        bybit_angle=bybit_angle,
        bybit_cta=bybit_cta,
        related="None (automated scan)",
        competitive="Automated signal detection — check CT for competing coverage.",
    )

    return filename, content


def write_crisis_escalation(crisis: dict, output_dir: str, cycle: int):
    """Write a crisis signal to the governance handoff folder."""
    gov_dir = os.path.join(os.path.dirname(output_dir), "..", "scout-to-governance")
    gov_dir = os.path.normpath(gov_dir)
    os.makedirs(gov_dir, exist_ok=True)

    now = datetime.now(timezone.utc)
    crisis_id = f"{now.strftime('%Y%m%dT%H%M')}-001"
    filename = f"crisis-{now.strftime('%Y-%m-%dT%H%M')}-001.md"

    content = f"""---
id: crisis-{crisis_id}
from: scout
to: governance
timestamp: {now.strftime("%Y-%m-%dT%H:%M:%SZ")}
cycle: {cycle}
priority: urgent
status: pending
expires: {(now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")}
---

# Crisis Signal

**Type**: {crisis.get("type", "unknown")}

## Signal Details

{crisis.get("details", "Crisis signal detected.")}

## Sources

{json.dumps(crisis.get("sources", []), indent=2)}

## Recommended Action

{crisis.get("recommended_action", "Pause publishing and monitor.")}

## Severity Score

{crisis.get("severity", 90)}/100
"""
    filepath = os.path.join(gov_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"CRISIS escalation written: {filepath}", file=sys.stderr)


def get_current_cycle() -> int:
    """Read current cycle number from state file."""
    try:
        with open("state/current-cycle.md") as f:
            text = f.read()
        m = re.search(r"cycle:\s*(\d+)", text)
        return int(m.group(1)) if m else 1
    except FileNotFoundError:
        return 1


def load_narrative_tracker() -> set[str]:
    """Load recently covered narrative titles to check cooldown."""
    try:
        with open("data/narrative-tracker.md") as f:
            return set(re.findall(r"\|\s*(.+?)\s*\|", f.read()))
    except FileNotFoundError:
        return set()


def update_narrative_tracker(narratives: list[dict]):
    """Append new narratives to the tracker."""
    tracker_path = "data/narrative-tracker.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with open(tracker_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Narrative Tracker\n\n| Narrative | First Detected | Last Covered | Times Covered | Avg Score | Status |\n|-----------|---------------|-------------|---------------|-----------|--------|\n"

    lines = []
    for n in narratives:
        title = n.get("title", "Untitled")[:40]
        score = n.get("score", 0)
        lines.append(f"| {title} | {now} | {now} | 1 | {score} | active |")

    if lines:
        content = content.rstrip() + "\n" + "\n".join(lines) + "\n"
        with open(tracker_path, "w") as f:
            f.write(content)


def update_agent_health():
    """Update Scout heartbeat in agent-health.md."""
    health_path = "state/agent-health.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with open(health_path, "r") as f:
            content = f.read()
        # Replace existing scout line or append
        if "scout:" in content:
            content = re.sub(r"scout:.*", f"scout: {now}", content)
        else:
            content = content.rstrip() + f"\nscout: {now}\n"
        with open(health_path, "w") as f:
            f.write(content)
    except FileNotFoundError:
        with open(health_path, "w") as f:
            f.write(f"scout: {now}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="BotDAO Scout Agent — Signal Scanner")
    parser.add_argument("--config", required=True, help="Path to scout config.md")
    parser.add_argument("--output-dir", required=True, help="Directory for brief output")
    parser.add_argument("--priority-override", default="", help="Force priority level")
    parser.add_argument("--focus-topic", default="", help="Optional topic to focus scan on")
    args = parser.parse_args()

    # Load config
    config = parse_config(args.config)
    print(f"Config loaded: threshold={config['relevance_threshold']}, "
          f"max_briefs={config['max_briefs_per_cycle']}, "
          f"accounts={len(config['monitored_accounts'])}, "
          f"keywords={len(config['monitored_keywords'])}",
          file=sys.stderr)

    # Gather signals from all sources
    all_signals = []

    # Twitter
    twitter_token = os.environ.get("TWITTER_BEARER_TOKEN", "")
    twitter_signals = fetch_twitter_signals(
        twitter_token,
        config["monitored_accounts"],
        config["monitored_keywords"],
        config["scan_interval"],
    )
    all_signals.extend(twitter_signals)

    # DeFiLlama
    defillama_base = os.environ.get("DEFILLAMA_API", "https://api.llama.fi")
    defi_signals = fetch_defillama_signals(defillama_base)
    all_signals.extend(defi_signals)

    if not all_signals:
        print("No signals collected from any source. Exiting.", file=sys.stderr)
        update_agent_health()
        sys.exit(0)

    print(f"Total signals collected: {len(all_signals)}", file=sys.stderr)

    # If focus topic provided, filter signals
    if args.focus_topic:
        focus = args.focus_topic.lower()
        all_signals = [s for s in all_signals
                       if focus in s.get("text", "").lower()
                       or focus in json.dumps(s, default=str).lower()]
        print(f"Filtered to {len(all_signals)} signals matching '{args.focus_topic}'",
              file=sys.stderr)

    # Score and cluster via Claude
    result = score_and_cluster(all_signals, config)
    narratives = result.get("narratives", [])
    crises = result.get("crisis_signals", [])

    cycle = get_current_cycle()

    # Handle crisis signals
    for crisis in crises:
        write_crisis_escalation(crisis, args.output_dir, cycle)

    # Apply priority override if set
    if args.priority_override:
        for n in narratives:
            n["priority"] = args.priority_override

    # Generate briefs
    os.makedirs(args.output_dir, exist_ok=True)
    brief_count = 0
    for i, narrative in enumerate(narratives[:config["max_briefs_per_cycle"]], start=1):
        filename, content = generate_brief(narrative, i, cycle, config)
        filepath = os.path.join(args.output_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        brief_count += 1
        print(f"Brief written: {filepath} (score: {narrative.get('score', 0)}, "
              f"priority: {narrative.get('priority', 'normal')})", file=sys.stderr)

    # Update tracking
    if narratives:
        update_narrative_tracker(narratives[:config["max_briefs_per_cycle"]])

    # Update health
    update_agent_health()

    # Summary
    print(f"\nScan complete: {len(all_signals)} signals → {brief_count} briefs, "
          f"{len(crises)} crisis escalations", file=sys.stderr)


if __name__ == "__main__":
    main()
