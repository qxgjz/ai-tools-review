# 指挥官周迭代报告

**日期：** 2026-09-21（周一）
**周期：** 2026-09-14 ~ 2026-09-21
**指挥官自评：** 6.5/10

---

## 一、本周做了什么

### 窗口1（改代码/技术SEO）
| 动作 | 结果 | Commit |
|------|------|--------|
| 修复31个GSC 404错误 | 15缺categorySlug + 4错误slug + 13不存在工具页 → 308重定向 | 4a429d4 |
| 修复54个页面双H1 | markdown渲染h1→h2 | eb491c6 |
| 修复canonical标签 | /blog、/blog/tag、/blog/category 全部自引用 | 82ea09a |
| 删除违规aggregateRating | 单篇评测不应有ratingCount=1 | ff358cc |
| 自托管字体 | Google Fonts → geist/font，消除外部请求 | 7a16dc4 |
| content-visibility:auto | 533个工具页folded下方 sections 延迟渲染 | ef3b56c |
| 文章JSON-LD升级 | ImageObject数组 + author统一为Research Team | 561231d |
| AI爬虫放行 | robots.ts加ChatGPT-User/Perplexity-User/Claude-SearchBot | 37240c2 |
| llms.txt扩展 | 8个分类 + 6个旗舰评测 + 免费工具指南 | 37240c2 |
| Title/meta截断修复 | 46个>60字符Title + 27个>160字符Meta Description | 6ad5d59 |
| 图片deviceSizes精简 | 8→6，减少CDN变体数 | 5be4dac |

### 窗口6（UI/UX）
| 动作 | 结果 |
|------|------|
| 全站品牌色统一 | blue/indigo/purple → emerald/teal，~30个文件清零 |
| 工具页hero加16:9真实截图 | 20个核心工具加Live screenshot区块 |
| CTA按钮标准化到48px | 符合WCAG触摸目标 |
| "No credit card required"信任信号 | AffiliateCTA按钮下方 |
| 无障碍对比度修复 | text-zinc-400 → text-zinc-500（2.8:1→4.6:1） |
| 按钮加载状态 | loading spinner + opacity-60 |
| 移动端Top3 strip | 首页hero下方 |
| color-scheme声明 | 深色模式表单控件正确渲染 |

### 窗口3（内容）
- 104/104文章完成 Quick Answer + Key Takeaways（100%覆盖）
- 发布10篇新文章（91→101→104 posts）

### 窗口4（数据分析）
- 完成21次深度学习（GSC方法、长尾词、GEO、内链、KD评分、排名追踪等）
- 建立GSC+Cloudflare+GA4三角验证框架
- 识别P0：4篇Top10文章CTR=0%

---

## 二、哪些有效（有数据支撑）

### 有效 ✅

| 动作 | 数据证据 |
|------|----------|
| **404修复 + canonical修复** | GSC曝光 908→1506（+66%，3天内），Google收录了更多页面 |
| **品牌词排名** | plandex #1.33、windsurf #4、priompt #8.82——评测页有自然排名 |
| **Top10文章** | 5篇文章进前10（stable-diffusion #5.38、dify #5.5、gemini #7.57、cursor #7.38、midjourney v7 #7.5） |
| **AI agent趋势** | /category/agent曝光 61→73（+20%），Google在给我们更多agent类曝光 |
| **技术SEO修复** | 31个404清零、54个双H1修复、canonical修复——这些是Google收录的基础 |
| **GEO布局** | robots.txt放行AI爬虫 + llms.txt结构化——为AI搜索流量铺路 |

### 无效/效果不明显 ❌

| 动作 | 数据证据 |
|------|----------|
| **Top10文章CTR=0%** | dify/stable-diffusion/cursor/gemini 4篇合计157曝光0点击。Title修改做了但Google还没重新抓取，或修改不够吸引 |
| **桌面端排名仍差** | 桌面23.16 vs 移动18.76，差距4.4名没缩小 |
| **Cloudflare流量99.9%是爬虫** | 452 UV/天中真人不到1个，说明外链/目录提交带来的都是机器人 |
| **联盟点击=0** | affiliate_clicks.md无数据，还没有用户点联盟链接 |
| **P1-004内链未做** | midjourney/cursor/elevenlabs/notion-ai入链不足问题仍在 |
| **227个孤立页面** | Ahrefs报告显示，还没系统修复 |

---

## 三、本周最大问题

1. **CTR=0%是最大浪费**：Google已经把我们排到第5-8名，但完全没人点。这是目前ROI最高的优化点——不改内容不改外链，只改Title和Meta Description。
2. **没有真实用户流量**：Cloudflare 452 UV/天中真人<1个。说明目录提交/外链带来的都是爬虫，Google自然搜索还没开始送流量（CTR 0.46%）。
3. **内链结构薄弱**：227个孤立页面 + P1-004四个核心工具页入链不足。Google爬不到所有页面。

---

## 四、本周学到的新方法（3条）

