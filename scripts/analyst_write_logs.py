# -*- coding: utf-8 -*-
"""分析师：更新日报 + 写双日志（analyst + analyst_keyword）"""
import os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now = datetime.now().strftime('%Y-%m-%d %H:%M')
today = '2026-10-25'

# 日报更新（追加今日结论）
rep_path = os.path.join(P, 'gsc-ga4-report', 'latest_report_2026-10-25.md')
rep = f"""
## 本轮执行结论（{now} 手动触发轮）

### 待办执行（5 条处理，3 条闭环）
| 待办 | 优先级 | 结果 |
|---|---|---|
| P1-AUTOCHAIN-CHECK-20261025 | P1 | ✅ 闭环：autochain-review-2026 在线且内容完整（fetch 200，~2200词），关键词消失=排名波动非页面下线 |
| CMD-20261024-002 | P1 | ✅ 中间核查：13 URL 已入抓取队列；tools/claude=not_indexed、category/video+agent=indexed；正式复查 10-31 |
| P2-INDEX-MONITOR-1026-20261025 | P2 | ✅ 预检：sitemap submitted=0/indexed=0 仍异常（vs 10-12 基线）；2/14 URL 已 indexed |
| P1-GEO-BASELINE-AUDIT-20261013 | P1 | ⚠️ 阻塞保持 pending（需浏览器跑 AI SERP） |
| P1-TOOL-ELMO-20261017 | P1 | ⚠️ 阻塞保持 pending（docker 不可用） |

### 新发现（+8 待办）
- CTR 优化 ×3（openai_astra 11.4位/0.64%、ai-coding-tools-comparison 5.5位/0%、midjourney 6.8位/0%）
- 竞品缺口 ×5（art-generators/e-commerce/fitness/legal/teachers，futurepedia 1 分类 vs 我们 0，SERP 已验证）
- 关键词挖掘 ×8（art-generators/legal/ecommerce=P0 已验证；spreadsheet/sql/presentation/paraphrasing/design-generators=P1）

### GSC 快照（live_pull_20261024_0939）
- 查询窗口 09-25→10-22：7 查询词全 0 点击；日曝光 0-5；sitemap submitted=0 indexed=0
- 与昨日一致：真实搜索流量仍被收录异常压制，索引恢复是当前唯一 P0 级杠杆
"""
with open(rep_path, 'a', encoding='utf-8') as f:
    f.write(rep)
print('report updated:', len(rep.encode('utf-8')), 'bytes')

# 日志 analyst
log = f"""# 分析师日志 · {today}（数据洞察轮）

- 执行待办：3 条闭环（AUTOCHAIN-CHECK / CMD-20261024-002 / INDEX-MONITOR）+ 2 条阻塞复查（GEO-BASELINE / ELMO）
- 新发现：3 条（CTR 优化 ×3）
- 竞品缺口：5 条（CA-* 系列，SERP 验证通过）
- 关键词挖掘：8 条（KW-* 系列，3 P0 + 5 P1）
- 剩余 pending（分析师）：2（GEO-BASELINE、ELMO，均为阻塞）
- 数据源：live_pull_20261024_0939.json（实际读取）、competitor_sitemap_cache.json（实际抓取）、general_search SERP 实搜
- 环境：本地 Windows 主项目（任务已迁移 runtime_type=2）
"""
open(os.path.join(P, 'window_logs', 'analyst_2026-10-25.md'), 'w', encoding='utf-8').write(log)
print('analyst log written')

# 日志 analyst_keyword
kwlog = f"""# 分析师关键词挖掘日志 · {today}

## 执行结果
- 挖掘关键词：8 个（P0×3 / P1×5）
- SERP 验证：3 个（art-generators/legal/ecommerce，全部 High/Medium 明确差异化）
- 竞品对比：1 站（futurepedia 75 分类实抓，topai 404）
- 写入 state.json 待办：8 条（P0×3 + P1×5，assigned=[window2,创作家]）
- keyword_opportunities.md 更新：{now}

## 步骤状态
| 步骤 | 状态 | 说明 |
|---|---|---|
| 1. 竞品 sitemap 挖词 | ✅ | competitor_gap_runner（代理 7890+UA）实抓：futurepedia 75 分类，aitoolcrux 0（结构问题），topai 404 |
| 2. GSC Easy Wins | ⚠️ 跳过 | live_pull 排名 20-50 有曝光词 <5 个（全 0 点击低曝光） |
| 3. 关键词扩展 | ✅ | 基于 5 个缺口分类扩展长尾（best X 2026） |
| 4. 分级 | ✅ | P0×3（SERP 验证）/ P1×5（分类缺口依据） |
| 5. SERP 验证（P0） | ✅ | 3 个 P0 实搜，记录前 10 竞品+竞争度 |
| 6. 输出 keyword_opportunities.md | ✅ | 追加本批次，Total=8 |
| 7. P0 写入 state.json | ✅ | 8 条 |
| 8. 日志 | ✅ | 本文件 |

## 硬约束核对
- 搜索量全部标注"预估"附依据 ✅
- P0 词全部 serp_verified=true ✅
- 数据来自实际抓取/实搜，无编造 ✅
- 与 10-14/10-22/10-23/10-24 批次词无重复（art/legal/ecommerce 为新缺口）✅
"""
open(os.path.join(P, 'window_logs', 'analyst_keyword_2026-10-25.md'), 'w', encoding='utf-8').write(kwlog)
print('keyword log written')
