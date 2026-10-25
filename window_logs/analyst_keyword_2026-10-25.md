# 分析师关键词挖掘日志 · 2026-10-25（r26 · 15:09 档）

## 执行结果
- 挖掘关键词：8 个（P0×3 / P1×5）
- SERP 验证：3 个（audio-generators/workflow-automation/presentation-generators，全 High）
- 竞品对比：1 站（futurepedia 75 分类实抓，topai 404）
- 写入 state.json 待办：13 条（CA×5 P1 + KW×8：3 P0 + 5 P1）
- keyword_opportunities.md 更新：2026-10-25 15:13

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