1. **排名追踪三档频率法**（第19次学习）：P0词每天追踪，P1每3天，P2每周。单日波动1-3名是噪音，连续3天同方向>3名才是真趋势。→ 落地：把GSC有曝光的~50个query加入OpenSEO rank_tracking。

2. **免费SERP难度五步法**（第20次学习）：不用付费工具，Google搜词看Top10——数小站数量、看SERP特性、判断搜索意图、决定写不写。→ 落地：keyword_opportunities.md里的候选词全部过一遍五步法。

3. **内链机会四步法**（第21次学习）：从OpenSEO拉入链<3的页面 → grep文章里未链接提及 → 建立Pillar-Cluster链接 → 新文章发布SOP。→ 落地：P1-004的执行方法。

---

## 五、下周策略调整

### 优先级重排

| 优先级 | 任务 | 分配窗口 | 理由 |
|--------|------|----------|------|
| **P0** | 重写4篇Top10文章的Title+Meta Description | 窗口1 | 157曝光0点击，ROI最高 |
| **P0** | P1-004内链：grep文章里midjourney/cursor/elevenlabs/notion提及，加链接 | 窗口1 | 第21次学习方法已就绪 |
| **P1** | /compare页面内链建设（pillar→所有tools） | 窗口1 | /compare是曝光最高页面，应该分发权重 |
| **P1** | 围绕"AI agent"写2-3篇深度文章 | 窗口3 | 趋势+20%，排名80+是低成本入场窗口 |
| **P1** | 把GSC有曝光的~50个query加入OpenSEO rank_tracking | 窗口4 | 第19次学习方法落地 |
| **P2** | 桌面端文章限宽72ch + 右侧边栏 | 窗口6 | 桌面排名差4.4名 |
| **P2** | 修复227个孤立页面（从高曝光页面加内链） | 窗口1 | Ahrefs报告 |
| **P2** | 9/24验证iteration 65的7个Title修改效果 | 窗口4 | A/B测试5步SOP |

### 砍掉/降级的方向

- **目录提交/外链建设**：Cloudflare数据显示99.9%是爬虫，带来的真人流量≈0。不再花时间提交新目录，除非有明确的dofollow外链价值。
- **截图爬取**：用户反馈"截图很多都不对"，暂停自动爬取，改为手动确认后再部署。
- **Cloudflare细分维度**：免费版GraphQL不支持，不再折腾。

### 加大投入的方向

- **Title/Meta优化**：这是目前唯一不改内容不改外链就能提升CTR的杠杆
- **内链建设**：零成本、立竿见影，第21次学习方法已就绪
- **GEO/AI搜索**：robots放行 + llms.txt已做，下一步写适合被AI引用的Quick Answer格式内容

---

## 六、各窗口下周重点

### 窗口1（改代码）
1. 重写dify/stable-diffusion/cursor/gemini 4篇文章的Title+Meta Description（加数字+年份+情绪词+CTA）
2. grep文章里midjourney/cursor/elevenlabs/notion提及，加内链到/tools/xxx
3. /compare页面加Popular Tools内链区块
4. 修复孤立页面（从/blog/index、/ranking、/category加内链）

### 窗口3（内容）
1. 写2-3篇AI agent深度文章（承接+20%趋势）
2. 新文章发布后：从2-3篇旧文章加内链 + 正文加2-3个上下文内链
3. 从keyword_opportunities.md挑绿灯词（五步法）写文章

### 窗口4（数据分析）
1. 把GSC有曝光的~50个query加入OpenSEO rank_tracking
2. 9/24验证iteration 65的Title修改效果
3. 每周一拉GSC"曝光>10、排名15-50"的关键词更新keyword_opportunities.md
4. 继续每2小时学习1个主题（已学21次）

### 窗口6（UI/UX）
1. 桌面端文章限宽72ch + 右侧边栏目录
2. 排查粉色悬浮widget来源
3. P0-UX-001确认后修复

### 窗口5（变现）
1. 等CTR提升后开始有流量再谈联盟变现
2. 检查GA4 outbound clicks事件是否正常采集

---

## 七、体系健康度评分

| 维度 | 评分(1-10) | 说明 |
|------|-----------|------|
| 技术SEO | 8 | 404/H1/canonical/structured data基本修复 |
| 内容覆盖 | 7 | 104篇文章+533工具页，Quick Answer 100%覆盖 |
| 内链结构 | 4 | 227孤立页 + 4个核心工具入链不足 |
| 流量增长 | 5 | 曝光+66%但CTR 0.46%，真人流量≈0 |
| 变现 | 2 | 0联盟点击，还没开始 |
| 数据分析 | 8 | 21次学习+GSC+Cloudflare+GA4+OpenSEO多源 |
| 自动化 | 8 | 多窗口定时任务体系稳定运行 |
| 竞品监控 | 5 | 有方法但执行不够频繁 |

**总评：6.5/10**

技术底子打好了，但"最后一公里"没打通——Google排了我们但用户不点，点了但不买。下周核心就是**提升CTR**（改Title）和**补内链**（让Google爬更深）。这两个动作做了，曝光增长才能转化为真实流量。

---

*下次周迭代：2026-09-28（周一）*
