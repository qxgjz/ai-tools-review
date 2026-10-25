# -*- coding: utf-8 -*-
"""分析师职责A：写 competitor_analysis_2026-10-25.md + 职责B keyword_opportunities 追加 + 日报更新 + 日志"""
import os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
now = datetime.now().strftime('%Y-%m-%d %H:%M')
today = '2026-10-25'

# ============ 职责A：competitor_analysis ============
ca = f"""# 竞品网站分析 · {today}

**生成时间：** {now}
**数据源：** competitor_gap_runner（代理 127.0.0.1:7890 + UA）实抓 sitemap + general_search SERP 实搜
**缓存：** iteration_center/competitor_sitemap_cache.json（cached_at=2026-10-25T12:06:35）

## 竞品内容矩阵对比
| 竞品 | 分类数(/ai-tools/) | 工具数 | 内容类型 | 变现方式 |
|---|---|---|---|---|
| futurepedia.io | **75**（sitemap 实抓） | 大量工具页 | 分类目录+工具页（无强 blog） | 目录收录+联盟 |
| topai.tools | sitemap 404（未抓到） | - | 分类目录 | 目录收录 |
| aitoolcrux.com（我们） | **0**（sitemap 无 /ai-tools/ 分类路径，结构需规范化） | 533（data/*.json）+ 243 blog 页 | blog 评测为主 | 联盟（待拓荒者执行） |

## 内容缺口清单（futurepedia 75 分类 vs 本地 blog，本轮命中 36 个缺口）
已排除 10-22/10-23/10-24 已开单分类（presentation/sql/detection/text-to-video/video-editing/paraphrasing/text-to-speech/translation/social-media/email-assistant/summarizer/music-generator/avatar-generator/website-builders/SEO-tools/transcription/note-taking/stock-trading/no-code/video-enhancer/finance/students）。

本轮新缺口（SERP 已验证 5 个）：
| 缺口分类 | 竞品数据 | 我们 | 建议选题 | SERP 竞争度 | 前 10 竞品 |
|---|---|---|---|---|---|
| art-generators | futurepedia 1 分类 | 0 分类 | best-ai-art-generators-2026 | High | TechRepublic/Dreamina(×2)/dev.to/CompareBestAI |
| e-commerce | futurepedia 1 分类 | 0 分类 | best-ai-ecommerce-tools-2026 | Medium | TechieHub/Airwallex/TrueProfit/Apify/Trendtrack |
| fitness | futurepedia 1 分类 | 0 分类 | best-ai-fitness-apps-2026 | Medium | nesyona/pontefuerteai/AIFitnessAdvisor/ultrafit360/SensAI |
| legal | futurepedia 1 分类 | 0 分类 | best-ai-legal-tools-2026 | High | scored.tools/GenieAI/Toolradar/ZeroTwo |
| teachers | futurepedia 1 分类 | 0 分类 | best-ai-tools-for-teachers-2026 | Medium | EducatorsTech/AIToolDiscovery/ZeroTwo/AIMiracle/Fello |

其余缺口（未 SERP 验证，P2 候选）：3D-generator/ai-detection/audio-editing/audio-generators/automations/business/churn-management/code-assistant/copywriting-assistant/design-generators/email-assistant/fun-tools/gift-ideas/human-resources/image-editing/misc-tools/paraphrasing/portrait-generators/presentations/religion/spreadsheet-assistant/sql-assistant/startup-assistant/storyteller/text-generators/text-to-image/ticketing-management/transcriber/workflows/writing-generators（共 31 个）

## 可借鉴选题（5 个，已 SERP 验证）
1. **Best AI Art Generators 2026**（slug: best-ai-art-generators-2026）— High — 切入：按用途矩阵（写实=Midjourney/易用=DALL-E 3/Adobe 工作流=Firefly/本地控制=SD/开源=FLUX）+ 实测样图对比
2. **Best AI Ecommerce Tools 2026**（slug: best-ai-ecommerce-tools-2026）— Medium — 切入：按电商环节分（建站=Shopify Sidekick/客服=Gorgias/邮件=Klaviyo/搜索=Algolia）+ 定价分层
3. **Best AI Fitness Apps 2026**（slug: best-ai-fitness-apps-2026）— Medium — 切入：按训练目标分（力量=Fitbod/教练=Future/自重=Freeletics/恢复=Whoop）+ 价格对比表
4. **Best AI Legal Tools 2026**（slug: best-ai-legal-tools-2026）— High — 切入：按律所规模分（大所=Harvey/中台=Lexis+ AI/起草=Spellbook/合同管理=Evisort）+ 合规/幻觉风险视角
5. **Best AI Tools for Teachers 2026**（slug: best-ai-tools-for-teachers-2026）— Medium — 切入：按教学环节分（备课=MagicSchool/写作=Khan Writing Coach/评测=AI grader）+ 免费 tier 优先

## SERP 验证章节
- 每个词用 general_search 实搜，前 10 竞品见上方表格；竞争度 High 站点含 TechRepublic/Dreamina/ZeroTwo 等权威域。
- 我们的差异化：全部采用"按任务/用例矩阵"结构（区别于竞品单维度排名），并叠加真实使用体验与定价分层。

## 待办（已写入 state.json，5 条 P1）
CA-ART-GENERATORS-20261025 / CA-ECOMMERCE-20261025 / CA-FITNESS-20261025 / CA-LEGAL-20261025 / CA-TEACHERS-20261025
"""
open(os.path.join(P, 'iteration_center', 'competitor_analysis_2026-10-25.md'), 'w', encoding='utf-8').write(ca)
print('competitor_analysis written:', len(ca.encode('utf-8')), 'bytes')

