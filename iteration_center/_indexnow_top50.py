# -*- coding: utf-8 -*-
"""P0-2: 批量IndexNow提交Top50高价值工具页"""
import json
import requests
from datetime import datetime

INDEXNOW_KEY = "3f7f80308bcbbd81d91bd93cdc0e1120"
INDEXNOW_URL = "https://api.indexnow.org/IndexNow"
SITE_URL = "https://www.aitoolcrux.com"

# 读取数据
with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

print("tools数量:", len(tools))

def get_score(tool):
    scores = tool.get('scores', {})
    if not scores:
        return 0
    numeric_scores = [v for v in scores.values() if isinstance(v, (int, float))]
    return sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0

# P0-2 要求的重点高价值工具（无曝光优先提交）
priority_slugs = ['midjourney', 'elevenlabs', 'notion-ai', 'gpt-4', 'github-copilot',
                  'sora', 'gemini', 'claude', 'chatgpt', 'stable-diffusion', 'copilot',
                  'dall-e', 'perplexity', 'runway', 'leonardo', 'midjourney-alternatives']

# 构建 Top50：优先 priority 工具 + 按评分补充到 50 个
sorted_tools = sorted(tools, key=get_score, reverse=True)
selected = []
seen = set()
for slug in priority_slugs:
    for t in tools:
        if t.get('slug') == slug and slug not in seen:
            selected.append(t)
            seen.add(slug)
            break
for t in sorted_tools:
    if t.get('slug') not in seen:
        selected.append(t)
        seen.add(t.get('slug'))
    if len(selected) >= 50:
        break

urls = [f"{SITE_URL}/tools/{t['slug']}" for t in selected]
print(f"\n=== Top {len(urls)} 高价值工具页 ===")
for u in urls:
    print(f"  + {u}")

# 提交到 IndexNow
payload = {
    "host": "www.aitoolcrux.com",
    "key": INDEXNOW_KEY,
    "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
    "urlList": urls
}

try:
    response = requests.post(INDEXNOW_URL, json=payload, timeout=30)
    print(f"\n=== IndexNow Submission Result ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print("\nSUCCESS! URLs submitted to IndexNow.")
    elif response.status_code == 202:
        print("\nACCEPTED! URLs received, processing in background.")
    else:
        print(f"\nUnexpected status code: {response.status_code}")
except Exception as e:
    print(f"\nERROR submitting to IndexNow: {e}")

# 保存 URL 列表
with open('daily_urls_for_gsc_top50.txt', 'w', encoding='utf-8') as f:
    f.write(f"# Top50 high-value tool URLs for GSC\n")
    f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"# Total: {len(urls)} URLs\n\n")
    for url in sorted(urls):
        f.write(f"{url}\n")
print(f"\nURL list saved to: daily_urls_for_gsc_top50.txt")
