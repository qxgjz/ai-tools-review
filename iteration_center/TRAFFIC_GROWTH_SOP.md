# AI工具站快速起流量标准化SOP（v1.0）

> 本文档是所有窗口必须严格遵守的执行标准。任何偏离本文档的操作都必须先报告指挥官。
> 最后更新：2026-09-28
> 目标：24周内GSC月点击从9→10000+

---

## 0. 全局铁律（所有窗口必须遵守）

### 0.1 JSON解析铁律
- ❌ 绝对禁止用PowerShell的`ConvertFrom-Json`解析任何JSON文件
- ✅ 所有JSON必须用Python解析：`python -c "import json; data=json.load(open(r'路径','r',encoding='utf-8')); ..."`
- 大文件（tools.json 7.86MB）必须写.py文件执行，禁止用`python -c`一行命令

### 0.2 发现问题必须写待办
- 发现任何问题/机会，**必须**写入`iteration_center/state.json`的`next_iteration_focus`
- 格式：`{"task":"描述","assigned_to":"窗口X","priority":"P0/P1/P2","source":"来源文件","created_at":"日期"}`
- ❌ 禁止只写知识库不写待办——各窗口主任务只读state.json待办

### 0.3 定时任务能做的必须做完
- 每次定时任务触发，能在本次完成的必须完成，不许留到下次
- 干完一个任务立刻读下一个，不要停
- 最后写一条总结：本次干了几个、还剩几个

### 0.4 指挥官不直接改代码
- 指挥官只做：发现机会、分配任务、协调资源、自我进化
- 紧急问题（网站打不开、CI全红）例外，但必须事后记录

### 0.5 Git操作规范
- 代理：`http://127.0.0.1:7890`
- push前必须`git pull --rebase`
- 禁止force push
- commit message格式：`type(scope): 描述`，如`feat(content): add ChatGPT vs Claude comparison`

---

## 1. 战略方向（什么内容能快速起流量）

### 1.1 内容优先级金字塔

| 层级 | 占比 | 内容类型 | 月搜索量 | 竞争度 | 转化率 | 我们的状态 |
|------|------|---------|---------|--------|--------|-----------|
| 塔尖 | 10% | 大品牌评测（ChatGPT review） | 5万+ | 极高 | 20-35% | ❌ 几乎没有 |
| 塔身 | 30% | 对比页+场景指南 | 3000-5万 | 中 | 18-25% | ❌ 只有泛/compare |
| 塔基 | 60% | 长尾词（for students/free alternative） | 500-3000 | 低 | 15-22% | ⚠️ 有但方向偏 |

### 1.2 立即停止做的事
- ❌ 停止写月搜<500的纯小众工具评测（priompt、autopr、creatium等）
- ❌ 停止用article-api-xxx格式的URL
- ❌ 停止每天发低质量新文，改为每周3-5篇高质量
- ❌ 停止写"AI正在改变世界"类开头废话

### 1.3 必须集中做的事
- ✅ 大品牌对比页：ChatGPT vs Claude、Midjourney vs Flux等
- ✅ 大品牌评测：ChatGPT review 2026、Claude review等
- ✅ 场景指南：Best AI tools for coding/students/writers
- ✅ 免费替代：Best free AI image generator no signup
- ✅ 定价/值不值：Is ChatGPT worth it、ChatGPT pricing 2026

---

## 2. 关键词分析标准（窗口4负责）

### 2.1 关键词挖掘流程

#### Step 1：种子词列表（固定，每次扩展用）
```
大品牌：ChatGPT, Claude, Gemini, Midjourney, Grammarly, Cursor, 
        Dify, Stable Diffusion, DeepSeek, Perplexity, Jasper, Notion AI
品类词：AI chatbot, AI image generator, AI coding tool, AI writer,
        AI video generator, AI audio tool, AI agent
场景词：for students, for coding, for writers, for marketing, for designers,
        for real estate, for beginners, for business
意图词：vs, alternative, free alternative, review, pricing, worth it,
        best, top, comparison
```

