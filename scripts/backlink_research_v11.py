import urllib.request, json, os, ssl, time
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
OPPORTUNITIES = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
PROXY = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
opener = urllib.request.build_opener(PROXY, urllib.request.HTTPSHandler(context=ctx))

def serper(q, num=10):
    data = json.dumps({"q": q, "num": num, "gl": "us", "hl": "en"}).encode()
    req = urllib.request.Request("https://google.serper.dev/search", data=data,
        headers={"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"})
    try:
        with opener.open(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  ERR {q[:40]}: {e}")
        return {"organic": []}

queries = [
    ("R11A", "best AI tools 2026 list site:producthunt.com OR site:beta-list.com", "PH/BetaList近期launch"),
    ("R11B", "AI tool review write for us submit your review", "AI评测博客投稿"),
    ("R11C", "chrome extension AI tool review submit", "Chrome商店提交"),
    ("R11D", "linkedin pulse AI tools article submit contribute", "LinkedIn投稿"),
    ("R11E", "AI tool directory add your site free no backlink required", "零成本新目录"),
]

results_md = f"\n\n---\n\n## 第11轮外链调研（{now_str}）\n\n"
new_opps = []
for tag, q, label in queries:
    print(f"[{tag}] {q}")
    r = serper(q)
    orgs = r.get("organic", [])[:8]
    results_md += f"\n### {tag}: {label}\n"
    results_md += f"**Query**: `{q}`\n\n"
    for i, o in enumerate(orgs[:6], 1):
        t = o.get("title","")[:80]
        u = o.get("link","")
        sn = o.get("snippet","")[:120]
        results_md += f"{i}. [{t}]({u}) — {sn}\n"
        if any(k in (u+t+sn).lower() for k in ["submit","add your","list your","write for us","contribute","review","directory"]):
            new_opps.append((label, t, u))
    time.sleep(1)

seen = set()
uniq = []
for l, t, u in new_opps:
    if u not in seen:
        seen.add(u); uniq.append((l, t, u))

results_md += f"\n\n### 本轮新发现可操作机会（{len(uniq)}个）\n\n"
for i, (l, t, u) in enumerate(uniq[:10], 1):
    results_md += f"{i}. [{t[:60]}]({u}) — {l}\n"

with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(results_md)

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)
todo = state.setdefault("next_iteration_focus", [])
for l, t, u in uniq[:5]:
    todo.append({
        "task": f"外链机会: {t[:60]}",
        "url": u,
        "assigned_to": ["window2", "拓荒者"],
        "priority": "P1",
        "source": f"r11_backlink_research_{today}",
        "category": l
    })
state["last_updated"] = now_str
state.setdefault("completed_tasks", []).append({
    "task": "拓荒者-外链调研(10点档R11)",
    "time": now_str,
    "result": f"5 queries, {len(uniq)} new opps found"
})
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 第11轮外链调研（{now_str}）\n\n- 5个Serper查询\n- 新发现{len(uniq)}个可操作机会\n- 已写入backlink_opportunities.md和state.json\n")

print(f"\nDone. {len(uniq)} new opps")
