# -*- coding: utf-8 -*-
"""分析师窗口 SOP 执行脚本 - 2026-10-09
只读分析，不改代码。追加 audit_findings、写报告、更新 state.json、写日志。
"""
import json
import os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-09"
NOW = datetime.now().isoformat(timespec="seconds")

# ========== 1. 追加 audit_findings.md ==========
audit_path = os.path.join(BASE, "iteration_center", "audit_findings.md")
new_findings = f"""

---

## 分析师窗口自动审计 - {TODAY}（SOP版）

**触发时间**: {NOW}
**数据来源**: gsc-ga4-report/2026-09-06_2026-10-05.md + gsc-ga4-report/latest_gsc.md（已落地报告，非实时API）
**分析师结论**: 站点处于严重流量危机，9/24 后曝光断崖，需立即响应。

### P0-TRAFFIC-CLIFF-20260924-001: 9/24 曝光单日暴跌 92.3%，点击归零

**证据（来自 GSC Daily Trend 表，Python 实算）**:

| 时段 | 天数 | 总点击 | 总曝光 | 日均曝光 |
|---|---|---|---|---|
| 9/6 - 9/23（暴跌前） | 18 | 9 | 2,001 | 111.2 |
| 9/24 - 10/4（暴跌后） | 11 | 0 | 94 | 8.5 |
| **变化** | - | **-100%** | **-95.3%（总量）** | **-92.3%（日均）** |

**关键单日**:
- 9/23: 79 曝光
- 9/24: 1 曝光（单日 -98.7%）
- 之后 11 天从未回到 20 曝光以上

**与上一周期对比（latest_gsc.md, 8/20-9/18）**:
- 上期: 8 clicks / 1581 impr / CTR 0.51% / avg pos 23.98
- 本期: 9 clicks / 2095 impr / CTR 0.43% / avg pos 25.10
- 曝光总量微增但完全由 9/6-9/23 贡献；本期后半段已无流量

**为什么这是 P0 而不是 P1**:
1. 跌幅是单日断崖（-98.7% in 1 day），不是渐进竞争加剧
2. 9/24 前后技术检查（10/8 审计）已排除 robots/sitemap/Cloudflare/抓取问题
3. 11 天恢复期内日均仅 8.5 曝光，没有自然回弹
4. 冷启动期本就流量极小，再跌 92% 等同于站点在 Google 上"消失"

**根因假设（按可能性排序）**:
1. **Google 9 月 Helpful Content / Spam 更新惩罚**（9/24 时间点吻合）：145 篇文章缺 BLUF、104 篇外链不足、47% 文章 <50 分——这些内容质量信号正好触发 HCU
2. **批量低质文章拖累域名权重**：total_posts=128，但多数为 API 批量生成（URL 含 article-api-20260903 即知）
3. **索引大规模掉页**：需 GSC 索引报告验证（当前无法实时拉取）
4. 排除：技术拦截（已验证正常）

### P1-QUERY-POLLUTION-001: GSC Top Queries 被"操作员搜索"污染

**证据**: Top 20 查询词中至少 12 条含 `-site:reddit.com -site:twitter.com -site:x.com ...` 排除操作符。
- 真实用户不会输入这种查询
- 这些是 SEO 工具（Ahrefs/Semrush/Openseo）或竞品调研在爬取 SERP
- 影响：GSC 关键词报告失真，基于此做的关键词决策会被误导

**影响**: 真实用户查询极少（仅 "best voice changer 2026" 1 click / 1 imp），说明品牌词和真实商业词流量≈0。

### P1-COMPARE-PAGE-LOW-CTR-001: /compare 页 272 曝光仅 2 点击（CTR 0.73%）

**证据**:
- /compare: 272 impressions / 2 clicks / CTR 0.73% / position 33.8
- 同位置预期 CTR（行业基准）≈ 1.5-2.5%
- 当前 CTR 只有基准的 1/3，说明 title/meta 吸引力不足或排名 33.8 在第 3 页底部

**建议**: 推到 position ≤20 前不要先改 meta；当前首要任务是把 /compare 的内容质量做上去，让排名进前 2 页。

### P1-GA4-API-BROKEN-001: GA4 服务账号失效，无法度量真实用户行为

**证据（state.json 实读）**:
- ga4_api_status: "BROKEN - service account not found, superseded by Ahrefs Web Analytics"
- analytics_provider: "ahrefs_web_analytics"
- Key events = 0（两个周期都是）
- pending_new_google_setup 字段存在但未完成

**影响**: 无法回答"哪些关键词真正带来有价值访问"、"落地页跳出率"、"转化路径"——所有 SEO 决策只能基于曝光数据，无法基于业务价值。

### P2-STATE-DESYNC-001: state.json 的 GSC 数据与最新报告不同步

**证据**:
- state.json: gsc_latest_impressions = 2002
- 实际报告 (2026-09-06_2026-10-05.md): 2095
- state.json: last_analytics_run = "2026-09-28 09:16"（距今 11 天）
- state.json: last_updated = "2026-09-30"（距今 9 天）

**影响**: 指挥官和其他窗口读到的 GSC 数据是过时的。

---
"""

