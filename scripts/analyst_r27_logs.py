# -*- coding: utf-8 -*-
"""分析师 r27：更新日报 + 双日志 + audit_findings"""
import os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now = datetime.now().strftime('%Y-%m-%d %H:%M')

# 日报追加
rep_path = os.path.join(P, 'gsc-ga4-report', 'latest_report_2026-10-25.md')
rep = f"""
## r27 追加（{now} · 21:00 档）

### GSC 新拉取（fetch_gsc 实跑）
- Clicks 0 | Impressions 167 | CTR 0% | AvgPos 14.13（与 r26 同口径，环比持平）
- **收录纠偏（P0 完成）**：真实收录 477/905（52.8%），非 0。sitemap API indexed=0 是 GSC 口径 bug（301/308 重定向链导致）。基线见 gsc_indexed_baseline_20261025.md

### 本轮产出
| 项 | 数量 | 明细 |
|---|---|---|
| 待办执行 | 1 完成 + 2 复查 | P0-GSC-INDEXED-ZERO-REPORT 完成（产出基线）；GEO-BASELINE/ELMO 阻塞保持 |
| CTR 优化 | +3 | best-ai-coding-tools(4.1/12imp/0%)、comparison-tools/(18.0/0%)、copilot-pricing 查询(5.0/0%) |
| 竞品缺口 | +5 (P1) | portrait-generators/text-to-image/project-management/code-assistant/gift-ideas（SERP High×4/Medium×1） |
| 关键词挖掘 | +8 | 3 P0（portrait/project-mgmt/coding-assistant 全 SERP High）+ 5 P1（text-to-image/gift/3D/churn/fun） |
| focus | 245 | pending 222 → +16 |

### 关键结论
- 收录 52.8% 意味着"收录为零"不是问题；真正杠杆：discovered_not_indexed 400 条（内容质量）+ CTR/Title 优化
- GSC 点击归零下，内容 backlog 持续增长（本周 CA 15 + KW 32 + CTR 8），创作家消化节奏需关注
"""
with open(rep_path, 'a', encoding='utf-8') as f:
    f.write(rep)
print('report appended:', len(rep.encode('utf-8')), 'bytes')

# 日志 analyst（追加）
log = f"""
---

## r27 追加（{now} · 21:00 档）

- 执行待办：1 条完成（P0-GSC-INDEXED-ZERO-REPORT-20261025 → gsc_indexed_baseline_20261025.md，纠正收录=0 误判，真实 477/905=52.8%）
- 阻塞复查：2 条（GEO-BASELINE / ELMO，保持 pending）
- 新发现：16 条待办（CTR×3 + CA×5 + KW×8）
- 剩余 pending（分析师）：2（GEO-BASELINE、ELMO）
- GSC 实拉：0/167/14.13（环比持平）；收录纠偏为最大产出
- 数据源：fetch_gsc.py 实跑 + indexing_snapshot_20261012.json（AdsPower CDP 实抓）+ competitor_sitemap_cache + general_search SERP 实搜
"""
log_path = os.path.join(P, 'window_logs', 'analyst_2026-10-25.md')
with open(log_path, 'a', encoding='utf-8') as f:
    f.write(log)
print('analyst log appended')

# 日志 analyst_keyword（追加）
kwlog = f"""
---

## r27 追加（{now} · 21:00 档）

- 挖掘关键词：8 个（P0×3 / P1×5）
- SERP 验证：5 个词实搜（portrait/text-to-image/project-mgmt/code-assistant/gift，High×4/Medium×1）
- 竞品对比：futurepedia 75 分类（缓存）vs 本地 40 篇 published
- 写入待办：16 条（CTR 3 + CA 5 + KW 8）
- 硬约束：搜索量全标"预估"附依据 ✅；P0 全部 serp_verified=true ✅；与 r25/r26 无重复分类 ✅
"""
kwlog_path = os.path.join(P, 'window_logs', 'analyst_keyword_2026-10-25.md')
with open(kwlog_path, 'a', encoding='utf-8') as f:
    f.write(kwlog)
print('keyword log appended')

# audit_findings 追加（纠偏段）
audit = f"""
## {now} r27 追加 · 收录认知纠偏（P0 已闭环）

**结论**：此前"收录=0"为 GSC sitemap API 口径误判（站点存在 301/308 重定向链时 indexed 长期显示 0）。AdsPower CDP 实抓 GSC 页面得到真实基线：
- 总 URL 905 / **indexed 477（52.8%）** / not_indexed 428
- 未收录 428 分解：discovered_not_indexed 400（93.5%，最大类）、duplicate_without_canonical 9、auto_redirect 9、noindex 5、404 2、crawled_not_indexed 2、redirect_error 1
- **P0 杠杆修正**：真实问题不是"未收录"，而是 ①discovered_not_indexed 400 条指向内容质量/相关性不足 ②GSC 点击归零下的 CTR/Title 优化。sitemap 提交问题降级为 P1（canonical/重定向链修复）
- 周度跟踪：每周 AdsPower CDP 拉索引覆盖率更新 gsc_indexed_baseline 表
"""
audit_path = os.path.join(P, 'iteration_center', 'audit_findings.md')
with open(audit_path, 'a', encoding='utf-8') as f:
    f.write(audit)
print('audit_findings appended:', len(audit.encode('utf-8')), 'bytes')
