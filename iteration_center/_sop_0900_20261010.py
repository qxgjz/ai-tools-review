# -*- coding: utf-8 -*-
"""分析师 SOP 9:00 班次 - 2026-10-10"""
import json, os, shutil
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-10"
NOW = datetime.now().isoformat(timespec="seconds")

# 读最新 GSC 数据
gsc_path = os.path.join(BASE, "gsc-ga4-report", "live_pull_20261010_0809.json")
with open(gsc_path, "r", encoding="utf-8") as f:
    gsc = json.load(f)

daily = gsc.get("daily", [])
queries = gsc.get("top_queries", [])
pages = gsc.get("top_pages", [])

def get_date(d): return d.get("keys", [""])[0]
def get_url(p): return p.get("keys", [""])[0].replace("https://www.aitoolcrux.com", "") or "/"
def get_clicks(d): return d.get("clicks", 0)
def get_impr(d): return d.get("impressions", 0)
def get_pos(d): return d.get("position", 999)

# 1. 趋势
total_impr = sum(get_impr(d) for d in daily)
total_clk = sum(get_clicks(d) for d in daily)
avg_pos = sum(get_pos(d) * get_impr(d) for d in daily) / max(total_impr, 1)
ctr_overall = total_clk / max(total_impr, 1) * 100
print(f"[TREND] {get_date(daily[0])}~{get_date(daily[-1])}: {total_impr} impr, {total_clk} clk, CTR={ctr_overall:.2f}%, avg pos={avg_pos:.1f}")

# 2. CTR 优化筛选（5-15, CTR<3%, 曝光>=10）
ctr_opps = []
for p in pages:
    pos, impr, clk = get_pos(p), get_impr(p), get_clicks(p)
    ctr = clk / max(impr, 1) * 100
    url = get_url(p)
    if 5 <= pos <= 15 and ctr < 3 and impr >= 10:
        ctr_opps.append({"url": url, "pos": round(pos,1), "impr": impr, "clk": clk, "ctr": round(ctr,2)})

# 不足2个则扩大到 5-20
if len(ctr_opps) < 2:
    for p in pages:
        pos, impr, clk = get_pos(p), get_impr(p), get_clicks(p)
        ctr = clk / max(impr, 1) * 100
        url = get_url(p)
        if 5 <= pos <= 20 and ctr < 3 and impr >= 10:
            if not any(c["url"] == url for c in ctr_opps):
                ctr_opps.append({"url": url, "pos": round(pos,1), "impr": impr, "clk": clk, "ctr": round(ctr,2), "expanded": True})

print(f"[CTR] {len(ctr_opps)} opportunities:")
for c in ctr_opps:
    print(f"  {c['url']}: pos={c['pos']}, impr={c['impr']}, CTR={c['ctr']}%")

# 3. 问题发现
findings = []
if total_clk <= 1 and total_impr > 50:
    findings.append(("P1", f"近7天 {total_impr} 曝光仅 {total_clk} 点击，流量极低。"))
compare_p = next((p for p in pages if "/compare" in get_url(p)), None)
if compare_p and get_pos(compare_p) > 35:
    findings.append(("P1", f"/compare {get_impr(compare_p)} 曝光排 {get_pos(compare_p):.1f} 位，CTR 仅 {get_clicks(compare_p)/max(get_impr(compare_p),1)*100:.2f}%。"))
agent_q = [q for q in queries if "agent" in q.get("keys",[""])[0].lower()]
agent_impr = sum(get_impr(q) for q in agent_q)
if agent_impr > 5:
    findings.append(("P2", f"'ai agent' 词簇 {agent_impr} 曝光，平均排名 60+，无对应落地页。"))

# 4. 写 audit_findings.md
audit_path = os.path.join(BASE, "iteration_center", "audit_findings.md")
with open(audit_path, "a", encoding="utf-8") as f:
    f.write(f"\n\n## 分析师 SOP 09:00 - {NOW}\n\n")
    f.write(f"**GSC ({get_date(daily[0])}~{get_date(daily[-1])})**: {total_impr} impr, {total_clk} clk, avg pos {avg_pos:.1f}\n\n")
    for sev, desc in findings:
        f.write(f"- **[{sev}]** {desc}\n")
    f.write(f"\n**CTR 优化 ({len(ctr_opps)} 个)**:\n")
    for c in ctr_opps:
        f.write(f"  - {c['url']}: pos={c['pos']}, impr={c['impr']}, CTR={c['ctr']}%\n")
print("[OK] audit_findings.md")

# 5. 更新 state.json
state_path = os.path.join(BASE, "iteration_center", "state.json")
shutil.copy(state_path, state_path + f".backup_0900_{TODAY.replace('-','')}")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

added = 0
for c in ctr_opps:
    # 避免重复：检查是否已有相同 URL 的待办
    existing = [t for t in state["next_iteration_focus"] if t.get("url") == c["url"] and t.get("source","").startswith("ctr_optimization")]
    if existing:
        print(f"  [SKIP] {c['url']} already has CTR todo")
        continue
    todo = {
        "id": f"CTR-{TODAY.replace('-','')}-{added+1:03d}",
        "task": f"页面 {c['url']} 排名 {c['pos']} 但 CTR 仅 {c['ctr']}%（{c['impr']}曝光），优化 title/meta description 提升点击率",
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
    added += 1

state["last_gsc_pull"] = NOW
state["last_gsc_impr"] = total_impr
state["last_gsc_clk"] = total_clk
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] state.json: {added} new CTR todos")

# 6. 写日志
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 09:00 班次 - {NOW}\n\n")
    f.write(f"- GSC 周期: {get_date(daily[0])}~{get_date(daily[-1])}\n")
    f.write(f"- 曝光: {total_impr} | 点击: {total_clk} | CTR: {ctr_overall:.2f}% | avg pos: {avg_pos:.1f}\n")
    f.write(f"- CTR 优化产出: {len(ctr_opps)} 个（新增写入 {added} 个）\n")
    for c in ctr_opps:
        f.write(f"  - {c['url']}: pos={c['pos']}, impr={c['impr']}, CTR={c['ctr']}%\n")
    f.write(f"- 问题发现: {len(findings)} 条\n")
    for sev, desc in findings:
        f.write(f"  - [{sev}] {desc}\n")
print("[OK] log written")

print("\n=== 09:00 SOP COMPLETE ===")
print(f"Impr={total_impr}, Clk={total_clk}, CTR opps={len(ctr_opps)}, New todos={added}")
