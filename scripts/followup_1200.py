#!/usr/bin/env python3
"""10-11 12点档外链跟进"""
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
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

def check(url):
    try:
        req = urllib.request.Request(url)
        with opener.open(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore").lower()
            return r.status, "aitoolcrux" in html
    except Exception as e:
        return -1, False

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

print("=== backlinks ===")
results = []
for name, url in backlinks:
    s, h = check(url)
    icon = "✅" if s==200 and h else "⚠️" if s==200 else "❌"
    print(f"{icon} {name}: {s}, has={h}")
    results.append((name, url, s, h))

print("\n=== pending ===")
pend = []
for name, url in pending:
    s, h = check(url)
    print(f"  {name}: {s}, found={h}")
    pend.append((name, url, s, h))

alive = sum(1 for _,_,s,h in results if s==200 and h)
aitools_up = any(h for _,_,_,h in pend)

md = f"\n\n---\n\n## 外链跟进（{now_str}）\n\n| 站 | HTTP | 含aitoolcrux | 状态 |\n|----|------|-------------|------|\n"
for name, url, s, h in results:
    st = "ALIVE ✅" if s==200 and h else "⚠️" if s==200 else "❌"
    md += f"| {name} | {s} | {'是' if h else '否'} | {st} |\n"
md += f"\n**aitoolsdirectory.com**: {'✅ 已上线' if aitools_up else '仍在审核中（~30小时）'}\n"
with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(md)

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)
state["completed_tasks"].append({
    "task": "拓荒者-外链跟进(12点)",
    "time": now_str,
    "result": f"{alive}/4 backlinks alive; aitoolsdirectory={'上线' if aitools_up else '仍审核'}"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 外链跟进（{now_str}）\n\n- {alive}/4 backlinks存活\n- aitoolsdirectory: {'✅上线' if aitools_up else '仍审核中(~30h)'}\n")
print(f"\nDone. {alive}/4 alive, aitoolsdirectory={'up' if aitools_up else 'pending'}")
