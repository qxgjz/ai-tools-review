"""Check Perplexity and all CTA links, plus find any Chinese in UI-rendered strings"""
import json
import re

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# Check Perplexity specifically
print("=== PERPLEXITY TOOL ===")
for t in tools:
    if 'perplexity' in t.get('slug', '').lower() or 'perplexity' in t.get('name', '').lower():
        print(f"  slug: {t['slug']}")
        print(f"  name: {t['name']}")
        print(f"  officialUrl: {t.get('officialUrl', 'N/A')}")
        print(f"  affiliateUrl: {t.get('affiliateUrl', 'N/A')}")
        print(f"  hasFreeTier: {t.get('hasFreeTier', 'N/A')}")
        print()

# Check all tools for suspicious URLs (not official domains)
print("=== ALL OFFICIAL URLS (checking for non-official domains) ===")
suspicious = []
for t in tools:
    url = t.get('officialUrl', '') or ''
    if not url:
        continue
    # Extract domain
    domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if domain_match:
        domain = domain_match.group(1)
        # Check if domain looks like a search engine or aggregator
        bad_domains = ['google.com', 'baidu.com', 'bing.com', 'yahoo.com', 
                       'duckduckgo.com', 'toolify.ai', 'futurepedia.io',
                       'theresanaiforthat.com', 'aitoolcrux.com']
        for bad in bad_domains:
            if bad in domain:
                suspicious.append((t['slug'], t['name'], url, domain))
                break

if suspicious:
    for slug, name, url, domain in suspicious:
        print(f"  SUSPICIOUS: [{slug}] {name} -> {url} (domain: {domain})")
else:
    print("  All URLs look like official domains")

print()

# Check affiliate URLs too
print("=== AFFILIATE URLS ===")
aff_count = 0
for t in tools:
    aff = t.get('affiliateUrl', '') or ''
    if aff:
        aff_count += 1
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', aff)
        domain = domain_match.group(1) if domain_match else 'unknown'
        if any(bad in domain for bad in ['google.com', 'baidu.com', 'bing.com']):
            print(f"  BAD AFF: [{t['slug']}] {t['name']} -> {aff}")

print(f"  Total tools with affiliateUrl: {aff_count}")
print()

# Show a sample of official URLs to verify they're correct
print("=== SAMPLE OFFICIAL URLS ===")
for t in tools[:20]:
    print(f"  {t['name']}: {t.get('officialUrl', 'N/A')}")
