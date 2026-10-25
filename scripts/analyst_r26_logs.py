# -*- coding: utf-8 -*-
"""分析师 r26：更新日报 + 写双日志"""
import os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now = datetime.now().strftime('%Y-%m-%d %H:%M')
today = '2026-10-25'

# 日报追加
rep_path = os.path.join(P, 'gsc-ga4-report', 'latest_report_2026-10-25.md')
rep = f"""
## r26 追加（{now} 15:09 档 · 手动触发）

### 新 GSC 拉取（fetch_gsc 实跑）
- 报告：gsc-ga4-report/2026-09-24_2026-10-23.md（新生成）
- **Clicks 0 | Impressions 167 | CTR 0% | AvgPos 14.13**（环比 09-23~10-22: clk 0/impr 167 持平；对照更早 08-12~09-23 期 impr 2001 → 大幅回落）
- 趋势判断：曝光连续走低，收录异常未恢复（sitemap submitted=0 indexed=0），真实流量继续被压制

### 本轮产出
| 项 | 数量 | 明细 |
|---|---|---|
| 待办执行 | 2 条复查 | GEO-BASELINE / ELMO 均阻塞，保持 pending+note |
| CTR 优化 | +5 | ai-coding-tools-comparison(5.5/0%)、creatium-coach(6.0/0%)、meeting-assistants(9.0/0%)、observability(9.5/0%)、productivity(10.5/0%) |
| 竞品缺口 | +5 (P1) | audio-generators/startup-assistant/workflows/presentations/image-editing（SERP 验证 High×4/Medium×1） |
| 关键词挖掘 | +8 | 3 P0（audio-generators/workflow/presentation-generators 全 SERP High）+ 5 P1 |
| 剩余 pending（分析师） | 2 | GEO-BASELINE / ELMO（阻塞） |

### 关键结论
- 页面级 CTR 目标集中在排名 5-10 但 0% 点击的 5 个页面——title/meta 优化优先级最高
- 竞品内容缺口每轮 +5，创作家 backlog 充足（本周已产出 CA 10 条 + KW 16 条）
"""
with open(rep_path, 'a', encoding='utf-8') as f:
    f.write(rep)
print('report updated:', len(rep.encode('utf-8')), 'bytes')

# 日志 analyst
log = f"""# 分析师日志 · {today}（r26 · 15:09 档）

- 执行待办：2 条复查（GEO-BASELINE / ELMO，均阻塞保持 pending）
- 新发现：5 条 CTR 优化待办（页面级，排名 5-10.5 位 CTR 0%）
- 竞品缺口：5 条（CA-* 系列，SERP 验证通过，futurepedia 1 分类 vs 我们 0）
- 关键词挖掘：8 条（KW-* 系列，3 P0 + 5 P1）
- 剩余 pending（分析师）：2（GEO-BASELINE、ELMO，均为阻塞）
- GSC 实拉：2026-09-24_2026-10-23 → clicks 0 / impr 167 / pos 14.13（环比回落，收录异常未恢复）
- 数据源：fetch_gsc.py 实跑 + live_pull_20261024_0939 + competitor_sitemap_cache（实抓）+ general_search SERP 实搜
- 环境：本地 Windows 主项目
"""
open(os.path.join(P, 'window_logs', 'analyst_2026-10-25.md'), 'w', encoding='utf-8').write(log)
print('analyst log written')

# 日志 analyst_keyword
kwlog = f"""# 分析师关键词挖掘日志 · {today}（r26 · 15:09 档）

## 执行结果
- 挖掘关键词：8 个（P0×3 / P1×5）
- SERP 验证：3 个（audio-generators/workflow-automation/presentation-generators，全 High）
- 竞品对比：1 站（futurepedia 75 分类实抓，topai 404）
- 写入 state.json 待办：13 条（CA×5 P1 + KW×8：3 P0 + 5 P1）
- keyword_opportunities.md 更新：{now}

## 步骤状态
| 步骤 | 状态 | 说明 |
|---|---|---|
| 1. 竞品 sitemap 挖词 | ✅ | competitor_gap_runner（代理 7890+UA）实抓：futurepedia 75 分类，topai 404 |
| 2. GSC Easy Wins | ⚠️ 跳过 | live_pull 排名 20-50 有曝光词 <5 个（全 0 点击低曝光） |
| 3. 关键词扩展 | ✅ | 基于 5 个新缺口分类扩展长尾（best X 2026） |
| 4. 分级 | ✅ | P0×3（SERP 验证）/ P1×5（分类缺口依据） |
| 5. SERP 验证（P0） | ✅ | 3 个 P0 + 2 个候选共 5 词实搜 |
| 6. 输出 keyword_opportunities.md | ✅ | 追加本批次，Total=8 |
| 7. 写入 state.json | ✅ | 13 条（CA 5 + KW 8） |
| 8. 日志 | ✅ | 本文件 |

## 硬约束核对
- 搜索量全部标注"预估"附依据 ✅
- P0 词全部 serp_verified=true ✅
- 数据来自实际抓取/实搜，无编造 ✅
- 与 r25 批次（art/legal/ecommerce/spreadsheet/sql/presentation/paraphrasing/design）无重复 ✅
"""
open(os.path.join(P, 'window_logs', 'analyst_keyword_2026-10-25.md'), 'w', encoding='utf-8').write(kwlog)
print('keyword log written')
