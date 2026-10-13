# 关键词挖掘日志 - 2026-10-09

**触发时间**: 2026-10-09T18:49:03
**任务**: 主动挖掘关键词机会

## 数据来源

- GSC API 实时拉取：20 queries, 15 pages
- 时间窗口：2026-09-09 ~ 2026-10-06（28天）
- GA4 页面表现补充

## 挖掘结果

| 分类 | 数量 |
|---|---|
| Total keywords analyzed | 20 queries + 15 pages |
| Easy Wins (pos 20-50) | 1 query + 3 page |
| 高曝光低排名 (pos > 50) | 5 |
| **P0** | **6** |
| **P1** | **6** |
| **P2** | **3** |

## P0 关键词列表

- `best ai agents 2026` → /blog/best-ai-agents-2026 (500-1000/mo (基于 ai agent 词簇 GSC 曝光推断), 竞争 Medium)
- `ai agent vs chatbot` → /blog/ai-agent-vs-chatbot-2026 (200-500/mo, 竞争 Low)
- `how to build an ai agent` → /blog/how-to-build-an-ai-agent (300-800/mo, 竞争 Low-Medium)
- `best ai comparison tools` → /blog/best-ai-comparison-tools-2026 (200-500/mo, 竞争 Low)
- `best ai voice changer for content creators` → /blog/best-ai-voice-changers-content-creators (300-800/mo, 竞争 Medium)
- `suno alternatives 2026` → /blog/suno-alternatives-2026 (500-1500/mo, 竞争 Medium)

## 写入 state.json 待办

6 条 P0 待办已写入 next_iteration_focus。

## 产出文件

- `iteration_center/keyword_opportunities.md`
- `state.json` (新增 6 条待办)
- 本日志

## 核心发现

1. "ai agent" 词簇（10 impr, pos 94.7）是最大机会，需要专门内容
2. /compare 页面（212 impr, pos 38.8）有流量基础，需优化
3. voice changers 文章（68 impr, pos 16.5）是全站最佳内容页
4. suno-alternatives（GA4 57.5% ER）值得扩写同类 alternatives


---

## 补充调研验证 - 2026-10-09T19:07:45

**用户要求**: 关键词挖掘需要经过大量调研和验证

**补充完成**:
1. SERP 竞争分析：6 个 P0 词全部用 general_search 实际搜索，记录前 10 竞品
2. 竞品抓取：futurepedia.io（sitemap 30+分类）+ topai.tools（23522工具/120分类）
3. theresanaiforthat.com 被安全策略拦截，未抓取

**关键发现**:
- best ai comparison tools 是蓝海（SERP 无专门文章）
- AI Agents 是 futurepedia + topai.tools 共同缺口
- Tool Playbooks 是 topai.tools 有但我们没有的内容类型
- 深度评测是我们的差异化优势

**更新**:
- keyword_opportunities.md 新增第七、八、九章（SERP验证+竞品对比+调研总结）
- state.json 6 条 P0 待办补充 serp_competition / serp_verified / our_angle
