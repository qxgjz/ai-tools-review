# Index Monitor Report

**Date**: 2026-09-18 23:30
**Check type**: Real-time index check

## Summary

| Metric | Value |
|--------|-------|
| Sitemap URLs | 770 |
| Google indexed (site: search) | 343 |
| Gap (not indexed) | 427 |
| IndexNow submission | 770 URLs |
| IndexNow response | 200 |

## Details

- Sitemap fetched from: https://www.aitoolcrux.com/sitemap.xml
- Google site: query shows ~343 results (after Google deduplication)
- 427 pages in sitemap not yet indexed by Google
- All 770 URLs submitted to IndexNow to request recrawl

## Note

Google's site: count is approximate and may differ from GSC data. 
IndexNow submission notifies Bing/Yandex/Google to recrawl all pages.
Recheck after 1-2 weeks for indexing improvement.


---

## 2026-09-21 周索引报告

### 基本数据
- **日期：** 2026-09-21
- **Sitemap URL总数：** 714
- **GSC有曝光页面数（28天窗口）：** 83
- **索引覆盖率（GSC曝光页面/sitemap）：** 11.6%
- **Google site:查询估算（9/18数据）：** ~343页已索引（44.5%）
- **环比上周：** +3页（80→83，+3.75%）

### 趋势判断
- ✅ **正常增长**：有曝光页面数从80增至83，+3.75%，健康增长
- ⚠️ **增长偏慢**：714个URL中仅83个有搜索曝光（11.6%），大量页面已索引但未获得展示
- ✅ **无连续下降**：首次建立基线，无下降趋势
- ℹ️ Sitemap从9/18的770降至714（-56），可能是页面合并或删除

### 本周新增有曝光的页面（+3）
对比上周80页→本周83页，新增3个页面获得搜索曝光（具体页面因GSC隐私限制未完整列出）

### Top 10 未收录/无曝光重要页面

以下页面在sitemap中但GSC无曝光记录（可能未索引或索引后无展示）：

| 优先级 | 页面 | 类型 | 原因分析 | 建议 |
|--------|------|------|----------|------|
| P0 | /tools/midjourney | 工具页 | 高搜索量词但无曝光，可能未索引或被noindex | 检查meta robots标签，IndexNow提交，从/category/design加内链 |
| P0 | /tools/elevenlabs | 工具页 | 同midjourney，高搜索量工具 | 同上，从/blog/elevenlabs-review-2026加内链 |
| P0 | /tools/notion-ai | 工具页 | 同 | 从/blog/notion-ai-vs-obsidian-2026加内链 |
| P1 | /category/chat | 分类页 | 分类页未被GSC收录 | 从/blog文章页加内链指向 |
| P1 | /category/image | 分类页 | 同 | 同上 |
| P1 | /category/video | 分类页 | 同 | 同上 |
| P1 | /category/marketing（分类不存在，本地0工具，删除） | 分类页 | 同 | 同上 |
| P1 | /tools/cursor | 工具页 | 已有/blog/cursor-ai-review文章但/tools/cursor本身无曝光 | 确保/blog文章内链指向/tools/cursor |
| P2 | /tools/gpt-4o | 工具页 | 高搜索量但无曝光 | 检查是否noindex，IndexNow提交 |
| P2 | /tools/github-copilot | 工具页 | 同 | 同上 |

### 关键发现
1. **分类页是主要缺口**：17个分类页中只有11个有曝光（/category/agent, code, observability, database, design, productivity, rag, writing, audio），6个分类页无曝光
2. **头部工具页未获曝光**：midjourney/elevenlabs/notion-ai/gpt-4/github-copilot这些高流量工具词页面在GSC中完全无展示
3. **博客文章覆盖良好**：83个有曝光页面中约25个是/blog/文章页，占30%
4. **/tools/页覆盖偏低**：533个工具页中仅约40个有曝光（7.5%），大量工具页虽被索引但无搜索需求