#### Step 2：AI扩展指令（直接复制）
```
你是SEO关键词专家。基于以下种子词，为aitoolcrux.com扩展关键词。

种子词：[粘贴上面的列表]

扩展规则：
1. 组合公式：{大品牌} + {意图词} + {场景词}，如"ChatGPT vs Claude for students"
2. 每个大品牌生成8-10个变体
3. 每个品类词生成5-8个场景变体
4. 对每个词评估：
   - 搜索量级别：高(>10K)/中(1K-10K)/低(<1K)
   - 竞争度：搜索该词看前10名，全DR70+=高，有中小站=中低
   - 商业意图：高(vs/alternative/pricing/worth it)/中(best/guide)/低(what is)
5. 只保留商业意图中高的词
6. 输出Markdown表格，按搜索量×商业意图排序

输出格式：
| 关键词 | 搜索量级别 | 竞争度 | 商业意图 | 内容类型 | 优先级 | 所属集群 |
```

#### Step 3：竞争度验证（必须做，不能只靠AI猜）
对每个P0/P1词，手动搜索验证：
- 前10名中是否有DR<50的站？有→能打
- 前10名是否全是官方+维基+巨头？是→放弃或改长尾
- 是否有AI Overview占用？有→需要GEO优化
- 搜索结果是否有对比页/列表页？有→说明用户要这种内容

#### Step 4：输出文件
- 写入`iteration_center/keyword_pyramid.md`
- 同时写入`state.json`的`next_iteration_focus`，分配给窗口3

### 2.2 关键词质量标准
- ✅ 月搜>500（塔基）或>3000（塔身）
- ✅ 前10名有至少1个DR<60的站
- ✅ 商业意图中高
- ✅ 与AI工具品类相关
- ❌ 月搜<100（除非是零搜索量但高意图的对话式查询）
- ❌ 前10全是DR80+巨头
- ❌ 与我们网站主题无关

---

## 3. 内容集群标准（窗口3+窗口4协同）

### 3.1 集群结构定义

每个集群必须包含：
```
Pillar页（1篇，3000-5000字）：
  标题：Best {Category} 2026: {Benefit}
  内容：品类概述+Top10工具对比表+分场景推荐+FAQ+购买建议
  内链：链向所有支撑文

支撑文（10-15篇，每篇2000-3500字）：
  类型A：单工具评测（{Tool} Review 2026）
  类型B：对比页（{Tool} vs {Tool} 2026）
  类型C：场景指南（Best {Category} for {Use Case}）
  类型D：替代方案（{Tool} Alternative: 10 Best Options）
  每篇支撑文必须链回Pillar页+链向2-3篇相关支撑文
```

### 3.2 我们的8个集群规划

| 集群ID | 集群名 | Pillar关键词 | 支撑文数 | 优先级 |
|--------|--------|-------------|---------|--------|
| C1 | AI聊天机器人 | Best AI Chatbots 2026 | 12 | P0 |
| C2 | AI图片生成 | Best AI Image Generators | 10 | P0 |
| C3 | AI编程工具 | Best AI Coding Tools 2026 | 10 | P0 |
| C4 | AI写作工具 | Best AI Writing Tools | 8 | P1 |
| C5 | AI视频生成 | Best AI Video Generators | 8 | P1 |
| C6 | AI音频工具 | Best AI Audio Tools | 6 | P1 |
| C7 | AI Agent | Best AI Agents 2026 | 6 | P1（搜索量+450%） |
| C8 | 对比中心 | AI Tool Comparisons | 15 | P0 |

### 3.3 集群规划AI指令
```
为以下Pillar页规划完整内容集群：

Pillar关键词：[填入]
月搜索量：[填入]
所属集群：[填入]

输出：
1. Pillar页完整大纲（H2/H3，必须含：对比表、分场景推荐、FAQ、购买建议）
2. 10-15篇支撑文清单（每篇：标题格式、目标关键词、搜索量级别、内容类型）
3. 发布顺序（先发哪3篇长尾低竞争→再发哪几篇中等→最后Pillar）
4. 内链结构（每篇链向哪几篇，锚文本用什么）
5. 每篇的联盟链接策略（推荐哪个工具、放在什么位置）
```

---

## 4. 文章写作标准（窗口3负责，零出错）

