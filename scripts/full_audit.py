#!/usr/bin/env python3
"""
AIToolCrux Full Site Audit (v1.0)
Unified audit covering all 753+ pages from sitemap.xml.
Integrates: Technical SEO + Content Quality + GEO/AI Citation + Broken Links + Accessibility

Usage:
  python scripts/full_audit.py                  # Full audit (all pages)
  python scripts/full_audit.py --quick          # Quick audit (sample 50 pages)
  python scripts/full_audit.py --content-only   # Only content quality (local, no crawl)
  python scripts/full_audit.py --fail-on-error  # Exit 1 if any critical issue
"""

import json
import re
import os
import sys
import time
import html
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from collections import defaultdict
from urllib.parse import urljoin, urlparse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_PATH = os.path.join(PROJECT_ROOT, "data", "posts.json")
REPORT_PATH = os.path.join(PROJECT_ROOT, "iteration_center", "full_audit_report.md")
JSON_REPORT_PATH = os.path.join(PROJECT_ROOT, "iteration_center", "full_audit_results.json")

# Import quality_audit functions for consistency
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
try:
    from quality_audit import audit_post as qa_audit_post
    HAS_QUALITY_AUDIT = True
except ImportError:
    HAS_QUALITY_AUDIT = False
    print("WARNING: Could not import quality_audit.audit_post, using fallback")

BASE_URL = "https://www.aitoolcrux.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ============================================================
# 1. SITEMAP FETCH
# ============================================================

def get_all_urls():
    """Fetch all URLs from sitemap.xml."""
    try:
        r = requests.get(f"{BASE_URL}/sitemap.xml", headers=HEADERS, timeout=30)
        urls = re.findall(r"<loc>(.*?)</loc>", r.text)
        return [u.strip() for u in urls]
    except Exception as e:
        print(f"ERROR fetching sitemap: {e}")
        return []

# ============================================================
# 2. CONTENT QUALITY AUDIT (local, no crawl)
# ============================================================

def count_words(content):
    text = re.sub(r"<[^>]+>", " ", content)
    text = re.sub(r"[#|*\-]", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())

def count_internal_links(content):
    html_links = len(re.findall(r'href="/(blog|category|tools|alternatives|comparisons|compare|ranking|best-for|subcategory)/', content))
    md_links = len(re.findall(r"\]\(/(blog|category|tools|alternatives|comparisons|compare|ranking|best-for|subcategory)/", content))
    return html_links + md_links

def has_section(content, patterns):
    for p in patterns:
        if re.search(p, content, re.I):
            return True
    return False

def count_images(content):
    return len(re.findall(r"<img\s", content, re.I)) + len(re.findall(r"!\[.*?\]\(.*?\)", content))

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
    html_q = len(re.findall(r"<(?:strong|b|h4|p|h3)[^>]*>\s*(?:Q[:\.]?|Question[:\.]?|How|What|Why|When|Where|Can|Is|Are|Do|Does|Should|Which|Who|Will|Could|Would)\b", content, re.I))
    md_q = len(re.findall(r"(?:\*\*|\#\#\#)\s*(?:Q[:\.]?|Question[:\.]?|How|What|Why|When|Where|Can|Is|Are|Do|Does|Should|Which|Who|Will|Could|Would)\b", content, re.I))
    return html_q + md_q

def count_external_links(content):
    html_ext = len(re.findall(r'href="https?://(?!www\.aitoolcrux\.com)(?!aitoolcrux\.com)', content))
    return html_ext

