import json, os, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
OPPS_PATH = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

API_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
SERPER_URL = "https://google.serper.dev/search"

queries = [
    ('R14a', '"best AI tools 2026" intitle:resources -site:futurepedia.io'),
    ('R14b', '"submit AI tool" free directory 2026 -paid'),
    ('R14c', 'AI tools blog "write for us" guest post 2026'),
    ('R14d', 'awesome AI tools list site:github.com 2026'),
    ('R14e', 'AI SaaS link building case study reddit'),
]

all_results = []
for label, q in queries:
    try:
        data = json.dumps({"q": q, "num": 10}).encode()
        req = urllib.request.Request(SERPER_URL, data=data, headers={
            "X-API-KEY": API_KEY, "Content-Type": "application/json"
        })
        r = urllib.request.urlopen(req, timeout=20)
        d = json.loads(r.read())
        orgs = d.get("organic", [])[:8]
        print(f"\n=== {label}: {q} ({len(orgs)} results) ===")
        for o in orgs:
            t = o.get("title","")[:70]
            u = o.get("link","")
            sn = o.get("snippet","")[:100].replace("\n"," ")
            print(f"  - {t}\n    {u}\n    {sn}")
            all_results.append({"label": label, "q": q, "title": t, "url": u, "snippet": sn})
    except Exception as e:
        print(f"{label} ERROR: {e}")

# 挑高价值的写入backlink_opportunities.md
high_value = [r for r in all_results if any(kw in r["url"].lower() or kw in r["title"].lower()
    for kw in ["submit", "write for us", "guest", "awesome", "resource", "directory", "list"])]

with open(OPPS_PATH, "a", encoding="utf-8") as fh:
    fh.write(f"\n\n## R14 外链调研 — {now_str}\n")
    for label, q in queries:
        fh.write(f"\n### {label}: `{q}`\n")
        for r in [x for x in all_results if x["label"] == label]:
            fh.write(f"- [{r['title']}]({r['url']})\n  - {r['snippet']}\n")

# state.json: 写前5个高价值待办
with open(STATE_PATH, "r", encoding="utf-8") as fh:
    state = json.load(fh)

todos = state.setdefault("next_iteration_focus", [])
added = 0
for r in high_value[:5]:
    todos.append({
        "task": f"R14: 评估并行动 {r['title'][:60]} — {r['url']}",
        "assigned_to": "拓荒者", "priority": "P2",
        "source": f"r14_{today}"
    })
    added += 1

state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as fh:
    json.dump(state, fh, ensure_ascii=False, indent=2)

with open(LOG_PATH, "a", encoding="utf-8") as fh:
    fh.write(f"\n## R14调研 ({now_str})\n- 5个查询，{len(all_results)}条结果，{added}条高价值待办入state.json\n")

print(f"\n=== DONE: {len(all_results)} results, {added} todos ===")
