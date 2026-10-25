# -*- coding: utf-8 -*-
"""合并云端 10-25 批次到本地：keyword_opportunities.md + 日志 + 报告"""
import os
from datetime import datetime

PROJ = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now = datetime.now().strftime('%Y-%m-%d %H:%M')

# 1) keyword_opportunities.md 追加 10-25 批次
kw_path = os.path.join(PROJ, 'iteration_center', 'keyword_opportunities.md')
kw_block = f"""

---

## 2026-10-25 关键词挖掘（主动版）批次【云端合并】

**Generated:** {now}
**数据源：** general_search SERP 实搜验证（竞品 sitemap 实抓失败——快照代理离线、无 zens_ink 模块，按硬约束改用 general_search 补充）+ futurepedia 74 分类（10-24 批次 sitemap 实抓记录）+ 本地 41 slug 实读
**Total keywords analyzed: 14**（P0×3 + P1×5 + P2×6）

### P0 候选（SERP 已验证）
| 词 | 竞争度 | 建议标题 | 建议 slug |
|---|---|---|---|
| best AI SEO tools 2026 | High | Best AI SEO Tools 2026: 10 Tested (Semrush vs Surfer vs Frase) — With GEO/AI-Search Angle | best-ai-seo-tools-2026 |
| best AI transcription tools 2026 | High | Best AI Transcription Tools 2026: 9 Tested (Otter vs Fireflies vs Descript) | best-ai-transcription-tools-2026 |
| best AI note taking apps 2026 | High | Best AI Note-Taking Apps 2026: 10 Compared (Notion AI vs Mem vs NotebookLM) | best-ai-note-taking-apps-2026 |

### P1 候选（竞品分类缺口，futurepedia 有我们无）
| 词 | 竞争度 | 建议标题 | 建议 slug |
|---|---|---|---|
| best AI stock trading tools 2026 | Medium | Best AI Stock Trading Tools 2026: 7 Tested (TrendSpider vs Danelfin vs Trade Ideas) | best-ai-stock-trading-tools-2026 |
| best AI no-code tools 2026 | Medium | Best AI No-Code Tools 2026: 10 Tested (Bubble vs Lovable vs Bolt) | best-ai-no-code-tools-2026 |
| best AI video enhancers 2026 | Medium | Best AI Video Enhancers 2026: 8 Tested (Topaz vs HitPaw vs CapCut) | best-ai-video-enhancer-tools-2026 |
| best AI finance tools 2026 | Medium | Best AI Finance Tools 2026: 9 Tested (for budgeting & investing) | best-ai-finance-tools-2026 |
| best AI tools for students 2026 | High | Best AI Tools for Students 2026: 12 Picks (Study Stack) | best-ai-tools-for-students-2026 |

### P2 候选
| 词 | 竞争度 | 建议标题 | 建议 slug |
|---|---|---|---|
| AI search engines 2026 | Medium | Best AI Search Engines 2026: 9 Tested (Perplexity vs SearchGPT) | best-ai-search-engines-2026 |
| AI travel planning tools 2026 | Low | Best AI Travel Planning Tools 2026: 8 Tested | best-ai-travel-planning-tools-2026 |
| AI fitness tools 2026 | Low | Best AI Fitness Tools 2026: 9 Tested (Workout + Nutrition) | best-ai-fitness-tools-2026 |
| AI tools for gaming 2026 | Low | Best AI Tools for Gamers 2026: 8 Picks | best-ai-tools-for-gamers-2026 |
| AI real estate tools 2026 | Low | Best AI Real Estate Tools 2026: 7 Tested | best-ai-real-estate-tools-2026 |
| AI sales assistant tools 2026 | Medium | Best AI Sales Assistant Tools 2026: 8 Tested | best-ai-sales-assistant-tools-2026 |

### SERP 验证（本轮 3 个 P0 实搜）
| 词 | 前 10 竞品 | 竞争度 | 我们的切入角度 |
|---|---|---|---|
| best AI SEO tools 2026 | aisotools.com, toolsolved.com, popularaitools.ai, linezine.com, xseek.io | High | 分任务矩阵（Semrush=全站/Ahrefs=外链/Surfer=内容优化）+ GEO 与 AI 搜索可见性差异化 |
| best AI transcription tools 2026 | remogrid.com, aitoolsbreakdown.com, atter-ai.com, riverside.com, hubspot.com, criticnest.com | High | 按用例分（会议=Otter/CRM=Fireflies/播客=Descript/企业=Deepgram）+ 实测准确率对比（93.4% vs 98.7%） |
| best AI note taking apps 2026 | opentoolhq.com, dev.to, zapier.com, techpresso.co, reworkcontent, pickmysoft.com | High | 按需求分（工作区=Notion/第二大脑=Mem/加密=Reflect/研究=NotebookLM/自托管=Obsidian），定价+加密双矩阵 |

### 竞品对比
- futurepedia /ai-tools/ 分类：**74 个**（10-24 批次 sitemap 实抓记录，本轮代理离线未重抓）
- aitoolcrux：本地 posts slug 41 篇实读（content_drafts/published）+ tools 533（data/*.json）
- 本轮内容缺口命中：SEO-tools / transcription / note-taking（我们 0，竞品分类有）；stock-trading / no-code / video-enhancer / finance / students（沿用 10-24 批次已列缺口，本轮开单）
- 已覆盖避免重复：email-assistant/summarizer/music-generator/avatar-generator/website-builders（CA 10-23）、presentation/sql/detection（KW 10-22）、text-to-video/video-editing/paraphrasing（KW 10-23）、text-to-speech/translation/social-media（KW 10-24）

### 搜索量标注（全部"预估"，附依据）
| 词 | 搜索量 | 依据 |
|---|---|---|
| best AI SEO tools 2026 | 预估高（SEO 从业者刚需） | SERP 实搜 5 站竞争 High；未来 10-14 发布活跃 |
| best AI transcription tools 2026 | 预估高（会议/播客刚需） | SERP 实搜 6 站竞争 High（含 HubSpot 权威站） |
| best AI note taking apps 2026 | 预估高（生产力工具刚需） | SERP 实搜 6 站竞争 High（含 Zapier/DEV） |
| best AI stock trading tools 2026 | 预估中高 | 文件 10-24 SERP 记录 6 站 Medium |
| best AI no-code tools 2026 | 预估高 | futurepedia no-code 分类我们 0 |
| best AI video enhancers 2026 | 预估中 | futurepedia video-enhancer 分类我们 0 |
| best AI finance tools 2026 | 预估中高 | futurepedia finance 分类我们 0 |
| best AI tools for students 2026 | 预估高 | futurepedia students/education 分类我们 0；本地仅 free 限定版有差异 |
"""
with open(kw_path, 'a', encoding='utf-8') as f:
    f.write(kw_block)
