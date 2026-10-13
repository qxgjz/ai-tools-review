#!/usr/bin/env python3
"""拓荒者-外链跟进 v2: 验证backlink + 检查新提交状态"""
import urllib.request, urllib.error, json, os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
OPPORTUNITIES = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

PROXY = "http://127.0.0.1:7890"
proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
opener = urllib.request.build_opener(proxy_handler)

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AIToolCruX"})
        with opener.open(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return -1, str(e)[:80]

# === 1. 验证已知4个backlink ===
known_links = [
    ("ai-saas.org", "https://ai-saas.org/projects/aitoolcrux"),
    ("productcool", "https://www.productcool.com/product/aitoolcrux-ai-tool-reviews"),
    ("sideprojectors.com", "https://www.sideprojectors.com/project/95323"),
    ("thehackstack.com", "https://thehackstack.com/product/de31942a-cd6d-4dfe-bf71-456535853b8f"),
]

print("=== 1. Verifying known backlinks ===")
results = []
for name, url in known_links:
    code, html = fetch(url)
    has_link = "aitoolcrux.com" in html.lower() if code == 200 else False
    status = "LINK-ALIVE" if (code == 200 and has_link) else ("PAGE-OK-NO-LINK" if code == 200 else f"HTTP-{code}")
    print(f"  {name:25s} | HTTP {code:3d} | {status}")
    results.append({"name": name, "url": url, "code": code, "status": status})

# === 2. 检查今天新提交的aitoolsdirectory.com ===
print("\n=== 2. Checking aitoolsdirectory.com (new submission) ===")
# 直接搜有没有aitoolcrux页面
code, html = fetch("https://aitoolsdirectory.com/?s=aitoolcrux")
found = "aitoolcrux" in html.lower() if code == 200 else False
print(f"  Search page: HTTP {code}, found='aitoolcrux': {found}")
# 也试直接URL
code2, html2 = fetch("https://aitoolsdirectory.com/tool/aitoolcrux")
found2 = "aitoolcrux" in html2.lower() if code2 == 200 else False
print(f"  Direct URL: HTTP {code2}, found: {found2}")

# === 3. 检查其他无提及目录站是否有新变化 ===
print("\n=== 3. Re-checking pending directories ===")
pending = [
    ("dang.ai", "https://dang.ai"),
    ("insidr.ai", "https://www.insidr.ai"),
    ("hatchr.in", "https://hatchr.in/post/6aad2a8e33511e5661ce5e2d"),
    ("fivetaco.com", "https://fivetaco.com"),
    ("anyfp.com", "https://anyfp.com"),
    ("agenthunter.io", "https://www.agenthunter.io"),
]
pending_results = []
for name, url in pending:
    code, html = fetch(url)
    has = "aitoolcrux" in html.lower() if code == 200 else False
    status = "MENTION-FOUND" if has else "NO-MENTION"
    print(f"  {name:20s} | HTTP {code:3d} | {status}")
    pending_results.append({"name": name, "code": code, "status": status, "has_mention": has})

# === 4. 更新backlink_opportunities.md ===
md = f"""

---

## Backlink状态跟进（{now_str}）

### 已知backlink验证（4个）
| 目录站 | HTTP | 状态 |
|--------|------|------|
"""
for r in results:
    md += f"| {r['name']} | {r['code']} | {r['status']} |\n"

md += f"""
### 新提交检查（aitoolsdirectory.com）
- 提交时间: 2026-10-10 06:12 JST
- 当前状态: {"已上线" if found or found2 else "仍在审核中"}
- 搜索页找到aitoolcrux: {found}
- 直接URL找到: {found2}

### 待审核目录站复查（6个）
| 目录站 | HTTP | 状态 |
|--------|------|------|
"""
for r in pending_results:
    md += f"| {r['name']} | {r['code']} | {r['status']} |\n"

alive_count = sum(1 for r in results if r["status"] == "LINK-ALIVE")
md += f"""
### 统计
- 存活backlink: {alive_count}/4
- 新提交aitoolsdirectory: {"已上线" if found or found2 else "审核中"}
- 待审核站仍无提及: {sum(1 for r in pending_results if not r['has_mention'])}/6
"""

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)
print(f"\nbacklink_opportunities.md updated")

# === 5. 更新state.json ===
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

state["completed_tasks"].append({
    "task": "拓荒者-外链跟进（12点档）",
    "time": now_str,
    "result": f"验证{len(results)}个已知backlink: {alive_count}存活; aitoolsdirectory={'上线' if found or found2 else '审核中'}; 复查{len(pending_results)}个待审站",
    "alive_links": [r["name"] for r in results if r["status"] == "LINK-ALIVE"],
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("state.json updated")

# === 6. 写日志 ===
log = f"""

---

## 外链跟进执行（{now_str}）

**工具**: Python + 代理 127.0.0.1:7890

### 已知backlink
- 存活: {alive_count}/4
- 全部存活: {[r['name'] for r in results if r['status']=='LINK-ALIVE']}

### 新提交aitoolsdirectory.com
- 状态: {"✅ 已上线" if found or found2 else "⏳ 审核中（提交后约6小时）"}

### 待审核站复查
- 6个站仍无aitoolcrux提及（可能项目页URL不对或审核中）
"""
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log)
print("Log written. Done.")