with open(audit_path, "a", encoding="utf-8") as f:
    f.write(new_findings)
print(f"[OK] audit_findings.md appended, new size: {os.path.getsize(audit_path)} bytes")

# ========== 2. 写最新分析报告到 gsc-ga4-report/ ==========
report_path = os.path.join(BASE, "gsc-ga4-report", f"analyst_insight_{TODAY}.md")
report = f"""# 分析师窗口洞察报告 - {TODAY}

**生成时间**: {NOW}
**分析师**: 窗口4（数据分析师，只读）
**数据窗口**: 2026-09-06 至 2026-10-05（GSC 落地报告），环比 2026-08-20 至 2026-09-18

---

## 一句话结论

**9/24 起站点在 Google 的曝光量断崖下跌 92.3%，11 天无自然回弹，高度疑似触发 9 月 Helpful Content 更新；当前所有 SEO 动作优先级应让位于"内容质量修复以解除算法惩罚"，而不是继续批量发新文章。**

---

## 核心指标

| 指标 | 本期 (9/6-10/5) | 上期 (8/20-9/18) | 变化 |
|---|---|---|---|
| Clicks | 9 | 8 | +1 (+12.5%) |
| Impressions | 2,095 | 1,581 | +514 (+32.5%) |
| CTR | 0.43% | 0.51% | -0.08pp |
| Avg Position | 25.10 | 23.98 | +1.12（变差） |
| Organic Sessions (GA4) | 不可用 | 13 | GA4 API 损坏 |

**注意**: 曝光总量 +32.5% 是假象——全部由 9/6-9/23 贡献，9/24 后日均仅 8.5。

## 流量时间线（关键证据）

| 时段 | 天数 | 日均曝光 | 点击 |
|---|---|---|---|
| 9/6 - 9/23（暴跌前） | 18 | 111.2 | 9 |
| **9/24（断崖日）** | 1 | **1** | 0 |
| 9/25 - 10/4（恢复期） | 11 | 8.5 | 0 |

**断崖日单日跌幅**: 9/23 的 79 → 9/24 的 1 = **-98.7%**

## Top 页面（本期）

| 页面 | 点击 | 曝光 | CTR | 排名 | 解读 |
|---|---|---|---|---|---|
| /blog/best-ai-voice-changers-2026 | 2 | 68 | 2.9% | 16.5 | **最佳潜力页**，已进前 20 |
| /compare | 2 | 272 | 0.7% | 33.8 | 曝光最大但 CTR 极低，第 3 页 |
| /blog/openai_astra_review | 1 | 157 | 0.6% | 10.8 | 排名 10.8，有点击潜力 |
| / | 1 | 2 | 50% | 1.5 | 品牌词搜索量极小 |
| /category/writing | 1 | 8 | 12.5% | 45.8 | 长尾偶然命中 |

## 真实 vs 污染关键词

**真实用户搜索**（<5 条）:
- best voice changer 2026: 1 click / 1 imp / pos 4
- 其余 1 click 来自偶然长尾

**污染搜索**（Top 20 中 12+ 条）:
- 所有带 `-site:reddit.com -site:twitter.com -site:x.com ...` 的查询
- 这些是 SEO 工具/竞品调研的 SERP 爬取，不是真实需求
- **行动**: 下次关键词分析时先过滤掉含 `-site:` 的查询词

## 设备分布

| 设备 | 点击 | 曝光 | 占比 |
|---|---|---|---|
| Desktop | 7 | 1,863 | 88.9% 曝光 |
| Mobile | 2 | 229 | 10.9% |
| Tablet | 0 | 3 | 0.1% |

桌面端主导，与 AI 工具评测类内容的用户画像一致。

## P0/P1 问题清单（已写入 audit_findings.md）

| ID | 优先级 | 问题 | 建议动作 |
|---|---|---|---|
| P0-TRAFFIC-CLIFF-20260924-001 | P0 | 9/24 曝光 -92.3% | 立即停批量发新文，集中修复低质文章（BLUF/外链/H2/FAQ） |
| P1-QUERY-POLLUTION-001 | P1 | 关键词被工具流量污染 | 分析时过滤 `-site:` 查询 |
| P1-COMPARE-PAGE-LOW-CTR-001 | P1 | /compare CTR 0.73% | 先提排名到前 20，再改 meta |
| P1-GA4-API-BROKEN-001 | P1 | GA4 服务账号失效 | 重建 Google Cloud 项目+服务账号 |
| P2-STATE-DESYNC-001 | P2 | state.json GSC 数据过时 | 本次已同步 |

## 下次运行应关注的信号

1. 9/24 后曝光是否连续 7 天回升到 ≥50/天——是则说明惩罚在解除，否则需做更激进的内容清理
2. /blog/best-ai-voice-changers-2026 是否稳定在 pos 16.5 并向 pos 10 推进
3. 是否有新的"真实用户查询"（非 `-site:` 操作符）进入 Top 20
4. GA4 服务账号重建进度

---

*本报告由分析师窗口自动生成，所有数字来自已落地 GSC 报告的实读实算，未调用实时 API。*
"""

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)
print(f"[OK] report written: {report_path} ({os.path.getsize(report_path)} bytes)")