print('keyword_opportunities appended:', len(kw_block.encode('utf-8')), 'bytes')

# 2) 报告 latest_report_2026-10-25.md
rep_path = os.path.join(PROJ, 'gsc-ga4-report', 'latest_report_2026-10-25.md')
rep = f"""# AIToolCrux 数据日报 · 2026-10-25（云端合并版）

**数据说明**：本日报由云端快照侧 10-25 轮产出后合并回本地主项目。

## 10-25 轮核心结论
| 项目 | 结果 |
|---|---|
| GSC 查询级数据 | 23 个查询词，清洗后干净词仅 10 个（全为 agent 类低质量词，impr<40） |
| 查询级污染 | 13/23 为 -site: 过滤器垃圾查询（工具生成 site 排除式长查询）→ 已开单 P1-GSC-QUERY-DATA-GAP-20261025 |
| 页面级 CTR 命中 | 18 条命中全部闭环 → 补 3 条 CTR 待办（openai_astra www / midjourney v7 / creatium coach） |
| CTR 待办累计 | 22 条（19 页面级 + 3 查询级，全部 pending） |
| 周报趋势（08-12~09-23） | clk 2→9（连续 5 周停滞 9）；impr 681→2001（+193.8%） |
| /compare 聚合 | 2791imp / 38clk / CTR 1.36% / pos 21-26 |

## 待办（10-25 新增，已合并本地 state.json）
- 关键词轮 +8：KW-SEO-TOOLS / KW-TRANSCRIPTION / KW-NOTE-TAKING（P0，SERP High）；KW-STOCK-TRADING / KW-NO-CODE / KW-VIDEO-ENHANCER / KW-FINANCE / KW-STUDENTS（P1）
- SOP 轮 +4：CTR-BLOG-OPENAI-ASTRA-WWW / CTR-BLOG-MIDJOURNEY-V7-215236 / CTR-BLOG-CREATIUM-COACH-173022 + P1-GSC-QUERY-DATA-GAP
"""
with open(rep_path, 'w', encoding='utf-8') as f:
    f.write(rep)
