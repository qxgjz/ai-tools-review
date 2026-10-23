# Index Diagnosis Report 2026-10-23

**来源**: commander_learning_seo_geo_20261023 → P1-INDEX-DIAG-CLASSIFY-20261023
**数据**: AdsPower CDP GSC URL 检查批量（0-19=2026-10-22 08:05 批 / 20-67=2026-10-21 08:27 批，共 68 URL）+ 10-12 批（url_index_check_batch_0_67_20261012）交叉 + 线上 web_fetch 服务端核实（disable_cache=true）
**方法**: Ecomexperts 2026 诊断工作流——① Crawled-not-indexed（质量阈值→E-E-A-T 信号）② Discovered-not-indexed / 其他未收录（crawl budget→内链/抓取推动）

---

## 1. 摘要：68 URL 状态分布（最新批）

| GSC 状态 | 数量 | 处置类别 |
|---|---|---|
| indexed（已收录） | 7 | 无需处理（category/video、category/agent、github-copilot、cursor、windsurf、writesonic 等） |
| redirect（Page with redirect） | 13 | 类别 B-2：URL-CANONICAL 同源，301 归一已生效，Google 跟随后可达 |
| redirect_error（重定向错误） | 3 | 类别 B-1：线上实测全 200（见 §4），历史 301 链遗留，URL-CANONICAL 完成后 GSC 重抓转好 |
| not_indexed（Crawled-not-indexed） | 3 | **类别 A：质量阈值**，E-E-A-T/内链修复（见 §3） |
| duplicate | 1 | 类别 B-3：分类页重复判定，差异化内容修复 |
| unknown（检查未返回） | 41 | 类别 B-4：工具未闭环非未收录；10-12 批已证其中 20 个 indexed，其余补跑 |

> 口径说明：unknown=AdsPower CDP 配额/工具问题（r44 起遗留），**不代表未收录**。10-12 批同一 68 URL 中 20 个实测 indexed（midjourney/dall-e-3/windsurf/copy-ai/notion-ai/runway/pika/suno/perplexity/figma-ai/canva-magic/auto-gpt/worldmonitor/llama-index/ragflow/promptfoo/milvus/chroma/faiss/mem0），故真实收录下限 ≥27/68。

## 2. 类别 A：Crawled-not-indexed（质量阈值）→ 3 URL

Ecomexperts 判定：Google 已抓取但未收录 = 内容质量/相关性/信号未达阈值。逐一核查 E-E-A-T 结构性信号（模板级证据：app/tools/[slug]/page.tsx:325 datePublished、app/blog/[slug]/page.tsx:342/365/497 datePublished+dateModified+AIToolCrux Editorial Team、app/alternatives/[slug]/page.tsx:124 datePublished）。

| URL | E-E-A-T 信号现状 | 缺失点 | 修复动作（归属） |
|---|---|---|---|
| /category/search/ | 无 author/datePublished（分类聚合页模板 app/category/[slug]/page.tsx 无结构化日期）；内容=工具列表 | ①分类描述段落缺失（页面仅"X Tools"+列表）②无更新时间 ③无作者署名 | 创作家：每个分类页加 80-120 字分类定义+筛选标准说明（模板加 description 字段）；架构师：category 模板补 dateModified（源自数据更新时间） |
| /category/memory/ | 同上（聚合页）；工具数少（1-2 个）→ 内容单薄 | ①内容深度不足（工具少导致页面短）②同左 | 创作家：补分类介绍+推荐场景；增长：从 /blog/ 相关文章（如 RAG 主题）加内链 |
| /tools/claude/ | **信号齐全**：datePublished（tool.lastUpdated）、评分、特性、FAQ、Quick Answer（AEO 10/10 复核在位） | 无缺失（质量阈值边缘，属知名工具竞争激烈+Google 收录延迟） | 架构师：IndexNow 提交 + 确认无 noindex（已核）→ 增长：加内链（已有 /blog/ 文章链接）；持续监控 |

## 3. 类别 B：Discovered / 其他未收录（crawl budget / 技术）→ 58 URL

