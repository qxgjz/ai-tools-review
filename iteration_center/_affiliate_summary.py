"""Final check: which GSC pages already have affiliate, and what's the coverage"""
import json, os, re

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# GSC pages with impressions
gsc_pages = {
    '/blog/best-ai-voice-changers-2026': 68,
    '/compare': 272,
    '/': 2,
    '/blog/openai_astra_review': 157,
    '/category/writing': 8,
    '/tools/ailice': 2,
    '/tools/wrenai': 3,
    '/about': 14,
    '/blog/adobe-firefly-review-2026': 33,
    '/blog/ai-coding-tools-comparison-2026': 15,
}

with open(os.path.join(base, 'data', 'posts.json'), 'r', encoding='utf-8') as f:
    posts = json.load(f)

affiliate_patterns = [r'partnerstack', r'impact', r'ref=', r'affiliate', r'af_fid', r'amazon\.com/dp/']

print("=== GSC impression pages affiliate status ===")
for path, imp in sorted(gsc_pages.items(), key=lambda x: -x[1]):
    slug = path.replace('/blog/','').rstrip('/')
    post = next((p for p in posts if p.get('slug')==slug), None)
    if post:
        content = post.get('content', post.get('body', ''))
        has = any(re.search(pat, content, re.IGNORECASE) for pat in affiliate_patterns)
        # Count affiliate links
        links = len(re.findall(r'href="[^"]*ref=[^"]*"', content))
        print(f"  {path:50s} imp={imp:4d} affiliate={'YES' if has else 'NO'} links={links}")
    else:
        print(f"  {path:50s} imp={imp:4d} (not a blog post)")

# Summary
total = len(posts)
with_aff = sum(1 for p in posts if any(re.search(pat, p.get('content',''), re.IGNORECASE) for pat in affiliate_patterns))
print(f"\n=== Summary ===")
print(f"Total posts: {total}")
print(f"With affiliate: {with_aff} ({with_aff*100//total}%)")
print(f"Without: {total-with_aff}")
print(f"Affiliate patches generated: 20 (in content_drafts/affiliate_patches/)")
