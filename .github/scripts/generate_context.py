#!/usr/bin/env python3
"""
AIToolCrux Context Generator (CI version)
Runs in GitHub Actions. Reads repo files and generates a structured context doc.
Output: iteration_center/CONTEXT.md
"""
import json
import os
import glob
import re
from datetime import datetime, timezone

REPO_ROOT = os.environ.get("GITHUB_WORKSPACE", ".")
OUTPUT_PATH = os.path.join(REPO_ROOT, "iteration_center", "CONTEXT.md")


def read_json(rel_path):
    fp = os.path.join(REPO_ROOT, rel_path)
    try:
        with open(fp, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return None


def read_text(rel_path):
    fp = os.path.join(REPO_ROOT, rel_path)
    try:
        with open(fp, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def get_content_stats():
    posts = read_json("data/posts.json")
    tools = read_json("data/tools.json")
    cats = read_json("data/categories.json")
    comps = read_json("data/comparisons.json")

    stats = {}
    if posts:
        stats["posts"] = len(posts)
        stats["recent_posts"] = [
            {"slug": p.get("slug", "?"), "title": p.get("title", "?")[:70]}
            for p in posts[:5]
        ]
    if tools:
        stats["tools"] = len(tools) if isinstance(tools, list) else len(tools.get("tools", []))
    if cats:
        stats["categories"] = len(cats) if isinstance(cats, list) else len(cats.get("categories", []))
    if comps:
        stats["comparisons"] = len(comps) if isinstance(comps, list) else len(comps.get("comparisons", []))
    return stats


def get_state():
    s = read_json("iteration_center/state.json")
    return s or {}


def get_recent_logs(limit=5):
    log = read_json("iteration_center/iteration_log.json")
    if not log:
        return []
    entries = log if isinstance(log, list) else log.get("entries", log.get("iterations", []))
    valid = [e for e in entries if isinstance(e, dict) and any(k in e for k in ("round", "date", "commit"))]
    return valid[:limit]


def get_audit_findings():
    return read_text("iteration_center/audit_findings.md")


def get_latest_gsc_report():
    reports = glob.glob(os.path.join(REPO_ROOT, "gsc-ga4-report", "*.md"))
    if not reports:
        return None
    latest = max(reports, key=os.path.getmtime)
    with open(latest, "r", encoding="utf-8") as f:
        content = f.read()
    # Match both Chinese (GSC 点击) and English (| Clicks |) report formats
    clicks = re.search(r"GSC 点击[：:]\s*(\d+)", content) or re.search(r"\|\s*Clicks\s*\|\s*(\d+)", content)
    imp = re.search(r"GSC 曝光[：:]\s*(\d+)", content) or re.search(r"\|\s*Impressions\s*\|\s*(\d+)", content)
    ctr = re.search(r"平均\s*CTR[：:]\s*([\d.]+%)", content) or re.search(r"\|\s*CTR\s*\|\s*([\d.]+%)", content)
    rank = re.search(r"平均\s*排名[：:]\s*([\d.]+)", content) or re.search(r"\|\s*Avg Position\s*\|\s*([\d.]+)", content)
    return {
        "file": os.path.basename(latest),
        "clicks": clicks.group(1) if clicks else "N/A",
        "impressions": imp.group(1) if imp else "N/A",
        "ctr": ctr.group(1) if ctr else "N/A",
        "ranking": rank.group(1) if rank else "N/A",
    }


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    stats = get_content_stats()
    state = get_state()
    logs = get_recent_logs(5)
    audit = get_audit_findings()
    gsc = get_latest_gsc_report()

    lines = [
        f"# AIToolCrux Context (auto-generated)",
        f"",
        f"> Generated: {now}",
        f"> This file is auto-updated by GitHub Actions (context-update.yml)",
        f"",
        f"## Core Info",
        f"",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Website | https://www.aitoolcrux.com |",
        f"| Repo | qxgjz/ai-tools-review |",
        f"| Stack | Next.js 14 + TypeScript + Tailwind |",
        f"| Deploy | Vercel (auto from main) |",
        f"",
        f"## Content Stats",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Tools | {stats.get('tools', 'N/A')} |",
        f"| Posts | {stats.get('posts', 'N/A')} |",
        f"| Categories | {stats.get('categories', 'N/A')} |",
        f"| Comparisons | {stats.get('comparisons', 'N/A')} |",
        f"",
        f"## Recent Posts",
        f"",
    ]
    for i, p in enumerate(stats.get("recent_posts", []), 1):
        lines.append(f"{i}. **{p['title']}** (`{p['slug']}`)")

    lines += [
        f"",
        f"## Iteration State",
        f"",
        f"- Current round: {state.get('current_round', state.get('current_iteration', 'N/A'))}",
        f"- Last commit: {state.get('last_commit', 'N/A')}",
        f"- Last iteration: {state.get('last_iteration_date', 'N/A')}",
        f"",
        f"## Recent Iterations",
        f"",
    ]
    for entry in logs:
        rnd = entry.get("round", entry.get("date", "?"))
        commit = entry.get("commit", "")
        changes = entry.get("changes", entry.get("tasks_completed", []))
        if isinstance(changes, list):
            changes = "; ".join(str(c)[:80] for c in changes[:3])
        lines.append(f"- **Round {rnd}** ({commit}): {str(changes)[:200]}")

    lines += [
        f"",
        f"## GSC Data",
        f"",
    ]
    if gsc:
        lines += [
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Clicks | {gsc['clicks']} |",
            f"| Impressions | {gsc['impressions']} |",
            f"| CTR | {gsc['ctr']} |",
            f"| Avg Ranking | {gsc['ranking']} |",
            f"| Report | {gsc['file']} |",
        ]
    else:
        lines.append("No GSC report found.")

    lines += [
        f"",
        f"## Audit Findings (pending)",
        f"",
        audit[:3000] if audit else "No audit findings file.",
        f"",
        f"---",
        f"*Auto-generated by context-update workflow. Do not edit manually.*",
        f"",
    ]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    size = os.path.getsize(OUTPUT_PATH)
    print(f"Context written to {OUTPUT_PATH} ({size} bytes)")
    print(f"Tools: {stats.get('tools', '?')}, Posts: {stats.get('posts', '?')}")


if __name__ == "__main__":
    main()
