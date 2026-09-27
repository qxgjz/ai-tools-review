# AIToolCrux Context (auto-generated)

> Generated: 2026-09-27 20:10 UTC
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

- **Round ?** (0bb21db7): 
- **Round ?** (6dbbeede2d4dbdc817783c7ffe948961ccd6b882): 导入 usePathname from next/navigation; 添加 isActive(href) 辅助函数（/精确匹配，其他startsWith）; 桌面端导航：active时 text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emera
- **Round ?** (9e9bfcb6, 06436f3e, 2a29c53e): 全站CTA按钮对比度修复: bg-emerald-600(3.72:1 AA失败) -> bg-emerald-700(5.15:1 AA通过); 移除CTA按钮暗色模式反效果变体 dark:bg-emerald-500 dark:hover:bg-emerald-400 (暗色模式更浅=对比度更差); 修复9处CTA hover状态: hover:bg-emerald-700(与base相同无反
- **Round ?** (19c4054acf3a9bec3d67dab311ff9979b9686799): FadeIn + ToolCard: add prefers-reduced-motion (framer-motion useReducedMotion ho; ToolCard: hover shadow-md -> shadow-lg, score numbers tabular-nums; Tool detail page: big score + 6 dimension scores t
- **Round 2026-09-26** (8364a11570c4e601e78361cde90db749e512bb9d): 修复英文站残留中文UI：首页移动端快速入口芯片改为 Quick Access + AI Chat/AI Image/AI Coding/AI Writing/A; 修复英文站残留中文UI：工具详情页主CTA信任行改为 Independently tested / Transparent scoring / No paid ; 新建 iteration_center/ux_audit.md 记录全面

## GSC Data

| Metric | Value |
|--------|-------|
| Clicks | 7 |
| Impressions | 1506 |
| CTR | 0.46% |
| Avg Ranking | 23.87 |
| Report | prev_gsc.md |

## Audit Findings (pending)


---

## OpenSEO全站审计对比 — 2026-09-27 (auditId: fe647625-f39c-44da-8cd5-8d5a16e67d54)

### 审计摘要对比

| 指标 | 本次(9/27) | 上次(9/26) | 变化 |
|------|-----------|-----------|------|
| Critical | **23** | 0 | **↑23 新增** |
| Warning | 153 | 135 | ↑18 |
| Info | 324(返回上限500) | 365 | ↓41 |
| 总问题类型 | 10种 | 8种 | +2 |

### P0 - Critical: 23个断链（新增，上次0个）

**根因**: 20个页面返回404，被9个博客页内部链接引用。存在URL路径不一致（根路径vs /blog/路径）。

**404目标URL清单（20个）**:
1. `/best-ai-coding-tools-2026` (根路径404，但/blog/版本存在)
2. `/best-ai-content-creation-tools-2026`
3. `/best-ai-email-tools-2026`
4. `/best-ai-image-generators-2026`
5. `/best-ai-note-taking-tools-2026`
6. `/best-ai-productivity-tools-2026`
7. `/best-ai-seo-tools-2026`
8. `/canva-ai-vs-adobe-firefly-2026-comparison` (根路径404)
9. `/cursor-vs-github-copilot-2026`
10. `/cursor-vs-github-copilot-2026-comparison`
11. `/how-to-use-cursor-for-react-development`
12. `/jasper-vs-copy-ai-2026-comparison`
13. `/midjourney-vs-dall-e-3-2026-comparison`
14. `/notion-ai-vs-obsidian-2026`
15. `/blog/ai-tools-for-content-creation`
16. `/blog/best-ai-animation-tools-2026`
17. `/blog/elevenlabs-vs-murf-2026`
18. `/blog/perplexity-vs-chatgpt-2026`
19. `/blog/runway-vs-pika-vs-sora`
20. `/blog/suno-vs-udio-2026`

**含断链的源页面（9个）**:
- /blog/best-ai-scheduling-tools-2026 (4个断链)
- /blog/surfer-seo-vs-frase-2026-comparison (4个断链)
- /blog/best-ai-slack-bots-2026 (3个断链)
- /blog/best-ai-video-generators-2026 (3个断链)
- /blog/canva-ai-vs-adobe-firefly-2026-comparison (3个断链)
- /blog/github-copilot-review-2026 (2个断链)
- /blog/best-ai-podcast-tools-2026 (2个断链)
- /blog/best-ai-translation-tools-2026 (1个断链)
- /blog/best-ai-idea-generators-2026 (1个断链)

**行动建议**: 
1. 立即为20个404页面设置301重定向到正确的/blog/版本或相关分类页
2. 修复9个源页面中的内部链接，指向正确URL
3. 检查URL路由规则：根路径best-ai-*和comparison页应重定向到/blog/对应页

### P1 - Warning: 121个页面缺少H1（↑1）

主要集中在博客文章页，包括5个article-api-*自动生成页面（URL格式异常）。
**行动建议**: 窗口3在批量生成内容时确保H1标签正确输出；修复article-api-*页面的URL slug。

### P1 - Warning: 10个薄内容分类页（↑2）

全部为/blog/category/*和/subcategory/*页面，字数仅138-148词。
**行动建议**: 为分类页添加描述性介绍文字（≥300词），或设置noindex。

### P2 - Info: 582个标题层级跳跃（↑27）

全站系统性问题，H1直接跳到H3。
**行动建议**: 模板层面修复，确保H2→H3层级正确。

### 正面变化
- slow-response: 13→1（服务器性能改善）
- noindex-page: 17（稳定）
- canonicalized-page: 15（稳定，搜索页正确canonicalize）

### GSC交叉验证
- 404页面中 `/best-ai-image-generators-2026` 在GSC中有63曝光/2点击（CTR 3.17%）→ 该页面曾有流量，404会导致排名丢失
- `/blog/best-ai-voice-changers-2026` 排名16.47但不在404列表 → 正常
- 建议优先恢复有GSC曝光的404页面



---

# 🔴 2026-09-27 数据分析异常发现（窗口4完整分析轮）

**分析时间**: 2026-09-27 21:45 CST
**数据来源**: GA4 API(近7天) + GSC(8/26-9/24) + Cloudflare(24h) + zens-ink(美国Top20)

---

## P0 异常

### P0-1: 新加坡Bot流量仍占97.5%，数据污染持续
- **严重度**: 🔴 P0 紧急
- **数据**: 新加坡1097用户/1099会话，占总用户97.5%，互动率6.2%，停留5秒
- **趋势**: 从上轮96.1%略升至97.5%，Bot洪水未消退
- **影响**: 所有GA4指标（互动率/停留/跳出率）被Bot严重扭曲，无法判断真实用户行为
- **建议**: 
  1. 立即在GA4 Admin中创建Bot过滤规则（排除新加坡数据中心IP段）
  2. 在Cloudflare中添加新加坡数据中心IP的WAF规则或JS Challenge
  3. 创建"排除Bot"分段，所有报告默认使用该分段
- **关联任务**: P0-GA4-BOT-FILTER-001 (pending，需用户手动操作GA4 Admin)

### P0-2: 4个高排名页面零点击，CTR严重异常
- **严重度

---
*Auto-generated by context-update workflow. Do not edit manually.*
