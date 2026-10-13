#!/usr/bin/env python3
"""拓荒者-外链调研 v7: 竞品backlink + Dev.to/Hashnode + 2026Q4新目录"""
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
    # 1. 竞品futurepedia的backlink来源（哪些站链接到它）
    ("竞品futurepedia", '"futurepedia.io" OR "futurepedia" backlinks OR listed OR directory -site:futurepedia.io'),
    # 2. Dev.to/Hashnode技术博客投稿
    ("Dev.to/Hashnode", 'site:dev.to OR site:hashnode.com "AI tool" review OR list OR comparison 2026'),
    # 3. 2026 Q4新AI目录
    ("2026Q4新目录", '"AI tool directory" OR "AI tools list" submit November OR December OR Q4 2026'),
    # 4. Reddit r/SideProject / r/learnprogramming launch
    ("Reddit侧边项目", 'site:reddit.com/r/SideProject OR site:reddit.com/r/learnprogramming "AI tool" launch OR built'),
    # 5. 资源页"best AI tools 2026"（争取被收录）
    ("资源页", '"best AI tools 2026" OR "top AI tools 2026" list OR roundup -youtube -linkedin'),
    # 6. 播客/YouTube提及
    ("播客/YouTube", 'AI tool podcast OR "AI tools" youtube channel review submit OR pitch'),
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

## 外链调研第七轮（{now_str}）

> 工具: Serper API
> 角度: 竞品futurepedia backlink + Dev.to/Hashnode + 2026Q4新目录 + Reddit侧边项目 + 资源页

### 一、竞品futurepedia反向链接

"""
fp = all_results.get("竞品futurepedia", [])
if fp:
    md += "| # | 来源站 | URL |\n|---|--------|-----|\n"
    for i, r in enumerate(fp[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 二、Dev.to/Hashnode技术博客

"""
devto = all_results.get("Dev.to/Hashnode", [])
if devto:
    md += "| # | 文章 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(devto[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 三、2026 Q4新AI目录

"""
new_dirs = all_results.get("2026Q4新目录", [])
if new_dirs:
    md += "| # | 目录 | URL | 备注 |\n|---|------|-----|------|\n"
    for i, r in enumerate(new_dirs[:6], 1):
        md += f"| {i} | {r.get('title','')[:45]} | {r.get('link','')[:55]} | {r.get('snippet','')[:40]} |\n"

md += f"""
### 四、资源页"best AI tools 2026"

"""
resources = all_results.get("资源页", [])
if resources:
    md += "| # | 资源页 | URL |\n|---|--------|-----|\n"
    for i, r in enumerate(resources[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 五、本轮统计
- 竞品futurepedia: {len(fp)}条
- Dev.to/Hashnode: {len(devto)}条
- 2026Q4新目录: {len(new_dirs)}条
- Reddit侧边项目: {len(all_results.get('Reddit侧边项目',[]))}条
- 资源页: {len(resources)}条
- 播客/YouTube: {len(all_results.get('播客/YouTube',[]))}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print(f"\nbacklink_opportunities.md updated")

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = []
if new_dirs:
    todos.append({
        "id": f"GROWTH-DIR-V7-{today}",
        "priority": "P2",
        "title": f"调研{min(2,len(new_dirs))}个第七轮新目录站",
        "description": "筛选免费、无需登录的目录站",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })
if resources:
    todos.append({
        "id": f"GROWTH-RESOURCE-PITCH-{today}",
        "priority": "P1",
        "title": f"向{min(3,len(resources))}个'best AI tools 2026'资源页发邮件推荐AIToolCrux",
        "description": "资源页收录是高质量外链",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第七轮",
    "time": now_str,
    "result": f"Serper 6组: 竞品{len(fp)}+Dev.to{len(devto)}+新目录{len(new_dirs)}+资源页{len(resources)}"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 外链调研第七轮（{now_str}）\n\n- 竞品futurepedia: {len(fp)}条\n- Dev.to/Hashnode: {len(devto)}条\n- 2026Q4新目录: {len(new_dirs)}条\n- 资源页: {len(resources)}条\n- 补录待办: {len(todos)}个\n")
print("Done.")
