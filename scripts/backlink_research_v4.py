#!/usr/bin/env python3
"""拓荒者-外链调研 v4: 竞品TAIAF + 评论站 + 社交书签 + 直接submit"""
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
    # 1. 竞品theresanaiforthat外链来源
    ("竞品TAIAF", 'site:theresanaiforthat.com OR "theresanaiforthat" directory OR list OR review'),
    # 2. AI工具评论/评价站（除G2/Capterra外）
    ("AI评论站", 'AI tool review site submit OR "rate AI tool" OR "review AI tool" platform 2026'),
    # 3. 社交书签站（Reddit已搜过，找其他）
    ("社交书签", 'AI tool submission site:news.ycombinator.com OR site:lobste.rs OR site:dev.to OR site:medium.com'),
    # 4. 直接搜索免费submit目录（还没被发现的）
    ("免费submit目录", '"submit your AI tool" free listing -paid -sponsored 2026'),
    # 5. AI工具导航站/聚合站
    ("聚合导航站", 'AI tools aggregator OR "AI tools index" OR "AI tools catalog" submit'),
    # 6. 客座博客（具体SEO/增长方向）
    ("SEO增长客座", '"write for us" SEO OR growth OR SaaS 2026 AI'),
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

# === 输出 ===
md = f"""

---

## 外链调研第四轮（{now_str}）

> 工具: Serper API
> 角度: 竞品TAIAF + 评论站 + 社交书签 + 免费submit目录 + 聚合导航站

### 一、竞品theresanaiforthat外链线索

"""
taiaf = all_results.get("竞品TAIAF", [])
if taiaf:
    md += "| # | 结果 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(taiaf[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 二、AI工具评论/评价站

"""
reviews = all_results.get("AI评论站", [])
if reviews:
    md += "| # | 平台 | URL | 类型 |\n|---|------|-----|------|\n"
    for i, r in enumerate(reviews[:6], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | {r.get('snippet','')[:40]} |\n"

md += f"""
### 三、免费submit目录（未被前三轮覆盖的）

"""
free_dirs = all_results.get("免费submit目录", [])
if free_dirs:
    md += "| # | 目录站 | URL | 备注 |\n|---|--------|-----|------|\n"
    for i, r in enumerate(free_dirs[:8], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | {r.get('snippet','')[:50]} |\n"

md += f"""
### 四、AI聚合导航站

"""
agg = all_results.get("聚合导航站", [])
if agg:
    md += "| # | 站 | URL |\n|---|------|-----|\n"
    for i, r in enumerate(agg[:5], 1):
        md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} |\n"

md += f"""
### 五、本轮统计
- 竞品TAIAF: {len(taiaf)}条
- AI评论站: {len(reviews)}条
- 免费submit目录: {len(free_dirs)}条
- 社交书签: {len(all_results.get('社交书签',[]))}条
- 聚合导航站: {len(agg)}条
- SEO客座: {len(all_results.get('SEO增长客座',[]))}条
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print(f"\nbacklink_opportunities.md updated")

# === state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = []
if free_dirs:
    todos.append({
        "id": f"GROWTH-DIR-V4-{today}",
        "priority": "P1",
        "title": f"提交{min(2,len(free_dirs))}个第四轮新发现的免费目录站",
        "description": "筛选免费、即时审核的目录站提交",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["next_iteration_focus"].extend(todos)
state["completed_tasks"].append({
    "task": "拓荒者-外链调研第四轮",
    "time": now_str,
    "result": f"Serper 6组新角度: TAIAF{len(taiaf)}+评论站{len(reviews)}+免费目录{len(free_dirs)}+聚合{len(agg)}",
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"state.json: +{len(todos)} todos")

log = f"""

---

## 外链调研第四轮（{now_str}）

**工具**: Serper API
**角度**: 竞品TAIAF + 评论站 + 免费submit目录 + 聚合站

### 结果
- 竞品TAIAF线索: {len(taiaf)}条
- AI评论站: {len(reviews)}条
- 免费submit目录: {len(free_dirs)}条
- 聚合导航站: {len(agg)}条

### 已补录待办: {len(todos)}个
"""
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log)
print("Log written. Done.")
