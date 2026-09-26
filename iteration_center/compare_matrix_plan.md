# X vs Y 对比页内容矩阵规划

> 任务ID: P1-CONTENT-COMPARE-MATRIX-001
> 创建日期: 2026-09-24
> 负责人: 窗口3
> 状态: 规划完成，待执行

## 为什么对比页优先级最高

对比页是转化率最高的内容类型（4-7%），因为读者已经在做购买决策，处于漏斗底部。
- 搜索意图：commercial investigation → transactional
- 读者已知道两个工具，在选哪个
- 联盟CTA点击率最高
- Perplexity/GEO引用友好（结构化对比表+明确推荐）

## 现有对比页盘点（15篇，含重复）

| 对比页 | 状态 | 质量评估 |
|---|---|---|
| cursor-vs-github-copilot-2026-comparison | 已发布+草稿 | 高（草稿2600+词） |
| midjourney-vs-dall-e-3-2026-comparison | 已发布+草稿（重复3次） | 中，需去重 |
| chatgpt-vs-claude-2026-comparison | 已发布+草稿（重复2次） | 中，需去重 |
| chatgpt-vs-gemini-2026-comparison | 已发布 | 中 |
| claude-vs-gemini-2026-comparison | 已发布 | 中 |
| notion-ai-vs-obsidian-ai-2026 | 草稿READY | 高（1908词） |
| dify-vs-langchain-2026 | 已发布 | 中 |
| dify-vs-coze-2026-comparison | 已发布 | 中 |
| cursor-vs-windsurf-2026 | 已发布 | 中 |
| elevenlabs-vs-playht-2026 | 草稿READY | 高 |
| elevenlabs-vs-murf-2026 | 草稿READY | 高（2645词） |
| runway-vs-pika-2026 | 草稿READY | 高 |
| best-ai-chatbots-2026 | 榜单非对比 | 归类错误 |
| best-ai-coding-tools-2026 | 榜单非对比 | 归类错误 |
| best-ai-image-generators-2026 | 榜单非对比 | 归类错误 |

**去重后实际对比页：12篇**（3篇best-of被误分类）

## 待新增对比页矩阵（按优先级）

### P0 — 高搜索量+高转化+我们有评测基础（立即写）

| # | 对比页 | 搜索意图 | 联盟潜力 | 优先级理由 |
|---|---|---|---|---|
| 1 | Jasper vs Copy.ai | 写作工具选型 | 高（两者都有联盟） | 经典对比，搜索量稳定 |
| 2 | Canva AI vs Adobe Firefly | 设计工具选型 | 高（Canva联盟+Adobe） | 我们有Canva替代方案文，内链自然 |
| 3 | Perplexity vs ChatGPT | AI搜索选型 | 中 | Perplexity是我们排名#11的工具，流量大 |
| 4 | Suno vs Udio | AI音乐选型 | 中 | 我们有Suno评测（排名#11），缺Udio |
| 5 | Surfer SEO vs Frase | SEO工具选型 | 高（SEO工具联盟佣金高） | 高佣金niche，竞争中等 |

### P1 — 中等搜索量+我们有相关内容（下一批）

| # | 对比页 | 搜索意图 | 联盟潜力 | 优先级理由 |
|---|---|---|---|---|
| 6 | Figma AI vs Canva AI | 设计工具选型 | 高 | 设计niche高转化 |
| 7 | Replit vs Cursor | AI编程选型 | 中 | 我们有Cursor评测和替代方案 |
| 8 | Leonardo AI vs Midjourney | AI图像选型 | 中 | 我们有Midjourney评测和对比页 |
| 9 | Otter AI vs Fireflies | 会议转录选型 | 高 | 生产力niche，B2B高转化 |
| 10 | Synthesia vs HeyGen | AI视频生成选型 | 高 | 我们有两者评测 |
| 11 | Tabnine vs GitHub Copilot | AI编程选型 | 中 | 我们有Copilot评测 |
| 12 | Microsoft 365 Copilot vs ChatGPT | 办公AI选型 | 中 | 我们有M365 Copilot评测 |
| 13 | Kling vs Sora | AI视频选型 | 低 | 我们有两者评测 |
| 14 | Writesonic vs Jasper | 写作工具选型 | 高 | 我们有两者评测 |
| 15 | Notion AI vs ClickUp AI | 生产力选型 | 中 | 我们有Notion AI评测 |

### P2 — 长尾+低竞争（持续补充）

| # | 对比页 | 搜索意图 |
|---|---|---|
| 16 | Zapier AI vs Make AI | 自动化选型 |
| 17 | Adobe Firefly vs DALL-E 3 | 图像选型 |
| 18 | Gemini Advanced vs ChatGPT Plus | 订阅选型 |
| 19 | Claude Pro vs ChatGPT Plus | 订阅选型 |
| 20 | Runway vs Kling | 视频选型 |
| 21 | ElevenLabs vs Play.ht | 语音选型（已有草稿） |
| 22 | Murf vs Play.ht | 语音选型 |
| 23 | Copy.ai vs Writesonic | 写作选型 |
| 24 | Frase vs Clearscope | SEO选型 |
| 25 | Dify vs Coze | 已有，需更新 |

## 对比页统一模板（高转化率结构）

每篇对比页必须包含：
1. **Quick Answer**（2-3句直接推荐，definitive无hedging）
2. **At a Glance对比表**（价格/免费额度/核心功能/适用人群/评分，5列以上）
3. **3个A vs B对比结论**（每个结论含测试数据+适用人群）
4. **A工具深度评测**（功能/定价/优缺点/真实测试数据）
5. **B工具深度评测**（同上）
6. **Head-to-Head测试**（3-5个具体任务对比，含时长/质量评分）
7. **Who Should Choose A / Who Should Choose B**（明确人群划分）
8. **Free Tier Limitation & Best Paid Alternative**（免费薅羊毛类必加）
9. **How We Tested**（测试方法+数据）
10. **FAQ 5+**
11. **Key Takeaways 3-5**
12. **内链≥3**（链向相关评测/替代方案/榜单）

## 执行节奏

- 每周写2篇P0对比页
- P0完成后转P1
- 每篇对比页发布后，在相关评测文和榜单文中加内链
- 去重：合并midjourney-vs-dalle-3的3个重复URL为1个，chatgpt-vs-claude的2个为1个

## 联盟CTA优化

- 对比页底部放2个CTA按钮："Try [A] Free" / "Try [B] Free"
- 中间正文在推荐处inline CTA
- Quick Answer后立即放推荐工具的CTA
- 对比表中价格列加"View Plans"链接
