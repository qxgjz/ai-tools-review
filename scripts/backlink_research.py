#!/usr/bin/env python3
"""拓荒者-外链调研: 用Serper API搜索外链机会"""
import requests
import json
import os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
SERPER_URL = "https://google.serper.dev/search"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
OUTPUT_PATH = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_DIR = os.path.join(PROJECT, "window_logs")
LOG_PATH = os.path.join(LOG_DIR, f"growth_{datetime.now(JST).strftime('%Y-%m-%d')}.md")

def serper_search(q, num=15):
    """用Serper API搜索"""
    try:
        r = requests.post(SERPER_URL, headers=HEADERS, json={"q": q, "num": num}, timeout=20)
        data = r.json()
        return data.get("organic", [])
    except Exception as e:
        print(f"  [ERROR] search '{q[:50]}...': {e}")
        return []

# === 搜索4类机会 ===
searches = [
    ("客座博客机会", "AI tools write for us guest post contribute 2026"),
    ("资源页/榜单页", "best AI tools list 2026 top recommendations"),
    ("新目录站", "submit AI tool directory free submission 2026"),
    ("Reddit品牌提及", 'site:reddit.com "AI tool" recommendation 2026'),
]

all_results = {}
for label, query in searches:
    print(f"\n=== Searching: {label} ===")
    print(f"  Query: {query}")
    results = serper_search(query, num=15)
    all_results[label] = results
    for i, r in enumerate(results[:10]):
        print(f"  {i+1}. {r.get('title','')[:70]}")
        print(f"     {r.get('link','')[:80]}")
        print(f"     {r.get('snippet','')[:100]}")

# === 生成backlink_opportunities.md ===
md = f"""# Backlink Opportunities（外链机会清单）

> 生成时间: {now}
> 工具: Serper API (现成工具，无重复造轮子)
> 目的: 找到可获取外链的目录站、资源页、客座博客、社区讨论

---

## 一、客座博客机会（Write for Us / Guest Post）

| # | 网站 | URL | 为什么有价值 | 行动 |
|---|------|-----|-------------|------|
"""

guest_results = all_results.get("客座博客机会", [])
for i, r in enumerate(guest_results[:8], 1):
    md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | {r.get('snippet','')[:60]} | 待评估 |\n"

md += f"""
---

## 二、资源页/榜单页（Best AI Tools Lists）

> 在这些页面被收录 = 高相关dofollow外链

| # | 页面 | URL | 类型 | 行动 |
|---|------|-----|------|------|
"""

list_results = all_results.get("资源页/榜单页", [])
for i, r in enumerate(list_results[:10], 1):
    md += f"| {i} | {r.get('title','')[:50]} | {r.get('link','')[:60]} | 榜单/资源页 | 待评估 |\n"

md += f"""
---

## 三、新目录站（未提交过的）

> 对比accounts.md已有14个目录，这些是新发现的

| # | 目录站 | URL | 备注 | 行动 |
|---|--------|-----|------|------|
"""

dir_results = all_results.get("新目录站", [])
existing_dirs = ["ai-saas.org", "productcool.com", "dang.ai", "insidr.ai", "aixploria.com",
                 "bestaibrands.com", "hatchr.in", "sideprojectors.com", "thehackstack.com",
                 "fivetaco.com", "anyfp.com", "agenthunter.io", "aitoolfind.com"]
new_count = 0
for r in dir_results:
    url = r.get("link", "")
    # 跳过已有的
    if any(d in url for d in existing_dirs):
        continue
    new_count += 1
    md += f"| {new_count} | {r.get('title','')[:50]} | {url[:60]} | {r.get('snippet','')[:50]} | 待提交 |\n"
    if new_count >= 10:
        break

md += f"""
---

## 四、Reddit品牌提及机会（可回复的讨论帖）

> 这些帖子讨论AI工具推荐，我们可以以真实用户身份参与

| # | 帖子 | URL | 子版 | 回复角度 |
|---|------|-----|------|---------|
"""

reddit_results = all_results.get("Reddit品牌提及", [])
for i, r in enumerate(reddit_results[:8], 1):
    url = r.get("link", "")
    sub = ""
    if "reddit.com/r/" in url:
        parts = url.split("reddit.com/r/")
        if len(parts) > 1:
            sub = "/r/" + parts[1].split("/")[0]
    md += f"| {i} | {r.get('title','')[:50]} | {url[:60]} | {sub} | 真实评测视角 |\n"

md += f"""
---

## 五、优先级行动清单

### 立即做（P0）
1. 从上面「新目录站」中选3-5个DR>40的提交
2. 从「Reddit品牌提及」中选2-3个帖子，登录后回复（不硬广）

### 本周做（P1）
3. 从「客座博客机会」中选2-3个高质量博客投稿
4. 从「资源页/榜单页」中找联系邮箱，发收录请求

### 长期做（P2）
5. Broken link building: 扫描竞品(toolify.ai/futurepedia.io)的死链
6. 监控品牌提及（未链接的→请求加链接）

---

## 六、数据统计

- 客座博客搜索结果: {len(guest_results)}条
- 资源页/榜单搜索结果: {len(list_results)}条
- 新目录站搜索结果: {new_count}个新（未在已有清单中）
- Reddit讨论帖: {len(reddit_results)}条
"""

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(md)
print(f"\n=== Output written to: {OUTPUT_PATH} ===")
print(f"=== File size: {os.path.getsize(OUTPUT_PATH)} bytes ===")

# === 更新state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

# 补录待办
new_todos = [
    {
        "id": "GROWTH-DIR-NEW-001",
        "priority": "P1",
        "title": "从新目录站清单提交3-5个高质量目录",
        "description": "见backlink_opportunities.md第三节，选DR>40的提交",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now
    },
    {
        "id": "GROWTH-REDDIT-REPLY-002",
        "priority": "P1",
        "title": "Reddit品牌提及帖回复2-3个",
        "description": "见backlink_opportunities.md第四节，登录后以真实用户身份回复",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now
    },
    {
        "id": "GROWTH-GUEST-001",
        "priority": "P2",
        "title": "客座博客投稿2-3篇",
        "description": "见backlink_opportunities.md第一节，选高质量AI博客投稿",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now
    }
]
state["next_iteration_focus"].extend(new_todos)

# 记录本轮完成
new_task = {
    "task": "拓荒者-外链调研（现成工具版）",
    "time": now,
    "result": f"Serper API搜索完成: {len(guest_results)}客座博客, {len(list_results)}资源页, {new_count}新目录站, {len(reddit_results)} Reddit帖",
    "output_file": OUTPUT_PATH,
    "todos_added": 3
}
state["completed_tasks"].append(new_task)
state["last_updated"] = now

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("state.json updated with 3 new todos")

# === 写日志 ===
log_addition = f"""

---

## 外链调研执行（{now}）

**工具**: Serper API（现成工具，未重复造轮子）

### 搜索结果
- 客座博客机会: {len(guest_results)}条结果
- 资源页/榜单: {len(list_results)}条结果
- 新目录站: {new_count}个（未在已有14个目录中）
- Reddit品牌提及帖: {len(reddit_results)}条

### 输出文件
- `iteration_center/backlink_opportunities.md`（新建）

### 补录待办（3个，assigned_to=拓荒者）
1. GROWTH-DIR-NEW-001: 提交3-5个新目录站
2. GROWTH-REDDIT-REPLY-002: Reddit回复2-3个品牌提及帖
3. GROWTH-GUEST-001: 客座博客投稿2-3篇
"""
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log_addition)
print("Log updated")
print("Done.")
