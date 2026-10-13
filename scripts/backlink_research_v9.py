#!/usr/bin/env python3
"""拓荒者-外链调研 v9: 新免费目录 + 客座博客 + toolify外链 + AI聚合站"""
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
    # 1. 新免费目录（不同于之前关键词）
    ("新免费目录", 'submit AI tool free directory list 2026 -futurepedia -theresanaiforthat -producthunt'),
    # 2. 客座博客pitch（接受guest post的AI博客）
    ("客座博客", '"write for us" OR "guest post" AI tools OR AI software OR SaaS 2026'),
    # 3. toolify.ai竞品外链
    ("toolify外链", "toolify.ai OR toolify backlinks OR listed -site:toolify.ai"),
    # 4. AI工具聚合站/RSS
    ("AI聚合站", 'AI tool aggregator OR AI tools RSS feed OR AI tools newsletter submit'),
    # 5. Reddit r/ChatGPT评论区
    ("r/ChatGPT评论", 'site:reddit.com/r/ChatGPT "best AI" OR "AI tool" OR "alternative to"'),
    # 6. Dev.to客座文章
    ("Dev.to客座", 'site:dev.to "write for us" OR "guest post" AI OR SaaS OR technology'),
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

## 外链调研第九轮（{now_str}）

> 工具: Serper API
> 角度: 新免费目录 + 客座博客 + toolify外链 + AI聚合站 + r/ChatGPT评论

"""

new_dirs = all_results.get("新免费目录", [])
md += "### 一、新免费目录\n\n"
if new_dirs:
    md += "| # | 目录 | URL | 备注 |\n|---|------|-----|------|\n"
    for i, r in enumerate(new_dirs[:6], 1):
        md += f"| {i} | {r.get('title','')[:45]} | {r.get('link','')[:55]} | {r.get('snippet','')[:35]} |\n"

guest = all_results.get("客座博客", [])
md += "\n### 二、客座博客（接受投稿）\n\n"
if guest:
    md += "| # | 博客 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(guest[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

toolify = all_results.get("toolify外链", [])
md += "\n### 三、toolify.ai外链来源\n\n"
if toolify:
    md += "| # | 来源 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(toolify[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

aggregator = all_results.get("AI聚合站", [])
md += "\n### 四、AI聚合站/Newsletter\n\n"
if aggregator:
    md += "| # | 聚合站 | URL |\n|---|--------|-----|\n"
    for i, r in enumerate(aggregator[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

reddit = all_results.get("r/ChatGPT评论", [])
md += "\n### 五、r/ChatGPT评论区\n\n"
if reddit:
    md += "| # | 帖子 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(reddit[:4], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 六、本轮统计
- 新免费目录: {len(new_dirs)}条
- 客座博客: {len(guest)}条
- toolify外链: {len(toolify)}条
- AI聚合站: {len(aggregator)}条
- r/ChatGPT: {len(reddit)}条
- Dev.to客座: {len(all_results.get('Dev.to客座',[]))}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print("\nbacklink_opportunities.md updated")

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = []
if new_dirs:
    todos.append({
        "id": f"GROWTH-DIR-V9-{today}",
        "priority": "P2",
        "title": f"调研{min(2,len(new_dirs))}个第九轮新免费目录",
        "description": "筛选免费、无需登录、编辑审核的目录站",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })
if guest:
    todos.append({
        "id": f"GROWTH-GUEST-{today}",
        "priority": "P1",
        "title": f"向{min(2,len(guest))}个接受guest post的AI博客投稿",
        "description": "客座博客=高质量外链+精准流量",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第九轮",
    "time": now_str,
    "result": f"Serper 6组: 新目录{len(new_dirs)}+客座{len(guest)}+toolify{len(toolify)}+聚合{len(aggregator)}"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 外链调研第九轮（{now_str}）\n\n- 新免费目录: {len(new_dirs)}条\n- 客座博客: {len(guest)}条\n- toolify外链: {len(toolify)}条\n- AI聚合站: {len(aggregator)}条\n- 补录待办: {len(todos)}个\n")
print("Done.")