### 4.1 标准化Brief模板（每篇文章必须先生成Brief）

```markdown
## 文章Brief
- 目标关键词：[关键词]
- 搜索量级别：[高/中/低]
- 内容类型：[对比页/评测/场景指南/列表/替代方案]
- 所属集群：[集群ID]
- 发布顺序：[第N篇]
- 标题：[含关键词+年份+数字/结论，<60字符]
- Meta description：[150字，含关键词+CTA]
- 文章结构：[H2/H3大纲]
- 开头Quick Answer：[前3行必须给出的明确答案，280-320字符]
- 对比表格字段：[价格/免费额度/强项/弱项/最适合谁/评分]
- FAQ：[5-8个，从PAA提取，每个第一句直接回答]
- 内链：[链向哪3-5篇已有文章，锚文本]
- 联盟链接：[推荐哪个工具，放在对比表+结尾，共2处]
- 需要截图：[哪3个界面，具体到哪个功能页]
- 字数目标：[2500-3500]
- 工具数据来源：[从tools.json提取哪些工具的真实数据]
```

### 4.2 文章结构标准（按内容类型）

#### 类型A：对比页（X vs Y）
```
H1: X vs Y 2026: Which [Category] Is Best? [Tested]
[Quick Answer - 280-320字符，直接给购买建议]
H2: Key Takeaways（3-5条，每条1句）
H2: X vs Y: Comparison Table（含：价格/免费额度/核心功能/强项/弱项/最适合谁/评分）
H2: X Overview（功能+定价+优缺点）
H2: Y Overview（功能+定价+优缺点）
H2: 3 Key Differences（每个差异：场景+测试数据+适用人群）
H2: Who Should Choose X?（分场景：学生/程序员/写作者/设计师）
H2: Who Should Choose Y?
H2: Who Should Look Elsewhere?（诚实说谁不适合）
H2: How We Tested（测试时长/硬件/样本量/评分维度）
H2: FAQ（5-8个，从PAA提取）
H2: Final Verdict（明确结论+联盟链接）
[Last updated行]
```

#### 类型B：单工具评测
```
H1: {Tool} Review 2026: {Benefit}
[Quick Answer - 直接回答"值不值得用"]
H2: Key Takeaways
H2: What Is {Tool}?（1段）
H2: Key Features（5-8个，每个含截图）
H2: Pricing（真实成本计算：年付总价/每用户成本/免费版能做什么）
H2: Pros and Cons（各5条，诚实）
H2: Who Is {Tool} Best For?（分场景）
H2: Who Should Look Elsewhere?
H2: {Tool} vs {Competitor}（简要对比，链向对比页）
H2: How We Tested
H2: FAQ
H2: Final Verdict（明确推荐+联盟链接）
[Last updated行]
```

#### 类型C：场景指南（Best X for Y）
```
H1: Best {Category} for {Use Case} in 2026
[Quick Answer - 直接推荐Top3]
H2: Key Takeaways
H2: Our Top Picks（3-5个工具，每个：简介+为什么适合这个场景+价格+优缺点）
H2: Comparison Table
H2: How to Choose（这个场景的用户最该看什么）
H2: FAQ
H2: Final Recommendation（分预算/分需求推荐）
[Last updated行]
```

#### 类型D：替代方案（X Alternative）
```
H1: Best {Tool} Alternatives in 2026 (Free & Paid)
[Quick Answer - 直接说Top3替代]
H2: Key Takeaways
H2: Why Look for an Alternative?（{Tool}的3个最大缺点）
H2: Top 10 {Tool} Alternatives（每个：简介+价格+优缺点+适合谁）
H2: Comparison Table
H2: Free Alternatives（单独列出真正免费的）
H2: FAQ
H2: Final Recommendation
[Last updated行]
```

### 4.3 写作AI指令（直接复制，每篇用）

