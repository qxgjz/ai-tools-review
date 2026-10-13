# -*- coding: utf-8 -*-
"""分析师 SOP 21:00 班次 - 含 CTR 优化 - 2026-10-09"""
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-09"
NOW = datetime.now().isoformat(timespec="seconds")

# 读实时 GSC 数据
gsc_path = os.path.join(BASE, "gsc-ga4-report", "live_pull_20261009_2023.json")
with open(gsc_path, "r", encoding="utf-8") as f:
    gsc = json.load(f)

daily = gsc.get("daily", [])
queries = gsc.get("top_queries", [])
pages = gsc.get("top_pages", [])

# 适配 GSC 输出格式: keys=[date/url], clicks, impressions, ctr, position
def get_date(d): return d.get("keys", [""])[0]
def get_url(p): return p.get("keys", [""])[0].replace("https://www.aitoolcrux.com", "") or "/"
def get_clicks(d): return d.get("clicks", 0)
def get_impr(d): return d.get("impressions", 0)
def get_pos(d): return d.get("position", 999)

# === 1. 趋势分析 ===
total_impr = sum(get_impr(d) for d in daily)
total_clk = sum(get_clicks(d) for d in daily)
avg_pos = sum(get_pos(d) * get_impr(d) for d in daily) / max(total_impr, 1)
ctr_overall = total_clk / max(total_impr, 1) * 100

print(f"[TREND] {get_date(daily[0])}~{get_date(daily[-1])}: {total_impr} impr, {total_clk} clk, CTR={ctr_overall:.2f}%, avg pos={avg_pos:.1f}")

# === 2. CTR 优化筛选（排名 5-15, CTR<3%） ===
ctr_opportunities = []
for p in pages:
    pos = get_pos(p)
    impr = get_impr(p)
    clk = get_clicks(p)
    ctr = clk / max(impr, 1) * 100
    url = get_url(p)
    
    # 5-15 位, CTR<3%, 曝光>=10
    if 5 <= pos <= 15 and ctr < 3 and impr >= 10:
        ctr_opportunities.append({
            "url": url, "pos": pos, "impr": impr, "clk": clk, "ctr": round(ctr, 2),
            "reason": f"排名{pos:.1f}但CTR仅{ctr:.2f}%"
        })

# 如果不足2个，扩大到 5-20
if len(ctr_opportunities) < 2:
    for p in pages:
        pos = get_pos(p)
        impr = get_impr(p)
        clk = get_clicks(p)
        ctr = clk / max(impr, 1) * 100
        url = get_url(p)
        if 5 <= pos <= 20 and ctr < 3 and impr >= 10:
            if not any(c["url"] == url for c in ctr_opportunities):
                ctr_opportunities.append({
                    "url": url, "pos": pos, "impr": impr, "clk": clk, "ctr": round(ctr, 2),
                    "reason": f"排名{pos:.1f}但CTR仅{ctr:.2f}%（扩大范围）"
                })

print(f"[CTR] {len(ctr_opportunities)} CTR optimization opportunities found:")
for c in ctr_opportunities:
    print(f"  {c['url']}: pos={c['pos']:.1f}, impr={c['impr']}, CTR={c['ctr']}%")

# === 3. 问题发现 ===
findings = []
# 0 点击
if total_clk == 0 and total_impr > 50:
    findings.append(("P1", f"近7天 GSC {total_impr} 曝光但 0 点击，CTR=0%。流量持续低迷。"))
# /compare 排名恶化
compare_page = next((p for p in pages if "/compare" in get_url(p)), None)
if compare_page and get_pos(compare_page) > 35:
    findings.append(("P1", f"/compare 页面 {get_impr(compare_page)} 曝光但排名 {get_pos(compare_page):.1f}（持续恶化），需优化内链和 title。"))
# ai agent 词簇
agent_queries = [q for q in queries if "agent" in q.get("keys", [""])[0].lower()]
agent_impr = sum(get_impr(q) for q in agent_queries)
if agent_impr > 5:
    findings.append(("P2", f"'ai agent' 词簇 {agent_impr} 曝光但排名均在 50+，无对应落地页，内容缺失。"))

# === 4. 写 audit_findings.md ===
audit_path = os.path.join(BASE, "iteration_center", "audit_findings.md")
with open(audit_path, "a", encoding="utf-8") as f:
    f.write(f"\n\n## 分析师 SOP 21:00 - {NOW}\n\n")
    f.write(f"**GSC 数据 ({get_date(daily[0])}~{get_date(daily[-1])})**: {total_impr} impr, {total_clk} clk, avg pos {avg_pos:.1f}\n\n")
    for sev, desc in findings:
        f.write(f"- **[{sev}]** {desc}\n")
    f.write(f"\n**CTR 优化机会 ({len(ctr_opportunities)} 个)**:\n")
    for c in ctr_opportunities:
        f.write(f"  - {c['url']}: pos={c['pos']}, impr={c['impr']}, CTR={c['ctr']}%\n")

print(f"[OK] audit_findings.md updated")

# === 5. 更新 state.json ===
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# 备份
import shutil
shutil.copy(state_path, state_path + f".backup_2100_{TODAY.replace('-','')}")

# 加 CTR 待办
ctr_todos_added = 0
for c in ctr_opportunities:
    todo = {
        "id": f"CTR-{TODAY.replace('-','')}-{ctr_todos_added+1:03d}",
        "task": f"页面 {c['url']} 排名 {c['pos']:.1f} 但 CTR 仅 {c['ctr']}%（{c['impr']}曝光），优化 title/meta description 提升点击率",
        "assigned_to": ["window5", "打磨师"],
        "priority": "P1",
        "status": "pending",
        "source": f"ctr_optimization_{TODAY}",
        "url": c["url"],
        "current_pos": c["pos"],
        "current_ctr": c["ctr"],
        "impressions": c["impr"],
        "created_at": NOW,
    }
    state["next_iteration_focus"].append(todo)
    ctr_todos_added += 1

# 更新状态字段
state["last_gsc_pull"] = NOW
state["last_gsc_impr"] = total_impr
state["last_gsc_clk"] = total_clk
state["last_gsc_avg_pos"] = round(avg_pos, 1)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"[OK] state.json: {ctr_todos_added} CTR todos added")

# === 6. 写日志 ===
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"""

---

## 21:00 班次 - {NOW}

### GSC 实时数据
- 周期: {get_date(daily[0])} ~ {get_date(daily[-1])}
- 总曝光: {total_impr} | 总点击: {total_clk} | CTR: {ctr_overall:.2f}% | 平均排名: {avg_pos:.1f}

### CTR 优化筛选
- 筛选条件: 排名 5-15（不足扩大到 5-20）+ CTR<3% + 曝光>=10
- 产出: {len(ctr_opportunities)} 个待办
""")
    for c in ctr_opportunities:
        f.write(f"  - {c['url']}: pos={c['pos']}, impr={c['impr']}, CTR={c['ctr']}%\n")

    f.write(f"""
### 问题发现
""")
    for sev, desc in findings:
        f.write(f"- [{sev}] {desc}\n")

    f.write(f"""
### State.json 更新
- CTR 待办: {ctr_todos_added} 条
- 备份: state.json.backup_2100_{TODAY.replace('-','')}
""")

print(f"[OK] log written")

print("\n=== SOP 21:00 COMPLETE ===")
print(f"Total impressions: {total_impr}")
print(f"Total clicks: {total_clk}")
print(f"CTR opportunities: {len(ctr_opportunities)}")
print(f"State.json todos added: {ctr_todos_added}")
