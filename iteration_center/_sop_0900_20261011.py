# -*- coding: utf-8 -*-
"""分析师 SOP 09:00 - 2026-10-11 (GSC + GA4 综合)"""
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-11"
NOW = datetime.now().isoformat(timespec="seconds")

# === GSC ===
gsc = json.load(open(os.path.join(BASE, "gsc-ga4-report", "live_pull_20261011_0807.json"), "r", encoding="utf-8"))
daily = gsc["daily"]
queries = gsc["top_queries"]
pages = gsc["top_pages"]

def gd(d): return d["keys"][0]
def gu(p): return p["keys"][0].replace("https://www.aitoolcrux.com", "") or "/"
def gi(d): return d["impressions"]
def gp(d): return d["position"]

total_impr = sum(gi(d) for d in daily)
total_clk = sum(d["clicks"] for d in daily)
avg_pos = sum(gp(d) * gi(d) for d in daily) / max(total_impr, 1)
print(f"[GSC] {gd(daily[0])}~{gd(daily[-1])}: {total_impr} impr, {total_clk} clk, avg pos {avg_pos:.1f}")

# CTR 筛选
ctr_opps = []
for p in pages:
    pos, impr, clk = gp(p), gi(p), p["clicks"]
    c = clk / max(impr, 1) * 100
    u = gu(p)
    if 5 <= pos <= 15 and c < 3 and impr >= 10:
        ctr_opps.append({"url": u, "pos": round(pos,1), "impr": impr, "clk": clk, "ctr": round(c,2)})
if len(ctr_opps) < 2:
    for p in pages:
        pos, impr, clk = gp(p), gi(p), p["clicks"]
        c = clk / max(impr, 1) * 100
        u = gu(p)
        if 5 <= pos <= 20 and c < 3 and impr >= 10 and not any(x["url"] == u for x in ctr_opps):
            ctr_opps.append({"url": u, "pos": round(pos,1), "impr": impr, "clk": clk, "ctr": round(c,2), "expanded": True})
print(f"[CTR] {len(ctr_opps)} opps:")
for x in ctr_opps:
    print(f"  {x['url']}: pos={x['pos']}, impr={x['impr']}, CTR={x['ctr']}%")

# === GA4 ===
ga4 = json.load(open(os.path.join(BASE, "gsc-ga4-report", "ga4_live_20261011_0807.json"), "r", encoding="utf-8"))
ov = ga4["overview"]
ga4_daily = ga4["daily"]
landing = ga4["top_landing"]

sessions = int(ov["sessions"])
users = int(ov["totalUsers"])
engaged = int(ov["engagedSessions"])
eng_rate = engaged / sessions * 100
avg_dur = float(ov["averageSessionDuration"])
print(f"[GA4] 28d: {sessions} sess, {users} users, eng {eng_rate:.1f}%, avg {avg_dur:.1f}s")

# GA4 异常
not_set = next((l for l in landing if l["page"] == "(not set)"), None)
not_set_s = int(not_set["sessions"]) if not_set else 0
not_set_e = int(not_set["engaged"]) if not_set else 0

zero_eng = [l for l in landing if int(l["engaged"]) == 0 and int(l["sessions"]) >= 5]
high_eng = [l for l in landing if int(l["sessions"]) >= 5 and int(l["engaged"])/max(int(l["sessions"]),1) > 0.5]

# === 写 audit_findings ===
findings = []
findings.append(("P1", f"GSC 近7天 {total_impr} 曝光仅 {total_clk} 点击，流量极低。"))
if not_set_s > 100:
    findings.append(("P0", f"GA4 '(not set)' 落地页 {not_set_s} sessions 仅 {not_set_e} engaged（{not_set_e/max(not_set_s,1)*100:.1f}%），疑似爬虫/垃圾流量。"))
if eng_rate < 15:
    findings.append(("P1", f"GA4 engagement rate 仅 {eng_rate:.1f}%，平均会话 {avg_dur:.1f}s，内容留存差。"))
for l in zero_eng[:3]:
    findings.append(("P1", f"GA4 页面 {l['page']}: {l['sessions']} sessions 0 engaged。"))

with open(os.path.join(BASE, "iteration_center", "audit_findings.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## 分析师 SOP 09:00 + GA4 - {NOW}\n\n")
    f.write(f"**GSC ({gd(daily[0])}~{gd(daily[-1])})**: {total_impr} impr, {total_clk} clk, avg pos {avg_pos:.1f}\n\n")
    f.write(f"**GA4 28d**: {sessions} sess, {eng_rate:.1f}% eng, avg {avg_dur:.1f}s\n\n")
    f.write(f"**CTR 优化 ({len(ctr_opps)} 个)**:\n")
    for x in ctr_opps:
        f.write(f"  - {x['url']}: pos={x['pos']}, impr={x['impr']}, CTR={x['ctr']}%\n")
    f.write(f"\n**问题发现**:\n")
    for sev, desc in findings:
        f.write(f"- **[{sev}]** {desc}\n")
    f.write(f"\n**高表现页面**:\n")
    for l in high_eng:
        rate = int(l["engaged"])/max(int(l["sessions"]),1)*100
        f.write(f"  - {l['page']}: {l['sessions']} sess, {rate:.0f}% eng\n")

# === 更新 state.json ===
state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))

added = 0
# CTR 待办（去重）
for x in ctr_opps:
    existing = [t for t in state["next_iteration_focus"] if t.get("url") == x["url"] and "ctr_optimization" in t.get("source", "")]
    if existing:
        print(f"  [SKIP CTR] {x['url']}")
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

# GA4 待办
for sev, desc in findings:
    if sev in ("P0", "P1"):
        state["next_iteration_focus"].append({
            "id": f"GA4-{TODAY.replace('-','')}-{added:03d}",
            "task": desc, "assigned_to": ["window4", "分析师"],
            "priority": sev, "status": "pending",
            "source": f"ga4_analysis_{TODAY}", "created_at": NOW,
        })
        added += 1

state["last_gsc_pull"] = NOW
state["last_ga4_pull"] = NOW
json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"[OK] state.json: {added} new todos")

# === 写日志 ===
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"# 分析师日志 - {TODAY}\n\n## 09:00 班次 - {NOW}\n\n")
    f.write(f"- GSC: {gd(daily[0])}~{gd(daily[-1])}, {total_impr} impr, {total_clk} clk\n")
    f.write(f"- GA4: {sessions} sess, {eng_rate:.1f}% eng, avg {avg_dur:.1f}s\n")
    f.write(f"- CTR opps: {len(ctr_opps)}\n")
    f.write(f"- State todos added: {added}\n")
print("DONE")
