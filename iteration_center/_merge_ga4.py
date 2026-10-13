# -*- coding: utf-8 -*-
"""GA4 数据合并入实时洞察报告 - 2026-10-09"""
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-09"
NOW = datetime.now().isoformat(timespec="seconds")

# 读 GA4 数据
ga4_path = os.path.join(BASE, "gsc-ga4-report", "ga4_live_20261009_1503.json")
with open(ga4_path, "r", encoding="utf-8") as f:
    ga4 = json.load(f)

overview = ga4["overview"]
daily = ga4["daily"]
top_landing = ga4["top_landing"]

sessions = int(overview.get("sessions", 0))
users = int(overview.get("totalUsers", 0))
new_users = int(overview.get("newUsers", 0))
engaged = int(overview.get("engagedSessions", 0))
duration = float(overview.get("averageSessionDuration", 0))
engagement_rate = engaged / max(sessions, 1) * 100
new_user_pct = new_users / max(users, 1) * 100

# 找爆发日
peak = max(daily, key=lambda x: int(x["sessions"]))
avg_daily = sessions / 28

# 读已有报告
report_path = os.path.join(BASE, "gsc-ga4-report", f"analyst_live_insight_{TODAY}.md")
with open(report_path, "r", encoding="utf-8") as f:
    report = f.read()

# 追加 GA4 部分
ga4_section = f"""

---

## GA4 实时数据（28 天：9/10 - 10/7）

**Property**: `properties/556518278`（aitoolcrux）
**原始数据**: `ga4_live_20261009_1503.json`

### 总览

| 指标 | 值 | 健康度 |
|---|---|---|
| Sessions | {sessions} | - |
| Users | {users} | - |
| New Users | {new_users}（{new_user_pct:.1f}%） | 🔴 几乎 0 回访 |
| Engaged Sessions | {engaged} | - |
| **Engagement Rate** | **{engagement_rate:.1f}%** | 🔴 远低于 30% 行业基准 |
| Avg Session Duration | {duration:.1f}s | 🔴 极短 |
| 日均 Sessions | {avg_daily:.0f} | - |

### 每日趋势（14 天）

| 日期 | Sessions | Users | Engaged |
|---|---|---|---|
"""
for r in sorted(daily, key=lambda x: x["date"]):
    d = r["date"]
    d = f"{d[:4]}-{d[4:6]}-{d[6:]}"
    flag = " 🔥" if int(r["sessions"]) > 500 else ""
    ga4_section += f"| {d} | {r['sessions']} | {r['users']} | {r['engaged']} |{flag}\n"

ga4_section += f"""
**10/3 异常爆发**：{peak['sessions']} sessions（其他天日均 ~100），疑似被某外部链接/Reddit/HN 推荐带量，需查 referral 来源。

### Top Landing Pages

| 页面 | Sessions | Engaged | Engagement Rate |
|---|---|---|---|
"""
for p in top_landing:
    sess = int(p["sessions"])
    eng = int(p["engaged"])
    er = eng / max(sess, 1) * 100
    flag = " ✅" if er > 30 else (" 🔴" if er < 5 else "")
    ga4_section += f"| `{p['page']}` | {sess} | {eng} | {er:.0f}%{flag} |\n"

ga4_section += f"""

### P0：GA4 vs GSC 严重不匹配

- **GSC 说**：/compare 28 天 212 impressions、2 clicks；/blog/best-ai-voice-changers-2026 68 impr、2 clicks
- **GA4 说**：/compare 和 voice-changers 都没进 top landing 15
- **结论**：GSC 给的曝光大部分没转化成真实 session，或落地页加载/追踪有问题

### P0：22.6% 的 landing page 是 `(not set)`
- 240 / 1063 sessions 没有正确的 landing page 标记
- 说明 gtag/GA4 配置有 bug，可能是 SPA 路由变化没触发 page_view

### P1：`/blog/suno-alternatives` 是唯一健康页
- 30 sessions / 22 engaged / 73% engagement rate
- 但 GSC 里这个词没出现——说明流量不是 Google 自然搜索来的（可能直接/社媒/referral）
- **机会**：分析这 30 个 session 从哪来，复制这个引流路径

### P1：99.9% 是新用户
- 1596 / 1598 是新用户——网站几乎没有回访
- 冷启动期正常，但内容留存力不足（10.5 秒就走了）

---

## 综合结论（GSC + GA4）

**流量现状**：
- Google 自然搜索：58 impr / 0 clicks（7 天），在枯竭
- 实际 sessions：日均 ~100，但 92% 不互动（engagement rate 7.9%）
- 10/3 有一波外部引流（893 sessions），但不是 Google 来的

**最该做的 3 件事**：
1. 🔴 **修 GA4 配置**：`(not set)` 占 22.6% 说明追踪漏了，先把这个修了
2. 🔴 **查 10/3 爆发来源**：893 sessions 从哪来的？如果是 Reddit/HN，复制这个渠道
3. 🟡 **优化 /blog/suno-alternatives**：唯一 73% 互动率的页，把它推成流量主力

"""

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report + ga4_section)
print(f"[OK] report updated with GA4: {report_path}")

