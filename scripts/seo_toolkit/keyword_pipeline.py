"""
关键词挖掘流水线 - 全自动
调用: python scripts/seo_toolkit/keyword_pipeline.py --seed "ChatGPT" [--count 20]
输出: iteration_center/keyword_pipeline.md + 自动写入state.json待办

整合工具:
- zens-ink keyword_research.expand_keyword (关键词扩展)
- zens-ink kd.fetch_serp + calculate_kd (SERP获取+难度计算)
- zens-ink search_intent.classify (意图判断)
- Serper API (PAA+相关搜索)
"""
import sys, os, json, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *

def expand_keywords(seed, count=20):
    """用Serper API的relatedSearches扩展关键词（不需要翻墙）"""
    import requests
    results = set()
    try:
        resp = requests.post(SERPER_API_URL,
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            data=json.dumps({"q": seed, "num": 10}), timeout=15)
        data = resp.json()
        for r in data.get("relatedSearches", []):
            q = r.get("query", "")
            if q and len(q) > 5:
                results.add(q)
    except Exception as e:
        print(f"[WARN] Serper relatedSearches failed: {e}")
    # 高意图模板词
    templates = [
        f"{seed} vs ChatGPT", f"{seed} vs Gemini", f"best {seed} alternatives",
        f"{seed} review 2026", f"{seed} pricing", f"is {seed} worth it",
        f"{seed} free alternative", f"{seed} for students",
        f"how to use {seed}", f"{seed} tutorial", f"{seed} discount code",
        f"cheaper alternative to {seed}", f"{seed} open source alternative",
        f"{seed} API pricing", f"{seed} vs Claude",
    ]
    for t in templates:
        results.add(t)
    final = [r for r in results if r and len(r) > 5]
    return final[:count]

def analyze_keyword(keyword):
    """分析单个关键词：SERP+竞争度+意图+PAA（全部用Serper API）"""
    import requests
    result = {"keyword": keyword, "serp": [], "kd": None, "intent": None,
              "paa": [], "related": [], "low_dr_count": 0, "has_comparison": False}
    try:
        # 1. 用Serper API获取SERP
        resp = requests.post(SERPER_API_URL,
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            data=json.dumps({"q": keyword, "num": 10}), timeout=15)
        data = resp.json()
        organic = data.get("organic", [])
        result["serp"] = [{"title": r.get("title",""), "url": r.get("link",""),
                           "domain": r.get("domain","")} for r in organic[:10]]
        # 2. PAA + 相关搜索
        result["paa"] = [p.get("question","") for p in data.get("peopleAlsoAsk", [])[:6]]
        result["related"] = [r.get("query","") for r in data.get("relatedSearches", [])[:8]]
        # 3. 估算竞争度（0-100，越低越容易）
        # 基于：前10名中大站数量、有无中小站、标题匹配度
        big_domains = ["youtube.com", "wikipedia.org", "amazon.com", "reddit.com",
                       "medium.com", "github.com", "quora.com", "pinterest.com",
                       "linkedin.com", "twitter.com", "facebook.com", "instagram.com"]
        big_count = sum(1 for r in organic[:10] if any(b in r.get("domain","") for b in big_domains))
        # 估算DR：大站90+，知名品牌站70-90，中小站<60
        estimated_drs = []
        for r in organic[:10]:
            domain = r.get("domain", "")
            if any(b in domain for b in big_domains):
                estimated_drs.append(90)
            elif any(b in domain for b in ["openai.com", "anthropic.com", "google.com", "microsoft.com", "meta.com", "apple.com", "adobe.com", "canva.com", "notion.so", "figma.com"]):
                estimated_drs.append(85)
            elif any(b in domain for b in ["techcrunch.com", "theverge.com", "wired.com", "zdnet.com", "forbes.com", "pcmag.com", "tomshardware.com"]):
                estimated_drs.append(75)
            else:
                estimated_drs.append(45)  # 假设中小站
        avg_dr = sum(estimated_drs) / max(len(estimated_drs),1)
        low_dr = sum(1 for d in estimated_drs if d < 60)
        result["low_dr_count"] = low_dr
        # KD公式：大站多→高KD，低DR站多→低KD
        kd = min(95, max(5, int(avg_dr * 0.6 + big_count * 5 + (10-low_dr) * 2)))
        result["kd"] = kd
        # 4. 检测有无对比页/列表页
        for r in organic[:10]:
            title = r.get("title","").lower()
            if "vs" in title or "versus" in title or "best" in title or "top" in title:
                result["has_comparison"] = True
                break
        # 5. 意图判断（基于关键词模式）
        kw_lower = keyword.lower()
        if any(w in kw_lower for w in ["buy", "price", "pricing", "cost", "discount", "deal", "coupon"]):
            result["intent"] = "transactional"
        elif any(w in kw_lower for w in ["vs", "versus", "alternative", "compare", "best", "top", "review", "worth it"]):
            result["intent"] = "commercial"
        elif any(w in kw_lower for w in ["how", "what", "why", "when", "tutorial", "guide", "use"]):
            result["intent"] = "informational"
        else:
            result["intent"] = "navigational"
    except Exception as e:
        print(f"[ERROR] analyze {keyword}: {e}")
    return result