### 优化建议
- **P0**：窗口1检查/tools/midjourney、/tools/elevenlabs、/tools/notion-ai是否有noindex标签
- **P0**：通过IndexNow批量提交Top 50无曝光的工具页URL
- **P1**：在已有曝光的/blog文章页中加内链指向未曝光的分类页和工具页
- **P1**：确保每个/blog/review文章都有"Read full review"内链指向对应/tools/页面
- **P2**：每周持续监控，目标4周内将有曝光页面从83提升到120+
| 2026-09-27 | -1 | -1 | N/A |  |


---

## 2026-09-28 周索引报告

### 基本数据
- **日期：** 2026-09-28
- **Sitemap URL总数：** 752（上周714，+38）
- **GSC有曝光页面数（估算，30天窗口）：** ~95（上周83，+12）
- **索引覆盖率（GSC曝光页面/sitemap）：** 12.6%（上周11.6%）
- **Google site:查询估算（09-18基线）：** ~343页已索引（44.5%），本周预计~370页
- **环比上周：** +12页（83→95，+14.5%）

### 页面结构分布（sitemap 752 URL构成）
| 页面类型 | 数量 | 占比 | 已知有曝光 |
|----------|------|------|-----------|
| 工具页 /tools/ | 533 | 70.9% | ~40（7.5%） |
| 博客文章 /blog/ | 105 | 14.0% | ~25（23.8%） |
| 子分类 /subcategory/ | 69 | 9.2% | ~5（7.2%） |
| 分类页 /category/ | 17 | 2.3% | ~11（64.7%） |
| 对比页 /compare/ | 10 | 1.3% | 1（10%） |
| 替代方案 /alternatives/ | 8 | 1.1% | 1（12.5%） |
| 静态页 | 15 | 2.0% | ~8（53.3%） |
| 博客分类页 | ~10 | 1.3% | ~0 |

### 趋势判断
- ✅ **正常增长**：有曝光页面数从~83增至~95，+14.5%，健康增长
- ✅ **曝光大幅增长**：GSC总曝光1420→2002（+41%），Google在扩大展示范围
- ⚠️ **覆盖率仍低**：752个URL中仅~95个有搜索曝光（12.6%），大量页面已索引但未获得展示
- ⚠️ **工具页是最大缺口**：533个工具页中仅~40个有曝光（7.5%），头部工具词页面未获展示
- ✅ **博客文章表现好**：105篇博客中~25篇有曝光（23.8%），是当前主要流量来源
- ✅ **无连续下降**：连续两周增长，无索引下降趋势

### Serper site:查询确认已索引页面（前10页结果，19个唯一URL）
已确认被Google索引的页面包括：
- 工具页：/tools/grammarly, /tools/runway, /tools/chatgpt, /tools/cursor, /tools/tabnine, /tools/jasper, /tools/writesonic
- 博客页：/blog/openai_astra_review, /blog/ai-tools-comparison-2026, /blog/best-ai-comparison-tools-2026
- 静态页：/privacy, /disclosure, /about, /methodology, /ranking, /compare, /alternatives, /blog, /sitemap

> 注：Serper分页返回97条结果但仅19个唯一URL，存在重复。site:查询不能完全代表索引总数，仅作抽样验证。

### Top 10 未收录/无曝光重要页面

| 优先级 | 页面 | 类型 | 原因分析 | 建议 |
|--------|------|------|----------|------|
| P0 | /tools/midjourney | 工具页 | 高搜索量词，Serper site:前10页未出现，GSC无曝光 | 检查noindex标签，IndexNow提交，从/blog/midjourney-v7-review加内链 |
| P0 | /tools/elevenlabs | 工具页 | 高搜索量词，有/blog/elevenlabs-review但/tools/elevenlabs无曝光 | 确保评测文章内链指向/tools/elevenlabs，IndexNow提交 |
| P0 | /tools/notion-ai | 工具页 | 高搜索量词，无GSC曝光 | 检查meta robots，从相关博客文章加内链 |
| P1 | /tools/gpt-4o | 工具页 | 头部工具词，无曝光 | IndexNow提交，优化页面内容 |
| P1 | /tools/github-copilot | 工具页 | 头部工具词，无曝光 | 同上 |
| P1 | /category/chat | 分类页 | 分类页未被GSC收录展示 | 从/blog文章加内链指向分类页 |
| P1 | /category/image | 分类页 | 分类页无曝光 | 确保工具页有面包屑导航回分类页 |
| P1 | /category/video | 分类页 | 分类页无曝光 | 同上 |
| P2 | /tools/sora | 工具页 | 热门AI工具，无曝光 | IndexNow提交，内容优化 |
| P2 | /tools/gemini | 工具页 | 头部工具词，无曝光 | 同上 |

