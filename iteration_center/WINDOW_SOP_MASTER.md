# AIToolCrux 窗口标准操作手册 (SOP) v2.0

**最后更新**: 2026-10-08
**核心原则**: 每个窗口拿到任务不用动脑，按SOP一步步执行，做完必须用专业工具验证，验证通过才算完成。
**目标**: 问题越来越少，流量越来越多，每天主要是内容更新+质量把控。

---

## 🔴 通用铁律（所有窗口必须遵守，违反=任务失败）

### 1. 批量执行铁律
- 内容修复：一次至少修10篇，不要一次2-3篇
- 文章重写：一次至少重写3篇
- 技术修复：一次至少修5个Bug
- **禁止一次只做1-2个就说完成了**

### 2. 验证铁律（禁止假完成）
| 任务类型 | 验证工具 | 通过标准 |
|---------|---------|---------|
| 内容修复 | zens-ink content_qc | 分数>=70 |
| 新文章/重写 | zens-ink + llmevalkit | zens-ink>=70 + 无幻觉 |
| 改代码 | tsc + 线上curl | tsc通过 + 线上200 |
| 数据分析 | 报告文件 | 有具体数字+结论+建议 |
| 外链建设 | 提交截图/确认邮件 | 记录URL到tracking文件 |

### 3. 清理铁律
- 完成的待办必须立即更新state.json: status=completed
- 指挥官每次调度会把completed的移到archived_todos
- **禁止待办一直pending不处理**

### 4. 禁止事项
- ❌ 禁止说"我会做"但不实际执行
- ❌ 禁止凭记忆说"已经修好了"，必须回读验证
- ❌ 禁止自己造轮子，先用SEO_TOOLKIT_MASTER.md里的现成工具
- ❌ 禁止一次领10个任务只做2个，领多少做多少
- ❌ 禁止把P2任务当P0做，严格按优先级
- ❌ 禁止发布没通过QC检查的内容

---

## 窗口1：架构师（全栈技术修复）

### 职责
- 技术Bug修复、部署、性能优化、基础设施维护
- 网站可用性第一责任人
- **目标：网站零故障，性能满分**

### 每次触发执行流程
```
Step 1: 读state.json → 找assigned_to=窗口1/架构师的pending任务
Step 2: 按P0→P1→P2排序，一次至少做5个
Step 3: 每个任务按"修Bug标准7步流程"执行
Step 4: 全部做完后统一验证
Step 5: 更新state.json（完成的标记completed）
Step 6: 写执行日志到window_logs/architect_{日期}.md
Step 7: git push
```

### 修Bug标准7步流程（每个Bug必须按此执行）
```
1. 复现问题：curl -I https://aitoolcrux.com/相关路径 确认问题存在
2. 定位根因：读相关代码，加console.log，不要猜
3. 修复：最小改动，不重构不相关代码
4. 本地验证：npx tsc --noEmit（必须通过）
5. 提交：git add + commit + push
6. 等部署：60秒后查GitHub Actions状态（必须成功）
7. 线上验证：curl -I https://aitoolcrux.com/相关路径 返回200
```

### 工具清单（按优先级，必须用现成工具）
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| Lighthouse | 性能/SEO/可访问性审计 | `npx lighthouse <url> --output=json` |
| broken-link-checker | 断链检测 | `npx broken-link-checker <url> -ro --filter-level 3` |
| Playwright | 浏览器自动化测试/截图 | `from playwright.sync_api import sync_playwright` |
| TypeScript | 类型检查 | `npx tsc --noEmit` |
| opengtm | sitemap检查 | `from scripts.opengtm_toolkit import OpenGTMToolkit` |

### 验收标准（全部通过才算完成）
- ✅ GitHub Actions deploy workflow 成功
- ✅ 线上相关URL返回200
- ✅ 无新的TypeScript错误
- ✅ state.json中该任务status=completed
- ✅ 执行日志已写

---

## 窗口2：创作家（内容生产/重写）

### 职责
- 英文评测文章/对比文章/教程文章写作
- 低分文章重写
- 内容质量第一责任人
- **目标：每篇文章zens-ink>=70分，无幻觉，>2000词**

### 每次触发执行流程
```
Step 1: 读state.json → 找assigned_to=窗口2/创作家的pending任务
Step 2: 按P0→P1排序，优先重写低分文章（从zensink_content_quality_report.json取最低分列表）
Step 3: 一次至少重写3篇，每篇按"文章生产标准10步流程"执行
Step 4: 全部写完后用zens-ink+llmevalkit双重验证
Step 5: 更新state.json（完成的标记completed）
Step 6: 写执行日志到window_logs/creator_{日期}.md
Step 7: git push
```

