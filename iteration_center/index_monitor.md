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
| P1 | /category/chatbots | 分类页 | 分类页未被GSC收录 | 从/blog文章页加内链指向 |
| P1 | /category/image-generation | 分类页 | 同 | 同上 |
| P1 | /category/video | 分类页 | 同 | 同上 |
| P1 | /category/marketing | 分类页 | 同 | 同上 |
| P1 | /tools/cursor | 工具页 | 已有/blog/cursor-ai-review文章但/tools/cursor本身无曝光 | 确保/blog文章内链指向/tools/cursor |
| P2 | /tools/gpt-4 | 工具页 | 高搜索量但无曝光 | 检查是否noindex，IndexNow提交 |
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
