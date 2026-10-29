# -*- coding: utf-8 -*-
"""r40 收尾：产出追加 + 日志 + state 复核（本轮 0 新待办，诚实记录）"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
today = '2026-10-29'

# ===== audit_findings 追加 =====
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write("""

## r40（2026-10-29 · 分析师-数据洞察 SOP 触发）

### GSC 实拉（fetch_gsc 2026-09-28~10-27）
| 指标 | r40 本期 | r39 修正 | 变化 |
|---|---|---|---|
| Impressions | **181** | 188 | -3.7% |
| Clicks | 0 | 0 | — |
| Avg Position | 14.12 | 13.86 | -0.26 位 |
| MOBILE | 4 imp（2.2%） | 4（2.1%） | 持平低位 |
- 断崖持续：vs 上期窗口 2015 imp，**-91.0%**（P0-EXPOSURE-CLIFF 在池）

### P1: 10-26 回升信号未延续（证伪/未确立）
- 10-26 单日 18 imp 为本窗口峰值，但 **10-27 回落至 5 imp**——单日峰值不代表走出低位，需继续观察（下轮 GSC 验证）

### P0: AdsPower 离线阻塞索引快照（本轮环境故障）
- 双 profile CDP 端口探测均 live=False（k1hfuvv6:56307 / k1fpm0ag:50787），AdsPower 浏览器进程未运行
- P0-GSC-SNAPSHOT-RETRY-20261029 无法执行，保持 pending（周度收录跟踪断档第 1 轮）；需用户启动 AdsPower 后重试；API 路线（sitemaps 404/urlInspection 403）仍为死路不复测

### 复核：CTR 候选 0 新（页面级+查询级全历史覆盖）
- 5-20 位页面：ai-tools-review-guide(10.0)/comparison-tools(18.0)/meeting-assistants(9.0)/observability(9.5)/productivity(10.5)/coding-tools(4.1)/ai-policy(8.0) 均在 r25-r39 已开单
- 查询级：tabbyml(18.0)/copilot-pricing(5.0) 已开单 completed
- **本轮 0 新 CTR 待办**，不重复开单（r31 CTR-CHECK 先例）

### P1: live_pull 数据结构纠偏
- live_pull_20261024_0939.json 真实结构 = {site, daily[], top_queries[], top_pages[], sitemap_summary}（此前记忆的 rows/keys 结构与文件不符，已修正 re-grounding 指针）
- top_queries 仅 7 条（全站查询量极低），Easy Wins pos20-50=0
""")

# ===== keyword_opportunities 追加 =====
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write("""

## r40（2026-10-29 · Easy Wins 复核档）

- GSC 实拉：181 imp / 0 clk / pos 14.12（vs r39 188/13.86，回落）
- live_pull top_queries 全量 7 条：ai-native ide(pos1)/bondai(pos89.3)/copilot pricing(pos5)/gemini langgraph(pos75)/milvus ui(pos84)/react agent(pos82)/tabbyml(pos18)
- **Easy Wins（pos 20-50 有曝光）：0 个**（top_queries 无该区间命中，诚实跳过，与 r38/r39 一致）
- 竞品缺口：0 新分类（futurepedia 77 分类 12 名义 GAP 全历史覆盖复核，与 r39 结论一致）；无新 P0/P1/P2 词
- Total keywords analyzed：本轮实读 7 查询 + 77 分类（竞品实抓）
""")

# ===== 日志 =====
open(os.path.join(P, 'window_logs', f'analyst_{today}.md'), 'a', encoding='utf-8').write("""

## r40（2026-10-29 · 分析师-数据洞察 SOP 触发）

- 执行待办：**0 条闭环**（P0-GSC-SNAPSHOT-RETRY 阻塞=AdsPower 双 profile 离线 CDP 不可用；P0-REQ13-VERIFY 未到期=11-02 才到验证窗口；GEO-BASELINE/ELMO 阻塞复核确认，**不凑数不编造**）
- 新发现：3 条（GSC 181 imp/pos14.12 回落；10-26 峰值未延续 10-27=5；live_pull 结构纠偏）
- 挖词：0 个 P0 + 0 个 P1 + 0 个 P2（Easy Wins=0、竞品缺口 0 新）
- 竞品缺口：0 个（77 分类 12 名义 GAP 全历史覆盖复核）
- SERP 验证：0 个（无新候选词）
- CTR 待办：**0 条新**（5-20 位页面+查询级全部已在 r25-r39 开单，复核不重复）
- 写入待办：0 条
- 剩余 pending：424
- 环境记录：AdsPower 离线（需用户启动后方可执行 P0 快照）；ego-browser 仍不可用（未安装）；代理 7890 正常；fetch_gsc 实拉成功
""")
open(os.path.join(P, 'window_logs', f'analyst_keyword_{today}.md'), 'a', encoding='utf-8').write("""

## r40 关键词挖掘（2026-10-29）

1. 竞品 sitemap 挖词：✅ futurepedia 实抓 77 ai-tools 分类（requests+7890，同 r39 通道）；12 名义 GAP 全覆盖核对=0 新
2. GSC Easy Wins：✅ live_pull 解析（真实结构=top_queries/top_pages），pos 20-50 有曝光词=0，跳过
3. 关键词扩展：无新核心词（竞品缺口 0 新 + Easy Wins 0），跳过
4. 分级：P0=0 / P1=0 / P2=0
5. SERP 验证：0（无 P0 候选）
6. 输出：✅ keyword_opportunities.md r40 段（7 查询清单 + Easy Wins=0）
7. state.json：0 条写入（无新 P0/CA）
8. 目标产出：P0 0/3、P1 0/5（客观无新词不硬凑，r38/r39 先例）
""")
print('appended OK')
