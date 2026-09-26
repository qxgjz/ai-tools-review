"""
AIToolCrux Keyword Opportunity Miner
Scans GSC reports for high-impression, mid-ranking keywords (20-50)
that can be pushed to top 10 with optimization.
Output: iteration_center/keyword_opportunities.md
"""
import re
import os
from datetime import datetime
from pathlib import Path

PROJECT = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
GSC_DIR = PROJECT / "gsc-ga4-report"
OUTPUT_FILE = PROJECT / "iteration_center" / "keyword_opportunities.md"

# Thresholds
MIN_IMPRESSIONS = 5
TARGET_RANK_MIN = 10   # Better than 10 = already ranking well
TARGET_RANK_MAX = 60   # Worse than 60 = too far to push
EASY_WIN_MAX = 30      # Rank 10-30 = very easy win
QUICK_WIN_MAX = 50     # Rank 30-50 = moderate effort


def find_latest_gsc_report():
    """Find the most recent GSC report markdown file."""
    if not GSC_DIR.exists():
        return None
    reports = sorted(GSC_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    return reports[0] if reports else None


def parse_gsc_report(filepath):
    """Parse GSC report markdown for keyword data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse core summary
    summary = {}
    for line in content.split('\n'):
        if 'GSC 点击' in line and '**' in line:
            m = re.search(r'GSC 点击[：:]\s*(\d+)', line)
            if m:
                summary['clicks'] = int(m.group(1))
        elif 'GSC 曝光' in line and '**' in line:
            m = re.search(r'GSC 曝光[：:]\s*(\d+)', line)
            if m:
                summary['impressions'] = int(m.group(1))
        elif '平均 CTR' in line and '**' in line:
            m = re.search(r'平均 CTR[：:]\s*([\d.]+)%', line)
            if m:
                summary['ctr'] = float(m.group(1))
        elif '平均排名' in line and '**' in line:
            m = re.search(r'平均排名[：:]\s*([\d.]+)', line)
            if m:
                summary['avg_position'] = float(m.group(1))

    # Parse Top 查询词 table
    keywords = []
    in_table = False
    for line in content.split('\n'):
        if 'Top 查询词' in line or 'Top queries' in line.lower():
            in_table = True
            continue
        if in_table:
            if line.startswith('## '):
                break
            # Match table rows: | keyword | clicks | impressions | ctr | position |
            m = re.match(r'\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)%\s*\|\s*([\d.]+)\s*\|', line)
            if m:
                keywords.append({
                    'query': m.group(1).strip(),
                    'clicks': int(m.group(2)),
                    'impressions': int(m.group(3)),
                    'ctr': float(m.group(4)),
                    'position': float(m.group(5)),
                })

    # Parse keyword clusters
    clusters = []
    in_cluster = False
    for line in content.split('\n'):
        if '关键词簇' in line:
            in_cluster = True
            continue
        if in_cluster:
            if line.startswith('## '):
                break
            m = re.match(r'\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)%\s*\|\s*([\d.]+)\s*\|', line)
            if m:
                clusters.append({
                    'cluster': m.group(1).strip(),
                    'clicks': int(m.group(2)),
                    'impressions': int(m.group(3)),
                    'ctr': float(m.group(4)),
                    'position': float(m.group(5)),
                })

    return summary, keywords, clusters, filepath.name


def classify_keyword(kw):
    """Classify keyword opportunity by difficulty."""
    pos = kw['position']
    imp = kw['impressions']

    if imp < MIN_IMPRESSIONS:
        return None

    if TARGET_RANK_MIN < pos <= EASY_WIN_MAX:
        return 'EASY_WIN'  # Rank 11-30, very close to top 10
    elif EASY_WIN_MAX < pos <= QUICK_WIN_MAX:
        return 'QUICK_WIN'  # Rank 31-50, moderate effort
    elif QUICK_WIN_MAX < pos <= TARGET_RANK_MAX:
        return 'LONG_SHOT'  # Rank 51-60, needs more work
    else:
        return None


def generate_report(summary, keywords, clusters, source_file):
    """Generate keyword opportunities markdown report."""
    now = datetime.now()

    # Classify keywords
    easy_wins = []
    quick_wins = []
    long_shots = []

    for kw in keywords:
        category = classify_keyword(kw)
        if category == 'EASY_WIN':
            easy_wins.append(kw)
        elif category == 'QUICK_WIN':
            quick_wins.append(kw)
        elif category == 'LONG_SHOT':
            long_shots.append(kw)

    # Sort by impressions descending
    easy_wins.sort(key=lambda x: x['impressions'], reverse=True)
    quick_wins.sort(key=lambda x: x['impressions'], reverse=True)
    long_shots.sort(key=lambda x: x['impressions'], reverse=True)

    lines = []
    lines.append("# Keyword Opportunities Report")
    lines.append(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Source:** `{source_file}`")
    lines.append(f"**Total keywords analyzed:** {len(keywords)}")
    lines.append("")

    # Summary stats
    lines.append("## Site Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    if summary:
        lines.append(f"| Total Clicks | {summary.get('clicks', 'N/A')} |")
        lines.append(f"| Total Impressions | {summary.get('impressions', 'N/A')} |")
        lines.append(f"| Average CTR | {summary.get('ctr', 'N/A')}% |")
        lines.append(f"| Avg Position | {summary.get('avg_position', 'N/A')} |")
    lines.append(f"| Easy Wins (rank 11-30) | {len(easy_wins)} |")
    lines.append(f"| Quick Wins (rank 31-50) | {len(quick_wins)} |")
    lines.append(f"| Long Shots (rank 51-60) | {len(long_shots)} |")
    lines.append("")

    # Easy wins - highest priority
    lines.append("## 🟢 Easy Wins (Rank 11-30) - Push to Top 10")
    lines.append("")
    lines.append("These keywords are already on page 2. Small content optimization can push them to page 1.")
    lines.append("")
    if easy_wins:
        lines.append("| Keyword | Impressions | Clicks | Position | Action |")
        lines.append("|---------|------------|--------|----------|--------|")
        for kw in easy_wins:
            action = "Add to H2, internal links, optimize meta"
            lines.append(f"| `{kw['query']}` | {kw['impressions']} | {kw['clicks']} | #{kw['position']:.1f} | {action} |")
    else:
        lines.append("_No easy win keywords found in current data._")
    lines.append("")

    # Quick wins
    lines.append("## 🟡 Quick Wins (Rank 31-50) - Page 2-3")
    lines.append("")
    lines.append("These need moderate content expansion and internal linking.")
    lines.append("")
    if quick_wins:
        lines.append("| Keyword | Impressions | Clicks | Position | Action |")
        lines.append("|---------|------------|--------|----------|--------|")
        for kw in quick_wins:
            action = "Create dedicated section, add FAQ, build internal links"
            lines.append(f"| `{kw['query']}` | {kw['impressions']} | {kw['clicks']} | #{kw['position']:.1f} | {action} |")
    else:
        lines.append("_No quick win keywords found in current data._")
    lines.append("")

    # Long shots
    lines.append("## 🔵 Long Shots (Rank 51-60) - Lower Priority")
    lines.append("")
    lines.append("These have impressions but rank far. Consider for future content batches.")
    lines.append("")
    if long_shots:
        lines.append("| Keyword | Impressions | Clicks | Position |")
        lines.append("|---------|------------|--------|----------|")
        for kw in long_shots:
            lines.append(f"| `{kw['query']}` | {kw['impressions']} | {kw['clicks']} | #{kw['position']:.1f} |")
    else:
        lines.append("_No long shot keywords found in current data._")
    lines.append("")

    # Keyword clusters
    if clusters:
        lines.append("## Keyword Clusters")
        lines.append("")
        lines.append("| Cluster | Impressions | Avg Position |")
        lines.append("|---------|------------|-------------|")
        for c in sorted(clusters, key=lambda x: x['impressions'], reverse=True):
            lines.append(f"| `{c['cluster']}` | {c['impressions']} | #{c['position']:.1f} |")
        lines.append("")

    # Action plan for next content
    lines.append("## 📋 Next Content Priorities")
    lines.append("")
    lines.append("### For Window 3 (next article generation):")
    lines.append("")
    priority_keywords = easy_wins[:3] + quick_wins[:3]
    if priority_keywords:
        for i, kw in enumerate(priority_keywords, 1):
            lines.append(f"{i}. **`{kw['query']}`** - {kw['impressions']} impressions, currently #{kw['position']:.1f}")
            lines.append(f"   - Write an article or expand existing page targeting this query")
            lines.append(f"   - Add FAQ section answering related sub-questions")
            lines.append(f"   - Build 3-5 internal links from related tool pages")
            lines.append("")
    else:
        lines.append("- No priority keywords identified. Focus on content expansion for existing top pages.")
        lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated by keyword_miner.py at {now.strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines), len(easy_wins), len(quick_wins)


def main():
    latest = find_latest_gsc_report()
    if not latest:
        print("⚠️ No GSC reports found!")
        # Write a minimal report
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# Keyword Opportunities Report\n\n**Status:** No GSC data available.\n\nRun the GSC pipeline first.")
        return

    summary, keywords, clusters, source = parse_gsc_report(latest)
    report, easy_count, quick_count = generate_report(summary, keywords, clusters, source)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"=== Keyword Opportunity Mining Complete ===")
    print(f"  Source: {source}")
    print(f"  Keywords analyzed: {len(keywords)}")
    print(f"  Easy Wins (11-30): {easy_count}")
    print(f"  Quick Wins (31-50): {quick_count}")
    print(f"  Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