# ============ 职责B：keyword_opportunities 追加 ============
kw = f"""

---

## {today} 关键词挖掘（职责B · 与竞品分析同轮）

**生成：** {now}
**数据源：** futurepedia 75 分类 sitemap 实抓 + 5 词 SERP 实搜（general_search）
**Total keywords analyzed: 8**（P0×3 + P1×5）

### P0（SERP 已验证）
| 词 | 竞争度 | 建议标题 | slug | SERP 依据 |
|---|---|---|---|---|
| best AI art generators 2026 | High | Best AI Art Generators 2026: 8 Tested (Midjourney vs DALL-E 3 vs Adobe Firefly) | best-ai-art-generators-2026 | TechRepublic/Dreamina×2/dev.to/CompareBestAI 6 站 |
| best AI legal tools 2026 | High | Best AI Legal Tools 2026: 8 Tested (Harvey vs Lexis+ AI vs Spellbook) | best-ai-legal-tools-2026 | scored.tools/GenieAI/Toolradar/ZeroTwo 5 站 |
| best AI ecommerce tools 2026 | Medium | Best AI Ecommerce Tools 2026: 9 Tested (Shopify Sidekick vs Gorgias vs Klaviyo) | best-ai-ecommerce-tools-2026 | TechieHub/Airwallex/TrueProfit/Apify/Trendtrack 6 站 |

### P1（futurepedia 分类缺口，未 SERP 验证）
| 词 | 竞争度(估) | 建议标题 | slug |
|---|---|---|---|
| best AI spreadsheet tools 2026 | Medium | Best AI Spreadsheet Tools 2026: 8 Tested | best-ai-spreadsheet-tools-2026 |
| best AI SQL tools 2026 | Medium | Best AI SQL Tools 2026: 7 Tested | best-ai-sql-tools-2026 |
| best AI presentation tools 2026 | High | Best AI Presentation Tools 2026: 9 Tested | best-ai-presentation-tools-2026 |
| best AI paraphrasing tools 2026 | High | Best AI Paraphrasing Tools 2026: 8 Tested | best-ai-paraphrasing-tools-2026 |
| best AI design generators 2026 | Medium | Best AI Design Generators 2026: 10 Tested | best-ai-design-generators-2026 |

### 竞品对比
- futurepedia 75 分类（实抓）vs 我们 0 分类（sitemap 无 /ai-tools/ 路径）；本地 blog 243 页、tools 533。
- 本轮 P0 词全部命中"竞品有分类我们无文章"缺口，且 SERP 竞争度 High/Medium 有明确差异化空间。

### 搜索量标注（全部"预估"）
| 词 | 搜索量 | 依据 |
|---|---|---|
| best AI art generators 2026 | 预估高 | SERP 6 站竞争 High（TechRepublic/Dreamina 权威域）；艺术生成是 AI 图像最大类目 |
| best AI legal tools 2026 | 预估中高 | SERP 5 站竞争 High（含 OpenAI Astra for Law 新动态）；B2B 高客单 |
| best AI ecommerce tools 2026 | 预估高 | SERP 6 站竞争 Medium（Airwallex/TechieHub 等），电商刚需 |
| P1 五个词 | 预估中-高 | futurepedia 分类缺口依据，未实搜 |
"""
kw_path = os.path.join(P, 'iteration_center', 'keyword_opportunities.md')
open(kw_path, 'a', encoding='utf-8').write(kw)
print('keyword_opportunities appended:', len(kw.encode('utf-8')), 'bytes')