```
根据以下Brief写一篇AI工具评测文章，严格遵守所有规则。

## 硬性规则（违反任何一条=不合格，必须重写）
1. 开头3行内给出明确结论，禁止"AI正在改变世界"类废话
2. Quick Answer控制在280-320字符，直接给购买建议
3. 每个工具必须说清：免费额度/付费价格/最适合谁/最大缺点
4. 对比表格用Markdown，数据必须来自我们的tools.json，禁止编造
5. 分场景推荐：学生/程序员/写作者/设计师各选谁
6. 必须有"Who Should Look Elsewhere"小节，诚实说缺点
7. 定价必须做真实成本计算（年付总价/每用户成本/免费版限制）
8. "How We Tested"必须有具体数字（测试时长/硬件/样本量/评分维度）
9. FAQ用问答格式，每个答案第一句直接回答，2-3句
10. 联盟链接自然融入，标注"affiliate"，加rel="sponsored"
11. 全文英文，面向美国用户，口语化但专业
12. 不确定的数据标注"[需核实]"，不要编
13. 结尾："大多数人选X，如果你是Y场景选Z"
14. 末尾加："Last updated: [日期]. We re-tested this tool in [月份] and confirmed the pricing/features below are accurate."
15. 字数2500-3500

## Brief内容
[粘贴Brief]

## 我们的工具数据（从tools.json提取）
[粘贴相关工具的价格/功能/链接数据]
```

### 4.4 质量门（发布前必须逐项检查，不达标不准提交）

#### 内容质量门
- [ ] 字数2500-3500
- [ ] 100%英文，无中文
- [ ] Quick Answer 280-320字符，直接给结论
- [ ] Key Takeaways ≥3条
- [ ] 有对比表格（对比页/列表页必须）
- [ ] 有分场景推荐
- [ ] 有"Who Should Look Elsewhere"
- [ ] 有"How We Tested"含具体数字
- [ ] FAQ ≥5个，从真实PAA提取
- [ ] 定价有真实成本计算
- [ ] 诚实说缺点，不全是好话
- [ ] Last updated行

#### SEO质量门
- [ ] 标题含主关键词+年份，<60字符
- [ ] Meta description 150字，含CTA
- [ ] 前100字出现主关键词
- [ ] H1唯一，H2/H3层级清晰
- [ ] URL是关键词slug，不是article-api-xxx
- [ ] 图片有alt text
- [ ] FAQPage schema标记
- [ ] Article schema标记

#### 链接质量门
- [ ] 内链≥3个，锚文本用关键词
- [ ] 联盟链接≥2处（对比表+结尾），加rel="sponsored"
- [ ] 外链≥1个权威源（官方文档/G2/行业报告）

#### 媒体质量门
- [ ] 真实截图≥3张（不是SVG模拟图），截图是工具实际界面
- [ ] 截图有alt text
- [ ] 截图文件在public/screenshots/下

#### 技术质量门
- [ ] 文章页返回200
- [ ] 无控制台错误
- [ ] 移动端可正常显示
- [ ] Lighthouse移动端性能>50

### 4.5 发布流程
1. 生成Brief → 2. AI写初稿 → 3. 过质量门 → 4. 不合格重写 → 5. 提交PR → 6. CI通过 → 7. merge → 8. 线上验证200 → 9. 更新iteration_log → 10. 写入state.json完成

---

## 5. 技术SEO标准（窗口1负责）

### 5.1 URL规范
- ✅ 格式：`/blog/keyword-slug-2026`
- ❌ 禁止：`/blog/article-api-20260903-171438-xxx`
- 已有异常URL：301重定向到正常slug

### 5.2 必须修复的技术问题清单
| 问题 | 优先级 | 修复方法 |
|------|--------|---------|
| article-api URL | P0 | 批量301重定向 |
| 4个零点击页title/meta | P0 | 重写，加数字+年份+结论 |
| /compare页内容太泛 | P0 | 拆成具体对比页，/compare做索引 |
| sitemap完整性 | P1 | 检查包含所有文章 |
| robots.txt允许GPTBot | P1 | 确认不拦截GPTBot |
| schema标记 | P1 | Article+FAQPage+Product批量添加 |
| 页面速度 | P1 | Lighthouse移动端>70 |
| 重复内容/标题 | P2 | 扫描并修复 |

