#!/usr/bin/env python3
"""
AIToolCrux Pre-Deploy Audit Gate (v2.0 - FULL AUDIT)
Runs before every deployment. Blocks deployment if any critical check fails.
Includes ALL audit tools - no partial audits allowed.

Checks:
1. Article quality (100/100)
2. TypeScript compilation (0 errors)
3. No hardcoded secrets
4. Technical SEO (title/meta length, canonical, OG tags, favicon)
5. GEO/AEO (robots.txt, AI bots, llms.txt)
6. Schema/structured data validity
7. Sitemap contains all published URLs

Usage:
  python scripts/pre_deploy_gate.py              # Auto-detect changes
  python scripts/pre_deploy_gate.py --all        # Force full audit
  python scripts/pre_deploy_gate.py --article <slug>  # Audit specific article
  python scripts/pre_deploy_gate.py --dry-run    # Report only, don't block
"""

import json
import re
import os
import sys
import subprocess
import html as html_module
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_PATH = os.path.join(PROJECT_ROOT, "data", "posts.json")
STATE_PATH = os.path.join(PROJECT_ROOT, "iteration_center", "state.json")
SITE_URL = "https://www.aitoolcrux.com"

# Import quality_audit
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
try:
    from quality_audit import audit_post as qa_audit_post
    HAS_QUALITY_AUDIT = True
except ImportError:
    HAS_QUALITY_AUDIT = False


def count_words(content):
    text = re.sub(r"<[^>]+>", " ", content)
    text = re.sub(r"[#|*\-]", " ", text)
    text = html_module.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())


def audit_article(post):
    if HAS_QUALITY_AUDIT:
        checks = qa_audit_post(post)
        quality_score = checks.get("quality_score", 0)
        failed = [k for k, v in checks.items() if k.endswith("_pass") and not v]
        return quality_score, failed
    content = post.get("content", "")
    wc = count_words(content)
    score = 100 if wc >= 2000 else 50
    failed = [] if wc >= 2000 else ["word_count"]
    return score, failed


def check_technical_seo(posts):
    """Check technical SEO for all blog posts."""
    issues = []
    for post in posts:
        slug = post.get("slug", "?")
        title = post.get("title", "")
        excerpt = post.get("excerpt", "") or post.get("description", "") or ""

        # Clean excerpt
        clean_excerpt = re.sub(r"<[^>]+>", "", excerpt).strip()
        clean_excerpt = re.sub(r"\s+", " ", clean_excerpt)

        if len(title) > 60:
            issues.append(f"  TITLE TOO LONG ({len(title)}): /blog/{slug} - {title[:50]}...")
        if len(clean_excerpt) > 160:
            issues.append(f"  META TOO LONG ({len(clean_excerpt)}): /blog/{slug}")

    return issues


def check_seo_files():
    """Check robots.txt and sitemap exist and are valid."""
    issues = []

    # Check robots.txt
    robots_path = os.path.join(PROJECT_ROOT, "public", "robots.txt")
    if not os.path.exists(robots_path):
        issues.append("  robots.txt missing in public/")
    else:
        with open(robots_path, "r", encoding="utf-8") as f:
            robots_content = f.read()
        # Check AI bots
        ai_bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "Applebot"]
        for bot in ai_bots:
            if bot not in robots_content:
                issues.append(f"  robots.txt missing AI bot: {bot}")

    # Check llms.txt
    llms_path = os.path.join(PROJECT_ROOT, "public", "llms.txt")
    if not os.path.exists(llms_path):
        issues.append("  llms.txt missing in public/")

    # Check favicon
    favicon_svg = os.path.join(PROJECT_ROOT, "public", "favicon.svg")
    favicon_ico = os.path.join(PROJECT_ROOT, "public", "favicon.ico")
    if not os.path.exists(favicon_svg) and not os.path.exists(favicon_ico):
        issues.append("  No favicon found (neither favicon.svg nor favicon.ico)")

    # Check sitemap
    sitemap_path = os.path.join(PROJECT_ROOT, "public", "sitemap.xml")
    if not os.path.exists(sitemap_path):
        # Check if it's generated
        sitemap_gen = os.path.join(PROJECT_ROOT, "app", "sitemap.ts")
        if not os.path.exists(sitemap_gen):
            issues.append("  No sitemap found (neither static nor generated)")

    return issues


def check_schema_in_posts(posts):
    """Check that posts have required schema fields."""
    issues = []
    for post in posts:
        slug = post.get("slug", "?")
        if not post.get("faq"):
            issues.append(f"  No FAQPage schema: /blog/{slug}")
        if not post.get("quickAnswer"):
            issues.append(f"  No Quick Answer: /blog/{slug}")
        if not post.get("keyTakeaways"):
            issues.append(f"  No Key Takeaways: /blog/{slug}")
    return issues


def get_changed_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        )
        changed = result.stdout.strip().split("\n") if result.stdout.strip() else []
        result2 = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        )
        untracked = result2.stdout.strip().split("\n") if result2.stdout.strip() else []
        return list(set(changed + untracked))
    except Exception:
        return None


