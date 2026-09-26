import json
import requests
from datetime import datetime

# IndexNow配置
INDEXNOW_KEY = "3f7f80308bcbbd81d91bd93cdc0e1120"
INDEXNOW_URL = "https://api.indexnow.org/IndexNow"
SITE_URL = "https://www.aitoolcrux.com"

# 读取数据
with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# 构建URL列表
urls = []

# 1. 最新3篇文章
print("=== Latest Articles ===")
for post in posts[:3]:
    url = f"{SITE_URL}/blog/{post['slug']}"
    urls.append(url)
    print(f"  + {url}")

# 2. Top10工具页（按评分排序）
def get_score(tool):
    scores = tool.get('scores', {})
    if not scores:
        return 0
    numeric_scores = [v for v in scores.values() if isinstance(v, (int, float))]
    return sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0

sorted_tools = sorted(tools, key=get_score, reverse=True)
print("\n=== Top 10 Tools ===")
for tool in sorted_tools[:10]:
    url = f"{SITE_URL}/tools/{tool['slug']}"
    urls.append(url)
    print(f"  + {url}")

# 3. 所有分类页（从工具中提取唯一分类）
categories = set()
for tool in tools:
    cat = tool.get('category', '')
    if cat and isinstance(cat, str):
        # 转换为slug格式
        cat_slug = cat.lower().replace(' ', '-').replace('/', '-')
        categories.add(cat_slug)

print(f"\n=== Categories ({len(categories)}) ===")
for cat in sorted(categories):
    url = f"{SITE_URL}/category/{cat}"
    urls.append(url)
    print(f"  + {url}")

# 4. 核心页面
core_pages = [
    f"{SITE_URL}/",
    f"{SITE_URL}/ranking",
    f"{SITE_URL}/blog",
    f"{SITE_URL}/about",
    f"{SITE_URL}/methodology",
    f"{SITE_URL}/privacy",
    f"{SITE_URL}/terms",
]
print("\n=== Core Pages ===")
for url in core_pages:
    urls.append(url)
    print(f"  + {url}")

# 去重
urls = list(set(urls))
print(f"\n=== Total URLs to submit: {len(urls)} ===")

# 提交到IndexNow
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
        print("\n✅ SUCCESS! URLs submitted to IndexNow.")
        print("   Search engines (Bing, Yandex, etc.) will crawl these pages soon.")
    elif response.status_code == 202:
        print("\n✅ ACCEPTED! URLs received, processing in background.")
    else:
        print(f"\n⚠️  Unexpected status code: {response.status_code}")

except Exception as e:
    print(f"\n❌ Error submitting to IndexNow: {e}")

# 保存URL列表供GSC手动提交
with open('daily_urls_for_gsc.txt', 'w', encoding='utf-8') as f:
    f.write(f"# URLs for Google Search Console manual submission\n")
    f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"# Total: {len(urls)} URLs\n\n")
    for url in sorted(urls):
        f.write(f"{url}\n")

print(f"\n📄 URL list saved to: daily_urls_for_gsc.txt")
print("   Use this list to manually request indexing in Google Search Console.")