### 5.3 自动内链系统（必须搭建）
- 维护`internal_link_map.json`：关键词→文章URL
- 新文章merge后，脚本自动运行：
  1. 扫描新文章，找到3-5个已有文章关键词，自动加内链
  2. 扫描3-5篇已有文章，找到新文章关键词，反向加内链
- 内链锚文本必须用关键词，不是"点击这里"

### 5.4 GEO/AI搜索优化标准
- robots.txt允许GPTBot
- 每个工具信息结构化（名称/价格/免费额度/强项/弱项/最适合谁）
- FAQPage schema
- 对比表格清晰表头
- "Quick Answer"板块用1-2句回答核心问题（AI优先引用）
- 原创数据内容（用533工具数据库做价格报告等）

---

## 6. 数据分析与迭代标准（窗口4负责）

### 6.1 每周GSC分析流程
1. 拉取本周GSC数据（已有gsc-fetch workflow）
2. AI自动识别3类页面：

| 类型 | 识别条件 | 动作 | 输出待办 |
|------|---------|------|---------|
| 高曝光低CTR | 曝光>100且CTR<1% | 生成新title+meta建议 | assigned_to=窗口4, P1 |
| 排名11-20 | 平均排名11-20 | 分析缺什么（字数/内链/内容深度） | assigned_to=窗口3, P1 |
| 排名1-3低点击 | 排名1-3但CTR<2% | 生成CTR优化建议 | assigned_to=窗口4, P0 |

3. 新出现有曝光的关键词→评估是否值得写新文章
4. 所有发现写入state.json待办

### 6.2 GSC分析AI指令
```
分析本周GSC数据，输出优化待办。

1. 找出曝光>100但CTR<1%的页面，为每个生成：
   - 当前标题
   - 新标题建议（含数字+年份+明确价值，<60字符）
   - 新meta description（150字，含CTA）
2. 找出排名11-20的页面，为每个分析：
   - 当前字数
   - 缺什么（内链？FAQ？对比表？内容深度？）
   - 具体优化建议
3. 找出排名1-3但CTR<2%的页面，生成CTR优化建议
4. 找出新出现的有曝光（>10）但无专门文章的关键词，评估是否值得写
5. 输出JSON格式的待办列表，每项含：
   {"task":"描述","assigned_to":"窗口X","priority":"P0/P1","source":"gsc_analysis_日期"}

GSC数据：
[粘贴本周报告]
```

### 6.3 关键词排名监控
- 每周记录P0/P1关键词的排名变化
- 排名上升的词→加大内链投入
- 排名下降的词→分析原因，写入待办
- 连续3周排名11-20的词→P0优化

---

## 7. 外链建设标准（窗口2负责）

### 7.1 外链目标优先级
| 方法 | 效果 | 难度 | 每周目标 |
|------|------|------|---------|
| 原创数据/研究被引用 | 最高 | 中 | 1篇原创数据内容/月 |
| Guest Post | 高 | 中 | 2篇/月 |
| 资源页链接 | 中 | 低 | 5个/周 |
| Reddit/社区 | 中 | 低 | 3次/周 |
| 免费工具引流 | 高 | 高 | 长期项目 |

### 7.2 外链目标生成AI指令
```
生成50个外链目标，分类输出。

1. 搜索"AI tools"相关的博客、资源页、论坛
2. 对每个目标评估：域名DR、内容相关性、是否接受guest post/资源提交
3. 分类：
   A类（DR50+，接受guest post）：列出网站、URL、DR、投稿指南链接
   B类（DR30-50，资源页）：列出网站、URL、DR、提交方式
   C类（社区/论坛）：列出网站、URL、规则、适合的内容类型
4. 每个目标给出具体的外链策略（写什么主题的guest post/在资源页加什么描述/在社区回答什么问题）
```

### 7.3 Reddit社区操作规范
-  subreddit：r/ChatGPT, r/artificial, r/MachineLearning, r/AItools, r/singularity
- ❌ 禁止硬广，禁止只发链接
- ✅ 回答问题时自然引用我们的对比页作为参考
- ✅ 分享我们的原创数据内容
- ✅ 每个subreddit先参与讨论1周再发链接
- 每周3次有价值的回答，每次可带1个相关链接

---

