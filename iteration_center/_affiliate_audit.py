"""P1-MONETIZE: Find top articles by GSC impressions, check affiliate link coverage"""
import json, os, re, glob

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# 1. Load posts
with open(os.path.join(base, 'data', 'posts.json'), 'r', encoding='utf-8') as f:
    posts = json.load(f)
print(f"Total posts: {len(posts)}")

# 2. Check which posts already have affiliate links
affiliate_patterns = [
    r'partnerstack', r'impact', r'ref=', r'affiliate', r'af_fid',
    r'utm_source=aff', r'amazon\.com/dp/', r'amazon\.com/gp/',
]

has_affiliate = []
no_affiliate = []
for p in posts:
    content = p.get('content', p.get('body', ''))
    slug = p.get('slug', '')
    found = False
    for pat in affiliate_patterns:
        if re.search(pat, content, re.IGNORECASE):
            found = True
            break
    if found:
        has_affiliate.append(slug)
    else:
        no_affiliate.append(slug)

print(f"\nWith affiliate: {len(has_affiliate)}")
print(f"No affiliate: {len(no_affiliate)}")

# 3. Read GSC report to get impression data
gsc_file = os.path.join(base, 'gsc-ga4-report', '2026-09-06_2026-10-05.md')
impressions = {}
if os.path.exists(gsc_file):
    with open(gsc_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Match table rows like: | /blog/slug | clicks | impressions | ctr | position |
            m = re.match(r'\|\s*(/blog/[^|]+)\|\s*(\d+)\s*\|\s*(\d+)\s*\|', line)
            if m:
                path = m.group(1).strip()
                clicks = int(m.group(2))
                imps = int(m.group(3))
                slug = path.replace('/blog/', '').rstrip('/')
                impressions[slug] = {'clicks': clicks, 'impressions': imps, 'path': path}

print(f"\nGSC impressions found for {len(impressions)} URLs")

# 4. Rank by impressions, filter no-affiliate articles
no_aff_set = set(no_affiliate)
ranked = []
for slug, data in impressions.items():
    if slug in no_aff_set and data['impressions'] > 0:
        ranked.append((slug, data['impressions'], data['clicks']))

ranked.sort(key=lambda x: x[1], reverse=True)
print(f"\n=== Top 30 high-impression articles WITHOUT affiliate links ===")
for i, (slug, imps, clicks) in enumerate(ranked[:30], 1):
    # Find the post title
    title = next((p.get('title','') for p in posts if p.get('slug')==slug), '?')
    print(f"{i:2d}. {slug:50s} imp={imps:5d} clicks={clicks:3d} | {title[:50]}")
