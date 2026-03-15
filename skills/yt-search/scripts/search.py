#!/usr/bin/env python3
"""
YouTube Search Skill for BotDAO
Searches YouTube for videos matching a query and returns ranked results.
Uses yt-dlp for scraping — no API key required.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


def search_youtube(query, max_results=20, max_age_days=180, sort="relevance"):
    """Search YouTube using yt-dlp and return structured results."""

    # Build yt-dlp command
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--dump-json",
        "--flat-playlist",
        "--no-download",
        "--quiet",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"Error: yt-dlp failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp not installed. Run: pip install yt-dlp", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: yt-dlp search timed out after 60s", file=sys.stderr)
        sys.exit(1)

    # Parse results
    videos = []
    cutoff_date = datetime.now() - timedelta(days=max_age_days)

    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Extract upload date
        upload_date_str = data.get("upload_date", "")
        if upload_date_str:
            try:
                upload_date = datetime.strptime(upload_date_str, "%Y%m%d")
            except ValueError:
                upload_date = None
        else:
            upload_date = None

        # Filter by age
        if upload_date and upload_date < cutoff_date:
            continue

        video = {
            "url": f"https://youtube.com/watch?v={data.get('id', '')}",
            "title": data.get("title", "Unknown"),
            "channel": data.get("channel", data.get("uploader", "Unknown")),
            "views": data.get("view_count", 0),
            "duration": format_duration(data.get("duration", 0)),
            "date": upload_date.strftime("%b %d") if upload_date else "Unknown",
            "date_raw": upload_date if upload_date else datetime.min,
        }
        videos.append(video)

    # Sort
    if sort == "views":
        videos.sort(key=lambda v: v["views"], reverse=True)
    elif sort == "date":
        videos.sort(key=lambda v: v["date_raw"], reverse=True)
    # relevance = default order from yt-dlp

    # Filter out videos older than max_age
    filtered_count = max_results - len(videos)
    if filtered_count > 0:
        print(f"(Filtered out {filtered_count} video(s) older than {max_age_days} days)", file=sys.stderr)

    return videos


def format_duration(seconds):
    """Convert seconds to MM:SS or HH:MM:SS format."""
    if not seconds:
        return "0:00"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_views(count):
    """Format view count as human-readable (e.g., 45K, 1.2M)."""
    if not count:
        return "0"
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def output_table(videos, query):
    """Print results as a formatted table."""
    print(f'\nTop {len(videos)} YouTube results for "{query}":\n')

    # Header
    print(f"{'#':<4} {'URL':<45} {'Title':<40} {'Channel':<20} {'Views':<8} {'Length':<8} {'Date':<8}")
    print("-" * 133)

    for i, v in enumerate(videos, 1):
        title = v["title"][:38] + ".." if len(v["title"]) > 40 else v["title"]
        channel = v["channel"][:18] + ".." if len(v["channel"]) > 20 else v["channel"]
        print(f"{i:<4} {v['url']:<45} {title:<40} {channel:<20} {format_views(v['views']):<8} {v['duration']:<8} {v['date']:<8}")


def output_markdown(videos, query):
    """Print results as markdown table."""
    now = datetime.now().strftime("%Y-%m-%d")
    print(f'## YouTube Research: "{query}"')
    print(f"*Searched on {now} | {len(videos)} results*\n")
    print("| # | Title | Channel | Views | Length | Date | Link |")
    print("|---|-------|---------|-------|--------|------|------|")

    for i, v in enumerate(videos, 1):
        print(f"| {i} | {v['title']} | {v['channel']} | {format_views(v['views'])} | {v['duration']} | {v['date']} | [Watch]({v['url']}) |")


def output_json(videos, query):
    """Print results as JSON."""
    output = {
        "query": query,
        "searched_at": datetime.now().isoformat(),
        "count": len(videos),
        "results": [{k: v for k, v in video.items() if k != "date_raw"} for video in videos],
    }
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Search YouTube for videos on a topic")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--max-age", type=int, default=180, help="Max age in days (default: 180)")
    parser.add_argument("--sort", choices=["relevance", "date", "views"], default="relevance")
    parser.add_argument("--output", choices=["table", "markdown", "json"], default="table")

    args = parser.parse_args()

    videos = search_youtube(args.query, args.max_results, args.max_age, args.sort)

    if not videos:
        print(f'No results found for "{args.query}"')
        sys.exit(0)

    if args.output == "table":
        output_table(videos, args.query)
    elif args.output == "markdown":
        output_markdown(videos, args.query)
    elif args.output == "json":
        output_json(videos, args.query)


if __name__ == "__main__":
    main()
