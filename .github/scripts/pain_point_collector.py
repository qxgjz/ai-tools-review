"""
用户痛点数据采集脚本（云端执行）
从Reddit、论坛、评论中采集用户讨论和痛点
输出：pain_points_raw.json（本地AI后续分析）
"""
import json
import os
import requests
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE, "iteration_center")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")

# Reddit AI相关subreddit
REDDIT_SUBS = [
    "artificial",
    "MachineLearning",
    "ChatGPT",
    "Midjourney",
    "StableDiffusion",
    "SaaS",
    "Entrepreneur",
    "webdev",
    "productivity",
    "nocode",
]

# 痛点搜索查询
PAIN_QUERIES = [
    "ai tools frustrating",
    "ai tool not working",
    "best ai tool for problem",
    "ai tool alternative free",
    "ai tool too expensive",
    "ai tool limit reached",
    "ai tool quality bad",
    "struggling with ai tools",
    "ai tool for beginners",
    "ai tool comparison",
]

def search_serper(query, num=10, time_period="month"):
    """用Serper API搜索"""
    if not SERPER_API_KEY:
        return []
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": query, "num": num, "tbs": "qdr:m"},
            timeout=15
        )
        if r.status_code == 200:
            return r.json().get("organic", [])
    except Exception as e:
        print(f"  ⚠️ 搜索失败: {query} - {e}")
    return []

def search_reddit(query, sub="all"):
    """搜索Reddit帖子"""
    if not SERPER_API_KEY:
        return []
    reddit_query = f"site:reddit.com/r/{sub} {query}"
    return search_serper(reddit_query, 10)

def extract_pain_points(results, source="search"):
    """从搜索结果中提取潜在痛点"""
    pains = []
    for r in results:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        # 简单的痛点信号检测
        pain_signals = ["problem", "issue", "frustrat", "bad", "terrible", "awful", 
                        "hate", "disappoint", "not working", "broken", "limit", 
                        "expensive", "cost", "price", "alternative", "vs", 
                        "compare", "best", "recommend", "suggest", "help",
                        "struggle", "difficult", "hard", "confusing", "complicated"]
        has_pain = any(sig.lower() in (title + " " + snippet).lower() for sig in pain_signals)
        if has_pain or source == "reddit":
            pains.append({
                "title": title,
                "snippet": snippet[:300],
                "url": link,
                "source": source,
                "has_pain_signal": has_pain,
                "collected_at": datetime.utcnow().isoformat() + "Z"
            })
    return pains

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_pains = []
    
    print("🔍 开始用户痛点数据采集")
    print(f"Serper API Key: {'✅ 已配置' if SERPER_API_KEY else '❌ 未配置'}")
    
    # 1. Reddit痛点采集
    print("\n📱 Reddit采集:")
    for sub in REDDIT_SUBS[:5]:  # 先采5个sub，避免API超限
        print(f"  r/{sub}...")
        for query in PAIN_QUERIES[:3]:
            results = search_reddit(query, sub)
            pains = extract_pain_points(results, source=f"reddit/r/{sub}")
            all_pains.extend(pains)
            print(f"    {query}: {len(pains)}条")
    
    # 2. 通用搜索痛点采集
    print("\n🌐 通用搜索采集:")
    for query in PAIN_QUERIES:
        results = search_serper(query, 10)
        pains = extract_pain_points(results, source="google_search")
        all_pains.extend(pains)
        print(f"  {query}: {len(pains)}条")
    
    # 3. 去重
    seen_urls = set()
    unique_pains = []
    for p in all_pains:
        if p["url"] not in seen_urls:
            seen_urls.add(p["url"])
            unique_pains.append(p)
    
    # 保存原始数据
    output = {
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "total_collected": len(all_pains),
        "unique_count": len(unique_pains),
        "sources": list(set(p["source"] for p in unique_pains)),
        "pain_points": unique_pains
    }
    
    output_path = os.path.join(OUTPUT_DIR, "pain_points_raw.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 生成简要报告
    md_path = os.path.join(OUTPUT_DIR, "pain_points_summary.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# 用户痛点数据采集报告\n\n")
        f.write(f"采集时间: {output['collected_at']}\n\n")
        f.write(f"## 统计\n\n")
        f.write(f"- 总采集数: {output['total_collected']}\n")
        f.write(f"- 去重后: {output['unique_count']}\n")
        f.write(f"- 来源数: {len(output['sources'])}\n\n")
        f.write(f"## 来源分布\n\n")
        for src in output['sources']:
            count = sum(1 for p in unique_pains if p['source'] == src)
            f.write(f"- {src}: {count}条\n")
        f.write(f"\n## 高优先级痛点（含痛点信号）\n\n")
        high_priority = [p for p in unique_pains if p.get('has_pain_signal')][:20]
        for p in high_priority:
            f.write(f"### {p['title']}\n")
            f.write(f"- 来源: {p['source']}\n")
            f.write(f"- URL: {p['url']}\n")
            f.write(f"- 摘要: {p['snippet'][:200]}\n\n")
    
    print(f"\n✅ 完成！")
    print(f"  总采集: {len(all_pains)}条")
    print(f"  去重后: {len(unique_pains)}条")
    print(f"  高优先级: {len([p for p in unique_pains if p.get('has_pain_signal')])}条")
    print(f"  原始数据: {output_path}")
    print(f"  简要报告: {md_path}")
    print(f"\n📝 下一步：本地AI（分析师/创作家）读取pain_points_raw.json，分析真实用户痛点，生成内容方向")

if __name__ == '__main__':
    main()
