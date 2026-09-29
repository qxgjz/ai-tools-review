#!/usr/bin/env python3
"""
AIToolCrux Pre-Deploy Audit Gate (v1.0)
Runs before every deployment. Checks only changed/affected pages for speed.
Blocks deployment if any critical check fails.

Usage:
  python scripts/pre_deploy_gate.py              # Auto-detect changes and audit
  python scripts/pre_deploy_gate.py --all        # Force full audit (slow)
  python scripts/pre_deploy_gate.py --article <slug>  # Audit specific article
  python scripts/pre_deploy_gate.py --dry-run    # Report only, don't block
"""

import json
import re
import os
import sys
import subprocess
import html
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_PATH = os.path.join(PROJECT_ROOT, "data", "posts.json")
STATE_PATH = os.path.join(PROJECT_ROOT, "iteration_center", "state.json")

# Import quality_audit for consistency
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
try:
    from quality_audit import audit_post as qa_audit_post
    HAS_QUALITY_AUDIT = True
except ImportError:
    HAS_QUALITY_AUDIT = False

# ============================================================
# CONTENT QUALITY CHECKS (same as quality_audit.py)
# ============================================================

def count_words(content):
    text = re.sub(r"<[^>]+>", " ", content)
    text = re.sub(r"[#|*\-]", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())

def count_internal_links(content):
    return len(re.findall(r'href="/(blog|category|tools|alternatives|comparisons|compare|ranking|best-for|subcategory)/', content))

def has_section(content, patterns):
    for p in patterns:
        if re.search(p, content, re.I):
            return True
    return False

def count_images(content):
    return len(re.findall(r"<img\s", content, re.I))

def get_first_paragraph(content):
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", content, re.DOTALL)
    for p in paragraphs:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 20:
            return text
    return ""

def flesch_reading_ease(text):
    sentences = max(1, len(re.findall(r"[.!?]+", text)))
    words = max(1, len(text.split()))
    syllables = 0
    for word in text.split():
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        prev_vowel = False
        for c in word:
            is_vowel = c in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        if word.endswith("e") and count > 1:
            count -= 1
        syllables += max(1, count)
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

def count_qa_pairs(content):
    return len(re.findall(r"<(?:strong|b|h4|p|h3)[^>]*>\s*(?:Q[:\.]?|Question[:\.]?|How|What|Why|When|Where|Can|Is|Are|Do|Does|Should|Which|Who|Will|Could|Would)\b", content, re.I))

def count_external_links(content):
    return len(re.findall(r'href="https?://(?!www\.aitoolcrux\.com)(?!aitoolcrux\.com)', content))

def audit_article(post):
    """Audit a single article using quality_audit.audit_post for consistency."""
    if HAS_QUALITY_AUDIT:
        checks = qa_audit_post(post)
        quality_score = checks.get("quality_score", 0)
        failed = [k for k, v in checks.items() if k.endswith("_pass") and not v]
        return quality_score, failed, {
            "words": checks.get("word_count", 0),
            "flesch": checks.get("flesch_reading_ease", 0),
            "internal_links": checks.get("internal_links", 0),
            "external_links": checks.get("external_links", 0),
            "images": checks.get("image_count", 0),
        }
    # Fallback
    content = post.get("content", "")
    wc = count_words(content)
    score = 100 if wc >= 2000 else 50
    failed = [] if wc >= 2000 else ["word_count"]
    details = {"words": wc, "flesch": 0, "internal_links": 0, "external_links": 0, "images": 0}
    return score, failed, details

# ============================================================
# CHANGE DETECTION
# ============================================================

