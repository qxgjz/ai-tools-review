#!/usr/bin/env python3
"""拓荒者-外链调研 v8: Newsletter + Reddit求推荐 + TAIAF反向链接 + 榜单站"""
import urllib.request, json, os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
SERPER_URL = "https://google.serper.dev/search"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
OPPORTUNITIES = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

def serper(q, num=10):
    try:
        data = json.dumps({"q": q, "num": num}).encode()
        req = urllib.request.Request(SERPER_URL, data=data, headers=HEADERS, method="POST")
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get("organic", [])
    except Exception as e:
        print(f"  [ERR] {q[:50]}: {e}")
        return []

searches = [
    # 1. Newsletter投稿（AI工具类newsletter接受推荐）
    ("AI Newsletter投稿", "AI tool newsletter submit OR recommend OR feature 2026"),
    # 2. Reddit求AI工具推荐（评论区自然推荐）
    ("Reddit求推荐", 'site:reddit.com/r/SaaS OR site:reddit.com/r/smallbusiness OR site:reddit.com/r/Entrepreneur "best AI tool" OR "looking for AI" OR "AI alternative"'),
    # 3. TAIAF竞品反向链接
    ("TAIAF外链来源", "theresanaiforthat.com OR theresanaiforthat backlinks OR listed -site:theresanaiforthat.com"),
    # 4. AI工具榜单/排名站
    ("AI榜单站", '"top AI tools" OR "best AI software" OR "AI tool ranking" 2026 submit OR list'),
    # 5. LinkedIn/Medium客座博客
    ("LinkedIn/Medium", 'site:medium.com OR site:linkedin.com "AI tools" OR "AI software" 2026 list OR review'),
    # 6. 播客/YouTube pitch
    ("播客/YouTube pitch", 'AI podcast OR "AI tools" youtube channel review submit OR pitch OR guest'),
]

all_results = {}
for label, q in searches:
    print(f"\n=== {label} ===")
    results = serper(q, num=10)
    all_results[label] = results
    for i, r in enumerate(results[:5]):
        print(f"  {i+1}. {r.get('title','')[:55]}")
        print(f"     {r.get('link','')[:70]}")

md = f"""

---

## 外链调研第八轮（{now_str}）

> 工具: Serper API
> 角度: Newsletter投稿 + Reddit求推荐 + TAIAF反向链接 + AI榜单站 + LinkedIn/Medium + 播客

"""

# Newsletter
news = all_results.get("AI Newsletter投稿", [])
md += "### 一、AI Newsletter投稿\n\n"
if news:
    md += "| # | Newsletter | URL |\n|---|-----------|-----|\n"
    for i, r in enumerate(news[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

# Reddit
reddit = all_results.get("Reddit求推荐", [])
md += "\n### 二、Reddit求推荐帖（评论区自然推荐）\n\n"
if reddit:
    md += "| # | 帖子 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(reddit[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

# TAIAF
taiaf = all_results.get("TAIAF外链来源", [])
md += "\n### 三、TAIAF反向链接来源\n\n"
if taiaf:
    md += "| # | 来源站 | URL |\n|---|--------|-----|\n"
    for i, r in enumerate(taiaf[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

# 榜单站
rankings = all_results.get("AI榜单站", [])
md += "\n### 四、AI榜单/排名站\n\n"
if rankings:
    md += "| # | 榜单 | URL | 备注 |\n|---|------|-----|------|\n"
    for i, r in enumerate(rankings[:6], 1):
        md += f"| {i} | {r.get('title','')[:45]} | {r.get('link','')[:55]} | {r.get('snippet','')[:35]} |\n"

# LinkedIn/Medium
li = all_results.get("LinkedIn/Medium", [])
md += "\n### 五、LinkedIn/Medium客座\n\n"
if li:
    md += "| # | 文章 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(li[:4], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

# 播客
pod = all_results.get("播客/YouTube pitch", [])
md += "\n### 六、播客/YouTube\n\n"
if pod:
    md += "| # | 频道 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(pod[:4], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 七、本轮统计
- Newsletter投稿: {len(news)}条
- Reddit求推荐: {len(reddit)}条
- TAIAF反向链接: {len(taiaf)}条
- AI榜单站: {len(rankings)}条
- LinkedIn/Medium: {len(li)}条
- 播客/YouTube: {len(pod)}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print("\nbacklink_opportunities.md updated")

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = []
if news:
    todos.append({
        "id": f"GROWTH-NEWSLETTER-{today}",
        "priority": "P2",
        "title": f"向{min(2,len(news))}个AI Newsletter推荐AIToolCrux",
        "description": "Newsletter提及=高质量外链",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })
if rankings:
    todos.append({
        "id": f"GROWTH-RANKING-{today}",
        "priority": "P1",
        "title": f"向{min(2,len(rankings))}个AI榜单站提交AIToolCrux",
        "description": "榜单站收录=高权重外链",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第八轮",
    "time": now_str,
    "result": f"Serper 6组: Newsletter{len(news)}+Reddit{len(reddit)}+TAIAF{len(taiaf)}+榜单{len(rankings)}"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 外链调研第八轮（{now_str}）\n\n- Newsletter: {len(news)}条\n- Reddit求推荐: {len(reddit)}条\n- TAIAF反向链接: {len(taiaf)}条\n- AI榜单站: {len(rankings)}条\n- 补录待办: {len(todos)}个\n")
print("Done.")
