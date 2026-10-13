#!/usr/bin/env python3
"""拓荒者-外链调研 v2: 竞品外链分析 + 深挖昨日线索"""
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

# === 本轮搜索: 换角度，找新机会 ===
searches = [
    # 1. 竞品外链来源（找竞品被哪些目录站收录）
    ("竞品Futurepedia外链", 'site:futurepedia.io OR "futurepedia" directory listing AI tools'),
    # 2. 新目录站（昨天没搜的关键词）
    ("新AI目录站2", 'submit AI tool free listing 2026 "no review" OR "instant approval"'),
    # 3. 客座博客（具体AI方向）
    ("AI博客投稿2", '"AI tools" "write for us" OR "contribute guest post" 2026'),
    # 4. 资源页（更具体）
    ("AI工具资源页", '"best AI tools" OR "top AI tools" list 2026 submit your tool'),
    # 5. 未被竞争的小目录站
    ("小目录站", 'new AI tool directory 2026 free submit emerging'),
    # 6. Reddit帖子（直接搜AI工具推荐帖）
    ("Reddit推荐帖", 'site:reddit.com "best AI tools" 2026 OR "recommend AI tool" OR "what AI tool"'),
]

all_results = {}
for label, q in searches:
    print(f"\n=== {label} ===")
    print(f"  Q: {q}")
    results = serper(q, num=10)
    all_results[label] = results
    for i, r in enumerate(results[:6]):
        print(f"  {i+1}. {r.get('title','')[:65]}")
        print(f"     {r.get('link','')[:75]}")

# === 输出到backlink_opportunities.md（追加新一节） ===
md = f"""

---

## 外链调研第二轮（{now_str}）

> 工具: Serper API
> 角度: 竞品外链来源 + 新目录站 + 客座博客 + Reddit推荐帖

### 一、竞品外链线索

"""
comp_results = all_results.get("竞品Futurepedia外链", [])
if comp_results:
    md += "| # | 结果 | URL | 可行动作 |\n|---|------|-----|---------|\n"
    for i, r in enumerate(comp_results[:8], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | 分析是否可同样提交 |\n"

md += f"""
### 二、新发现目录站（即时审核/免费）

"""
new_dirs = all_results.get("新AI目录站2", [])
if new_dirs:
    md += "| # | 目录站 | URL | 备注 |\n|---|--------|-----|------|\n"
    for i, r in enumerate(new_dirs[:8], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | {r.get('snippet','')[:50]} |\n"

md += f"""
### 三、客座博客新机会

"""
guest = all_results.get("AI博客投稿2", [])
if guest:
    md += "| # | 博客 | URL | 备注 |\n|---|------|-----|------|\n"
    for i, r in enumerate(guest[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | {r.get('snippet','')[:50]} |\n"

md += f"""
### 四、Reddit AI工具推荐帖（可参与）

"""
reddit = all_results.get("Reddit推荐帖", [])
if reddit:
    md += "| # | 帖子 | URL | 回复角度 |\n|---|------|-----|---------|\n"
    for i, r in enumerate(reddit[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | 真实评测视角 |\n"

md += f"""
### 五、本轮统计
- 竞品外链线索: {len(comp_results)}条
- 新目录站: {len(new_dirs)}条
- 客座博客: {len(guest)}条
- Reddit推荐帖: {len(reddit)}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print(f"\nbacklink_opportunities.md updated")

# === 更新state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

# 补录待办
new_todos = []
if new_dirs:
    new_todos.append({
        "id": f"GROWTH-DIR-ROUND2-{today}",
        "priority": "P1",
        "title": f"提交{min(3, len(new_dirs))}个本轮新发现的目录站",
        "description": "从第二轮调研结果选3个高DR目录站提交",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })
if reddit:
    new_todos.append({
        "id": f"GROWTH-REDDIT-ROUND2-{today}",
        "priority": "P2",
        "title": f"Reddit回复{min(2, len(reddit))}个AI工具推荐帖",
        "description": "登录后以真实用户身份参与讨论",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(new_todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第二轮",
    "time": now_str,
    "result": f"Serper搜索6组关键词, 竞品{len(comp_results)}+新目录{len(new_dirs)}+客座{len(guest)}+Reddit{len(reddit)}",
})
state["last_updated"] = now_str

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"state.json: +{len(new_todos)} todos")

# === 写日志 ===
log = f"""

---

## 外链调研第二轮（{now_str}）

**工具**: Serper API
**角度**: 换关键词找新机会，不重复第一轮

### 搜索结果
- 竞品Futurepedia外链线索: {len(comp_results)}条
- 新目录站（即时审核/免费）: {len(new_dirs)}条
- 客座博客新机会: {len(guest)}条
- Reddit AI工具推荐帖: {len(reddit)}条

### 输出
- backlink_opportunities.md 追加第二轮章节
- state.json 补录{len(new_todos)}个待办
"""
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log)
print(f"Log written. Done.")
