"""
关键词挖掘脚本（云端执行）
用Serper API + Google Autocomplete + People Also Ask挖掘关键词
输出：keyword_research_results.json + keyword_opportunities.md
"""
import json
import os
import requests
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE, "iteration_center")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")

# 核心种子词（AI工具站）
SEED_KEYWORDS = [
    "ai tools",
    "best ai tools",
    "ai tools for",
    "free ai tools",
    "ai image generator",
    "ai writing assistant",
    "ai code generator",
    "ai video generator",
    "ai voice generator",
    "ai chatbot",
    "ai seo tools",
    "ai marketing tools",
    "ai productivity tools",
    "ai design tools",
    "ai music generator",
]

# 长尾词模板
LONG_TAIL_TEMPLATES = [
    "best {seed} for students",
    "best {seed} for small business",
    "free {seed} no sign up",
    "{seed} vs {seed2}",
    "{seed} alternative",
    "is {seed} free",
    "how to use {seed}",
    "{seed} pricing",
    "{seed} review",
    "{seed} tutorial",
]

def search_serper(query, num=10):
    """用Serper API搜索"""
    if not SERPER_API_KEY:
        return []
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": query, "num": num},
            timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            return data.get("organic", [])
    except Exception as e:
        print(f"  ⚠️ Serper搜索失败: {query} - {e}")
    return []

def get_autocomplete_suggestions(seed):
    """Google Autocomplete建议（通过Serper的autocomplete端点）"""
    if not SERPER_API_KEY:
        return []
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": seed, "autocomplete": True},
            timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            return data.get("autocomplete", [])
    except Exception as e:
        print(f"  ⚠️ Autocomplete失败: {seed} - {e}")
    return []

def estimate_difficulty(results):
    """根据搜索结果估算关键词难度（0-100）"""
    if not results:
        return 50
    # 简单估算：首页域名权威度、内容长度、是否有大站
    high_authority_domains = ["wikipedia.org", "youtube.com", "github.com", "medium.com", "reddit.com", "amazon.com"]
    ha_count = sum(1 for r in results if any(d in r.get("link", "") for d in high_authority_domains))
    base = 30 + ha_count * 10
    return min(base, 95)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    results = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "seed_keywords": SEED_KEYWORDS,
        "keywords": [],
        "long_tail_opportunities": [],
        "paa_questions": []
    }
    
    print(f"🔍 开始关键词挖掘（{len(SEED_KEYWORDS)}个种子词）")
    print(f"Serper API Key: {'✅ 已配置' if SERPER_API_KEY else '❌ 未配置'}")
    
    for i, seed in enumerate(SEED_KEYWORDS):
        print(f"\n[{i+1}/{len(SEED_KEYWORDS)}] 种子词: {seed}")
        
        # 1. 搜索结果分析
        organic = search_serper(seed, 10)
        difficulty = estimate_difficulty(organic)
        results["keywords"].append({
            "keyword": seed,
            "difficulty": difficulty,
            "search_results_count": len(organic),
            "top_domains": [r.get("link", "").split("/")[2] if "://" in r.get("link", "") else r.get("link", "") for r in organic[:5]],
        })
        print(f"  难度: {difficulty}/100, 结果数: {len(organic)}")
        
        # 2. Autocomplete建议
        suggestions = get_autocomplete_suggestions(seed)
        for sug in suggestions[:10]:
            if sug not in [k["keyword"] for k in results["keywords"]]:
                results["keywords"].append({
                    "keyword": sug,
                    "difficulty": difficulty - 10,  # 长尾词通常更容易
                    "source": "autocomplete",
                    "seed": seed
                })
        print(f"  Autocomplete建议: {len(suggestions)}个")
        
        # 3. People Also Ask
        for r in organic:
            paa = r.get("snippet", "")
            if "?" in paa and len(paa) < 200:
                results["paa_questions"].append({"question": paa, "source": seed})
    
    # 4. 生成长尾词机会
    for seed in SEED_KEYWORDS[:5]:
        for template in LONG_TAIL_TEMPLATES:
            if "{seed2}" in template:
                seed2 = SEED_KEYWORDS[(SEED_KEYWORDS.index(seed) + 1) % len(SEED_KEYWORDS)]
                kw = template.format(seed=seed, seed2=seed2)
            else:
                kw = template.format(seed=seed)
            results["long_tail_opportunities"].append({
                "keyword": kw,
                "estimated_difficulty": 20,
                "type": "long_tail",
                "seed": seed
            })
    
    # 保存结果
    output_path = os.path.join(OUTPUT_DIR, "keyword_research_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 生成Markdown报告
    md_path = os.path.join(OUTPUT_DIR, "keyword_opportunities.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# 关键词挖掘报告\n\n")
        f.write(f"生成时间: {results['generated_at']}\n\n")
        f.write(f"## 核心关键词难度分析\n\n")
        f.write("| 关键词 | 难度 | 首页Top域名 |\n")
        f.write("|---|---|---|\n")
        for kw in sorted(results["keywords"], key=lambda x: x.get("difficulty", 50))[:20]:
            domains = ", ".join(kw.get("top_domains", [])[:3])
            f.write(f"| {kw['keyword']} | {kw.get('difficulty', 'N/A')}/100 | {domains} |\n")
        f.write(f"\n## 长尾词机会（{len(results['long_tail_opportunities'])}个）\n\n")
        for kw in results["long_tail_opportunities"][:30]:
            f.write(f"- {kw['keyword']}（预估难度: {kw['estimated_difficulty']}/100）\n")
        f.write(f"\n## People Also Ask 问题（{len(results['paa_questions'])}个）\n\n")
        for q in results["paa_questions"][:20]:
            f.write(f"- {q['question']}\n")
    
    print(f"\n✅ 完成！")
    print(f"  关键词总数: {len(results['keywords'])}")
    print(f"  长尾词机会: {len(results['long_tail_opportunities'])}")
    print(f"  PAA问题: {len(results['paa_questions'])}")
    print(f"  结果文件: {output_path}")
    print(f"  报告文件: {md_path}")

if __name__ == '__main__':
    main()