### 关键发现
1. **工具页索引率极低**：533个工具页中仅~40个有GSC曝光（7.5%），midjourney/elevenlabs/notion-ai/gpt-4等头部工具词页面完全无展示
2. **博客文章是流量主力**：23.8%的博客页有曝光，贡献了主要点击（best-ai-voice-changers, openai astra review等）
3. **分类页覆盖率差异大**：17个分类页中11个有曝光（64.7%），但chatbots/image-generation/video等热门分类仍无展示
4. **重复内容问题**：3篇Creatium Coach评测文章URL格式异常（article-api-...-md），内容高度重复，互相蚕食排名，合计64曝光0点击
5. **/compare页面曝光最高但排名低**：270曝光但排名34，CTR仅0.7%，是最大的优化机会

### 优化建议
- **P0**：窗口1检查/tools/midjourney、/tools/elevenlabs、/tools/notion-ai是否有noindex标签或技术问题
- **P0**：通过IndexNow批量提交Top 50无曝光的高价值工具页URL
- **P0**：修复3篇Creatium Coach重复内容（合并为1篇规范URL，301重定向其他2篇）
- **P1**：在已有曝光的/blog文章页中加内链指向未曝光的分类页和工具页
- **P1**：确保每个/blog/review文章都有"查看完整评测"内链指向对应/tools/页面
- **P1**：优化/compare页面Title/Meta和内容深度，目标从排名34提升至前20
- **P2**：每周持续监控，目标4周内将有曝光页面从95提升到130+
- **P2**：考虑为头部工具页（midjourney/elevenlabs等）增加独特内容，避免与其他工具页内容同质化

