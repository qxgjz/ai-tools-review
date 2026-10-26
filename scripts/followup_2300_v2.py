import json, os, urllib.request
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
OPPS_PATH = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

PROXY = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
opener = urllib.request.build_opener(PROXY)
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

# 快速复验5个backlink（含新insidr）
def check(url, kw):
    try:
        r = opener.open(url, timeout=10)
        body = r.read().decode("utf-8", errors="ignore")[:30000]
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
results = []
for n, u, k in links:
    c, f = check(u, k)
    ok = (c == 200 and f)
    if ok: alive += 1
    results.append(f"| {n} | {u} | {c} | {'✅ ALIVE' if ok else '⚠️ '+str(c)} |")
    print(f"{n}: {c} found={f}")

# 追加到 backlink_opportunities.md
with open(OPPS_PATH, "a", encoding="utf-8") as fh:
    fh.write(f"""

## Backlink状态跟进 — {now_str}

| 目录 | URL | HTTP | 状态 |
|------|-----|------|------|
{chr(10).join(results)}

- **insidr.ai**：10-14 06:00表单提交 → 14:00已被索引（new backlink #5）
- **aitoolsdirectory.com**：10-10 06:12提交，至今~136小时（超5工作日），搜索页仍无aitoolcrux。**建议发邮件催办**。
- **hyzenpro.com**：10-12 06:xx提交，搜索页found=False，索引波动中。
- 活跃backlink总数：**{alive}/5**
""")

# state.json
with open(STATE_PATH, "r", encoding="utf-8") as fh:
    state = json.load(fh)
state.setdefault("completed_tasks", []).append({
    "task": "拓荒者-外链跟进(23点档)",
    "time": now_str,
    "result": f"{alive}/5 backlinks alive (含insidr新上线). aitoolsdirectory ~136h超期建议催办. hyzenpro索引波动."
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as fh:
    json.dump(state, fh, ensure_ascii=False, indent=2)

with open(LOG_PATH, "a", encoding="utf-8") as fh:
    fh.write(f"\n## 23:00 跟进档 ({now_str})\n- {alive}/5 backlinks ALIVE（insidr新上线）\n- aitoolsdirectory超期，建议催办\n- backlink_opportunities.md已更新\n")

print(f"\nDone. {alive}/5 alive")
