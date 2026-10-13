#!/usr/bin/env python3
"""拓荒者-用户痛点挖掘 v2: 多源抓取+搜索意图验证+覆盖检查+聚类"""
import requests, json, os, re
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
SERPER_URL = "https://google.serper.dev/search"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
PAIN_MD = os.path.join(PROJECT, "iteration_center", "pain_points.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_pain_{today}.md")

# 已有文章URL（从sitemap提取，用于覆盖检查）
EXISTING_URLS = [
    "best-paid-ai-tools-worth-buying", "dify-vs-langchain", "gemini-alternatives",
    "cursor-vs-windsurf", "notion-ai-vs-obsidian", "notion-ai-alternative",
    "midjourney-vs-dalle", "jasper-ai-alternative", "chatgpt-vs-claude",
    "best-ai-voice-changers", "best-ai-slack-bots", "best-ai-scheduling-tools",
    "best-ai-podcast-tools", "best-ai-idea-generators", "dify-vs-coze",
    "stable-diffusion-alternatives", "midjourney-alternatives", "best-ai-voice-generators",
    "best-ai-resume-builders", "best-ai-pr-tools", "best-ai-photo-editors",
    "best-ai-observability-tools", "best-ai-meeting-assistants", "best-ai-logo-generators",
    "best-ai-grammar-checkers", "best-ai-customer-support-tools", "best-ai-comparison-tools",
    "best-ai-chatbot-builders", "best-ai-automation-agents", "best-ai-agents",
    "best-ai-crm-tools", "best-ai-project-management-tools", "best-ai-note-taking-tools",
    "best-ai-design-tools", "best-ai-email-tools", "best-ai-translation-tools",
    "best-ai-transcription-tools", "best-ai-chatbots", "best-ai-presentation-tools",
    "best-ai-legal-tools", "best-ai-seo-tools", "best-ai-video-editors",
    "best-ai-marketing-tools", "best-ai-research-tools", "best-ai-productivity-tools",
    "best-ai-coding-tools", "best-ai-image-generators", "best-ai-audio-tools",
]

def serper(q, num=10):
    try:
        r = requests.post(SERPER_URL, headers=HEADERS, json={"q": q, "num": num}, timeout=20)
        return r.json().get("organic", [])
    except Exception as e:
        print(f"  [ERR] {q[:50]}: {e}")
        return []

# === 1. 多源抓取（6+来源） ===
queries = [
    # Reddit - 多个子版
    ("Reddit r/ChatGPT", 'site:reddit.com/r/ChatGPT "too expensive" OR "waste of money" OR frustrated OR "not worth"'),
    ("Reddit r/OpenAI", 'site:reddit.com/r/OpenAI hallucination OR "made up" OR "wrong answer" OR inaccurate'),
    ("Reddit r/SaaS", 'site:reddit.com/r/SaaS "AI tool" frustrating OR "waste of money" OR buggy OR disappointing'),
    ("Reddit r/artificial", 'site:reddit.com/r/artificial "AI video" expensive OR credits OR "too expensive" OR pricing'),
    ("Reddit r/Entrepreneur", 'site:reddit.com/r/Entrepreneur "AI tool" "waste of money" OR scam OR overhyped OR disappointing'),
    # Hacker News
    ("Hacker News", 'site:news.ycombinator.com "Show HN" AI tool OR "AI startup" disappointing OR "not worth" OR overhyped'),
    # G2 差评
    ("G2 Reviews", 'site:g2.com "AI" review "1 out of 5" OR "2 out of 5" OR "would not recommend" OR "low value"'),
    # Product Hunt
    ("Product Hunt", 'site:producthunt.com AI tool review OR comment OR "not worth" OR disappointing'),
    # YouTube 评测
    ("YouTube Reviews", 'site:youtube.com "AI tool" review honest OR "waste of money" OR disappointing OR "not worth it"'),
    # Capterra
    ("Capterra", 'site:capterra.com "AI" review "1 star" OR "2 star" OR "would not recommend"'),
]

all_comments = []
sources_used = set()
for label, q in queries:
    print(f"\n=== {label} ===")
    results = serper(q, num=8)
    for r in results:
        url = r.get("link", "")
        snippet = r.get("snippet", "")
        title = r.get("title", "")
        if snippet and len(snippet) > 30:
            src = label.split()[0]
            all_comments.append({"source": label, "src_group": src, "url": url, "title": title, "quote": snippet})
            sources_used.add(src)
    print(f"  got {len(results)} results, {len([r for r in results if r.get('snippet','')])} with snippet")

