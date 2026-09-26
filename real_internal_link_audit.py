#!/usr/bin/env python3
"""
Real Internal Link Audit - Based on Thibaultbm/seo-internal-linking methodology
Actually crawls hub pages and analyzes internal link structure
"""

import requests
import re
import json
from urllib.parse import urljoin, urlparse
from datetime import datetime
from collections import defaultdict

BASE_URL = "https://www.aitoolcrux.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Hub pages that should link to important content
HUB_PAGES = [
    "/",
    "/ranking",
    "/category/chat",
    "/category/writing",
    "/category/agent",
    "/category/code",
    "/category/image",
    "/category/video",
    "/category/audio",
    "/category/productivity",
    "/blog",
    "/alternatives",
]

# Important pages that should have inbound links
IMPORTANT_PAGES = [
    "/tools/chatgpt",
    "/tools/midjourney",
    "/tools/cursor",
    "/tools/gemini",
    "/tools/claude",
    "/tools/perplexity",
    "/tools/dall-e",
    "/tools/elevenlabs",
    "/tools/notion-ai",
    "/tools/canva",
    "/blog/chatgpt-vs-claude-2026-comparison",
    "/alternatives/chatgpt-alternatives",
    "/alternatives/midjourney-alternatives",
    "/methodology",
    "/about",
]

