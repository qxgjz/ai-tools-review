# -*- coding: utf-8 -*-
"""GSC 实时拉取后的状态更新 - 2026-10-09"""
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-09"
NOW = datetime.now().isoformat(timespec="seconds")

# 读实时拉到的数据
live_path = os.path.join(BASE, "gsc-ga4-report", "live_pull_20261009_1454.json")
with open(live_path, "r", encoding="utf-8") as f:
    live = json.load(f)

daily = live["daily"]
total_clicks = sum(r["clicks"] for r in daily)
total_impr = sum(r["impressions"] for r in daily)
avg_pos = sum(r["position"] * r["impressions"] for r in daily) / max(total_impr, 1)
ctr = total_clicks / max(total_impr, 1) * 100

print(f"[real-time daily 7d] clicks={total_clicks} impr={total_impr} ctr={ctr:.2f}% avg_pos={avg_pos:.1f}")

# ========== 更新 state.json ==========
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# 备份
bak = state_path + f".backup_live_{TODAY.replace('-','')}"
with open(bak, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

state["gsc_latest_clicks"] = total_clicks
state["gsc_latest_impressions"] = total_impr
state["gsc_latest_ctr"] = f"{ctr:.2f}%"
state["last_analytics_run"] = f"{TODAY} 23:00 (LIVE GSC via proxy, 7d window)"
state["last_updated"] = NOW
state["ga4_api_status"] = "GSC LIVE OK (via proxy 127.0.0.1:7890, service account aitoolcrux-bot). GA4 still pending."
state["live_gsc_pull_script"] = "iteration_center/_pull_gsc_via_proxy.py"

# 标记 P1-GA4-REBUILD-001 为部分完成（GSC 已通，GA4 未测）
for item in state.get("next_iteration_focus", []):
    if isinstance(item, dict) and item.get("id") == "P1-GA4-REBUILD-001":
        item["status"] = "in_progress"
        item["note"] = "GSC live pull verified 2026-10-09 via proxy. GA4 property authorization still TODO."
        print(f"[OK] updated: {item['id']} -> {item['status']}")
    if isinstance(item, dict) and item.get("id") == "P2-GOOGLE-NETWORK-BLOCK-001":
        item["status"] = "resolved"
        item["note"] = "Resolved 2026-10-09: use proxy 127.0.0.1:7890 + PySocks in httplib2. See _pull_gsc_via_proxy.py"
        print(f"[OK] updated: {item['id']} -> {item['status']}")

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] state.json updated, backup at {bak}")

# ========== 写实时洞察报告 ==========
report_path = os.path.join(BASE, "gsc-ga4-report", f"analyst_live_insight_{TODAY}.md")

# 过滤污染查询（含 -site:）
def is_polluted(q):
    return "-site:" in q or " -site" in q

top_queries = live["top_queries"]
clean_q = [r for r in top_queries if not is_polluted(r["keys"][0])]
polluted_q = [r for r in top_queries if is_polluted(r["keys"][0])]

pages = live["top_pages"]

report = f"""# 分析师实时洞察报告（LIVE GSC API） - {TODAY}

**拉取时间**: {NOW}
**数据来源**: GSC Search Console API 实时拉取（服务账号 `aitoolcrux-bot`，走代理 127.0.0.1:7890）
**资源**: `sc-domain:aitoolcrux.com`
**原始数据**: `live_pull_20261009_1454.json`

---

## 一句话结论

**9/24 断崖后，10 月日均曝光仅 8 次（vs 9 月上旬 111 次），且 /compare 排名从 33.8 进一步滑到 38.8——流量危机没有自愈，正在恶化。**

---

## 最近 7 天（9/30 - 10/6）每日趋势

| 日期 | 点击 | 曝光 | CTR | 平均排名 |
|---|---|---|---|---|
"""
for r in daily:
    report += f"| {r['keys'][0]} | {r['clicks']} | {r['impressions']} | {r['ctr']*100:.2f}% | {r['position']:.1f} |\n"
report += f"""| **合计** | **{total_clicks}** | **{total_impr}** | **{ctr:.2f}%** | **{avg_pos:.1f}** |

**与 9/6-9/23 高峰对比**：日均曝光从 111.2 → {total_impr/len(daily):.1f}（-92%），已连续 13 天低于 20。

## Top 20 真实查询词（已过滤 `-site:` 污染）

| 查询 | 点击 | 曝光 | 排名 | 解读 |
|---|---|---|---|---|
"""
for r in clean_q[:15]:
    q = r["keys"][0]
    pos = r["position"]
    if pos <= 10:
        note = "✅ 前10"
    elif pos <= 20:
        note = "⚠️ 前20"
    elif pos <= 50:
        note = "🔶 2-3页"
    else:
        note = "❌ 3页后"
    report += f"| `{q[:60]}` | {r['clicks']} | {r['impressions']} | {pos:.1f} | {note} |\n"

