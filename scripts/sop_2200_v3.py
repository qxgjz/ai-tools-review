import json, os, urllib.request
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

PROXY = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
opener = urllib.request.build_opener(PROXY)
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

def check(url, kw):
    try:
        r = opener.open(url, timeout=12)
        body = r.read().decode("utf-8", errors="ignore")
        return r.getcode(), kw.lower() in body.lower()
    except Exception as e:
        return str(e)[:40], None

links = [
    ("ai-saas", "https://ai-saas.org/projects/aitoolcrux", "aitoolcrux"),
    ("productcool", "https://www.productcool.com/product/aitoolcrux-ai-tool-reviews", "aitoolcrux"),
    ("sideprojectors", "https://www.sideprojectors.com/project/95323", "aitoolcrux"),
    ("hackstack", "https://thehackstack.com/product/de31942a-cd6d-4dfe-bf71-456535853b8f", "aitoolcrux"),
    ("insidr", "https://insidr.ai/?s=aitoolcrux", "aitoolcrux"),
]
alive = 0
for n, u, k in links:
    c, f = check(u, k)
    ok = (c == 200 and f)
    if ok: alive += 1
    print(f"  {n}: {c}, found={f} -> {'ALIVE' if ok else 'ISSUE'}")

# pending
c1, f1 = check("https://aitoolsdirectory.com/?s=aitoolcrux", "aitoolcrux")
c2, f2 = check("https://hyzenpro.com/?s=aitoolcrux", "aitoolcrux")
print(f"  aitoolsdirectory: {c1}, found={f1}")
print(f"  hyzenpro: {c2}, found={f2}")

with open(STATE_PATH, "r", encoding="utf-8") as fh:
    state = json.load(fh)
state.setdefault("completed_tasks", []).append({
    "task": "拓荒者-外链增长SOP(22点档)",
    "time": now_str,
    "result": f"{alive}/5 backlinks alive; HN NOT-LOGGED-IN; Reddit NOT-LOGGED-IN; aitoolsdirectory found={f1}; hyzenpro found={f2}"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as fh:
    json.dump(state, fh, ensure_ascii=False, indent=2)

with open(LOG_PATH, "a", encoding="utf-8") as fh:
    fh.write(f"\n## 22:00 SOP档 ({now_str})\n- Backlinks: {alive}/5 ALIVE\n- HN/Reddit: NOT-LOGGED-IN\n- aitoolsdirectory: {'已上线' if f1 else '仍pending'}\n- hyzenpro: {'已上线' if f2 else '仍pending'}\n")

print(f"\nDone. {alive}/5 alive")
