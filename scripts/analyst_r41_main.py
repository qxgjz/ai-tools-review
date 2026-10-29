# -*- coding: utf-8 -*-
"""r41 收尾：state 更新（SlugGuard/AFF 闭环 + P0 快照 evidence）+ 产出追加 + 双日志"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
NOW = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# ===== 1. state.json 更新 =====
sp = os.path.join(P, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    d = json.load(f)

closed = {'P1-SCRIPT-SLUG-GUARD-20261029', 'P1-AFF-PROGRAM-SCORING-20261029'}
for i in d['next_iteration_focus']:
    if i.get('id') in closed and i.get('status') == 'pending':
        i['status'] = 'completed'
        i['completed_at'] = NOW
        i['closed_by'] = 'analyst_r41'
    if i.get('id') == 'P0-GSC-SNAPSHOT-RETRY-20261029':
        i['evidence'] = (
            'r41 2026-10-29 尝试：AdsPower 在线(k1hfuvv6:63325)；sitemaps 页实抓 submitted=931(10-18提交/10-28读取成功)；'
            'AI 报告实抓 8 次曝光(8-31~10-26, suno3/gemini2/首页1/cursor1/knowledge1, 与 r38 基线持平)；'
            '旧版 /search-console/indexing 端点 404（GSC 改版，indexed/not_indexed 饼图无法从 UI 抓取，与 r33 时期对比通道失效）——完整环比待 GSC 恢复或改抓 URL 变体'
        )
with open(sp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print('state updated')

# ===== 2. audit_findings r41 段 =====
open(os.path.join(P, 'iteration_center', 'audit_findings.md'), 'a', encoding='utf-8').write("""

## r41（2026-10-29 下午档 · 分析师-数据洞察 SOP 触发）

### GSC 二次实拉（同一窗口 09-28~10-27 数据回填后）：197 imp / 0 clk / pos 13.22
| 指标 | r41 下午 | r40 早间 | 变化 |
|---|---|---|---|
| Impressions | **197** | 181 | **+16（+8.8%）** |
| Avg Position | **13.22** | 14.12 | **+0.90 位改善** |
| MOBILE | 5 imp（2.5%） | 4（2.2%） | 微升 |
- **P0 观察：同窗口两次拉取数据不同（181→197），GSC 仍在回填；回升信号加强（位次改善最显著），10-26 单日峰值后未再跌落**
- 新查询 aizolo reviews（pos 22.0 imp 1）——首个 pos20-50 区间曝光词，数量不足 5 跳过 Easy Wins

### P0: 索引快照降级实抓（AdsPower 本轮在线）
- sitemaps 页实抓：submitted=931（2026-10-18 提交 / 2026-10-28 读取成功）
- AI 报告实抓：8 次曝光（suno 3/gemini 2/首页 1/cursor 1/knowledge 1，与 r38 基线持平）
- **旧版 /search-console/indexing 端点 404（GSC 改版）**：indexed/not_indexed 饼图无法抓取 → P0-GSC-SNAPSHOT-RETRY 保持 pending，完整环比待 GSC 恢复

### P1: Slug Guard 治理闭环（新发现 4 条历史冲突待办）
- COMP-20261012-04/05、COMP-20261013-03/04 建议 slug 与 data/posts.json 已存在文章冲突
- 实核：best-ai-coding-tools-2026（09-14 已发）/ best-no-code-ai-tools-2026（同款标题已存在）/ best-ai-transcription-tools-2026（**10-29 当天已发布**）
- 处理：4 条标 completed（目标文章已存在，避免创作家重复产出），源头脚本 scripts/analyst_slug_guard.py 落地
""")

# ===== 3. keyword_opportunities r41 段 =====
open(os.path.join(P, 'iteration_center', 'keyword_opportunities.md'), 'a', encoding='utf-8').write("""

## r41（2026-10-29 下午档 · Easy Wins 复核）

- GSC 二次实拉：197 imp / pos 13.22（imp +16、位次 +0.9 改善）
- Top queries 8 条（新增 aizolo reviews pos22.0 imp1）
- **Easy Wins（pos 20-50）：1 个候选（aizolo reviews pos22），不足 5 个跳过**（SOP 阈值）
- 竞品缺口：0 新（11 个名义 GAP 全历史覆盖复核，与 r40 一致）
- Total keywords analyzed：本轮实读 8 查询 + 77 分类（竞品实抓）
""")

# ===== 4. 双日志 r41 段 =====
open(os.path.join(P, 'window_logs', 'analyst_2026-10-29.md'), 'a', encoding='utf-8').write("""

## r41（2026-10-29 下午档）

- 执行待办：**3 条闭环**（P1-SCRIPT-SLUG-GUARD completed：4 条历史 COMP slug 冲突修复+脚本落地；P1-AFF-PROGRAM-SCORING completed：8 维评分 4 工具产出；4 条 COMP 待办 slug 冲突闭环）
- P0-GSC-SNAPSHOT-RETRY：降级实抓完成（sitemaps 931 + AI 8），indexing 端点 404 死路记录，保持 pending
- 新发现：3 条（GSC 197/pos13.22 回升加强·数据回填；索引端点 404 死路；4 条历史 COMP slug 冲突）
- 挖词：0（aizolo pos22 单词不足 5 跳过）；竞品缺口 0 新；SERP 0；CTR 0 新（复核）
- 写入待办：0 条；剩余 pending：405（412-4 COMP-2 闭环-1 = 405，以脚本复核为准）
- 环境：AdsPower 在线（k1hfuvv6:63325）但 indexing 端点 404；ego-browser 不可用；fetch_gsc 二次实拉成功
""")
open(os.path.join(P, 'window_logs', 'analyst_keyword_2026-10-29.md'), 'a', encoding='utf-8').write("""

## r41 关键词挖掘（2026-10-29 下午档）

1. 竞品 sitemap 挖词：✅ 复抓 futurepedia 77 分类（11 名义 GAP 全历史覆盖，0 新）
2. GSC Easy Wins：✅ live_pull + 新报告解析；aizolo reviews pos22 唯一候选，不足 5 个跳过
3. 关键词扩展：无新核心词（缺口 0 + Easy Wins 不足），跳过
4. 分级：P0=0 / P1=0 / P2=0
5. SERP 验证：0（无 P0 候选）
6. 输出：✅ keyword_opportunities.md r41 段
7. state.json：0 条新写入（Slug Guard 修复 4 条属闭环非新增）
8. 目标产出：P0 0/3、P1 0/5（客观无新词不硬凑）
""")
print('artifacts appended')