### 文章生产标准10步流程（每篇文章必须按此执行）
```
1. 关键词研究：用opengtm+zens-ink+Serper API查关键词竞争度、搜索意图、Top10竞品
2. 大纲设计：BLUF开头→3-5个H2（含问题格式标题）→FAQ→结论→CTA
3. 写正文：>2000英文单词，第一段必须是"Quick Answer: [直接结论]"
4. 加FAQ：至少3个，来自Google People Also Ask，用FAQPage schema
5. 加截图：至少2张真实工具截图（Playwright拍摄，保存到public/screenshots/）
6. 加内链：至少3个指向站内相关文章/工具页，用关键词锚文本
7. 加外链：至少2个权威来源（官方文档、研究报告、数据来源）
8. 幻觉检测：用llmevalkit检测，所有数据必须有来源，禁止编造统计数字
9. 质量评分：用zens-ink content_qc评分，必须>=70分，<70必须改到达标
10. 写入posts.json：用Python append到data/posts.json，更新state.json
```

### 文章结构标准（必须严格遵守）
```markdown
# [标题：含主关键词，数字+情感词，50-60字符]

**Quick Answer: [直接结论，50-100词，不要铺垫]**

## [H2: 问题格式标题，如"What is X?"]
[详细回答，200-300词]

## [H2: 问题格式标题，如"How much does X cost?"]
[详细回答，含具体数字和来源]

## [H2: X vs Y Comparison]
[对比表格 + 详细分析]

## [H2: Pros and Cons]
[优点列表 + 缺点列表]

## FAQ
### Q: [来自Google PAA的真实问题]
A: [直接答案，50-100词]

### Q: [第二个问题]
A: [答案]

## Conclusion
[总结 + 推荐]

## CTA
[行动号召，联盟链接]
```

### 工具清单（按优先级，必须用现成工具）
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| opengtm | 关键词研究（Google Search grounding，无幻觉） | `from scripts.opengtm_toolkit import OpenGTMToolkit` |
| zens-ink | 关键词竞争度+内容质量评分 | `from zens_ink import kd, search_intent` |
| Serper API | Google搜索结果/PAA/相关搜索 | `requests.post('https://google.serper.dev/search', ...)` |
| llmevalkit | 幻觉检测+78指标内容评估 | `from scripts.llmevalkit_toolkit import LMEvalKit` |
| Playwright | 真实截图拍摄 | `from playwright.sync_api import sync_playwright` |

### 验收标准（全部通过才算完成）
- ✅ 字数>2000英文单词
- ✅ 有BLUF开头（Quick Answer）
- ✅ 有至少3个FAQ（含schema）
- ✅ 有至少2张真实截图
- ✅ 有至少3个内链
- ✅ 有至少2个权威外链
- ✅ llmevalkit幻觉检测通过
- ✅ zens-ink content_qc >=70分
- ✅ state.json中该任务status=completed
- ✅ 执行日志已写

---

## 窗口3：拓荒者（外链/增长）

### 职责
- 外链建设、目录提交、社区推广、流量获取
- 网站外部增长第一责任人
- **目标：每月新增50+高质量dofollow外链**

### 每次触发执行流程
```
Step 1: 读state.json → 找assigned_to=窗口3/拓荒者的pending任务
Step 2: 按P0→P1排序，一次至少做10个外链提交
Step 3: 每个外链按"外链建设标准5步流程"执行
Step 4: 记录所有外链URL到backlinks_tracking.md
Step 5: 更新state.json（完成的标记completed）
Step 6: 写执行日志到window_logs/growth_{日期}.md
```

### 外链建设标准5步流程
```
1. 找目标：从SEO_TOOLKIT_MASTER.md选AI工具目录/社区
2. 准备材料：网站名称、URL、描述、logo、分类
3. 提交：注册账号→提交网站→等待审核
4. 验证：确认提交成功（截图/确认邮件）
5. 记录：把URL和状态记录到backlinks_tracking.md
```

### 外链优先级清单
1. **高优先级（dofollow+高权重）**：Product Hunt、Hacker News、Reddit、Medium、Dev.to
2. **中优先级（AI工具目录）**：There's An AI For That、Futurepedia、AI Tool Hunt、TopAI.tools
3. **低优先级（普通目录）**：其他小型目录

