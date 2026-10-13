# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-11"
NOW = datetime.now().isoformat(timespec="seconds")

gsc = json.load(open(os.path.join(BASE, "gsc-ga4-report", "live_pull_20261011_2015.json"), "r", encoding="utf-8"))
daily, pages = gsc["daily"], gsc["top_pages"]

def gd(d): return d["keys"][0]
def gu(p): return p["keys"][0].replace("https://www.aitoolcrux.com", "") or "/"

total_impr = sum(d["impressions"] for d in daily)
total_clk = sum(d["clicks"] for d in daily)
avg_pos = sum(d["position"] * d["impressions"] for d in daily) / max(total_impr, 1)
print(f"[GSC] {gd(daily[0])}~{gd(daily[-1])}: {total_impr} impr, {total_clk} clk, avg pos {avg_pos:.1f}")

ctr = []
for p in pages:
    pos, impr, clk = p["position"], p["impressions"], p["clicks"]
    c = clk / max(impr, 1) * 100
    u = gu(p)
    if 5 <= pos <= 15 and c < 3 and impr >= 10:
        ctr.append({"url": u, "pos": round(pos,1), "impr": impr, "ctr": round(c,2)})
if len(ctr) < 2:
    for p in pages:
        pos, impr, clk = p["position"], p["impressions"], p["clicks"]
        c = clk / max(impr, 1) * 100
        u = gu(p)
        if 5 <= pos <= 20 and c < 3 and impr >= 10 and not any(x["url"] == u for x in ctr):
            ctr.append({"url": u, "pos": round(pos,1), "impr": impr, "ctr": round(c,2), "expanded": True})

print(f"[CTR] {len(ctr)} opps")
for x in ctr:
    print(f"  {x['url']}: pos={x['pos']}, impr={x['impr']}, CTR={x['ctr']}%")

ga4 = json.load(open(os.path.join(BASE, "gsc-ga4-report", "ga4_live_20261011_2015.json"), "r", encoding="utf-8"))
ov = ga4["overview"]
sessions = int(ov["sessions"])
engaged = int(ov["engagedSessions"])
eng_rate = engaged / sessions * 100
print(f"[GA4] {sessions} sess, {eng_rate:.1f}% eng")

with open(os.path.join(BASE, "iteration_center", "audit_findings.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## SOP 21:00 - {NOW}\n\n")
    f.write(f"GSC: {total_impr} impr, {total_clk} clk | GA4: {sessions} sess, {eng_rate:.1f}% eng\n\n")
    f.write(f"CTR opps: {len(ctr)}\n")
    for x in ctr:
        f.write(f"  - {x['url']}: pos={x['pos']}, CTR={x['ctr']}%\n")

state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))
added = 0
for x in ctr:
    existing = [t for t in state["next_iteration_focus"] if t.get("url") == x["url"] and "ctr_optimization" in t.get("source", "")]
    if existing:
        print(f"  [SKIP] {x['url']}")
        continue
    state["next_iteration_focus"].append({
        "id": f"CTR-{TODAY.replace('-','')}-21{added:02d}",
        "task": f"page {x['url']} rank {x['pos']} CTR only {x['ctr']}% ({x['impr']} impr), optimize title/meta",
        "assigned_to": ["window5", "打磨师"], "priority": "P1", "status": "pending",
        "source": f"ctr_optimization_{TODAY}", "url": x["url"],
        "current_pos": x["pos"], "current_ctr": x["ctr"], "impressions": x["impr"],
        "created_at": NOW,
    })
    added += 1
state["last_gsc_pull"] = NOW
state["last_ga4_pull"] = NOW
json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"[OK] state.json: {added} new CTR todos")

log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 21:00 shift - {NOW}\n\n")
    f.write(f"GSC: {total_impr} impr, {total_clk} clk | GA4: {sessions} sess, {eng_rate:.1f}% eng\n")
    f.write(f"CTR: {len(ctr)} opps, {added} new\n")
print("DONE")
