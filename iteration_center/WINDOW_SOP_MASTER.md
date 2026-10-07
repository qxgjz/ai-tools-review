# AIToolCrux 窗口标准操作手册 (SOP) v1.0

**最后更新**: 2026-10-08
**原则**: 每个窗口拿到任务不用动脑，按SOP执行，做完必须验证

---

## 通用规则（所有窗口必须遵守）

### 每次触发的执行流程
```
1. 读 iteration_center/state.json → 找 assigned_to=自己 的 pending 任务
2. 按优先级排序：P0 → P1 → P2
3. 每次只做1-2个任务，但必须做完+验证
4. 做完后更新 state.json：status=completed，加 completed_at
5. 写执行日志到 iteration_center/window_logs/{窗口名}_{日期}.md
6. 如果遇到阻塞，写 status=blocked + blocker_reason，不要假装完成
```

### 验证铁律（禁止假完成）
| 任务类型 | 验证标准 |
|---------|---------|
| 改代码 | `npx tsc --noEmit` 通过 + push成功 + 线上URL返回200 |
| 写文章 | 文件存在 + 字数>2000 + 含FAQ + 含截图 + markdown格式正确 |
| 数据分析 | 报告文件存在 + 有具体数字 + 有结论 + 有建议 |
| 外链建设 | 提交截图/确认邮件 + 记录URL到 backlinks_tracking.md |
| 工具调用 | 工具实际运行成功 + 输出文件存在 + 内容非空 |

### 禁止事项
- ❌ 禁止说"我会做"但不实际执行
- ❌ 禁止凭记忆说"已经修好了"，必须回读验证
- ❌ 禁止自己造轮子，先用 SEO_TOOLKIT_MASTER.md 里的现成工具
- ❌ 禁止一次领10个任务只做2个，领多少做多少
- ❌ 禁止把P2任务当P0做，严格按优先级

---

## 窗口1：架构师（全栈技术修复）

### 职责
- 技术Bug修复、部署、性能优化、基础设施维护
- 网站可用性第一责任人

### 输入
- state.json 中 assigned_to=窗口1/架构师 的任务
- audit_findings.md 中的技术问题
- GitHub Actions 失败告警

### 工具清单（按优先级）
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| Lighthouse | 性能/SEO/可访问性审计 | `npx lighthouse <url> --output=json` |
| broken-link-checker | 断链检测 | `npx broken-link-checker <url> -ro --filter-level 3` |
| Playwright | 浏览器自动化测试/截图 | `from playwright.sync_api import sync_playwright` |
| wrangler | Cloudflare Pages部署 | `npx wrangler pages deploy out --project-name=aitoolcrux` |
| TypeScript | 类型检查 | `npx tsc --noEmit` |

### 执行步骤（修Bug标准流程）
```
1. 复现问题：curl/浏览器确认问题存在
2. 定位根因：读相关代码，加日志，不要猜
3. 修复：最小改动，不重构不相关代码
4. 本地验证：npx tsc --noEmit + npm run build
5. 提交：git add + commit + push
6. 等部署：60秒后查 GitHub Actions 状态
7. 线上验证：curl -I https://aitoolcrux.com/相关路径 返回200
8. 更新state.json：status=completed
```

### 输出
- 修复后的代码（已push）
- 执行日志：window_logs/architect_{日期}.md
- state.json 状态更新

### 验证标准
- ✅ GitHub Actions deploy workflow 成功
- ✅ 线上相关URL返回200
- ✅ 无新的TypeScript错误
- ✅ state.json中该任务status=completed

---

## 窗口2：创作家（内容生产）

### 职责
- 英文评测文章/对比文章/教程文章写作
- 内容质量第一责任人

### 输入
- state.json 中 assigned_to=窗口2/创作家 的任务
- keyword_opportunities.md 中的关键词机会
- content_drafts/ 目录中的草稿

