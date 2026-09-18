"""
Pre-commit quality check for AIToolCrux blog posts.
Checks each post in data/posts.json against quality gates.
Run: python pre_commit_check.py
"""
import json
import os
import re
import sys

PROJECT_ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
POSTS_FILE = os.path.join(PROJECT_ROOT, "data", "posts.json")

REQUIRED_CHECKS = {
    "quick_answer": "Has Quick Answer / TL;DR block",
    "min_internal_links": "Has at least 8 internal links",
    "has_affiliate_link": "Has at least 1 affiliate CTA link",
    "has_screenshot": "Has at least 1 screenshot/image",
}


def check_post(post: dict) -> dict:
    """Check a single post against quality gates."""
    content = post.get("content", "")
    title = post.get("title", "")
    slug = post.get("slug", "")
    issues = []

    # 1. Quick Answer check
    has_quick = bool(re.search(r"(?i)(quick answer|tl;dr|tldr|summary:|at a glance|in short)", content))
    if not has_quick:
        issues.append("MISSING_QUICK_ANSWER")

    # 2. Internal links check (links to aitoolcrux.com or /blog/ or /tools/)
    internal_links = re.findall(r'href=["\'](/[^"\']+|https?://www\.aitoolcrux\.com/[^"\']+)["\']', content)
    internal_count = len([l for l in internal_links if not l.startswith("http") or "aitoolcrux.com" in l])
    if internal_count < 8:
        issues.append(f"LOW_INTERNAL_LINKS({internal_count}/8)")

    # 3. Affiliate link check
    has_affiliate = bool(re.search(r'(?i)(affiliate|sponsored|rel=["\'][^"\']*sponsored|try now|visit.*official|start.*free.*trial)', content))
    if not has_affiliate:
        issues.append("NO_AFFILIATE_CTA")

    # 4. Screenshot check
    has_screenshot = bool(re.search(r'(?i)(screenshot|\.png|\.jpg|\.webp|img.*src.*screenshot|hasRealScreenshots)', content))
    if not has_screenshot:
        # Also check metadata
        if not post.get("hasRealScreenshots") or post.get("screenshotCount", 0) == 0:
            issues.append("NO_SCREENSHOT")

    return {
        "slug": slug,
        "title": title,
        "issues": issues,
        "pass": len(issues) == 0,
        "internal_links": internal_count,
    }


def main():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"Checking {len(posts)} posts...")
    results = []
    failed = 0
    for post in posts:
        r = check_post(post)
        results.append(r)
        if not r["pass"]:
            failed += 1
            print(f"  FAIL: {r['slug']} - {', '.join(r['issues'])}")

    print(f"\n=== Quality Check Summary ===")
    print(f"Total posts: {len(posts)}")
    print(f"Passed: {len(posts) - failed}")
    print(f"Failed: {failed}")
    print(f"Pass rate: {(len(posts)-failed)/len(posts)*100:.1f}%")

    # Group issues
    issue_counts = {}
    for r in results:
        for issue in r["issues"]:
            key = issue.split("(")[0]
            issue_counts[key] = issue_counts.get(key, 0) + 1
    if issue_counts:
        print(f"\nIssue breakdown:")
        for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"  {issue}: {count} posts")

    return failed


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
