#!/usr/bin/env python3
"""拓荒者-外链调研 v3: 垂直目录 + broken link + GitHub awesome"""
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
    # 1. GitHub awesome列表（在README被提及=免费外链）
    ("GitHub Awesome列表", 'site:github.com "awesome AI tools" OR "awesome ai" list 2026'),
    # 2. Broken link building（找断链资源页）
    ("断链资源页", '"best AI tools" "top AI tools" resource page submit your site'),
    # 3. 垂直细分目录（AI写作/视频/图像）
    ("垂直AI目录", 'AI writing tools directory OR AI video tools directory OR AI image tools directory submit'),
    # 4. Product Hunt相关（被收录后的二级外链）
    ("Product Hunt二级", 'site:producthunt.com "AI tools" review OR list OR collection 2026'),
    # 5. 问答社区外链（Quora/Stack Overflow）
    ("问答社区", 'site:quora.com "best AI tools" OR "AI tool review" recommendation 2026'),
    # 6. 竞品toolify外链来源
    ("竞品Toolify", '"toolify.ai" OR "toolify" directory listing backlink source'),
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

# === 输出到backlink_opportunities.md ===
md = f"""

---

## 外链调研第三轮（{now_str}）

> 工具: Serper API
> 角度: GitHub awesome列表 + 断链资源页 + 垂直目录 + Quora + 竞品Toolify

### 一、GitHub Awesome列表（README外链）

"""
gh = all_results.get("GitHub Awesome列表", [])
if gh:
    md += "| # | 仓库 | URL | 可行动作 |\n|---|------|-----|---------|\n"
    for i, r in enumerate(gh[:8], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | 提PR或邮件请求收录 |\n"

md += f"""
### 二、垂直细分AI目录站

"""
vert = all_results.get("垂直AI目录", [])
if vert:
    md += "| # | 目录站 | URL | 细分领域 |\n|---|--------|-----|---------|\n"
    for i, r in enumerate(vert[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | {r.get('snippet','')[:40]} |\n"

md += f"""
### 三、Quora问答（可回答带链接）

"""
quora = all_results.get("问答社区", [])
if quora:
    md += "| # | 问题 | URL | 回答角度 |\n|---|------|-----|---------|\n"
    for i, r in enumerate(quora[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | 引用评测 |\n"

md += f"""
### 四、竞品Toolify外链线索

"""
toolify = all_results.get("竞品Toolify", [])
if toolify:
    md += "| # | 结果 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(toolify[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 五、本轮统计
- GitHub awesome列表: {len(gh)}条
- 断链资源页: {len(all_results.get('断链资源页',[]))}条
- 垂直目录: {len(vert)}条
- Product Hunt二级: {len(all_results.get('Product Hunt二级',[]))}条
- Quora问答: {len(quora)}条
- 竞品Toolify: {len(toolify)}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print(f"\nbacklink_opportunities.md updated")

# === 更新state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = []
if gh:
    todos.append({
        "id": f"GROWTH-GITHUB-PR-{today}",
        "priority": "P2",
        "title": f"向{min(2,len(gh))}个GitHub awesome AI仓库提PR请求收录aitoolcrux.com",
        "description": "找README中列出AI工具评测站的仓库，提PR添加aitoolcrux",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })
if quora:
    todos.append({
        "id": f"GROWTH-QUORA-{today}",
        "priority": "P2",
        "title": f"Quora回答{min(2,len(quora))}个AI工具推荐问题",
        "description": "以真实评测视角回答，引用aitoolcrux.com",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第三轮",
    "time": now_str,
    "result": f"Serper 6组新角度搜索: GitHub{len(gh)}+垂直{len(vert)}+Quora{len(quora)}+Toolify{len(toolify)}",
})
state["last_updated"] = now_str

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"state.json: +{len(todos)} todos")

# 日志
log = f"""

---

## 外链调研第三轮（{now_str}）

**工具**: Serper API
**角度**: GitHub awesome + 垂直目录 + Quora + 竞品Toolify

### 结果
- GitHub awesome列表: {len(gh)}条（高价值，PR=免费dofollow外链）
- 垂直AI目录: {len(vert)}条
- Quora问答: {len(quora)}条（回答带链接）
- Product Hunt二级: {len(all_results.get('Product Hunt二级',[]))}条
- 竞品Toolify: {len(toolify)}条

### 已补录待办: {len(todos)}个
"""
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log)
print("Log written. Done.")
