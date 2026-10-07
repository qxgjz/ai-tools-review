"""Check GSC data for review guide keyword + current SERP"""
import json, os, requests

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# 1. Search GSC report for this keyword
gsc_file = os.path.join(base, 'gsc-ga4-report', '2026-09-06_2026-10-05.md')
if os.path.exists(gsc_file):
    with open(gsc_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find rows with review-guide or "ai tools review"
    lines = content.split('\n')
    print("=== GSC rows mentioning 'review-guide' or 'ai tools review' ===")
    for line in lines:
        if 'review-guide' in line.lower() or 'ai tools review' in line.lower():
            print(f"  {line[:200]}")

# 2. Check latest_gsc.md
latest = os.path.join(base, 'gsc-ga4-report', 'latest_gsc.md')
if os.path.exists(latest):
    with open(latest, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    print("\n=== latest_gsc.md rows mentioning review-guide ===")
    for line in lines:
        if 'review-guide' in line.lower() or 'review guide' in line.lower():
            print(f"  {line[:200]}")

# 3. Current SERP for the keyword
SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
print("\n=== Current SERP for 'ai tools review guide 2026' ===")
r = requests.post("https://google.serper.dev/search",
    headers={"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"},
    json={"q": "ai tools review guide 2026", "num": 10}, timeout=30)
data = r.json()
for i, o in enumerate(data.get('organic', [])[:10], 1):
    print(f"  #{i}: {o.get('title','')[:70]}")
    print(f"      {o.get('link','')}")

# Also check broader keyword
print("\n=== Current SERP for 'ai tools review' ===")
r2 = requests.post("https://google.serper.dev/search",
    headers={"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"},
    json={"q": "ai tools review", "num": 10}, timeout=30)
data2 = r2.json()
for i, o in enumerate(data2.get('organic', [])[:10], 1):
    print(f"  #{i}: {o.get('title','')[:70]}")
    print(f"      {o.get('link','')}")
