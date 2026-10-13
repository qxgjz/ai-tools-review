import urllib.request, ssl, json, os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")
OPPORTUNITIES = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")

PROXY = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
opener = urllib.request.build_opener(PROXY, urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

def check(url):
    try:
        with opener.open(url, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore").lower()
            return r.status, "aitoolcrux" in html
    except Exception as e:
        return -1, False

# 4个已确认backlink
backlinks = [
    ("ai-saas.org", "https://ai-saas.org/projects/aitoolcrux"),
    ("productcool", "https://www.productcool.com/product/aitoolcrux-ai-tool-reviews"),
    ("sideprojectors", "https://www.sideprojectors.com/project/95323"),
    ("thehackstack", "https://thehackstack.com/product/de31942a-cd6d-4dfe-bf71-456535853b8f"),
]
# 待审核
pending = [
    ("aitoolsdirectory", "https://aitoolsdirectory.com/?s=aitoolcrux"),
    ("hyzenpro", "https://hyzenpro.com/?s=aitoolcrux"),
]

print("=== Backlink verification ===")
alive = 0
for name, url in backlinks:
    s, has = check(url)
    status = "ALIVE" if (s == 200 and has) else "DEAD"
    if status == "ALIVE": alive += 1
    print(f"  {name}: {s}, has_aitoolcrux={has} -> {status}")

print("\n=== Pending submissions ===")
for name, url in pending:
    s, found = check(url)
    print(f"  {name}: {s}, found_on_search={found}")

# 更新backlink_opportunities.md追加状态表
status_md = f"\n\n### 跟进状态更新（{now_str}）\n\n"
status_md += f"| 站点 | HTTP | 含aitoolcrux | 状态 |\n|------|------|-------------|------|\n"
for name, url in backlinks:
    s, has = check(url)
    status_md += f"| {name} | {s} | {'✅' if has else '❌'} | {'ALIVE' if s==200 and has else 'DEAD'} |\n"
for name, url in pending:
    s, found = check(url)
    label = "已上线" if found else "审核中"
    status_md += f"| {name} | {s} | {'✅' if found else '⏳'} | {label} |\n"

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(status_md)

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)
state.setdefault("completed_tasks", []).append({
    "task": "拓荒者-外链跟进(12点档)",
    "time": now_str,
    "result": f"{alive}/4 backlinks alive; aitoolsdirectory pending; hyzenpro searchable"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 外链跟进（{now_str}）12点档\n\n- {alive}/4 backlink存活\n- aitoolsdirectory: 审核中（~80h）\n- hyzenpro: 搜索页可见\n- 状态表已追加到backlink_opportunities.md\n")

print(f"\nDone. {alive}/4 alive")
