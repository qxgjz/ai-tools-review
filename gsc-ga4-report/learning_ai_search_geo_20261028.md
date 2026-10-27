# 数据学习：AI 搜索流量分析（GEO/AEO）· 2026-10-28

## 主题
AI 搜索流量分析：GSC Generative AI 报告 + GEO 测量方法论 + 2026 AIO 点击影响数据

## 权威来源（5 组）
1. Google Search Console Generative AI 报告（leadverge.io / web25.io / auspia.ai / computese.com / neuraladx.com，2026-09 实操指南）
2. Princeton GEO 论文（arXiv 2311.09735 / OpenReview NV6rn7j5p5，GEO-bench 10k 查询）
3. Proof Ledger 方法论（theanswerengine.ai，2026-06）
4. 零点击研究（SparkToro/Search Engine Land 68%；Ahrefs 减点击 58%；Pew 8%）
5. AIO 覆盖率与 CTR 影响（soedja/DemandSphere 品牌词 80%；toolsolved position-1 丢 34.5-58%；euracle share of mentions）

## 12 个知识点
1. **GSC Generative AI 报告**：2026-08-31 全站上线，统计 AI Overviews + AI Mode 印象，可按页面/国家/设备/日期拆分
2. **报告显示门槛**：AI 数据量过少时不显示该 tab（aitoolcrux 印象量小，需实测核查）
3. **Opt-out 存在**：Search generative AI control 可排除站点出 AIO/AI Mode（几天生效，不影响普通搜索排名）
4. **GA4 原生 AI 行**：traffic acquisition 自带 AI Assistant 渠道行
5. **GA4 补漏**：自定义渠道组 regex 匹配 AI 来源（GA4 会漏计 AI 工具引流）
6. **PAWC 指标**：Princeton 提出位置调整字数 = 答案中出现位置越靠前权重越高 + 引用字数贡献
7. **GEO 方法有效性**：9 种方法中引文/引语类提升可见性最高 40%，且领域依赖（同一方法不同领域效果不同）
8. **Proof Ledger**：固定 20 个买家问题，月度跑 4 引擎，记引用出现/URL/位置 = 免费可复现的 GEO 基线
9. **零点击 68%**：SparkToro 2026 初，不到 1/3 Google 搜索仍产生点击
10. **AIO 减点击 58%**：Ahrefs 30 万关键词研究（2025-12 发布）
11. **Pew 8%**：AI 框出现时用户点击有机结果仅 8%；position-1 丢 34.5%-58% 点击
12. **品牌词 AIO 激增**：2026-09 品牌词 AI Overviews 覆盖 26%→80%（三倍）；share of mentions = 品牌出现 prompts/总 prompts

## 对 AIToolCrux 的可落地结论
- GEO-BASELINE-AUDIT 阻塞项有了完整方法论：GSC Generative AI 报告（Google 侧）+ Proof Ledger 四引擎（AI 侧）双轨
- 文章层：引用权威来源+直接引语 → AI 引用可见性提升（联动现有 GEO/AEO 审计强约束）
- 监控层：GA4 AI 渠道 regex + GSC AIO 印象 = 零成本 AI 流量监控
- 数据层：AIO 印象 = 无点击也有曝光价值（当前 GSC 0 点击不代表无 AI 价值）

## 落地待办
["P1-AI-OVERVIEWS-BASELINE-20261028", "P1-GEO-PROOF-LEDGER-20261028", "P2-GA4-AI-CHANNEL-20261028", "P2-QUOTE-CITATION-GEO-20261028"]