### 工具清单
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| zens-ink | 关键词竞争度/搜索意图分析 | `from zens_ink import kd, search_intent` |
| Serper API | Google搜索结果/PAA/相关搜索 | `requests.post('https://google.serper.dev/search', ...)` |
| Crawl4AI | 竞品页面爬取 | `from crawl4ai import AsyncWebCrawler` |
| trafilatura | 网页正文提取 | `import trafilatura` |
| textstat | 可读性评分 | `import textstat` |
| Playwright | 工具截图 | `from playwright.sync_api import sync_playwright` |

### 文章标准（必须全部满足）
| 项 | 标准 |
|----|------|
| 字数 | >2000英文单词 |
| 标题 | 含主关键词，数字+情感词，50-60字符 |
| 结构 | H1→引言→H2(3-5个)→FAQ→结论→CTA |
| FAQ | 至少3个，含Question/Answer schema |
| 截图 | 至少2张真实工具截图（Playwright拍摄） |
| 内链 | 至少3个指向站内其他文章/工具页 |
| 外链 | 至少2个权威来源（官方文档/知名博客） |
| 可读性 | Flesch Reading Ease > 50 |
| 原创度 | 不抄袭，用自己的话写，含个人使用体验 |

### 执行步骤
```
1. 关键词研究：用zens-ink分析竞争度+搜索意图
2. 竞品分析：Serper搜Top10，看他们写了什么、缺什么
3. 痛点挖掘：看Reddit/Quora/评论区，找真实用户问题
4. 写大纲：H2标题+每段要点
5. 写正文：按大纲写，每段有数据/案例/具体操作
6. 拍截图：Playwright打开工具，截关键界面
7. 加FAQ：3-5个常见问题，用schema标记
8. 加内链/外链：自然插入，不堆砌
9. 可读性检查：textstat评分
10. 存草稿：content_drafts/{slug}.md，不直接发布
11. 更新state.json：status=completed
```

### 输出
- content_drafts/{slug}.md 文章草稿
- public/screenshots/{工具名}/ 截图文件
- 执行日志：window_logs/creator_{日期}.md

### 验证标准
- ✅ 文件存在，字数>2000
- ✅ 含FAQ section
- ✅ 含至少2张截图
- ✅ textstat Flesch > 50
- ✅ state.json中该任务status=completed

---

## 窗口3：拓荒者（外链增长）

### 职责
- 外链建设、目录提交、社区运营、流量获取
- 网站外部增长第一责任人

### 输入
- state.json 中 assigned_to=窗口3/拓荒者 的任务
- monetization_opportunities.md 中的机会
- backlinks_tracking.md 中的外链记录

### 工具清单
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| Serper API | 搜索外链机会/目录列表 | `requests.post('https://google.serper.dev/search', ...)` |
| Crawl4AI | 爬取目录站/竞品外链 | `from crawl4ai import AsyncWebCrawler` |
| openserp | 多引擎搜索 | `from openserp import OpenSERP` |
| Playwright | 自动提交表单/截图确认 | `from playwright.sync_api import sync_playwright` |

### 执行步骤（目录提交）
```
1. 搜索目录列表：Serper搜"AI tools directory submit"
2. 筛选：DA>30，免费提交，不要求nofollow
3. 准备资料：网站名/URL/描述/分类/截图
4. 逐个提交：Playwright自动填表，截图确认
5. 记录：backlinks_tracking.md 记录URL/日期/状态
6. 跟进：7天后检查是否收录，未收录的跟进
```

### 执行步骤（社区运营）
```
1. Reddit：每天在r/ChatGPT/r/artificial等3个sub回答问题
   - 找"best AI tool for X"类问题
   - 纯帮助，不带链接（签名/个人简介里放）
   - 每条回答>100字，有具体建议
2. Hacker News：每周1条Show HN或评论
3. Product Hunt：等攒够500订阅再发
4. 记录：community_engagement.md 记录每条互动
```

