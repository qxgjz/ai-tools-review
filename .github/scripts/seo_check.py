#!/usr/bin/env python3
"""
SEO Health Check (CI version)
Fetches key pages from aitoolcrux.com and checks SEO basics.
Outputs report to iteration_center/seo_check_latest.md
"""
import re
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

BASE = "https://www.aitoolcrux.com"
PAGES = [
    ("/", "Homepage"),
    ("/ranking", "Ranking"),
    ("/compare", "Compare"),
    ("/blog", "Blog index"),
    ("/category/chat", "Category: Chat"),
    ("/tools/chatgpt", "Tool: ChatGPT"),
    ("/blog/stable-diffusion-review-2026", "Blog: Stable Diffusion Review"),
    ("/blog/cursor-review-2026", "Blog: Cursor Review"),
]

OUTPUT = "iteration_center/seo_check_latest.md"


def fetch(url):
    req = Request(url, headers={"User-Agent": "SEO-Checker/1.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, str(e)


def check_page(path, name):
    url = BASE + path
    status, html = fetch(url)
    result = {"path": path, "name": name, "status": status, "issues": []}

    if status != 200:
        result["issues"].append(f"HTTP {status}")
        return result

    # Title
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    title = title_m.group(1).strip() if title_m else ""
    result["title"] = title
    result["title_len"] = len(title)
    if not title:
        result["issues"].append("Missing title")
    elif len(title) < 30:
        result["issues"].append(f"Title too short ({len(title)} chars)")
    elif len(title) > 65:
        result["issues"].append(f"Title too long ({len(title)} chars)")

    # Meta description
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.S | re.I)
    desc = desc_m.group(1).strip() if desc_m else ""
    result["desc"] = desc
    result["desc_len"] = len(desc)
    if not desc:
        result["issues"].append("Missing meta description")
    elif len(desc) < 50:
        result["issues"].append(f"Meta desc too short ({len(desc)} chars)")
    elif len(desc) > 170:
        result["issues"].append(f"Meta desc too long ({len(desc)} chars)")

    # H1
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    h1 = re.sub(r"<[^>]+>", "", h1_m.group(1)).strip() if h1_m else ""
    result["h1"] = h1
    if not h1:
        result["issues"].append("Missing H1")

    # Canonical
    canon_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.I)
    result["canonical"] = canon_m.group(1) if canon_m else ""
    if not result["canonical"]:
        result["issues"].append("Missing canonical")

    # Robots meta
    robots_m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html, re.I)
    result["robots"] = robots_m.group(1) if robots_m else "index,follow (default)"

    # OG tags
    og_title = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', html, re.I)
    og_desc = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']', html, re.I)
    result["og_title"] = bool(og_title)
    result["og_desc"] = bool(og_desc)
    if not og_title:
        result["issues"].append("Missing og:title")
    if not og_desc:
        result["issues"].append("Missing og:description")

    # Word count (rough)
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    words = len(text.split())
    result["words"] = words

    return result


def main():
    print(f"SEO Check: {datetime.now(timezone.utc).isoformat()}")
    results = []
    for path, name in PAGES:
        print(f"  Checking {path}...")
        r = check_page(path, name)
        results.append(r)
        status_icon = "OK" if not r["issues"] else f"{len(r['issues'])} issues"
        print(f"    {status_icon} | title={r.get('title_len', 0)} chars | desc={r.get('desc_len', 0)} chars")

    # Build report
    lines = [
        f"# SEO Health Check",
        f"",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"",
        f"## Summary",
        f"",
        f"| Page | HTTP | Title | Desc | H1 | Canonical | Issues |",
        f"|------|------|-------|------|----|-----------|--------|",
    ]
    total_issues = 0
    for r in results:
        n = len(r["issues"])
        total_issues += n
        lines.append(
            f"| {r['name']} | {r['status']} | {r.get('title_len', 0)}c | {r.get('desc_len', 0)}c | "
            f"{'Y' if r.get('h1') else 'N'} | {'Y' if r.get('canonical') else 'N'} | {n} |"
        )

    lines += [
        f"",
        f"## Details",
        f"",
    ]
    for r in results:
        lines.append(f"### {r['name']} (`{r['path']}`)")
        lines.append(f"- HTTP: {r['status']}")
        if r.get("title"):
            lines.append(f"- Title ({r['title_len']}c): {r['title']}")
        if r.get("desc"):
            lines.append(f"- Description ({r['desc_len']}c): {r['desc'][:120]}")
        if r.get("h1"):
            lines.append(f"- H1: {r['h1'][:80]}")
        lines.append(f"- Canonical: {r.get('canonical', 'MISSING')}")
        lines.append(f"- Robots: {r.get('robots', 'N/A')}")
        lines.append(f"- Words: {r.get('words', 'N/A')}")
        if r["issues"]:
            lines.append(f"- **Issues:**")
            for issue in r["issues"]:
                lines.append(f"  - {issue}")
        lines.append("")

    lines += [
        f"---",
        f"Total issues: {total_issues}",
        f"*Generated by seo-check workflow*",
    ]

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nReport saved to {OUTPUT}")
    print(f"Total issues: {total_issues}")


if __name__ == "__main__":
    main()
