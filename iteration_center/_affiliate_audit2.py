"""Check GSC file format and list posts without affiliate"""
import json, os, re

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# Read GSC file raw to see format
gsc_file = os.path.join(base, 'gsc-ga4-report', '2026-09-06_2026-10-05.md')
with open(gsc_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("=== First 30 lines of GSC report ===")
for line in lines[:30]:
    print(repr(line[:150]))

# Load posts
with open(os.path.join(base, 'data', 'posts.json'), 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Find posts without affiliate
affiliate_patterns = [
    r'partnerstack', r'impact', r'ref=', r'affiliate', r'af_fid',
    r'utm_source=aff', r'amazon\.com/dp/',
]
no_aff = []
for p in posts:
    content = p.get('content', p.get('body', ''))
    slug = p.get('slug', '')
    found = any(re.search(pat, content, re.IGNORECASE) for pat in affiliate_patterns)
    if not found:
        no_aff.append((slug, p.get('title',''), len(content.split())))

print(f"\n=== {len(no_aff)} posts WITHOUT affiliate links ===")
for slug, title, wc in sorted(no_aff, key=lambda x: -x[2])[:30]:
    print(f"  {slug:55s} wc={wc:5d} | {title[:50]}")