print('report written:', len(rep.encode('utf-8')), 'bytes')

# 3) 日志 analyst_2026-10-25.md
log_path = os.path.join(PROJ, 'window_logs', 'analyst_2026-10-25.md')
log = f"""# 分析师日志 · 2026-10-25（云端合并版）

- 执行待办：0 条（快照侧分析师专属 pending=0）
- 新发现：1 条（P1-GSC-QUERY-DATA-GAP-20261025：查询级数据被 -site: 过滤器污染）
- CTR 优化待办：+3（openai_astra www / midjourney v7 / creatium coach）
- 页面级命中闭环：18 条全闭环 → 累计 22 条 CTR 待办
- 剩余 pending（分析师）：0（快照侧）
- 本文件为云端产物合并回本地主项目
"""
with open(log_path, 'w', encoding='utf-8') as f:
    f.write(log)
print('analyst log written:', len(log.encode('utf-8')), 'bytes')

# 4) 日志 analyst_keyword_2026-10-25.md
kwlog_path = os.path.join(PROJ, 'window_logs', 'analyst_keyword_2026-10-25.md')
kwlog = f"""# 分析师关键词挖掘日志 · {now}（云端合并版）

## 执行结果
- 挖掘关键词：14 个（P0×3 / P1×5 / P2×6）
- SERP 验证：3 个（P0 全部验证，竞争度 High×3）
- 竞品对比：1 站（futurepedia 74 分类，沿用 10-24 实抓记录）
- 写入 state.json 待办：8 条（P0×3 + P1×5，assigned=[window2,创作家]）
- keyword_opportunities.md 更新：{now}

## 步骤状态
| 步骤 | 状态 | 说明 |
|---|---|---|
| 1. 竞品 sitemap 挖词 | ⚠️ 失败降级 | 快照代理离线（127.0.0.1:7890 Connection refused）+ 无 zens_ink 模块，无法运行 competitor_gap；按硬约束改用 general_search 补充 |
| 2. GSC Easy Wins | ⚠️ 跳过 | 快照侧无 live_pull_*.json（无凭证无网络），数据不足 5 个，按规则跳过 |
| 3. 关键词扩展 | ✅ 成功 | general_search 实搜 4 个核心词扩展 |
| 4. 分级 | ✅ 成功 | P0×3 / P1×5 / P2×6 |
| 5. SERP 验证（P0） | ✅ 成功 | 3 个 P0 全部实搜，记录前 10 竞品 |
| 6. 输出 keyword_opportunities.md | ✅ 成功 | 追加 10-25 批次，Total=14 |
| 7. P0 写入 state.json | ✅ 成功 | 8 条（3 P0 + 5 P1） |
| 8. 日志 | ✅ 本文件 | |

## 硬约束核对
- 搜索量全部标注"预估"+依据 ✅
- 禁止编造：SERP 数据来自 general_search 实搜 ✅
- P0 词全部 serp_verified=true ✅
- 已覆盖避免重复：CA 10-23 / KW 10-22 / KW 10-23 / KW 10-24 全部避开 ✅
"""
with open(kwlog_path, 'w', encoding='utf-8') as f:
    f.write(kwlog)
print('keyword log written:', len(kwlog.encode('utf-8')), 'bytes')
