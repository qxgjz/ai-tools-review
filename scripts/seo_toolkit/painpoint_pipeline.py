"""
用户痛点挖掘流水线 - 全自动
调用: python scripts/seo_toolkit/painpoint_pipeline.py --keyword "ChatGPT"
输出: iteration_center/user_painpoints/{keyword}_summary.md

整合工具:
- zens-ink reddit_blueocean (Reddit蓝海挖掘)
- Serper API (搜索Reddit帖子+G2评论+PAA)
- Playwright (抓取帖子内容)
"""
import sys, os, json, argparse, time, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *

def search_reddit(keyword):
    """用Serper API搜索Reddit帖子"""
    import requests
    queries = [
        f"site:reddit.com {keyword} review",
        f"site:reddit.com {keyword} vs",
        f"site:reddit.com {keyword} alternative",
        f"site:reddit.com {keyword} worth it",
    ]
    posts = []
    for q in queries:
        try:
            resp = requests.post(SERPER_API_URL,
                headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
                data=json.dumps({"q": q, "num": 10}), timeout=10)
            data = resp.json()
            for r in data.get("organic", []):
                url = r.get("link", "")
                if "reddit.com" in url:
                    posts.append({"title": r.get("title",""), "url": url,
                                  "snippet": r.get("snippet",""), "query": q})
        except Exception as e:
            print(f"[WARN] Reddit search failed: {e}")
        time.sleep(0.5)
    # 去重
    seen = set()
    unique = []
    for p in posts:
        if p["url"] not in seen:
            seen.add(p["url"])
            unique.append(p)
    return unique[:20]

def fetch_reddit_post(url):
    """用Playwright抓取Reddit帖子内容和高赞评论"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(3000)
            data = page.evaluate("""() => {
                const title = document.querySelector('h1')?.innerText || '';
                const body = document.querySelector('[data-testid=\"post-content\"]')?.innerText || '';
                const comments = [...document.querySelectorAll('[data-testid=\"comment\"]')]
                    .slice(0,10).map(c => ({
                        text: c.querySelector('[data-testid=\"comment\"] div')?.innerText?.slice(0,300) || '',
                        score: c.querySelector('[data-testid=\"comment-upvote\"]')?.innerText || '0'
                    }));
                return {title, body, comments};
            }""")
            browser.close()
            return data
    except Exception as e:
        return {"title": "", "body": "", "comments": [], "error": str(e)}

def search_g2_reviews(keyword):
    """搜索G2/Capterra评论"""
    import requests
    try:
        resp = requests.post(SERPER_API_URL,
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            data=json.dumps({"q": f"{keyword} reviews g2 capterra complaints", "num": 10}), timeout=10)
        data = resp.json()
        return [{"title": r.get("title",""), "url": r.get("link",""),
                 "snippet": r.get("snippet","")} for r in data.get("organic", [])]
    except:
        return []

def get_paa(keyword):
    """获取Google PAA问题"""
    import requests
    try:
        resp = requests.post(SERPER_API_URL,
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            data=json.dumps({"q": keyword, "num": 10}), timeout=10)
        data = resp.json()
        return [p.get("question","") for p in data.get("peopleAlsoAsk", [])[:8]]
    except:
        return []

def extract_painpoints(posts):
    """从帖子中提取痛点模式"""
    painpoint_patterns = {
        "免费替代需求": ["free", "alternative", "cheaper", "open source", "without paying"],
        "对比决策需求": ["vs", "versus", "which is better", "compare", "difference between"],
        "价格敏感": ["expensive", "pricing", "cost", "worth it", "too much", "subscription"],
        "功能缺陷": ["bug", "broken", "doesn't work", "missing", "lack", "terrible", "worst"],
        "场景化推荐": ["for students", "for beginners", "for business", "for coding", "for writing"],
        "购买犹豫": ["worth it", "should I buy", "is it good", "review", "experience"],
    }
    found = {k: [] for k in painpoint_patterns}
    for post in posts:
        text = (post.get("title","") + " " + post.get("snippet","")).lower()
        for pain, patterns in painpoint_patterns.items():
            if any(p in text for p in patterns):
                found[pain].append(post["title"][:80])
    return found

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True, help="目标关键词/工具名")
    args = parser.parse_args()

    print(f"=== 用户痛点挖掘流水线 ===")
    print(f"关键词: {args.keyword}")

    # Step 1: 搜索Reddit
    print("\n[1/4] 搜索Reddit讨论...")
    reddit_posts = search_reddit(args.keyword)
    print(f"  找到 {len(reddit_posts)} 个相关帖子")

    # Step 2: 抓取Top5帖子内容
    print("\n[2/4] 抓取Top5帖子详情...")
    detailed_posts = []
    for i, post in enumerate(reddit_posts[:5]):
        print(f"  [{i+1}/5] {post['title'][:50]}...")
        detail = fetch_reddit_post(post["url"])
        detail.update(post)
        detailed_posts.append(detail)
        time.sleep(1)

    # Step 3: G2评论 + PAA
    print("\n[3/4] 搜索G2评论和PAA...")
    g2_reviews = search_g2_reviews(args.keyword)
    paa = get_paa(args.keyword)
    print(f"  G2评论: {len(g2_reviews)} 条")
    print(f"  PAA问题: {len(paa)} 个")

    # Step 4: 提取痛点+输出
    print("\n[4/4] 提取痛点模式...")
    painpoints = extract_painpoints(detailed_posts + reddit_posts)

    os.makedirs(USER_PAINPOINTS_DIR, exist_ok=True)
    safe_keyword = re.sub(r'[^\w]', '_', args.keyword)
    output_file = os.path.join(USER_PAINPOINTS_DIR, f"{safe_keyword}_summary.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# 用户痛点挖掘 - {args.keyword}\n\n")
        f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## 核心痛点（按出现频率排序）\n\n")
        for pain, examples in sorted(painpoints.items(), key=lambda x: -len(x[1])):
            if examples:
                f.write(f"### {pain}（{len(examples)}次提及）\n")
                for ex in examples[:3]:
                    f.write(f"- {ex}\n")
                f.write(f"**内容机会**: 写关于{pain}的文章\n\n")
        f.write(f"## Google PAA问题（直接用作FAQ）\n\n")
        for q in paa:
            f.write(f"- {q}\n")
        f.write(f"\n## 高赞Reddit帖子\n\n")
        for p in detailed_posts:
            f.write(f"### {p.get('title','无标题')}\n")
            f.write(f"- URL: {p.get('url','')}\n")
            if p.get("body"):
                f.write(f"- 正文摘要: {p['body'][:200]}\n")
            if p.get("comments"):
                f.write(f"- 高赞评论:\n")
                for c in p["comments"][:3]:
                    f.write(f"  - [{c.get('score','?')}赞] {c.get('text','')[:100]}\n")
            f.write("\n")
        f.write(f"## G2/Capterra评论线索\n\n")
        for r in g2_reviews[:5]:
            f.write(f"- {r['title']}: {r['snippet'][:100]}\n")

    print(f"\n=== 完成 ===")
    print(f"Reddit帖子: {len(reddit_posts)} 个")
    print(f"详细抓取: {len(detailed_posts)} 个")
    print(f"痛点类型: {sum(1 for v in painpoints.values() if v)} 种")
    print(f"PAA问题: {len(paa)} 个")
    print(f"输出: {output_file}")

if __name__ == "__main__":
    main()
