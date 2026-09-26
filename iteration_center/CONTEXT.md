# AIToolCrux Context (auto-generated)

> Generated: 2026-09-26 19:53 UTC
> This file is auto-updated by GitHub Actions (context-update.yml)

## Core Info

| Item | Value |
|------|-------|
| Website | https://www.aitoolcrux.com |
| Repo | qxgjz/ai-tools-review |
| Stack | Next.js 14 + TypeScript + Tailwind |
| Deploy | Vercel (auto from main) |

## Content Stats

| Metric | Value |
|--------|-------|
| Tools | 533 |
| Posts | 108 |
| Categories | N/A |
| Comparisons | 10 |

## Recent Posts

1. **Best Paid AI Tools Worth Buying in 2026 (No Waste of Money) | AIToolCr** (`best-paid-ai-tools-worth-buying-2026`)
2. **Dify vs LangChain 2026: Which AI App Builder | AIToolCrux** (`dify-vs-langchain-2026`)
3. **7 Best Gemini Alternatives in 2026 | AIToolCrux** (`gemini-alternatives-2026`)
4. **Cursor vs Windsurf 2026: Which AI Code Editor | AIToolCrux** (`cursor-vs-windsurf-2026`)
5. **Notion AI vs Obsidian 2026: Which Note-Taking | AIToolCrux** (`notion-ai-vs-obsidian-2026`)

## Iteration State

- Current round: 77
- Last commit: 63d2b22
- Last iteration: 2026-09-26

## Recent Iterations