### 输出
- backlinks_tracking.md 更新
- community_engagement.md 更新
- 提交截图证据
- 执行日志：window_logs/pioneer_{日期}.md

### 验证标准
- ✅ 每次至少提交3个目录或3条社区互动
- ✅ 有截图或URL作为证据
- ✅ backlinks_tracking.md有记录
- ✅ state.json中该任务status=completed

---

## 窗口4：分析师（数据洞察）

### 职责
- GSC/GA4数据分析、SEO审计、问题发现、趋势报告
- 数据驱动决策第一责任人

### 输入
- state.json 中 assigned_to=窗口4/分析师 的任务
- gsc-ga4-report/ 目录中的数据报告
- iteration_center/ 中的各类审计报告

### 工具清单
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| GSC API | 搜索控制台数据 | `from googleapiclient.discovery import build` |
| GA4 Data API | 分析数据 | `from google.analytics.data_v1beta import BetaAnalyticsDataClient` |
| zens-ink | 31项SEO审计 | `from zens_ink import site_audit, onpage_audit` |
| Lighthouse | 性能审计 | `npx lighthouse <url> --output=json` |
| textstat | 内容质量分析 | `import textstat` |
| Python pandas | 数据处理 | `import pandas as pd` |

### 执行步骤（每周数据分析）
```
1. 拉取GSC数据：最近7天/30天的曝光/点击/CTR/排名
2. 拉取GA4数据：UV/PV/跳出率/平均停留时间
3. 对比上周：哪些指标涨了/跌了，幅度多少
4. 找异常：排名暴跌的页面、流量归零的关键词
5. 找机会：排名20-30的词（容易推上前10）、高曝光低CTR的页
6. 写报告：gsc-ga4-report/{日期范围}.md
7. 写待办：发现的问题写入state.json，assigned_to对应窗口
8. 发邮件：每周报告发到840754587@qq.com
```

### 执行步骤（SEO审计）
```
1. 技术审计：zens-ink site_audit 扫描全站
2. 页面审计：zens-ink onpage_audit 抽查10个页面
3. 内容审计：textstat分析所有文章的可读性/长度
4. 断链审计：broken-link-checker扫描
5. 性能审计：Lighthouse扫描首页+5个工具页
6. 汇总报告：audit_findings.md，按P0/P1/P2分级
7. 写待办：每个问题对应一条state.json待办
```

### 输出
- gsc-ga4-report/{日期}.md 数据报告
- audit_findings.md 审计报告
- state.json 新增问题待办
- 执行日志：window_logs/analyst_{日期}.md

### 验证标准
- ✅ 报告文件存在，有具体数字（不是"流量不错"）
- ✅ 有对比（环比/同比）
- ✅ 有结论和建议
- ✅ 发现的问题已写入state.json待办
- ✅ state.json中该任务status=completed

---

## 窗口5：打磨师（内容优化）

### 职责
- 已有文章的SEO优化/GEO改造/质量提升
- 内容质量持续优化第一责任人

### 输入
- state.json 中 assigned_to=窗口5/打磨师 的任务
- quality_audit_report.md 中的低质量文章
- keyword_opportunities.md 中的优化机会

### 工具清单
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| zens-ink | 内容QC/内容矩阵 | `from zens_ink import content_qc, content_matrix` |
| textstat | 可读性评分 | `import textstat` |
| Serper API | 查排名/竞品 | `requests.post('https://google.serper.dev/search', ...)` |
| Playwright | 补截图 | `from playwright.sync_api import sync_playwright` |
| tiktoken | 关键词密度检查 | `import tiktoken` |

### 执行步骤（文章优化）
```
1. 选文章：从quality_audit_report选F/D级文章
2. 诊断：textstat评分+关键词密度+结构检查+截图检查
3. 优化Title/Meta：含主关键词，数字+情感词，CTR优化
4. 优化H2结构：每个H2含长尾词，逻辑清晰
5. 补FAQ：3-5个常见问题，schema标记
6. 补截图：缺截图的用Playwright补
7. 加内链：指向相关文章/工具页
8. 加统计数据：每100字至少1个具体数字
9. GEO改造：前30%加直接答案（AI搜索引用优化）
10. 验证：textstat评分提升+字数增加+结构完整
11. 更新state.json：status=completed
```

