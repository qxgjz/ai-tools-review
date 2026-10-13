# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-12"
NOW = datetime.now().isoformat(timespec="seconds")

gsc = json.load(open(os.path.join(BASE, "gsc-ga4-report", "live_pull_20261012_0816.json"), "r", encoding="utf-8"))
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

ga4 = json.load(open(os.path.join(BASE, "gsc-ga4-report", "ga4_live_20261012_0816.json"), "r", encoding="utf-8"))
ov = ga4["overview"]
landing = ga4["top_landing"]
sessions = int(ov["sessions"])
engaged = int(ov["engagedSessions"])
eng_rate = engaged / sessions * 100
avg_dur = float(ov["averageSessionDuration"])
print(f"[GA4] {sessions} sess, {eng_rate:.1f}% eng, avg {avg_dur:.1f}s")

zero_eng = [l for l in landing if int(l["engaged"]) == 0 and int(l["sessions"]) >= 5]
print(f"[ZERO_ENG] {len(zero_eng)} pages:")
for l in zero_eng:
    print(f"  {l['page']}: {l['sessions']} sess")

# audit_findings
with open(os.path.join(BASE, "iteration_center", "audit_findings.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## SOP 09:00 + GA4 - {NOW}\n\n")
    f.write(f"GSC: {gd(daily[0])}~{gd(daily[-1])}, {total_impr} impr, {total_clk} clk | GA4: {sessions} sess, {eng_rate:.1f}% eng, avg {avg_dur:.1f}s\n\n")
    f.write(f"CTR opps: {len(ctr)}\n")
    for x in ctr:
        f.write(f"  - {x['url']}: pos={x['pos']}, CTR={x['ctr']}%\n")
    f.write(f"\n0 engagement pages: {len(zero_eng)}\n")
    for l in zero_eng:
        f.write(f"  - {l['page']}: {l['sessions']} sess\n")

# state.json
state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))
added = 0
for x in ctr:
    existing = [t for t in state["next_iteration_focus"] if t.get("url") == x["url"] and "ctr_optimization" in t.get("source", "")]
    if existing:
        print(f"  [SKIP] {x['url']}")
        continue
    state["next_iteration_focus"].append({
        "id": f"CTR-{TODAY.replace('-','')}-{added:03d}",
        "task": f"page {x['url']} rank {x['pos']} CTR only {x['ctr']}% ({x['impr']} impr), optimize title/meta",
        "assigned_to": ["window5", "打磨师"], "priority": "P1", "status": "pending",
        "source": f"ctr_optimization_{TODAY}", "url": x["url"],
        "current_pos": x["pos"], "current_ctr": x["ctr"], "impressions": x["impr"],
        "created_at": NOW,
    })
    added += 1
# 新的 0 engagement 页面
for l in zero_eng:
    desc = f"GA4 page {l['page']}: {l['sessions']} sessions 0 engaged, content quality issue"
    state["next_iteration_focus"].append({
        "id": f"GA4-{TODAY.replace('-','')}-{added:03d}",
        "task": desc, "assigned_to": ["window4", "分析师"],
        "priority": "P1", "status": "pending",
        "source": f"ga4_analysis_{TODAY}", "created_at": NOW,
    })
    added += 1
state["last_gsc_pull"] = NOW
state["last_ga4_pull"] = NOW
json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"[OK] state.json: {added} new todos")

# log
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"# Analyst Log - {TODAY}\n\n## 09:00 shift - {NOW}\n\n")
    f.write(f"GSC: {total_impr} impr, {total_clk} clk | GA4: {sessions} sess, {eng_rate:.1f}% eng\n")
    f.write(f"CTR: {len(ctr)} opps, {added} new todos\n")
    f.write(f"0 eng pages: {len(zero_eng)}\n")
print("DONE")