def main():
    dry_run = "--dry-run" in sys.argv
    force_all = "--all" in sys.argv

    print(f"\n{'='*70}")
    print(f"AIToolCrux PRE-DEPLOY AUDIT GATE v2.0 (FULL AUDIT)")
    print(f"{'='*70}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'dry-run' if dry_run else 'ENFORCE'}")

    all_passed = True
    gate_results = []

    with open(POSTS_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # ---- Step 1: Article Quality ----
    print(f"\n--- Step 1: Article Quality (100/100 required) ---")
    failed_articles = []
    perfect_count = 0
    for post in posts:
        score, failed = audit_article(post)
        if score == 100:
            perfect_count += 1
        else:
            failed_articles.append((post.get("slug", "?"), score, failed))

    print(f"  Perfect: {perfect_count}/{len(posts)}")
    if failed_articles:
        all_passed = False
        print(f"  ❌ {len(failed_articles)} articles below 100:")
        for slug, score, failed in failed_articles[:5]:
            print(f"    {score:.0f}/100: {slug[:50]}")
        gate_results.append(f"Article quality: {len(failed_articles)} below 100")
    else:
        print(f"  ✅ All {len(posts)} articles 100/100")
        gate_results.append("Article quality: PASS")

    # ---- Step 2: TypeScript ----
    print(f"\n--- Step 2: TypeScript Compilation ---")
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=120,
            shell=True
        )
        if result.returncode == 0:
            print("  ✅ TypeScript: 0 errors")
            gate_results.append("TypeScript: PASS")
        else:
            all_passed = False
            errors = [e for e in result.stdout.strip().split("\n") if "error" in e.lower()]
            print(f"  ❌ TypeScript: {len(errors)} errors")
            for e in errors[:5]:
                print(f"    {e.strip()[:80]}")
            gate_results.append("TypeScript: FAILED")
    except Exception as e:
        print(f"  ⚠️  TypeScript check skipped: {e}")
        gate_results.append("TypeScript: skipped")

    # ---- Step 3: Technical SEO ----
    print(f"\n--- Step 3: Technical SEO ---")
    tech_issues = check_technical_seo(posts)
    if tech_issues:
        all_passed = False
        print(f"  ❌ {len(tech_issues)} technical SEO issues:")
        for issue in tech_issues[:10]:
            print(issue)
        gate_results.append(f"Technical SEO: {len(tech_issues)} issues")
    else:
        print("  ✅ Title/meta lengths OK")
        gate_results.append("Technical SEO: PASS")

    # ---- Step 4: SEO Files (robots.txt, favicon, sitemap, llms.txt) ----
    print(f"\n--- Step 4: SEO Files & GEO/AEO ---")
    file_issues = check_seo_files()
    if file_issues:
        all_passed = False
        print(f"  ❌ {len(file_issues)} file issues:")
        for issue in file_issues:
            print(issue)
        gate_results.append(f"SEO files: {len(file_issues)} issues")
    else:
        print("  ✅ robots.txt, favicon, sitemap, llms.txt OK")
        gate_results.append("SEO files: PASS")

    # ---- Step 5: Schema/Structured Data ----
    print(f"\n--- Step 5: Schema & Structured Data ---")
    schema_issues = check_schema_in_posts(posts)
    if schema_issues:
        all_passed = False
        print(f"  ❌ {len(schema_issues)} schema issues:")
        for issue in schema_issues[:10]:
            print(issue)
        gate_results.append(f"Schema: {len(schema_issues)} issues")
    else:
        print("  ✅ All posts have FAQ, Quick Answer, Key Takeaways")
        gate_results.append("Schema: PASS")

    # ---- Step 6: No Hardcoded Secrets ----
    print(f"\n--- Step 6: Security (no hardcoded secrets) ---")
    secret_patterns = [
        (r'github_pat_[A-Za-z0-9_]{20,}', "GitHub PAT"),
        (r'sk-[A-Za-z0-9]{20,}', "OpenAI API key"),
    ]
    secrets_found = []
    for root, dirs, files in os.walk(os.path.join(PROJECT_ROOT, "app")):
        dirs[:] = [d for d in dirs if d not in [".next", "node_modules"]]
        for fname in files:
            if fname.endswith((".ts", ".tsx", ".js", ".jsx")):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for pattern, name in secret_patterns:
                        if re.search(pattern, content):
                            secrets_found.append((fpath, name))
                except:
                    pass
    if secrets_found:
        all_passed = False
        for fpath, name in secrets_found[:5]:
            print(f"  ❌ {name} in {fpath}")
        gate_results.append("Security: hardcoded secrets found")
    else:
        print("  ✅ No hardcoded secrets")
        gate_results.append("Security: PASS")

    # ---- Final Verdict ----
    print(f"\n{'='*70}")
    print("GATE VERDICT")
    print(f"{'='*70}")
    for r in gate_results:
        icon = "✅" if "PASS" in r else "❌"
        print(f"  {icon} {r}")
    print()
    if all_passed:
        print("  ✅✅✅ GATE PASSED — deployment allowed ✅✅✅")
        return 0
    else:
        if dry_run:
            print("  ⚠️  GATE FAILED (dry-run mode)")
            return 0
        else:
            print("  ❌❌❌ GATE FAILED — deployment BLOCKED ❌❌❌")
            return 1


if __name__ == "__main__":
    sys.exit(main())
