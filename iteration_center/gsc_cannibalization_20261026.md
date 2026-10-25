# GSC 蚕食（Cannibalization）检测报告

- 生成时间：2026-10-26 00:27
- 数据源：`gsc-ga4-report/live_pull_20261024_0939.json`（GSC 实拉，2026-09-24~10-23 窗口）
- 待办：P0-GSC-CANNIBAL-AUDIT-20261025

## 检测结果

### A. URL 变体蚕食（页面级，确定性最高）
同一页面多 URL 变体共享曝光，稀释单一 URL 的排名权重：

| URL 变体 | Impressions | Position | 判定 |
|---|---|---|---|
| http://www.aitoolcrux.com/ | 1 | 1.0 | 非规范版本 |
| https://www.aitoolcrux.com/ | 4 | 2.0 | **规范版本（保留）** |
| https://www.aitoolcrux.com/about | 7 | 3.3 | 无斜杠变体 |
| https://www.aitoolcrux.com/about/ | 2 | 1.0 | 尾部斜杠变体 |
| https://www.aitoolcrux.com/ai-policy | 1 | 8.0 | 无斜杠变体 |

首页 3 版本（http/www-无斜杠/www）+ about 2 版本 → 至少 5 组 URL 变体在蚕食曝光。全部 0 点击，权重被拆分。

### B. 主题族多页竞争（关键词级潜在蚕食）
| 关键词族 | 页面 1 | 页面 2 | 风险 |
|---|---|---|---|
| ai coding tools | /blog/best-ai-coding-tools-2026（12 imp, pos 4.1） | /blog/ai-coding-tools-comparison-2026（2 imp, pos 5.5） | 同族 2 页共享，Google 只挑一页进首页 |

### C. 异常 URL 污染（第三方导入产生）
`/blog/article-api-20260903-171438-creatium-coach-review-2025-...md` 这类含时间戳+markdown 后缀的 URL 共 4 imp，是早期批量导入遗留，占用索引预算且无 SEO 价值。

## 修复建议（按优先级）
1. **P0（架构师/窗口1）**：全站 301 规范化——http→https、www→非www（或反向）、尾部斜杠统一；`_redirects` 加规则
2. **P0（架构师/窗口1）**：`/blog/article-api-*` 系列 301 → 对应规范文章或 410，释放索引预算
3. **P1（内容/打磨师）**：best-ai-coding-tools-2026 与 ai-coding-tools-comparison-2026 二选一为主页，另一页改为差异化长尾（comparison 页做对比表、best 页做列表），内链互指明确主次
4. **P1（分析师监控）**：每周 GSC 复查 URL 变体数量，目标降至 0 组

## 验证方法
- 修复后重拉 live_pull：检查 top_pages 中 http:// / 无斜杠变体消失，曝光合并到规范 URL
- GSC URL 检查工具逐页验证 canonical