def classify_priority(kw_data):
    """根据KD+低DR数量+意图分类优先级"""
    kd = kw_data.get("kd", 50) or 50
    low_dr = kw_data.get("low_dr_count", 0)
    intent = kw_data.get("intent", "")
    has_comp = kw_data.get("has_comparison", False)
    # P0: KD<40 且 低DR≥2 且 意图是商业/对比
    if kd < 40 and low_dr >= 2 and intent in ["commercial", "transactional", "comparison"]:
        return "P0"
    # P1: KD<50 且 低DR≥1
    if kd < 50 and low_dr >= 1:
        return "P1"
    # P2: 其他
    return "P2"

def intent_to_content_type(intent, keyword):
    """意图→内容类型映射"""
    kw_lower = keyword.lower()
    if "vs" in kw_lower or "versus" in kw_lower:
        return "对比页"
    if "alternative" in kw_lower:
        return "替代方案页"
    if "best" in kw_lower or "top" in kw_lower:
        return "场景列表页"
    if "review" in kw_lower or "worth it" in kw_lower:
        return "评测页"
    if "pricing" in kw_lower or "cost" in kw_lower:
        return "定价分析页"
    if intent in ["commercial", "transactional"]:
        return "对比页"
    return "信息页"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, help="种子关键词")
    parser.add_argument("--count", type=int, default=15, help="扩展词数量")
    parser.add_argument("--no-write", action="store_true", help="不写入state.json")
    args = parser.parse_args()

    print(f"=== 关键词挖掘流水线 ===")
    print(f"种子词: {args.seed}")
    print(f"扩展数量: {args.count}")

    # Step 1: 扩展关键词
    print("\n[1/4] 扩展关键词...")
    keywords = expand_keywords(args.seed, args.count)
    print(f"  扩展到 {len(keywords)} 个词")

    # Step 2: 逐个分析
    print("\n[2/4] 逐个分析SERP+KD+意图+PAA...")
    results = []
    for i, kw in enumerate(keywords):
        print(f"  [{i+1}/{len(keywords)}] {kw}...", end=" ")
        data = analyze_keyword(kw)
        data["priority"] = classify_priority(data)
        data["content_type"] = intent_to_content_type(data["intent"], kw)
        results.append(data)
        print(f"KD={data.get('kd','?')} 低DR={data['low_dr_count']} 意图={data['intent']} 优先级={data['priority']}")
        time.sleep(1)  # 避免API限流

    # Step 3: 输出Markdown
    print("\n[3/4] 输出keyword_pipeline.md...")
    os.makedirs(ITERATION_DIR, exist_ok=True)
    with open(KEYWORD_PIPELINE, "w", encoding="utf-8") as f:
        f.write(f"# 关键词挖掘结果 - 种子词: {args.seed}\n\n")
        f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## 优先级排序\n\n")
        f.write("| 优先级 | 关键词 | KD | 低DR站数 | 意图 | 内容类型 | PAA数量 |\n")
        f.write("|--------|--------|-----|---------|------|---------|--------|\n")
        for r in sorted(results, key=lambda x: {"P0":0,"P1":1,"P2":2}[x["priority"]]):
            f.write(f"| {r['priority']} | {r['keyword']} | {r.get('kd','?')} | {r['low_dr_count']} | {r['intent']} | {r['content_type']} | {len(r['paa'])} |\n")
        f.write("\n## P0词详情\n\n")
        for r in results:
            if r["priority"] == "P0":
                f.write(f"### {r['keyword']}\n")
                f.write(f"- KD: {r.get('kd','?')}\n")
                f.write(f"- 意图: {r['intent']}\n")
                f.write(f"- 内容类型: {r['content_type']}\n")
                f.write(f"- 低DR站数: {r['low_dr_count']}\n")
                if r["paa"]:
                    f.write(f"- PAA问题:\n")
                    for q in r["paa"]:
                        f.write(f"  - {q}\n")
                if r["related"]:
                    f.write(f"- 相关搜索: {', '.join(r['related'][:5])}\n")
                f.write("\n")

    # Step 4: 写入state.json待办
    p0_count = 0
    if not args.no_write:
        print("\n[4/4] 写入state.json待办...")
        with open(STATE_JSON, "r", encoding="utf-8") as f:
            state = json.load(f)
        existing = {t.get("task","") for t in state.get("next_iteration_focus", [])}
        for r in results:
            if r["priority"] in ["P0", "P1"]:
                task_desc = f"写文章：{r['keyword']}（{r['content_type']}）"
                if task_desc not in existing:
                    state["next_iteration_focus"].append({
                        "id": f"kw_{r['keyword'].replace(' ','_').replace('?','')}",
                        "task": task_desc,
                        "assigned_to": "窗口3",
                        "priority": r["priority"],
                        "source": f"keyword_pipeline_{args.seed}",
                        "keyword_data": {
                            "kd": r.get("kd"),
                            "intent": r["intent"],
                            "content_type": r["content_type"],
                            "paa": r["paa"],
                            "low_dr_count": r["low_dr_count"]
                        },
                        "status": "pending",
                        "created_at": time.strftime("%Y-%m-%d")
                    })
                    p0_count += 1
        with open(STATE_JSON, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"  新增待办: {p0_count} 条")

    # 汇总
    p0 = sum(1 for r in results if r["priority"]=="P0")
    p1 = sum(1 for r in results if r["priority"]=="P1")
    print(f"\n=== 完成 ===")
    print(f"总分析: {len(results)} 词")
    print(f"P0: {p0} 词")
    print(f"P1: {p1} 词")
    print(f"输出文件: {KEYWORD_PIPELINE}")
    print(f"新增待办: {p0_count} 条")

if __name__ == "__main__":
    main()
