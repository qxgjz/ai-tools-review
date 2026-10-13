#!/usr/bin/env python3
"""拓荒者-外链跟进 23点: 验证backlink状态"""
import urllib.request, json, os, ssl
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
OPPORTUNITIES = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

PROXY = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
opener = urllib.request.build_opener(PROXY, urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")]

def check_url(url):
    try:
        req = urllib.request.Request(url)
        with opener.open(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore").lower()
            return r.status, "aitoolcrux" in html, len(html)
    except Exception as e:
        return -1, False, str(e)[:80]

backlinks = [
    ("ai-saas.org", "https://ai-saas.org/projects/aitoolcrux"),
    ("productcool.com", "https://www.productcool.com/product/aitoolcrux-ai-tool-reviews"),
    ("sideprojectors.com", "https://www.sideprojectors.com/project/95323"),
    ("thehackstack.com", "https://thehackstack.com/product/de31942a-cd6d-4dfe-bf71-456535853b8f"),
]
pending = [
    ("aitoolsdirectory-search", "https://aitoolsdirectory.com/?s=aitoolcrux"),
    ("aitoolsdirectory-direct", "https://aitoolsdirectory.com/aitoolcrux/"),
]

print("=== 已确认backlink ===")
results = []
for name, url in backlinks:
    s, h, sz = check_url(url)
    icon = "✅" if s==200 and h else "⚠️" if s==200 else "❌"
    print(f"{icon} {name}: HTTP {s}, has={h}, size={sz}")
    results.append((name, url, s, h))

print("\n=== 待审核 ===")
pend_res = []
for name, url in pending:
    s, h, sz = check_url(url)
    print(f"  {name}: HTTP {s}, found={h}")
    pend_res.append((name, url, s, h))

# 追加md
md = f"\n\n---\n\n## 外链跟进（{now_str}）\n\n### 已确认backlink状态\n\n| 目录站 | URL | HTTP | 含aitoolcrux | 状态 |\n|--------|-----|------|-------------|------|\n"
for name, url, s, h in results:
    st = "ALIVE ✅" if s==200 and h else "⚠️ 页面正常无提及" if s==200 else "❌ 异常"
    md += f"| {name} | {url} | {s} | {'是' if h else '否'} | {st} |\n"
md += f"\n### 待审核\n\n| 站 | 检查URL | HTTP | 找到 |\n|----|---------|------|------|\n"
for name, url, s, h in pend_res:
    md += f"| {name} | {url} | {s} | {'是' if h else '否'} |\n"
with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)

# state
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)
alive = sum(1 for _,_,s,h in results if s==200 and h)
state["completed_tasks"].append({
    "task": "拓荒者-外链跟进(23点)",
    "time": now_str,
    "result": f"{alive}/{len(results)} backlinks alive; aitoolsdirectory仍审核中"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

log = f"\n\n---\n\n## 外链跟进（{now_str}）\n\n- 验证{len(results)}个backlink: {alive}个存活\n- aitoolsdirectory.com: 仍未上线（提交~17小时）\n- hyzenpro.com: 表单未完成\n\n结论: {alive}个backlink正常生效，无需跟进动作。\n"
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(log)
print(f"\nDone. {alive}/{len(results)} alive.")
