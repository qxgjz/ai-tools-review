"""Diagnose rank crash for ai-tools-review-guide-2026"""
import json, os, glob

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# 1. Find the post in posts.json
with open(os.path.join(base, 'data', 'posts.json'), 'r', encoding='utf-8') as f:
    posts = json.load(f)

target = None
for p in posts:
    if 'review-guide' in p.get('slug', '') or 'review-guide' in p.get('title', '').lower():
        target = p
        break

if target:
    print("=== FOUND POST ===")
    print(f"Slug: {target.get('slug')}")
    print(f"Title: {target.get('title')}")
    print(f"Published: {target.get('publishedAt')}")
    print(f"Updated: {target.get('updatedAt', 'N/A')}")
    print(f"Word count: {len(target.get('content', target.get('body', '')).split())}")
    print(f"Has screenshots: {target.get('hasRealScreenshots')}")
    print(f"Tags: {target.get('tags', [])}")
    print(f"Category: {target.get('category', 'N/A')}")
    # Check content length
    content = target.get('content', target.get('body', ''))
    print(f"Content length: {len(content)} chars")
    # Check internal links
    import re
    internal_links = re.findall(r'href="(/blog/[^"]+)"', content)
    print(f"Internal links: {len(internal_links)}")
    for il in internal_links[:10]:
        print(f"  -> {il}")
    # Check H2s
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE)
    print(f"H2 count: {len(h2s)}")
    for h in h2s[:10]:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        print(f"  H2: {clean[:80]}")
else:
    print("POST NOT FOUND in posts.json")
    # Search drafts
    drafts = glob.glob(os.path.join(base, 'content_drafts', '*review-guide*'))
    print(f"Drafts matching: {drafts}")

# 2. Check for cannibalization - articles targeting similar keyword
print("\n=== CANNIBALIZATION CHECK ===")
kw = "ai tools review guide"
related = []
for p in posts:
    title = p.get('title', '').lower()
    desc = p.get('metaDescription', p.get('description', '')).lower()
    slug = p.get('slug', '').lower()
    if 'review' in slug and ('guide' in slug or 'best' in slug or 'tools' in slug):
        related.append(p)

print(f"Articles with review/guide/best in slug ({len(related)}):")
for p in related[:15]:
    print(f"  {p.get('slug')}: {p.get('title','')[:70]}")

# 3. Check GSC data if available
gsc_dir = os.path.join(base, 'gsc-ga4-report')
if os.path.exists(gsc_dir):
    files = sorted(os.listdir(gsc_dir), reverse=True)
    print(f"\n=== GSC reports available: {len(files)} ===")
    for f in files[:5]:
        print(f"  {f}")