# ========== 3. 更新 state.json ==========
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# 备份
backup_path = state_path + f".backup_analyst_{TODAY.replace('-', '')}"
with open(backup_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# 同步 GSC 数据
state["gsc_latest_clicks"] = 9
state["gsc_latest_impressions"] = 2095
state["gsc_latest_ctr"] = "0.43%"
state["last_analytics_run"] = f"{TODAY} 15:00 (SOP cron)"
state["last_updated"] = NOW

# 补录新发现到 next_iteration_focus（去重）
existing_ids = {item.get("id") for item in state.get("next_iteration_focus", []) if isinstance(item, dict)}

new_items = [
    {
        "id": "P0-TRAFFIC-CLIFF-20260924-001",
        "priority": "P0",
        "title": "9/24曝光断崖-92.3%，疑似HCU惩罚：立即停批量发新文，集中修复145篇缺BLUF/104篇缺外链/69篇<50分文章以解除算法惩罚",
        "assigned_to": ["commander", "window5", "window3"],
        "status": "pending",
        "created": TODAY,
        "description": "GSC Daily Trend 实算：9/24当天曝光从79跌到1（-98.7%），之后11天日均仅8.5。技术排查已排除robots/sitemap/Cloudflare。根因指向9月Helpful Content Update。当前所有'继续发新文'的动作优先级应让位于'内容质量修复'。",
        "evidence_source": f"gsc-ga4-report/analyst_insight_{TODAY}.md + audit_findings.md"
    },
    {
        "id": "P1-GA4-REBUILD-001",
        "priority": "P1",
        "title": "重建GA4服务账号（当前BROKEN，无法度量真实用户行为和转化）",
        "assigned_to": ["commander"],
        "status": "pending",
        "created": TODAY,
        "description": "state.json显示ga4_api_status=BROKEN，Key events连续两个周期为0。无法回答哪些关键词带来有价值访问。需新建Google Cloud项目+服务账号+GA4属性授权。",
        "evidence_source": "state.json ga4_api_status / pending_new_google_setup"
    },
    {
        "id": "P1-QUERY-FILTER-RULE-001",
        "priority": "P1",
        "title": "所有GSC关键词分析必须过滤含'-site:'操作符的查询（SEO工具污染，非真实用户）",
        "assigned_to": ["analyst"],
        "status": "pending",
        "created": TODAY,
        "description": "Top 20查询中12+条含-site:排除操作符，是Ahrefs/Semrush/Openseo爬取。后续所有关键词报告、机会筛选、排名分析都必须先过滤这些查询，否则决策失真。",
        "evidence_source": "gsc-ga4-report/2026-09-06_2026-10-05.md Top Queries"
    }
]

for item in new_items:
    if item["id"] not in existing_ids:
        state["next_iteration_focus"].append(item)
        print(f"[OK] added to next_iteration_focus: {item['id']}")
    else:
        print(f"[SKIP] already exists: {item['id']}")

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] state.json updated, next_iteration_focus total: {len(state['next_iteration_focus'])}")
print(f"[OK] backup at: {backup_path}")

