#!/usr/bin/env python3
"""拓荒者-外链调研 v6: Product Hunt/BetaList + LinkedIn + 新垂直目录"""
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
    # 1. Product Hunt / BetaList类提交
    ("PH/BetaList", '"product hunt" OR "betalist" OR "startup stash" submit AI tool 2026'),
    # 2. 新垂直AI目录（2026新）
    ("垂直目录", '"AI tool directory" OR "AI tools list" submit free 2026 -paid'),
    # 3. Reddit r/SaaS r/Entrepreneur
    ("Reddit SaaS", 'site:reddit.com/r/SaaS OR site:reddit.com/r/Entrepreneur "AI tool" launch OR review OR list'),
    # 4. LinkedIn发布（可带链接）
    ("LinkedIn", '"best AI tools" OR "AI tool review" linkedin article 2026'),
    # 5. 客座博客（具体SEO/AI方向）
    ("客座博客", '"write for us" AI tools OR "AI review" OR "AI directory" blog 2026'),
    # 6. 邮件通讯/Newsletter提及
    ("Newsletter", 'AI tools newsletter submit OR "AI tools roundup" OR "best AI tools weekly"'),
]

all_results = {}
for label, q in searches:
    print(f"\n=== {label} ===")
    results = serper(q, num=10)
    all_results[label] = results
    for i, r in enumerate(results[:5]):
        print(f"  {i+1}. {r.get('title','')[:60]}")
        print(f"     {r.get('link','')[:70]}")

md = f"""

---

## 外链调研第六轮（{now_str}）

> 工具: Serper API
> 角度: PH/BetaList + 垂直目录 + Reddit SaaS + LinkedIn + 客座博客 + Newsletter

### 一、Product Hunt / BetaList类

"""
ph = all_results.get("PH/BetaList", [])
if ph:
    md += "| # | 平台 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(ph[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 二、新垂直AI目录

"""
vd = all_results.get("垂直目录", [])
if vd:
    md += "| # | 目录 | URL | 备注 |\n|---|------|-----|------|\n"
    for i, r in enumerate(vd[:6], 1):
        md += f"| {i} | {r.get('title','')[:45]} | {r.get('link','')[:55]} | {r.get('snippet','')[:40]} |\n"

md += f"""
### 三、客座博客

"""
guest = all_results.get("客座博客", [])
if guest:
    md += "| # | 博客 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(guest[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 四、本轮统计
- PH/BetaList: {len(ph)}条
- 垂直目录: {len(vd)}条
- Reddit SaaS: {len(all_results.get('Reddit SaaS',[]))}条
- LinkedIn: {len(all_results.get('LinkedIn',[]))}条
- 客座博客: {len(guest)}条
- Newsletter: {len(all_results.get('Newsletter',[]))}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print(f"\nbacklink_opportunities.md updated")

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = []
if vd:
    todos.append({
        "id": f"GROWTH-DIR-V6-{today}",
        "priority": "P2",
        "title": f"调研{min(2,len(vd))}个第六轮新目录站",
        "description": "筛选免费、无需登录的目录站",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第六轮",
    "time": now_str,
    "result": f"Serper 6组: PH{len(ph)}+垂直目录{len(vd)}+客座{len(guest)}+Reddit{len(all_results.get('Reddit SaaS',[]))}"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 外链调研第六轮（{now_str}）\n\n- PH/BetaList: {len(ph)}条\n- 垂直目录: {len(vd)}条\n- 客座博客: {len(guest)}条\n- 补录待办: {len(todos)}个\n")
print("Done.")