def audit_content_quality():
    """Audit all articles from posts.json using quality_audit.audit_post for consistency."""
    print("\n" + "=" * 70)
    print("PHASE 1: CONTENT QUALITY AUDIT (all articles, quality_audit.py standard)")
    print("=" * 70)

    with open(POSTS_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    results = []
    for post in posts:
        if HAS_QUALITY_AUDIT:
            checks = qa_audit_post(post)
            quality_score = checks.get("quality_score", 0)
            failed = [k for k, v in checks.items() if k.endswith("_pass") and not v]
            results.append({
                "slug": post.get("slug", ""),
                "title": post.get("title", ""),
                "quality_score": quality_score,
                "word_count": checks.get("word_count", 0),
                "flesch": checks.get("flesch_reading_ease", 0),
                "internal_links": checks.get("internal_links", 0),
                "external_links": checks.get("external_links", 0),
                "images": checks.get("image_count", 0),
                "failed_checks": failed,
            })
        else:
            # Fallback: basic checks
            content = post.get("content", "")
            wc = count_words(content)
            results.append({
                "slug": post.get("slug", ""),
                "title": post.get("title", ""),
                "quality_score": 100 if wc >= 2000 else 50,
                "word_count": wc,
                "flesch": 0,
                "internal_links": count_internal_links(content),
                "external_links": count_external_links(content),
                "images": count_images(content),
                "failed_checks": [] if wc >= 2000 else ["word_count"],
            })

    avg_score = sum(r["quality_score"] for r in results) / len(results) if results else 0
    perfect = sum(1 for r in results if r["quality_score"] == 100)
    below_85 = sum(1 for r in results if r["quality_score"] < 85)

    print(f"  Articles audited: {len(results)}")
    print(f"  Average score: {avg_score:.1f}/100")
    print(f"  Perfect (100/100): {perfect}")
    print(f"  Below 85: {below_85}")

    if below_85 > 0:
        print(f"\n  ⚠️  Articles below 85:")
        for r in sorted(results, key=lambda x: x["quality_score"]):
            if r["quality_score"] < 85:
                print(f"    {r['quality_score']:.0f}: {r['slug'][:50]} - failed: {', '.join(r['failed_checks'][:3])}")

    return {
        "total_articles": len(results),
        "average_score": avg_score,
        "perfect_count": perfect,
        "below_85_count": below_85,
        "articles": results,
    }

# ============================================================
# 3. TECHNICAL SEO AUDIT (crawl all pages)
# ============================================================

def audit_page_technical(url):
    """Audit a single page for technical SEO issues."""
    issues = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        content = r.text
        status = r.status_code

        if status != 200:
            issues.append(("critical", f"HTTP {status}", url))
            return issues

        # Title
        title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.I | re.DOTALL)
        if not title_match:
            issues.append(("critical", "Missing <title>", url))
        else:
            title = title_match.group(1).strip()
            if len(title) < 30:
                issues.append(("warning", f"Title too short ({len(title)}): {title[:40]}", url))
            elif len(title) > 60:
                issues.append(("warning", f"Title too long ({len(title)}): {title[:40]}", url))

        # Meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.I)
        if not desc_match:
            issues.append(("critical", "Missing meta description", url))
        else:
            desc = desc_match.group(1).strip()
            if len(desc) < 70:
                issues.append(("warning", f"Meta too short ({len(desc)})", url))
            elif len(desc) > 160:
                issues.append(("warning", f"Meta too long ({len(desc)})", url))

        # Canonical
        canonical_match = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.I)
        if not canonical_match:
            issues.append(("warning", "Missing canonical tag", url))
        else:
            canonical = canonical_match.group(1)
            if canonical != url and canonical != url + "/":
                issues.append(("notice", f"Canonical mismatch: {canonical}", url))

        # H1
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", content, re.I | re.DOTALL)
        if len(h1s) == 0:
            issues.append(("critical", "Missing H1", url))
        elif len(h1s) > 1:
            issues.append(("warning", f"Multiple H1 ({len(h1s)})", url))

        # Heading order
        headings = re.findall(r"<h([1-6])[^>]*>", content, re.I)
        levels = [int(h) for h in headings]
        for i in range(1, len(levels)):
            if levels[i] > levels[i-1] + 1:
                issues.append(("notice", f"Heading skip: H{levels[i-1]} -> H{levels[i]}", url))
                break

        # Images without alt
        imgs = re.findall(r"<img[^>]*>", content, re.I)
        no_alt = [img for img in imgs if not re.search(r'\salt=["\']', img, re.I)]
        if no_alt:
            issues.append(("warning", f"{len(no_alt)}/{len(imgs)} images missing alt", url))

        # Structured data
        json_ld = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.I | re.DOTALL)
        if not json_ld:
            issues.append(("notice", "No JSON-LD structured data", url))

        # Broken internal links (sample)
        internal_links = re.findall(r'href=["\'](/[^"\']+)["\']', content)
        # Only check first 5 to avoid too many requests
        for link in internal_links[:5]:
            if link.startswith("//") or link.startswith("#"):
                continue
            full_url = urljoin(BASE_URL, link)
            if "aitoolcrux.com" in full_url:
                try:
                    lr = requests.head(full_url, headers=HEADERS, timeout=10, allow_redirects=True)
                    if lr.status_code >= 400:
                        issues.append(("critical", f"Broken internal link: {link} ({lr.status_code})", url))
                except:
                    pass

        # Response time
        response_time = r.elapsed.total_seconds() * 1000
        if response_time > 3000:
            issues.append(("warning", f"Slow response: {response_time:.0f}ms", url))

    except Exception as e:
        issues.append(("critical", f"Fetch error: {str(e)[:50]}", url))

    return issues

