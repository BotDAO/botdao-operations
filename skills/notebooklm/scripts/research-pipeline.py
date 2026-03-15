#!/usr/bin/env python3
"""
BotDAO Research Pipeline
Chains yt-search + NotebookLM for automated research.

Usage:
    python skills/notebooklm/scripts/research-pipeline.py "mantle defi" \
        --notebook-name "Scout Research" \
        --questions "What are the top narratives?" "What trading opportunities exist?"
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime


def run_cmd(cmd, capture=True, timeout=120):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd, capture_output=capture, text=True, timeout=timeout
        )
        if result.returncode != 0 and capture:
            print(f"Warning: command failed: {' '.join(cmd)}", file=sys.stderr)
            print(f"  stderr: {result.stderr[:200]}", file=sys.stderr)
        return result
    except subprocess.TimeoutExpired:
        print(f"Timeout: {' '.join(cmd)}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"Not found: {cmd[0]}. Is it installed?", file=sys.stderr)
        return None


def step_1_search_youtube(query, max_results=10, max_age=60):
    """Search YouTube and return video list."""
    print(f"\n{'='*60}")
    print(f"STEP 1: Searching YouTube for \"{query}\"")
    print(f"{'='*60}")

    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    search_script = os.path.join(script_dir, "..", "yt-search", "scripts", "search.py")

    result = run_cmd([
        sys.executable, search_script, query,
        "--max-results", str(max_results),
        "--max-age", str(max_age),
        "--output", "json"
    ])

    if not result or result.returncode != 0:
        print("Failed to search YouTube", file=sys.stderr)
        return []

    try:
        data = json.loads(result.stdout)
        videos = data.get("results", [])
        print(f"Found {len(videos)} videos")
        for i, v in enumerate(videos, 1):
            print(f"  {i}. {v['title'][:50]} ({v['channel']}, {v.get('views', '?')} views)")
        return videos
    except json.JSONDecodeError:
        print("Failed to parse YouTube results", file=sys.stderr)
        return []


def step_2_create_notebook(name):
    """Create a NotebookLM notebook and return ID."""
    print(f"\n{'='*60}")
    print(f"STEP 2: Creating NotebookLM notebook: \"{name}\"")
    print(f"{'='*60}")

    result = run_cmd(["notebooklm", "create", name])
    if not result:
        return None

    # Parse notebook ID from output
    notebook_id = result.stdout.strip()
    print(f"Notebook created: {notebook_id}")

    # Set as active
    run_cmd(["notebooklm", "use", notebook_id])
    return notebook_id


def step_3_load_sources(videos, max_sources=10):
    """Load video URLs into NotebookLM as sources."""
    print(f"\n{'='*60}")
    print(f"STEP 3: Loading {min(len(videos), max_sources)} sources into NotebookLM")
    print(f"{'='*60}")

    loaded = 0
    for v in videos[:max_sources]:
        url = v.get("url", "")
        if not url:
            continue
        print(f"  Loading: {v['title'][:40]}...")
        result = run_cmd(["notebooklm", "source", "add", url], timeout=30)
        if result and result.returncode == 0:
            loaded += 1

    print(f"Loaded {loaded}/{min(len(videos), max_sources)} sources")
    return loaded


def step_4_analyze(questions):
    """Ask analysis questions to NotebookLM."""
    print(f"\n{'='*60}")
    print(f"STEP 4: Running analysis ({len(questions)} questions)")
    print(f"{'='*60}")

    answers = []
    for q in questions:
        print(f"\n  Q: {q}")
        result = run_cmd(["notebooklm", "ask", q], timeout=60)
        if result and result.returncode == 0:
            answer = result.stdout.strip()
            print(f"  A: {answer[:200]}...")
            answers.append({"question": q, "answer": answer})
        else:
            answers.append({"question": q, "answer": "[Failed to get answer]"})

    return answers


def step_5_generate(deliverables, output_dir):
    """Generate NotebookLM deliverables."""
    print(f"\n{'='*60}")
    print(f"STEP 5: Generating deliverables")
    print(f"{'='*60}")

    os.makedirs(output_dir, exist_ok=True)
    generated = []

    for d in deliverables:
        print(f"  Generating: {d}...")
        result = run_cmd(["notebooklm", "generate", d], timeout=180)
        if result and result.returncode == 0:
            # Download the output
            ext = {"infographic": "png", "mind-map": "png", "audio": "mp3",
                   "flashcards": "md", "slide-deck": "pptx", "data-table": "md"}.get(d, "txt")
            output_path = os.path.join(output_dir, f"{d}.{ext}")
            dl_result = run_cmd(["notebooklm", "download", d, output_path], timeout=60)
            if dl_result and dl_result.returncode == 0:
                print(f"  Saved: {output_path}")
                generated.append(output_path)

    return generated


def step_6_save_report(query, videos, answers, generated, output_dir):
    """Save a research report summarizing everything."""
    print(f"\n{'='*60}")
    print(f"STEP 6: Saving research report")
    print(f"{'='*60}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    report_path = os.path.join(output_dir, "research-report.md")

    with open(report_path, "w") as f:
        f.write(f"---\n")
        f.write(f"query: \"{query}\"\n")
        f.write(f"timestamp: {now}\n")
        f.write(f"sources: {len(videos)}\n")
        f.write(f"questions: {len(answers)}\n")
        f.write(f"deliverables: {len(generated)}\n")
        f.write(f"---\n\n")
        f.write(f"# Research Report: {query}\n\n")
        f.write(f"*Generated {now}*\n\n")

        f.write(f"## Sources ({len(videos)} videos)\n\n")
        for i, v in enumerate(videos, 1):
            f.write(f"{i}. [{v['title']}]({v['url']}) — {v['channel']} ({v.get('views', '?')} views, {v.get('date', '?')})\n")

        f.write(f"\n## Analysis\n\n")
        for qa in answers:
            f.write(f"### {qa['question']}\n\n")
            f.write(f"{qa['answer']}\n\n")

        if generated:
            f.write(f"## Generated Deliverables\n\n")
            for g in generated:
                f.write(f"- [{os.path.basename(g)}]({g})\n")

    print(f"Report saved: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="BotDAO Research Pipeline: yt-search + NotebookLM")
    parser.add_argument("query", help="YouTube search query")
    parser.add_argument("--notebook-name", default=None, help="NotebookLM notebook name")
    parser.add_argument("--max-results", type=int, default=10, help="Max YouTube results")
    parser.add_argument("--max-age", type=int, default=60, help="Max video age in days")
    parser.add_argument("--questions", nargs="+", default=[
        "What are the main themes and narratives across these sources?",
        "What opportunities or catalysts are mentioned?",
        "What is the overall sentiment?",
    ], help="Analysis questions for NotebookLM")
    parser.add_argument("--deliverables", nargs="+", default=["infographic"],
                        choices=["infographic", "mind-map", "audio", "flashcards", "slide-deck", "data-table"],
                        help="Deliverables to generate")
    parser.add_argument("--output-dir", default="./data/research", help="Output directory")
    parser.add_argument("--skip-notebooklm", action="store_true", help="Skip NotebookLM (YouTube search only)")

    args = parser.parse_args()

    notebook_name = args.notebook_name or f"BotDAO Research: {args.query} ({datetime.now().strftime('%Y-%m-%d')})"
    output_dir = os.path.join(args.output_dir, datetime.now().strftime("%Y%m%d-%H%M"))
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: YouTube search
    videos = step_1_search_youtube(args.query, args.max_results, args.max_age)
    if not videos:
        print("No videos found. Exiting.")
        sys.exit(1)

    if args.skip_notebooklm:
        # Save just the YouTube results
        step_6_save_report(args.query, videos, [], [], output_dir)
        print("\nDone (NotebookLM skipped)")
        sys.exit(0)

    # Step 2: Create notebook
    notebook_id = step_2_create_notebook(notebook_name)
    if not notebook_id:
        print("Failed to create notebook. Is notebooklm-py installed and authenticated?")
        print("Run: pip install notebooklm-py && notebooklm login")
        sys.exit(1)

    # Step 3: Load sources
    loaded = step_3_load_sources(videos)
    if loaded == 0:
        print("No sources loaded. Exiting.")
        sys.exit(1)

    # Step 4: Analyze
    answers = step_4_analyze(args.questions)

    # Step 5: Generate deliverables
    generated = step_5_generate(args.deliverables, output_dir)

    # Step 6: Save report
    report = step_6_save_report(args.query, videos, answers, generated, output_dir)

    print(f"\n{'='*60}")
    print(f"COMPLETE")
    print(f"{'='*60}")
    print(f"  Sources: {len(videos)} videos loaded")
    print(f"  Questions: {len(answers)} answered")
    print(f"  Deliverables: {len(generated)} generated")
    print(f"  Report: {report}")


if __name__ == "__main__":
    main()