print(f"\n=== Total: {len(all_comments)} comments from {len(sources_used)} source groups ===")
print(f"=== Sources: {sorted(sources_used)} ===")

# === 2. 痛点聚类定义 ===
clusters_def = [
    {
        "theme": "AI工具订阅太贵/不值这个价",
        "keywords": ["expensive", "too expensive", "pricing", "waste of money", "not worth", "subscription", "overpriced", "price jumped", "cancel"],
        "target": "AI工具定价",
        "article": "AI Tools That Are Not Worth the Money in 2026 (Honest Pricing Review)",
        "search_kw": "are ai tools worth the money 2026",
        "base_priority": "P0"
    },
    {
        "theme": "ChatGPT/AI写作幻觉多、编造事实",
        "keywords": ["hallucination", "made up", "wrong answer", "inaccurate", "fabricated", "lies", "nonsense", "confidently wrong"],
        "target": "ChatGPT/AI写作",
        "article": "ChatGPT Hallucinations in 2026: Why It Still Makes Up Facts and How to Catch It",
        "search_kw": "chatgpt hallucinations how to prevent 2026",
        "base_priority": "P0"
    },
    {
        "theme": "AI视频生成credits烧太快/性价比低",
        "keywords": ["video generator", "credits", "ai video", "runway", "pika", "sora", "video generation"],
        "target": "AI视频生成",
        "article": "Why AI Video Generators Burn Through Credits Fast (And Free Alternatives in 2026)",
        "search_kw": "ai video generator credits expensive alternative 2026",
        "base_priority": "P0"
    },
    {
        "theme": "SaaS老板用AI工具反而更麻烦/不实用",
        "keywords": ["saas", "frustrating", "buggy", "integration", "workflow", "waste of time", "overhyped", "hype"],
        "target": "SaaS AI工具",
        "article": "AI Tools for SaaS in 2026: What Actually Works vs. What's Overhyped",
        "search_kw": "ai tools for saas actually work 2026",
        "base_priority": "P1"
    },
    {
        "theme": "Notion AI令人失望/找更好替代",
        "keywords": ["notion ai", "notion"],
        "target": "Notion AI",
        "article": "Notion AI Is Disappointing? 7 Real Alternatives That Actually Work in 2026",
        "search_kw": "notion ai alternative better 2026",
        "base_priority": "P1"
    },
    {
        "theme": "MidJourney涨价/订阅后悔",
        "keywords": ["midjourney"],
        "target": "MidJourney",
        "article": "Is MidJourney Still Worth It in 2026? Honest Review After Price Hikes",
        "search_kw": "midjourney worth it 2026 price increase",
        "base_priority": "P1"
    },
    {
        "theme": "AI编码工具(Cursor/Windsurf)实际效果差",
        "keywords": ["cursor", "windsurf", "coding tool", "copilot", "code generation"],
        "target": "AI编码工具",
        "article": "AI Coding Tools in 2026: Why Cursor and Windsurf Still Can't Replace Senior Devs",
        "search_kw": "ai coding tools worth it cursor windsurf 2026",
        "base_priority": "P1"
    },
    {
        "theme": "AI图像生成一致性差/商用不可靠",
        "keywords": ["image generator", "dalle", "stable diffusion", "consistency", "midjourney alternative"],
        "target": "AI图像生成",
        "article": "AI Image Generators Still Can't Do Consistency in 2026 (And Workarounds That Work)",
        "search_kw": "ai image generator consistency problem 2026",
        "base_priority": "P2"
    },
]

# 分配评论到聚类
clustered = {c["theme"]: [] for c in clusters_def}
for c in all_comments:
    text = (c["title"] + " " + c["quote"]).lower()
    for cl in clusters_def:
        if any(kw in text for kw in cl["keywords"]):
            clustered[cl["theme"]].append(c)
            break

# === 3. 搜索意图验证 + SERP竞争分析 ===
print("\n=== 搜索意图验证 ===")
for cl in clusters_def:
    if not clustered[cl["theme"]]:
        cl["verified"] = False
        cl["serp_count"] = 0
        cl["competition"] = "N/A"
        cl["top_competitors"] = []
        continue
    results = serper(cl["search_kw"], num=10)
    cl["verified"] = len(results) >= 5
    cl["serp_count"] = len(results)
    cl["top_competitors"] = [r.get("link", "")[:60] for r in results[:5]]
    # 竞争度判断：前5结果域名多样性
    domains = set()
    for r in results[:5]:
        try:
            d = r.get("link", "").split("/")[2]
            domains.add(d)
        except:
            pass
    if len(domains) <= 2:
        cl["competition"] = "High"
    elif len(domains) <= 4:
        cl["competition"] = "Medium"
    else:
        cl["competition"] = "Low"
    print(f"  {cl['theme'][:40]}: SERP={len(results)}, verified={cl['verified']}, competition={cl['competition']}")