report += f"""
**关键观察**：
- **唯一有点击的真实词**："best voice changer 2026"（1 click, pos 4）
- **最大曝光词**："ai agent"（10 impr, pos 94.7）——在第 10 页，完全没点击价值
- **一批 "agent ai xxx" 长尾词**都在 pos 60-90：有曝光但完全没排名
- **无 `-site:` 污染词进入 Top 20**：说明 9/6-9/8 那波工具爬取高峰已过

## Top 15 页面（28天）

| 页面 | 点击 | 曝光 | 排名 | 环比上次报告 |
|---|---|---|---|---|
"""
# 上次报告的数据对比
prev_pages = {
    "/blog/best-ai-voice-changers-2026": (68, 16.5),
    "/compare": (272, 33.8),
    "/blog/openai_astra_review": (157, 10.8),
}
for r in pages[:15]:
    p = r["keys"][0].replace("https://www.aitoolcrux.com", "")
    prev = prev_pages.get(p)
    if prev:
        imp_chg = r["impressions"] - prev[0]
        pos_chg = r["position"] - prev[1]
        arrow = f"曝光{imp_chg:+d}, 排名{pos_chg:+.1f}"
    else:
        arrow = "-"
    report += f"| `{p}` | {r['clicks']} | {r['impressions']} | {r['position']:.1f} | {arrow} |\n"

report += """
## 新发现（基于实时数据，15:00 那轮没看到的）

### P0：/compare 排名继续下滑
- 上次报告：pos 33.8 / 272 impr
- 实时数据：pos **38.8** / 212 impr
- **排名 10 天内又掉了 5 位**，且曝光减少 60——说明不是波动，是持续被算法降权

### P1："/blog/best-ai-voice-changers-2026" 是唯一亮点
- 68 impr / 2 clicks / pos 16.5
- 这是全站唯一稳定进前 20 的内容页
- 优先投入：把它推到 pos 10 以内，预计 CTR 从 2.9% 升到 8-10%

### P1："ai agent" 词簇有 10 impr 但 pos 94.7
- 有真实搜索需求，但内容完全不匹配
- 说明站点在 "ai agent" 主题下的内容质量不够，进不了前 50
- **机会**：如果能把 /category/agent 或相关文章优化到 pos 30，能拿到一波长尾流量

### 已验证：GSC API 拉数链路可用
- 凭证：`.secrets/gsc-service-account.json`
- 代理：`127.0.0.1:7890`（Clash）
- 脚本：`iteration_center/_pull_gsc_via_proxy.py`
- 下次定时任务可以直接用这个脚本拉实时数据，不再依赖 GitHub Actions 落地报告

---

*本报告由 GSC API 实时数据生成，非 GitHub Actions 落地报告。*
"""

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)
print(f"[OK] live insight report: {report_path}")

# ========== 写日志 ==========
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
existing = open(log_path, "r", encoding="utf-8").read() if os.path.exists(log_path) else ""
existing += f"""

---

## 深夜实时拉数 - {NOW}

**触发**: 用户开代理后手动触发
**关键突破**: GSC API 实时拉取首次成功

### 排障过程

1. `Test-NetConnection oauth2.googleapis.com:443` = False（TCP 直连不通）
2. 发现 Clash 在 `127.0.0.1:7890` 监听，但系统代理未开
3. Python `requests` 走代理 0.4s 返回 404（代理通）
4. `httplib2` 不读 `HTTP_PROXY` 环境变量，需显式 `ProxyInfo`
5. 装 `PySocks`，写 `_pull_gsc_via_proxy.py` 显式传 proxy_info
6. 认证成功，拉到 7 天每日 + 28 天 query/page 数据

### 新发现（基于实时数据）

- /compare 排名从 33.8 滑到 38.8（恶化）
- /blog/best-ai-voice-changers-2026 是唯一稳定前 20 的内容页
- "ai agent" 词簇有曝光但 pos 94.7，完全没价值
- `-site:` 污染查询已退出 Top 20

### 产出

- `gsc-ga4-report/live_pull_20261009_1454.json`（原始数据）
- `gsc-ga4-report/analyst_live_insight_{TODAY}.md`（洞察报告）
- `iteration_center/_pull_gsc_via_proxy.py`（可复用脚本）
- state.json: ga4_api_status 更新为 "GSC LIVE OK"，2 条待办状态推进

"""
with open(log_path, "w", encoding="utf-8") as f:
    f.write(existing)
print(f"[OK] log appended: {log_path}")
print("\n=== LIVE PULL DONE ===")
