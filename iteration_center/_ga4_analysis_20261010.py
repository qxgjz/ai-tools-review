# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-10"
NOW = datetime.now().isoformat(timespec="seconds")

ga4 = json.load(open(os.path.join(BASE, "gsc-ga4-report", "ga4_live_20261010_2047.json"), "r", encoding="utf-8"))
ov = ga4["overview"]
daily = ga4["daily"]
landing = ga4["top_landing"]

sessions = int(ov["sessions"])
users = int(ov["totalUsers"])
engaged = int(ov["engagedSessions"])
eng_rate = engaged / sessions * 100
avg_dur = float(ov["averageSessionDuration"])
pageviews = int(ov["screenPageViews"])

# 异常天检测
daily_sorted = sorted(daily, key=lambda x: int(x["sessions"]), reverse=True)
peak_day = daily_sorted[0]
peak_sessions = int(peak_day["sessions"])
median_sessions = sorted([int(d["sessions"]) for d in daily])[len(daily)//2]

# (not set) 问题
not_set = next((l for l in landing if l["page"] == "(not set)"), None)
not_set_sessions = int(not_set["sessions"]) if not_set else 0
not_set_engaged = int(not_set["engaged"]) if not_set else 0

# 0 engagement 页面
zero_eng = [l for l in landing if int(l["engaged"]) == 0 and int(l["sessions"]) >= 5]
# 高 engagement 页面
high_eng = [l for l in landing if int(l["sessions"]) >= 5 and int(l["engaged"])/max(int(l["sessions"]),1) > 0.5]

print(f"[GA4] 28d: {sessions} sess, {users} users, eng_rate={eng_rate:.1f}%, avg_dur={avg_dur:.1f}s, pv={pageviews}")
print(f"[ANOMALY] peak {peak_day['date']}: {peak_sessions} sess (median={median_sessions})")
print(f"[NOTSET] {not_set_sessions} sess, engaged={not_set_engaged}")
print(f"[ZERO_ENG] {len(zero_eng)} pages with 0 engagement:")
for l in zero_eng:
    print(f"  {l['page']}: {l['sessions']} sess")
print(f"[HIGH_ENG] {len(high_eng)} pages >50% engagement:")
for l in high_eng:
    print(f"  {l['page']}: {l['sessions']} sess, {l['engaged']} engaged")

# 写 audit_findings
findings = []
if peak_sessions > median_sessions * 3:
    findings.append(("P0", f"GA4 异常流量：{peak_day['date']} 单日 {peak_sessions} sessions，是中位数({median_sessions})的 {peak_sessions//max(median_sessions,1)} 倍。需排查是否爬虫/垃圾流量。"))
if not_set_sessions > 50 and not_set_engaged < 5:
    findings.append(("P0", f"GA4 '(not set)' 落地页 {not_set_sessions} sessions 但仅 {not_set_engaged} engaged（{not_set_engaged/max(not_set_sessions,1)*100:.1f}%），大量流量无有效落地页，可能是直接访问/爬虫。"))
if eng_rate < 15:
    findings.append(("P1", f"GA4 整体 engagement rate 仅 {eng_rate:.1f}%（{engaged}/{sessions}），平均会话 {avg_dur:.1f} 秒，内容留存极差。"))
for l in zero_eng[:3]:
    findings.append(("P1", f"GA4 页面 {l['page']}: {l['sessions']} sessions 但 0 engaged，用户进来就走，内容或加载有问题。"))

with open(os.path.join(BASE, "iteration_center", "audit_findings.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## GA4 数据分析 - {NOW}\n\n")
    f.write(f"**28天概览**: {sessions} sessions, {users} users, engagement {eng_rate:.1f}%, avg duration {avg_dur:.1f}s, {pageviews} pageviews\n\n")
    for sev, desc in findings:
        f.write(f"- **[{sev}]** {desc}\n")
    f.write(f"\n**高表现页面**:\n")
    for l in high_eng:
        rate = int(l["engaged"])/max(int(l["sessions"]),1)*100
        f.write(f"  - {l['page']}: {l['sessions']} sess, {rate:.0f}% engagement\n")

# 写 state.json 待办
state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))
added = 0
for sev, desc in findings:
    if sev in ("P0", "P1"):
        state["next_iteration_focus"].append({
            "id": f"GA4-{TODAY.replace('-','')}-{added:03d}",
            "task": desc,
            "assigned_to": ["window4", "分析师"],
            "priority": sev,
            "status": "pending",
            "source": f"ga4_analysis_{TODAY}",
            "created_at": NOW,
        })
        added += 1
state["last_ga4_pull"] = NOW
state["last_ga4_sessions"] = sessions
state["last_ga4_engagement_rate"] = round(eng_rate, 1)
json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"[OK] state.json: {added} GA4 todos")

# 写日志
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## GA4 分析 - {NOW}\n\n")
    f.write(f"- 28d: {sessions} sess, {users} users, eng {eng_rate:.1f}%, avg {avg_dur:.1f}s\n")
    f.write(f"- 异常: {peak_day['date']} {peak_sessions} sess (median {median_sessions})\n")
    f.write(f"- (not set): {not_set_sessions} sess, {not_set_engaged} engaged\n")
    f.write(f"- 0 engagement 页面: {len(zero_eng)} 个\n")
    f.write(f"- 高 engagement 页面: {len(high_eng)} 个\n")
    f.write(f"- 写入待办: {added} 条\n")
print("DONE")