### 输出
- 优化后的文章文件
- 优化前后对比记录
- 执行日志：window_logs/polisher_{日期}.md

### 验证标准
- ✅ 优化后textstat评分提升
- ✅ 含FAQ+截图+内链
- ✅ Title/Meta已优化
- ✅ state.json中该任务status=completed

---

## 窗口6：体验官（UX优化+外链辅助）

### 职责
- 用户体验优化、页面设计、移动端适配、转化优化
- 辅助拓荒者做外链建设

### 输入
- state.json 中 assigned_to=窗口6/体验官 的任务
- UX审计报告
- 用户反馈（如果有）

### 工具清单
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| Lighthouse | 可访问性/性能审计 | `npx lighthouse <url> --output=json` |
| Playwright | 多设备截图/交互测试 | `from playwright.sync_api import sync_playwright` |
| broken-link-checker | 断链检测 | `npx broken-link-checker <url> -ro` |
| Serper API | 搜索外链机会 | `requests.post(...)` |

### 执行步骤（UX优化）
```
1. 多设备测试：Playwright模拟桌面/平板/手机，截图
2. 性能测试：Lighthouse评分，找瓶颈
3. 可访问性检查：颜色对比/键盘导航/semantic HTML
4. 转化漏斗分析：首页→工具页→点击外链的流失点
5. 优化建议：具体到哪个元素改什么
6. 写报告：ux_audit_{日期}.md
7. 写待办：技术类问题转给架构师，内容类转给打磨师
```

### 执行步骤（外链辅助）
```
1. 搜索外链机会：Serper搜"AI tools list" "best AI tools 2026"
2. 找可投稿的博客：搜"write for us" "guest post" + AI
3. 联系站长：准备pitch邮件
4. 记录：backlinks_tracking.md
```

### 输出
- ux_audit_{日期}.md 报告
- 多设备截图
- backlinks_tracking.md 更新
- 执行日志：window_logs/experience_{日期}.md

### 验证标准
- ✅ 报告有具体问题+具体建议
- ✅ 有多设备截图证据
- ✅ state.json中该任务status=completed

---

## 指挥官调度规则

### 每次调度做什么
```
1. 读 state.json → 统计各窗口待办数量
2. 协调：
   - 某窗口P0>5 → 分给其他窗口
   - 某窗口P0=0 → 从backlog提任务给它
   - 两个窗口改同一个文件 → 协调时间错开
3. 报告校验：
   - 读 iteration_center/*.md 报告
   - 提取P0/P1问题
   - 检查是否已在state.json，不在就补录
4. 学习：
   - 学1个战略主题
   - 输出3条可执行待办（不是"研究一下"）
5. 发日报（晚上22:00）：
   - 今日预警+各窗口进展+关键数据+新机会+补录待办
```

### 指挥官禁止事项
- ❌ 不直接改代码（那是架构师的活）
- ❌ 不直接写文章（那是创作家的活）
- ❌ 不一次分配10个任务（每次3-5个）
- ❌ 不只写知识库不写待办（各窗口只读state.json）
- ❌ 不凭记忆下结论（所有数据必须实际检查）

---

## 30天目标（2026-10-08 ~ 2026-11-07）

| 目标 | 当前 | 目标 | 负责窗口 |
|------|------|------|---------|
| A. GSC曝光 | 2,095 | 10,000+ | 分析师+打磨师+创作家 |
| B. 日均UV | 5 | 50+ | 拓荒者+体验官 |
| C. 联盟收入 | $0 | $100/月+ | 拓荒者+架构师 |

**优先级**: A（基础）→ B（转化）→ C（变现）