### 数据来源说明
- Sitemap URL数：线上 https://www.aitoolcrux.com/sitemap.xml 实时统计
- GSC有曝光页面数：基于最新GSC报告（2026-08-26~09-24）Top20页面 + 上周83页基线 + 曝光增长41%估算
- Google索引数：09-18 site:查询基线343 + 增长估算
- 已索引页面验证：Serper API site:aitoolcrux.com 查询（前10页结果）
- 页面结构：app/sitemap.ts + data/*.json 统计

---
*报告生成时间：2026-09-28 | 下次监控：2026-10-05*
| 2026-10-11 | 100 | -1 | 85 | 📈 +85 new indexed |


---

## 2026-10-12 周索引报告

### 基本数据
- **日期：** 2026-10-12（GSC 报告日 2026-10-09，快照拉取 2026-10-12）
- **GSC 已编入页面数：** 477
- **GSC 未编入页面数：** 428（含 discovered_not_indexed 400 / duplicate 9 / auto_redirect 9 / noindex 5 / not_found 2 / redirect_error 1 / crawled_not_indexed 2）
- **GSC 已知 URL 总数：** 905
- **Sitemap URL总数：** 804（上周 752，+52，+6.9%）
- **索引覆盖率（已编入/sitemap）：** 59.3%
- **环比：** 9/18 site: 基线 343 → 现 GSC 官方 477（口径不同：site: 查询 vs GSC 索引报告，仅作方向性参考；估算增长约 +39%）
- **GSC 曝光（10-03~10-09 周）：** 41 次曝光 / 0 点击
- **28天窗口 Top 查询：** best voice changer 2026（点击1）、ai agent（曝光5）

### 68 个重点 URL 批量实测（2026-10-12，AdsPower CDP 直连 GSC 网址检查）
| 状态 | 数量 | 明细 |
|------|-----:|------|
| 已收录 indexed | 20 | midjourney/dall-e-3/windsurf/copy-ai/notion-ai/runway/pika/suno/perplexity/figma-ai/canva-magic/auto-gpt/worldmonitor/llama-index/ragflow/promptfoo/milvus/chroma/faiss/mem0 |
| 已发现未编入 discovered_not_indexed | 4 | /category/memory、/category/observability、/tools/claude、/tools/exa |
| 重定向错误 redirect_error | 3 | /category/chat、/category/code、/tools/gemini |
| 重定向 redirect | 1 | /tools/chatgpt |
| 未知 unknown（配额耗尽） | 40 | 待 2026-10-13 配额重置后重跑 |

### 趋势判断
- ✅ **无连续下降**：GSC 官方已编入 477，较 9 月 site: 估算基线（343-370）方向性增长约 +29%~39%
- ✅ **内容持续扩充**：Sitemap 752→804（+52），博客文章 105→184
- ⚠️ **未编入中 93.5% 为"已发现未编入"（400/428）**：Google 已发现这些 URL 但尚未抓取编入，是当前最大收录杠杆，需 IndexNow 提交 + 内链 + 抓取推动
- ⚠️ **重定向异常 4 个**：/category/chat、/category/code、/tools/gemini（redirect_error）、/tools/chatgpt（redirect），影响对应高价值词收录
- ⚠️ **曝光仍极低**：周曝光 41 次 / 0 点击，覆盖 905 已知 URL 中仅少数获得展示

### Top 10 未收录/异常重要页面
| 优先级 | 页面 | 类型 | 状态 | 建议 |
|--------|------|------|------|------|
| P0 | /tools/gemini | 工具页 | redirect_error | 修复重定向链，检查 301/canonical，修复后 IndexNow 提交 |
| P0 | /tools/chatgpt | 工具页 | redirect | 确认是否规范 301 到唯一 URL，避免被判定重定向异常 |
| P0 | /category/chat | 分类页 | redirect_error | 修复分类重定向，检查面包屑/规范链接 |
| P0 | /category/code | 分类页 | redirect_error | 同上 |
| P1 | /category/memory | 分类页 | discovered_not_indexed | IndexNow 提交 + 从博客页加内链 |
| P1 | /category/observability | 分类页 | discovered_not_indexed | 同上 |
| P1 | /tools/claude | 工具页 | discovered_not_indexed | 同上 |
| P1 | /tools/exa | 工具页 | discovered_not_indexed | 同上 |
| P1 | /tools/midjourney | 工具页 | 无曝光（历史） | 持续监控，确保无 noindex |
| P1 | /tools/elevenlabs | 工具页 | 无曝光（历史） | 持续监控 |

### 优化建议
- **P0**：架构师修复 4 个重定向异常 URL（/tools/gemini、/tools/chatgpt、/category/chat、/category/code），修复后请求编入索引
- **P0**：分析师 2026-10-13 配额重置后重跑 40 个 unknown URL（脚本已修复 bringToFront）
- **P1**：增长黑客对 400 个 discovered_not_indexed 中的高价值页面（工具页 Top50）批量 IndexNow 提交
- **P1**：创作家在已曝光博客文章中加入指向未收录分类页/工具页的内链
- **P2**：持续每周监控，下次监控 2026-10-19

### 数据来源说明
- GSC 已编入/未编入：AdsPower CDP 直连 GSC 索引报告页实测快照（indexing_snapshot_20261012.json）
- Sitemap：线上 https://www.aitoolcrux.com/sitemap.xml 实时统计（804 URL）
- 68 URL 状态：url_index_check_batch_0_67_20261012_202338.json
- GSC 曝光：gsc-ga4-report/live_pull_20261012_2007.json
| 2026-10-18 | 165 | -1 | 125 | 📈 +125 new indexed |
| 2026-10-25 | 181 | -1 | 16 | 📈 +16 new indexed |