- **Round ?** (6dbbeede2d4dbdc817783c7ffe948961ccd6b882): 导入 usePathname from next/navigation; 添加 isActive(href) 辅助函数（/精确匹配，其他startsWith）; 桌面端导航：active时 text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emera
- **Round ?** (9e9bfcb6, 06436f3e, 2a29c53e): 全站CTA按钮对比度修复: bg-emerald-600(3.72:1 AA失败) -> bg-emerald-700(5.15:1 AA通过); 移除CTA按钮暗色模式反效果变体 dark:bg-emerald-500 dark:hover:bg-emerald-400 (暗色模式更浅=对比度更差); 修复9处CTA hover状态: hover:bg-emerald-700(与base相同无反
- **Round ?** (19c4054acf3a9bec3d67dab311ff9979b9686799): FadeIn + ToolCard: add prefers-reduced-motion (framer-motion useReducedMotion ho; ToolCard: hover shadow-md -> shadow-lg, score numbers tabular-nums; Tool detail page: big score + 6 dimension scores t
- **Round 2026-09-26** (8364a11570c4e601e78361cde90db749e512bb9d): 修复英文站残留中文UI：首页移动端快速入口芯片改为 Quick Access + AI Chat/AI Image/AI Coding/AI Writing/A; 修复英文站残留中文UI：工具详情页主CTA信任行改为 Independently tested / Transparent scoring / No paid ; 新建 iteration_center/ux_audit.md 记录全面
- **Round 2026-09-25** (2fd76f49571d08adb0f5a97ccdeb24c79bf43715): 工具详情页主CTA下方加编辑独立信任行（✓ 编辑独立测试 · 评分透明 · 无付费排名），来源Baymard信任信号在决策点可见提升转化; 移动端首页hero下方加横向滚动快速入口芯片（热门工具/AI图像/AI编程/AI写作/AI视频/评测博客），来源NN/g可见导航发现率48% vs 汉堡21%

## GSC Data

| Metric | Value |
|--------|-------|
| Clicks | 2 |
| Impressions | 799 |
| CTR | 0.25% |
| Avg Ranking | 21.04 |
| Report | 2026-08-13_2026-09-11.md |

## Audit Findings (pending)

# 🚨 紧急数据分析报告 - 2026-09-26

## 数据快照

| 指标 | 值 | 来源 |
|------|-----|------|
| GSC周期 | 2026-08-24 ~ 2026-09-22 (28天) | GitHub latest report |
| GSC点击 | 9 | GSC |
| GSC曝光 | 1922 | GSC |
| GSC CTR | 0.47% | GSC |
| GSC平均排名 | 25.32 | GSC |
| GA4近7天用户 | 1140 | GA4 API |
| GA4近7天会话 | 1156 | GA4 API |
| GA4近7天PV | 1349 | GA4 API |
| GA4近7天互动率 | 8.1% | GA4 API |
| GA4近7天跳出率 | 91.9% | GA4 API |
| 今日GA4 | 2用户/2会话 | GA4 API |
| OpenSEO审计 | 3 critical / 12 warning / 485 info | OpenSEO MCP 9/24 |

---

## P0 紧急问题

### P0-1: GA4 Bot洪水 — 新加坡数据中心IP 95.1%会话

**数据证据**：
- 近7天1156会话中，新加坡1099会话(95.1%)，互动率仅6.3%，平均停留5秒
- 09-21单日爆发1043会话(1041用户)，互动率6.0%，是正常日(10-34)的30-100倍
- Bot流量全部来自 direct/none (1153/1156 = 99.7%)
- Bot设备：desktop 1148/1156 (99.3%)，mobile仅8会话
- 排除Bot后真实用户：约25-50会话/周（美国27会话互动率29.6%，中国22会话互动率68.2%/停留254秒）
- Bot期间(9/21)互动率6.0% vs 正常期间(9/12-9/20)互动率33-83%

**需要操作**（需管理员在GA4 Admin和Cloudflare Dashboard配置，API无法修改Admin设置）：
1. GA4 Admin → Data Streams → 更多标记设置 → 启用"排除已知机器人流量"
2. GA4创建过滤器：排除新加坡IP段（Cloudflare数据中心IP）
3. Cloudflare WAF：对来自新加坡数据中心IP的请求启用JS Challenge
4. 后续所有分析排除Singapore来源

### P0-2: 品牌词排名Top 10但0点击 — 标题/描述严重问题

**数据证据**（GSC 28天）：

| 查询词 | 曝光 | 排名 | CTR | 预期CTR(pos 5-10) |
|--------|------|------|-----|-------------------|
| priompt | 13 | 8.92 | 0% | 5-12% |
| autopr | 10 | 6.9 | 0% | 5-12% |
| creatium coach | 8 | 8.13 | 0% | 5-12% |

**诊断**：用户搜索品牌词时，我们排名第7-9位但0点击，说明：
- SERP标题/描述可能不吸引人或被Google重写
- 品牌词搜索量极小（8-13曝光/28天=约0.3-0.5次/天），统计噪声大
- 但即使如此，排名前10的品牌词应有至少1-2次点击

**行动**：检查这些品牌词在Google SERP实际显示的标题和描述，对比我们的title标签，确认是否被Google重写。

### P0-3: 评测页排名Top 10但0点击 — 标题模板问题

**数据证据**（GSC 28天，高曝光+好排名+0点击）：

| 页面 | 曝光 | 排名 | CTR | 预期CTR |
|------|------|------|-----|---------|
| /blog/dify_ai_review | 47 | 5.47 | 0% | 8-15% |
| /blog/cursor_ai_review | 46 | 6.8 | 0% | 6-12% |
| /blog/stable-diffusion-review-2026 | 51 | 8.45 | 0% | 5-10% |
| /blog/gemini_38_flash_review | 82 | 9.61 | 0% | 3-8% |
| /blog/openai_astra_review | 144 | 11.06 | 0.69% | 2-5% |

**诊断**：这些页面排名5-11但几乎0点击，结合刚学的CTR优化知识：
- 533个工具页用同一标题模板"[Tool] Review: Pricing, Pros, Cons"触发micro-boilerplate
- Google可能重写了这些页面的标题为不吸引人的版本
- titleClickSatisfaction权重9/10，低CTR会触发恶性循环

**行动**：对这5个高曝光评测页检查SERP实际标题，优化为问题式标题如"Dify AI Review 2026: Is It Worth It?"

---

## P1 重要问题

### P1-1: CTR<1%高曝光关键词（有曝光无点击）

| 查询词 | 曝光 | 排名 | CTR | 问题 |
|--------|------|------|-----|------|
| ai tool comparison | 31 | 76.9 | 0% | 排名太靠后 |
| pr agent | 23 | 83.48 | 0% | 排名太靠后 |
| ai observability tools | 16 | 84.06 | 0% | 排名太靠后 |
| ai comparison tools | 13 | 71.54 | 0% | 排名太靠后 |
| cursor ai review | 13 | 53.62 | 0% | 排名53，接近前50 |
| ai agent | 11 | 94.64 | 0% | 排名94，太远 |
| ai agent tools | 10 | 81.7 | 0% | 排名靠后 |

**分析**：大部分词排名在50-95，CTR<1%是正常的。但cursor ai review排名53.62，接近前50，有提升空间。

### P1-2: 已收录但排名差的页面

| 页面 | 曝光 | 排名 | 问题 |
|------|------|------|------|
| /compare | 258 | 34.4 | 最高曝光页，排名34需进前10 |
| /category/agent | 82 | 82.94 | 分类页排名靠后 |
| /category/code | 39 | 30.46 | 排名尚可但CTR 0% |
| /blog/best-ai-voice-changers-2026 | 63 | 15.73 

---
*Auto-generated by context-update workflow. Do not edit manually.*
