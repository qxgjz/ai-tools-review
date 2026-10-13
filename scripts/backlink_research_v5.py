#!/usr/bin/env python3
"""拓荒者-外链调研 v5: 竞品topai/toolify + Reddit求推荐 + IH社区 + YouTube"""
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
    # 1. Reddit求推荐帖（可回复推荐AIToolCrux）
    ("Reddit求推荐", 'site:reddit.com "best AI tool" OR "AI tool recommendation" OR "what AI tool" 2026'),
    # 2. Indie Hackers社区
    ("IH社区", 'site:indiehackers.com "AI tool" submit OR list OR directory'),
    # 3. 竞品topai.tools外链
    ("竞品topai", 'topai.tools OR "top AI tools" directory submit free'),
    # 4. YouTube AI评测视频（描述可放外链）
    ("YouTube评测", 'AI tool review video 2026 best AI tools comparison youtube'),
    # 5. 新免费目录（2026新出现的）
    ("2026新目录", '"free AI tool directory" OR "submit AI tool" 2026 -paid -listing'),
    # 6. Quora/知乎类问答（可回答带链接）
    ("Quora问答", 'site:quora.com "best AI tool" OR "AI tool review" OR "AI tool comparison"'),
]

all_results = {}
for label, q in searches:
    print(f"\n=== {label} ===")
    results = serper(q, num=10)
    all_results[label] = results
    for i, r in enumerate(results[:5]):
        print(f"  {i+1}. {r.get('title','')[:60]}")
        print(f"     {r.get('link','')[:70]}")

# 输出md
md = f"""

---

## 外链调研第五轮（{now_str}）

> 工具: Serper API
> 角度: Reddit求推荐 + IH社区 + 竞品topai + YouTube + 2026新目录 + Quora

### 一、Reddit求推荐帖（可回复推荐）

"""
reddit = all_results.get("Reddit求推荐", [])
if reddit:
    md += "| # | 帖子 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(reddit[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 二、Indie Hackers社区

"""
ih = all_results.get("IH社区", [])
if ih:
    md += "| # | 帖子 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(ih[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 三、2026新免费目录站

"""
new_dirs = all_results.get("2026新目录", [])
if new_dirs:
    md += "| # | 目录 | URL | 备注 |\n|---|------|-----|------|\n"
    for i, r in enumerate(new_dirs[:6], 1):
        md += f"| {i} | {r.get('title','')[:45]} | {r.get('link','')[:55]} | {r.get('snippet','')[:40]} |\n"

md += f"""
### 四、本轮统计
- Reddit求推荐: {len(reddit)}条
- IH社区: {len(ih)}条
- 竞品topai: {len(all_results.get('竞品topai',[]))}条
- YouTube评测: {len(all_results.get('YouTube评测',[]))}条
- 2026新目录: {len(new_dirs)}条
- Quora问答: {len(all_results.get('Quora问答',[]))}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print(f"\nbacklink_opportunities.md updated")

# state
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = []
if new_dirs:
    todos.append({
        "id": f"GROWTH-DIR-V5-{today}",
        "priority": "P2",
        "title": f"调研{min(2,len(new_dirs))}个第五轮新发现目录站",
        "description": "筛选免费、无需登录的目录站",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })
if reddit:
    todos.append({
        "id": f"GROWTH-REDDIT-REPLY-{today}",
        "priority": "P1",
        "title": f"在Reddit求推荐帖中回复推荐AIToolCrux（{len(reddit)}个候选）",
        "description": "需Reddit登录态，回复要自然不spam",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第五轮",
    "time": now_str,
    "result": f"Serper 6组: Reddit{len(reddit)}+IH{len(ih)}+新目录{len(new_dirs)}+Quora{len(all_results.get('Quora问答',[]))}"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"state.json: +{len(todos)} todos")

log = f"""

---

## 外链调研第五轮（{now_str}）

**角度**: Reddit求推荐 + IH社区 + 2026新目录 + Quora

### 结果
- Reddit求推荐帖: {len(reddit)}个候选
- 新免费目录: {len(new_dirs)}个
- Quora问答: {len(all_results.get('Quora问答',[]))}个

### 补录待办: {len(todos)}个
"""
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log)
print("Done.")
