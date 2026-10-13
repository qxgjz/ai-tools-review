#!/usr/bin/env python3
"""拓荒者-外链跟进: 用代理验证14个目录站backlink状态"""
import urllib.request, urllib.error, json, os, re
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
OPPORTUNITIES = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

# 代理
PROXY = "http://127.0.0.1:7890"
proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(proxy_handler)

def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AIToolCruX growth",
            "Accept": "text/html"
        })
        with opener.open(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return -1, str(e)[:100]

# === 14个目录站验证清单 ===
dirs = [
    ("ai-saas.org", "https://ai-saas.org/projects/aitoolcrux", "project page (known dofollow)"),
    ("productcool", "https://www.productcool.com/product/aitoolcrux-ai-tool-reviews", "product page (known link)"),
    ("dang.ai", "https://dang.ai", "homepage (need project page)"),
    ("insidr.ai", "https://www.insidr.ai", "homepage"),
    ("aixploria.com", "https://www.aixploria.com", "homepage"),
    ("bestaibrands.com", "https://bestaibrands.com", "homepage"),
    ("hatchr.in", "https://hatchr.in/post/6aad2a8e33511e5661ce5e2d", "post page"),
    ("sideprojectors.com", "https://www.sideprojectors.com/project/95323", "project page"),
    ("thehackstack.com", "https://thehackstack.com/product/de31942a-cd6d-4dfe-bf71-456535853b8f", "product page"),
    ("fivetaco.com", "https://fivetaco.com", "homepage"),
    ("anyfp.com", "https://anyfp.com", "homepage"),
    ("agenthunter.io", "https://www.agenthunter.io", "homepage"),
    ("aitoolfind.com", "https://aitoolfind.com", "homepage"),
    ("aixploria_search", "https://www.aixploria.com/search?q=aitoolcrux", "search page"),
]

print("=== Verifying backlinks via proxy ===\n")
results = []
for name, url, note in dirs:
    code, html = fetch(url)
    has_aitoolcrux = "aitoolcrux" in html.lower() if code == 200 else False
    has_link = "aitoolcrux.com" in html.lower() if code == 200 else False
    
    if code == 200 and has_link:
        status = "LINK-FOUND"
    elif code == 200 and has_aitoolcrux:
        status = "MENTION-BUT-NO-LINK"
    elif code == 200:
        status = "PAGE-OK-NO-MENTION"
    elif code == 403:
        status = "BLOCKED-403"
    elif code == 404:
        status = "NOT-FOUND-404"
    elif code == -1:
        status = f"CONN-FAILED"
    else:
        status = f"HTTP-{code}"
    
    print(f"  {name:25s} | HTTP {code:3d} | {status:25s} | {url[:60]}")
    results.append({
        "name": name, "url": url, "code": code, "status": status,
        "has_mention": has_aitoolcrux, "has_link": has_link, "note": note
    })

# 统计
link_found = [r for r in results if r["status"] == "LINK-FOUND"]
no_mention = [r for r in results if r["status"] == "PAGE-OK-NO-MENTION"]
blocked = [r for r in results if "BLOCKED" in r["status"] or "FAILED" in r["status"]]
print(f"\n=== Summary: {len(link_found)} links found, {len(no_mention)} pages OK no mention, {len(blocked)} blocked/failed ===")

# === 更新backlink_opportunities.md ===
status_md = f"""

---

## Backlink 状态跟进（{now_str}）

> 验证方式: Python urllib + 代理 127.0.0.1:7890
> 验证了 {len(results)} 个已提交目录站

| # | 目录站 | 验证URL | HTTP | 状态 | 说明 |
|---|--------|---------|------|------|------|
"""
for i, r in enumerate(results, 1):
    status_md += f"| {i} | {r['name']} | {r['url'][:50]} | {r['code']} | {r['status']} | {r['note']} |\n"

status_md += f"""
### 统计
- ✅ LINK-FOUND（有实际指向aitoolcrux.com的链接）: {len(link_found)}个
- ⚠️ PAGE-OK-NO-MENTION（页面正常但无aitoolcrux提及，可能审核中或项目页URL不对）: {len(no_mention)}个
- ❌ BLOCKED/FAILED（403/连接失败）: {len(blocked)}个

### 行动建议
"""
if link_found:
    status_md += "**已获外链的目录站**: " + ", ".join(r["name"] for r in link_found) + "\n"
if no_mention:
    status_md += "**需登录后台查审核状态的目录站**: " + ", ".join(r["name"] for r in no_mention) + "\n"
if blocked:
    status_md += "**需手动检查的目录站（403/连接失败）**: " + ", ".join(r["name"] for r in blocked) + "\n"

# 追加到opportunities文件
with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(status_md)
print(f"\nbacklink_opportunities.md updated")

# === 更新state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

state["completed_tasks"].append({
    "task": "拓荒者-外链跟进（现成工具版）",
    "time": now_str,
    "result": f"验证{len(results)}个目录站: {len(link_found)}个有链接, {len(no_mention)}个无提及, {len(blocked)}个被墙/失败",
    "link_found": [r["name"] for r in link_found],
    "need_login_check": [r["name"] for r in no_mention],
    "blocked": [r["name"] for r in blocked],
})

# 补录待办：登录后台查审核状态
if no_mention:
    state["next_iteration_focus"].append({
        "id": f"GROWTH-DIR-REVIEW-{today}",
        "priority": "P1",
        "title": f"登录{len(no_mention)}个目录站后台查审核状态: {', '.join(r['name'] for r in no_mention[:5])}",
        "description": "这些目录站首页正常但找不到aitoolcrux提及，可能项目页URL不对或审核中。需登录后台确认提交状态",
        "assigned_to": "拓荒者",
        "status": "pending",
        "created": now_str
    })

state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("state.json updated")

# === 写日志 ===
log_add = f"""

---

## 外链跟进执行（{now_str}）

**工具**: Python urllib + 代理 127.0.0.1:7890

### 验证结果
- 验证目录站: {len(results)}个
- ✅ 有实际链接: {len(link_found)}个 ({', '.join(r['name'] for r in link_found)})
- ⚠️ 页面正常无提及: {len(no_mention)}个 ({', '.join(r['name'] for r in no_mention)})
- ❌ 被墙/连接失败: {len(blocked)}个 ({', '.join(r['name'] for r in blocked)})

### 补录待办
- GROWTH-DIR-REVIEW-{today}: 登录后台查审核状态
"""
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log_add)
print("Log written")
print(f"\nDone. {now_str}")
