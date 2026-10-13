#!/usr/bin/env python3
"""拓荒者-用户痛点挖掘: 用Serper API抓取真实用户评论"""
import requests
import json
import os
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

# === 8个真实社区搜索查询 ===
queries = [
    ("Reddit r/ChatGPT 定价抱怨", 'site:reddit.com/r/ChatGPT expensive OR "too expensive" OR pricing complaint'),
    ("Reddit AI写作幻觉", 'site:reddit.com ChatGPT hallucination OR "made up" OR "wrong answer" OR inaccurate'),
    ("Reddit AI视频生成贵", 'site:reddit.com "AI video generator" expensive OR pricing OR credits OR "too expensive"'),
    ("Reddit r/SaaS AI工具问题", 'site:reddit.com/r/SaaS "AI tool" frustrating OR issue OR "waste of money" OR buggy'),
    ("HN AI工具抱怨", 'site:news.ycombinator.com AI tool complaint OR frustrating OR disappointing OR "not worth"'),
    ("G2 AI工具1星差评", 'site:g2.com "AI" review "1 star" OR "low value" OR "would not recommend"'),
    ("Reddit Notion AI替代", 'site:reddit.com "Notion AI" alternative OR "better than" OR disappointed'),
    ("Reddit MidJourney订阅抱怨", 'site:reddit.com MidJourney pricing OR subscription OR "cancel" OR expensive'),
]

def serper(q, num=10):
    try:
        r = requests.post(SERPER_URL, headers=HEADERS, json={"q": q, "num": num}, timeout=20)
        return r.json().get("organic", [])
    except Exception as e:
        print(f"  [ERR] {q[:50]}: {e}")
        return []

# === 抓取 ===
all_comments = []  # (source_label, url, title, snippet)
sources_used = set()
for label, q in queries:
    print(f"\n=== {label} ===")
    print(f"  Q: {q}")
    results = serper(q, num=10)
    for r in results:
        url = r.get("link", "")
        snippet = r.get("snippet", "")
        title = r.get("title", "")
        if snippet and len(snippet) > 40:
            all_comments.append({
                "source": label,
                "url": url,
                "title": title,
                "quote": snippet
            })
            if "reddit.com" in url:
                sources_used.add("Reddit")
            elif "news.ycombinator.com" in url:
                sources_used.add("Hacker News")
            elif "g2.com" in url:
                sources_used.add("G2")
    print(f"  got {len(results)} results")

print(f"\n=== Total comments with snippet: {len(all_comments)} ===")
print(f"=== Sources: {sources_used} ===")

# === 痛点聚类（基于关键词） ===
# 每个聚类: 标签、匹配关键词、目标工具、文章标题模板
clusters = [
    {
        "theme": "ChatGPT/AI写作工具幻觉多、编造事实",
        "keywords": ["hallucination", "made up", "wrong", "inaccurate", "fabricated", "lie", "nonsense"],
        "target_tool": "ChatGPT / AI写作",
        "article_title": "ChatGPT Hallucinations in 2026: Why It Still Makes Up Facts (And How to Catch It)",
        "priority": "P0"
    },
    {
        "theme": "AI工具订阅太贵、不值",
        "keywords": ["expensive", "pricing", "too expensive", "worth", "waste", "subscription", "cancel", "not worth"],
        "target_tool": "通用AI工具定价",
        "article_title": "AI Tools That Are Not Worth the Money in 2026 (And Cheaper Alternatives)",
        "priority": "P0"
    },
    {
        "theme": "AI视频生成credits/积分烧太快",
        "keywords": ["video generator", "credits", "video", "runway", "pika", "sora", "image generation"],
        "target_tool": "AI视频生成",
        "article_title": "Why AI Video Generators Burn Through Credits Fast (And Free Alternatives)",
        "priority": "P0"
    },
    {
        "theme": "SaaS老板用AI工具反而更麻烦",
        "keywords": ["saas", "frustrating", "buggy", "integration", "workflow", "waste of time"],
        "target_tool": "SaaS AI工具",
        "article_title": "AI Tools for SaaS in 2026: What Actually Works vs. What's Hype",
        "priority": "P1"
    },
    {
        "theme": "Notion AI令人失望、找替代",
        "keywords": ["notion", "notion ai"],
        "target_tool": "Notion AI",
        "article_title": "Notion AI Is Disappointing? Here Are 7 Real Alternatives in 2026",
        "priority": "P1"
    },
    {
        "theme": "MidJourney订阅后悔/想取消",
        "keywords": ["midjourney", "midjourney pricing"],
        "target_tool": "MidJourney",
        "article_title": "Is MidJourney Still Worth It in 2026? Honest Review After Price Hikes",
        "priority": "P1"
    },
    {
        "theme": "HN对AI工具失望/不实用",
        "keywords": ["not worth", "disappointing", "overhyped", "waste"],
        "target_tool": "AI工具整体",
        "article_title": "Hacker News Hates These AI Tools for Good Reason (2026)",
        "priority": "P2"
    },
]

# 把评论分配到聚类
clustered = {c["theme"]: [] for c in clusters}
unassigned = []
for c in all_comments:
    text = (c["title"] + " " + c["quote"]).lower()
    matched = False
    for cl in clusters:
        if any(kw in text for kw in cl["keywords"]):
            clustered[cl["theme"]].append(c)
            matched = True
            break
    if not matched:
        unassigned.append(c)