results = {
    "audit_time": datetime.now().isoformat(),
    "hub_pages_crawled": 0,
    "total_internal_links_found": 0,
    "unique_pages_linked": 0,
    "orphan_pages": [],
    "link_distribution": {},
    "anchor_text_analysis": {},
    "content_clusters": {},
    "score": 0,
    "findings": [],
    "recommendations": [],
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        return response, response.text
    except Exception as e:
        return None, str(e)

def extract_internal_links(content, source_url):
    """Extract all internal links from a page"""
    links = []
    # Find all <a> tags with href
    a_tags = re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
    
    for href, anchor_text in a_tags:
        # Clean href
        href = href.strip()
        # Skip empty, javascript, mailto, tel
        if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
            continue
        
        # Convert to absolute URL
        if href.startswith('/'):
            full_url = urljoin(BASE_URL, href)
        elif BASE_URL in href:
            full_url = href
        else:
            continue  # External link
        
        # Clean anchor text
        anchor_text = re.sub(r'<[^>]+>', '', anchor_text).strip()
        anchor_text = re.sub(r'\s+', ' ', anchor_text)
        
        # Get path
        parsed = urlparse(full_url)
        path = parsed.path
        
        links.append({
            'url': full_url,
            'path': path,
            'anchor_text': anchor_text,
            'source': source_url,
        })
    
    return links

def analyze_anchor_text(anchor_text):
    """Analyze anchor text quality"""
    if not anchor_text:
        return "empty", 0
    
    # Generic anchor texts to avoid
    generic_texts = ['click here', 'learn more', 'read more', 'here', 'more', 'link', 'this']
    if anchor_text.lower() in generic_texts:
        return "generic", 2
    
    # Descriptive anchor text (contains keywords)
    if len(anchor_text) > 10 and any(word in anchor_text.lower() for word in ['ai', 'tool', 'review', 'best', 'alternative', 'vs', 'comparison']):
        return "descriptive", 10
    
    # Brand anchor text
    if 'aitoolcrux' in anchor_text.lower():
        return "brand", 7
    
    # Moderate
    if len(anchor_text) > 5:
        return "moderate", 6
    
    return "short", 4

# Main execution
print("=" * 70)
print("REAL INTERNAL LINK AUDIT")
print("Based on: Thibaultbm/seo-internal-linking methodology")
print("=" * 70)
print(f"Target: {BASE_URL}")
print(f"Hub pages to crawl: {len(HUB_PAGES)}")
print(f"Important pages to check: {len(IMPORTANT_PAGES)}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Crawl all hub pages and collect links
all_links = []
page_link_counts = {}
inbound_links = defaultdict(list)  # path -> list of source pages

for hub_path in HUB_PAGES:
    url = urljoin(BASE_URL, hub_path)
    print(f"\nCrawling: {hub_path}")
    
    response, content = fetch_page(url)
    if response is None:
        print(f"  ❌ Failed: {content}")
        continue
    
    links = extract_internal_links(content, hub_path)
    all_links.extend(links)
    page_link_counts[hub_path] = len(links)
    
    # Track inbound links
    for link in links:
        inbound_links[link['path']].append(hub_path)
    
    print(f"  ✅ Found {len(links)} internal links")
    results["hub_pages_crawled"] += 1

# Summary stats
unique_paths = set(link['path'] for link in all_links)
results["total_internal_links_found"] = len(all_links)
results["unique_pages_linked"] = len(unique_paths)

print("\n" + "=" * 70)
print("LINK DISTRIBUTION BY HUB PAGE")
print("=" * 70)
for page, count in sorted(page_link_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {page}: {count} outbound links")

# Check important pages for inbound links
print("\n" + "=" * 70)
print("IMPORTANT PAGES - INBOUND LINK CHECK")
print("=" * 70)

orphan_pages = []
for page_path in IMPORTANT_PAGES:
    inbound = inbound_links.get(page_path, [])
    if len(inbound) == 0:
        status = "❌ ORPHAN (no inbound links from hub pages)"
        orphan_pages.append(page_path)
        results["findings"].append(f"Orphan page: {page_path} - no inbound links from hub pages")
    elif len(inbound) < 2:
        status = f"⚠️ Only {len(inbound)} inbound link(s)"
        results["findings"].append(f"Low inbound links: {page_path} - only {len(inbound)} link(s)")
    else:
        status = f"✅ {len(inbound)} inbound links"
    
    print(f"  {status}: {page_path}")
    if inbound:
        print(f"     From: {', '.join(inbound[:5])}")

results["orphan_pages"] = orphan_pages

# Anchor text analysis
print("\n" + "=" * 70)
print("ANCHOR TEXT QUALITY ANALYSIS")
print("=" * 70)

anchor_categories = defaultdict(int)
anchor_examples = defaultdict(list)

for link in all_links:
    category, score = analyze_anchor_text(link['anchor_text'])
    anchor_categories[category] += 1
    if len(anchor_examples[category]) < 3 and link['anchor_text']:
        anchor_examples[category].append(link['anchor_text'][:50])

total_anchors = sum(anchor_categories.values())
for category, count in sorted(anchor_categories.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total_anchors) * 100 if total_anchors > 0 else 0
    print(f"  {category.upper()}: {count} ({percentage:.1f}%)")
    for example in anchor_examples[category]:
        print(f"    Example: \"{example}\"")

results["anchor_text_analysis"] = dict(anchor_categories)

# Content cluster analysis
print("\n" + "=" * 70)
print("CONTENT CLUSTER ANALYSIS")
print("=" * 70)

# Check if category pages link to blog posts about that category
category_clusters = {
    'chat': ['/blog/chatgpt-vs-claude-2026-comparison'],
    'writing': [],
    'code': [],
    'image': [],
}

for category, expected_articles in category_clusters.items():
    category_path = f"/category/{category}"
    links_from_category = [link for link in all_links if link['source'] == category_path]
    blog_links = [link for link in links_from_category if '/blog/' in link['path']]
    
    print(f"\n  Category: {category}")
    print(f"    Total links from category page: {len(links_from_category)}")
    print(f"    Links to blog posts: {len(blog_links)}")
    
    if expected_articles:
        for article in expected_articles:
            if article in [l['path'] for l in blog_links]:
                print(f"    ✅ Links to {article}")
            else:
                print(f"    ❌ Does NOT link to {article} (cluster gap)")
                results["findings"].append(f"Content cluster gap: /category/{category} doesn't link to {article}")

# Calculate score
print("\n" + "=" * 70)
print("INTERNAL LINK AUDIT SCORE")
print("=" * 70)

# Score components
hub_coverage_score = (results["hub_pages_crawled"] / len(HUB_PAGES)) * 20 if len(HUB_PAGES) > 0 else 0
orphan_score = 20 if len(orphan_pages) == 0 else max(0, 20 - len(orphan_pages) * 5)
anchor_score = (anchor_categories.get('descriptive', 0) / total_anchors) * 30 if total_anchors > 0 else 0
link_volume_score = min(30, len(all_links) / 50)  # 1500+ links = 30 points

overall_score = hub_coverage_score + orphan_score + anchor_score + link_volume_score
overall_score = min(100, overall_score)

print(f"  Hub page coverage: {hub_coverage_score:.1f}/20")
print(f"  Orphan page penalty: {orphan_score:.1f}/20")
print(f"  Descriptive anchor text: {anchor_score:.1f}/30")
print(f"  Link volume: {link_volume_score:.1f}/30")
print(f"\n  Overall Internal Link Score: {overall_score:.1f}/100")

if overall_score >= 80:
    grade = "A (Excellent internal linking)"
elif overall_score >= 60:
    grade = "B (Good, room for improvement)"
elif overall_score >= 40:
    grade = "C (Average, needs work)"
else:
    grade = "D (Poor, major issues)"

print(f"  Grade: {grade}")
results["score"] = overall_score

# Recommendations
print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)
recommendations = [
    "Add Quick Answer/Key Takeaways sections to all article pages (improves AEO and provides natural internal link opportunities)",
    "Ensure every important tool page is linked from at least 2-3 hub pages",
    "Add 'Related Articles' sections to all category pages (content cluster linking)",
    "Use descriptive anchor text instead of generic 'click here' or 'learn more'",
    "Add internal links from blog posts to relevant tool pages (and vice versa)",
    "Create a 'Related Tools' section on all blog posts",
    "Ensure orphan pages get at least one inbound link from a relevant hub page",
]
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

# Save results
results["recommendations"] = recommendations
with open("real_internal_link_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Full results saved to: real_internal_link_audit_results.json")
print("=" * 70)