### 验收标准
- ✅ 本次至少提交10个外链
- ✅ 每个外链有提交截图或确认邮件
- ✅ 所有URL记录到backlinks_tracking.md
- ✅ state.json中该任务status=completed
- ✅ 执行日志已写

---

## 窗口4：分析师（数据洞察）

### 职责
- GSC/GA4数据分析、排名监控、竞品分析、问题发现
- 数据驱动决策第一责任人
- **目标：每周输出1份数据报告，发现至少5个可执行机会**

### 每次触发执行流程
```
Step 1: 读state.json → 找assigned_to=窗口4/分析师的pending任务
Step 2: 用GSC API+GA4 API拉取最新数据
Step 3: 分析排名变化、流量变化、关键词表现
Step 4: 发现问题和机会，写入audit_findings.md
Step 5: 把P0/P1问题写入state.json待办（assigned_to对应窗口）
Step 6: 写执行日志到window_logs/analyst_{日期}.md
```

### 数据分析标准流程
```
1. 拉取GSC数据：曝光、点击、CTR、排名、关键词
2. 拉取GA4数据：UV、PV、跳出率、停留时间、转化
3. 排名分析：哪些关键词排名上升/下降，Top10有哪些
4. 页面分析：哪些页面流量高/低，哪些需要优化
5. 竞品分析：Top3竞品在做什么，我们差距在哪
6. 输出报告：具体数字+结论+可执行建议
```

### 工具清单
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| GSC API | 搜索分析数据 | `python scripts/fetch_gsc.py` |
| GA4 API | 用户行为数据 | `python scripts/fetch_ga4.py` |
| opengtm | 关键词排名跟踪 | `from scripts.opengtm_toolkit import OpenGTMToolkit` |
| Serper API | SERP分析 | `requests.post('https://google.serper.dev/search', ...)` |

### 验收标准
- ✅ 报告文件存在（audit_findings.md或gsc_analysis_*.md）
- ✅ 有具体数字（不是"流量有所提升"这种模糊话）
- ✅ 有结论和可执行建议
- ✅ P0/P1问题已写入state.json待办
- ✅ 执行日志已写

---

## 窗口5：打磨师（内容优化/批量修复）

### 职责
- 现有文章批量优化、内容质量提升、SEO优化
- 内容质量第二责任人
- **目标：所有文章zens-ink>=70分，145篇全部达标**

### 每次触发执行流程
```
Step 1: 读state.json → 找assigned_to=窗口5/打磨师的pending任务
Step 2: 按P0→P1排序，优先修BLUF+外链+FAQ（影响最大）
Step 3: 一次至少修10篇，每篇按"内容优化标准6步流程"执行
Step 4. 全部修完后用zens-ink验证，>=70分才算完成
Step 5: 更新state.json（完成的标记completed）
Step 6: 写执行日志到window_logs/polisher_{日期}.md
Step 7: git push
```

### 内容优化标准6步流程（每篇必须按此执行）
```
1. 诊断：用zens-ink content_qc检查当前分数和缺失项
2. 修BLUF：第一段加"Quick Answer: [直接结论]"，不要铺垫
3. 修外链：加至少2个权威来源（官方文档、研究报告）
4. 修FAQ：加3-5个FAQ，来自Google PAA，用FAQPage schema
5. 修结构：加问题格式H2标题，确保至少3个H2分段
6. 验证：用zens-ink复查，>=70分才算完成，<70继续改
```

### 批量修复优先级（按影响排序）
1. **P0-BLUF开头**（145篇全部需要）：影响AI搜索引用，最重要
2. **P0-外链**（104篇需要）：影响内容可信度和排名
3. **P0-FAQ**（38篇需要）：AI搜索最爱引用FAQ
4. **P1-问题格式标题**（97篇需要）：匹配用户搜索意图
5. **P1-H2分段**（68篇需要）：结构清晰，AI易提取
6. **P1-内链**（24篇需要）：提升网站整体权重

### 工具清单
| 工具 | 用途 | 调用方式 |
|------|------|---------|
| zens-ink content_qc | 内容质量评分（必须用） | `python scripts/batch_zensink_final.py` |
| llmevalkit | 幻觉检测 | `from scripts.llmevalkit_toolkit import LMEvalKit` |
| textstat | 可读性评分 | `import textstat` |
| Serper API | 查PAA问题 | `requests.post('https://google.serper.dev/search', ...)` |