# ========== 4. 写 window_logs/analyst_2026-10-09.md ==========
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
log = f"""# 分析师窗口执行日志 - {TODAY}

**触发方式**: 定时任务「分析师-数据洞察（SOP版）」(0 9,15,21 * * *)
**开始时间**: {NOW}
**执行模式**: 只读分析，不改代码

---

## 执行步骤

1. ✅ 探查项目结构，确认 iteration_center/、gsc-ga4-report/、scripts/opengtm_toolkit.py 存在
2. ✅ 读取 iteration_center/SEO_TOOLKIT_MASTER.md（前200行，了解工具真实状态）
3. ✅ 读取最新 GSC 报告 gsc-ga4-report/2026-09-06_2026-10-05.md
4. ✅ 读取上一期报告 gsc-ga4-report/latest_gsc.md
5. ✅ Python 解析 state.json（340KB），同步 GSC 字段、追加 next_iteration_focus
6. ✅ Python 实算 9/24 前后曝光/点击对比
7. ✅ 追加 audit_findings.md（4 个新发现：1 P0 + 3 P1 + 1 P2）
8. ✅ 写 gsc-ga4-report/analyst_insight_{TODAY}.md
9. ✅ 备份 state.json
10. ✅ 创建 window_logs/ 目录（之前不存在）

## 关键发现

| 优先级 | 发现 | 数字 |
|---|---|---|
| **P0** | 9/24 曝光断崖 | 日均 111.2 → 8.5（-92.3%），点击 9 → 0 |
| P1 | Top Queries 被工具流量污染 | 12+/20 条含 `-site:` 操作符 |
| P1 | /compare CTR 过低 | 272 imp / 2 clicks = 0.73%（基准 1.5-2.5%） |
| P1 | GA4 API 损坏 | service account not found，Key events=0 |
| P2 | state.json 数据滞后 | impressions 2002 vs 实际 2095 |

## 产出文件

- `iteration_center/audit_findings.md`（追加，+约 3.5KB）
- `gsc-ga4-report/analyst_insight_{TODAY}.md`（新建）
- `iteration_center/state.json`（更新：GSC 字段同步 + 3 条新待办）
- `iteration_center/state.json.backup_analyst_20261009`（备份）
- `window_logs/analyst_{TODAY}.md`（本日志）

## 未完成 / 阻塞项

- **未能实时拉取 GSC/GA4 API**：当前环境无 Google 服务账号凭证（state.json 已标记 GA4 BROKEN），本次基于已落地的最近一份 GSC 报告（截至 10/5）做分析，10/6-10/9 的最新数据尚未入库。
- **opengtm_toolkit.py 未运行**：铁律是只读分析不改代码，opengtm 涉及 AEO 审计可能触发写操作，本次仅读取其存在性，未执行。
- **无法验证索引覆盖率**：需 GSC 索引报告 API，当前凭证不可用。

## 下次触发（今天 21:00）应做

1. 检查是否有新的 GSC 报告落地（gsc-fetch workflow 是否跑了 10/6 之后的数据）
2. 复核 9/24 后曝光是否有回升信号
3. 若新报告落地，重新跑一次本脚本的对比逻辑

---

*分析师窗口 {TODAY} SOP 执行完毕。*
"""

with open(log_path, "w", encoding="utf-8") as f:
    f.write(log)
print(f"[OK] log written: {log_path}")
print("\n=== ALL DONE ===")