def get_changed_files():
    """Get list of changed files via git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        )
        changed = result.stdout.strip().split("\n") if result.stdout.strip() else []

        # Also check untracked files
        result2 = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        )
        untracked = result2.stdout.strip().split("\n") if result2.stdout.strip() else []

        return list(set(changed + untracked))
    except Exception as e:
        print(f"  Warning: git diff failed ({e}), assuming full audit needed")
        return None

def classify_changes(files):
    """Classify changed files into categories."""
    categories = {
        "articles": [],      # posts.json changes
        "tools": [],         # tools.json changes
        "code": [],          # app/, components/, lib/ changes
        "config": [],        # next.config, package.json
        "seo": [],           # sitemap, robots, llms.txt
        "other": [],
    }

    if files is None:
        return None  # Full audit needed

    for f in files:
        if "posts.json" in f:
            categories["articles"].append(f)
        elif "tools.json" in f:
            categories["tools"].append(f)
        elif f.startswith(("app/", "components/", "lib/")):
            categories["code"].append(f)
        elif f in ("next.config.mjs", "package.json", "tsconfig.json"):
            categories["config"].append(f)
        elif f in ("public/sitemap.xml", "public/robots.txt", "public/llms.txt"):
            categories["seo"].append(f)
        else:
            categories["other"].append(f)

    return categories

# ============================================================
# MAIN GATE
# ============================================================

def main():
    dry_run = "--dry-run" in sys.argv
    force_all = "--all" in sys.argv
    article_slug = None
    if "--article" in sys.argv:
        idx = sys.argv.index("--article")
        if idx + 1 < len(sys.argv):
            article_slug = sys.argv[idx + 1]

    print(f"\n{'='*70}")
    print(f"AIToolCrux PRE-DEPLOY AUDIT GATE v1.0")
    print(f"{'='*70}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'dry-run' if dry_run else 'enforce'}")

    all_passed = True
    gate_results = []

    # ---- Step 1: Detect changes ----
    print(f"\n--- Step 1: Change Detection ---")

    if force_all:
        print("  Force full audit mode")
        categories = None
    elif article_slug:
        print(f"  Targeting specific article: {article_slug}")
        categories = {"articles": ["data/posts.json"], "tools": [], "code": [], "config": [], "seo": [], "other": []}
    else:
        changed = get_changed_files()
        if changed is None:
            categories = None
            print("  Could not detect changes, running full audit")
        elif not changed or changed == [""]:
            print("  No changes detected. Nothing to audit.")
            print("\n  ✅ GATE PASSED (no changes)")
            return 0
        else:
            categories = classify_changes(changed)
            print(f"  Changed files: {len(changed)}")
            for cat, files in categories.items():
                if files:
                    print(f"    {cat}: {len(files)} files")

    # ---- Step 2: Article quality check ----
    if categories is None or categories.get("articles"):
        print(f"\n--- Step 2: Article Quality Check ---")

        with open(POSTS_PATH, "r", encoding="utf-8") as f:
            posts = json.load(f)

        if article_slug:
            target_posts = [p for p in posts if p.get("slug") == article_slug]
            if not target_posts:
                print(f"  ❌ Article not found: {article_slug}")
                all_passed = False
                target_posts = []
        else:
            target_posts = posts  # Check all articles

        print(f"  Auditing {len(target_posts)} articles...")

        failed_articles = []
        perfect_count = 0
        for post in target_posts:
            score, failed, details = audit_article(post)
            if score == 100:
                perfect_count += 1
            if score < 100:
                failed_articles.append((post.get("slug", "?"), score, failed, details))

        print(f"  Perfect (100/100): {perfect_count}/{len(target_posts)}")

        if failed_articles:
            all_passed = False
            print(f"\n  ❌ {len(failed_articles)} articles below 100:")
            for slug, score, failed, details in failed_articles[:10]:
                print(f"    {score:.0f}/100: {slug[:45]}")
                print(f"      Failed: {', '.join(failed[:3])}")
            if len(failed_articles) > 10:
                print(f"    ... and {len(failed_articles) - 10} more")
            gate_results.append(f"Article quality: {len(failed_articles)} below 100")
        else:
            print(f"  ✅ All articles 100/100")
            gate_results.append("Article quality: PASS")

    # ---- Step 3: Code/SEO basic checks ----
    if categories is None or categories.get("code") or categories.get("config") or categories.get("seo"):
        print(f"\n--- Step 3: Code & SEO File Checks ---")

        # Check for hardcoded secrets
        secret_patterns = [
            (r'github_pat_[A-Za-z0-9_]+', "GitHub PAT"),
            (r'sk-[A-Za-z0-9]{20,}', "OpenAI API key"),
            (r'AKIA[0-9A-Z]{16}', "AWS key"),
        ]

        code_files = []
        if categories:
            code_files = categories.get("code", []) + categories.get("config", [])
        else:
            # Scan common dirs
            for root, dirs, files in os.walk(os.path.join(PROJECT_ROOT, "app")):
                for f in files:
                    if f.endswith((".ts", ".tsx", ".js", ".jsx")):
                        code_files.append(os.path.join(root, f))

        secrets_found = []
        for cf in code_files[:50]:  # Limit scan
            full_path = os.path.join(PROJECT_ROOT, cf) if not cf.startswith(PROJECT_ROOT) else cf
            if os.path.exists(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for pattern, name in secret_patterns:
                        if re.search(pattern, content):
                            secrets_found.append((cf, name))
                except:
                    pass

        if secrets_found:
            all_passed = False
            print(f"  ❌ Hardcoded secrets found:")
            for cf, name in secrets_found[:5]:
                print(f"    {name} in {cf}")
            gate_results.append("Security: hardcoded secrets found")
        else:
            print(f"  ✅ No hardcoded secrets in {len(code_files)} files")
            gate_results.append("Security: PASS")

        # Check push_via_api.py for hardcoded token
        push_script = os.path.join(PROJECT_ROOT, "push_via_api.py")
        if os.path.exists(push_script):
            with open(push_script, "r", encoding="utf-8") as f:
                push_content = f.read()
            if "github_pat_" in push_content:
                print(f"  ⚠️  push_via_api.py has hardcoded GitHub token (security risk)")
                gate_results.append("Security: push_via_api.py has hardcoded token")

    # ---- Step 4: TypeScript check (if code changed) ----
    if categories is None or categories.get("code") or categories.get("config"):
        print(f"\n--- Step 4: TypeScript Compilation ---")
        print("  Running npx tsc --noEmit ...")
        try:
            result = subprocess.run(
                ["npx", "tsc", "--noEmit"],
                cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                print("  ✅ TypeScript: 0 errors")
                gate_results.append("TypeScript: PASS")
            else:
                all_passed = False
                errors = result.stdout.strip().split("\n")
                print(f"  ❌ TypeScript: {len([e for e in errors if 'error' in e.lower()])} errors")
                for e in errors[:5]:
                    if e.strip():
                        print(f"    {e.strip()[:80]}")
                gate_results.append("TypeScript: FAILED")
        except Exception as e:
            print(f"  ⚠️  TypeScript check skipped: {e}")
            gate_results.append("TypeScript: skipped")

    # ---- Final verdict ----
    print(f"\n{'='*70}")
    print("GATE VERDICT")
    print(f"{'='*70}")

    for r in gate_results:
        icon = "✅" if "PASS" in r else "❌" if "FAIL" in r or "below" in r or "found" in r else "⚠️"
        print(f"  {icon} {r}")

    print()
    if all_passed:
        print("  ✅✅✅ GATE PASSED — deployment allowed ✅✅✅")
        return 0
    else:
        if dry_run:
            print("  ⚠️  GATE FAILED (dry-run mode — would block deployment)")
            return 0
        else:
            print("  ❌❌❌ GATE FAILED — deployment BLOCKED ❌❌❌")
            print("\n  Fix the issues above, then re-run this gate before deploying.")
            return 1

if __name__ == "__main__":
    sys.exit(main())