def audit_technical_seo(urls, quick=False):
    """Crawl all pages and audit technical SEO."""
    print("\n" + "=" * 70)
    print("PHASE 2: TECHNICAL SEO AUDIT (crawling pages)")
    print("=" * 70)

    if quick:
        # Sample: homepage + 5 tools + 5 blog + 5 categories
        tools = [u for u in urls if "/tools/" in u][:5]
        blogs = [u for u in urls if "/blog/" in u][:5]
        cats = [u for u in urls if "/category/" in u or "/subcategory/" in u][:5]
        others = [u for u in urls if u not in tools + blogs + cats][:5]
        audit_urls = [BASE_URL + "/"] + tools + blogs + cats + others
        audit_urls = list(dict.fromkeys(audit_urls))  # dedupe
        print(f"  Quick mode: auditing {len(audit_urls)} sample pages")
    else:
        audit_urls = urls
        print(f"  Full mode: auditing {len(audit_urls)} pages")

    all_issues = []
    start = time.time()
    completed = 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(audit_page_technical, url): url for url in audit_urls}
        for future in as_completed(futures):
            completed += 1
            issues = future.result()
            all_issues.extend(issues)
            if completed % 50 == 0:
                elapsed = time.time() - start
                rate = completed / elapsed if elapsed > 0 else 0
                print(f"  Progress: {completed}/{len(audit_urls)} ({rate:.0f} pages/s)")

    elapsed = time.time() - start
    print(f"\n  Completed in {elapsed:.0f}s")

    # Summarize
    by_severity = defaultdict(int)
    by_type = defaultdict(int)
    for sev, msg, url in all_issues:
        by_severity[sev] += 1
        # Extract issue type from message
        issue_type = msg.split(":")[0].split("(")[0].strip()
        by_type[issue_type] += 1

    print(f"\n  Issues by severity:")
    for sev in ["critical", "warning", "notice"]:
        print(f"    {sev}: {by_severity.get(sev, 0)}")

    print(f"\n  Top issue types:")
    for itype, count in sorted(by_type.items(), key=lambda x: -x[1])[:10]:
        print(f"    {count}: {itype}")

    # Show critical issues
    critical = [(sev, msg, url) for sev, msg, url in all_issues if sev == "critical"]
    if critical:
        print(f"\n  ⚠️  CRITICAL ISSUES ({len(critical)}):")
        for sev, msg, url in critical[:20]:
            short_url = url.replace(BASE_URL, "")
            print(f"    {short_url[:50]}: {msg[:60]}")

    return {
        "pages_audited": len(audit_urls),
        "total_issues": len(all_issues),
        "by_severity": dict(by_severity),
        "by_type": dict(by_type),
        "critical_issues": critical[:50],
        "all_issues": all_issues,
        "elapsed_seconds": round(elapsed, 1),
    }

# ============================================================
# 4. GEO / AI CITATION AUDIT
# ============================================================