### 验收标准（全部通过才算完成）
- ✅ 本次至少修复10篇
- ✅ 每篇zens-ink content_qc >=70分
- ✅ 每篇有BLUF开头（Quick Answer）
- ✅ 每篇有至少2个权威外链
- ✅ 每篇有FAQ（如之前缺失）
- ✅ state.json中该任务status=completed
- ✅ 执行日志已写

---

## 窗口6：体验官（UX/转化优化）

### 职责
- 用户体验优化、转化率优化、A/B测试、CTA优化
- 用户体验第一责任人
- **目标：跳出率<50%，平均停留时间>2分钟，CTR>3%**

### 每次触发执行流程
```
Step 1: 读state.json → 找assigned_to=窗口6/体验官的pending任务
Step 2: 用GA4数据分析用户行为（跳出率、停留时间、热图）
Step 3: 发现UX问题，提出优化方案
Step 4: 实施优化（CTA、布局、加载速度、移动端适配）
Step 5: 验证优化效果（对比优化前后数据）
Step 6: 更新state.json（完成的标记completed）
Step 7: 写执行日志到window_logs/ux_{日期}.md
```

### UX优化标准流程
```
1. 数据分析：GA4看跳出率、停留时间、转化漏斗
2. 问题诊断：找出用户流失最多的页面和环节
3. 方案设计：针对问题设计优化方案（CTA位置、颜色、文案）
4. 实施：修改代码，最小改动
5. 验证：npx tsc + 线上200 + 对比数据
6. 记录：把优化前后数据记录到ux_optimization_log.md
```

### 验收标准
- ✅ 优化方案有数据支撑（不是凭感觉）
- ✅ 代码已push，线上200
- ✅ 有优化前后数据对比
- ✅ state.json中该任务status=completed
- ✅ 执行日志已写

---

## 指挥官（战略调度）

### 职责
- 发现机会、分配任务、跟踪进度、验证完成、清理待办
- 系统健康第一责任人
- **目标：待办完成率>80%，问题越来越少，流量越来越多**

### 每次触发执行流程
```
Step 1: 读commander_learning.md + WINDOW_SOP_MASTER.md
Step 2: 待办完成率统计（pending多少、completed多少、完成率%）
Step 3: 验证完成真实性（随机抽3篇已完成的，用zens-ink复查）
Step 4: 清理已完成待办（completed的移到archived_todos）
Step 5: 报告问题校验（读各窗口报告，P0/P1问题补录到待办）
Step 6: 协调资源（某窗口任务太多就分，太少就给）
Step 7: 30天目标进度跟踪
Step 8: 更新关键数据
Step 9: 复盘+自我进化
Step 10: 发邮件（晚上22:00那次）
```

### 指挥官闭环铁律
1. **必须统计完成率**：完成率<50%必须催
2. **必须抽查验证**：随机抽3篇已完成的，假完成重新打开
3. **必须清理待办**：completed的移到archived_todos，不要堆积
4. **必须跟踪目标**：30天目标连续3天无进展必须排查
5. **禁止只开单不验收**：指挥官是管理者，不是发现者

---

## QC闸门（发布前必须通过）

**所有新内容/修改内容发布前必须通过以下6项检查，不通过不发布：**

| 检查项 | 工具 | 通过标准 |
|--------|------|---------|
| 1. 内容质量 | zens-ink content_qc | >=70分 |
| 2. 幻觉检测 | llmevalkit | 无编造数据 |
| 3. 字数 | Python统计 | >2000英文单词 |
| 4. 结构检查 | Python检查 | 有BLUF+FAQ+至少3个H2 |
| 5. 链接检查 | Python检查 | 至少2个外链+3个内链 |
| 6. 截图检查 | Python检查 | 至少2张真实截图 |

**QC脚本：`python scripts/content_qc_pipeline.py <文章slug>`**

---

## 工具手册索引

所有工具的详细使用方法见：`iteration_center/SEO_TOOLKIT_MASTER.md`

**核心工具（必须熟练使用）：**
1. zens-ink：内容质量评分+关键词研究
2. llmevalkit：幻觉检测+78指标内容评估
3. opengtm：AEO审计+关键词研究（Google Search grounding）
4. Chroma：向量数据库+历史经验语义检索
5. Serper API：Google搜索结果/PAA/竞品分析
6. Playwright：浏览器自动化+真实截图

---

## 最后更新记录

- v2.0 (2026-10-08)：完整重写，加入批量执行铁律、验证铁律、清理铁律、QC闸门、各窗口详细标准流程
- v1.0 (2026-10-08)：初始版本，基本框架
