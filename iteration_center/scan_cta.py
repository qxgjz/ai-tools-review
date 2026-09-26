"""Scan tools.json for bad CTA URLs and Chinese text"""
import json
import re

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

print(f"Total tools: {len(tools)}")
print()

# 1. Check for bad URLs (Google, Baidu, aggregators)
bad_patterns = [
    'google.com/search',
    'baidu.com',
    'bing.com/search',
    'yahoo.com/search',
    'duckduckgo.com',
    'toolify.ai',
    'futurepedia.io',
    'theresanaiforthat.com',
    'aitoolcrux.com',  # self-referential
]

print("=== BAD URLs (not official domains) ===")
bad_url_count = 0
for tool in tools:
    url = tool.get('officialUrl', '') or tool.get('affiliateUrl', '') or ''
    if not url:
        continue
    for pattern in bad_patterns:
        if pattern in url:
            print(f"  [{tool['slug']}] {tool['name']} -> {url}")
            bad_url_count += 1
            break

if bad_url_count == 0:
    print("  None found")

print()

# 2. Check for Chinese characters in tool names, descriptions, CTA text
print("=== CHINESE TEXT IN DATA ===")
chinese_count = 0
for tool in tools:
    for field in ['name', 'description', 'tagline', 'ctaText', 'affiliateUrl', 'officialUrl']:
        val = tool.get(field, '')
        if val and re.search(r'[\u4e00-\u9fff]', str(val)):
            print(f"  [{tool['slug']}] {field}: {val[:80]}")
            chinese_count += 1

if chinese_count == 0:
    print("  None found in tools.json")

print()

# 3. Check what URL fields exist
print("=== SAMPLE TOOL DATA ===")
sample = tools[0]
print(f"  Keys: {list(sample.keys())}")
print(f"  officialUrl: {sample.get('officialUrl', 'N/A')}")
print(f"  affiliateUrl: {sample.get('affiliateUrl', 'N/A')}")
print(f"  name: {sample.get('name', 'N/A')}")