def audit_geo():
    """Check GEO/AI citation readiness."""
    print("\n" + "=" * 70)
    print("PHASE 3: GEO / AI CITATION AUDIT")
    print("=" * 70)

    findings = []

    # robots.txt
    try:
        r = requests.get(f"{BASE_URL}/robots.txt", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            robots = r.text
            findings.append(("good", "robots.txt found", ""))
            # Check AI crawlers
            ai_crawlers = ["GPTBot", "ClaudeBot", "Claude-Web", "PerplexityBot",
                          "Google-Extended", "Applebot", "OAI-SearchBot", "CCBot"]
            for crawler in ai_crawlers:
                if crawler in robots:
                    findings.append(("good", f"AI crawler configured: {crawler}", ""))
        else:
            findings.append(("critical", f"robots.txt returned {r.status_code}", ""))
    except Exception as e:
        findings.append(("critical", f"robots.txt error: {e}", ""))

    # llms.txt
    try:
        r = requests.get(f"{BASE_URL}/llms.txt", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            findings.append(("good", f"llms.txt found ({len(r.text)} bytes)", ""))
        else:
            findings.append(("warning", f"llms.txt returned {r.status_code}", ""))
    except:
        findings.append(("warning", "llms.txt not accessible", ""))

    # Check a sample page for GEO features
    sample_urls = [BASE_URL + "/", BASE_URL + "/tools/midjourney",
                   BASE_URL + "/blog/best-ai-image-generators-2026"]
    for url in sample_urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            content = r.text
            # Check for structured data
            if "application/ld+json" in content:
                findings.append(("good", f"JSON-LD present: {url.replace(BASE_URL,'')}", ""))
            # Check for FAQ schema
            if "FAQPage" in content:
                findings.append(("good", f"FAQPage schema: {url.replace(BASE_URL,'')}", ""))
            # Check for Article schema
            if '"Article"' in content or '"BlogPosting"' in content:
                findings.append(("good", f"Article schema: {url.replace(BASE_URL,'')}", ""))
        except:
            pass

    for sev, msg, _ in findings:
        icon = "✅" if sev == "good" else "⚠️" if sev == "warning" else "❌"
        print(f"  {icon} {msg}")

    good_count = sum(1 for s, _, _ in findings if s == "good")
    geo_score = round(good_count / len(findings) * 100) if findings else 0
    print(f"\n  GEO Score: {geo_score}/100")

    return {"geo_score": geo_score, "findings": findings}

# ============================================================
# 5. MAIN
# ============================================================

def main():
    quick = "--quick" in sys.argv
    content_only = "--content-only" in sys.argv
    fail_on_error = "--fail-on-error" in sys.argv

    print(f"\n{'#'*70}")
    print(f"# AIToolCrux FULL SITE AUDIT v1.0")
    print(f"# {'Quick mode' if quick else 'Full mode'}")
    print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*70}")

    # Phase 1: Content quality (always)
    content_results = audit_content_quality()

    # Phase 2 & 3: Technical SEO + GEO (skip if content-only)
    tech_results = None
    geo_results = None
    if not content_only:
        urls = get_all_urls()
        print(f"\n  Found {len(urls)} URLs in sitemap")

        if urls:
            tech_results = audit_technical_seo(urls, quick=quick)
            geo_results = audit_geo()
        else:
            print("  ERROR: Could not fetch sitemap, skipping technical audit")

    # Generate report
    print("\n" + "=" * 70)
    print("GENERATING REPORT")
    print("=" * 70)

    report_lines = [
        f"# AIToolCrux Full Site Audit Report",
        f"",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Mode:** {'Quick' if quick else 'Full'}",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Articles | {content_results['total_articles']} |",
        f"| Avg content score | {content_results['average_score']:.1f}/100 |",
        f"| Perfect articles | {content_results['perfect_count']} |",
        f"| Articles below 85 | {content_results['below_85_count']} |",
    ]

    if tech_results:
        report_lines.extend([
            f"| Pages audited | {tech_results['pages_audited']} |",
            f"| Technical issues | {tech_results['total_issues']} |",
            f"| Critical issues | {tech_results['by_severity'].get('critical', 0)} |",
            f"| Audit duration | {tech_results['elapsed_seconds']}s |",
        ])

    if geo_results:
        report_lines.append(f"| GEO score | {geo_results['geo_score']}/100 |")

    report_lines.extend([
        f"",
        f"## Content Quality Details",
        f"",
        f"| Slug | Score | Words | Flesch | Links | Failed |",
        f"|------|-------|-------|--------|-------|--------|",
    ])

    for r in sorted(content_results["articles"], key=lambda x: x["quality_score"]):
        failed_str = ", ".join(r["failed_checks"][:3]) if r["failed_checks"] else "—"
        report_lines.append(
            f"| {r['slug'][:35]} | {r['quality_score']:.0f} | {r['word_count']} | "
            f"{r['flesch']} | {r['internal_links']} | {failed_str} |"
        )

    if tech_results and tech_results["critical_issues"]:
        report_lines.extend([
            f"",
            f"## Critical Technical Issues",
            f"",
        ])
        for sev, msg, url in tech_results["critical_issues"][:30]:
            short_url = url.replace(BASE_URL, "")
            report_lines.append(f"- `{short_url[:50]}`: {msg}")

    if geo_results:
        report_lines.extend([
            f"",
            f"## GEO / AI Citation",
            f"",
        ])
        for sev, msg, _ in geo_results["findings"]:
            icon = "✅" if sev == "good" else "⚠️" if sev == "warning" else "❌"
            report_lines.append(f"- {icon} {msg}")

    report = "\n".join(report_lines)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Report: {REPORT_PATH}")

    # Save JSON results
    json_results = {
        "audit_time": datetime.now().isoformat(),
        "mode": "quick" if quick else "full",
        "content": content_results,
        "technical": tech_results,
        "geo": geo_results,
    }
    # Remove large fields for JSON
    if tech_results:
        json_results["technical"].pop("all_issues", None)
    with open(JSON_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(json_results, f, ensure_ascii=False, indent=2)
    print(f"  JSON: {JSON_REPORT_PATH}")

    # Final verdict
    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)

    has_critical = (content_results["below_85_count"] > 0 or
                    (tech_results and tech_results["by_severity"].get("critical", 0) > 0))

    if has_critical:
        print("  ❌ AUDIT FAILED — critical issues found, deployment blocked")
        if fail_on_error:
            sys.exit(1)
    else:
        print("  ✅ AUDIT PASSED — ready for deployment")

    return 0

if __name__ == "__main__":
    sys.exit(main())