## 8. 变现优化标准（窗口5负责）

### 8.1 联盟链接优化
- 每篇文章联盟链接≥2处（对比表+结尾）
- 对比表中推荐工具的名称直接链联盟链接
- 结尾Final Verdict中明确推荐+联盟链接
- 所有联盟链接加`rel="sponsored"`
- 跟踪每个联盟链接的点击数（已有affiliate_clicks.md）

### 8.2 转化率优化
- 对比页是转化率最高的格式（18-25%），优先做
- "Most people choose X"式明确推荐比"both are good"转化率高3倍
- 独家优惠/折扣码如果有，必须放在显眼位置
- 每月分析哪些文章联盟点击多，哪些少，优化少的

---

## 9. UI/UX标准（窗口6负责）

### 9.1 对比页设计
- 对比表格固定表头，滚动时可见
- 推荐工具高亮（边框/背景色）
- 价格/免费额度用徽章显示
- 移动端表格横向滚动或卡片式展示

### 9.2 文章页设计
- Quick Answer板块用特殊背景色突出
- Key Takeaways用列表图标
- 截图宽度100%，圆角
- 目录导航（长文章）
- 相关文章推荐在文末

---

## 10. 发布节奏与时间线

### 10.1 每周发布计划
| 周次 | 新文章 | 旧文优化 | 技术修复 | 外链 |
|------|--------|---------|---------|------|
| 第1-2周 | 3篇（P0对比页） | 4个零点击页 | URL修复+sitemap | 10个资源页 |
| 第3-4周 | 4篇（2对比+2评测） | 5篇 | 内链系统上线 | 10个+2guest post |
| 第5-8周 | 5篇/周（集群支撑文） | 5篇/周 | schema批量 | 15个/周 |
| 第9-12周 | 4篇/周 | 排名11-20优化 | GEO优化 | 15个+2guest |
| 第13-24周 | 3-4篇/周 | 持续迭代 | 性能优化 | 持续 |

### 10.2 24周流量目标
| 阶段 | 周次 | GSC曝光 | GSC点击/月 |
|------|------|---------|------------|
| 基建期 | 1-2 | 2000→5000 | 9→20 |
| 长尾起量 | 3-6 | 5000→15000 | 20→100 |
| 集群成型 | 7-12 | 1.5万→5万 | 100→500 |
| 权重突破 | 13-18 | 5万→15万 | 500→2000 |
| 放量期 | 19-24 | 15万→50万 | 2000→10000 |

---

## 11. 各窗口职责矩阵

| 任务 | 窗口1 | 窗口2 | 窗口3 | 窗口4 | 窗口5 | 窗口6 |
|------|-------|-------|-------|-------|-------|-------|
| 关键词挖掘 | | | | ✅主 | | |
| 集群规划 | | | ✅ | ✅协同 | | |
| Brief生成 | | | ✅ | ✅提供词 | | |
| 文章写作 | | | ✅主 | | | |
| 质量门检查 | | | ✅ | ✅抽检 | | |
| 技术SEO修复 | ✅主 | | | | | |
| 自动内链 | ✅主 | | | | | |
| GSC分析 | | | | ✅主 | | |
| 排名监控 | | | | ✅主 | | |
| 外链建设 | | ✅主 | | | | |
| 联盟优化 | | | | | ✅主 | |
| UI/UX | | | | | | ✅主 |
| 截图获取 | | | ✅ | | | ✅协同 |

---

## 12. 验收标准

### 12.1 每周验收（指挥官检查）
- [ ] 本周发文量达标
- [ ] 所有新文过质量门
- [ ] P0待办数量减少
- [ ] GSC数据有记录
- [ ] 外链目标有推进
- [ ] 无新增技术问题

### 12.2 每月验收
- [ ] GSC曝光环比增长
- [ ] GSC点击环比增长
- [ ] 至少5个关键词进入前20
- [ ] 至少1个关键词进入前10
- [ ] 联盟点击数有记录
- [ ] 外链数环比增长

---

> 本文档是活文档，每次发现新问题/新方法都要更新。
> 所有窗口必须在每次定时任务触发时先读本文件，再执行任务。
