# 竞品网站分析 · 2026-10-28（r37 档）

## 数据来源
- 竞品 sitemap：**缓存 competitor_sitemap_cache.json**（cached_at 2026-10-25T15:11，实抓 futurepedia 75 分类；topai HTTP 404；本轮实抓失败=代理 7890 拒绝连接 WinError 10061）
- 本地内容：content_drafts 全量 **237 md**（含 published）
- SERP 验证：general_search 实搜 5 词（09:04）

## 竞品内容矩阵对比表
| 维度 | futurepedia | aitoolcrux |
|---|---|---|
| /ai-tools/ 分类数 | **75** | 0（工具页 533 + blog 按工具组织） |
| 内容主题 | blog + 工具分类页 | blog 评测/对比 + 目录 |
| 内容类型 | best-of/工具清单 | best/alternatives/vs |
| 变现 | 付费收录+联盟+newsletter | 联盟（规划中） |
| 更新频率 | 日更 | batch65（10-28） |

## 内容缺口清单（竞品有/本地无，25 个）
ai-detection* / automations* / chatbots★ / churn-management* / copywriting-assistant / design-generators★ / e-commerce★ / gaming* / gift-ideas* / human-resources* / legal* / misc-tools / presentations* / productivity* / project-management* / religion* / spreadsheet-assistant* / sql-assistant* / startup-assistant* / storyteller* / teachers* / text-generators★ / ticketing-management★ / transcriber* / workflows*
（★=本轮新开单；*=历史已开单，见防重复清单）

## 5 个可借鉴选题（含竞争度 + slug + SERP 验证）
| # | 选题 | 竞争度 | slug | 切入角度 |
|---|---|---|---|---|
| 1 | Best AI E-commerce Tools 2026 | **Medium** | best-ai-ecommerce-tools-2026 | 按店铺功能（产品描述/客服/邮件/推荐） |
| 2 | Best AI Text Generators 2026 | **Medium** | best-ai-text-generators-2026 | 按写作任务类型+输出质量实测 |
| 3 | Best AI Chatbot Builders 2026 | **Medium** | best-ai-chatbot-builders-2026 | 按用途（客服/电商/内容训练） |
| 4 | Best AI Design Generators 2026 | **Medium** | best-ai-design-generators-2026 | 按设计任务（海报/UI/品牌资产） |
| 5 | Best AI Ticketing Tools 2026 | **High** | best-ai-ticketing-tools-2026 | 按团队规模/预算/AI 自动化 |

## SERP 验证章节（5 词实搜，前 6-10 竞品）
1. e-commerce：Shopify(官方) / Ecommerce-Platforms / Printful / Wisepops / Rework → Medium（官方第1但独立站可排前6）
2. text-generators：HotBot / FluxGrowth / bestwriting / Manus / AI Buzz / SocialAtoZ → Medium（全独立站）
3. chatbot-builders：SiteGPT / Tidio / Chat Data / YourGPT / Toolradar / Conferbot → Medium（独立站+工具商）
4. design-generators：Digital Trends / Dreamina(CapCut) / Guideflow / Design Shifu / Kimi → Medium（混排可打）
5. ticketing：Zendesk(官方×4) / Salesforce(官方) / ONES(Freshservice) / Zoho → High（官方自营霸榜）


## r38 复核（09:3x · 代理恢复后实抓）
- **实抓成功**：requests+浏览器 UA+7890 直抓 futurepedia sitemap（200/635 URLs）→ **72 分类**（10-25 缓存为 75，差异 3 个=分类下线或 slug 变更，已按实抓更新缓存，source=live_fetch_20261028_requests_ua）
- **缺口复核**：72 分类 vs 本地 237 md → 23 个缺口，与 r37 清单一致；copywriting-assistant 与 text-generators 工具重叠不重复开；video-editing 与本地视频类内容疑似覆盖不重复开
- **结论**：r37 已开 5 个 CA（ecommerce/text-generators/chatbot-builders/design-generators/ticketing）在池未动，本轮无新缺口待办（避免待办池膨胀）
- topai.tools sitemap 持续 404（第 N 次确认，死路）