# === 生成pain_points.md ===
md = f"""# 用户痛点挖掘（真实社区评论聚类）

> 更新时间: {now_str}
> 数据来源: Serper API 搜索真实社区页面
> 抓取来源数: {len(sources_used)}（{', '.join(sorted(sources_used))}）
> 抓取评论数: {len(all_comments)}条带snippet的真实用户内容
> 聚类数: {len(clusters)}个主题

---

## P0 痛点（高频+有搜索意图，立即写文章）

"""

p0_count = 0
p1_count = 0
p2_count = 0

for cl in clusters:
    items = clustered[cl["theme"]]
    if not items:
        continue
    if cl["priority"] == "P0":
        p0_count += 1
    elif cl["priority"] == "P1":
        p1_count += 1
    else:
        p2_count += 1
    
    md += f"### [{cl['priority']}] {cl['theme']}\n\n"
    md += f"- **目标工具/主题**: {cl['target_tool']}\n"
    md += f"- **建议文章标题**: {cl['article_title']}\n"
    md += f"- **聚类到的真实评论数**: {len(items)}\n\n"
    md += "| # | 来源URL | 用户原话（英文原文snippet） |\n"
    md += "|---|---------|---------------------------|\n"
    for i, item in enumerate(items[:4], 1):
        quote = item["quote"].replace("|", "\\|").replace("\n", " ")[:200]
        md += f"| {i} | {item['url'][:80]} | {quote} |\n"
    md += "\n"

md += f"""---

## 未归类评论（{len(unassigned)}条，留作后续挖掘素材）

| # | 来源 | URL | 摘要 |
|---|------|-----|------|
"""
for i, item in enumerate(unassigned[:10], 1):
    md += f"| {i} | {item['source']} | {item['url'][:60]} | {item['quote'][:120]} |\n"

md += f"""
---

## 统计

- 抓取来源: {len(sources_used)}个（{', '.join(sorted(sources_used))}）
- 抓取评论: {len(all_comments)}条
- P0痛点: {p0_count}个
- P1痛点: {p1_count}个
- P2痛点: {p2_count}个
"""

with open(PAIN_MD, "w", encoding="utf-8") as f:
    f.write(md)
print(f"\n=== pain_points.md written: {os.path.getsize(PAIN_MD)} bytes ===")

# === 更新state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

# 为每个P0痛点写待办
p0_todos = []
for cl in clusters:
    if cl["priority"] != "P0":
        continue
    if not clustered[cl["theme"]]:
        continue
    todo = {
        "id": f"PAIN-P0-{today}-{hash(cl['theme'])%10000}",
        "priority": "P0",
        "task": f"用户痛点【{cl['theme']}】，建议写文章【{cl['article_title']}】，正文必须引用用户原话做H2/FAQ",
        "assigned_to": ["window2", "创作家"],
        "source": f"pain_point_mining_{today}",
        "target_tool": cl["target_tool"],
        "evidence_count": len(clustered[cl["theme"]]),
        "status": "pending",
        "created": now_str
    }
    state["next_iteration_focus"].append(todo)
    p0_todos.append(todo)

# P1也写但priority=P1
p1_todos = []
for cl in clusters:
    if cl["priority"] != "P1":
        continue
    if not clustered[cl["theme"]]:
        continue
    todo = {
        "id": f"PAIN-P1-{today}-{hash(cl['theme'])%10000}",
        "priority": "P1",
        "task": f"用户痛点【{cl['theme']}】，建议写文章【{cl['article_title']}】",
        "assigned_to": ["window2", "创作家"],
        "source": f"pain_point_mining_{today}",
        "target_tool": cl["target_tool"],
        "evidence_count": len(clustered[cl["theme"]]),
        "status": "pending",
        "created": now_str
    }
    state["next_iteration_focus"].append(todo)
    p1_todos.append(todo)

state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"state.json updated: {len(p0_todos)} P0 + {len(p1_todos)} P1 todos added")

# === 写日志 ===
log = f"""
# 用户痛点挖掘日志 {today}

**执行时间**: {now_str}
**工具**: Serper API

## 抓取结果
- 来源数: {len(sources_used)}（{', '.join(sorted(sources_used))}）
- 带snippet评论数: {len(all_comments)}条

## 痛点聚类
- P0: {p0_count}个
- P1: {p1_count}个
- P2: {p2_count}个

## P0待办（已写state.json）
"""
for t in p0_todos:
    log += f"- [{t['id']}] {t['task']} (证据{t['evidence_count']}条)\n"

log += f"""
## P1待办（已写state.json）
"""
for t in p1_todos:
    log += f"- [{t['id']}] {t['task']} (证据{t['evidence_count']}条)\n"

log += f"""
## 输出文件
- iteration_center/pain_points.md（{os.path.getsize(PAIN_MD)} bytes）
- iteration_center/state.json（追加{len(p0_todos)+len(p1_todos)}条待办）
"""
with open(LOG_PATH, "w", encoding="utf-8") as f:
    f.write(log)
print(f"Log written to {LOG_PATH}")

# === 最终输出 ===
print("\n" + "="*50)
print("EXECUTION SUMMARY")
print("="*50)
print(f"Sources scraped: {len(sources_used)} ({', '.join(sorted(sources_used))})")
print(f"Comments collected: {len(all_comments)}")
print(f"Pain points clustered: {p0_count+p1_count+p2_count}")
print(f"P0: {p0_count} | P1: {p1_count} | P2: {p2_count}")
print(f"State.json todos added: {len(p0_todos)+len(p1_todos)}")
print(f"pain_points.md updated: {now_str}")