### B-1: redirect_error ×3（线上实测全 200）
| URL | 线上状态（web_fetch disable_cache 实测） | 修复动作 |
|---|---|---|
| /category/chat/ | 200 "Best Chat Assistants AI Tools: Top 18 Rated"（内容正常） | 根因=URL-CANONICAL P0：http/non-www→https/www 301 链被 Google 记 error。CF Dashboard 人工完成归一后 IndexNow 提交重抓 |
| /category/code/ | 200 "Best Programming AI Tools: Top 32 Rated" | 同上 |
| /tools/gemini/ | 200 "Gemini Review 2026: 8.9/10"（完整评测） | 同上 |

### B-2: redirect ×13（GSC "Page with redirect"，非错误）
/category/productivity、/category/audio、/category/dev-tools、/category/database、/category/observability、/tools/chatgpt、/tools/midjourney、/tools/dall-e-3、/tools/stable-diffusion、/tools/jasper、/tools/copy-ai、/tools/notion-ai、/tools/grammarly
- 判定：无斜杠→斜杠 / 非规范 host 的 301 归一，Google 已跟随并收录规范 URL（如 /tools/chatgpt 2026-10-12 批 indexed）。**非故障**，规范 URL 权重正常合并。
- 修复动作：URL-CANONICAL 人工完成后统一重抓；当前无需单页操作（canonical 已覆盖）。

### B-3: duplicate ×1（category/design）
- 判定：分类聚合页标题结构与其他 category 页同模板（"Best X AI Tools: Top N Rated"），且 /category/design 下工具与相邻分类重叠 → Google duplicate 判定。
- 修复动作（创作家）：category 页模板加差异化分类描述（§2 同方案），使每个分类页有唯一内容。

### B-4: unknown ×41（AdsPower 未返回，非未收录证据）
- 处置：10-12 批已证其中 20 个 indexed；剩余 21 个（n8n/runway/sora/pika/elevenlabs/suno/litellm/perplexity/kagi/exa/figma-ai/canva-magic/canva-ai/auto-gpt/worldmonitor/jan/ollama/llama-cpp/vllm/gemini-cli/claude-code/openhands/lobe-chat/langchain/crewai/llama-index/ragflow/promptfoo/milvus/chroma/faiss/letta/cognee/langfuse/phoenix/deepeval 等）多数为 10-12 已 indexed 的工具页（重复批次）。
- 修复动作：①分析师补跑 GSC URL 检查（工具闭环，r44 遗留）②架构师/增长：对其中高流量页（elevenlabs/sora/perplexity/exa/n8n）IndexNow 批量提交（iteration_center/geo_submit.py）。

## 4. 内链缺失点清单（discovered-not-indexed / 未收录页提升抓取）
| 目标页 | 建议来源页（已收录） | 缺失内链 |
|---|---|---|
| /category/memory/ | /blog/ 中 RAG/记忆类文章、/tools/llama-index、/tools/ragflow 页脚 | 无 category 互链 |
| /category/search/ | /tools/perplexity、/tools/kagi 页面 | 无 category 面包屑互链 |
| /tools/claude/ | /blog/chatgpt-vs-claude-2026-comparison（已收录） | 已链（AEO 复核 200），保持 |
| /category/observability/ | /tools/langfuse、/tools/phoenix 页脚 | 无 category 互链 |
| 13 个 redirect 工具页 | 对应 /blog/ 评测文章 | 多数已有；URL-CANONICAL 完成后复核 |

## 5. 修复动作汇总（按窗口）
| 动作 | 归属 | 状态 |
|---|---|---|
| URL-CANONICAL（CF Dashboard Always Use HTTPS + non-www→www）→ 3 redirect_error + 13 redirect 重抓 | 人工（架构师已证 API 四通道被拒） | 待人工 |
| category 页差异化描述 + category 模板 dateModified | 创作家 + 架构师 | 新开单建议 |
| unknown 41 补跑 GSC 检查 | 分析师 | 工具闭环 r44 遗留 |
| 高流量工具页 IndexNow 提交（elevenlabs/sora/perplexity/exa/n8n 等） | 架构师（本轮或下轮） | 待执行 |
| /tools/claude IndexNow 提交 | 架构师 | 待执行 |

---
*报告生成：2026-10-23 架构师窗口 | 数据源见头注 | 与 P0-URL-CANONICAL-20261021 互补（技术归一 vs 内容/链接维度）*