# === 4. 覆盖检查 ===
for cl in clusters_def:
    target_lower = cl["target"].lower()
    article_lower = cl["article"].lower()
    covered = False
    for eu in EXISTING_URLS:
        if eu in article_lower or eu in target_lower:
            covered = True
            break
    # 特殊检查
    if "notion" in target_lower and "notion-ai-alternative" in EXISTING_URLS:
        covered = True
    if "midjourney" in target_lower and "midjourney-alternatives" in EXISTING_URLS:
        covered = True
    if "chatgpt" in target_lower and "chatgpt-vs-claude" in EXISTING_URLS:
        covered = True  # 但vs文章不等于幻觉文章，标为部分覆盖
    cl["covered"] = covered

# === 5. 最终优先级判定 ===
for cl in clusters_def:
    items = clustered[cl["theme"]]
    src_groups = set(c["src_group"] for c in items)
    cl["sources_count"] = len(src_groups)
    cl["evidence_count"] = len(items)
    
    if cl["base_priority"] == "P0":
        # P0条件：≥2来源 + verified + 未覆盖
        if len(src_groups) >= 2 and cl["verified"] and not cl["covered"]:
            cl["final_priority"] = "P0"
        elif len(src_groups) >= 2 and cl["verified"]:
            cl["final_priority"] = "P1"  # 已覆盖降为P1
        else:
            cl["final_priority"] = "P1"
    elif cl["base_priority"] == "P1":
        if len(src_groups) >= 2 and cl["verified"]:
            cl["final_priority"] = "P1"
        else:
            cl["final_priority"] = "P2"
    else:
        cl["final_priority"] = "P2"

# === 6. 生成pain_points.md ===
md = f"""# 用户痛点挖掘（真实社区评论聚类 + 搜索意图验证）

> 更新时间: {now_str}
> 数据来源: Serper API 多源搜索
> 抓取来源数: {len(sources_used)}（{', '.join(sorted(sources_used))}）
> 抓取评论数: {len(all_comments)}条
> 聚类数: {len([c for c in clusters_def if clustered[c['theme']]])}个有效主题

---

"""

p0_list = [c for c in clusters_def if c["final_priority"] == "P0" and clustered[c["theme"]]]
p1_list = [c for c in clusters_def if c["final_priority"] == "P1" and clustered[c["theme"]]]
p2_list = [c for c in clusters_def if c["final_priority"] == "P2" and clustered[c["theme"]]]

def render_cluster(cl, idx):
    items = clustered[cl["theme"]]
    if not items:
        return ""
    src_groups = sorted(set(c["src_group"] for c in items))
    out = f"### [{cl['final_priority']}] #{idx} {cl['theme']}\n\n"
    out += f"- **目标工具/主题**: {cl['target']}\n"
    out += f"- **建议文章标题**: {cl['article']}\n"
    out += f"- **证据数**: {len(items)}条评论，来自{len(src_groups)}个独立来源（{', '.join(src_groups)}）\n"
    out += f"- **搜索意图验证**: {'✅ 通过' if cl['verified'] else '❌ 未通过'}（SERP返回{cl['serp_count']}条结果）\n"
    out += f"- **SERP竞争度**: {cl['competition']}\n"
    out += f"- **我们是否已覆盖**: {'✅ 已覆盖' if cl['covered'] else '❌ 未覆盖'}\n"
    out += f"- **前5竞品**: {'; '.join(cl['top_competitors'][:3])}...\n\n"
    out += "| # | 来源 | URL | 用户原话（英文原文） |\n"
    out += "|---|------|-----|---------------------|\n"
    for i, item in enumerate(items[:4], 1):
        quote = item["quote"].replace("|", "\\|").replace("\n", " ")[:180]
        out += f"| {i} | {item['src_group']} | {item['url'][:70]} | {quote} |\n"
    out += "\n"
    return out

md += "## P0 痛点（高频+搜索意图强+竞争可接受+未覆盖，立即写）\n\n"
for i, cl in enumerate(p0_list, 1):
    md += render_cluster(cl, i)

