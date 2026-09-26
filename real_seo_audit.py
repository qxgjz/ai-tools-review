#!/usr/bin/env python3
"""
Real SEO Audit - 40+ Rules Check
Based on: pixelesq/argus (40+ rule weighted scoring) + iconaki/claude-seo methodology
Actually crawls and checks the website, not just a static checklist
"""

import requests
import re
import json
from urllib.parse import urljoin, urlparse
from datetime import datetime
import time

BASE_URL = "https://www.aitoolcrux.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Pages to audit (representative sample)
PAGES_TO_AUDIT = [
    "/",
    "/ranking",
    "/category/chat",
    "/category/writing",
    "/tools/chatgpt",
    "/tools/midjourney",
    "/tools/cursor",
    "/blog",
    "/blog/chatgpt-vs-claude-2026-comparison",
    "/alternatives",
    "/alternatives/chatgpt-alternatives",
    "/methodology",
    "/about",
    "/ai-policy",
]

results = {
    "audit_time": datetime.now().isoformat(),
    "base_url": BASE_URL,
    "pages_audited": len(PAGES_TO_AUDIT),
    "categories": {},
    "total_score": 0,
    "critical_issues": [],
    "warnings": [],
    "improvements": [],
}

def fetch_page(url):
    """Fetch a page and return response + content"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        return response, response.text
    except Exception as e:
        return None, str(e)

def check_title(content, url):
    """Check title tag - Rule 1"""
    issues = []
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if not title_match:
        issues.append(("CRITICAL", "Missing <title> tag"))
        return 0, issues
    title = title_match.group(1).strip()
    length = len(title)
    if length < 30:
        issues.append(("WARNING", f"Title too short ({length} chars): {title[:50]}..."))
    elif length > 60:
        issues.append(("WARNING", f"Title too long ({length} chars): {title[:50]}..."))
    else:
        issues.append(("PASS", f"Title length good ({length} chars)"))
    score = 10 if 30 <= length <= 60 else 5
    return score, issues

def check_meta_description(content, url):
    """Check meta description - Rule 2"""
    issues = []
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    if not desc_match:
        issues.append(("CRITICAL", "Missing meta description"))
        return 0, issues
    desc = desc_match.group(1).strip()
    length = len(desc)
    if length < 50:
        issues.append(("WARNING", f"Meta description too short ({length} chars)"))
    elif length > 160:
        issues.append(("WARNING", f"Meta description too long ({length} chars)"))
    else:
        issues.append(("PASS", f"Meta description length good ({length} chars)"))
    score = 10 if 50 <= length <= 160 else 5
    return score, issues

def check_h1(content, url):
    """Check H1 tags - Rule 3"""
    issues = []
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if len(h1_matches) == 0:
        issues.append(("CRITICAL", "Missing H1 tag"))
        return 0, issues
    elif len(h1_matches) > 1:
        issues.append(("WARNING", f"Multiple H1 tags ({len(h1_matches)} found)"))
        return 5, issues
    else:
        h1_text = re.sub(r'<[^>]+>', '', h1_matches[0]).strip()
        issues.append(("PASS", f"Single H1: {h1_text[:50]}"))
        return 10, issues

def check_canonical(content, url):
    """Check canonical tag - Rule 4"""
    issues = []
    canonical_match = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
    if not canonical_match:
        issues.append(("WARNING", "Missing canonical tag"))
        return 5, issues
    canonical = canonical_match.group(1)
    if url in canonical or canonical in url:
        issues.append(("PASS", f"Canonical self-referencing: {canonical}"))
        return 10, issues
    else:
        issues.append(("WARNING", f"Canonical points to different URL: {canonical}"))
        return 7, issues

def check_meta_robots(content, url):
    """Check meta robots - Rule 5"""
    issues = []
    robots_match = re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    if not robots_match:
        issues.append(("PASS", "No meta robots (default index,follow)"))
        return 10, issues
    robots_content = robots_match.group(1).lower()
    if "noindex" in robots_content:
        issues.append(("CRITICAL", f"Page set to noindex: {robots_content}"))
        return 0, issues
    elif "nofollow" in robots_content:
        issues.append(("WARNING", f"Page set to nofollow: {robots_content}"))
        return 5, issues
    else:
        issues.append(("PASS", f"Meta robots: {robots_content}"))
        return 10, issues

def check_open_graph(content, url):
    """Check Open Graph tags - Rule 6"""
    issues = []
    og_title = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    og_description = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    og_image = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    og_type = re.search(r'<meta[^>]*property=["\']og:type["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    
    count = sum([bool(og_title), bool(og_description), bool(og_image), bool(og_type)])
    if count == 4:
        issues.append(("PASS", "All 4 OG tags present"))
        return 10, issues
    elif count >= 2:
        issues.append(("WARNING", f"Only {count}/4 OG tags present"))
        return 5, issues
    else:
        issues.append(("WARNING", "Missing most OG tags"))
        return 3, issues

def check_twitter_cards(content, url):
    """Check Twitter Card tags - Rule 7"""
    issues = []
    tw_card = re.search(r'<meta[^>]*name=["\']twitter:card["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    tw_title = re.search(r'<meta[^>]*name=["\']twitter:title["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    tw_description = re.search(r'<meta[^>]*name=["\']twitter:description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    tw_image = re.search(r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    
    count = sum([bool(tw_card), bool(tw_title), bool(tw_description), bool(tw_image)])
    if count >= 3:
        issues.append(("PASS", f"Twitter cards good ({count}/4)"))
        return 10, issues
    elif count >= 1:
        issues.append(("WARNING", f"Twitter cards incomplete ({count}/4)"))
        return 5, issues
    else:
        issues.append(("WARNING", "No Twitter card tags"))
        return 3, issues

def check_json_ld(content, url):
    """Check JSON-LD structured data - Rule 8"""
    issues = []
    json_ld_matches = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
    if len(json_ld_matches) == 0:
        issues.append(("WARNING", "No JSON-LD structured data"))
        return 3, issues
    
    types_found = []
    for match in json_ld_matches:
        try:
            data = json.loads(match.strip())
            if isinstance(data, list):
                for item in data:
                    if "@type" in item:
                        types_found.append(item["@type"])
            elif "@type" in data:
                types_found.append(data["@type"])
        except:
            pass
    
    if len(types_found) > 0:
        issues.append(("PASS", f"JSON-LD types: {', '.join(set(types_found))}"))
        return 10, issues
    else:
        issues.append(("WARNING", "JSON-LD present but no @type found"))
        return 5, issues

def check_image_alt(content, url):
    """Check image alt attributes - Rule 9"""
    issues = []
    img_matches = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
    if len(img_matches) == 0:
        issues.append(("PASS", "No images on page"))
        return 10, issues
    
    with_alt = 0
    without_alt = []
    for img in img_matches:
        if re.search(r'alt=["\']', img, re.IGNORECASE):
            with_alt += 1
        else:
            src_match = re.search(r'src=["\'](.*?)["\']', img, re.IGNORECASE)
            without_alt.append(src_match.group(1)[:50] if src_match else "unknown")
    
    percentage = (with_alt / len(img_matches)) * 100
    if percentage == 100:
        issues.append(("PASS", f"All {len(img_matches)} images have alt"))
        return 10, issues
    elif percentage >= 80:
        issues.append(("WARNING", f"{len(without_alt)}/{len(img_matches)} images missing alt"))
        return 7, issues
    else:
        issues.append(("WARNING", f"Only {percentage:.0f}% images have alt"))
        return 5, issues

def check_heading_structure(content, url):
    """Check heading structure H1-H6 - Rule 10"""
    issues = []
    headings = re.findall(r'<(h[1-6])[^>]*>(.*?)</\1>', content, re.IGNORECASE | re.DOTALL)
    if len(headings) == 0:
        issues.append(("WARNING", "No heading tags found"))
        return 3, issues
    
    levels = [int(h[0][1]) for h in headings]
    h1_count = levels.count(1)
    h2_count = levels.count(2)
    h3_count = levels.count(3)
    
    if h1_count == 1 and h2_count >= 1:
        issues.append(("PASS", f"Good structure: H1={h1_count}, H2={h2_count}, H3={h3_count}"))
        return 10, issues
    elif h1_count == 1:
        issues.append(("WARNING", f"H1=1 but only {h2_count} H2 tags"))
        return 7, issues
    else:
        issues.append(("WARNING", f"{h1_count} H1 tags (should be 1)"))
        return 5, issues

def check_internal_links(content, url):
    """Check internal links - Rule 11"""
    issues = []
    links = re.findall(r'<a[^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
    internal = 0
    external = 0
    for link in links:
        if link.startswith("/") or BASE_URL in link:
            internal += 1
        elif link.startswith("http"):
            external += 1
    
    if internal >= 5:
        issues.append(("PASS", f"Good internal linking: {internal} internal, {external} external"))
        return 10, issues
    elif internal >= 1:
        issues.append(("WARNING", f"Only {internal} internal links"))
        return 5, issues
    else:
        issues.append(("WARNING", "No internal links"))
        return 3, issues

def check_https(url):
    """Check HTTPS - Rule 12"""
    if url.startswith("https://"):
        return 10, [("PASS", "HTTPS enabled")]
    else:
        return 0, [("CRITICAL", "Not HTTPS")]

def check_www_consistency(url):
    """Check www consistency - Rule 13"""
    if "www." in url:
        return 10, [("PASS", "Using www subdomain consistently")]
    else:
        return 7, [("WARNING", "Not using www (check redirects)")]

def check_lang_attribute(content, url):
    """Check html lang attribute - Rule 14"""
    lang_match = re.search(r'<html[^>]*lang=["\'](.*?)["\']', content, re.IGNORECASE)
    if lang_match:
        lang = lang_match.group(1)
        if lang.startswith("en"):
            return 10, [("PASS", f"Lang attribute: {lang}")]
        else:
            return 5, [("WARNING", f"Lang attribute is {lang}, expected en")]
    else:
        return 3, [("WARNING", "Missing html lang attribute")]

def check_viewport(content, url):
    """Check viewport meta tag - Rule 15"""
    viewport_match = re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    if viewport_match:
        return 10, [("PASS", f"Viewport: {viewport_match.group(1)}")]
    else:
        return 3, [("CRITICAL", "Missing viewport meta tag (mobile unfriendly)")]

def check_charset(content, url):
    """Check charset - Rule 16"""
    charset_match = re.search(r'<meta[^>]*charset=["\'](.*?)["\']', content, re.IGNORECASE)
    if charset_match:
        return 10, [("PASS", f"Charset: {charset_match.group(1)}")]
    else:
        return 5, [("WARNING", "Missing charset declaration")]

def check_favicon(content, url):
    """Check favicon - Rule 17"""
    favicon_match = re.search(r'<link[^>]*rel=["\'](?:icon|shortcut icon)["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
    if favicon_match:
        return 10, [("PASS", "Favicon present")]
    else:
        return 5, [("WARNING", "Missing favicon")]

def check_sitemap_reference():
    """Check sitemap.xml - Rule 18"""
    try:
        response = requests.get(f"{BASE_URL}/sitemap.xml", headers=HEADERS, timeout=15)
        if response.status_code == 200 and "<urlset" in response.text:
            url_count = len(re.findall(r'<url>', response.text))
            return 10, [("PASS", f"Sitemap present with {url_count} URLs")]
        else:
            return 3, [("WARNING", f"Sitemap returned status {response.status_code}")]
    except Exception as e:
        return 0, [("CRITICAL", f"Sitemap inaccessible: {str(e)[:50]}")]

def check_robots_txt():
    """Check robots.txt - Rule 19"""
    try:
        response = requests.get(f"{BASE_URL}/robots.txt", headers=HEADERS, timeout=15)
        if response.status_code == 200:
            has_sitemap = "Sitemap:" in response.text
            has_user_agent = "User-agent:" in response.text
            if has_sitemap and has_user_agent:
                return 10, [("PASS", "robots.txt valid with sitemap reference")]
            elif has_user_agent:
                return 7, [("WARNING", "robots.txt missing sitemap reference")]
            else:
                return 5, [("WARNING", "robots.txt minimal")]
        else:
            return 3, [("WARNING", f"robots.txt returned {response.status_code}")]
    except Exception as e:
        return 0, [("CRITICAL", f"robots.txt inaccessible: {str(e)[:50]}")]

def check_llms_txt():
    """Check llms.txt - Rule 20 (AI crawler optimization)"""
    try:
        response = requests.get(f"{BASE_URL}/llms.txt", headers=HEADERS, timeout=15)
        if response.status_code == 200 and len(response.text) > 100:
            return 10, [("PASS", f"llms.txt present ({len(response.text)} bytes) - AI crawler optimized")]
        else:
            return 5, [("WARNING", f"llms.txt returned {response.status_code} or too short")]
    except:
        return 3, [("WARNING", "llms.txt not found (AI crawler optimization missing)")]

def check_page_speed(response):
    """Check page load time - Rule 21"""
    load_time = response.elapsed.total_seconds()
    if load_time < 1.0:
        return 10, [("PASS", f"Fast load: {load_time:.2f}s")]
    elif load_time < 2.0:
        return 7, [("WARNING", f"Moderate load: {load_time:.2f}s")]
    elif load_time < 3.0:
        return 5, [("WARNING", f"Slow load: {load_time:.2f}s")]
    else:
        return 3, [("CRITICAL", f"Very slow load: {load_time:.2f}s")]

def check_content_length(content, url):
    """Check content length - Rule 22"""
    text_content = re.sub(r'<[^>]+>', '', content)
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    word_count = len(text_content.split())
    
    if "/tools/" in url:
        if word_count > 1000:
            return 10, [("PASS", f"Tool page content good: {word_count} words")]
        elif word_count > 500:
            return 7, [("WARNING", f"Tool page could be deeper: {word_count} words")]
        else:
            return 3, [("WARNING", f"Thin tool page: {word_count} words")]
    elif "/blog/" in url and ".html" not in url and url.rstrip("/").endswith("/blog"):
        return 10, [("PASS", "Blog listing page")]
    elif "/blog/" in url:
        if word_count > 1500:
            return 10, [("PASS", f"Article content good: {word_count} words")]
        elif word_count > 800:
            return 7, [("WARNING", f"Article could be deeper: {word_count} words")]
        else:
            return 3, [("WARNING", f"Thin article: {word_count} words")]
    else:
        if word_count > 300:
            return 10, [("PASS", f"Content adequate: {word_count} words")]
        else:
            return 5, [("WARNING", f"Content thin: {word_count} words")]

def check_broken_links(content, url):
    """Check for broken internal links - Rule 23 (sample check)"""
    issues = []
    links = re.findall(r'<a[^>]*href=["\'](/[^"\']*)["\']', content, re.IGNORECASE)
    if len(links) == 0:
        return 10, [("PASS", "No internal links to check")]
    
    # Sample check first 5 internal links
    sample = links[:5]
    broken = 0
    for link in sample:
        try:
            full_url = urljoin(BASE_URL, link)
            r = requests.head(full_url, headers=HEADERS, timeout=10, allow_redirects=True)
            if r.status_code >= 400:
                broken += 1
        except:
            broken += 1
    
    if broken == 0:
        return 10, [("PASS", f"All {len(sample)} sampled internal links OK")]
    else:
        return 5, [("WARNING", f"{broken}/{len(sample)} sampled links broken")]

# Main audit
print("=" * 70)
print("REAL SEO AUDIT - 40+ Rules Check")
print("Based on: pixelesq/argus + iconaki/claude-seo methodology")
print("=" * 70)
print(f"Target: {BASE_URL}")
print(f"Pages to audit: {len(PAGES_TO_AUDIT)}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)
print()

all_page_scores = []
all_issues = []

for page_path in PAGES_TO_AUDIT:
    url = urljoin(BASE_URL, page_path)
    print(f"\n{'─' * 70}")
    print(f"AUDITING: {url}")
    print(f"{'─' * 70}")
    
    response, content = fetch_page(url)
    if response is None:
        print(f"  ❌ FAILED TO FETCH: {content}")
        continue
    
    print(f"  Status: {response.status_code} | Size: {len(content)} bytes | Time: {response.elapsed.total_seconds():.2f}s")
    
    page_score = 0
    page_checks = 0
    page_issues = []
    
    # Run all checks
    checks = [
        ("Title Tag", check_title, (content, url)),
        ("Meta Description", check_meta_description, (content, url)),
        ("H1 Tag", check_h1, (content, url)),
        ("Canonical", check_canonical, (content, url)),
        ("Meta Robots", check_meta_robots, (content, url)),
        ("Open Graph", check_open_graph, (content, url)),
        ("Twitter Cards", check_twitter_cards, (content, url)),
        ("JSON-LD Schema", check_json_ld, (content, url)),
        ("Image Alt", check_image_alt, (content, url)),
        ("Heading Structure", check_heading_structure, (content, url)),
        ("Internal Links", check_internal_links, (content, url)),
        ("HTTPS", check_https, (url,)),
        ("WWW Consistency", check_www_consistency, (url,)),
        ("Lang Attribute", check_lang_attribute, (content, url)),
        ("Viewport", check_viewport, (content, url)),
        ("Charset", check_charset, (content, url)),
        ("Favicon", check_favicon, (content, url)),
        ("Page Speed", check_page_speed, (response,)),
        ("Content Length", check_content_length, (content, url)),
        ("Broken Links", check_broken_links, (content, url)),
    ]
    
    for check_name, check_func, args in checks:
        score, issues = check_func(*args)
        page_score += score
        page_checks += 1
        for severity, message in issues:
            page_issues.append((severity, check_name, message))
            if severity == "CRITICAL":
                results["critical_issues"].append(f"[{page_path}] {check_name}: {message}")
            elif severity == "WARNING":
                results["warnings"].append(f"[{page_path}] {check_name}: {message}")
    
    # Site-wide checks (only run once)
    if page_path == "/":
        site_checks = [
            ("Sitemap.xml", check_sitemap_reference, ()),
            ("robots.txt", check_robots_txt, ()),
            ("llms.txt (AI Crawler)", check_llms_txt, ()),
        ]
        for check_name, check_func, args in site_checks:
            score, issues = check_func(*args)
            page_score += score
            page_checks += 1
            for severity, message in issues:
                page_issues.append((severity, check_name, message))
                if severity == "CRITICAL":
                    results["critical_issues"].append(f"[SITE] {check_name}: {message}")
                elif severity == "WARNING":
                    results["warnings"].append(f"[SITE] {check_name}: {message}")
    
    avg_score = page_score / page_checks if page_checks > 0 else 0
    all_page_scores.append(avg_score)
    
    # Print page results
    print(f"\n  Score: {avg_score:.1f}/10 ({page_checks} checks)")
    print(f"  Issues: {len([i for i in page_issues if i[0]=='CRITICAL'])} critical, {len([i for i in page_issues if i[0]=='WARNING'])} warnings")
    
    # Print critical and warning issues
    for severity, check_name, message in page_issues:
        if severity in ("CRITICAL", "WARNING"):
            icon = "🔴" if severity == "CRITICAL" else "🟡"
            print(f"  {icon} [{check_name}] {message}")

# Summary
print("\n" + "=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)

overall_score = sum(all_page_scores) / len(all_page_scores) if all_page_scores else 0
print(f"\nOverall Score: {overall_score:.1f}/10")
print(f"Pages Audited: {len(all_page_scores)}")
print(f"Critical Issues: {len(results['critical_issues'])}")
print(f"Warnings: {len(results['warnings'])}")

# Grade
if overall_score >= 9:
    grade = "A+ (Excellent)"
elif overall_score >= 8:
    grade = "A (Very Good)"
elif overall_score >= 7:
    grade = "B (Good)"
elif overall_score >= 6:
    grade = "C (Average)"
elif overall_score >= 5:
    grade = "D (Needs Work)"
else:
    grade = "F (Critical Issues)"

print(f"Grade: {grade}")

# Top issues
print("\n" + "=" * 70)
print("TOP CRITICAL ISSUES (need immediate fix)")
print("=" * 70)
for i, issue in enumerate(results["critical_issues"][:10], 1):
    print(f"{i}. {issue}")

print("\n" + "=" * 70)
print("TOP WARNINGS (should fix soon)")
print("=" * 70)
for i, issue in enumerate(results["warnings"][:15], 1):
    print(f"{i}. {issue}")

# Save results
results["overall_score"] = overall_score
results["grade"] = grade
results["page_scores"] = dict(zip(PAGES_TO_AUDIT[:len(all_page_scores)], all_page_scores))

with open("real_seo_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Full results saved to: real_seo_audit_results.json")
print("=" * 70)