# ========== 更新 state.json ==========
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["last_analytics_run"] = f"{TODAY} 23:00 (LIVE GSC+GA4 via proxy, 28d window)"
state["ga4_api_status"] = f"LIVE OK. property=properties/556518278. {sessions} sessions / {engaged} engaged / ER={engagement_rate:.1f}%."
state["ga4_live_pull_script"] = "iteration_center/_pull_ga4_via_proxy.py"
state["last_updated"] = NOW

# 推进 P1-GA4-REBUILD-001 为 resolved
for item in state.get("next_iteration_focus", []):
    if isinstance(item, dict) and item.get("id") == "P1-GA4-REBUILD-001":
        item["status"] = "resolved"
        item["note"] = f"Resolved {TODAY}: GSC+GA4 live pull both working via proxy. 28d sessions={sessions}, ER={engagement_rate:.1f}%."
        print(f"[OK] {item['id']} -> resolved")

# 新增 P0 发现
new_todos = [
    {
        "id": "P0-GA4-NOTSET-001",
        "assigned_to": "工程师",
        "title": "GA4 22.6% landing page 为 (not set)，追踪配置漏了",
        "detail": "240/1063 sessions 没有正确 landing page。可能是 Next.js SPA 路由切换没触发 gtag page_view。需要检查 next/script 配置和 routeChangeComplete 钩子。",
        "status": "open",
        "created": TODAY,
    },
    {
        "id": "P0-ANALYZE-1003-SPIKE",
        "assigned_to": "增长黑客",
        "title": "查 10/3 那 893 sessions 从哪来的（referral/社媒/直接）",
        "detail": "10/3 突然 893 sessions，其他天日均 100。GA4 Explorer 查 sessionSource / sessionMedium / sessionCampaign 维度。如果是 Reddit/HN，复制渠道。",
        "status": "open",
        "created": TODAY,
    },
    {
        "id": "P1-SUNO-ALTS-001",
        "assigned_to": "创作家",
        "title": "/blog/suno-alternatives 73% engagement，扩写同类内容",
        "detail": "全站唯一健康页。用户停留/互动好。可以复制结构到 voice-changers、video-generators 等同类 alternatives 文章。",
        "status": "open",
        "created": TODAY,
    },
]
state.setdefault("next_iteration_focus", []).extend(new_todos)
print(f"[OK] added {len(new_todos)} new todos")

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# ========== 追加日志 ==========
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"""

---

## GA4 实时拉数 - {NOW}

**突破**: GA4 API 首次拉通
- property: `properties/556518278` (aitoolcrux)
- 自动发现: 服务账号能看到 2 个 account、2 个 property
- 脚本: `iteration_center/_pull_ga4_via_proxy.py`

**关键数字（28天）**:
- {sessions} sessions / {users} users / {new_users} new users
- engagement rate {engagement_rate:.1f}%（远低于 30% 基准）
- avg session duration {duration:.1f}s
- 10/3 异常 893 sessions（疑似外部引流）

**新 P0/P1**:
- P0-GA4-NOTSET-001: 22.6% landing page 是 (not set)
- P0-ANALYZE-1003-SPIKE: 查 10/3 爆发来源
- P1-SUNO-ALTS-001: suno-alternatives 73% ER，扩写同类

**产出**:
- `gsc-ga4-report/ga4_live_20261009_1503.json`
- 报告已合并 GSC+GA4 综合结论
""")
print(f"[OK] log appended")
print("\n=== GA4 PULL DONE ===")