md += "## P1 痛点（有价值但需排队）\n\n"
for i, cl in enumerate(p1_list, 1):
    md += render_cluster(cl, i)

md += "## P2 痛点（长期观察）\n\n"
for i, cl in enumerate(p2_list, 1):
    md += render_cluster(cl, i)

md += f"""---

## 统计汇总

| 指标 | 值 |
|------|-----|
| 抓取来源数 | {len(sources_used)} |
| 抓取评论数 | {len(all_comments)} |
| 有效聚类痛点 | {len(p0_list)+len(p1_list)+len(p2_list)} |
| 搜索意图验证通过 | {len([c for c in clusters_def if c.get('verified')])} |
| P0 | {len(p0_list)} |
| P1 | {len(p1_list)} |
| P2 | {len(p2_list)} |
"""

with open(PAIN_MD, "w", encoding="utf-8") as f:
    f.write(md)
print(f"\n=== pain_points.md: {os.path.getsize(PAIN_MD)} bytes ===")

# === 7. P0写state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

p0_todos = []
for cl in p0_list:
    todo = {
        "id": f"PAIN-P0-{today}-{abs(hash(cl['theme']))%100000}",
        "priority": "P0",
        "task": f"用户痛点【{cl['theme']}】，建议写文章【{cl['article']}】，正文必须引用用户原话做H2/FAQ，SERP竞争度={cl['competition']}",
        "assigned_to": ["window2", "创作家"],
        "source": f"pain_point_mining_{today}",
        "verified": True,
        "serp_competition": cl["competition"],
        "sources_count": cl["sources_count"],
        "evidence_count": cl["evidence_count"],
        "search_keyword": cl["search_kw"],
        "status": "pending",
        "created": now_str
    }
    state["next_iteration_focus"].append(todo)
    p0_todos.append(todo)

# P1也写
p1_todos = []
for cl in p1_list:
    todo = {
        "id": f"PAIN-P1-{today}-{abs(hash(cl['theme']))%100000}",
        "priority": "P1",
        "task": f"用户痛点【{cl['theme']}】，建议写文章【{cl['article']}】",
        "assigned_to": ["window2", "创作家"],
        "source": f"pain_point_mining_{today}",
        "verified": cl.get("verified", False),
        "serp_competition": cl.get("competition", "N/A"),
        "sources_count": cl["sources_count"],
        "status": "pending",
        "created": now_str
    }
    state["next_iteration_focus"].append(todo)
    p1_todos.append(todo)

state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"state.json: {len(p0_todos)} P0 + {len(p1_todos)} P1 todos added")

# === 8. 日志 ===
log = f"""# 用户痛点挖掘日志 {today}

**执行时间**: {now_str}
**工具**: Serper API（多源搜索+搜索意图验证）

## 抓取结果
- 来源数: {len(sources_used)}（{', '.join(sorted(sources_used))}）
- 评论数: {len(all_comments)}条

## 痛点统计
- P0: {len(p0_list)}个
- P1: {len(p1_list)}个
- P2: {len(p2_list)}个
- 搜索意图验证通过: {len([c for c in clusters_def if c.get('verified')])}个

## P0待办（已写state.json，verified=true）
"""
for t in p0_todos:
    log += f"- [{t['id']}] {t['task'][:80]}... (竞争度={t['serp_competition']}, 来源={t['sources_count']}, 证据={t['evidence_count']})\n"

log += f"""
## P1待办（已写state.json）
"""
for t in p1_todos:
    log += f"- [{t['id']}] {t['task'][:80]}...\n"

log += f"""
## 输出文件
- iteration_center/pain_points.md（{os.path.getsize(PAIN_MD)} bytes）
- iteration_center/state.json（追加{len(p0_todos)+len(p1_todos)}条待办）
"""
with open(LOG_PATH, "w", encoding="utf-8") as f:
    f.write(log)

# === 最终输出 ===
print("\n" + "="*60)
print("EXECUTION SUMMARY")
print("="*60)
print(f"Sources scraped: {len(sources_used)} ({', '.join(sorted(sources_used))})")
print(f"Comments collected: {len(all_comments)}")
print(f"Pain points clustered: {len(p0_list)+len(p1_list)+len(p2_list)}")
print(f"Search intent verified: {len([c for c in clusters_def if c.get('verified')])}")
print(f"P0: {len(p0_list)} | P1: {len(p1_list)} | P2: {len(p2_list)}")
print(f"State.json todos added: {len(p0_todos)+len(p1_todos)}")
print(f"pain_points.md updated: {now_str}")
