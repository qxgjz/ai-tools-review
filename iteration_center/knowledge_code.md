## ⚠️ 部署前必做检查清单（2026-09-26新增，违反必导致Vercel构建失败）

**背景**：2026-09-26因GA4PageTracker.tsx新文件从未git跟踪，Vercel连续9次构建失败。以下清单每次迭代后必须全部通过：

1. **git status检查**：git status --short 确认没有未跟踪的新文件（??开头的文件必须git add）
2. **新组件必须跟踪**：任何新创建的.tsx/.ts组件文件，如果被其他文件import了，必须git add确认被跟踪
3. **立即提交**：每次迭代修改完后，不要积累，立即 git add -A && git commit -m "..." && git push origin main
4. **禁止提交token**：commit/push/deploy临时脚本中绝不硬编码ghp_/vcp_/cfut_ token，全部加入.gitignore
5. **push前验证**：git diff --cached --name-only 检查是否有.py脚本被staged，有则确认不含token
6. **Vercel构建监控**：push后等2分钟，去Vercel看部署状态是否READY，失败立即看日志修复

---
# 知识库：核心迭代（窗口1）

## 📋 每日SOP（每次触发强制执行）

1. 读 iteration_center/state.json → 找 current_todo 里 priority=P0 或 P1 且 status!=completed 的任务
2. 读 iteration_center/audit_findings.md → 找标 P0/P1 的问题
3. 按优先级选1-3个任务执行，不要贪多
4. 改完代码必须跑 npx tsc --noEmit，0 errors才继续
5. 通过GitHub API提交（不要git push）
6. 等90秒后线上验证：关键页面返回200，改动内容确实出现在HTML里
7. 更新 iteration_log.json 记录这轮做了什么
8. 更新 state.json 标记完成状态

## 🚪 质量门（不达标不准提交）

- [ ] tsc --noEmit 0 errors
- [ ] 线上至少3个页面返回200
- [ ] 改动的内容能在HTML源码里搜到
- [ ] 没有硬编码任何API Key/Token
- [ ] 改的文件不碰样式（样式归窗口6）


## ⚡ 批量执行规则（重要！）

不要干完1个任务就停。每次触发按这个逻辑跑：
1. 读 state.json 和 audit_findings.md
2. 找出所有 P0/P1 任务
3. 按优先级逐个执行，直到：
   - P0任务全部干完，或
   - 实在干不动了（比如需要用户手动操作/登录）
4. 干完一个立刻读下一个，不要停
5. 最后写一条总结：本次干了几个、还剩几个


## 🏷️ 修复标注规则（重要！）

每修完一个SEO问题，在iteration_log.json里必须写：
1. 这个问题预计影响哪个关键词/哪个页面
2. 预期效果（比如"双H1修复后，预计Google正确识别主标题，排名上升"）
3. 下周由窗口4验证这个效果有没有出现

不要只写"修了什么"，要写"为什么修、预期什么效果"。

## 📊 每日KPI

- 修复P0/P1问题数量
- 线上验证通过率
- TypeScript编译通过（必须100%）

---
## ⚠️ 误报纠正（2026-09-18 指挥官核实）

P0-HEALTH-001 说 public/screenshots/ 有0个webp文件 —— 这是误报。
实际核实：public/screenshots/ 根目录17个文件（11 webp + 6 svg），递归共66个webp + 40个svg = 106个。
你的脚本可能只查了某个子目录或路径不对。请用 Get-ChildItem -Recurse 重新核实，不要标0。
这个任务标记为false alarm，不需要重做。
## 🔴 全站审计新任务（2026-09-17 seo_audit_full_20260917.md，770 URL扫描结果）

0个P0问题（好）。257个P1问题，按优先级排：

1. **54个页面有2个H1（应=1）** —— 这是结构性问题，找出哪54个页面，删掉多余H1或改成H2
2. **约100个工具页>500KB** —— 最大的2.6MB（/tools/xxx），严重影响LCP。检查是不是内联了大JSON或重复渲染。Top20工具页优先压缩
3. **chatgpt-vs-claude重复URL** —— /blog/chatgpt-vs-claude-2026 和 /blog/chatgpt-vs-claude-2026-comparison 两个URL用了相同meta description。加canonical指向最终URL，或301
4. **8个重复Title组** —— 找出8组，每组加差异化title
5. **10个Title过长/过短** —— /contact 23字符、/privacy 27字符、/terms 29字符、/compare 61字符、4个工具页69字符
6. **13个Meta Description过长** —— /disclosure 161字符、/contact等，截到160字符以内
7. **165个broken外链** —— 大部分是GitHub timeout（爬的时候网络问题），不是真broken。真404的：microsoft-copilot-studio-pricing、stately.ai/docs/agents。真403的不用管（对方拒绝爬虫）

执行顺序：先做1（双H1）和3（重复URL canonical），这两个最影响SEO。工具页体积问题（2）单独排一轮，因为可能要改组件。
# 知识库：代码/工程（窗口1）

## 🆕 指挥官新任务（2026-09-17 第66轮学习后下发）

### 新任务：部署web-vitals真实用户监控（RUM）
- **背景**：P0-MOBILE-001待做，但之前只用Lighthouse实验室数据，没有真实用户数据
- **要做什么**：
  1. 安装 `web-vitals` npm包（Google官方，~1KB）
  2. 在app/layout.tsx加一个Reporter组件，把LCP/INP/CLS三个指标上报
  3. 先console.log打印，积累7天数据
  4. 7天后根据真实用户数据，针对性优化最差的那个指标
- **Core Web Vitals 2026标准（必须达标）**：
  | 指标 | 含义 | 目标 |
  |------|------|------|
  | LCP | 最大内容绘制 | ≤2.5s（理想<2.0s）|
  | INP | 交互响应（已替换FID）| ≤200ms |
  | CLS | 累积布局偏移 | ≤0.1 |
- **注意**：CLS归窗口6管（布局/图片尺寸），LCP/INP归你管（代码/资源加载）
- **来源**：Google官方 + a1technovation 2026指南 + corewebvitals.io

---


## 🚨 团队新成员（2026-09-17加入）

**窗口6：UI/UX设计工程师** 已经加入团队！

| 窗口6负责 | 你不要碰 |
|----------|---------|
| 网站视觉设计、美观度 | 设计、配色、排版、组件样式 |
| 用户体验优化 | 导航、交互、移动端体验 |
| 交互效果 | hover、动画、加载效果 |

**你和窗口6怎么协同：**
- 你改代码逻辑、SEO、内容、数据的时候，不要改样式和设计
- 如果发现设计问题，写进 audit_findings.md，窗口6会去改
- 如果窗口6改设计影响了你的功能，写进 iteration_log.json，指挥官会协调



> 每次完成任务后更新：学到了什么、犯了什么错、积累了什么经验。
> 目的：不重复踩坑。

## 🎯 极致标准（每次干完活自己对照）

### 什么叫干到极致？
- **60分（及格）**：tsc通过，线上验证200，没报错
- **90分（优秀）**：改完之后数据有提升（排名涨了/CTR升了/速度快了）
- **100分（极致）**：不仅改了，而且找到了最优解，用最少的代码、最快的速度、最好的效果

### 每次干完活必须做的3件事
1. **结果验证**：改完7天后，去看数据是不是真的提升了，不是自己觉得改得好就行
2. **复盘改进**：这次哪里做得好？哪里可以更好？下次怎么改进？
3. **沉淀经验**：这次学到了什么？写进这个文件，下次不踩坑

### 不要满足于"干完了"
- 不要只改完就完事了，要去验证效果
- 不要只用一种方法，去搜有没有更好的方法
- 不要只改代码，要去看用户数据，确认是不是真的解决了问题

---


## 🤖 作为AI的潜能发挥方向（窗口1）

### 不要只做"代码工人"，要做"全栈工程师+产品经理"
- 不只改完代码就完事，要主动思考：有没有更好的实现方式？
- 不只修bug，要主动发现潜在的bug、性能问题、用户体验问题
- 不只按任务清单干活，要主动找优化点：哪个页面加载慢？哪个组件可以优化？
- 不只写代码，要思考用户：这个改动对用户体验有什么影响？

### AI优势要用到极致
- **不知疲倦**：一次改多个小问题，不用等下次任务
- **精确**：改代码前先想清楚，一次改对，不要反复改
- **学习能力**：遇到新问题，主动搜解决方案，不要自己瞎写
- **全局视野**：改一个地方，想想会不会影响其他页面

---


## 2026-09-16

### 今天学到了什么
1. **GitHub API提交模式**：GET获取sha → PUT提交（base64编码content），比git push稳定，大陆网络友好。
2. **Vercel部署等待**：每次GitHub提交后等90秒再验证，不要提前。
3. **posts.json字段结构**：slug, title, excerpt, date(ISO), category, categorySlug, author, readingTime, wordCount, tags[], hasRealScreenshots, screenshotCount, content(HTML)。

### 犯过什么错
1. **截图URL检查误判**：用`"/screenshots/" in content`判断是否有截图，但SVG模拟图也包含这个路径，导致误判"已有截图"。应该同时检查`.svg`排除。
2. **windsurf.ai重定向**：windsurf.ai现在重定向到devin.ai（Cognition Labs改名），截到的是Devin页面不是Windsurf编辑器。下次需要找正确URL。
3. **插入截图找不到章节**：部分文章没有"How We Tested"章节，需要fallback到第一个h2后面插入。

### 积累了什么经验
1. **HTML figure格式（用户确认通过）**：
```html
<figure style="text-align:center;margin:2rem 0;">
  <img src="/screenshots/{filename}" alt="{Tool} interface" style="width:100%;max-width:860px;border:1px solid #e5e7eb;border-radius:8px;" />
  <figcaption style="margin-top:0.5rem;font-size:0.875rem;color:#6b7280;">{Tool} interface</figcaption>
</figure>
```
2. **截图插入位置**：统一插在"How We Tested"或"Hands-On Experience"章节后，不要插在开头或结尾。
3. **批量操作效率**：每次batch做5篇，写Python脚本批量处理，比逐篇Edit快10倍。
4. **PowerShell注意**：不支持`&&`，用分号；Python多行脚本写成.py文件执行，不要用`python -c`。
5. **提交前检查**：每次写脚本后先在本地跑，确认输出正确再提交GitHub。

## 待验证/待做
- [ ] 重截Windsurf正确界面
- [ ] 把新截的runway/pika/leonardo/coze截图插入文章正文
- [ ] 解决Stable Diffusion/ChatGPT/Claude截图问题（YouTube截帧失败）


## 待补充
- [2026-09-26] 学习主题：高星GitHub开源工具全景（SEO审计+性能监控+自动化测试）

  **知识点1：Lighthouse是Google官方开源审计引擎，GitHub 30k+ stars**——Chrome团队维护，覆盖Performance/Accessibility/Best Practices/SEO/Progressive Web App五大类审计。基于Puppeteer启动真实Chrome运行页面，输出JSON/HTML报告。CLI用法：`npx lighthouse https://example.com --output=json --output-path=report.json`。是所有性能/SEO审计工具的底层引擎。（来源：https://github.com/GoogleChrome/lighthouse + https://developer.chrome.com/docs/lighthouse/overview/）

  **知识点2：Lighthouse CI (LHCI)是Google官方CI集成方案，@lhci/cli月下载~2M**——专为持续集成设计，核心命令`lhci autorun`自动收集URL、运行Lighthouse、上传结果。支持assert断言（如`performance: 0.9`低于90分失败）、assertMatrix多URL不同阈值、GitHub Status Check在PR上显示分数。可选@lhci/server存储历史数据做趋势追踪。配置文件.lighthouserc.js。（来源：https://github.com/GoogleChrome/lighthouse-ci + https://googlechrome.github.io/lighthouse-ci/docs/getting-started.html）

  **知识点3：Unlighthouse（4.8k stars）实现全站Lighthouse并行扫描**——`npx unlighthouse --site example.com`一条命令自动发现sitemap/爬取所有URL、并行运行Lighthouse、生成统一交互式报告。与单页Lighthouse CLI的区别：自动URL发现、无限页面、并行扫描、交互式UI。支持CI模式`unlighthouse-ci`，分数低于budget时构建失败。大站点用smart sampling只测代表性页面模板。（来源：https://github.com/harlan-zw/unlighthouse + https://unlighthouse.dev/）

  **知识点4：Playwright（89.8k stars，Microsoft）已超越Cypress成为E2E测试首选**——支持Chromium/Firefox/WebKit三引擎、TypeScript/JS/Python/Java/C#多语言、内置auto-wait（元素就绪才操作，无需手动sleep）、API测试内置（APIRequestContext）、trace viewer调试、并行sharding。周npm下载52M+，活跃贡献者720+。State of JS 2024首次超越Cypress使用率。（来源：https://github.com/microsoft/playwright + https://testdino.com/blog/playwright-market-share）

  **知识点5：Cypress（49.7k stars）仍有独特优势但局限明显**——优势：时间旅行调试（Test Runner可回看每步DOM状态）、初学者友好文档、实时重载。局限：仅JS/TS、iframe支持弱、多标签页/多域支持差、无原生移动端测试。企业采用率从Playwright的65%降至24%。新项目优先选Playwright。（来源：https://github.com/cypress-io/cypress + https://softwaretestpilot.com/blog/automation-testing/is-cypress-dead-playwright-market-share）

  **知识点6：Vitest（13k+ stars）是Vite生态的单元测试框架**——基于Vite的ESM原生支持、零配置、Watch模式极快（利用Vite HMR）、Jest兼容API（describe/it/expect）、内置coverage（v8或istanbul）。与Next.js集成需mock next/image/next/navigation。适合组件测试和工具函数测试，不适合E2E。（来源：https://github.com/vitest-dev/vitest + https://www.pistack.xyz/posts/2026-07-21-javascript-testing-frameworks-vitest-jest-playwright/）

  **知识点7：axe-core（7k+ stars，Deque）是行业标准无障碍测试引擎**——自动化检测90%以上WCAG 2.0/2.1/2.2 A/AA级问题，零误报设计（只报告确定的违规，不确定标记为incomplete）。支持@axe-core/playwright（Playwright集成）、@axe-core/cli（命令行）、@axe-core/puppeteer。是Lighthouse无障碍审计的底层引擎。（来源：https://github.com/dequelabs/axe-core + https://www.npmjs.com/package/axe-core）

  **知识点8：Pa11y（4.5k stars）是CLI无障碍测试工具，支持双引擎**——`npx pa11y https://example.com`单页扫描，支持axe和HTML_CodeSniffer两种runner（`--runner axe --runner htmlcs`）。Pa11y CI可批量扫描URL列表，Pa11y Dashboard提供Web界面每日自动测试+趋势图。输出JSON/CSV/HTML格式，适合CI门禁。（来源：https://github.com/pa11y/pa11y + https://pa11y.org/）

  **知识点9：@axe-core/playwright实现E2E测试中内嵌无障碍断言**——在Playwright测试导航到页面后调用`await AxeBuilder({ page }).analyze()`获取violations数组，用expect断言`violations.length === 0`。可配置`withTags(['wcag2a','wcag2aa'])`只检查特定标准，`disableRules(['color-contrast'])`排除已知问题。结果可附在Playwright HTML报告中。（来源：https://github.com/dequelabs/axe-core-npm + https://qaskills.sh/blog/axe-core-playwright-accessibility-testing-2026）

  **知识点10：eslint-plugin-jsx-a11y在编码阶段拦截无障碍问题**——基于AST静态分析JSX，检查alt文本、aria属性、标题层级、交互元素键盘可达性等。与axe-core互补：eslint-plugin-jsx-a11y在写代码时发现问题（左移），axe-core在运行时发现动态渲染问题。Next.js项目默认已包含此插件。（来源：https://github.com/jsx-eslint/eslint-plugin-jsx-a11y + https://sujeet.pro/articles/accessibility-testing-tooling）

  **知识点11：Plausible Analytics（28.9k stars）是隐私友好的轻量级GA替代**——无cookie、符合GDPR/CCPA、脚本<1KB（GA4约17KB）、实时仪表盘、开源可自托管。事件追踪用`plausible('event-name')`。适合不想用GA4但需要基础流量数据的站点。AIToolCrux已有GA4，可评估是否同时用Plausible做轻量备份。（来源：https://github.com/plausible/analytics + https://hellogithub.com/repository/plausible/analytics）

  **知识点12：@next/bundle-analyzer是Next.js官方bundle可视化工具**——`ANALYZE=true npm run build`生成report.html，treemap展示每个包及其依赖大小。用于发现大型依赖、决定是否拆分或懒加载。Next.js 16.1新增Turbopack版实验性Bundle Analyzer（`next experimental-analyze`）。AIToolCrux可定期运行识别bundle膨胀。（来源：https://nextjs.org/docs/app/guides/package-bundling + https://www.npmjs.com/package/@next/bundle-analyzer）

  **知识点13：size-limit是CI bundle预算门禁工具**——在.size-limit.json配置预算规则（如`"limit": "200 kB"`），CI中`size-limit`命令检查打包体积超预算则失败。支持webpack/rollup/esbuild，可按路径分别设限。AIToolCrux已有.size-limit.json（4条预算规则），应确保CI中运行。（来源：https://github.com/ai/size-limit + knowledge_code.md已记录）

  **知识点14：测试金字塔与工具选型决策**——单元测试（Vitest，快、覆盖工具函数/Hooks/纯组件）> 组件测试（Vitest+RTL，测交互行为）> E2E测试（Playwright，测关键用户旅程如搜索/导航/表单）。比例约70/20/10。不要用E2E测每个边界条件（慢且脆弱），不要用单元测试测跨页面流程。AIToolCrux当前有Playwright E2E，缺Vitest单元测试层。（来源：https://www.pistack.xyz/posts/2026-07-21-javascript-testing-frameworks-vitest-jest-playwright/ + 综合）

  **知识点15：工具组合推荐——AIToolCrux适用的CI质量门禁**——PR触发：①Vitest单元测试（快速反馈）②eslint+tsc（代码质量）③size-limit（bundle预算）④Lighthouse CI（性能/SEO/无障碍分数断言，对首页+工具页+文章页3个模板）⑤@axe-core/playwright（关键页面无障碍断言）。生产部署后：Unlighthouse全站扫描（每日定时）+ Plausible/GA4流量监控。形成左移（编码/PR阶段）+右移（生产监控）双层防护。（来源：综合Lighthouse CI/Unlighthouse/axe-core/Playwright官方文档）

  **落地计划（下次迭代执行）**：
  1. 知识点2+3（LHCI + Unlighthouse）→ 任务P2-QA-LHCI-SETUP：在.github/workflows/添加lighthouse-ci.yml，对首页/工具页/文章页3个模板做性能分数断言（performance>=80, seo>=90），生产部署后用unlighthouse-ci全站扫描
  2. 知识点7+9（axe-core + @axe-core/playwright）→ 任务P2-A11Y-AXE-CI：在现有Playwright E2E测试中添加axe-core断言，对首页和工具详情页检查WCAG 2.2 AA违规，violations>0则CI失败
  3. 知识点6+14（Vitest + 测试金字塔）→ 任务P2-QUALITY-VITEST-SETUP：初始化Vitest配置，为lib/工具函数（scoring/markdown/truncateAtWord）写单元测试，建立70%单元测试层
  4. 知识点12（Bundle Analyzer）→ 任务P1-PERF-BUNDLE-ANALYZE-001：运行ANALYZE=true npm run build生成报告，识别Top10最大依赖，制定懒加载/替换计划
  5. 知识点11（Plausible）→ 任务P2-GROWTH-PLAUSIBLE-EVAL：评估是否添加Plausible作为GA4的轻量备份（无cookie、脚本小），对比数据一致性
  6. 知识点15（工具组合）→ 任务P2-QA-CI-GATE：整合上述工具到CI workflow，形成PR阶段（Vitest+eslint+tsc+size-limit+LHCI）和生产阶段（Unlighthouse+axe-core）双层质量门禁

- [2026-09-20] 学习主题：IndexNow 协议完整实现规范（官方 indexnow.org FAQ + Bing 官方博客）
  1. IndexNow 是开放协议，一次请求同时推送给 Bing/Yandex/Naver/Seznam/Yep/Amazonbot 等所有参与搜索引擎，不需要逐个提交（来源：indexnow.org/faq + blogs.bing.com）
  2. API key 长度 8-128 字符，允许字符仅 [a-zA-Z0-9-]，不能有下划线/特殊符号（来源：indexnow.org/faq）
  3. key 文件必须 UTF-8 纯文本，文件名 = {key}.txt，文件内容 = key 本身（不能有额外换行/BOM），放在站点根目录 https://example.com/{key}.txt（来源：indexnow.org/faq + bing.com/indexnow/getstarted）
  4. 如果 key 文件不在根目录，提交时必须加 keyLocation 参数指向实际 URL；否则搜索引擎找不到文件会拒收（来源：indexnow.org/faq）
  5. 第一次提交会返回 HTTP 202（已接收，正在验证 key 文件）；验证通过后后续提交返回 200。不要把 202 当失败（来源：indexnow.org/faq）
  6. 批量提交用 POST 到 https://api.indexnow.org/indexnow，JSON body 格式 {host, key, keyLocation(可选), urlList:[...]}，单次最多 10,000 个 URL（来源：indexnow.org/faq）
  7. URL 必须按 RFC-3986 编码（:→%3A, /→%2F, ?→%3F, &→%26），GET 单条提交时 url 参数也要 encode（来源：indexnow.org/faq）
  8. 响应码含义：200=成功、202=首次验证中、400=格式错误（key/url 拼错）、422=域名不匹配/key 文件不可达/重复提交未变内容、429=触发限流（来源：indexnow.org/faq）
  9. 429 时必须读 Retry-After header 等待，至少 10 分钟后再重试；不要立即重试，否则会被持续限流（来源：indexnow.org/faq）
  10. 只在内容真的新增/更新/删除时提交，不要重复提交未变更的 URL——会浪费 crawl quota 且触发 422（来源：indexnow.org/faq）
  11. 404/410/301 重定向的 URL 也要提交，告诉搜索引擎更新索引/清理死链（来源：indexnow.org/faq）
  12. IndexNow 不适合全站批量提交（那是 sitemap 的活），它只负责"最近变更"的 URL；全站迁移后可以一次批量提交，日常用 sitemap 维护库存（来源：indexnow.org/faq）
  13. 每个子域名（blog.example.com）是独立 host，需要自己的 key 文件和 key，不能复用主域的 key（来源：indexnow.org/faq）
  14. IndexNow 不保证收录——只告诉搜索引擎"这个 URL 变了，快来爬"；是否收录还取决于内容质量、内链、noindex/robots 等（来源：indexnow.org/faq）
  15. 每次提交的 URL 都计入站点 crawl quota，所以不要浪费在 cosmetic 改动上（样式微调、纯文案改标点）（来源：indexnow.org/faq）
  落地计划：P1-INDEX-001 做 site: vs sitemap 对比找未收录页时，批量 POST 到 api.indexnow.org（一次最多 10k，我们只有 ~700 URL 一次搞定），用现有 /{key}.txt 文件，记录每个 URL 的 HTTP 响应码到 index_monitor.md；如果遇到 429 就按 Retry-After 等待。
- [2026-09-20] Google Article Schema 2026 官方规范（来源：developers.google.com/search/docs/appearance/structured-data/article，最后更新 2025-12-10）
  1. Article schema 没有 required 字段，但推荐字段：headline, image, datePublished, dateModified, author, publisher。
  2. image 必须是 repeated ImageObject 或 URL 数组；推荐多图（16:9、4:3、1:1 三种比例），最小像素量 width*height >= 50,000。我们用 1920x1080=2.07M 像素，远超阈值。
  3. image URL 必须 crawlable & indexable，不能是 logo 或 caption 占位图；必须用 Google Images 支持的格式（jpg/png/webp）。
  4. author 必须是 Person 或 Organization 类型，不要用 Thing；推荐加 author.url 或 sameAs 指向作者 bio 页。
  5. author.name 只放名字，不要把 jobTitle、honorific、"posted by" 塞进 name；jobTitle 单独字段。
  6. 多作者时 author 是数组，每个作者独立一个 Person 对象。
  7. datePublished / dateModified 必须 ISO 8601 带时区（如 2026-09-20T10:00:00+08:00），否则 Google 用 Googlebot 时区。
  8. publisher 必须是 Organization，logo 推荐 ImageObject 带 width/height（我们已加 512x512）。
  9. 多页文章（分页）canonical 要么指向单页要么指向 view-all，不要指向第 1 页。
  10. 订阅/付费墙内容要加 Subscription/PaywalledContent 结构化数据，否则 Google 可能不显示 rich result。
  11. 部署后必须用 Rich Results Test 验证，再用 URL Inspection tool 让 Google 重新抓取；sitemap 用 Search Console Sitemap API 自动提交。
  12. 违反 guideline（spammy markup）会触发 manual action，需要 reconsideration request。
  13. 我们本轮已落地：blog/[slug] Article schema image 改为 ImageObject 数组 1920x1080，author.url 指向 /about，publisher.logo 加 512x512。
  落地计划：下次迭代做 P2-BREADCRUMB-001（BreadcrumbList 审计）时，对照本规范第 8 条检查 publisher logo；做 P1-VERIFY-001 时用 Rich Results Test 验证 5 个工具页 Review schema。

### [2026-09-19] GitHub Actions CI/CD + Next.js 构建缓存 + Secrets安全 完整指南（GitHub官方Docs + Next.js官方Docs）

1. **定时任务默认UTC时区**：GitHub Actions `on.schedule` 用POSIX cron，默认在UTC运行。要指定本地时区，用 `timezone: Asia/Shanghai`（IANA格式）。最短间隔5分钟。来源：https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
2. **整点高峰会延迟甚至丢弃任务**：GitHub官方明确"High load times include the start of every hour. If the load is sufficiently high enough, some queued jobs may be dropped"。不要把cron设为 `0 * * * *`（整点开跑），错开到 `01,31 * * * *` 避开整点。来源：https://docs.github.com/en/actions/how-tos/troubleshoot-workflows
3. **定时任务跑的是默认分支最新commit**：`Scheduled workflows run on the latest commit on the default branch`。在feature branch上改了workflow必须merge到main才生效。来源：https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
4. **actions/setup-node 自动缓存npm依赖**：用 `actions/setup-node@v4` 时加 `cache: 'npm'`，自动读 package-lock.json 并缓存 ~/.npm，不需要手动写 actions/cache。来源：https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/caching-dependencies-to-speed-up-workflows
5. **Next.js构建缓存必须单独缓存 .next/cache**：除了node_modules，还要缓存 `${{ github.workspace }}/.next/cache`，key用 `runner.os + lockfile hash`。二次构建Turbopack/webpack复用缓存，构建时间降50-70%。来源：https://nextjs.org/docs/app/guides/ci-build-caching
6. **Cache key设计：restore-keys模糊匹配**：主key精确匹配（lockfile hash），restore-keys前缀匹配。依赖没变时命中缓存，依赖变了时至少restore到上次缓存加速npm install。来源：https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
7. **仓库缓存上限10GB，超了自动LRU淘汰**：每个repo所有cache加起来默认10GB上限，超了自动删最老的。不要缓存node_modules（太大且actions/setup-node已经管了），只缓存.npm和.next/cache。来源：https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository
8. **绝对不要把JSON blob当Secret存**：GitHub官方警告"Never use structured data as a secret"，因为日志脱敏靠精确字符串匹配，JSON里换行/空格一变就漏出来。每个敏感值单独存一个Secret。来源：https://docs.github.com/en/actions/reference/security/secure-use
9. **PAT遵循最小权限原则**：只读仓库就给 `contents: read`，不要给 `repo` 全权限。PAT过期了workflow会401失败，要定期rotate。来源：https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure
10. **Secret Scanning + Push Protection 要开**：GitHub免费提供secret scanning，push protection会在你把token推到repo时直接拦住。Settings→Code security and analysis里开启。来源：https://docs.github.com/en/get-started/learning-to-code/storing-your-secrets-safely
11. **公开repo的Actions分钟数免费无限**：GitHub托管runner对public repo免费，私有repo每月2000分钟。我们repo是public的所以免费。来源：https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions
12. **workflow失败排查三板斧**：① 看Actions tab红色job展开失败step日志 ② 确认runner版本（ubuntu-latest会自动升级偶尔breaking）③ 用 `node-version-file: '.nvmrc'` 锁定Node版本。来源：https://docs.github.com/en/actions/how-tos/troubleshoot-workflows
13. **Next.js 16.3+ Turbopack构建缓存默认开启**：`turbopackFileSystemCacheForBuild` 在v16.3默认true。如果CI每次fresh runner不保留.next/cache，在next.config里设 `turbopackFileSystemCacheForBuild: false` 避免写了用不上的缓存。来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache
14. **workflow_dispatch手动触发按钮**：workflow文件加 `on: workflow_dispatch:` 后，Actions页面出现"Run workflow"按钮，失败修复后不用等下一个cron周期直接手动跑验证。来源：https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
15. **健康检查workflow模式**：定时workflow失败时在job末尾加 `if: failure()` 的step，用curl把告警发到QQ邮箱/webhook。不要每次成功都发邮件，只在failure时发。来源：https://docs.github.com/en/actions/reference/security/secure-use

**落地计划（下次迭代执行）**：
- 任务A：检查现有3个workflow（gsc-fetch、context-update、uptime-monitor），把cron时间从整点错开5-10分钟，避免GitHub高峰丢弃
- 任务B：给Next.js构建workflow加actions/setup-node的cache:npm + .next/cache缓存，把构建时间降下来
- 任务C：检查GCP service account JSON是不是单独存为一个Secret，不要和其他key拼在一个JSON里
- 任务D：在Actions Settings里确认Secret Scanning和Push Protection已开启
- 任务E：给失败的workflow加workflow_dispatch按钮，下次修复后能手动触发验证不用等cron

### [2026-09-19] Google Review Snippet / AggregateRating Schema 官方规范（Google Search Central）

来源：https://developers.google.com/search/docs/appearance/structured-data/review-snippet （最后更新 2026-07-24）

**核心知识点（15个）：**

1. **AggregateRating 必须有 ratingCount 或 reviewCount**：Google 文档明确"At least one of ratingCount or reviewCount is required"。只有1条评论时 ratingCount="1" 虽然语法上满足必填，但语义上不满足"many people"要求。
2. **AggregateRating 是"多人评分的聚合"**："Make sure to mark up an aggregate evaluation of an item by **many people** with schema.org/AggregateRating"。单条编辑评测不应该用 AggregateRating。
3. **正确模式：多条 Review[] + 一个 AggregateRating**："If you include multiple individual reviews, also include an aggregate rating of the individual reviews"。不是单条 Review 里同时嵌 reviewRating 和 aggregateRating。
4. **单条评测正确模式**：只用 Review + reviewRating + author + itemReviewed，不加 aggregateRating。本次 P0-001 修复就是这个模式。
5. **SoftwareApplication 是合法的 itemReviewed 类型**：Google 支持列表明确包含 SoftwareApplication。
6. **reviewRating.ratingValue 支持小数**：用点不用逗号（4.4 不是 4,4）。
7. **bestRating/worstRating 可省略**：省略时 bestRating 默认 5，worstRating 默认 1。我们用 1-10 量表所以必须显式写。
8. **author 必须是人名（<100字符）**："The reviewer's name must be a valid name"。"50% off until Saturday" 这种不算。我们用 "Alex Chen" 是对的。
9. **review 内容必须在页面上可见**："It must be immediately obvious to users that the page has review content"。不能藏在 hidden div 里。
10. **不能从其他网站聚合评论**："Don't aggregate reviews or ratings from other websites"。我们只展示自己编辑团队的评测，合规。
11. **不能造假/激励评论**："Don't include fake or undisclosed incentivized reviews"。联盟链接不影响评分（footer 已声明）。
12. **自评分政策（self-serving）**：被评测实体不能控制自己的评测。这适用于 LocalBusiness/Organization，不适用于第三方评测站评测 SoftwareApplication。我们是第三方评测站，合规。
13. **datePublished 推荐字段**：ISO 8601 格式。我们已用 tool.lastUpdated。
14. **验证工具**：Rich Results Test（查富摘要资格）+ Schema Markup Validator（通用 schema 验证）。
15. **部署后要等 Google 重新抓取**："Allow time for re-crawling and re-indexing. It may take several days after publishing a page for Google to find and crawl it."

**落地计划：**
- P1-001 已完成：移除了工具页 Review schema 里的 aggregateRating，只保留 reviewRating。下次用 Rich Results Test 验证 /tools/chatgpt 是否还报错误。
- 下次迭代：用 Google Rich Results Test 批量抽查 5 个工具页，确认 Review rich result 资格恢复。
- 如果未来要加用户评分功能，需要实现 Review[] 数组 + 真实的 ratingCount（>=2），才能同时显示 AggregateRating。

- [2026-09-19] **Next.js Partial Prerendering (PPR) + Cache Components 完整指南 — 权威来源：Next.js官方docs + Vercel官方docs**

  1. **PPR是什么**：Partial Prerendering在同一路由里同时组合静态shell和动态流式内容。build时生成静态HTML shell + 序列化的postponed state blob；请求时shell立即从CDN发出，动态部分流式填充。来源：https://nextjs.org/docs/app/getting-started/partial-prerendering
  2. **Next.js 16把PPR转正**：从实验性 `experimental.ppr` 变成Cache Components默认模型。升级到Next.js 16后删掉旧flag，在next.config里开 `cacheComponents: true`。来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents
  3. **静态shell定义**：在任何async work resolve之前渲染的所有内容 = layouts、navigation、`<Suspense>`的fallback UI。这些在build时prerender，请求时从edge CDN立即发出（~32-65ms TTFB）。来源：https://nextjs.org/docs/app/guides/streaming
  4. **动态holes = `<Suspense>`边界**：依赖request-time数据的组件必须包在`<Suspense>`里，fallback进入静态shell，真正的数据在请求时并行stream进来。多个Suspense边界并行加载。来源：https://nextjs.org/docs/app/getting-started/cache-components
  5. **`use cache`指令**：在组件/函数顶部写 `"use cache"`，输出会被缓存并进入静态shell。适合所有用户共享的数据（如我们的工具列表、分类导航）。来源：https://nextjs.org/docs/app/api-reference/directives/use-cache
  6. **新鲜数据不要use cache**：需要每次请求都新鲜的数据（如个人化推荐），用`<Suspense>`包，不要加use cache。官方明确：async API/db/fetch需要fresh data时，不use cache，包Suspense。来源：https://nextjs.org/docs/app/getting-started/caching
  7. **loading.js自动成为Suspense边界**：Next.js里放一个 `loading.tsx` 文件就自动把整个segment包进`<Suspense>`，它的loading UI就是静态shell的fallback。来源：https://preview.nextjs.org/docs/app/guides/building
  8. **SEO好处**：静态shell是完整HTML，立即发给Googlebot，不需要等JS hydration。这解决了"CSR/SSR内容需要爬虫等JS"的老问题——Googlebot直接看到shell里的所有内容。来源：https://nextjs.org/docs/app/getting-started/caching
  9. **LCP好处**：LCP元素如果在静态shell里（如hero图、H1、产品图），它立即paint，LCP从几百ms降到几十ms。官方数据：把LCP元素放进shell后LCP从~650ms降到65ms。来源：https://nextjs.org/docs/app/guides/streaming
  10. **postponed state是什么**：build时序列化的RSC payload blob，客户端导航时hydrate用。直接访问URL时发HTML shell，客户端内部跳转时用postponed state。来源：https://preview.nextjs.org/docs/app/guides/ppr-platform-guide
  11. **ISR + Cache Components**：即使URL不在generateStaticParams里，第一次访问也能拿到即时shell（App Shell模式），动态内容stream进来。这对我们533个工具页+大量长尾页特别有用。来源：https://preview.nextjs.org/docs/app/guides/incremental-static-regeneration-cache-components
  12. **Vercel官方确认PPR替代Edge SSR**：PPR不阻塞serverless cold start的TTFB，比Edge SSR更省资源。Vercel的frontend cloud直接从edge cache发shell。来源：https://vercel.com/docs/frameworks/full-stack/nextjs
  13. **静态vs动态是光谱不是二元**：Next.js 16的渲染哲学——一个页面可以既有静态shell、又有cached function、又有动态个人化部分。不再需要"全站SSG或全站SSR"的选择。来源：https://nextjs.org/docs/app/guides/rendering-philosophy
  14. **迁移要点**：① 升级Next.js到16 ② next.config开 `cacheComponents: true` ③ 删 `experimental.ppr` flag ④ 检查每个路由有没有Suspense边界/loading.tsx ⑤ fresh数据的组件包Suspense，shared数据加use cache。来源：https://nextjs.org/docs/app/guides/migrating-to-cache-components
  15. **不阻塞主线程**：因为shell是CDN直接发的HTML，不经过serverless function，cold start不影响首屏。这对Vercel免费额度紧张的我们特别友好——shell不消耗ISR reads/serverless invocation。来源：https://vercel.com/resources/how-vercel-improves-your-websites-search-engine-ranking

  **落地计划（下次迭代执行）**：
  - 任务A：评估Next.js 16升级可行性（当前我们是Next.js 14.2.5），查Breaking Changes和我们用的依赖兼容性，出一份升级checklist
  - 任务B：在不升级的前提下，先用现有Next.js 14的Suspense + loading.tsx模式，把/blog/[slug]和/tools/[slug]里的非关键数据（Related Tools、FAQ手风琴）包进Suspense，让首屏HTML立即发出
  - 任务C：把tools.json里的静态工具列表用React.cache（不是use cache，Next.js 14版）包一层，减少重复render
  - 任务D：Lighthouse跑一次，确认我们LCP元素（H1、hero screenshot）已经在首屏HTML里，不需要客户端JS


- [2026-09-19] **Core Web Vitals: INP (Interaction to Next Paint) 完整优化指南 — 权威来源：Google官方web.dev/Codelabs + React官方docs + Vercel官方blog**

  1. **INP是什么**：INP测量用户交互（点击/点按/键盘）到浏览器下一帧绘制的延迟。2024年3月12日正式替代FID成为第三个Core Web Vital。来源：https://web.dev/articles/inp
  2. **INP阈值（p75真实用户）**：Good ≤200ms；Needs Improvement 200-500ms；Poor >500ms。Google Web Vitals团队数据显示INP从500ms优化到200ms可提升用户参与度22%。来源：https://web.dev/articles/evolving-inp-threshold
  3. **INP测量所有交互，不是只测第一次**：与FID只测首次输入不同，INP跟踪整个页面生命周期的所有click/tap/keyboard事件，报告最差的（p98）。来源：https://codelabs.developers.google.com/understanding-inp
  4. **INP的三个阶段**：① Input Delay（事件被浏览器接收前的排队延迟）② Event Processing Duration（事件处理器执行时间）③ Presentation Delay（浏览器绘制下一帧前的渲染时间）。三个阶段都要优化。来源：https://codelabs.developers.google.com/understanding-inp
  5. **Long Task >50ms是INP头号杀手**：任何阻塞主线程超过50ms的任务都会导致输入排队。优化方法：把长任务切成<50ms的小块，块之间用yield让浏览器绘制。来源：https://web.dev/articles/optimize-inp
  6. **scheduler.yield()（Chromium 115+）**：新API，把控制权交回浏览器立即绘制，然后恢复任务。比setTimeout更精确。降级方案：`if ('scheduler' in window && 'yield' in window.scheduler) window.scheduler.yield(); else new Promise(r => setTimeout(r, 0))`。来源：https://developer.chrome.com/docs/web-platform/scheduler-yield
  7. **React startTransition/useTransition（最重要的React优化）**：把非紧急的state更新包在startTransition里，React会把它们标记为可中断，浏览器优先响应用户输入。Vercel官方blog确认：如果慢操作是由state change引起的，包startTransition往往是最大单点修复。来源：https://react.dev/reference/react/useTransition ; https://vercel.com/blog/demystifying-inp-new-tools-and-actionable-insights
  8. **useDeferredValue**：把昂贵的派生渲染延迟到输入响应之后。适合搜索过滤、长列表渲染等场景——先响应用户输入，再慢慢渲染过滤结果。来源：https://react.dev/reference/react/useDeferredValue
  9. **web-vitals attribution build + LoAF API**：`web-vitals/attribution`构建用Long Animation Frames API精确告诉你哪个script/哪个event listener导致了慢INP，而不是只给一个数字。我们已部署WebVitalsReporter，下次可升级到attribution build拿到具体元凶。来源：https://codelabs.developers.google.com/measuring-inp
  10. **requestIdleCallback推迟非紧急工作**：analytics上报、logging、prefetching、预渲染等可以放到浏览器空闲时做，不阻塞交互。降级用setTimeout。来源：https://web.dev/articles/optimize-inp#defer-non-essential-work
  11. **事件委托减少监听器开销**：在父元素上放一个listener代替给每个子元素放listener，减少input delay。尤其适合我们工具页的Related Tools、Category列表。来源：https://web.dev/articles/optimize-inp#defer-non-essential-work
  12. **保持DOM小、避免强制reflow（layout thrashing）**：Presentation Delay和DOM复杂度正相关。避免read-write-read模式（循环里读offsetWidth再改style），用CSS containment隔离大列表。我们533个工具页每个渲染12个相关工具卡片，DOM不算大但要注意。来源：https://web.dev/articles/optimize-inp#reduce-presentation-delay
  13. **Server Components减少客户端JS**：Client Component越少，hydration越快，input delay越低。我们的SSG已帮大忙，但FAQ手风琴、CTA追踪、Newsletter表单都是'use client'组件，要确保它们是小型leaf组件，不拖累整页hydration。来源：https://nextjs.org/docs/app/building-your-application/rendering/server-components
  14. **Debounce/Throttle输入处理器**：搜索框、slider等不要每次keystroke都跑重活，debounce 100-300ms。来源：https://web.dev/articles/optimize-inp#defer-non-essential-work
  15. **Lighthouse TBT ≠ INP**：Lab工具（Lighthouse）测的是Total Blocking Time，不是真实INP。必须用RUM（web-vitals库）收集真实用户数据。我们已在WebVitalsReporter里onINP上报GA4，下一步要去GSC的Core Web Vitals报告看我们真实p75 INP是多少。来源：https://web.dev/articles/inp#what-is-inp

  **落地计划（下次迭代执行）**：
  - 任务A：把WebVitalsReporter升级到web-vitals/attribution build，拿到具体哪个client component导致慢INP（不改业务代码，只换import路径+加attribution:true）
  - 任务B：检查'use client'组件清单（FAQ手风琴、AffiliateCTA tracking、NewsletterSignup、WebVitalsReporter），把非紧急的trackCtaClick/analytics上报包进requestIdleCallback，不阻塞click事件
  - 任务C：GSC Core Web Vitals报告里查我们真实p75 INP，确认是Good/Needs Improvement/Poor，再决定要不要做startTransition
  - 任务D：Category页和Tools列表的渲染，如果单次渲染>50ms，用React.memo + useDeferredValue优化


- 2026-09-19 **Next.js Image Optimization + Font Optimization (App Router) — 权威来源：Next.js官方docs + Vercel官方docs**

  1. **next/image自动优化**：自动转WebP/AVIF格式，按设备尺寸返回正确大小的图，内置懒加载，用width/height防止CLS。来源：https://nextjs.org/docs/app/getting-started/images
  2. **`<img>`原生标签完全绕过Vercel图片优化管线**：直接用`<img>`不会走Next.js Image Optimization，不会自动压缩/转WebP/生成srcset。当前项目工具截图用的是原生`<img>`，这是~100个工具页>500KB的主要原因之一。来源：https://vercel.com/docs/image-optimization
  3. **`priority` prop = LCP图片preload**：首屏LCP图片（如工具页顶部screenshot）必须加`priority`，Next.js会自动加preload link标签，大幅提升LCP。不加的图片默认懒加载。来源：https://nextjs.org/docs/app/api-reference/components/image
  4. **`sizes` prop是关键，不是可选的**：没有`sizes`，浏览器默认按100vw选图，导致手机上下载2x甚至3x大的图。必须按实际渲染宽度设置，如sizes='(max-width: 768px) 100vw, 800px'。来源：https://nextjs.org/docs/app/api-reference/components/image#sizes
  5. **`unoptimized` prop用于SVG/GIF/小图(<1KB)**：对不需要优化的图（如SVG图标），加`unoptimized`跳过Vercel优化CPU，节省构建时间和函数调用。来源：https://nextjs.org/docs/app/api-reference/components/image#unoptimized
  6. **`quality` prop控制压缩质量**：默认75，截图类图片可降到60-70，视觉差异极小但文件体积减30-40%。来源：https://nextjs.org/docs/app/api-reference/components/image#quality
  7. **`fill` prop需要父容器position:relative**：当图片占满父容器时用`fill`，但父元素必须有明确的position:relative和尺寸，否则图片溢出。来源：https://nextjs.org/docs/app/api-reference/components/image#fill
  8. **本地图片（import的）不需要手动写width/height**：Next.js构建时自动检测尺寸。远程图片（在next.config.mjs配置remotePatterns的）必须手动传width/height。来源：https://nextjs.org/docs/app/getting-started/images
  9. **next/font/google自动自托管Google Fonts**：构建时下载字体文件，和静态资源一起serve，浏览器不向fonts.googleapis.com发请求，消除额外RTT，改善FCP/LCP。来源：https://nextjs.org/docs/app/getting-started/fonts
  10. **font-display必须用optional或swap**：Next.js官方警告不要用auto/block/fallback。optional对自定义字体最优（避免FOIT），swap对内容站点可接受。来源：https://nextjs.org/docs/messages/google-font-display
  11. **Variable Fonts推荐**：一个文件覆盖所有字重，不用为每个weight单独加载。来源：https://nextjs.org/docs/app/getting-started/fonts
  12. **next/font用CSS size-adjust实现零布局偏移**：字体文件构建时被调整metric，切换字体时不会导致文字跳动。来源：https://vercel.com/docs/frameworks/nextjs
  13. **next/font在build时内联font-face CSS**：不产生额外字体CSS网络请求，直接内联到HTML中。来源：https://nextjs.org/learn/seo/fonts
  14. **Vercel Image Optimization免费额度**：Pro计划每月有优化图额度。用unoptimized跳过不需要的图，用next.config.mjs的deviceSizes和imageSizes控制生成的尺寸变种，避免浪费。来源：https://vercel.com/docs/image-optimization
  15. **当前项目差距**：(a)工具页screenshot用原生img未优化→应迁到next/image；(b)需确认app/layout.tsx是否用next/font，如果还用link引Google Fonts要迁移；(c)首屏screenshot需加priority；(d)所有图片需加正确sizes。

  **落地计划（下次迭代执行）**：
  - 任务A：把app/tools/[slug]/page.tsx里的原生img截图改为next/image，加priority和sizes='(max-width: 768px) 100vw, 860px'，quality=70
  - 任务B：检查app/layout.tsx是否用next/font，如未用则迁移Inter字体
  - 任务C：SVG图标组件加unoptimized跳过图片优化
  - 任务D：在next.config.mjs配置deviceSizes减少多余的尺寸变种


- [2026-09-18] **学到：content-visibility: auto (CSS Containment Module Level 2)** — web.dev/Chrome团队官方性能优化技巧。对首屏以下的内容（Alternatives、Similar Tools、Compare等section）设置`content-visibility: auto`，浏览器会跳过渲染离屏内容，直到用户滚动到附近。配合`contain-intrinsic-size: auto 400px`预留空间防止CLS。实测对长列表/长文章页面LCP改善20-50%。来源：https://web.dev/articles/content-visibility。已落地：在app/tools/[slug]/page.tsx的4个below-fold section上加了cv-auto类，globals.css定义了.cv-auto工具类。下次可用到：Blog文章页的FAQ和Related Posts section、Category页的ToolList后半部分。

- [2026-09-18] **踩坑：Vercel SSG部署700+页面需要3-5分钟才能全量上线** — 提交commit后90秒检查，cv-auto还没出现在HTML里；等了270秒（4.5分钟）才确认8个cv-auto类出现在/tools/chatgpt上。经验：SSG全量构建比ISR慢，验证线上时至少等3分钟再查，不要90秒就判定部署失败。
- [2026-09-18 14:41] Blog post dual H1 root cause: markdown content starts with '# Title' AND template renders its own <h1>. Fix: downgrade markdown # to ## in posts.json.
- [2026-09-18 14:41] Vercel SSG rebuild delay: after committing data files, live site may show old content for 3-5 minutes while 700+ pages rebuild.
- [2026-09-18 14:41] GitHub Trees API 5-step flow works reliably from China without git push.

- [2026-09-16] Next.js App Router: if root layout sets `alternates.canonical` to homepage, child pages WITHOUT their own canonical inherit it. Must explicitly set `alternates.canonical` on every page that should be self-referencing.
- [2026-09-16] 308 redirects in next.config.mjs: `permanent: true` generates 308 (Next.js default). Works for old URL 404 fixes.
- [2026-09-16] Ahrefs "non-canonical pages" = pages in sitemap whose canonical tag points elsewhere. Root layout canonical bug can affect 50+ pages at once.
- [2026-09-16] PowerShell: `$variable:` in strings is parsed as a variable reference. Use `${variable}:` or write Python scripts instead.

- [2026-09-16] **GSC "应指定ratingCount或reviewCount"错误修复**: 工具页inline Review的itemReviewed SoftwareApplication需要单独加aggregateRating，即使ProductSchema组件已经传了ratingValue。Google会优先读取itemReviewed里的schema而不是独立的SoftwareApplication节点。教训：Review.itemReviewed里的嵌套schema必须自包含所有必需字段，不能依赖外部兄弟schema。
- [2026-09-16] **PowerShell $HOME变量只读**: 在PowerShell脚本中不要用$home作为变量名，它是内置只读变量，会报SessionStateUnauthorizedAccessException。改用$homepage或$hp。
- [2026-09-16] **Python多行字符串在dict中**: GitHub commit message如果有多行，不要直接在dict value里写换行字符串，先赋值给变量再引用。
- [2026-09-16] **重复SoftwareApplication诊断**: 工具页同时有inline Review（含itemReviewed.SoftwareApplication）和ProductSchema组件（独立SoftwareApplication），Google看到两个rating节点判重复。修复：删除ProductSchema调用，把brand/image/url合并到inline Review的itemReviewed里。教训：一个页面只保留一个产品实体schema，不要同时用组件+inline输出同一个实体。
- [2026-09-16] **Review author类型**: Google偏好Person。inline Review已用Person（Alex Chen），但blog Article schema和ComparisonSchema组件还用Organization。统一改为Person + jobTitle。
- [2026-09-16] **工具页schema itemReviewed.image 404修复**: 之前inline Review的itemReviewed.image硬编码为`/screenshots/${slug}.webp`，但533个工具中只有20个有真实截图文件，其余全部404。Google会把缺失image视为schema质量问题。修复：把toolScreenshotMap提到模块级，itemReviewed.image改为`toolScreenshotMap[slug] ? 真实路径 : /api/og`动态生成图，保证每个工具都有有效image URL。来源：Next.js官方Metadata文档(docs.nextjs.org)。
- [2026-09-16] **Next.js opengraph-image文件约定**: Next.js 13.3+支持`app/tools/[slug]/opengraph-image.tsx`文件约定，配合generateStaticParams在build时预生成所有OG图（SSG），比`/api/og`路由在请求时渲染更省Vercel函数调用。但我们已经用/api/og动态生成，短期不迁移；长期若OG图请求量大可考虑。来源：nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image。
- [2026-09-16] **llms.txt规范（GEO/AEO）**: 官方规范在llmstxt.org，由Answer.AI(Jeremy Howard)2024年9月提出。必须有：H1项目名 + blockquote一句话总结；可选：H2分节 + Markdown链接列表（`- [Title](url): desc`）。支持情况：Anthropic和Perplexity说他们读；Google说不影响Search；OpenAI GPTBot会抓但不承诺用。定位是"内容地图"不是爬虫控制文件。低风险长期投资。来源：llmstxt.org + indexlab.ai 2025年10月状态更新。验证通过：我们刚加的/llms.txt线上200，结构符合规范。
- [2026-09-16] **Vercel部署延迟**: GitHub API提交后，即使GitHub上文件已是新内容，Vercel CDN边缘节点可能要2-3分钟才更新。保险做法：提交后等90秒验证，若还是旧内容，再等60-90秒重试，最多3次。不要第一次验证失败就慌。

## 🔒 两道保险机制（每次迭代必须遵守，不能反）

### 保险1：改完任务同步更新 audit_findings.md
- 每次改完 audit_findings.md 里的一条问题，**当场把该条目标记为 `【已完成-YYYY-MM-DD】`**
- 这样窗口4下次跑不会重复加同一条
- 标记方式：在原问题那行末尾加 `✅ 已完成 2026-09-16`，不要删原问题（保留历史）

### 保险2：先验证线上生效，再改 state.json（顺序绝对不能反）
1. 写 Python 改代码
2. `npx tsc --noEmit` 编译通过
3. GitHub Trees API 提交（拿到 commit sha）
4. **等 75 秒 Vercel 部署**
5. **Invoke-WebRequest 线上验证修改真的生效**（HTTP 200 + 内容包含新标记）
6. 验证失败 → 等 60 秒重试，最多 3 次
7. **确认线上 OK 后**，才把 state.json 里对应任务标记为 completed
8. 最后写 iteration_log.json

**反例（禁止）**：先改 state.json 说"已完成"，再等部署。部署失败 = 状态不一致 = 下次永远跳过这个问题。

---

## 待补充

### [2026-09-26] GitHub Actions安全加固与OIDC无密钥认证最佳实践

**知识点1：OIDC概述——消除长期云密钥**
GitHub Actions支持OpenID Connect（OIDC），工作流可直接向云提供商（AWS/Azure/GCP）认证，无需将云凭证存储为长期GitHub Secrets。OIDC用短期令牌替代静态密钥，是GitHub官方推荐的云部署认证方式。核心优势：无需密钥轮换、减少攻击面、云提供商侧可精细控制授权。（来源：https://docs.github.com/en/actions/concepts/security/openid-connect、https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers）

**知识点2：OIDC工作原理——JWT令牌交换**
GitHub OIDC Provider为每次workflow run生成签名JWT（包含issuer=token.actions.githubusercontent.com、subject=repo:org/repo:ref:refs/heads/main、audience、repository_owner等claim）。工作流用`permissions: id-token: write`请求JWT，云提供商验证JWT签名和claim后颁发短期云访问令牌（通常1小时有效期）。整个过程无需任何静态密钥。（来源：https://docs.github.com/en/enterprise-cloud@latest/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect、https://docs.github.com/en/actions/concepts/security/openid-connect）

**知识点3：permissions最小权限配置**
OIDC需要两个权限：`id-token: write`（请求JWT令牌）和`contents: read`（actions/checkout需要）。应在workflow或job级别显式设置permissions，遵循最小权限原则。GitHub已将GITHUB_TOKEN默认权限改为只读，但仍应显式声明。常见权限：`contents: read/write`（代码读写）、`packages: write`（GHCR推送）、`issues: write`（issue操作）、`pull-requests: write`（PR操作）。不要使用`write-all`。（来源：https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services、https://github.blog/enterprise-software/devops/building-organization-wide-governance-and-re-use-for-ci-cd-and-automation-with-github-actions/）

**知识点4：AWS OIDC配置——IAM Identity Provider + Role**
AWS端配置步骤：①在IAM创建OIDC Identity Provider，URL=`https://token.actions.githubusercontent.com`，Audience=`sts.amazonaws.com`（或sts.cn-north-1.amazonaws.com.cn）②创建IAM Role，信任策略指定Principal为OIDC provider，Condition用`StringEquals`限制audience，用`StringLike`限制subject为特定仓库分支③workflow中用`aws-actions/configure-aws-credentials@v4`，指定`role-to-assume`和`aws-region`，action自动用OIDC令牌assume role。（来源：https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services、https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html）

**知识点5：AWS信任策略——用sub条件限制仓库和分支**
AWS IAM Role信任策略中必须用`token.actions.githubusercontent.com:sub`条件键限制可assume role的实体。格式：`"Condition": {"StringLike": {"token.actions.githubusercontent.com:sub": "repo:org-name/repo-name:ref:refs/heads/main"}}`。必须指定GitHub组织名（不允许通配符），仓库和分支可用通配符（如`repo:org/*:ref:refs/heads/*`）。这是防止其他GitHub仓库冒用你的role的关键安全控制。（来源：https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html、https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html）

**知识点6：GCP OIDC配置——Workload Identity Federation**
GCP端配置步骤：①创建Workload Identity Pool②创建OIDC Provider，issuer=`https://token.actions.githubusercontent.com`，属性映射`attribute.repository=assertion.repository`、`attribute.ref=assertion.ref`③为服务账号授予Workload Identity User角色，绑定条件`attribute.repository=="org/repo"`④workflow中用`google-github-actions/auth@v2`，指定`workload_identity_provider`和`service_account`。GCP支持自定义claim属性映射（AWS不支持）。（来源：https://docs.github.com/en/enterprise-server@3.9/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-google-cloud-platform）

**知识点7：Azure OIDC配置——Managed Identity + Federated Credential**
Azure端配置步骤：①创建User-Assigned Managed Identity②在Identity中添加Federated Credential，选择"GitHub Actions deploying Azure resources"，指定Organization、Repository、Branch（或Environment/Tag）③为Identity授予Azure资源的Contributor/Reader角色④workflow中用`azure/login@v3`，指定`client-id`（Managed Identity的client ID）、`tenant-id`、`subscription-id`，无需client-secret。Azure的Federated Credential直接绑定repo+branch。（来源：https://learn.microsoft.com/en-us/Azure/Azure-functions/functions-how-to-github-actions、https://learn.microsoft.com/en-us/samples/azure-samples/github-terraform-oidc-ci-cd/github-terraform-oidc-ci-cd/）

**知识点8：短期凭证的安全优势**
OIDC的核心安全优势：①JWT令牌由GitHub签名，云提供商验证，无法伪造②云访问令牌有效期通常1小时（AWS默认1小时，可配置最短15分钟），即使泄露也无法长期使用③无需存储和轮换静态密钥，消除密钥泄露风险④每次运行的JWT包含唯一的run_id和run_attempt，可审计追踪⑤云提供商侧可基于branch/environment/repo精细授权。对比静态密钥：一旦泄露可无限期使用直到手动轮换。（来源：https://docs.github.com/en/actions/concepts/security/openid-connect、http://raw.githubusercontent.com/github/awesome-copilot/main/instructions/github-actions-ci-cd-best-practices.instructions.md）

**知识点9：第三方Action锁定commit SHA**
安全最佳实践：第三方Action始终用完整commit SHA引用（`uses: actions/checkout@a5ac7e51b41094c92402da3b243769063920fc8`），而非tag（`@v4`）或branch（`@main`）。因为tag可被仓库维护者重新指向不同commit，branch会随推送变化，只有commit SHA是不可变的。项目已在第86轮将CI第三方action锁定commit SHA+Dependabot。对官方actions（actions/开头）风险较低，但对社区第三方action必须锁定SHA。（来源：https://docs.github.com/en/actions/reference/security/secure-use、https://github.blog/enterprise-software/devops/building-organization-wide-governance-and-re-use-for-ci-cd-and-automation-with-github-actions/）

**知识点10：Secrets安全管理**
Secrets管理最佳实践：①GitHub自动mask日志中的secrets值，但不要用`echo ${{ secrets.X }}`自定义输出（可能绕过mask）②使用Environment Secrets而非Repository Secrets，将生产密钥限制在production环境③不要在fork的PR中启用secrets（pull_request_target事件中secrets可用，需谨慎）④定期轮换secrets⑤用GitHub Secret Scanning自动检测代码中泄露的API密钥⑥不要将secrets传递给不受信任的第三方action。（来源：https://docs.github.com/en/actions/reference/security/secure-use）

**知识点11：Dependabot自动更新Action版本**
配置`.github/dependabot.yml`，`package-ecosystem: "github-actions"`，Dependabot会定期检查所有`uses:`引用的Action是否有新版本，自动创建PR更新。配合commit SHA锁定：Dependabot更新时会将SHA更新到新版本对应的SHA。设置`open-pull-requests-limit`控制并发PR数，`schedule.interval`设置检查频率（weekly推荐）。项目已配置Dependabot更新GitHub Actions。（来源：https://docs.github.com/en/actions/reference/security/secure-use、https://github.blog/enterprise-software/devops/building-organization-wide-governance-and-re-use-for-ci-cd-and-automation-with-github-actions/）

**知识点12：Environment保护规则——部署审批门控**
GitHub Environments支持保护规则：①Required reviewers：部署前需要指定人员批准（生产环境必须）②Wait timer：部署前等待时间（如30分钟冷却期）③Deployment branches：限制只有特定分支（如main）可部署到该环境④Custom deployment protection rules：集成第三方安全检查。生产环境deployment应配置required reviewers，防止自动部署到生产。项目可添加production环境限制Vercel部署。（来源：https://docs.github.com/en/actions/reference/security/secure-use、https://docs.github.com/en/enterprise-cloud@latest/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect）

**知识点13：Shell注入防护——环境变量传递不受信任输入**
不要将不受信任的输入（issue标题、PR正文、评论内容、外部API返回）直接内联到`run`脚本中，因为这些内容可能包含`;`、`&&`、`$(...)`等shell元字符导致注入攻击。正确做法：通过环境变量传递，`env: INPUT_TITLE: ${{ github.event.issue.title }}`，然后在脚本中用`"$INPUT_TITLE"`引用。PowerShell同理用`$env:INPUT_TITLE`。这是GitHub官方安全指南明确推荐的做法。（来源：https://docs.github.com/en/actions/reference/security/secure-use）

**知识点14：Dependency Review Action——PR依赖变更审计**
`actions/dependency-review-action`在PR时检查依赖变更：①阻止引入已知漏洞的依赖包（基于GitHub Advisory Database）②阻止许可证不兼容的依赖③检测版本降级攻击（从高版本降到被篡改的低版本）。配置在pull_request事件中运行，与CI并行。项目已在第86轮添加dependency-review-action。这是供应链安全的重要一环，防止恶意依赖通过PR进入代码库。（来源：https://docs.github.com/en/actions/reference/security/secure-use）

**知识点15：GitHub Advanced Security——CodeQL + Secret Scanning**
GitHub Advanced Security提供：①Code scanning（CodeQL）：自动分析代码中的安全漏洞（SQL注入、XSS、硬编码密钥等），支持多种语言，可配置在push/PR时运行②Secret scanning：自动扫描代码和历史中的API密钥、token、密码，支持100+服务商的密钥模式检测，发现后通知服务商吊销③Push protection：推送时实时阻止包含已知密钥的commit。公开仓库免费使用，私有仓库需Advanced Security许可。项目可启用CodeQL扫描Next.js/TypeScript代码。（来源：https://docs.github.com/en/actions/reference/security/secure-use）

**落地计划**：
1. 知识点3+9（permissions最小权限+commit SHA锁定）→ 任务P2-SEC-GHA-AUDIT：审计所有.github/workflows/*.yml的permissions配置和第三方action引用，确保最小权限和SHA锁定
2. 知识点10+13（Secrets管理+Shell注入防护）→ 任务P2-SEC-GHA-SECRETS：检查CI脚本中是否有echo secrets、是否将不受信任输入直接内联到run脚本，修复注入风险
3. 知识点12（Environment保护规则）→ 任务P2-SEC-GHA-ENV：创建production环境并配置required reviewers，限制生产部署需要人工批准
4. 知识点15（CodeQL + Secret Scanning）→ 任务P2-SEC-GHA-CODEQL：添加CodeQL扫描workflow（language: javascript-typescript），启用secret scanning和push protection
5. 知识点1+5（OIDC概述+AWS sub条件）→ 任务P2-SEC-GHA-OIDC-PLAN：评估将Vercel部署从API Token改为OIDC（Vercel支持OIDC），消除长期部署密钥


### [2026-09-26] Vitest前端单元测试与React Testing Library组件测试完整指南

**知识点1：Vitest——基于Vite的下一代测试框架**
Vitest（发音"veetest"）是基于Vite的测试框架，核心优势是与Vite共享配置（transformers、resolvers、plugins），无需为测试单独配置Babel/Webpack。开箱支持TypeScript、JSX、ESM。API与Jest高度兼容（test/describe/expect/beforeEach等），Jest项目迁移成本极低。GitHub 12k+ stars，由Vite团队维护。（来源：https://vitest.dev/guide/、https://vitest.dev/guide/features）

**知识点2：Vitest安装与jsdom环境配置**
React组件测试安装：`npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom`。vitest.config.ts中配置`test: { environment: 'jsdom', setupFiles: './setupTests.ts' }`。setupTests.ts中`import '@testing-library/jest-dom'`启用自定义匹配器。Next.js项目可用`create-next-app --example with-vitest`快速启动。（来源：https://vitest.fr/react/、https://preview.nextjs.org/docs/pages/guides/testing/vitest）

**知识点3：Vitest核心API与Jest兼容性**
Vitest核心API：`test(name, fn)`/`it(name, fn)`定义测试，`describe(name, fn)`分组，`expect(value)`断言，`beforeEach/afterEach/beforeAll/afterAll`钩子。与Jest API几乎1:1兼容，大多数Jest测试只需将`import from 'jest'`改为`import from 'vitest'`即可运行。Vitest还提供`vi.fn()`（替代jest.fn()）、`vi.mock()`、`vi.spyOn()`等mock API。（来源：https://vitest.dev/guide/）

**知识点4：Vitest Watch模式与性能优势**
`vitest`命令默认进入watch模式，修改源码后自动重跑相关测试，利用Vite的HMR机制实现毫秒级重跑。`vitest run`执行单次运行（CI用）。Vitest的冷启动和重跑速度比Jest快5-10倍，因为复用Vite的依赖预构建和transform缓存。支持`vitest --changed`只跑受git变更影响的测试。（来源：https://vitest.dev/guide/features）

**知识点5：React Testing Library核心理念——测试行为而非实现**
React Testing Library（RTL）的核心原则：测试用户可见的行为和交互，而非组件内部实现细节（如state、内部方法、props传递）。不鼓励使用`container.querySelector`或enzyme的`find('Component')`，而是通过用户可感知的方式（role、text、label）查询元素。这样测试在重构组件内部实现时不会失效，只在用户行为改变时才失败。（来源：https://testing-library.com/docs/react-testing-library/faq/、https://testing-library.com/docs/queries/about/）

**知识点6：Query优先级——从可访问性角度选择查询方式**
RTL的Query优先级（从高到低）：①`getByRole`（最优先，对应ARIA role，如button/heading/link）②`getByLabelText`（表单字段）③`getByPlaceholderText`（输入框占位符）④`getByText`（可见文本）⑤`getByDisplayValue`（表单当前值）⑥`getByAltText`（图片alt）⑦`getByTitle`（title属性）⑧`getByTestId`（最后手段，仅当其他方式都不可行时用）。优先使用可访问性查询天然提升a11y。（来源：https://testing-library.com/docs/queries/about/）

**知识点7：三种Query变体——getBy/queryBy/findBy**
三种变体区别：①`getBy*`：同步查询，找不到元素时抛错（测试失败），用于断言元素一定存在②`queryBy*`：同步查询，找不到返回null（不抛错），用于断言元素不存在（`expect(queryByText('x')).toBeNull()`）③`findBy*`：异步查询，返回Promise，默认每50ms重试一次、1000ms超时，用于等待异步渲染的元素出现。`findBy*` = `getBy*` + `waitFor`的组合。（来源：https://testing-library.com/docs/queries/about/）

**知识点8：user-event vs fireEvent——模拟真实用户交互**
`@testing-library/user-event`模拟真实用户交互（如点击前先聚焦、键盘输入时触发完整的keydown/keypress/keyup序列），比`fireEvent`更接近真实浏览器行为。user-event v14必须先调用`const user = userEvent.setup()`获取实例，且所有方法（click/type/selectOptions等）都是异步的必须`await`。`fireEvent`是底层事件分发，仅用于user-event不支持的特殊场景。（来源：https://testing-library.com/docs/react-testing-library/migrate-from-enzyme/、https://techoral.com/react/react-testing-library.html）

**知识点9：jest-dom自定义匹配器**
`@testing-library/jest-dom`提供DOM专用断言匹配器：`toBeInTheDocument()`（元素在DOM中）、`toHaveTextContent(text)`、`toHaveAttribute(name, value)`、`toBeVisible()`（可见而非display:none）、`toBeDisabled()`、`toHaveClass(class)`、`toBeChecked()`（checkbox/radio选中）、`toHaveFocus()`。需在setupFiles中导入，否则这些匹配器不可用。（来源：https://testing-library.com/docs/react-testing-library/setup/）

**知识点10：act()自动包裹——无需手动管理**
React Testing Library的`render`、`userEvent`、`waitFor`、`findBy*`都自动包裹在React的`act()`中，确保所有状态更新和效果完成后再进行断言，避免"not wrapped in act"警告。只有在测试中直接调用状态更新函数（如手动调用setState）时才需要手动`act()`。React官方文档推荐使用RTL而非直接使用act()，因为RTL的helper已正确处理。（来源：https://react.dev/reference/react/act、https://testing-library.com/docs/react-testing-library/setup/）

**知识点11：自定义render函数——包裹Provider**
当组件依赖Context Provider（如ThemeProvider、Redux Provider、Next.js Router）时，通过`render`的`wrapper`选项包裹。最佳实践是创建自定义render函数：`const customRender = (ui, options) => render(ui, { wrapper: AllProviders, ...options })`，其中AllProviders嵌套所有需要的Provider。然后导出`customRender`作为`render`，在测试中直接使用，避免每个测试重复配置wrapper。（来源：https://testing-library.com/docs/react-testing-library/setup/）

**知识点12：异步测试模式——findBy与waitFor**
异步渲染测试两种模式：①`findBy*`：等待元素出现，`const button = await screen.findByText('Submit')`，适合等待单个元素②`waitFor(callback)`：等待任意条件满足，`await waitFor(() => expect(mockFn).toHaveBeenCalled())`，适合等待副作用完成或多个条件。`findBy*`内部就是`waitFor(() => getBy*())`。避免使用`setTimeout`手动等待，应使用RTL的异步工具。（来源：https://testing-library.com/docs/queries/about/）

**知识点13：Vitest覆盖率与CI门禁**
`vitest run --coverage`生成覆盖率报告，支持`v8`（默认，更快）或`istanbul` provider。在vitest.config.ts中配置`test: { coverage: { provider: 'v8', thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 } } }`设置覆盖率门禁，低于阈值时CI失败。覆盖率报告输出到`coverage/`目录，支持HTML/JSON/文本格式。（来源：https://vitest.dev/guide/features）

**知识点14：Next.js + Vitest集成注意事项**
Next.js项目使用Vitest需注意：①配置`test.environment: 'jsdom'`模拟浏览器环境②setupFiles导入`@testing-library/jest-dom`③Mock Next.js特有的模块：`next/image`（用vi.mock替换为普通img）、`next/navigation`（mock useRouter/usePathname）、`next/headers`（mock cookies/headers）④Server Components不能直接在jsdom中测试，需测试其导出的纯函数或提取逻辑到独立模块⑤客户端组件（'use client'）可正常用RTL测试。（来源：https://preview.nextjs.org/docs/pages/guides/testing/vitest）

**知识点15：测试金字塔与最佳实践**
前端测试金字塔：①单元测试（最多）：纯函数、工具函数、自定义Hooks，快速且独立②组件测试：单个组件的交互行为（点击、输入、渲染）③集成测试：多个组件协作的页面流程④E2E测试（最少）：Playwright/Cypress模拟真实用户完整流程。最佳实践：每个测试独立（不共享状态，beforeEach重置）；测试名称描述行为而非实现（"点击按钮后计数增加"而非"调用handleClick"）；避免快照测试作为主要手段（易产生无意义的大diff）；优先测试用户可感知的行为。（来源：https://testing-library.com/docs/react-testing-library/faq/、https://vitest.dev/guide/）

**落地计划**：
1. 知识点2+14（安装配置+Next.js集成）→ 任务P2-QUALITY-VITEST-SETUP：在项目中初始化Vitest配置，安装依赖，配置jsdom环境和setupFiles，mock next/image/next/navigation
2. 知识点5+6+7（RTL理念+Query优先级+三种变体）→ 任务P2-QUALITY-COMPONENT-TESTS：为核心组件（SearchBox、BackToTop、RouteFocusManager）编写组件测试，使用getByRole/findBy等可访问性查询
3. 知识点8+9（user-event+jest-dom匹配器）→ 任务P2-QUALITY-INTERACTION-TESTS：为交互组件（搜索框输入、CTA按钮点击、筛选表单）编写用户交互测试，使用user-event模拟真实操作
4. 知识点13（覆盖率与CI门禁）→ 任务P2-QUALITY-COVERAGE-CI：在GitHub Actions中添加vitest --coverage步骤，设置覆盖率阈值门禁，防止测试覆盖率下降
5. 知识点15（测试金字塔）→ 任务P2-QUALITY-TEST-PYRAMID：制定测试策略，优先为工具函数和Hooks写单元测试，核心交互组件写组件测试，E2E用Playwright（已有）


### [2026-09-26] Next.js 15与React 19新特性深度解析及升级路径

**知识点1：Next.js 15两大破坏性变更——缓存语义与异步Request API**
Next.js 15有两个核心破坏性变更：①缓存语义：fetch请求、GET Route Handlers、客户端导航默认不再缓存（Next.js 14默认缓存），需显式设置`cache: 'force-cache'`或`revalidate`才能缓存；②异步Request API：`cookies()`、`headers()`、`params`/`searchParams`现在是异步的，必须用`await`。这两个变更是升级时最容易出错的地方。（来源：https://nextjs.org/blog/next-15、https://nextjs.org/docs/app/guides/upgrading/version-15）

**知识点2：React 19 Actions——表单处理的范式转变**
React 19引入Actions概念：将函数传递给`<form action={fn}>`属性默认使用Actions，提交后自动重置表单。Actions是异步函数，React自动管理pending状态、错误处理和乐观更新。与Server Components配合时，Server Actions（`"use server"`）让客户端组件直接调用服务端函数，无需手动创建API路由。（来源：https://react.dev/blog/2024/12/05/react-19、https://react.dev/reference/rsc/server-functions）

**知识点3：useActionState Hook——替代useFormState**
React 19中`useFormState`已被`useActionState`替代。签名：`const [state, dispatchAction, isPending] = useActionState(reducerAction, initialState, permalink?)`。reducerAction接收(previousState, formData)返回新状态。与Server Functions配合时，React会自动重放（replay）水合完成前用户输入的表单提交，实现渐进增强——用户在JS加载完成前就能交互。（来源：https://react.dev/reference/react/useActionState、https://nextjs.org/docs/app/guides/upgrading/version-15）

**知识点4：useOptimistic Hook——乐观更新的官方方案**
React 19新增`useOptimistic` Hook，用于在异步操作完成前立即更新UI（乐观更新）。签名：`const [optimisticState, setOptimistic] = useOptimistic(value, reducer?)`。调用setOptimistic后立即显示新状态，异步操作完成后根据结果确认或回滚。比手动管理loading+state更简洁，与Actions配合使用效果最佳。（来源：https://react.dev/reference/react/useOptimistic、https://react.dev/blog/2024/12/05/react-19）

**知识点5：use() Hook——渲染期间读取Promise与Context**
React 19新增`use()` Hook，可在渲染期间（包括条件语句和循环中）读取Promise和Context。读取Promise时类似Suspense的简化版——React会暂停渲染直到Promise resolve，然后重试。读取Context时替代`useContext`，可在条件中调用（不受Hooks规则限制）。这为数据获取提供了更灵活的模式。（来源：https://react.dev/blog/2024/12/05/react-19、https://react.dev/reference/react/use）

**知识点6：Partial Prerendering (PPR)——增量采用模式**
Next.js 15中PPR仍为experimental，但引入了`ppr: 'incremental'`模式，可在特定路由逐步采用而不影响全站。配置：next.config中设`experimental: { ppr: 'incremental' }`，然后在layout/page中导出`export const experimental_ppr = true`。PPR结合静态shell（即时响应）+动态内容（Suspense边界内流式渲染），是Next.js未来的默认渲染模式。子段可设`experimental_ppr: false`禁用。（来源：https://nextjs.org/docs/15/app/getting-started/partial-prerendering、https://nextjs.org/docs/15/app/api-reference/config/next-config-js/ppr）

**知识点7：Turbopack Dev稳定版——开发体验提升**
Next.js 15中Turbopack用于开发环境（`next dev --turbopack`）已稳定。Turbopack是Rust编写的打包工具，比Webpack快10倍以上的增量编译。Next.js 15对Turbopack做了大量性能和稳定性改进，包括更好的HMR（热模块替换）、更准确的错误覆盖层。生产构建仍使用Webpack（Turbopack生产构建仍在开发中）。（来源：https://nextjs.org/blog/next-15）

**知识点8：after API（Next.js 15.1稳定）——响应后执行代码**
Next.js 15.1中`after` API稳定，用于在响应流式传输完成后执行代码（如日志记录、分析追踪、后台任务），不阻塞响应发送。在Server Components/Route Handlers中调用`after(() => { ... })`，代码会在响应完成后异步执行。替代了之前需要手动管理的`waitUntil`模式，更简洁。适合不需要在响应中返回结果的副作用操作。（来源：https://nextjs.org/blog/next-15-1）

**知识点9：缓存语义变更对现有项目的影响**
Next.js 14→15缓存语义变更是最大的升级风险：①fetch默认从`force-cache`变为`no-store`，所有数据获取默认动态渲染，可能导致构建时间增加和性能下降；②GET Route Handlers默认不再缓存，需显式设置`export const dynamic = 'force-static'`或使用`revalidate`；③客户端导航默认不再缓存页面。升级后需审计所有fetch调用，对需要缓存的显式添加`cache: 'force-cache'`。（来源：https://nextjs.org/blog/next-15、https://nextjs.org/docs/app/guides/upgrading/version-15）

**知识点10：异步Request API变更——cookies/headers/params**
Next.js 15中`cookies()`和`headers()`从同步变为异步，必须用`await`：`const cookieStore = await cookies()`。`params`和`searchParams`在Page组件中也变为异步：`export default async function Page({ params, searchParams }) { const { slug } = await params; }`。这是因为Next.js 15使用了React 19的异步请求API，与React的新渲染模型对齐。升级时需全局搜索这些API调用并添加await。（来源：https://nextjs.org/blog/next-15、https://nextjs.org/docs/app/guides/upgrading/version-15）

**知识点11：React Compiler（实验性）——自动优化重新渲染**
Next.js 15支持React Compiler（实验性），这是一个Babel插件，自动优化React组件的重新渲染，减少手动使用`useMemo`/`useCallback`/`memo`的需求。Compiler会自动记忆计算值和回调，只在依赖变化时重新计算。配置：`experimental: { reactCompiler: true }`。目前仍为实验性，不建议在生产环境全面启用，但可在特定路由测试。（来源：https://nextjs.org/blog/next-15）

**知识点12：instrumentation.js稳定——服务器启动初始化**
Next.js 15中`instrumentation.ts`（或.js）文件稳定，用于在服务器启动时运行一次性初始化代码（如数据库连接池设置、监控SDK初始化、定时任务启动）。文件放在项目根目录，导出`register()`函数，在服务器启动时自动调用。支持`instrumentationHook`配置（已默认启用）。比在`next.config.js`中写初始化代码更清晰，且支持Edge和Node.js运行时。（来源：https://nextjs.org/blog/next-15）

**知识点13：next/form组件——预取表单目标路由**
Next.js 15引入`next/form`组件，替代原生`<form>`用于客户端导航。`next/form`会在表单提交前预取（prefetch）目标路由，提升导航性能。用法：`import Form from 'next/form'; <Form action="/search">...</Form>`。当用户点击提交按钮时，目标路由已预取完成，导航几乎即时。对搜索表单、筛选表单等高频交互场景特别有用。（来源：https://nextjs.org/blog/next-15）

**知识点14：升级路径与codemod工具**
Next.js 14→15升级步骤：①`npm install next@15 react@19 react-dom@19`；②运行`npx @next/codemod@latest upgrade`自动应用codemod（包括useFormState→useActionState、cookies/headers加await等）；③审计fetch缓存行为，对需要缓存的显式设置；④测试所有页面确保渲染正确；⑤逐步启用PPR（incremental模式）。注意：Next.js 15要求Node.js >= 18.18.0。Pages Router仍兼容React 18，可延后升级。（来源：https://nextjs.org/docs/app/guides/upgrading/version-15、https://nextjs.org/blog/next-15）

**知识点15：React 19其他重要改进**
React 19还有多项重要改进：①ref作为prop：函数组件可直接接收`ref`作为prop，无需`forwardRef`；②Context作为Provider：`<Context value={x}>`替代`<Context.Provider value={x}>`；③文档元数据改进：支持`<title>`、`<meta>`等标签直接在组件中渲染（自动提升到head）；④cleanup函数返回：useEffect的cleanup函数现在支持返回Promise（异步清理）；⑤更好的水合错误信息：React 19改进了水合不匹配的错误提示，更易定位问题。（来源：https://react.dev/blog/2024/12/05/react-19）

**落地计划**：
1. 知识点1+9+10（缓存语义+异步API变更）→ 任务P2-UPGRADE-NEXT15-AUDIT：升级前审计所有fetch调用和cookies()/headers()/params使用，标记需要修改的位置
2. 知识点3+4（useActionState+useOptimistic）→ 任务P2-UX-FORM-INTERACTION：搜索框和筛选表单改用Actions+useActionState，添加乐观更新和pending状态
3. 知识点6（PPR增量采用）→ 任务P1-PERF-PPR-TRIAL：在工具列表页和首页试点PPR（incremental模式），验证静态shell+动态内容的性能提升
4. 知识点8（after API）→ 任务P2-PERF-AFTER-ANALYTICS：GA4事件追踪改用after API，在响应完成后异步执行，不阻塞页面渲染
5. 知识点14（升级路径）→ 任务P2-UPGRADE-NEXT15-PLAN：制定Next.js 14→15升级计划，先在开发分支测试，确认无破坏后再合并


### [2026-09-26] Next.js Middleware与Edge Runtime深度指南

**知识点1：Middleware默认运行在Edge Runtime**
Next.js 14的Middleware仅支持Edge Runtime，不支持Node.js Runtime。Next.js 15.2+（canary）开始实验性支持Node.js Runtime，需在next.config中启用flag。Edge Runtime基于V8引擎，提供Web API子集，延迟极低但API受限。（来源：https://nextjs.org/docs/14/app/building-your-application/routing/middleware）

**知识点2：Middleware核心适用场景**
官方明确的有效场景包括：①读取请求后快速重定向（如基于cookie的认证守卫）②基于A/B测试或实验重写到不同页面（URL不变，内部渲染不同页面）③为所有或部分页面修改响应头（如安全头、缓存控制）④基于地理位置的重定向（如i18n路由、区域限制）。（来源：https://nextjs.org/docs/app/building-your-application/routing/middleware）

**知识点3：Middleware不适用场景**
官方明确不适合：①慢速数据获取（Middleware应轻量快速，不应等待外部API）②会话管理（应使用cookie而非在Middleware中管理会话状态）③简单的静态重定向（应使用next.config.js的redirects配置，无需Middleware开销）。（来源：https://nextjs.org/docs/app/building-your-application/routing/middleware）

**知识点4：Edge Runtime严格限制**
Edge Runtime不支持大多数Node.js API：不能读写文件系统（fs）、不能使用path模块、不能使用require()（必须用ES Modules import）、不支持ISR（增量静态再生）。部分npm包可能因依赖Node.js API而无法在Edge Runtime中工作。（来源：https://nextjs.org/docs/15/app/api-reference/edge、https://vercel.com/kb/guide/library-sdk-compatible-with-vercel-edge-runtime-and-functions）

**知识点5：Edge Function资源限制**
Vercel Edge Function限制：最大内存128MB（不可调整），最大初始响应时间25秒（开始发送响应后可继续流式传输最多300秒），压缩后最大体积Hobby计划1MB、Pro计划2MB、Enterprise计划4MB（包含代码和所有依赖）。超出内存限制会返回502错误。（来源：https://vercel.com/docs/functions/runtimes/edge、https://vercel.com/docs/concepts/limits/overview）

**知识点6：Middleware matcher配置**
使用`export const config = { matcher: [...] }`限制Middleware运行的路径，避免对所有请求执行Middleware。matcher支持正则表达式，如`matcher: ['/dashboard/:path*', '/api/:path*']`。也可以用negative lookahead排除静态资源：`matcher: ['/((?!_next/static|_next/image|favicon.ico).*)']`。（来源：https://nextjs.org/docs/app/building-your-application/routing/middleware）

**知识点7：NextResponse API**
Middleware返回NextResponse对象，核心方法：①`NextResponse.redirect(url)` - 发送重定向（默认302，可传301永久重定向）②`NextResponse.rewrite(url)` - 内部重写（URL不变，渲染不同页面）③`NextResponse.next()` - 继续正常响应，可通过request/headers修改请求头④`NextResponse.json(data)` - 返回JSON响应。可通过`response.headers.set()`修改响应头。（来源：https://nextjs.org/docs/app/building-your-application/routing/middleware）

**知识点8：Vercel地理位置数据**
在Vercel上部署时，Middleware可通过`request.geo`获取访问者地理位置：country（国家代码）、city（城市）、region（地区）、latitude（纬度）、longitude（经度）。Vercel还会自动注入geo头：`x-vercel-ip-country`、`x-vercel-ip-country-region`、`x-vercel-ip-city`，可在页面中读取。（来源：https://vercel.com/docs/routing-middleware/getting-started、https://vercel.com/docs/functions/edge-middleware/middleware-api）

**知识点9：A/B测试与Feature Flags模式**
Middleware可在边缘实现无闪烁A/B测试：检查用户cookie中的实验组标识，若无则随机分配并设置cookie，然后`NextResponse.rewrite()`到对应变体页面。用户URL不变，无客户端闪烁，不增加JS bundle体积。适合定价页、首页布局、CTA文案等实验。（来源：https://www.adeptdev.io/blogs/nextjs-middleware-complete-guide-for-2026、https://nextjslaunchpad.com/ja/article/nextjs-middleware-kanzen-guide-2026）

**知识点10：认证守卫模式**
Middleware可在页面渲染前检查认证状态：读取cookie中的JWT token，使用`jose`库（Edge Runtime兼容）验证token，未认证则`NextResponse.redirect()`到登录页，已认证则`NextResponse.next()`继续。比在每个页面中做认证检查更集中、更安全（在边缘拦截，未认证请求不会到达页面代码）。（来源：https://techoral.com/react/nextjs-middleware.html、https://nurbak.com/en/blog/nextjs-middleware-guide/）

**知识点11：Middleware vs next.config redirects选择**
选择原则：①静态规则（如`/old`→`/new`永久重定向）用next.config.js的redirects，零运行时开销②需要基于cookie、header、geo等请求数据的条件逻辑用Middleware③重定向列表来自CMS或数据库（动态变化）用Middleware④需要添加/移除trailing slash的自定义逻辑用Middleware（可在next.config中设置`skipTrailingSlashRedirect: true`后在Middleware中自定义处理）。（来源：https://reactdevelopers.org/docs/nextjs-routing/middleware/、https://strivelab.pl/blog/middleware-w-next-js-7-zastosowan-i-typowych-pulapek/）

**知识点12：Next.js 16将Middleware重命名为Proxy**
Next.js 16中Middleware文件从`middleware.ts`重命名为`proxy.ts`，默认运行时从Edge改为Node.js（可在config中设置`runtime: 'edge'`切回Edge）。Proxy导出从`export default function middleware`改为`export function proxy`。这一变化使Proxy可以使用完整Node.js API，适合更复杂的逻辑。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/proxy、https://nextjs.org/docs/app/getting-started/proxy）

**知识点13：Edge Runtime支持的API**
Edge Runtime支持的Web API包括：fetch（含HTTP缓存）、Web Crypto API（crypto.subtle用于JWT验证）、TextEncoder/TextDecoder、URL、URLSearchParams、Headers、Request、Response、AbortController、console、setTimeout/setInterval、atob/btoa、structuredClone。不支持：fs、path、os、net、tls、dns、child_process、worker_threads等Node.js核心模块。（来源：https://nextjs.org/docs/15/app/api-reference/edge、https://vercel.com/docs/functions/runtimes/edge）

**知识点14：Middleware性能最佳实践**
①保持Middleware轻量：避免复杂计算和大数据处理，Middleware在每个匹配请求上运行②使用matcher限制范围：不要对所有请求运行Middleware，排除静态资源③避免导入大型库：Edge Function体积限制严格（1-4MB压缩后），导入大库可能超限④优先使用next.config做静态重定向：零运行时开销⑤使用`waitUntil`处理非关键后台任务（如日志、分析），不阻塞响应⑥避免在Middleware中进行慢速外部API调用，会增加所有请求延迟。（来源：https://vercel.com/docs/functions/runtimes/edge、https://nextjs.org/docs/app/building-your-application/routing/middleware）

**知识点15：Edge Runtime超时处理**
Edge Function必须在25秒内开始发送响应，否则触发`EDGE_FUNCTION_INVOCATION_TIMEOUT`错误。如果后端API响应慢，应使用流式响应（streaming）避免空闲超时。对于需要更长执行时间的工作负载，应考虑迁移到Vercel Fluid Compute（提供更长持续时间和优化性能）或Vercel Workflows（允许代码暂停、恢复和保持状态数分钟到数月）。（来源：https://vercel.com/docs/errors/EDGE_FUNCTION_INVOCATION_TIMEOUT、https://vercel.com/docs/functions/limitations）

**落地计划**：
1. 知识点2+7（快速重定向+NextResponse）→ 任务P2-SEO-LEGACY-URL-REDIRECTS：用Middleware集中处理旧URL重定向（从CMS/数据库动态读取重定向列表），避免在next.config中硬编码数百条重定向
2. 知识点8（Vercel地理位置数据）→ 任务P2-GROWTH-GEO-TARGETED-CONTENT：在Middleware中读取request.geo，为不同国家用户设置x-user-country响应头，页面根据header展示区域化内容（如中国用户展示中文界面）
3. 知识点9（A/B测试模式）→ 任务P2-GROWTH-AB-TESTING-CTA：用Middleware实现CTA按钮A/B测试，50%用户看到变体A，50%看到变体B，通过cookie固定实验组，无客户端闪烁
4. 知识点10（认证守卫模式）→ 任务P2-SEC-ADMIN-AUTH-GUARD：如果未来添加管理员后台，用Middleware做认证守卫，在边缘拦截未认证请求
5. 知识点14（性能最佳实践）→ 任务P1-PERF-MIDDLEWARE-AUDIT：添加Middleware时必须遵循性能最佳实践，使用matcher排除静态资源，保持轻量


## [2026-09-26] Next.js App Router缓存与数据获取策略（四层缓存 + fetch缓存 + ISR + generateStaticParams + cache tags + Route Segment Config）

### 四层缓存架构
- 知识点1：**Next.js App Router有四层缓存，各有不同生命周期和失效规则**。①Request Memoization（请求内去重，单次请求生命周期，用React cache()）；②Data Cache（跨请求/部署持久化，用fetch()或unstable_cache）；③Full Route Cache（构建时预渲染页面，持久化到ISR缓存）；④Router Cache（客户端RSC缓存，浏览器会话级）。理解这四层是排查缓存问题的基础。（来源：https://nextjs.org/docs/app/guides/caching + https://nextjs.org/docs/app/getting-started/caching）
- 知识点2：**fetch()在App Router中默认缓存（cache: 'force-cache'）**。这与Pages Router不同（Pages Router中fetch不缓存）。要选择退出缓存：`fetch(url, { cache: 'no-store' })`或`{ next: { revalidate: 0 } }`。AIToolCrux读取本地JSON文件的函数不走fetch，需要用unstable_cache包装。（来源：https://nextjs.org/docs/app/api-reference/functions/fetch + https://nextjs.org/docs/app/guides/caching）

### fetch缓存与revalidate
- 知识点3：**next.revalidate设置数据缓存生命周期（秒）**。`fetch(url, { next: { revalidate: 3600 } })`缓存1小时。`revalidate: false`=永久缓存（等同于Infinity）。`revalidate: 0`=不缓存。这是ISR在数据层面的实现。（来源：https://nextjs.org/docs/app/api-reference/functions/fetch + https://nextjs.org/docs/app/guides/caching）
- 知识点4：**unstable_cache用于非fetch数据源的缓存**。对于数据库查询、SDK调用、本地文件读取等不使用fetch()的数据源，用`unstable_cache(fn, keyParts, { revalidate: 3600, tags: ['data'] })`包装。AIToolCrux的getPost()/getTool()等读取JSON文件的函数应使用此方法缓存。（来源：https://nextjs.org/docs/app/guides/caching + https://nextjs.org/docs/app/getting-started/caching-and-revalidating）
- 知识点5：**React cache()实现请求内去重**。`import { cache } from 'react'; const getPost = cache(async (slug) => ...)`确保同一请求中多个组件调用getPost('same-slug')只执行一次。这是Request Memoization层，仅在单次请求内有效，不跨请求持久化。（来源：https://nextjs.org/docs/app/guides/caching + https://react.dev/reference/react/cache）

### generateStaticParams与动态路由
- 知识点6：**generateStaticParams在构建时预渲染动态路由**。返回参数数组（如`[{ slug: 'post-1' }, { slug: 'post-2' }]`），Next.js在构建时为每个参数生成静态HTML。没有generateStaticParams的动态路由默认按需动态渲染（返回cache-control: no-store）。**这就是第96轮分类页no-store问题的根因——缺少generateStaticParams导致动态渲染**。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-static-params + https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes）
- 知识点7：**dynamicParams控制未预渲染参数的行为**。`true`（默认）= generateStaticParams未包含的参数在首次访问时按需生成（ISR风格，先渲染再缓存）。`false`= 未包含的参数返回404。对于内容有限的站点（如AIToolCrux的106篇文章），可设为false确保只有已知slug可访问，避免恶意参数触发渲染。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config + https://next.nodejs.cn/docs/app/api-reference/file-conventions/route-segment-config）

### Route Segment Config
- 知识点8：**Route Segment Config通过export变量控制页面级渲染行为**。关键选项：`dynamic`（'auto'|'force-dynamic'|'error'|'force-static'）、`revalidate`（false|0|number，页面级默认revalidate时间）、`fetchCache`（控制该路由内所有fetch的缓存行为）、`dynamicParams`、`runtime`（'nodejs'|'edge'）、`preferredRegion`。这些export放在page.tsx/layout.tsx/route.ts顶部。（来源：https://nextjs.org/docs/15/app/api-reference/file-conventions/route-segment-config + https://nextjs.org/docs/app/building-your-application/routing/route-handlers）
- 知识点9：**dynamic = 'force-static'强制静态渲染，可用于捕获意外的动态依赖**。如果页面使用了cookies()/headers()/searchParams等动态API，force-static会在构建时报错，帮助发现意外的动态渲染。`force-dynamic`则强制整个路由动态渲染（无缓存），适合需要实时数据的页面。`auto`（默认）让Next.js根据数据获取自动决定。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config + https://nextjs.org/docs/app/guides/caching）

### Cache Tags与按需重验证
- 知识点10：**Cache Tags通过next.tags标记缓存数据，支持批量失效**。`fetch(url, { next: { tags: ['posts', 'tools'] } })`给缓存数据打标签。`revalidateTag('posts')`使所有带该标签的缓存失效，下次请求触发重新渲染。在Next.js 16+中revalidateTag需要第二个参数（cacheLife profile如'max'），单参数形式已弃用。（来源：https://nextjs.org/docs/app/api-reference/functions/revalidateTag + https://nextjs.org/docs/app/guides/incremental-static-regeneration）
- 知识点11：**revalidatePath按路径失效，revalidateTag按标签失效**。`revalidatePath('/blog/post-1')`失效特定路径的Full Route Cache。`revalidateTag('posts')`失效所有带该标签的Data Cache条目。两者都是stale-while-revalidate：失效后下次请求立即返回旧缓存，后台重新生成。在Server Action或Route Handler中调用。（来源：https://nextjs.org/docs/app/guides/how-revalidation-works + https://nextjs.org/docs/app/getting-started/revalidating）

### ISR与Vercel缓存
- 知识点12：**ISR（增量静态再生）= 静态速度 + 动态灵活性，stale-while-revalidate模式**。访问者立即获得缓存响应，Vercel在后台根据时间间隔或API调用重新生成页面。ISR缓存持久化最多31天。优势：无需重建全站即可更新内容、减少服务器负载、自动添加正确的cache-control头、大量内容页不会拖慢构建时间。（来源：https://vercel.com/docs/incremental-static-regeneration + https://nextjs.org/docs/app/guides/incremental-static-regeneration）
- 知识点13：**Vercel缓存层级：CDN Edge Cache → ISR Cache → Data Cache → Function执行**。CDN未命中时检查ISR缓存（持久化存储在函数区域），ISR命中则不调用函数。请求折叠（Request collapsing）将并发的同路径ISR请求合并为单次函数调用。静态资源自动在CDN缓存。（来源：https://vercel.com/docs/caching + https://vercel.com/docs/how-vercel-cdn-works + https://vercel.com/docs/data-cache）
- 知识点14：**x-vercel-cache响应头是调试缓存的关键工具**。可能值：HIT（CDN缓存命中）、MISS（未命中，动态响应或首次访问）、STALE（返回过期缓存同时后台重新验证）、PRERENDER（构建时预渲染的静态页面）、BYPASS（动态渲染绕过缓存）。对于ISR和PPR页面，冷MISS通常意味着路径未提前预渲染。（来源：https://vercel.com/docs/caching/cache-status + https://examples.vercel.com/docs/caching/cdn-cache）

### 调试与最佳实践
- 知识点15：**调试缓存的三步法**：①检查`next build`输出——○=静态（Static）、λ=动态（Dynamic）、◐=Partial Prerendering；②检查x-vercel-cache响应头确认CDN/ISR缓存状态；③检查是否有动态API（cookies()/headers()/searchParams/useSearchParams）或`cache: 'no-store'`意外强制动态渲染。对内容型站点，目标是尽可能多的○（静态）和PRERENDER/HIT（缓存命中）。（来源：https://nextjs.org/docs/app/guides/caching + https://vercel.com/docs/caching/cache-status + https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config）

### 落地计划
- 知识点6（generateStaticParams）→ 下次迭代：审计所有动态路由（blog/[slug]、tools/[slug]、blog/category/[slug]、subcategory/[slug]、authors/[slug]、og/[slug]）确认都有generateStaticParams，第96轮已修复category页，需检查其他路由
- 知识点4（unstable_cache）→ 下次迭代：为getPost()/getTool()/getAllPosts()等读取JSON文件的函数添加unstable_cache包装，减少每次请求的文件读取开销
- 知识点5（React cache()）→ 下次迭代：用cache()包装数据获取函数，确保同一请求内多组件调用不重复读取
- 知识点9（force-static调试）→ 下次迭代：在所有内容页临时设置`export const dynamic = 'force-static'`运行构建，捕获意外的动态依赖（如cookies()/headers()）
- 知识点14（x-vercel-cache调试）→ 下次迭代：用curl/Invoke-WebRequest检查关键页面的x-vercel-cache头，确认应为HIT/PRERENDER而非MISS/BYPASS
- 知识点7（dynamicParams: false）→ 下次迭代：对blog/[slug]和tools/[slug]设置dynamicParams: false，确保只有已知slug可访问，避免恶意参数触发渲染



## [2026-09-26] 高星GitHub工具：代码质量工具链（ESLint v9扁平配置 + Prettier + Husky v9 + lint-staged + commitlint）

### ESLint v9 扁平配置（Flat Config）
- 知识点1：**ESLint v9将flat config设为默认格式**。配置文件名为eslint.config.js/mjs/cjs/ts，放在项目根目录，导出一个配置对象数组。旧的.eslintrc格式已弃用，v9默认不再读取.eslintrc。（来源：https://eslint.org/docs/latest/use/configure/configuration-files + https://eslint.org/docs/latest/use/migrate-to-9.0.0）
- 知识点2：**Flat config核心变化**：不再支持子目录嵌套.eslintrc，所有配置在一个文件中；plugins用对象而非字符串（直接import插件对象放入plugins键）；用languageOptions替代parserOptions/env/globals；用files属性指定应用范围，不指定则默认匹配**/*.{js,mjs,cjs}。（来源：https://eslint.org/docs/latest/use/configure/migration-guide + https://eslint.org/blog/2022/08/new-config-system-part-2/）
- 知识点3：**defineConfig辅助函数提供类型提示**。ESLint v9提供`import { defineConfig } from "eslint/config"`，包裹配置数组获得TypeScript类型提示和自动补全。配置数组中后面对象覆盖前面的规则（级联覆盖）。（来源：https://eslint.org/docs/latest/use/configure/migration-guide）

### TypeScript ESLint v8
- 知识点4：**typescript-eslint v8配合flat config使用tseslint.config()**。提供辅助函数合并配置，支持extends数组。推荐配置层级：recommended（代码正确性，无类型检查）→ recommended-type-checked（需类型信息）→ strict（更严格正确性）→ stylistic（代码风格）→ strictTypeChecked/stylisticTypeChecked。（来源：https://typescript-eslint.io/getting-started/ + https://typescript-eslint.io/users/configs/）
- 知识点5：**类型检查型linting需要配置project且影响性能**。使用recommendedTypeChecked/strictTypeChecked需在languageOptions.parserOptions.project指向tsconfig.json。类型检查会显著增加lint时间，建议：本地pre-commit只用recommended（无类型检查）保持速度，CI中运行完整类型检查版。（来源：https://typescript-eslint.io/troubleshooting/typed-linting/performance/ + https://typescript-eslint.io/linting/typed-linting/）

### Prettier
- 知识点6：**Prettier只做格式化，不做linting**。Prettier关注代码格式（缩进、引号、分号、行宽、换行），不检查代码质量问题。与ESLint明确分工：ESLint查代码质量（未使用变量、潜在bug），Prettier统一格式。使用eslint-config-prettier关闭ESLint中与Prettier冲突的格式规则，避免双重检查。（来源：https://prettier.io/docs/install + https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Environment_setup/Code_editors）
- 知识点7：**Prettier关键配置选项**。printWidth（默认80，建议100适配宽屏）、tabWidth（默认2）、semi（默认true）、singleQuote（默认false，JS项目常用true）、trailingComma（v3默认"all"）、arrowParens（默认"always"）、bracketSameLine（false时JSX的>单独一行）。配置文件支持.prettierrc（JSON/YAML）、prettier.config.js/mjs/cjs、.prettierrc.toml。（来源：https://prettier.io/docs/next/configuration/ + https://prettier.io/docs/next/options/）
- 知识点8：**Prettier CLI高效选项**。`prettier --write --ignore-unknown`格式化所有可解析文件并跳过二进制/图片；`--cache`使用缓存只格式化变更文件（缓存键含Prettier版本、选项、Node版本、文件内容），大幅提升大项目速度；`--check`只检查不修改，适合CI。（来源：https://prettier.io/docs/cli）

### Husky v9
- 知识点9：**Husky v9大幅简化Git hooks管理**。`npx husky init`一键初始化，创建.husky/目录和package.json的prepare脚本。v9 hook文件不需要shebang行（v8需要），是纯shell脚本。支持全部13个客户端Git hooks，兼容macOS/Linux/Windows和Git GUI/Node版本管理器/Monorepo。（来源：https://github.com/typicode/husky + https://husky.nodejs.cn/how-to.html）
- 知识点10：**prepare脚本确保团队自动安装hooks**。package.json中`"prepare": "husky"`在每次npm install后自动运行，确保团队每个成员clone项目后都获得相同的git hooks配置。这是Husky v9的标准安装方式。（来源：https://husky.nodejs.cn/how-to.html）
- 知识点11：**CI中跳过Husky hooks**。CI环境通常不需要运行本地git hooks（CI会运行完整检查）。通过设置环境变量`HUSKY=0`跳过，或git commit时用`--no-verify`。但lint和format检查应在CI中独立运行，不依赖hooks。（来源：https://sevic.dev/tags/husky/ + Husky官方文档）

### lint-staged
- 知识点12：**lint-staged只对git暂存文件运行linters**。在pre-commit hook中运行，只对`git add`的文件执行指定命令，避免每次提交都lint整个项目。配置在package.json的"lint-staged"字段或.lintstagedrc文件中，按glob模式匹配文件类型。（来源：https://lint-staged.nodejs.cn/docs/ + https://reactdevelopers.org/docs/linting-formatting/husky-lint-staged/）
- 知识点13：**lint-staged典型配置**。`"*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"]`先自动修复ESLint问题再格式化；`"*.{json,md,yml,yaml,css}": ["prettier --write"]`只格式化。命令按数组顺序执行，修复后的文件自动重新暂存。（来源：https://lint-staged.nodejs.cn/docs/）

### commitlint + Conventional Commits
- 知识点14：**commitlint强制Conventional Commits规范**。在commit-msg hook中运行（不支持pre-commit），检查commit message格式。使用@commitlint/config-conventional预设，格式为`type(scope): subject`，type包括feat/fix/docs/style/refactor/perf/test/chore/ci/build等。breaking changes用`!`或footer的`BREAKING CHANGE:`标记。配置文件commitlint.config.js用`export default { extends: ['@commitlint/config-conventional'] }`。（来源：https://commitlint.js.org/guides/getting-started + https://www.conventionalcommits.org/ + https://commitlint.js.org/guides/local-setup）
- 知识点15：**完整工具链集成架构**。pre-commit hook → lint-staged（eslint --fix + prettier --write，仅暂存文件，快速）；commit-msg hook → commitlint（检查commit格式）；pre-push hook → 可选运行完整tsc --noEmit + 测试。CI中运行：完整eslint（无--fix，确保0错误）+ tsc --noEmit + prettier --check + 测试 + commitlint --from <base> --to <head>。本地快速反馈+CI严格门禁的双层防护。（来源：https://reactdevelopers.org/docs/linting-formatting/husky-lint-staged/ + https://commitlint.js.org/guides/ci-setup + https://sevic.dev/tags/husky/）

### 落地计划
- 知识点1-5（ESLint flat config + TypeScript ESLint）→ 下次迭代：为AIToolCrux创建eslint.config.mjs（flat config），使用typescript-eslint v8的recommended配置，添加到CI workflow
- 知识点6-8（Prettier）→ 下次迭代：创建.prettierrc和.prettierignore，添加prettier --check到CI，与现有ESLint规则去冲突
- 知识点9-11（Husky）→ 下次迭代：注意AIToolCrux用GitHub API提交不用git push，本地hooks不会触发，但prepare脚本和hooks配置仍对其他贡献者有用
- 知识点12-13（lint-staged）→ 下次迭代：配置lint-staged在pre-commit运行eslint --fix + prettier --write
- 知识点14（commitlint）→ 下次迭代：添加commitlint配置，统一commit message格式（当前commits如"fix: ..."已部分符合conventional commits）
- 知识点15（完整架构）→ 下次迭代：在现有CI workflows中添加eslint和prettier检查步骤，形成本地+CI双层防护



## [2026-09-26] SEO技术新趋势：Google生成式AI搜索优化（AI Overviews/AI Mode）+ FAQ弃用 + Preferred Sources

### 核心原则（Google官方2026年5月15日发布，7月10日更新）
- 知识点1：Google官方明确"为生成式AI搜索做优化就是为搜索体验做优化，因此仍然是SEO"。AI Overviews和AI Mode基于核心搜索排名和质量系统，不存在独立的"AI索引"。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide）
- 知识点2：Google AI使用RAG（检索增强生成/grounding）从核心搜索排名系统检索相关、最新的网页内容，然后生成回答并显示可点击的来源链接；同时使用query fan-out生成并发相关查询获取更多信息。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide）
- 知识点3：页面必须先被索引且有资格显示标准搜索摘要，才能出现在AI功能中。被robots.txt屏蔽、noindex或技术损坏的页面无法出现在AI Overviews中。（来源：https://criticnest.com/how-to-rank-in-ai-overviews/ + https://developers.google.com/search/docs/fundamentals/ai-optimization-guide）

### Mythbusting：Google明确说不需要做的事
- 知识点4：**llms.txt对Google Search无用**。Google官方明确说不需要创建llms.txt等AI文本文件，Google Search不使用它们。创建它们不会帮助也不会损害Google搜索排名（但可能对ChatGPT/Claude/Perplexity等其他AI引擎有用）。AIToolCrux已有llms.txt和llms-full.txt，保留即可但不要期望Google收益。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide#mythbusting + https://www.getpassionfruit.com/blog/should-i-create-an-llms.txt-file-google-s-2026-guidance-explained）
- 知识点5：不需要"chunking"内容。Google系统能理解页面上多个主题的细微差别并显示相关部分，没有理想页面长度，应为受众而非AI创建页面。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide#mythbusting）
- 知识点6：不需要为AI重写内容。AI系统能理解同义词和一般含义，不需要担心长尾关键词覆盖或每个搜索变体。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide#mythbusting）
- 知识点7：不需要寻求不真实的"提及"。Google核心排名系统专注于高质量内容，其他系统阻止垃圾信息；生成式AI功能依赖两者。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide#mythbusting）
- 知识点8：结构化数据对AI非必需。没有特殊的schema.org标记需要添加来获得AI可见性。但继续使用结构化数据作为整体SEO策略的一部分仍是好主意（有助于富结果资格）。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide#mythbusting）

### 真正重要的优化方向
- 知识点9：**非商品内容（Non-commodity content）是AI可见性的最大影响因素**。创建独特、专家主导、超越常识的内容。第一手评测（如AIToolCrux的6维度评测）比内容摘要更有价值。商品内容（如"7个提示"）基于常识，增加很少独特见解。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide + https://blog.google/products-and-platforms/products/search/new-controls-website-owners/）
- 知识点10：高质量图片和视频增加AI可见性机会。生成式AI搜索功能可以引入相关图片和视频，网站有更多机会出现在网页链接之外。AIToolCrux应继续为工具评测添加高质量截图。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide）
- 知识点11：避免scaled content abuse。为每个可能的搜索变体创建单独内容以操纵排名违反Google的scaled content abuse垃圾信息政策。高页面数量不等于高质量。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide）

### 2026年重大变化
- 知识点12：**FAQ富摘要已弃用**。自2026年5月7日起，FAQ富结果不再出现在Google搜索中。Rich Result Test支持已在2026年6月移除，Search Console API支持在2026年8月移除。FAQPage结构化数据不再产生富摘要，但可见的FAQ部分仍对用户有帮助。AIToolCrux的FAQSchema组件可以保留（不影响）但不再有SEO收益。（来源：https://developers.google.com/search/docs/appearance/structured-data/faqpage + https://developers.google.com/search/updates#removing-practice-problems）
- 知识点13：**Preferred Sources功能扩展到AI Overviews和AI Mode**。用户可以将网站添加为首选来源，在AI回答中优先显示并标记。只有域名和子域名级别有资格（子目录如/blog没有资格）。关键标准是新鲜、定期发布的内容。AIToolCrux是域名级网站，有资格。（来源：https://developers.google.com/search/docs/appearance/preferred-sources + https://blog.google/products-and-platforms/products/search/original-high-quality-content-search/）
- 知识点14：**Search Console新增生成式AI效果报告**。网站所有者可以查看内容在AI Overviews和AI Mode中的表现（曝光、点击等）。这是衡量AI搜索可见性的官方工具。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide）
- 知识点15：**AI代理体验（Agentic Experiences）兴起**。AI代理可以代表用户执行任务（如预订、比较产品规格），浏览器代理可能访问网站收集数据（分析视觉渲染、检查DOM结构、解释可访问性树）。Universal Commerce Protocol（UCP）等新协议正在出现。网站应关注可访问性和语义HTML以适配代理。（来源：https://developers.google.com/search/docs/fundamentals/ai-optimization-guide）
- 知识点16：Google垃圾信息政策适用于AI回答。生成式AI回答中的内容也受Google垃圾信息政策约束。（来源：https://developers.google.com/search/updates#revisited-javascript-documentation）

### 落地计划
- 知识点4（llms.txt无用）→ 下次迭代：确认现有llms.txt保留但不投入更多资源，将P1-SEO-LLMSTXT-001降级或关闭
- 知识点9（非商品内容）→ 下次迭代：在文章生成模板中强化"第一手经验"和"独特观点"要求，避免商品式内容
- 知识点12（FAQ弃用）→ 下次迭代：评估是否移除FAQSchema组件（P1-SEO-SCHEMA-FAQ-001可关闭），保留可见FAQ部分用于用户体验
- 知识点13（Preferred Sources）→ 下次迭代：确保网站持续发布新鲜内容以符合Preferred Sources资格，在GSC中监控AI效果报告
- 知识点10（图片视频）→ 下次迭代：继续为缺少截图的工具评测添加高质量截图（与用户偏好一致）
- 知识点15（AI代理）→ 下次迭代：确保语义HTML和可访问性（刚完成的a11y工作直接适配AI代理）



### [2026-09-25] 前端可访问性（a11y）最佳实践：WCAG 2.2 + ARIA + 键盘导航 + 焦点管理（15知识点）

**知识点1：WCAG 2.2是当前W3C推荐标准，2023年10月发布，比2.1新增9条成功标准**
WCAG 2.2在2.1基础上新增9条成功标准，包括焦点不被遮挡（2.4.11/2.4.12）、可拖动移动（2.5.7）、目标尺寸最小值（2.5.8，最小24x24 CSS像素）、冗余输入（3.3.7）、可访问认证（3.3.8）等。AIToolCrux应至少满足AA级别。
（来源：https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ ，https://www.w3.org/TR/WCAG22/）

**知识点2：WCAG四层原则：POUR——可感知、可操作、可理解、健壮**
Perceivable（可感知）：文本替代、时间媒体、适应性、可区分；Operable（可操作）：键盘可访问、足够时间、癫痫、可导航；Understandable（可理解）：可读、可预测、输入辅助；Robust（健壮）：兼容辅助技术。所有成功标准归入这四类。
（来源：https://www.w3.org/WAI/standards-guidelines/wcag/ ，https://www.w3.org/TR/WCAG22/）

**知识点3：ARIA第一原则：能用原生HTML就不用ARIA**
如果原生HTML元素已有语义和行为（如button、nav、h1-h6），不要用div+role+ARIA重新实现。ARIA只补充HTML无法表达的交互模式（如tabs、menu、dialog）。用role="heading" aria-level="2"不如直接用h2。
（来源：https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA ，https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/heading_role）

**知识点4：ARIA只修改可访问性树，不改变元素行为或外观**
给div加role="button"不会让它可点击、可聚焦或有键盘事件。必须同时添加tabindex、onKeyDown（Enter/Space触发）、onClick。ARIA属性（aria-expanded、aria-selected等）只通知辅助技术状态，不提供功能。
（来源：https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA ，https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Accessible_web_applications_and_widgets）

**知识点5：所有交互元素必须可通过键盘操作**
Tab/Shift+Tab导航，Enter/Space激活按钮，Enter跟随链接，方向键操作复合组件（tabs/menus/radio group），Escape关闭模态框/下拉菜单。自定义组件（如工具卡片、CTA按钮）如果用div实现必须添加键盘事件处理。
（来源：https://www.iamuvin.com/blog/design-web-accessibility-nextjs-wcag-guide ，https://accessibility.build/guides/react-accessibility）

**知识点6：焦点指示器必须可见，禁止outline:none而不提供替代**
:focus { outline: none; }是最常见的可访问性破坏。可用:focus-visible伪类实现"鼠标用户不显示、键盘用户显示"的智能焦点环。Next.js/Tailwind项目应确保所有交互元素有可见焦点样式。
（来源：https://tomodahinata.com/blog/react-nextjs-web-accessibility-wcag22-guide ，https://codefrog.app/quality-engineering/accessibility/keyboard-navigation）

**知识点7：Next.js App Router客户端路由后焦点不会自动移动**
App Router有内置route announcer朗读新页面title，但键盘焦点仍停留在已卸载的链接上，下次Tab从文档顶部重新开始。修复：路由变化后将焦点移到h1（tabIndex={-1}）或main元素，约15行Client Component。
（来源：https://dev.to/ahmed_mahmoud360/focus-management-in-the-nextjs-app-router-field-notes-on-the-route-change-that-loses-focus-295d ，https://accessibility.build/guides/react-accessibility）

**知识点8：模态框/对话框必须实现焦点陷阱（focus trap）**
打开模态框时焦点移入模态框，Tab在模态框内循环（第一个和最后一个元素之间循环），Escape关闭，关闭后焦点返回触发按钮。用inert属性使背景内容不可访问。原生dialog元素已内置部分行为但浏览器支持需注意。
（来源：https://thefrontkit.com/blogs/keyboard-navigation-patterns-for-web-apps ，https://accessibility.build/blog/focus-management-accessibility-guide）

**知识点9：图片必须有alt文本，装饰性图片用alt=""**
工具logo、产品截图必须有描述性alt。纯装饰性图片（背景、分隔线）用alt=""让屏幕阅读器跳过。Next.js Image组件的alt属性是必填的。AIToolCrux有56篇文章有截图，需确保alt不为空且描述准确。
（来源：https://www.w3.org/WAI/standards-guidelines/wcag/ ，https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics）

**知识点10：颜色对比度AA级要求：正文4.5:1，大文本3:1**
WCAG AA要求正常文本与背景对比度至少4.5:1，大文本（18pt+或14pt+粗体）至少3:1。UI组件和图形对象至少3:1。Tailwind的zinc-500在白色背景上可能不足4.5:1，需检查。可用Chrome DevTools的Contrast检查器或axe DevTools审计。
（来源：https://www.w3.org/TR/WCAG22/ ，https://www.w3.org/WAI/standards-guidelines/wcag/）

**知识点11：表单必须有关联label，错误信息需关联到输入框**
每个input必须有可见label（用htmlFor/id关联），不能只用placeholder。错误信息用aria-describedby关联到输入框，并用aria-invalid="true"标记。AIToolCrux的contact页面如有表单需检查。搜索框应有aria-label。
（来源：https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Understanding_WCAG/Text_labels_and_names ，https://www.w3.org/TR/WCAG22/）

**知识点12：页面必须有且仅有一个h1，标题层级不能跳级**
每个页面一个h1（页面主标题），h2-h6按顺序使用不能从h2跳到h4。OpenSEO审计发现669个heading-order-skip问题，这是最大的可访问性问题。文章页的HTML内容必须确保标题层级正确。
（来源：https://www.w3.org/TR/WCAG22/ ，https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/heading_role）

**知识点13：ARIA live region用于动态内容更新通知**
搜索结果、表单提交反馈、加载状态等动态更新内容用aria-live="polite"或aria-live="assertive"通知屏幕阅读器。AIToolCrux的SearchBox搜索结果、compare页工具选择变化应考虑添加live region。
（来源：https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA ，https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Accessible_web_applications_and_widgets）

**知识点14：可访问性审计工具：axe DevTools + Lighthouse + WAVE**
axe DevTools（Chrome扩展，Deque Systems开发）是最准确的自动化审计工具，可检测约57%的可访问性问题。Lighthouse有Accessibility评分。WAVE（WebAIM）提供可视化标注。自动化只能发现部分问题，键盘导航和屏幕阅读器测试必须手动。
（来源：https://accessibility.build/guides/react-accessibility ，https://www.w3.org/WAI/standards-guidelines/wcag/）

**知识点15：skip link（跳过导航链接）是多页站的基本可访问性组件**
页面顶部第一个可聚焦元素应为"跳到主内容"链接（视觉隐藏，聚焦时显示），让键盘用户跳过重复导航直接到main。实现：a[href="#main"]绝对定位，:focus时显示。AIToolCrux应添加skip link到layout.tsx。
（来源：https://accessibility.build/guides/react-accessibility ，https://www.iamuvin.com/blog/design-web-accessibility-nextjs-wcag-guide）

**落地计划：**
- 知识点12 -> P1-A11Y-HEADING-001：修复OpenSEO发现的669个heading-order-skip问题，从文章模板和工具页开始
- 知识点7 -> P1-A11Y-ROUTE-FOCUS-001：Next.js App Router路由变化后焦点管理，添加Client Component聚焦h1
- 知识点15 -> P1-A11Y-SKIP-LINK-001：layout.tsx添加skip link跳到主内容
- 知识点6 -> P1-A11Y-FOCUS-VISIBLE-001：审计全站焦点指示器，确保无outline:none无替代
- 知识点14 -> P2-A11Y-AXE-AUDIT-001：CI中集成axe-core自动化可访问性审计



### [2026-09-25] 前端安全最佳实践：CSP + XSS防护 + 依赖安全 + 安全头（15知识点）

**知识点1：CSP是XSS的最后一道防线，不是第一道**
CSP通过限制可执行脚本来源缓解XSS，但不能替代输入验证和输出编码。React JSX自动转义是第一道防线，CSP是纵深防御。AIToolCrux已在next.config.mjs配置CSP头。
（来源：https://nextjs.org/docs/app/guides/content-security-policy ，https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet）

**知识点2：严格CSP应使用nonce或hash，避免unsafe-inline**
script-src 'unsafe-inline'会大幅削弱CSP效果。严格CSP用nonce（每次请求生成随机值）或hash（允许特定脚本内容）。Next.js中间件可生成nonce并注入header。但SSG静态站点无法动态生成nonce，需权衡。
（来源：https://nextjs.org/docs/app/guides/content-security-policy ，https://web.dev/articles/security-headers）

**知识点3：dangerouslySetInnerHTML是React XSS的主要风险点**
React JSX文本插值自动转义，但dangerouslySetInnerHTML绕过转义直接插入HTML。AIToolCrux文章内容用HTML标签渲染，必须确认是否用了dangerouslySetInnerHTML。如果用了，必须用DOMPurify消毒。
（来源：https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet ，https://tomodahinata.com/en/blog/nextjs-xss-dom-xss-dangerouslysetinnerhtml-prevention-guide）

**知识点4：href/src属性中的用户输入也是XSS向量**
javascript:协议URL可在href中执行脚本。必须验证用户提供的URL，拒绝javascript:、data:text/html等危险协议。工具页的affiliateUrl/officialUrl来自数据文件，但应做协议白名单（只允许http/https）。
（来源：https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet ，https://oneuptime.com/blog/post/2026-01-15-prevent-xss-attacks-react/view）

**知识点5：Next.js Server Components中的用户输入也需编码**
Server Components和generateMetadata中插值用户数据（如searchParams）到HTML/meta标签时，同样存在反射型XSS风险。模板字符串拼接到非JSX上下文需注意编码。Next.js对JSX插值自动转义。
（来源：https://cheatsheetseries.owasp.org/cheatsheets/Nextjs_Security_Cheat_Sheet.html ，https://teachmeidea.com/xss-prevention-modern-web-apps-practical-guide/）

**知识点6：HSTS必须设置max-age>=63072000（2年）并含includeSubDomains和preload**
AIToolCrux已设置max-age=63072000; includeSubDomains; preload，符合标准。HSTS告诉浏览器始终用HTTPS访问，防止SSL剥离攻击。preload指令可提交到浏览器HSTS预加载列表。
（来源：https://web.dev/articles/security-headers ，https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP）

**知识点7：X-Content-Type-Options: nosniff防止MIME类型嗅探**
浏览器可能根据文件内容猜测MIME类型而非Content-Type头，导致非脚本文件被当作脚本执行。nosniff强制浏览器尊重Content-Type头。AIToolCrux已设置。
（来源：https://web.dev/articles/security-headers ，https://cheatsheetseries.owasp.org/cheatsheets/Nextjs_Security_Cheat_Sheet.html）

**知识点8：X-Frame-Options: SAMEORIGIN防止点击劫持**
点击劫持通过iframe嵌套页面诱导用户点击。SAMEORIGIN只允许同域iframe嵌套。更现代的替代是CSP的frame-ancestors指令。AIToolCrux已设置X-Frame-Options。
（来源：https://web.dev/articles/security-headers ，https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP）

**知识点9：Referrer-Policy: strict-origin-when-cross-origin是推荐值**
跨域请求只发送origin（不含路径和查询参数），同域发送完整URL。保护敏感URL中的查询参数不泄露给第三方。AIToolCrux已设置。
（来源：https://web.dev/articles/security-headers ，https://cheatsheetseries.owasp.org/cheatsheets/Nextjs_Security_Cheat_Sheet.html）

**知识点10：Permissions-Policy限制浏览器功能访问**
camera=(), microphone=(), geolocation=()明确禁用不需要的API，防止被恶意脚本利用。AIToolCrux已设置。还可考虑添加payment=(), usb=(), magnetometer=()等。
（来源：https://web.dev/articles/security-headers ，https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP）

**知识点11：npm audit在CI中作为安全门禁**
npm audit检查依赖中的已知漏洞。可在CI中添加npm audit --audit-level=high步骤，high及以上漏洞阻断构建。AIToolCrux已有dependency-review-action（PR时检查依赖变更），可补充npm audit步骤。
（来源：https://github.blog/2023-01-19-unlocking-security-updates-for-transitive-dependencies-with-npm/ ，https://shattered.io/npm-audit-nodejs/）

**知识点12：Dependabot安全更新自动创建修复PR**
Dependabot监控依赖漏洞，发现可修复版本时自动创建PR。配置.github/dependabot.yml设置weekly检查和open-pull-requests-limit。AIToolCrux第83轮已添加Dependabot，需确认security updates已启用。
（来源：https://learn.microsoft.com/fil-ph/training/modules/software-composition-analysis/4-implement-github-dependabot-alerts-security-updates ，https://github.blog/2023-01-19-unlocking-security-updates-for-transitive-dependencies-with-npm/）

**知识点13：传递依赖漏洞是主要风险源，npm audit fix可能不够**
大多数漏洞在传递依赖（transitive dependencies）中。npm audit fix只修复有兼容更新的漏洞。对于无法自动修复的，需用npm overrides强制升级或等待上游修复。lockfile确保可复现构建。
（来源：https://github.blog/2023-01-19-unlocking-security-updates-for-transitive-dependencies-with-npm/ ，https://shattered.io/npm-audit-nodejs/）

**知识点14：CSP report-uri/report-to用于监控违规而不阻断**
先用Content-Security-Policy-Report-Only头收集违规报告，确认无误后再切换为强制模式。report-uri已废弃但仍广泛支持，report-to是新标准。AIToolCrux直接用了强制CSP，需监控是否有广告/分析脚本被误拦。
（来源：https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/report-uri ，https://nextjs.org/docs/app/guides/content-security-policy）

**知识点15：第三方脚本（AdSense/GA4/Umami）必须在CSP中显式允许**
AIToolCrux CSP的script-src已包含pagead2.googlesyndication.com、googletagmanager.com、google-analytics.com、analytics.umami.is、hm.baidu.com。connect-src也需对应允许。新增第三方服务时必须同步更新CSP，否则脚本被阻断。AdSense的frame-src也已配置。
（来源：https://nextjs.org/docs/app/guides/content-security-policy ，https://web.dev/articles/security-headers）

**落地计划：**
- 知识点3+4 -> 审计文章页和工具页是否使用dangerouslySetInnerHTML渲染内容，URL属性是否做协议白名单
- 知识点11 -> CI中添加npm audit --audit-level=high步骤
- 知识点14 -> 评估将CSP改为Report-Only模式一周收集违规，再切回强制
- 知识点10 -> 扩展Permissions-Policy添加payment/usb/magnetometer禁用
- 知识点12 -> 确认Dependabot security updates已在GitHub repo设置中启用



[2026-09-25] Next.js性能优化：Image Optimization+Font Optimization+Streaming+Partial Prerendering（来源：Next.js官方文档）

知识点1：next/image组件核心优势——扩展HTML img元素提供4大优化：①尺寸优化（自动为每设备提供正确尺寸+WebP/AVIF现代格式）②视觉稳定性（自动防止layout shift/CLS）③更快加载（视口内才加载，原生lazy loading+可选blur-up占位）④资产灵活性（远程图片也可按需调整大小）。AIToolCrux文章中的截图目前用原始img标签，未享受这些优化。（来源：https://nextjs.org/docs/app/getting-started/images）

知识点2：priority属性与LCP——对页面LCP元素（视口内最大可见图片/文本块）添加priority={true}，Next.js通过preload标签/priority hints特殊优先加载，显著提升LCP分数。priority图片自动禁用lazy loading。每个页面应有一个priority图片（通常是hero图/首屏大图）。第83轮已对工具详情页LCP图片转next/image+priority，但文章页首屏截图尚未处理。（来源：https://nextjs.org/docs/app/building-your-application/optimizing/images）

知识点3：width/height防止CLS——必须提供width和height（或fill模式+容器sizes），用于推断正确宽高比，在图片加载前预留空间防止layout shift。远程图片构建时无法获取尺寸，必须手动提供width/height。AIToolCrux文章中的截图用原始img标签可能缺width/height，是CLS的潜在来源（Core Web Vitals学习中已识别CLS风险）。（来源：https://nextjs.org/docs/app/api-reference/components/image）

知识点4：sizes属性——告诉浏览器不同视口宽度下图片显示尺寸，如sizes="(max-width: 768px) 100vw, 33vw"。Next.js根据sizes生成正确的srcset（多个分辨率版本），避免在小屏设备加载过大图片。不设sizes时默认100vw，可能导致列表页缩略图加载过大图片浪费带宽。（来源：https://nextjs.org/docs/app/api-reference/components/image）

知识点5：图片格式AVIF/WebP——next.config.js的images.formats配置，默认['image/webp']，可加AVIF：['image/avif', 'image/webp']。Next.js通过请求Accept头自动检测浏览器支持格式，数组中第一个匹配的优先使用。AVIF通常比WebP小20-30%但首次编码慢（后续缓存）。AIToolCrux的next.config.mjs已配置AVIF+WebP+remotePatterns通配。（来源：https://nextjs.org/docs/14/app/api-reference/components/image）

知识点6：remotePatterns远程图片白名单——远程图片必须在next.config.js的images.remotePatterns中配置白名单（protocol/hostname/port/pathname），否则next/image拒绝加载远程图片并报错。支持通配符**匹配任意子域名。AIToolCrux已配置remotePatterns通配，可加载任意远程图片。（来源：https://nextjs.org/docs/app/api-reference/components/image）

知识点7：placeholder="blur"模糊占位——图片加载时显示模糊占位（blur-up效果），提升感知性能和用户体验。本地图片自动生成blurDataURL，远程图片需手动提供blurDataURL（可用plaiceholder库生成base64占位）。需配合width/height使用。适合文章页长截图，减少空白感。（来源：https://nextjs.org/docs/app/api-reference/components/image）

知识点8：next/font概述——自动优化字体（含自定义字体），移除外部网络请求提升隐私和性能。内置任何字体文件的自动self-hosting：构建时下载Google Fonts的CSS和字体文件，与其他静态资产一起self-hosted，浏览器不向Google发任何请求。消除外部字体请求的DNS/TLS/下载延迟。（来源：https://nextjs.org/docs/app/getting-started/fonts）

知识点9：next/font零CLS原理——通过底层CSS size-adjust属性实现零布局偏移加载web字体。自动回退字体（adjustFontFallback默认true）：在自定义字体加载前用系统回退字体显示文本，size-adjust自动调整回退字体尺寸匹配目标字体的metrics，消除font swap时的layout shift（CLS）。这是next/font相比传统@font-face的核心优势。（来源：https://nextjs.org/docs/pages/building-your-application/optimizing/fonts）

知识点10：next/font/google用法——import { Inter } from 'next/font/google'，const inter = Inter({ subsets: ['latin'], weight: ['400','600','700'], display: 'swap' })，在layout.tsx的<html className={inter.className}>应用。支持variable CSS变量方式：const inter = Inter({ variable: '--font-inter' })，配合tailwind.config的fontFamily.extend使用。需指定subsets减少字体文件大小。（来源：https://nextjs.org/docs/app/getting-started/fonts）

知识点11：next/font/local自定义字体——import localFont from 'next/font/local'，const myFont = localFont({ src: './my-font.woff2', display: 'swap' })。支持多个字体文件：src: [{ path: './regular.woff2', weight: '400' }, { path: './bold.woff2', weight: '700' }]。字体文件放在app目录下，构建时自动处理和self-host。适合品牌定制字体。（来源：https://nextjs.org/docs/app/getting-started/fonts）

知识点12：Streaming流式渲染概述——将页面HTML分块从服务器逐步发送到客户端，而非等待全部渲染完成才发送。两种实现方式：①loading.tsx包裹整个路由段（自动创建Suspense边界）②<Suspense>包裹单个组件（更细粒度控制）。响应体在第一个Suspense fallback渲染时开始流式传输，后续内容逐步到达。（来源：https://nextjs.org/docs/app/getting-started/fetching-data）

知识点13：loading.tsx约定——app/feed/loading.tsx自动创建Suspense边界包裹该路由段内容，服务器端显示即时加载状态（skeleton/骨架屏），内容流式到达后自动替换。支持嵌套路由：父loading显示时子路由内容独立流式加载。注意：notFound()应在任何await之前调用以获得正确HTTP 404状态码（流式传输后无法改状态码）。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/loading）

知识点14：Partial Prerendering (PPR)——结合SSG的静态shell和SSR的动态内容。构建时预渲染静态内容+Suspense fallback UI，请求时立即发送静态HTML shell，动态内容流式推送。用<Suspense>标记动态边界（包裹使用cookies()/headers()/unstable_noStore()等动态API的组件）。Next.js 14为实验特性（experimental.ppr=true），15+逐步稳定。关键：包裹Suspense不使组件本身变动态，组件内的动态API调用才决定。（来源：https://nextjs.org/docs/app/getting-started/partial-prerendering）

知识点15：PPR请求时流程与适用场景——请求到达时：①服务器立即发送静态HTML shell给客户端②服务器用postponed state恢复渲染动态部分③动态内容流式传输，React hydration延迟的Suspense边界④客户端立即看到静态shell，动态内容解析后出现。适合：大部分静态+少量动态的页面（如博客+评论区、产品页+实时库存、文档站+个性化推荐）。AIToolCrux当前是纯SSG无动态内容，PPR暂不适用；但未来加用户评论/个性化推荐/实时价格时，PPR是最佳方案（比全SSR快、比全SSG灵活）。（来源：https://nextjs.org/docs/app/guides/ppr-platform-guide）

落地计划：
- 知识点1-3（next/image+priority+width/height）→ P1-PERF-ARTICLE-IMAGES-001：将文章页截图从原始img标签迁移到next/image，添加width/height防CLS，首屏截图加priority
- 知识点4（sizes）→ 工具列表页ToolCard图片添加正确sizes属性，避免小屏加载过大图片
- 知识点7（placeholder blur）→ 文章页长截图添加blur-up占位，提升感知性能
- 知识点8-10（next/font）→ P1-PERF-FONT-OPTIMIZE-001：检查layout.tsx是否使用next/font（当前可能用CSS @import或CDN字体），迁移到next/font/google实现零CLS字体加载
- 知识点12-13（Streaming）→ 当前SSG不需要streaming，但未来加动态功能时用loading.tsx+Suspense
- 知识点14-15（PPR）→ 未来加评论/个性化功能时启用PPR，当前纯静态不适用


[2026-09-25] 前端工程化最佳实践：代码分割+构建优化+Monorepo（来源：Next.js官方文档+Turborepo官方文档+Vercel官方文档）

知识点1：Next.js自动代码分割——按路由自动分割应用代码，导航时只加载当前路由需要的JS，减少初始加载时间。Server Components默认自动代码分割，且可通过streaming逐步从服务器发送UI片段。Client Components不会自动按组件分割，需要手动lazy loading。（来源：https://nextjs.org/docs/app/glossary）

知识点2：next/dynamic动态导入——React.lazy()+Suspense的组合封装，在app和pages目录行为一致。支持选项：ssr:false（纯客户端渲染，不SSR）、loading（加载时显示的组件）、suspense:true（配合Suspense边界）。典型用途：延迟加载Modal/Tabs/重型图表组件，使其不包含在页面初始JS bundle中。（来源：https://nextjs.org/docs/app/guides/lazy-loading）

知识点3：第三方库懒加载——对重型第三方库（图表库、富文本编辑器、动画库、代码高亮）使用动态导入，只在用户交互需要时加载。例如`const Editor = dynamic(() => import('../components/Editor'), { ssr: false, loading: () => <p>Loading...</p> })`。避免在页面顶部import大型库导致初始bundle膨胀。（来源：https://nextjs.org/docs/app/guides/lazy-loading）

知识点4：Server Components减少客户端bundle——Server Components在服务器运行，不发送任何JS到客户端，对客户端bundle大小零影响。最佳实践：默认用Server Components，只在需要交互（useState/useEffect/事件处理/浏览器API）时才用Client Components（"use client"）。将Client Components尽量下沉到叶子节点，使大部分UI保持Server Component。（来源：https://nextjs.org/docs/app/guides/production-checklist）

知识点5：@next/bundle-analyzer——Next.js官方bundle分析插件，生成可视化报告显示每个包及其依赖的大小。安装：`npm install @next/bundle-analyzer`，配置next.config.js的withBundleAnalyzer，运行`ANALYZE=true npm run build`生成report.html。用于发现大型依赖、决定是否拆分或懒加载。Next.js 16.1新增Turbopack版实验性Bundle Analyzer（next experimental-analyze）。（来源：https://nextjs.org/docs/app/guides/package-bundling）

知识点6：optimizePackageImports——对导出数百/数千模块的包（如lucide-react、antd、@mui/icons-material、lodash），添加到next.config.js的experimental.optimizePackageImports数组，只加载实际使用的模块而非全量导入。lucide-react和某些库默认已优化。AIToolCrux的next.config.mjs已配置lucide-react和framer-motion。效果：显著减少这些库的tree-shaking后体积。（来源：https://nextjs.org/docs/app/api-reference/next-config-js/optimizePackageImports）

知识点7：Tree Shaking原理——构建时自动移除未使用的导出代码（dead code elimination）。前提条件：使用ES模块语法（import/export）而非CommonJS（require/module.exports），因为ES模块静态可分析。避免`import * as X from 'lib'`全量导入（阻止tree-shaking），改用命名导入`import { Button } from 'lib'`。第三方库需提供ES模块版本（package.json的module字段）。（来源：https://nextjs.org/docs/app/glossary）

知识点8：Turbopack构建工具——Next.js的Rust编写构建工具，开发环境比Webpack快10倍。核心特性：增量计算（函数级缓存，已完成的工作不重复）、懒打包（只打包dev server实际请求的模块，减少初始编译时间和内存）、跨核心并行。Next.js 14生产环境仍用Webpack，Next.js 15+生产环境Turbopack逐步稳定。AIToolCrux当前Next.js 14.2.5，dev可用Turbopack（--turbo），生产用Webpack。（来源：https://nextjs.org/docs/app/api-reference/turbopack）

知识点9：Turborepo概述——Vercel官方的Monorepo构建系统（GitHub 25k+ stars），核心能力：增量任务运行（只执行变更影响的任务）、本地+远程缓存（任务结果缓存复用）、并行执行（无依赖任务并行）。Remote Cache存储所有任务结果，使CI永远不重复相同工作。turbo.json配置pipeline定义任务依赖关系图。（来源：https://turborepo.dev/docs）

知识点10：Turborepo任务缓存机制——每个任务的缓存key由输入（源文件hash+环境变量+依赖版本hash+任务参数）决定，命中缓存直接复用输出（outputs配置的文件）跳过执行。本地缓存（.turbo/cache）+ Vercel Remote Cache（跨机器/CI共享，需turbo login+turbo link）。可配置--cache-dir自定义缓存路径，--no-cache禁用缓存。（来源：https://turborepo.dev/docs/reference/run）

知识点11：Turborepo Pipeline配置——turbo.json中定义任务依赖图，关键配置：dependsOn（如"build": {"dependsOn": ["^build"]}表示依赖包先构建）、outputs（任务输出文件如[".next/**"]）、inputs（影响缓存的输入文件）、cache（设false禁用缓存，如dev任务）、persistent（长期运行任务如dev）。支持env配置环境变量作为缓存输入。（来源：https://turborepo.dev/docs）

知识点12：Next.js构建内存优化——大项目SSG（533工具+105文章全量静态生成）构建时内存可能溢出。优化方法：①减少依赖数量（Bundle Analyzer发现可移除的大依赖）②Next.js 15+用experimental.webpackMemoryOptimizations:true③增加Node内存上限`NODE_OPTIONS=--max-old-space-size=8192`④分批生成（用generateStaticParams限制每次构建页面数）⑤升级Node版本。AIToolCrux曾遇到构建内存问题（P1-PERF-BUILD-MEMORY-001待办）。（来源：https://nextjs.org/docs/app/guides/memory-usage）

知识点13：Link预取策略——Next.js的Link组件在生产环境默认prefetch视口内的链接（预取页面代码和数据），加速导航。可设prefetch={false}禁用（第91轮已对工具列表页ToolCard设prefetch={false}减少带宽）。注意：prefetch只在生产环境生效，开发环境不预取；prefetch会增加带宽消耗，对大量链接的列表页应谨慎使用。（来源：https://nextjs.org/docs/app/guides/production-checklist）

知识点14：依赖大小审计工具——添加新依赖前先查体积：Import Cost（VSCode扩展，行内显示导入包大小）、Package Phobia（web端查包安装大小和gzip大小）、Bundle Phobia（查包对bundle的影响）、bundlejs（在线打包测试）。避免引入大型库（如moment.js可换day.js，lodash可换lodash-es或原生方法）。AIToolCrux已有.size-limit.json做CI bundle门禁（4条预算规则）。（来源：https://nextjs.org/docs/app/guides/production-checklist）

知识点15：构建优化组合策略——①Server Components优先（最大程度减少客户端bundle）②next/dynamic懒加载重型组件/第三方库③optimizePackageImports优化大图标库/组件库④定期用Bundle Analyzer审计bundle⑤size-limit CI门禁防止bundle膨胀（AIToolCrux已有）⑥Turborepo缓存加速CI构建⑦NODE_OPTIONS内存调优应对大SSG构建。AIToolCrux已实现①③⑤，需加强②（重型组件懒加载）④（定期bundle审计）⑦（构建内存调优）。（来源：综合Next.js+Turborepo官方文档）

落地计划：
- 知识点2-3（next/dynamic懒加载）→ P1-PERF-DYNAMIC-IMPORT-001：审计Client Components，对重型组件（如compare页的工具选择器、搜索弹窗）使用next/dynamic懒加载
- 知识点5（Bundle Analyzer）→ P1-PERF-BUNDLE-ANALYZE-001：运行@next/bundle-analyzer生成报告，识别最大依赖，制定优化计划
- 知识点12（构建内存优化）→ P1-PERF-BUILD-MEMORY-001：配置NODE_OPTIONS=--max-old-space-size=8192和experimental.webpackMemoryOptimizations，解决SSG构建内存溢出
- 知识点6（optimizePackageImports）→ 检查next.config.mjs是否需添加更多包（如recharts/date-fns等如果使用）
- 知识点14（依赖审计）→ P2-QA-DEP-AUDIT-001：定期审计package.json依赖，移除未使用或可替换的大型依赖


[2026-09-25] SEO工程化：GSC API自动化+索引优化+AI搜索优化（llms.txt）（来源：Google官方文档+llmstxt.org规范+IndexNow官方FAQ）

知识点1：GSC Search Analytics API——POST /sites/{siteUrl}/searchAnalytics/query，核心参数：startDate/endDate（必需，至少1天）、dimensions（country/device/page/query/searchAppearance，可组合）、rowLimit（默认1000最大25000）、startRow（分页）、aggregationType（auto/byPage/byProperty）。结果按点击数降序排列，需要OAuth 2.0授权。AIToolCrux的gsc-fetch.yml已用此API每日拉取数据。（来源：https://developers.google.com/webmaster-tools/v1/searchanalytics/query）

知识点2：GSC API维度组合规则——dimensions可选5个值：country（国家）、device（设备桌面/移动/平板）、page（页面URL）、query（搜索查询词）、searchAppearance（搜索外观如Rich Results）。可组合多个维度（如["page","query"]获取每页每个查询词的表现）。特殊规则：如果date是维度之一，无数据的日期会被省略；需了解哪些天有数据，先查不带过滤按date分组的查询。（来源：https://developers.google.com/webmaster-tools/v1/searchanalytics/query）

知识点3：GSC API过滤与数据状态——dimensionFilterGroups支持AND/OR逻辑组，每个filter含dimension/operator（equals/contains/notContains/not等）/expression。可过滤特定页面（如只查/blog/*路径）、国家、设备。dataState参数："final"（最终数据，2-3天延迟）或"all"（含最新未最终化数据，可能不完整）。API配额：每项目每天50,000次查询，每分钟2,000次。（来源：https://developers.google.com/webmaster-tools/v1/searchanalytics/query）

知识点4：GSC API Sitemaps资源自动化——sitemaps.list列出所有已提交sitemap；sitemaps.get获取单个sitemap详情（提交日期/最后下载日期/错误数/警告数/已发现URL数/内容类型）；sitemaps.submit提交新sitemap；sitemaps.delete删除sitemap。可自动化监控sitemap健康状态，发现错误数增加时告警。（来源：https://developers.google.com/webmaster-tools/v1/sitemaps/）

知识点5：GSC API URL Inspection——urlInspection.index.inspect检查单个URL的索引状态，返回coverageState（已索引/已排除原因）、robotsTxtState（允许/阻止）、crawledAs（Googlebot类型）、googleCanonical（Google选择的canonical）、userCanonical（页面声明的canonical）、lastCrawlTime（最后爬取时间）、referringUrls（引用该URL的页面）。可自动化监控页面是否被索引、canonical是否被Google改写。（来源：https://developers.google.com/webmaster-tools/v1/api_reference_index）

知识点6：llms.txt概述——被称为"AI搜索时代的robots.txt"，是纯文本/Markdown文件放在网站根目录（/llms.txt），帮助AI爬虫和LLM快速理解网站结构和高价值内容。由llmstxt.org维护规范，v2版本已发布。与robots.txt（阻止/允许爬取）不同，llms.txt是主动引导AI关注哪些内容。（来源：https://llmstxt.org/ + Search Engine Land）

知识点7：llms.txt必需元素结构——# H1标题（网站/项目名，唯一必需元素）、> blockquote一句话电梯演讲（紧跟H1后，含关键事实）、## H2分组（逻辑分组链接如"核心工具页"/"评测文章"/"对比页"）、- [Title](url): description（每个链接带简洁描述）。文件Content-Type为text/plain或text/markdown，返回HTTP 200。（来源：https://llmstxt.org/ 规范）

知识点8：llms-full.txt完整内容导出——与llms.txt（导航索引视图）配合，llms-full.txt包含所有文档的纯Markdown格式完整内容，供AI爬虫批量获取。Zapier/Cloudflare等公司已部署。生成方式：从现有内容库/知识库导出，转换为Markdown，放在根目录。AIToolCrux已有public/llms.txt（2856字节）和public/llms-full.txt（464941字节）。（来源：https://searchengineland.com/guide/optimize-for-ai-crawlers）

知识点9：llms.txt v2规范更新——支持子路径文件（/docs/llms.txt覆盖该路径下页面，最具体的文件优先）；"Optional"标记失去机械语义；链接应指向LLM友好内容（Markdown版本页面）；基于137,000个域名的实际数据分析。v2简化了规范，减少了不必要的复杂性。（来源：https://dev.to/angeo/llmstxt-v2-what-the-spec-says-and-what-137000-domains-show-48bh）

知识点10：llms.txt技术最佳实践——所有列出的URL返回HTTP 200（无301/302重定向、无404）；不被robots.txt阻止；没有noindex meta robots标签；设置Cache-Control: public, max-age=86400（允许AI缓存）；链接到高质量权威页面而非薄内容页；描述简洁准确（10-30字），包含关键词帮助AI理解页面主题。（来源：https://theindexcraft.com/technical/llm-txt-guide）

知识点11：Google sitemap索引优化——sitemap是告诉Google哪些页面重要的主要方式，Google优先爬取sitemap中的页面。单个sitemap限制50MB（未压缩）或50,000个URL，超出需拆分多个sitemap并用sitemap index文件（sitemap.xml包含子sitemap列表）。sitemap中URL应包含lastmod（最后修改时间）、priority（优先级0.0-1.0）、changefreq（更新频率）元数据。AIToolCrux的sitemap.ts已包含工具页/文章页/分类页/子分类页/对比页。（来源：https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap）

知识点12：Google Request Indexing——GSC的URL Inspection工具可手动请求索引，有软日限额约10-12 URL/天。适合新发布页面或重要更新页面。不要对所有页面滥用，优先高质量高价值页面。请求索引后Google可能需要数小时到数天实际爬取和索引。（来源：https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl）

知识点13：IndexNow协议——微软Bing/Yandex等搜索引擎支持的即时索引协议。流程：在indexnow.org生成API key → 托管key文件在域名根目录（如/3f7f80308bcbbd81d91bd93cdc0e1120.txt）→ 通过API提交URL（单条POST或批量最多10,000条/请求）。Google截至2026年5月未正式支持IndexNow，但Bing/Yandex支持。AIToolCrux已配置IndexNow，第85轮批量提交714 URL返回HTTP 200。（来源：https://www.indexnow.org/faq）

知识点14：Google Indexing API限制——Indexing API（不同于Search Console API）只能用于包含JobPosting或BroadcastEvent结构化数据的页面，不能用于普通内容页面。普通页面应通过：①sitemap提交（批量）②GSC Request Indexing（少量高优先级）③内链建设（最重要的自然发现方式）来加速索引。内链是Google发现新页面的最有效自然方式，sitemap是辅助。（来源：https://developers.google.com/search/apis/indexing-api/v3/using-api）

知识点15：索引优化组合策略——新页面发布后：①自动更新sitemap.xml（Next.js动态sitemap）②通过IndexNow提交到Bing/Yandex（即时）③在已有排名文章中添加内链指向新页面（最重要，第92轮已做36个内链）④对高优先级页面用GSC Request Indexing（每天≤12个）⑤监控GSC Coverage报告发现被排除页面。避免：对薄内容页请求索引（浪费配额）、sitemap包含noindex页面（混淆Google）、大量301/302 URL在sitemap中。（来源：综合Google官方文档+IndexNow FAQ+实践经验）

落地计划：
- 知识点1-3（GSC Search Analytics）→ P1-SEO-GSC-AUTOMATION-001：增强gsc-fetch.yml，添加按page+query维度的查询，发现0点击高曝光页面（如dify/cursor排名5-7但0点击的问题），自动生成优化建议
- 知识点5（URL Inspection API）→ P1-SEO-INDEX-MONITOR-001：用URL Inspection API自动化监控关键页面索引状态，发现canonical被Google改写或被排除时告警
- 知识点7-10（llms.txt）→ P1-SEO-LLMSTXT-001：优化现有llms.txt，确保所有链接200、添加H2分组、更新描述；定期更新llms-full.txt包含最新文章和工具
- 知识点11-15（索引优化）→ P1-SEO-INDEX-STRATEGY-001：建立新页面发布后的索引自动化流程（sitemap更新+IndexNow提交+内链建设+GSC监控）


[2026-09-25] 高星GitHub开源工具：Playwright+Lighthouse CI+Unlighthouse+Pa11y（来源：官方文档+GitHub README）

知识点1：Playwright概述——Microsoft开源的端到端测试框架（GitHub 60k+ stars），支持Chromium/Firefox/WebKit三大浏览器引擎，提供TypeScript/Python/.NET/Java多语言API。一个API驱动所有浏览器，适用于测试、脚本和AI Agent工作流。（来源：https://playwright.dev/）

知识点2：Playwright自动等待机制——locators自动等待元素处于可交互状态（visible+enabled+stable+receives events），web-first断言（expect）自动重试直到条件满足或超时。无需手动setTimeout/waitForSelector，从根本上消除flaky tests（不稳定测试）。（来源：https://playwright.dev/docs/best-practices）

知识点3：Playwright测试隔离——每个测试获得全新的browser context（相当于全新浏览器配置文件，包含cookies/localStorage/storage隔离），近零开销实现完全隔离。可通过storageState保存认证状态（如登录态），在多个测试中复用，避免每个测试重新登录。（来源：https://playwright.dev/）

知识点4：Playwright Locators弹性定位——优先使用用户可见属性定位元素：page.getByRole()（按ARIA角色）、page.getByText()（按文本）、page.getByLabel()（按表单label）、page.getByPlaceholder()、page.getByAltText()、page.getByTitle()、page.getByTestId()。避免使用脆弱的CSS选择器或XPath，因为它们不反映用户视角且易因DOM结构变化而失效。（来源：https://playwright.dev/docs/best-practices）

知识点5：Playwright Fixtures——通过test.extend()创建自定义fixture，支持setup（测试前准备）和teardown（测试后清理），可在测试间共享资源（如测试用户账号、数据库连接、API客户端）。比beforeEach/beforeAll更灵活，支持按需懒加载和参数化fixture。（来源：https://playwright.io/playwright/nodejs/fixtures）

知识点6：Playwright Trace Viewer——测试失败时自动录制trace文件，包含DOM快照、网络请求/响应、控制台日志、截图时间线、用户操作记录。可在trace.playwright.dev中时间旅行调试，逐步回放失败前的所有操作，是CI中调试E2E失败的最强大工具。（来源：https://playwright.dev/）

知识点7：Playwright并行与分片——测试默认并行运行（workers可配置），支持shard分片在多CI机器上分布运行（--shard=1/4），支持fullyParallel模式在单个文件内并行。可配置retries重试flaky测试（如retries: 2），CI中设置2次重试可显著降低假阳性失败率。（来源：https://playwright.dev/）

知识点8：Lighthouse CI（LHCI）——GoogleChrome/lighthouse-ci，自动在CI中运行Lighthouse审计防止性能回归。lhci autorun三步流程：collect（每个URL运行N次Lighthouse）→ assert（检查结果是否符合预算/断言）→ upload（存储结果到临时存储/文件系统/LHCI服务器）。（来源：https://googlechrome.github.io/lighthouse-ci/docs/getting-started.html）

知识点9：Lighthouse CI断言配置——.lighthouserc.json中assert.preset可选lighthouse:recommended（推荐规则集）/lighthouse:all（全部规则）/lighthouse:no-pwa（不含PWA规则）。可自定义断言：categories:performance设minScore阈值（如['error', {minScore: 0.8}]），特定audit（如largest-contentful-paint）设error/warn/off级别和阈值。（来源：https://googlechrome.github.io/lighthouse-ci/docs/configuration.html）

知识点10：Lighthouse CI上传选项——temporary-public-storage（临时公开存储7天，适合PR预览对比，AIToolCrux当前使用）、filesystem（本地文件系统存储）、lhci server（自建服务器，支持历史趋势对比和diff，需sqlite/mysql/postgres数据库）。对于长期性能监控，建议自建LHCI server。（来源：https://googlechrome.github.io/lighthouse-ci/docs/server.html）

知识点11：Unlighthouse——harlan-zw/unlighthouse，开源CLI工具，一条命令扫描全站Lighthouse（从sitemap.xml/robots.txt/内链自动发现URL），并行审计所有页面，提供现代UI仪表盘展示性能/可访问性/SEO/最佳实践分数。零配置核心：npx unlighthouse --site example.com。智能采样系统可控制审计深度。（来源：https://unlighthouse.dev/guide/getting-started/installation）

知识点12：Unlighthouse CI集成——unlighthouse-ci在CI pipeline中运行，任何页面分数低于预算则CI构建失败。支持--budget-threshold设置最低可接受分数（如0.8），--samples设置每页采样次数，--output-path设置报告输出路径。适合AIToolCrux这种533工具+105文章的大站点批量性能监控，弥补Lighthouse CI只审计4个URL的不足。（来源：https://unlighthouse.dev/integrations/ci）

知识点13：Pa11y——pa11y/pa11y，可访问性自动化测试工具（GitHub 2.5k+ stars），基于axe-core引擎，检查WCAG 2.1/2.2合规性（A/AA/AAA级别）。提供CLI+Node API+CI集成，可生成HTML/JSON/CSV报告。pa11y-ci可批量测试多URL并在CI中门禁。可与Playwright结合：Playwright做功能测试，Pa11y做可访问性审计。（来源：https://github.com/pa11y/pa11y）

知识点14：工具链组合最佳实践——分层覆盖策略：①Lighthouse CI（关键页面性能门禁，每次PR运行4个URL，快速反馈）②Unlighthouse（全站批量扫描，定时运行如每周一次，发现长尾页面性能问题）③Playwright（E2E功能测试，每次PR运行，防止功能回归）④Pa11y（可访问性审计，定时运行如每月，确保WCAG合规）。关键页面严格门禁 + 全站定期扫描 + 功能回归测试 + 可访问性合规，四层互补。（来源：综合Playwright/LHCI/Unlighthouse/Pa11y官方文档）

知识点15：CI性能测试注意事项——CI环境性能不稳定（共享CPU/内存/网络），Lighthouse分数波动可达10-20%。缓解方法：①多次运行取中位数（numberOfRuns≥3，AIToolCrux已设3次）②使用专用CI runner或增加CPU/内存资源③设置合理阈值（不要设太高如0.95，建议0.8）④用assertions的aggregationMethod选median optimistic（乐观中位数，排除异常低值）⑤在PR评论中展示分数diff而非绝对分数，关注趋势而非单次值。（来源：https://googlechrome.github.io/lighthouse-ci/docs/configuration.html + 实践经验）

落地计划：
- 知识点1-7（Playwright）→ P1-QA-PLAYWRIGHT-001：添加Playwright E2E测试覆盖关键页面路径（首页加载/工具详情页/文章页/搜索/compare页交互），配置trace录制+retries+shard
- 知识点11-12（Unlighthouse）→ P1-PERF-UNLIGHTHOUSE-001：添加Unlighthouse全站Lighthouse扫描CI workflow（每周运行，budget-threshold 0.8，覆盖533工具+105文章），弥补当前Lighthouse CI只审计4个URL的不足
- 知识点13（Pa11y）→ P2-QA-PA11Y-001：添加Pa11y可访问性审计，检查全站WCAG 2.1 AA合规，每月运行
- 知识点14-15（工具链组合+CI性能注意）→ 优化现有.lighthouserc.json配置，确认aggregationMethod和阈值合理性


[2026-09-25] Core Web Vitals优化完整指南：LCP+INP+CLS（来源：Google web.dev + Vercel + MDN官方文档）

知识点1：Core Web Vitals三大指标及阈值（基于p75真实用户数据）——LCP最大内容绘制：好≤2.5s/需改进2.5-4s/差>4s；INP交互到下一帧：好≤200ms/需改进200-500ms/差>500ms；CLS累积布局偏移：好≤0.1/需改进0.1-0.25/差>0.25。所有阈值取页面加载的75分位用户数据，不是平均值。（来源：https://developers.google.com/search/docs/appearance/core-web-vitals）

知识点2：LCP（最大内容绘制）衡量页面主要内容的加载速度——LCP元素通常是页面视口中最大的可见元素：<img>图片、<video poster>视频封面、CSS background-image、或包含大文本的块级元素。LCP时间=从导航开始到最大可见元素渲染完成的时间。用户在几秒内形成第一印象，慢LCP=高跳出率。（来源：https://web.dev/articles/top-cwv）

知识点3：LCP优化核心1——确保LCP资源可从HTML源中被发现。如果LCP图片是通过CSS background-image或JavaScript动态加载的，浏览器无法在初始HTML解析时发现它，会严重延迟LCP。解决方案：使用<img>标签直接在HTML中引用LCP图片，或使用<link rel="preload" as="image">预加载。Chrome团队发现这是Web上LCP问题最常见的根因。（来源：https://web.dev/articles/optimize-lcp）

知识点4：LCP优化核心2——使用fetchpriority="high"提升LCP图片优先级。浏览器默认按启发式分配资源优先级，LCP图片可能被降级。使用<img fetchpriority="high">告诉浏览器优先下载该图片。在Next.js中使用next/image的priority属性，自动添加fetchpriority="high"和preload hint。注意：next/image默认lazy-load所有图片包括LCP图片，必须加priority才能预加载。（来源：https://developer.mozilla.org/en-US/blog/fix-image-lcp/）

知识点5：LCP优化核心3——优化TTFB（首字节时间）。TTFB是从导航开始到收到第一个字节的时间，直接影响LCP。TTFB应控制在200ms以内。优化方法：使用CDN（Vercel Edge Network）、静态生成/ISR减少服务器渲染时间、缓存策略（Data Cache + Full Route Cache + CDN缓存）、避免阻塞性服务端逻辑。（来源：https://web.dev/articles/top-cwv）

知识点6：LCP优化核心4——图片优化。使用WebP/AVIF现代格式（比JPEG小25-35%）、适当尺寸（不要加载远超显示尺寸的大图）、srcset/sizes响应式图片、压缩。next/image自动处理格式转换（AVIF/WebP）、尺寸优化和lazy loading。sizes属性告诉浏览器图片渲染宽度，影响下载哪个尺寸的图片，设置不当可能浪费带宽。（来源：https://web.dev/articles/optimize-lcp）

知识点7：INP（交互到下一帧）2024年3月取代FID——INP衡量页面整个生命周期内所有交互（点击/触摸/键盘）的响应延迟，取p75值。INP=输入延迟（等待主线程）+处理延迟（事件处理器执行时间）+呈现延迟（浏览器渲染下一帧时间）。与FID只衡量首次交互不同，INP衡量所有交互，更全面。好的INP≤200ms。（来源：https://developers.google.com/search/docs/appearance/core-web-vitals）

知识点8：INP优化核心1——减少主线程Long Tasks。任何超过50ms的任务都会阻塞主线程，导致交互无法及时响应。优化方法：使用requestIdleCallback处理非紧急工作、将重型计算（如大数据排序/复杂DOM操作）移到Web Worker、拆分长任务为多个小任务（使用await yield控制）、避免在事件处理器中执行同步重排。（来源：https://web.dev/articles/optimize-inp）

知识点9：INP优化核心2——第三方脚本是INP最大杀手。广告（AdSense）、分析（GA4/Umami）、聊天widget（Crisp）等第三方脚本经常执行长任务阻塞主线程。优化方法：延迟加载第三方脚本（defer/async/Next.js的lazyOnload策略）、使用Partytown将第三方脚本移到Web Worker线程、评估每个第三方脚本的必要性，移除不用的、合并重复功能的。（来源：https://vercel.com/kb/guide/optimizing-core-web-vitals-in-2024）

知识点10：INP优化核心3——避免昂贵的事件处理器。事件处理器中不要执行重型DOM查询/操作或同步计算。优化方法：使用事件委托（在父元素监听而非每个子元素）、防抖/节流高频事件（scroll/resize/input）、将状态更新批量化（React 18自动批处理）、使用useTransition/useDeferredValue将非紧急更新标记为可中断。（来源：https://web.dev/articles/optimize-inp）

知识点11：CLS（累积布局偏移）衡量页面视觉稳定性——CLS计算整个页面生命周期内所有意外布局偏移的总和（不包括用户交互触发的偏移）。CLS=影响分数（受影响视口比例）×距离分数（移动距离占视口比例）。好的CLS≤0.1。常见原因：图片无尺寸导致加载后撑开布局、广告/嵌入内容无预留空间、动态注入内容（如横幅/通知）、Web字体加载导致FOIT/FOUT。（来源：https://developers.google.com/search/docs/appearance/core-web-vitals）

知识点12：CLS优化核心1——始终为图片和视频设置尺寸。使用width/height属性或CSS aspect-ratio，让浏览器在资源加载前预留正确空间。next/image自动根据src的尺寸设置aspect-ratio，避免布局偏移。对于响应式图片，确保srcset中每个尺寸都有对应的width/height。（来源：https://web.dev/articles/optimize-cls）

知识点13：CLS优化核心2——为广告/嵌入/动态内容预留空间。不要在页面加载后动态插入内容（除非是用户交互触发的）。广告位应该有固定尺寸容器（即使广告未加载也保留空间）。使用min-height或skeleton骨架屏为异步加载内容预留空间。避免在已有内容上方插入横幅（这会导致最大的布局偏移）。（来源：https://web.dev/articles/optimize-cls）

知识点14：CLS优化核心3——字体加载优化。Web字体加载会导致FOIT（不可见文字闪烁）或FOUT（无样式文字闪烁），文字尺寸变化会导致布局偏移。优化方法：使用next/font（自动内联CSS、预加载字体、减少布局偏移）、font-display: swap（避免FOIT，文字先用系统字体显示再切换）、size-adjust描述符调整字体度量减少swap时的布局偏移、避免在页面加载后注入字体。（来源：https://web.dev/articles/optimize-cls）

知识点15：Core Web Vitals监控与测量——使用Chrome User Experience Report（CrUX）获取真实用户数据（BigQuery/PageSpeed Insights）、PageSpeed Insights（实验室Lighthouse + 真实CrUX数据）、Google Search Console的Core Web Vitals报告（按URL分组显示问题）、Lighthouse CI（自动化CI检查，AIToolCrux已有lighthouse-ci.yml）、web-vitals.js库（在生产环境中上报指标到GA4）。注意：实验室数据（Lighthouse）和真实用户数据（CrUX）可能差异很大，以真实用户p75为准，实验室数据用于诊断。（来源：https://web.dev/articles/vitals）

落地计划：
- 知识点4+6（LCP图片priority+优化）→ P1-PERF-LCP-TOOLS-001：审计工具详情页LCP图片，确保next/image加priority属性（第83轮已做部分，需复查所有工具页）
- 知识点9（第三方脚本INP优化）→ P1-PERF-PARTYTOWN-001：评估AdSense/GA4/Umami/BaiduAnalytics是否用Partytown迁移到Web Worker（当前已用lazyOnload，需评估是否足够）
- 知识点12+13（CLS图片尺寸+广告预留）→ P1-PERF-CLS-AUDIT-001：审计全站CLS，检查所有图片是否有aspect-ratio，广告位是否预留空间
- 知识点15（监控测量）→ P1-QA-CWV-MONITOR-001：将web-vitals.js指标上报到GA4，建立真实用户CWV监控看板


[2026-09-25] Next.js App Router高级渲染策略：generateStaticParams+动态渲染+ISR+缓存头（来源：Next.js官方文档+Vercel官方文档）

知识点1：generateStaticParams在构建时静态生成动态路由，而非请求时按需生成。返回参数数组，每个元素对应一个预渲染页面。与ISR结合时，未在generateStaticParams中列出的URL首次请求时按需生成并缓存（stale-while-revalidate）。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-static-params）

知识点2：静态渲染vs动态渲染——静态渲染在构建时或revalidation后后台渲染，结果缓存并跨请求复用；动态渲染在每个请求时渲染。当路由使用cookies()、headers()、searchParams等request-time APIs时，Next.js自动将整个路由切换为动态渲染。（来源：https://nextjs.org/docs/app/guides/caching）

知识点3：动态渲染触发API清单——cookies()、headers()、searchParams（page props）、draftMode()、connection()。使用其中任何一个都会使整个路由变为动态渲染，HTTP响应返回cache-control: private, no-cache, no-store, max-age=0, must-revalidate，Vercel CDN不缓存。（来源：https://nextjs.org/docs/app/getting-started/caching）

知识点4：force-static vs force-dynamic——export const dynamic = 'force-static'强制路由预渲染（此时cookies()/headers()返回空值，searchParams不可用）；export const dynamic = 'force-dynamic'强制路由在每个请求时动态渲染且不缓存。默认auto由Next.js根据使用的API自动判断。（来源：https://nextjs.org/docs/app/guides/caching）

知识点5：fetch缓存选项——cache: 'force-cache'（默认，缓存数据）、cache: 'no-store'（每次请求获取不缓存）、next: { revalidate: number }（设置缓存生命周期秒数）、next: { revalidate: false }（无限期缓存）、next: { revalidate: 0 }（不缓存）。no-cache在Next.js中等同于no-store。（来源：https://nextjs.org/docs/app/api-reference/functions/fetch）

知识点6：ISR（增量静态再生）——结合generateStaticParams + revalidate实现。构建时预渲染列出的页面，revalidate时间过期后首次请求触发后台重新渲染，期间继续提供旧内容（stale-while-revalidate语义）。新内容就绪后替换缓存。（来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration）

知识点7：ISR核心优势——无需重建全站即可更新静态内容、减少服务器负载（大部分请求服务预渲染页）、自动添加正确cache-control头、处理大量内容页时避免next build时间过长（533工具页全量SSG构建需2-5分钟）。（来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration）

知识点8：按需revalidation——revalidateTag(tag)和revalidatePath(path)显式失效缓存。下一次请求触发重新渲染。适用于CMS内容更新后通过webhook立即刷新页面。revalidatePath只失效缓存条目，再生发生在下一次请求（非立即）。（来源：https://nextjs.org/docs/app/guides/how-revalidation-works）

知识点9：Next.js四层缓存架构——①Request Memoization（单次React渲染内去重相同fetch）、②Data Cache（跨请求持久化fetch结果，存于磁盘）、③Full Route Cache（静态渲染的HTML/RSC payload，构建时生成）、④Router Cache（客户端导航缓存，内存中，30秒/5分钟）。（来源：https://nextjs.org/docs/app/getting-started/caching）

知识点10：Vercel CDN缓存头——静态/ISR页面返回cache-control: public, max-age=0, s-maxage=31536000, stale-while-revalidate；动态页面返回private, no-cache, no-store, max-age=0, must-revalidate。x-vercel-cache响应头显示HIT/MISS/PRERENDER/BYPASS/STALE/REVALIDATED。（来源：https://nextjs.org/docs/app/guides/cdn-caching）

知识点11：分类页no-store根因诊断——第95轮发现/blog/category/*返回x-vercel-cache=MISS + no-store。根因可能是category页面使用了cookies()、headers()或searchParams。诊断方法：grep搜索这些API调用；或在page.tsx顶部临时加export const dynamic = 'force-static'测试是否变为HIT；检查是否有未缓存的fetch（cache: 'no-store'）。（来源：https://nextjs.org/docs/app/guides/caching + 第95轮缓存审计发现）

知识点12：generateStaticParams性能优化策略——对于533个工具页，返回全部533个slug会导致构建时间2-5分钟。优化方案：结合ISR只预渲染高流量页面（如前100个按流量排序），其余页面设为动态按需生成+缓存（首次请求慢但后续HIT）。或用export const dynamicParams = true（默认）允许未列出的参数动态渲染。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-static-params）

知识点13：params是Promise（Next.js 15+变更）——在Next.js 15中，page组件的params和searchParams是Promise，需要await解构。Next.js 14中params是同步对象。AIToolCrux用14.2.5，params是同步的，升级到15时需重构所有动态路由页面。（来源：https://nextjs.org/docs/app/guides/upgrading/version-15）

知识点14：数据缓存与路由缓存的关系——fetch的next.revalidate控制Data Cache生命周期；路由级export const revalidate控制Full Route Cache生命周期。两者取较小值。如果fetch用no-store但路由设revalidate=3600，路由仍会动态渲染（因为uncached data使路由变为动态）。要让路由静态，所有fetch必须可缓存。（来源：https://nextjs.org/docs/app/getting-started/caching）

知识点15：缓存调试方法——①用x-vercel-cache响应头判断CDN缓存状态（HIT=缓存命中，MISS=未命中，PRERENDER=首次预渲染）；②用next build输出中的符号判断路由模式：○=静态，λ=动态，ƒ=ISR；③用Next.js DevTools的Cache标签查看Data Cache命中；④在fetch后加console.log判断是否每次请求都执行。（来源：https://nextjs.org/docs/app/guides/cdn-caching + https://nextjs.org/docs/app/getting-started/caching）

落地计划：
- 知识点3+11（动态渲染触发+no-store诊断）→ P1-PERF-CATEGORY-NOSTORE-001：诊断并修复/blog/category/[slug]分类页no-store问题，grep搜索cookies()/headers()/searchParams，移除动态API或用force-static
- 知识点6+7+12（ISR+generateStaticParams优化）→ P1-PERF-ISR-TOOLS-001：将533工具页从全量SSG改为ISR（预渲染前100高流量+其余按需生成缓存），减少构建时间从5分钟到1分钟
- 知识点10+15（缓存头+调试）→ P1-QA-CACHE-MONITOR-001：添加CI步骤检查关键页面x-vercel-cache状态，防止回归引入动态渲染
- 知识点8（按需revalidation）→ P2-PERF-ON-DEMAND-REVALIDATE-001：添加API route接收内容更新webhook，调用revalidateTag刷新工具/文章页缓存


[2026-09-25] GitHub Actions高级自动化：自定义Action开发+缓存策略+Secrets管理+并发控制（来源：GitHub官方文档）

知识点1：三种自定义Action类型——Docker container（环境一致性好但启动慢）、JavaScript（用@actions/core等toolkit，启动快需打包）、Composite（纯YAML组合步骤，最简单零依赖）。选择：简单步骤封装用Composite，需复杂逻辑用JavaScript，需特定环境用Docker。（来源：https://docs.github.com/en/actions/creating-actions/about-custom-actions）

知识点2：Action元数据文件必须命名为action.yml（首选）或action.yaml，包含name、description、inputs（含description/default/required）、outputs、runs（含using指定类型）。缺少required input会导致workflow失败。（来源：https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions）

知识点3：Composite Action的runs.using必须为"composite"，runs.steps可包含run和uses步骤，支持shell指定。可定义inputs/outputs在步骤间传递数据。适合封装"安装依赖+构建+测试"等重复流程。（来源：https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action）

知识点4：JavaScript Action必须使用@actions/toolkit包：@actions/core（getInput/setOutput/setFailed）、@actions/github（预认证Octokit客户端）、@actions/exec（执行命令）。必须提交node_modules或用@vercel/ncc打包为单文件，否则运行时找不到依赖。（来源：https://docs.github.com/en/actions/tutorials/create-actions/create-a-javascript-action）

知识点5：Docker Action的runs.using为"docker"，runs.image可指定Dockerfile路径（如'Dockerfile'）或公共镜像（如'docker://alpine:3'）。Dockerfile中ENTRYPOINT执行入口脚本。优点是环境完全一致，缺点是每次运行需构建/拉取镜像，启动慢10-30秒。（来源：https://docs.github.com/en/actions/creating-actions/about-custom-actions）

知识点6：actions/cache缓存机制——key唯一标识缓存（可用hashFiles('**/package-lock.json')生成），path指定缓存路径（如~/.npm）。完全匹配key为cache hit直接恢复；不匹配时按restore-keys前缀顺序匹配；job成功结束时自动保存新缓存。（来源：https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching）

知识点7：setup-node的cache参数可自动缓存npm/yarn/pnpm依赖（cache: 'npm'），无需手动配置actions/cache。缓存键自动基于lockfile hash和操作系统，比手动配置更可靠。pnpm还需指定cache-dependency-path。（来源：https://docs.github.com/en/actions/how-tos/writing-workflows/caching-dependencies-to-speed-up-workflows）

知识点8：缓存安全铁律——不要将secrets、tokens、credentials写入缓存路径。只从受信任的触发源（push到默认分支、release）保存缓存，防止恶意PR通过workflow注入污染缓存。缓存大小限制10GB/仓库，超出后LRU淘汰。（来源：https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching）

知识点9：cache-mode控制缓存访问权限——read（只读，适合fork PR）、write（读写，默认）、write-only（只写不读）、none（完全禁用）。可在workflow级或job级设置，job级覆盖workflow级。fork仓库的pull_request默认只读缓存。（来源：https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching）

知识点10：Secrets三级作用域——Repository secrets（单仓库可用）、Organization secrets（多仓库共享，可配"所有仓库"/"仅私有"/"指定仓库"访问策略）、Environment secrets（绑定deployment environment，可配环境审批规则）。优先级：Environment > Repository > Organization。（来源：https://docs.github.com/en/actions/how-tos/write-workflows/use-secrets）

知识点11：Secrets在workflow日志中自动脱敏（替换为***）。非secret的敏感值用::add-mask::VALUE工作流命令手动脱敏。Secrets不会自动传递给fork仓库的pull_request事件，需用pull_request_target或手动配置。（来源：https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions）

知识点12：concurrency并发控制——同一concurrency group同时最多1个running+1个pending。新pending进来时旧pending被替换。加cancel-in-progress: true会取消正在运行的旧任务，适合CI避免浪费分钟数。（来源：https://docs.github.com/en/actions/writing-workflows/control-the-concurrency-of-workflows-and-jobs）

知识点13：concurrency group表达式可用github.ref、github.workflow、github.event_name等上下文。典型CI配置：group: ci-${{ github.ref }} + cancel-in-progress: true，同一分支新push自动取消旧CI运行。部署工作流不应加cancel-in-progress（避免中断部署）。（来源：https://docs.github.com/en/actions/examples/using-concurrency-expressions-and-a-test-matrix）

知识点14：自定义Action版本管理——用Git tag发布（v1、v2、v1.0.0），消费者用uses: owner/action@v1。主版本tag（v1）应始终移动指向最新v1.x，通过git tag -fa v1 && git push --tags -f实现。破坏性变更升主版本号。（来源：https://docs.github.com/en/actions/creating-actions/about-custom-actions）

知识点15：私有仓库内Action引用——本地Action用uses: ./.github/actions/action-name引用，无需发布。同一组织内私有Action可用uses: org/repo/.github/actions/name@main（需在调用方workflow用actions/checkout with token checkout该仓库）。发布到Marketplace需action.yml+README+LICENSE+图标。（来源：https://docs.github.com/en/actions/creating-actions/about-custom-actions）

落地计划：
- 知识点3+6（Composite+setup-node cache）→ P1-CI-COMPOSITE-SETUP-001：创建Composite Action封装"checkout+setup-node(cache npm)+npm ci"，所有workflow复用
- 知识点12+13（concurrency）→ P1-CI-CONCURRENCY-001：为bundle-size和lighthouse CI添加concurrency group+cancel-in-progress，避免重复运行浪费
- 知识点8+9（缓存安全+cache-mode）→ P1-CI-CACHE-SECURITY-001：审计所有workflow缓存配置，确保fork PR只读缓存，不缓存含secrets的路径
- 知识点10+11（Secrets分级+脱敏）→ P1-CI-SECRETS-AUDIT-001：审计GitHub PAT等secrets的作用域，将可共享的移到Organization级，验证日志脱敏
- 知识点4（JavaScript Action）→ P2-CI-CUSTOM-ACTION-001：开发自定义Composite Action封装"部署后线上验证"流程（等待+3页面HTTP检查）


[2026-09-25] 结构化数据最佳实践（Schema.org + Google Rich Results）（来源：Google Search Central官方文档）

知识点1：JSON-LD是Google推荐的结构化数据格式——放在<script type="application/ld+json">标签中，优于Microdata和RDFa。JSON-LD与页面内容解耦，不易因HTML重构而损坏。（来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies）

知识点2：必须属性（required）缺失会直接取消富媒体搜索结果资格；推荐属性（recommended）提供越多，搜索结果展示质量越高。但"少而完整准确"优于"多而残缺不准"。（来源：https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data）

知识点3：不要用noindex或robots.txt阻止Googlebot访问含结构化数据的页面——如果Googlebot无法抓取页面，结构化数据也无法被处理。（来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies）

知识点4：SoftwareApplication类型必须属性：name和offers.price（免费应用设offers.price为"0"）。推荐属性：applicationCategory、operatingSystem、aggregateRating、review、downloadUrl。AIToolCrux的工具详情页应使用此类型。（来源：https://developers.google.com/search/docs/appearance/structured-data/software-app）

知识点5：Article/BlogPosting类型推荐属性：author（Person或Organization，需含name）、datePublished（ISO 8601格式）、dateModified、headline、image（至少1个，推荐1200x675）、publisher（含logo）。（来源：https://developers.google.com/search/docs/appearance/structured-data/article）

知识点6：Review snippet的author必须是有效人名或组织名（不能是"50% off until Saturday"这类促销文案），字符数必须<100。AggregateRating必须基于真实用户评价，虚假评价可能导致人工处理。（来源：https://developers.google.com/search/docs/appearance/structured-data/review-snippet）

知识点7：BreadcrumbList必须包含至少2个ListItem，每个item必须有position（从1开始递增）、name（页面标题）、item（规范URL）。Google建议面包屑反映典型用户导航路径而非简单镜像URL结构。（来源：https://developers.google.com/search/docs/appearance/structured-data/breadcrumb）

知识点8：FAQPage必须属性：每个Question有name（问题全文）和acceptedAnswer（答案文本）。FAQ内容必须在页面上可见，不能只在结构化数据中存在。每个问题只能有一个acceptedAnswer。（来源：https://developers.google.com/search/docs/appearance/structured-data/faqpage）

知识点9：Organization结构化数据放在首页，帮助Google消歧组织身份。推荐属性：url、logo（必须是图片URL，112x112以上）、sameAs（社交媒体和Wikipedia链接）、iso6523/naics（行业编码）。（来源：https://developers.google.com/search/docs/appearance/structured-data/organization）

知识点10：结构化数据必须与页面可见内容匹配——标记不可见内容、与页面无关内容或误导性内容违反质量指南，可能导致Google手动处罚（manual action）。（来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies）

知识点11：不要在结构化数据中使用虚假或误导性信息（如假评价、假价格、假可用性）。Google会在展示前尝试验证商家数据，发现不一致会拒绝展示。（来源：https://developers.google.com/search/docs/appearance/structured-data/merchant-listing）

知识点12：用Rich Results Test工具验证结构化数据技术合规性（能捕获大多数技术错误）；用Google Search Console的URL Inspection Tool检查Google实际是否能看到并解析页面上的结构化数据。（来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies）

知识点13：同一页面可以包含多种类型的结构化数据（如Article + BreadcrumbList + FAQPage + Organization），用多个独立的JSON-LD script块，或用@graph数组合并。每种类型独立验证。（来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies）

知识点14：data-vocabulary.org标记已不再适用于Google富媒体搜索结果（已停用），所有旧标记必须迁移到schema.org词汇表。（来源：https://developers.google.com/search/docs/appearance/structured-data/breadcrumb）

知识点15：Google Search Central文档是Google搜索行为的权威来源——schema.org上有更多属性和类型，但不一定被Google搜索支持。实现时应以Google文档列出的required/recommended属性为准，而非schema.org的完整属性列表。（来源：https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data）

落地计划：
- 知识点4（SoftwareApplication）→ P1-SEO-SCHEMA-SOFTWAREAPP-001：为/tools/[slug]工具详情页添加SoftwareApplication结构化数据（name+offers.price+applicationCategory+aggregateRating）
- 知识点7（BreadcrumbList）→ P1-SEO-SCHEMA-BREADCRUMB-001：为所有文章页/工具页/分类页添加BreadcrumbList结构化数据（至少2级）
- 知识点8（FAQPage）→ P1-SEO-SCHEMA-FAQ-001：为有FAQ章节的文章页添加FAQPage结构化数据，确保FAQ内容在页面可见
- 知识点5（Article完整属性）→ P1-SEO-SCHEMA-ARTICLE-001：补全文章页Article结构化数据的dateModified、image、publisher.logo属性
- 知识点12（Rich Results Test）→ P1-QA-SCHEMA-VALIDATE-001：用Rich Results Test API批量验证全站关键页面结构化数据合规性


[2026-09-24] TypeScript严格模式与类型安全最佳实践（来源：TypeScript官方Handbook + TSConfig Reference + Next.js官方Docs）

知识点1：strict标志一键开启7项严格检查——"strict": true同时启用noImplicitAny、strictNullChecks、strictFunctionTypes、strictBindCallApply、strictPropertyInitialization、alwaysStrict、useUnknownInCatchVariables。新项目必须开启，老项目可逐项迁移。（来源：https://www.typescriptlang.org/docs/handbook/2/basic-types.html）

知识点2：noImplicitAny——禁止隐式any类型。函数参数、返回值、变量如果无法推断类型且未显式标注，编译报错。这是严格模式中最重要的单项检查，能捕获大量"以为有类型实际是any"的bug。（来源：https://www.typescriptlang.org/docs/handbook/2/basic-types.html）

知识点3：strictNullChecks——null和undefined不再是所有类型的子类型。声明string类型的变量不能赋值null，必须用string | null显式标注。访问可能为null的属性前必须做null检查。这是减少运行时"Cannot read property of undefined"错误的最有效手段。（来源：https://www.typescriptlang.org/docs/handbook/2/everyday-types.html）

知识点4：noUncheckedIndexedAccess——数组和对象索引访问结果自动加undefined。arr[0]的类型是T | undefined而非T，强制检查越界访问。对处理动态数据（如JSON解析后的数组）特别重要。注意：此标志不在strict中，需单独开启。（来源：https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-1.html）

知识点5：exactOptionalPropertyTypes——可选属性不能显式赋值undefined。{ name?: string }类型的属性要么省略，要么赋值string，不能赋值undefined。这区分了"属性不存在"和"属性存在但值为undefined"两种语义，对序列化和API契约很重要。（来源：https://www.typescriptlang.org/tsconfig/）

知识点6：noImplicitReturns——函数所有代码路径必须有返回值。if/else分支中如果一个分支return了值，另一个分支也必须return，防止遗漏return导致函数返回undefined。（来源：https://www.typescriptlang.org/docs/handbook/compiler-options.html）

知识点7：noFallthroughCasesInSwitch——switch语句中case不能穿透到下一个case（除非case体为空或有fallthrough注释）。防止遗漏break导致的逻辑错误。（来源：https://www.typescriptlang.org/docs/handbook/compiler-options.html）

知识点8：noUnusedLocals + noUnusedParameters——禁止未使用的局部变量和函数参数。保持代码整洁，防止重构后遗留死代码。参数可用_前缀标记为有意未使用。（来源：https://www.typescriptlang.org/tsconfig/）

知识点9：判别联合（Discriminated Unions）——用共同的字面量类型字段（如kind、state、status）区分联合类型成员。TypeScript通过检查该字段自动窄化类型，无需类型断言。典型模式：{ status: "loading" } | { status: "success", data: T } | { status: "error", message: string }。（来源：https://www.typescriptlang.org/docs/handbook/2/narrowing.html）

知识点10：never类型穷尽检查——在switch的default分支中将值赋给never类型变量（const _exhaustive: never = value），如果联合类型新增了成员但未处理对应case，编译时报错。这是确保所有状态都被处理的编译时安全网。（来源：https://www.typescriptlang.org/docs/handbook/2/narrowing.html）

知识点11：类型窄化（Type Narrowing）——多种方式窄化联合类型：typeof（原始类型）、instanceof（类实例）、in运算符（属性存在性）、真值检查（!!）、判别联合、用户自定义类型守卫（is关键字）。窄化后在分支内可安全访问特定类型的属性。（来源：https://www.typescriptlang.org/docs/handbook/2/narrowing.html）

知识点12：Next.js App Router端到端类型安全——Server Components中fetch获取的数据无需序列化为JSON即可传递给Client Components，可直接传递Date、Map、Set、函数等复杂类型。这是App Router相对Pages Router的核心类型安全优势。（来源：https://nextjs.org/docs/app/api-reference/config/typescript）

知识点13：Next.js Typed Routes——编译时验证<Link href>和router.push()的路径有效性，自动生成基于文件结构的路由类型，防止死链接和拼写错误。Next.js 15.5起稳定，需在next.config中开启experimental.typedRoutes。（来源：https://nextjs.org/blog/next-15-5）

知识点14：PageProps/LayoutProps类型助手——Next.js 15+提供PageProps<'/blog/[slug]'>、LayoutProps<'/route'>、RouteContext<'/route'>类型助手，自动推断动态路由的params和searchParams类型，无需手动定义接口。（来源：https://nextjs.org/docs/15/app/api-reference/file-conventions/dynamic-routes）

知识点15：unknown替代any——useUnknownInCatchVariables使catch(e)中e默认为unknown而非any，强制在使用前做类型检查。函数返回值优先用unknown而非any，迫使消费方进行类型窄化。any是类型系统的"逃生舱"，应最小化使用并用eslint的no-explicit-any规则限制。（来源：https://www.typescriptlang.org/docs/handbook/2/functions.html）

落地计划：
- 知识点1+2+3 → P1-QA-TS-STRICT-AUDIT-001：审计当前tsconfig.json，确认strict已开启，扫描代码中剩余的any类型和隐式any，逐步消除
- 知识点4（noUncheckedIndexedAccess）→ P1-QA-TS-INDEX-SAFETY-001：评估开启noUncheckedIndexedAccess，重点修复tools.json/posts.json数据访问的越界风险
- 知识点9+10（判别联合+never穷尽检查）→ P1-QA-TS-DISCRIMINATED-001：将工具状态、加载状态等any/string类型重构为判别联合，添加never穷尽检查
- 知识点13（Typed Routes）→ P2-QA-TYPED-ROUTES-001：Next.js升级到15+后开启experimental.typedRoutes，编译时捕获无效链接
- 知识点15（unknown替代any）→ P1-QA-TS-NO-ANY-001：添加eslint-plugin-typescript-eslint的no-explicit-any规则，CI中阻断新增any类型


[2026-09-24] Vercel部署优化与构建性能完整指南（来源：Vercel官方Docs + Next.js官方Docs）

知识点1：Vercel Build Cache机制——自动缓存node_modules和框架特定构建产物，每个缓存最多1GB、保留1个月。缓存key由Team/Project/Framework Preset/Root Directory/lockfile hash组合生成，lockfile不变时安装可从数分钟缩短到数秒。（来源：https://vercel.com/docs/deployments/troubleshoot-a-build）

知识点2：VERCEL_FORCE_NO_BUILD_CACHE=1环境变量可跳过构建缓存恢复，用于排查缓存导致的构建问题。设置后构建开始时不恢复缓存，但成功构建后仍会上传新缓存。（来源：https://vercel.com/docs/deployments/troubleshoot-a-build）

知识点3：Framework Preset必须正确设置——Vercel根据Framework Preset决定缓存哪些文件（Next.js缓存.next/cache，其他框架缓存不同路径）。错误的Preset会导致缓存无法命中，构建时间显著增加。（来源：https://vercel.com/docs/deployments/troubleshoot-a-build）

知识点4：lockfile（package-lock.json/pnpm-lock.yaml/yarn.lock）必须提交到git——Vercel根据lockfile检测包管理器并确保依赖安装一致。没有lockfile时每次安装都重新解析依赖，无法利用缓存。（来源：https://vercel.com/docs/fundamentals/builds）

知识点5：Next.js的.next/cache在Vercel上自动配置——Vercel自动缓存Next.js构建缓存（包括webpack模块缓存和静态生成缓存），无需手动配置CI缓存步骤。这是Vercel部署Next.js比其他平台快的核心原因之一。（来源：https://nextjs.org/docs/pages/building-your-application/deploying/ci-build-caching）

知识点6：generateStaticParams控制构建时预渲染哪些动态路由——返回空数组[]可完全跳过预渲染，所有页面按需生成，构建时间极短但首次访问较慢。对于500+页面的大站，可只预渲染高流量页面，其余用ISR按需生成。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-static-params）

知识点7：dynamicParams配置控制未预渲染路径的行为——设为false时未在generateStaticParams中列出的路径返回404；设为true（默认）时按需渲染并缓存。结合ISR可实现"构建快+首屏不慢"的平衡。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config）

知识点8：ISR（Incremental Static Regeneration）可在不重建全站的情况下更新静态内容——页面在后台重新生成，旧版本继续服务直到新版本就绪。ISR缓存持久31天或直到revalidate触发，适合内容频繁更新的大站。（来源：https://vercel.com/docs/incremental-static-regeneration）

知识点9：On-demand revalidation通过API调用触发特定页面重新生成——使用revalidateTag()或revalidatePath()可精确更新单个页面，无需等待revalidate周期。适合CMS内容更新后即时刷新页面。（来源：https://nextjs.org/docs/app/api-reference/functions/revalidatePath）

知识点10：staticPageGenerationTimeout默认60秒——如果60秒内没有新页面完成静态生成，Next.js会重试3次，第4次失败则构建失败。大站点（500+页面）应在next.config.js中设置staticPageGenerationTimeout: 120或更高。（来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/staticPageGenerationTimeout）

知识点11：Turbopack FileSystem Cache可显著加速后续构建——Turbopack将编译产物存储在.next/cache，下次构建时直接复用。Next.js 16.1起dev模式默认启用，build模式需配置turbopackFileSystemCache。（来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopackFileSystemCache）

知识点12：experimental.webpackMemoryOptimizations（Next.js 15+）可降低构建内存峰值——通过改变webpack行为减少最大内存使用，但可能略微增加编译时间。适合Vercel构建时遇到内存限制（OOM）的项目。（来源：https://nextjs.org/docs/app/guides/memory-usage）

知识点13：Vercel构建机器规格影响构建速度——Standard（1 vCPU）/Enhanced（2 vCPU）/Turbo（4 vCPU）/Elastic（按需扩展）。大站点全量SSG构建建议升级到Enhanced或Turbo，构建时间可减少50%+。（来源：https://vercel.com/kb/guide/how-do-i-reduce-my-build-time-with-next-js-on-vercel）

知识点14：Cache-Control头策略分层——静态资源（_next/static/*）用immutable长期缓存；服务端渲染页用s-maxage=86400（CDN缓存1天）；半静态内容（博客/产品页）用max-age=120, s-maxage=86400（浏览器2分钟+CDN 1天）。（来源：https://vercel.com/docs/caching/cache-control-headers）

知识点15：Vercel CDN对content-addressed不可变静态资源跨部署复用——Next.js的_next/static/chunks/*文件带内容hash，Vercel自动跨部署复用这些文件，减少17%的CDN回源请求，提升缓存命中率。零配置生效。（来源：https://vercel.com/changelog/optimized-cdn-caching-and-deploying-of-immutable-static-assets）

落地计划：
- 知识点6+7（generateStaticParams优化）→ 下次迭代P1-PERF-BUILD-SPEED-001：评估将533个工具页从全量SSG改为"只预渲染Top 50 + 其余ISR按需"，构建时间预计从3-5分钟降到1分钟内
- 知识点10（staticPageGenerationTimeout）→ 下次迭代P1-PERF-BUILD-MEMORY-001：在next.config.mjs中添加staticPageGenerationTimeout: 120，防止大站点构建超时
- 知识点12（webpackMemoryOptimizations）→ 下次迭代P1-PERF-BUILD-MEMORY-001：评估添加experimental.webpackMemoryOptimizations降低Vercel构建内存峰值
- 知识点14（Cache-Control策略）→ 下次迭代P1-PERF-CACHE-AUDIT-001：审计当前缓存头，确保半静态页面使用max-age=120+s-maxage=86400
- 知识点13（构建机器升级）→ 下次迭代GROWTH-INFRA-001：评估升级Vercel构建机器到Enhanced（2 vCPU），投入产出比分析


[2026-09-24] 高星GitHub开源工具深度解析：SEO审计、性能监控与自动化测试（15知识点）

知识点1：Lighthouse CI (@lhci/cli) 是Google官方CI性能回归工具，npm月下载~200万，v0.15.x使用Lighthouse 12.6。核心能力：每个PR生成Lighthouse报告、防止a11y/SEO/性能回归、跟踪指标趋势、设置performance budget、多次运行减少方差、对比两个版本。CI集成两种方式：直接调用@lhci/cli（最大控制）或用treosh/lighthouse-ci-action（封装boilerplate，自动上传artifact+PR status check）。来源：https://googlechrome.github.io/lighthouse-ci/docs/getting-started.html + https://unlighthouse.dev/learn-lighthouse/lighthouse-ci

知识点2：Lighthouse CI assertMatrix 支持按URL模式设置不同断言阈值。示例：所有页面FCP>2s警告，/app开头的HTTPS页面TTI>5s警告。配置文件.lighthouserc.json中assert.preset可以设为lighthouse:recommended，还可单独断言CLS/TBT/resource-summary。项目已配置numberOfRuns=3减少方差。来源：https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md + 项目.lighthouserc.json

知识点3：LHCI Server 是可选的历史数据存储服务，保存历次Lighthouse数据、展示趋势dashboard、提供build对比UI。可部署在自有服务器，通过防火墙限制内网访问，CI机器需放行。适合长期跟踪性能趋势，temporary-public-storage适合快速开始但数据7天后过期。来源：https://googlechrome.github.io/lighthouse-ci/docs/server.html

知识点4：Unlighthouse 是全站Lighthouse扫描CLI（GitHub harlan-zw/unlighthouse，v0.12.2），一条命令扫描整个站点。核心能力：自动发现URL（robots.txt/sitemap.xml/内链）、多Chrome实例并行扫描、智能采样（大站按模板采样代表性页面）、统一报告UI。大站点优化：samples=1减少每页运行次数、throttling disabled加速、--site指定域名。来源：https://unlighthouse.dev/ + https://unlighthouse.dev/guide/recipes/large-sites

知识点5：Unlighthouse CI模式 (unlighthouse-ci) 可在pipeline中运行全站扫描，score低于budget时CI构建失败。与Lighthouse CI区别：LHCI针对指定URL列表，Unlighthouse自动爬取全站。适合SSG站点（如本项目533工具+105文章+37 subcategory）做全量性能审计。来源：https://unlighthouse.dev/integrations/ci

知识点6：Playwright (Microsoft开源，GitHub 60k+ stars) 是E2E测试框架，支持Chromium/Firefox/WebKit三引擎。核心特性：auto-waiting（元素可操作前自动等待，消除人工timeout导致的flaky test）、web-first assertions（自动重试直到条件满足或超时）、locator优先用getByRole/getByText/getByLabel而非CSS/XPath、tracing调试、并行执行。CI分片：--shard=1/3把20分钟套件拆成3台机器5分钟跑完，结果自动合并。来源：https://playwright.dev/docs/best-practices + https://playwright.io/playwright/nodejs/parallel-cross-browser

知识点7：Playwright + Lighthouse 集成可在E2E测试中同时运行性能审计。LambdaTest提供playwright lighthouse library，在page.evaluate中触发lighthouseReport action。也可用unlighthouse的Playwright集成指南在GitHub Actions中同时做E2E和Lighthouse。来源：https://unlighthouse.dev/learn-lighthouse/playwright/ci-cd + https://www.lambdatest.com/support/docs/playwright-lighthouse-library/

知识点8：axe-core (Deque Systems开源，GitHub dequelabs/axe-core，数十亿次下载) 是可访问性自动化测试引擎，覆盖WCAG 2.1/2.2和Section 508。版本一致性很重要：不同axe-core版本可能产生不同扫描结果，需在组件/开发者/团队间锁定同一版本。支持自定义规则（config/axe-ruleset.json或AXE_RULESET_PATH环境变量）。axe DevTools浏览器扩展也基于axe-core。来源：https://docs.deque.com/devtools-for-web/4/en/about-axe-devtools-apis + https://docs.deque.com/devtools-for-web/4/en/ar-custom-rules

知识点9：@axe-core/playwright 让axe-core直接集成到Playwright E2E测试中，在每个页面导航后自动运行可访问性检查。CI工作流：npx serve启动站点 → npx wait-on等待 → npx @axe-core/cli http://localhost:3000 --exit（有错误则退出码非0）。与pa11y可同时使用做双重检查。来源：https://github.com/github/awesome-copilot/blob/main/agents/accessibility.agent.md

知识点10：Pa11y / Pa11y CI 是可访问性CLI工具（GitHub pa11y/pa11y），支持双runner：axe（用axe-core引擎）和htmlcs（默认）。Pa11y CI专为CI设计，遍历URL列表或sitemap，error级别问题导致构建失败。配置文件.pa11yci：standard设为WCAG2AA（最常用），runners设为["axe"]，timeout 10000ms，viewport 1280x1024。来源：https://pa11y.org/ + https://www.npmjs.com/package/pa11y-ci

知识点11：sitespeed.io 是完整性能测试工具箱（GitHub sitespeedio/sitespeed.io），由Browsertime（底层浏览器计时）、Coach（性能建议）、PageXray（HAR分析）组成。支持Chrome/Firefox/Edge/Safari（桌面+Android+iOS有限），数据输出到Graphite/InfluxDB做长期监控。Docker运行避免依赖问题：docker run --shm-size=1g sitespeedio/sitespeed.io https://example.com -n 1。GitLab官方用它做性能监控。来源：https://www.sitespeed.io/documentation/sitespeed.io/ + https://www.sitespeed.io/documentation/sitespeed.io/web-performance-testing-in-practice/

知识点12：sitespeed.io scripting 支持模拟完整用户旅程而非仅测首页。脚本用async/await操作：commands.click、commands.type、commands.wait、commands.measure。可以测试登录后页面、搜索流程、购买漏斗等关键路径性能。脚本文件自动检测，不需要--multi开关。来源：https://www.sitespeed.io/documentation/sitespeed.io/scripting/examples/ + https://www.sitespeed.io/documentation/sitespeed.io/scripting/running-scripts/

知识点13：WebPageTest (WPT) 是性能测试黄金标准（GitHub catchpoint/WebPageTest，Catchpoint维护）。核心能力：全球测试节点、真实设备测试、视频录制+Visual Metrics计算Speed Index/Start Render、request waterfall详细分析、No-Code Experiments。REST API三步：提交测试→poll状态→获取结果。API Wrapper (webpagetest npm包) 封装了polling和pingback。GitHub Action可在代码变更时自动跑WPT。来源：https://www.webpagetest.org/tips + https://www.npmjs.com/package/webpagetest

知识点14：webpack-bundle-analyzer 生成交互式zoomable treemap可视化bundle组成，发现大依赖（lodash/moment/chart.js）、重复模块、未使用代码。Next.js项目可用ANALYZE=true npm run build触发。配合webpack performance配置做size budget：maxAssetSize 250KB（min后）、maxEntrypointSize 400KB、hints:'error'让构建失败而非仅警告。项目已用size-limit做CI门禁（4条预算规则），bundle-analyzer用于定位超预算原因。来源：https://www.npmjs.com/package/webpack-bundle-analyzer + https://webpack.js.org/guides/code-splitting/ + 项目.size-limit.json

知识点15：工具选型决策矩阵：①单页性能回归→Lighthouse CI（项目已有）；②全站性能扫描→Unlighthouse（适合本项目600+页面）；③E2E功能测试→Playwright；④可访问性自动化→axe-core+Pa11y CI双检查；⑤真实用户旅程性能→sitespeed.io scripting；⑥深度性能诊断→WebPageTest；⑦bundle体积控制→size-limit(门禁)+webpack-bundle-analyzer(定位)。本项目当前已有：Lighthouse CI、size-limit、dependency-review-action。缺失：Playwright E2E、axe-core可访问性、Unlighthouse全站扫描。来源：综合以上所有官方文档

落地计划：
- 知识点4+5（Unlighthouse全站扫描）→下次迭代任务P1-PERF-UNLIGHTHOUSE-001：在CI中添加Unlighthouse全站扫描workflow，对600+页面做性能审计，score<80的页面输出报告
- 知识点6+7（Playwright E2E+Lighthouse）→下次迭代任务P1-QA-PLAYWRIGHT-001：添加Playwright E2E测试覆盖首页/工具详情页/文章页/对比页关键路径，同时集成Lighthouse审计
- 知识点8+9+10（axe-core+Pa11y可访问性）→下次迭代任务P2-A11Y-AXE-001：添加@axe-core/cli到CI，对首页+3个模板页做可访问性检查，error级别问题阻断构建
- 知识点14（bundle-analyzer）→配合已有的size-limit，当CI bundle超预算时自动生成analyzer报告定位原因，任务P2-PERF-BUNDLE-DEBUG-001
- 知识点11+12（sitespeed.io用户旅程）→长期任务GROWTH-PERF-JOURNEY-001：用sitespeed.io scripting测试"首页→搜索工具→查看详情→对比"关键旅程性能


## [2026-09-24] Next.js Metadata API与Open Graph/Twitter Cards深度优化

**主题**：Config-based Metadata与generateMetadata、metadataBase、openGraph/twitter字段、OG图片尺寸标准、opengraph-image.tsx文件约定、ImageResponse动态生成、canonical/alternates/hreflang、robots metadata、title template、社交分享验证
**来源**：Next.js官方文档(Metadata optimization、generateMetadata API、opengraph-image/twitter-image文件约定、ImageResponse API、robots.txt、metadata-and-og-images入门、learn SEO metadata)、Vercel官方文档(OG Image Generation)、OG图片尺寸指南(ogimagen.com、opengraphgenerator.com、patrickstox.com)
**交叉验证**：Next.js generateMetadata docs + Metadata optimization docs确认两种metadata方式与parent扩展模式；Next.js opengraph-image docs + Vercel OG Image Generation确认ImageResponse用法与静态优化；ogimagen.com + patrickstox.com + opengraphgenerator.com确认1200x630通用标准与平台差异

### 知识点1：Metadata API两种方式（Config-based vs generateMetadata）
- **Config-based**：`export const metadata: Metadata = { title, description, ... }`，静态元数据，适合不依赖数据的页面
- **generateMetadata**：`export async function generateMetadata({ params, searchParams }, parent): Promise<Metadata>`，动态元数据，可fetch数据、访问params
- 只能在**Server Component**的layout或page中使用，Client Component不能直接导出metadata（需在父Server Component设置）
- 我们的项目：layout.tsx用config-based，blog/[slug]/page.tsx和tools/[slug]/page.tsx用generateMetadata
（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata ）

### 知识点2：metadataBase必须设置（绝对URL基础）
`metadataBase: new URL('https://www.aitoolcrux.com')`，所有相对路径的OG图片、canonical、alternates会自动拼接为绝对URL。**不设metadataBase时**，og:image等相对路径不会被转为绝对URL，社交平台（Facebook/X/LinkedIn）可能无法加载图片——这是常见的OG图不显示原因。我们的layout.tsx应确认已设置metadataBase。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata ）

### 知识点3：generateMetadata可访问parent元数据（扩展而非替换）
第二个参数`parent: ResolvingMetadata`，可`const previousImages = (await parent).openGraph?.images || []`获取父级metadata并扩展。关键模式：`openGraph: { images: ['/specific-page.jpg', ...previousImages] }`——子页面OG图在前，父级默认OG图作为fallback在后。不访问parent时，子页面的openGraph.images会**完全替换**父级（不是合并）。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata ）

### 知识点4：Open Graph metadata完整字段
openGraph对象包含：title、description、url（规范URL）、siteName（"AIToolCrux"）、images（数组，每项含url/width/height/alt/type）、locale（"en_US"）、type（"website"首页/"article"文章页/"profile"）。images必须是绝对URL（或设metadataBase后用相对路径）。文章页应设type:"article"并加publishedTime/modifiedTime/authors。（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata + https://nextjs.org/learn/seo/metadata ）

### 知识点5：Twitter Cards metadata与回退机制
twitter对象包含：card（"summary_large_image"最常用，大图卡片）、title、description、images、creator（@username）、site（@username）。**twitter:image优先于og:image**在X平台显示。不设twitter字段时X会回退使用og:标签（og:title/og:description/og:image）。summary_large_image的title最多70字符、description最多200字符（超出截断）。（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata + https://www.brandsnap.io/blog/social-media-preview-images-guide ）

### 知识点6：OG图片尺寸标准（跨平台兼容）
- **通用标准**：1200×630px（1.91:1），适用于Facebook/LinkedIn/Slack/Discord/iMessage
- **X(Twitter)**：summary_large_image推荐1200×600（2:1），接受1200×630但可能裁剪上下几像素
- **最小尺寸**：200×200（Facebook硬限制），小于600×315会渲染为小缩略图而非大图卡片
- **文件大小**：建议<1MB（WhatsApp需<300KB），Facebook上限8MB，X上限5MB
- **格式**：PNG或JPEG，WebP部分平台不支持（OG协议官方支持JPEG/PNG/GIF）
（来源：https://ogimagen.com/guides/og-image-sizes-2026 + https://patrickstox.com/technical-seo/on-page/meta-tags/social-images/ ）

### 知识点7：opengraph-image.tsx文件约定（自动生成路由）
在路由文件夹中放`opengraph-image.tsx`，Next.js自动生成`/route/opengraph-image`路由并在该页面metadata中自动引用（不需手动在openGraph.images中指定）。默认**静态优化**（构建时生成并缓存），使用Request-time API或未缓存数据时变为动态。可导出`size`（默认{width:1200,height:630}）、`contentType`（默认image/png）、`alt`。同一路由可同时有opengraph-image和twitter-image两个文件（分别生成不同尺寸）。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image ）

### 知识点8：ImageResponse用JSX+CSS生成PNG图片
`import { ImageResponse } from 'next/og'`，用React元素+内联style生成PNG。支持flexbox布局、自定义字体（需fetch或readFile加载ttf）、渐变、emoji、绝对URL的<img>。**不支持**：CSS Grid、外部CSS文件、相对路径图片、`position: fixed`。运行在Edge Runtime。我们的`app/og/[slug]/route.tsx`就是用ImageResponse手动生成OG图（Route Handler方式，比文件约定更灵活控制缓存）。（来源：https://nextjs.org/docs/app/api-reference/functions/image-response + https://vercel.com/docs/og-image-generation ）

### 知识点9：canonical URL与alternates（hreflang/feed）
`alternates: { canonical: '/path' }`生成`<link rel="canonical">`。**canonical是建议**（Google可选择不遵守），**robots是指令**（必须遵守）。alternates还支持：
- `languages`：hreflang多语言（{'en-US':'/en','zh-CN':'/zh'}）
- `media`：响应式canonical（移动端不同URL）
- `types`：RSS/JSON feed（{'application/rss+xml':'/feed.xml'}）
重复内容页面（分页、筛选参数、compare页）必须设canonical指向主页面，避免权重分散。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata + https://nextjs.org/learn/seo/metatags ）

### 知识点10：robots metadata与robots.txt双轨控制
- **页面级robots metadata**：`robots: { index: true, follow: true, googleBot: { 'max-image-preview': 'large', 'max-snippet': -1 } }`生成`<meta name="robots">`
- **站点级robots.txt**：`app/robots.ts`文件生成/robots.txt，可按user-agent设allow/disallow/crawlDelay
- noindex页面仍会被爬取但不索引；要完全阻止爬取用robots.txt Disallow
- `max-image-preview: 'large'`让Google搜索结果显示大图预览（对工具评测站很重要）
（来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots + https://nextjs.org/learn/seo/metatags ）

### 知识点11：metadata优先级与合并规则
- 子路由metadata**覆盖**父路由同名字段（title、description等标量字段）
- openGraph.images等数组字段默认是**替换**而非合并（需用parent手动扩展，见知识点3）
- 最接近页面的layout/page的metadata优先级最高
- 同一路由的page.tsx的metadata优先于同目录layout.tsx
- metadata对象浅合并：嵌套对象（如openGraph）也是浅合并（子页面设openGraph.title会保留父级openGraph.description？实际是整个openGraph对象替换，需验证）
（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata ）

### 知识点12：title template模式（自动拼接品牌名）
`title: { default: 'AIToolCrux - AI工具评测与对比', template: '%s | AIToolCrux' }`。子页面只需设`title: 'ChatGPT评测'`，自动渲染为"ChatGPT评测 | AIToolCrux"。不设template时子页面title完全替换父级。`absolute`字段可覆盖template：`title: { absolute: '不套模板的独立标题' }`。最佳实践：layout.tsx设template，所有子页面只设具体标题。（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata ）

### 知识点13：JSON-LD不是Metadata API字段（两者互补）
Metadata API**只负责meta/link标签**（title/description/og/twitter/canonical/robots），**不处理JSON-LD结构化数据**。JSON-LD（OrganizationSchema/ArticleSchema/Product/BreadcrumbList）需在页面组件中用`<script type="application/ld+json">`直接输出。我们的结构化数据组件是独立的，与Metadata API互补不重叠。常见错误：以为在metadata中设了openGraph就等于有了结构化数据——两者是不同的东西。（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata + 项目实际架构 ）

### 知识点14：大量动态OG图的构建性能考量
opengraph-image.tsx默认静态优化（构建时生成），但如果有大量动态页面（我们533工具+105文章=638个OG图），**构建时间会显著增加**（每个OG图需执行ImageResponse渲染）。优化策略：
- 用Route Handler（app/og/[slug]/route.tsx，我们当前做法）手动控制缓存头和生成时机
- 设`export const revalidate = 86400`（ISR，每天重新生成）
- 用Edge Runtime降低冷启动
- 对低流量页面可接受首次请求动态生成（不在构建时生成）
（来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image + https://vercel.com/docs/og-image-generation ）

### 知识点15：社交分享验证与OG缓存刷新
发布/更新后必须用官方验证工具检查OG标签：
- **Facebook Sharing Debugger**：developers.facebook.com/tools/debug（同时触发重新抓取）
- **LinkedIn Post Inspector**：linkedin.com/post-inspector
- **X**：旧Card Validator已停用，改用发布后查看或用第三方工具
- **关键**：社交平台有OG缓存，更新OG图片后**必须用验证工具触发重新抓取**，否则旧图会缓存数天甚至更久。每次修改og/[slug]/route.tsx后应验证至少一个工具页和一个文章页的OG图。
（来源：https://nextjs.org/learn/seo/metadata + https://ogimagen.com/guides/og-image-sizes-2026 ）

### 落地计划
- **P1-SEO-METADATA-AUDIT-001**（新增）：审计所有页面metadata完整性——确认layout.tsx已设metadataBase+title template，检查blog/[slug]和tools/[slug]的generateMetadata是否包含完整openGraph（type/article、images、siteName）、twitter（card:summary_large_image）、canonical。基于知识点1/2/4/5/12。
- **P2-SEO-OG-IMAGE-QUALITY-001**（新增）：优化og/[slug]/route.tsx生成的OG图片——确认1200×630尺寸、字体加载不失败、品牌一致性（logo/颜色）、文字不溢出。用Facebook Debugger验证至少3个页面。基于知识点6/8/14/15。
- **P2-SEO-CANONICAL-AUDIT-001**（新增）：审计分页页（/blog/page/2）、compare页、筛选页的canonical标签，确保重复内容指向主页面，避免权重分散。基于知识点9。
- 知识点10：所有工具页和文章页确认robots max-image-preview:large（Google大图预览）。


## [2026-09-24] Next.js Middleware与Edge Runtime：CSP Nonce、重定向、地理位置与边缘计算

**主题**：Next.js Middleware执行机制、matcher过滤、NextResponse四种响应、CSP nonce动态生成、Edge Runtime限制与适用场景、waitUntil异步任务、geo/cookies请求信息
**来源**：Next.js官方文档(Middleware routing、middleware.js API、NextResponse、CSP指南、redirecting指南、Edge vs Node.js runtimes、rewrites)、Vercel官方文档(Edge Runtime、Functions Limits、Runtime comparison、Edge Functions limitations、Routing Middleware API)
**交叉验证**：Next.js Middleware docs + Vercel Edge Runtime docs确认Middleware运行在Edge Runtime及其限制；Next.js CSP指南 + strict-csp-next GitHub项目确认nonce生成与动态渲染要求；Next.js redirecting指南 + rewrites docs确认rewrite vs redirect区别

### 知识点1：Middleware定位与执行时机
Middleware在请求完成前运行代码，基于传入请求修改响应——可rewrite（URL代理掩码）、redirect（重定向）、修改请求/响应headers、或直接响应。**每个项目只允许一个middleware文件**，放在项目根目录（与app/同级，即middleware.ts）。不能在子目录放多个middleware。执行顺序：请求→Middleware→路由/静态文件。（来源：https://nextjs.org/docs/app/building-your-application/routing/middleware ）

### 知识点2：matcher必须过滤路径（默认运行所有请求）
默认Middleware在**所有请求**上运行，包括静态文件（_next/static）、图片优化（_next/image）、favicon。必须用`export const config = { matcher: [...] }`过滤。推荐正则：`'/((?!_next/static|_next/image|favicon.ico|.*\\.png|.*\\.svg).*)'`排除静态资源。matcher支持单路径字符串、路径数组、正则。不设matcher会导致每次图片加载都执行Middleware逻辑，严重浪费执行次数。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/middleware ）

### 知识点3：NextResponse四种响应类型
- `NextResponse.next()`：继续请求（可修改headers）
- `NextResponse.rewrite(url)`：代理到不同URL，**浏览器地址栏不变**（URL掩码）
- `NextResponse.redirect(url)`：重定向到新URL，**浏览器地址栏变化**（307/308）
- `NextResponse.json(data)`：直接返回JSON响应
rewrite vs redirect核心区别：rewrite是内部代理（用户看到原URL），redirect是浏览器跳转。（来源：https://nextjs.org/docs/app/api-reference/functions/next-response ）

### 知识点4：CSP Nonce必须用Middleware生成（强制动态渲染）
带nonce的CSP必须在Middleware中生成：`const nonce = Buffer.from(crypto.randomUUID()).toString('base64')`，设置到`Content-Security-Policy`响应头和`x-nonce`请求头，Next.js会将nonce打到流式输出的script标签上。**每次页面浏览生成新nonce，必须使用动态渲染（不能SSG）**。nonced响应必须设`Cache-Control: no-store`防止nonce被缓存重放。我们当前是SSG+静态CSP，不能直接加nonce（会破坏SSG）。（来源：https://nextjs.org/docs/15/app/guides/content-security-policy ）

### 知识点5：strict-dynamic与nonce配合（CSP Level 3最佳实践）
`script-src 'self' 'nonce-xxx' 'strict-dynamic'`：strict-dynamic允许被nonce信任的脚本动态加载的子脚本，不需要逐个列第三方域名白名单。大幅减少维护AdSense/GA4/Umami等第三方脚本域名的负担。但注意：strict-dynamic会使'self'和域名白名单在支持CSP3的浏览器中被忽略（回退到nonce），不支持CSP3的旧浏览器回退到'self'+域名列表。（来源：https://nextjs.org/docs/15/app/guides/content-security-policy + https://www.vidhyasagarthakur.engineer/blog/security-hardening-nextjs-app-beyond-the-basics ）

### 知识点6：Middleware始终运行在Edge Runtime（不是Node.js）
Middleware**强制运行在Edge Runtime**（V8 isolates），不能切换到Node.js。不能使用Node.js API：fs、path、os、crypto模块（可用Web Crypto API替代）、mongoose、prisma（需edge adapter）。可用Web API：fetch、Request/Response、URL、TextEncoder/Decoder、crypto.subtle、Atomics、console。Buffer可用但有限（Edge Runtime提供了polyfill）。导入任何npm包前必须确认支持Edge Runtime。（来源：https://vercel.com/docs/functions/runtimes/edge + https://nextjs.org/docs/14/app/building-your-application/rendering/edge-and-nodejs-runtimes ）

### 知识点7：Edge Runtime硬限制
- 最大内存：128 MB
- 必须25秒内开始发送响应，之后可继续流式传输最多300秒
- 代码大小（gzip后）：Hobby 1MB / Pro 2MB / Enterprise 4MB（含所有import的包）
- 全局部署（默认所有区域），可指定region
- 无冷启动（V8 isolates启动<5ms，vs Serverless容器冷启动100-500ms）
- 并发自动扩展
（来源：https://vercel.com/docs/functions/limitations + https://vercel.com/docs/functions/runtimes/edge/edge-functions.rsc ）

### 知识点8：Edge vs Serverless选择决策
| 维度 | Edge Runtime | Serverless (Node.js) |
|------|-------------|---------------------|
| 冷启动 | 无（<5ms） | 有（100-500ms） |
| 区域 | 全局 | 单区域 |
| Node API | 有限子集 | 完整 |
| 大小 | 1-4MB | 50MB |
| 执行时间 | 25s开始响应 | 10s/60s/900s |
| 适用 | 轻量快速逻辑、geo重定向、CSP、A/B测试 | 重计算、数据库操作、Node依赖 |
决策：Middleware/CSP/geo重定向→Edge；API路由需数据库/重计算→Serverless。（来源：https://vercel.com/docs/concepts/limits/overview + https://examples.vercel.com/docs/infrastructure/runtime-comparison ）

### 知识点9：waitUntil执行不阻塞响应的异步任务
Middleware和Edge Functions中可用`event.waitUntil(promise)`执行不阻塞响应的异步任务（如日志上报、分析、缓存预热）。响应立即返回给用户，异步任务在后台继续执行直到完成或函数超时。Vercel Functions的`context.waitUntil()`同样可用。典型用途：Middleware中上报分析数据而不增加TTFB。（来源：https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package ）

### 知识点10：地理位置、cookie与请求信息
- `request.geo`：Vercel Edge Network提供city/country/region/latitude/longitude（仅Vercel部署，本地开发为空）
- `request.cookies`：RequestCookies API，get/set/delete cookie
- `request.headers`：所有请求头（含user-agent、accept-language）
- `request.nextUrl.pathname` / `searchParams`：解析URL路径和查询参数
典型用途：按国家重定向（`request.geo.country`）、A/B测试cookie分流、按accept-language设置语言。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/middleware ）

### 知识点11：Middleware不能直接返回HTML body
Next.js 14及之前的Middleware**不能直接返回HTML body或流式响应**，只能rewrite/redirect/修改headers/返回JSON。需要返回自定义HTML时，rewrite到一个Route Handler或页面。Next.js 15引入`proxy.js`（middleware的演进替代），支持更丰富的响应能力和直接返回body。我们用Next.js 14.2.5，受此限制。（来源：https://nextjs.org/docs/messages/middleware-upgrade-guide + https://nextjs.org/docs/app/api-reference/file-conventions/proxy ）

### 知识点12：静态CSP（next.config）vs 动态CSP（Middleware）选择
- **静态CSP**（我们当前做法）：在next.config.mjs的headers中设置，适用于SSG，无nonce，用域名白名单+哈希。优点：不破坏SSG缓存。缺点：第三方脚本变化时需手动更新白名单。
- **动态CSP（Middleware+nonce）**：每次请求生成nonce，更安全（防XSS注入），但强制动态渲染（失去SSG）。
- **内容站决策**：我们是SSG内容站（533工具+105文章），静态CSP是正确选择。nonce CSP适合需要严格安全的动态应用（如SaaS、用户登录系统）。（来源：https://nextjs.org/docs/15/app/guides/content-security-policy + 项目实际架构 ）

### 知识点13：重定向优先级与性能（config vs Middleware）
执行顺序：`next.config.mjs redirects`（静态配置）→ Middleware → `rewrites`。大量301重定向放在next.config.mjs比Middleware更高效——config redirects在Vercel边缘网络层直接处理（不需要执行函数代码），Middleware需要启动V8 isolate执行代码。我们next.config.mjs中有大量301重定向，应保持在config中，不要迁移到Middleware。（来源：https://nextjs.org/docs/app/guides/redirecting + https://nextjs.org/docs/15/app/api-reference/config/next-config-js/rewrites ）

### 知识点14：Middleware与next/link prefetch的交互
next/link的prefetch（视口内链接预获取）会触发Middleware执行。如果Middleware有重逻辑（geo查询、数据库调用、复杂计算），prefetch会导致大量不必要的执行（用户可能根本不点击）。优化：(a)matcher排除静态资源；(b)在Middleware中检查`request.headers.get('purpose') === 'prefetch'`或`x-middleware-prefetch`跳过重逻辑；(c)对工具列表页Link设prefetch={false}（我们第91轮已做）。（来源：https://nextjs.org/docs/app/building-your-application/routing/middleware + 第91轮prefetch优化经验 ）

### 知识点15：Edge Runtime不支持的常见库与替代
不能在Middleware/Edge中使用：fs、path、os、net、tls、crypto（Node模块，用Web Crypto替代）、mongoose、prisma（需`prisma@edge`或Data Proxy）、axios（可用但推荐原生fetch）、sharp（图片处理）、node-cron。可用：@vercel/edge、zod（验证）、jose（JWT）、ulid（ID生成）、nanoid、stripe（edge兼容模式）。导入包前查package.json的`exports`字段是否有`"edge"`条件。（来源：https://examples.vercel.com/docs/functions/edge-functions/limitations + https://vercel.com/docs/functions/runtimes/edge ）

### 落地计划
- **P1-SEC-MIDDLEWARE-CSP-001**（已存在待办）：评估CSP从next.config.mjs静态头迁移到Middleware+nonce的可行性。结论：我们是SSG内容站，nonce会强制动态渲染破坏SSG，**保持静态CSP**，改为优化当前CSP白名单（添加strict-dynamic评估）。基于知识点4/5/12。
- **P2-PERF-REDIRECT-AUDIT-001**（新增）：审计next.config.mjs中大量301重定向，确认是否有可合并/移除/已失效的重定向规则，保持在config层（不迁移到Middleware）。基于知识点13。
- **P2-PERF-MIDDLEWARE-GEO-001**（新增）：评估用Middleware geo实现按地区/语言轻量定制（如中文用户默认中文界面），注意matcher排除静态资源和prefetch。基于知识点2/10/14。
- 知识点6/7/8/15：未来添加任何Middleware功能前，必须确认依赖库支持Edge Runtime，代码大小<1MB（Hobby）。


## [2026-09-24] 前端真实用户监控(RUM)：web-vitals库、Next.js useReportWebVitals与Sentry性能/错误监控

**主题**：真实用户监控(RUM)体系——web-vitals库采集Core Web Vitals、Next.js内置hook、Sentry错误+性能+Replay一体化监控
**来源**：GoogleChrome/web-vitals(GitHub官方库)、web-vitals npm文档、Google Codelabs(Measure Core Web Vitals、web-vitals+GA+BigQuery)、Sentry官方文档(Next.js指南、Manual Setup、Source Maps、Automatic Instrumentation、Performance Monitoring、Browser Profiling、RUM)、Chrome for Developers
**交叉验证**：Google Codelabs + web-vitals GitHub README确认onLCP/onINP/onCLS API与reportAllChanges行为；Sentry官方文档多篇确认Next.js集成方式、source maps上传机制、tracesSampleRate策略

### 知识点1：web-vitals库定位与延迟加载原则
GoogleChrome/web-vitals是官方库（GitHub 7k+ stars），提供onLCP/onINP/onCLS/onFCP/onTTFB回调函数采集真实用户性能数据。**不需要早期加载**——库本身不影响性能测量准确性，应在其他用户影响代码之后延迟加载（dynamic import或defer script）。通过PerformanceObserver底层API采集，不手搓假指标。（来源：https://www.npmjs.com/package/web-vitals ）

### 知识点2：三大Core Web Vitals阈值（2024年3月INP正式替代FID）
LCP最大内容绘制：good≤2.5s，needs improvement 2.5-4s，poor>4s；INP交互到下次绘制：good≤200ms，needs improvement 200-500ms，poor>500ms；CLS累积布局偏移：good≤0.1，needs improvement 0.1-0.25，poor>0.25。INP于2024年3月12日正式成为Core Web Vitals，替代FID。INP衡量页面整个生命周期的最差交互延迟（非首次交互）。（来源：https://developers.google.com/codelabs/chrome-web-vitals-js ）

### 知识点3：reportAllChanges选项与默认行为
默认每个指标只在最终确定时报告一次（LCP在用户首次交互/页面隐藏时、INP在页面隐藏时、CLS在页面隐藏时）。`reportAllChanges:true`在指标每次变化时报告（CLS每次布局偏移增量、INP每次更差交互）。但**只在指标值变化时报告**——不增加CLS的布局偏移不会触发。Sentry默认开启此选项以保持内存中值刷新。多次报告同一指标时必须用metric.id去重。（来源：https://patch-diff.githubusercontent.com/GoogleChrome/web-vitals ）

### 知识点4：metric.id去重机制
每个metric对象有唯一`id`（如"v3-12345678"），reportAllChanges多次报告同一指标时用id去重。GA4集成中必须将metric.id作为event_label或自定义维度，否则同一页面多次报告会导致数据膨胀和P75计算错误。id在页面会话内唯一，跨页面不同。（来源：https://developers.google.com/codelabs/chrome-web-vitals-js + https://publishing-project.rivendellweb.net/web-vitals-and-google-analytics/ ）

### 知识点5：sendBeacon可靠上报RUM数据
上报RUM数据应使用`navigator.sendBeacon(url, data)`而非fetch——sendBeacon在页面卸载(unload/beforeunload/pagehide)时仍能可靠发送，且不阻塞导航、不影响下一页加载。数据量小时也可用`fetch(url, {method:'POST', body:data, keepalive:true})。sendBeacon有64KB数据上限，超出时需分批或改用fetch keepalive。（来源：https://developers.google.com/codelabs/chrome-web-vitals-js ）

### 知识点6：GA4集成标准模式
```
function sendToGA(metric) {
  gtag('event', metric.name, {
    event_category: 'Web Vitals',
    value: Math.round(metric.name === 'CLS' ? metric.delta * 1000 : metric.delta),
    event_label: metric.id,
    non_interaction: true
  });
}
onCLS(sendToGA); onINP(sendToGA); onLCP(sendToGA);
```
CLS乘1000取整因为GA事件值必须是整数（CLS是0.1这样的小数）。`non_interaction:true`避免Web Vitals事件影响跳出率计算。（来源：https://developers.google.com/codelabs/chrome-web-vitals-js ）

### 知识点7：INP五段式归因诊断
onINP回调的`metric.attribution`包含：interactionType(click/keydown/pointerdown)、interactionTime、eventTarget(目标元素选择器)、inputDelay(输入延迟-浏览器排队时间)、processingDuration(处理耗时-事件处理器+渲染)、presentationDelay(呈现延迟-浏览器绘制排队)。INP高=inputDelay高(主线程阻塞)或processingDuration高(JS执行重)或presentationDelay高(渲染复杂)。（来源：https://codelabs.developers.google.cn/measuring-inp ）

### 知识点8：LCP四阶段归因
onLCP的`metric.attribution`包含：element(LCP DOM元素)、url(资源URL如图片)、timeToFirstByte、resourceLoadDelay、resourceLoadDuration、elementRenderDelay。四阶段：TTFB(网络+服务端)→资源加载延迟(发现时机)→资源加载时长(下载)→元素渲染延迟(渲染排队)。LCP高的根因定位：TTFB高→服务端/CDN；resourceLoadDuration高→图片未优化；elementRenderDelay高→JS阻塞渲染。（来源：https://codelabs.developers.google.com/codelabs/web-vitals-google-analytics-bigquery ）

### 知识点9：CLS归因定位偏移源
onCLS的`metric.attribution`包含：largestShiftTarget(最大偏移元素选择器)、largestShiftTime、largestShiftValue、largestShiftSource(impactedNodes受影响节点列表)。用于定位是哪个元素导致了最大布局偏移——常见根因：图片无width/height、字体swap(FOIT/FOUT)、动态注入内容、广告位无预留。（来源：https://codelabs.developers.google.com/codelabs/web-vitals-google-analytics-bigquery ）

### 知识点10：Next.js内置useReportWebVitals hook
Next.js提供`useReportWebVitals((metric)=>{...})`内置hook，在app/layout.tsx的客户端组件('use client')中使用即可自动采集LCP/INP/CLS/FCP/TTFB。比直接安装web-vitals库更集成——Next.js内部已封装。metric对象包含name/value/id/startTime/attribution/rating。可上报到GA4、PostHog或自建端点。注意：只在客户端运行，服务端渲染时不执行。（来源：https://nextjslaunchpad.com/article/nextjs-web-vitals-usereportwebvitals-inp-lcp ）

### 知识点11：Sentry Next.js一键Wizard安装
`npx @sentry/wizard@latest -i nextjs`自动完成：创建sentry.client.config.ts(浏览器SDK)、sentry.server.config.ts(Node.js SDK)、sentry.edge.config.ts(Edge Runtime SDK)；修改next.config.mjs添加withSentryConfig包装；创建.env.sentry-build-plugin(SENTRY_AUTH_TOKEN)；添加.sentryclirc和示例page。App Router和Pages Router都支持。Wizard是推荐安装方式，手动配置容易遗漏edge runtime。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/ ）

### 知识点12：Sentry Source Maps上传与安全删除
生产构建(next build)时Sentry在"after production compile"阶段收集生成的chunks和source maps，上传到Sentry，然后**从构建输出中删除客户端source maps**（不发到浏览器）。服务端source maps(.next/server/)保留——运行时错误报告需要且不公开。CI中需设SENTRY_AUTH_TOKEN环境变量（.env.sentry-build-plugin在本地，自动加入.gitignore）。source maps只在生产构建上传，dev构建不上传。（来源：https://blog.sentry.io/setting-up-next-js-source-maps-sentry/ + https://docs.sentry.io/platforms/javascript/guides/nextjs/sourcemaps/ ）

### 知识点13：tracesSampleRate采样策略与tracePropagationTargets
`tracesSampleRate`控制transaction采样率：开发环境1.0(100%)，生产环境0.1(10%)。高流量站点应更低（0.01-0.05）。可用`tracesSampler`函数按路由/用户/操作精细控制（如首页0.05、支付页1.0）。`tracePropagationTargets`控制哪些URL启用分布式追踪header——**必须排除第三方API**（如AdSense、GA4），否则会给第三方请求加sentry-trace header导致CORS问题或数据泄露。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/ + https://sentry.io/lp/application-performance-monitoring/ ）

### 知识点14：Sentry自动埋点覆盖范围
@sentry/nextjs的BrowserTracing集成默认启用，自动采集：页面加载(navigation)、软导航(soft navigations)、用户交互(click/keydown)、fetch/XHR请求、长任务。API路由(Route Handlers)和Next.js Data Fetchers(Server Components/fetch)自动错误采集和tracing。stream模式(Streaming SSR)同样工作——错误在流式渲染过程中被捕获。无需手动instrument业务代码即可获得全链路trace。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/tracing/instrumentation/automatic-instrumentation/ ）

### 知识点15：Sentry Web Vitals集成与Session Replay
Sentry SDK**内置web-vitals采集**（通过browserTracingIntegration），自动上报LCP/INP/CLS/FCP/TTFB到Sentry Performance，与trace关联——可从慢指标页面直接下钻到trace waterfall和Session Replay。无需单独安装web-vitals库。Session Replay双采样率：`replaysSessionSampleRate`(正常会话采样率，如0.1=10%)+`replaysOnErrorSampleRate`(出错会话采样率，建议1.0=100%)。Replay可看用户操作视频+DOM快照+控制台错误+网络请求。（来源：https://sentry.io/solutions/real-user-monitoring-rum/ + https://docs.sentry.io/platforms/javascript/guides/nextjs/ ）

### 落地计划
- **P1-PERF-RUM-001**（已存在待办）：在app/layout.tsx添加useReportWebVitals客户端组件，采集LCP/INP/CLS/FCP/TTFB，通过sendBeacon上报到GA4（event_category=Web Vitals，CLS*1000取整，non_interaction=true，metric.id去重）。基于知识点4/5/6/10。
- **P1-OBS-SENTRY-001**（已存在待办）：用Sentry Wizard接入@sentry/nextjs，配置client/server/edge三个config，source maps自动上传，tracesSampleRate生产0.1，tracePropagationTargets排除第三方API，Session Replay错误会话100%采样。基于知识点11/12/13/14/15。
- **P2-PERF-RUM-DASHBOARD-001**（新增）：在GA4中建立Web Vitals自定义报告，按页面路径维度展示P75 LCP/INP/CLS，识别最差Top10页面作为性能优化优先级。基于知识点2/6。
- 知识点7/8/9（INP/LCP/CLS归因）：当RUM数据发现某页面指标差时，用attribution字段定位根因（inputDelay→主线程阻塞、resourceLoadDuration→图片未优化、largestShiftTarget→布局偏移元素）。


## [2026-09-24] GitHub Actions安全加固：Secrets管理、最小权限、OIDC与供应链安全

**主题**：GitHub Actions安全最佳实践（Secrets脱敏、GITHUB_TOKEN最小权限、OIDC无密钥云认证、Action SHA锁定、依赖供应链安全）
**来源**：GitHub官方文档(Secure use reference, Using secrets, Security hardening, OIDC hardening, Controlling GITHUB_TOKEN permissions, Automatic token authentication, GITHUB_TOKEN reference, Supply chain security, Dependency review, Securing builds)、GitHub Blog(2026 security roadmap)、Microsoft Learn(Manage secrets)、AWS Docs(Secrets Manager in GitHub jobs)
**交叉验证**：GitHub Docs secure-use + security-hardening + Aikido security checklist三方确认SHA锁定必要性；GitHub Docs + Microsoft Learn确认Secrets命名与脱敏机制；GitHub Docs OIDC + AWS Docs确认OIDC云认证流程

### 知识点1：第三方Action必须锁定完整commit SHA
标签(@v4)和分支(@main)是可变引用，仓库维护者可随时重新指向不同commit。锁定完整40位SHA是目前唯一使Action不可变的方式。选择SHA时必须验证它来自Action原仓库而非fork。@main/@master无论发布者是谁都属于高风险。我们已在第83轮对actions/checkout和actions/setup-python锁定SHA。（来源：https://docs.github.com/en/actions/reference/security/secure-use ）

### 知识点2：GITHUB_TOKEN默认权限应设为只读
最佳实践：在workflow级别设置`permissions: contents: read`作为默认，然后在需要写权限的job级别单独提升（如`issues: write, pull-requests: write`）。新仓库默认是restricted模式（contents只读），但旧仓库可能仍是permissive模式（全部read/write）。`pull_request_target`事件即使来自公开fork也授予read/write权限——这是高危点。（来源：https://docs.github.com/en/actions/reference/security/secure-use + https://docs.github.com/en/enterprise-server@3.13/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/controlling-permissions-for-github_token ）

### 知识点3：Secrets日志脱敏依赖精确匹配，结构化数据会导致脱敏失败
GitHub通过精确匹配secret值+常见编码（Base64等）来脱敏日志。如果将JSON/YAML/blob作为单个secret存储，脱敏器无法找到子串精确匹配，导致敏感值以明文出现在日志中。正确做法：每个敏感值创建独立secret。（来源：https://docs.github.com/en/actions/reference/security/secure-use ）

### 知识点4：Secrets不能直接用于if条件判断
`${{ secrets.SECRET }}`不能直接出现在`if:`条件中。正确做法：将secret设为job级别的环境变量，然后在条件中引用环境变量。这同时防止secret值意外出现在workflow逻辑评估中。（来源：https://docs.github.com/es/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets ）

### 知识点5：OpenID Connect(OIDC)消除长期云凭证
如果workflow需要访问支持OIDC的云服务商（AWS/Azure/GCP），可配置workflow直接通过短期JWT token认证，无需存储长期云凭证。需要`permissions: id-token: write`。OIDC交换的是短期凭证（通常1小时），大幅缩小攻击面。（来源：https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect ）

### 知识点6：OIDC信任策略必须验证sub claim限制来源
云服务商的信任策略必须验证JWT的`sub`（subject）claim，限制只有特定仓库/环境/分支/可复用workflow才能assume角色。示例条件：`repo:owner/repo:environment:production`或`repo:owner/repo:ref:refs/heads/main`。可用额外claim：`repository_id`、`repository_visibility`、`event_name`、`ref`、`sha`。AWS不支持自定义claim。不验证sub意味着任何GitHub仓库的workflow都能assume你的角色。（来源：https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect + https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services ）

### 知识点7：pull_request_target是最高危触发器
与`pull_request`不同，`pull_request_target`在目标仓库上下文中运行，拥有read/write GITHUB_TOKEN和secret访问权限，即使PR来自公开fork。绝对不能在`pull_request_target`触发的workflow中checkout并执行PR中的不可信代码。仅应用于打标签、评论等不需要执行PR代码的操作。如果必须checkout，使用`actions/checkout`的`ref`参数指定PR head sha，并在隔离环境中执行。（来源：https://docs.github.com/en/enterprise-server@3.13/actions/reference/github_token-reference + https://docs.github.com/en/actions/reference/security/secure-use ）

### 知识点8：Dependency Review Action阻止引入有漏洞依赖
在PR中显示新增/删除/更新的依赖，包含发布日期、流行度、漏洞信息。可配置严重程度阈值（critical/high/moderate/low），超过阈值直接fail PR。支持`fail-on-severity`、`allow-licenses`/`deny-licenses`、`warn-only`等选项。我们已在第88轮添加dependency-review-action。（来源：https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-supply-chain-security + https://docs.github.com/es/code-security/supply-chain-security/understanding-your-software-supply-chain/configuring-dependency-review ）

### 知识点9：Dependabot自动更新锁定的Action SHA
在dependabot.yml中设置`package-ecosystem: github-actions`，Dependabot会自动检测锁定的Action SHA是否有新版本并开PR更新。支持`cooldown`选项（版本更新延迟天数，安全更新不受此限）。7天cooldown是合理默认——避免自动采纳刚发布的被攻陷版本。我们已在第83轮配置Dependabot。（来源：https://docs.github.com/en/actions/reference/security/secure-use + https://blogs.eclipse.org/post/mika%C3%ABl-barbero/stop-trusting-mutable-references-how-eclipse-foundation-projects-should-harden ）

### 知识点10：2026 GitHub安全路线图：workflow级依赖锁定
GitHub将在workflow YAML中引入`dependencies:`段，锁定所有直接和传递依赖的commit SHA。解决供应链攻击中被攻陷依赖立即传播到所有引用它的workflow的问题。当前仅能锁定直接Action引用，传递依赖（Action内部调用的其他Action/脚本）无法锁定。（来源：https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/ ）

### 知识点11：Artifact Attestation建立构建来源证明
对构建产物生成加密签名声明，包含：关联workflow链接、仓库/组织/环境/commit SHA/触发事件、OIDC token信息。可附带SBOM（软件物料清单）。需要`permissions: attestations: write, id-token: write`。帮助验证你消费的软件的真实来源。（来源：https://docs.github.com/en/code-security/supply-chain-security/end-to-end-supply-chain/securing-builds ）

### 知识点12：Secrets命名规则与大小限制
命名规则：字母数字+下划线、无空格、不能以`GITHUB_`开头、不能以数字开头、大小写不敏感。单个secret最大48KB。更大的secret：本地用GPG加密文件后提交加密文件，将解密口令存为secret。小二进制blob用Base64编码后存储，workflow中解码。（来源：https://docs.github.com/en/enterprise-server@3.14/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets + https://docs.github.com/es/enterprise-server@3.11/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions ）

### 知识点13：Environment级Secret配合保护规则实现人工审批
Secret可限定到特定environment（production/staging）。Environment保护规则：required reviewers（必须人工批准）、wait timer（等待时间）、deployment branches（限制哪些分支可部署）。这将生产secret的访问门禁在人工审批之后。组织级secret可通过access policy限制只有特定仓库可用。（来源：https://learn.microsoft.com/en-us/training/modules/implement-github-actions/6-manage-github-secrets + https://docs.github.com/en/actions/reference/security/secure-use ）

### 知识点14：非Secret敏感值必须用::add-mask::手动脱敏
任何不是GitHub Secret但敏感的值（如动态生成的token、API响应中的密钥）必须通过`::add-mask::VALUE` workflow命令标记为脱敏。否则这些值会以明文出现在日志中。脱敏由runner执行，只在secret被实际使用的job中生效。（来源：https://docs.github.com/en/enterprise-server@3.11/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions ）

### 知识点15：第三方Action安全评估清单
使用第三方Action前检查：(1)是否锁定完整SHA（必须）；(2)star数和最近commit活跃度；(3)是否使用已废弃的`node16`运行时（应升级到node20）；(4)源码中是否有数据外泄行为（curl到未知域名、读取secrets后外传）；(5)是否是actions/*或github/*官方Action（官方仍建议SHA锁定）；(6)是否有已知CVE或安全公告。高风险Action：@main/@master引用、无README、单次commit后无维护。（来源：https://www.aikido.dev/blog/checklist-github-actions + https://docs.github.com/en/actions/reference/security/secure-use ）

### 落地计划
- **P1-SEC-GHA-PERMISSIONS-001**（新增）：审计所有workflow文件（lighthouse-ci.yml、bundle-size.yml、uptime-monitor.yml、index-monitor.yml、dependency-review.yml等），在workflow级别添加`permissions: contents: read`默认只读，对需要写权限的job单独提升。基于知识点2。
- **P2-SEC-GHA-SECRET-AUDIT-001**（新增）：审计所有secret使用，确认无结构化数据secret、无明文敏感值，对动态生成的token添加`::add-mask::`。基于知识点3/4/14。
- **P2-SEC-GHA-PR-TARGET-AUDIT-001**（新增）：检查是否有workflow使用`pull_request_target`触发器，如有则确认未checkout执行不可信PR代码。基于知识点7。
- 知识点1/9：我们已在第83轮完成Action SHA锁定+Dependabot，本次学习确认做法正确，后续新增workflow必须延续此规范。
- 知识点5/6：未来如果接入AWS/云服务部署，必须用OIDC替代长期凭证。当前Vercel部署用Vercel Token，暂不适用。


## [2026-09-24] HTTP缓存策略与Cache-Control/Vercel CDN最佳实践

**主题**：HTTP缓存策略与Cache-Control最佳实践（Vercel CDN + Next.js ISR + Data Cache三层缓存体系）
**来源**：Vercel官方文档(caching/cdn-cache, caching/cache-control-headers, incremental-static-regeneration, runtime-cache/data-cache, cdn-cache/debug-cache-issues)、Vercel KB(caching-antipatterns, optimize-function-invocations)、Next.js官方文档(app/guides/incremental-static-regeneration)、MDN Web Docs(Cache-Control)、Vercel Changelog(runtime-logs-cache-reasons)
**交叉验证**：Vercel docs + Next.js docs + MDN三方确认stale-while-revalidate语义；Vercel docs + KB确认x-vercel-cache头值和缓存可缓存标准

### 知识点1：x-vercel-cache响应头是缓存诊断的核心工具
Vercel CDN在每个响应中返回`x-vercel-cache`头，值包括：HIT（从CDN缓存提供，无Function调用）、STALE（缓存提供+后台重新验证）、MISS（不在缓存中，从源/Function生成）、REVALIDATED（按需重新验证后更新）、BYPASS（Draft Mode/爬虫绕过缓存）。这是判断缓存是否生效的第一手证据。（来源：https://vercel.com/docs/caching/cdn-cache ）

### 知识点2：Vercel CDN可缓存响应的严格标准
响应必须同时满足：GET/HEAD方法、无Range头、无Authorization头、状态码200/404/410/301/302/307/308、内容<10MB（流式Function<20MB）、无Set-Cookie头、Cache-Control不含private/no-cache/no-store、无Vary:*头、Vary不含高基数头（如Cookie）。任一条件不满足则MISS且不写入缓存。（来源：https://vercel.com/docs/caching/cdn-cache ）

### 知识点3：Vercel三级Cache-Control头优先级
Vercel-CDN-Cache-Control（最高，仅Vercel用，不发给客户端）> CDN-Cache-Control（Vercel+其他CDN用）> Cache-Control（Web标准，发给客户端）。Vercel代理会从发给客户端的Cache-Control中剥离s-maxage和stale-while-revalidate指令。Function返回的header优先级高于vercel.json/next.config.js中配置的header。（来源：https://vercel.com/docs/caching/cache-control-headers ）

### 知识点4：stale-while-revalidate(SWR)隐藏延迟
`Cache-Control: s-maxage=1, stale-while-revalidate=59`表示1秒新鲜期+59秒陈旧窗口。陈旧期内请求立即返回缓存内容，同时后台异步重新验证。Vercel代理消费此指令（不发给客户端）。浏览器devtools默认发Pragma:no-cache会触发同步重新验证，掩盖真实SWR行为。（来源：https://developer.mozilla.org/de/docs/Web/HTTP/Reference/Headers/Cache-Control + https://vercel.com/docs/caching/cache-control-headers ）

### 知识点5：stale-if-error容错缓存
`max-age=604800, stale-if-error=86400`表示7天新鲜期，过期后若上游返回500/502/503/504或网络错误，可继续返回陈旧内容1天。Vercel代理消费此指令。注意Vercel服务端缓存目前不支持proxy-revalidate指令。（来源：https://developer.mozilla.org/de/docs/Web/HTTP/Reference/Headers/Cache-Control + https://vercel.com/docs/caching/cdn-cache ）

### 知识点6：ISR优于纯Cache-Control头的六大能力
ISR（Incremental Static Regeneration）提供：持久化存储（31天未访问才淘汰）、自动请求合并（同一路径并发MISS合并为一次Function调用）、300ms全局一致清除、即时回滚（旧部署缓存保留）、缓存屏蔽（CDN MISS时先查ISR缓存）、选择性预渲染。纯Cache-Control头仅在首次响应后按区域缓存，无这些能力。框架支持时优先用ISR。（来源：https://examples.vercel.com/docs/incremental-static-regeneration ）

### 知识点7：ISR缓存按部署隔离——部署频率即缓存策略
每次生产部署获得独立的ISR缓存桶，不复用前一部署的运行时生成条目。高部署频率会严重限制缓存命中率（有团队从24%降到12%）。Data Cache（fetch带next.revalidate）则跨部署持久化。缓解：用staging部署合并PR，手动提升到生产；对共享数据fetch加force-cache。（来源：https://vercel.com/kb/guide/caching-antipatterns ）

### 知识点8：写放大反模式——缓存成本超过收益
ISR缓存写入量超过读取量（比例接近或超过1:1）意味着在为无人阅读的页面付费重新生成。某案例系统级6500万写入vs 4800万读取，产品路由每次读取对应两次重新生成。诊断：在Vercel仪表板比较每路由ISR写入vs读取。修复：增大revalidate间隔、仅对实际变更的内容用按需重新验证、避免cron批量清除。（来源：https://vercel.com/kb/guide/caching-antipatterns ）

### 知识点9：缓存命中但提供旋转骨架屏反模式
x-vercel-cache: HIT但HTML中几乎无实际内容（只有loader/skeleton），hero和主要内容缺失。某案例首页缓存HIT但移动端LCP p75超4秒。原因：useSearchParams()/usePathname()在页面/layout顶层读取导致Suspense边界上移到整页；loading.tsx返回null；主要内容客户端获取。诊断：curl路由确认HIT后读取HTML内容。（来源：https://vercel.com/kb/guide/caching-antipatterns ）

### 知识点10：Vary头缓存碎片化指数级放大
每个Vary头值创建独立缓存条目，额外头指数级增加条目数。高基数头（Cookie、完整Referer URL）使响应实际不可缓存。规则：仅包含真正改变渲染文档的头；优先用值集小且已知的头；避免对Referer做Vary（用query参数替代）；按路由设置Vary而非全局middleware设置。（来源：https://vercel.com/docs/caching/cdn-cache ）

### 知识点11：Next.js x-nextjs-cache与Vercel x-vercel-cache是两层独立缓存
Next.js ISR级别返回`x-nextjs-cache`头（HIT/STALE/MISS/REVALIDATED），Vercel CDN级别返回`x-vercel-cache`头，两者独立。本地调试ISR缓存设置`NEXT_PRIVATE_DEBUG_CACHE=1`可在控制台打印缓存命中/未命中日志。生产验证用`next build && next start`而非dev模式。（来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration ）

### 知识点12：Data Cache（Next.js fetch缓存）的特性与限制
Data Cache是区域级缓存（每个Function运行区域独立），跨部署持久化，单条目最大2MB，每条目最多128个标签，LRU淘汰策略。fetch配置`next: { revalidate: 3600, tags: ['posts'] }`使用。revalidateTag全局传播300ms。与CDN完整响应缓存是不同层：Data Cache存fetch结果，CDN缓存存完整HTTP响应。（来源：https://vercel.com/docs/caching/runtime-cache/data-cache ）

### 知识点13：四类内容的推荐Cache-Control策略
所有访客相同的静态页面：`max-age=0, s-maxage=86400`（CDN缓存1天，浏览器不缓存确保最新）；半静态内容（博客/产品/营销页）：`max-age=120, s-maxage=86400`（浏览器2分钟减少回访边缘请求）；个性化/按用户：`private, max-age=0`（禁止CDN缓存）；不可变哈希静态资源（JS/CSS/字体）：`max-age=31536000, immutable`（Next.js自动设置）。（来源：https://vercel.com/docs/caching/cache-control-headers ）

### 知识点14：Link prefetch对缓存和Function调用的直接影响
Next.js App Router的Link prefetch获取目标路由的RSC payload，在Vercel Query中显示为该路径的额外请求。CDN缓存的prefetch不触发Function，但未缓存的prefetch会触发。设置`prefetch={false}`禁用视口和悬停预取，直接减少Function调用和带宽——这正是本轮P1-PERF-PREFETCH-001的理论依据。prefetch量取决于路由和渲染模式，需实测而非估算。（来源：https://vercel.com/kb/guide/optimize-function-invocations ）

### 知识点15：缓存问题标准调试工作流
(1) `vercel httpstat /path`检查响应头和缓存状态，连续运行2-3次确认HIT一致性；(2) `vercel logs --query "cache" --expand`查看缓存原因（2026年7月起runtime logs显示Cache Reason：Cold/Request collapsed/Error/Draft Mode/Time-based revalidation/Tag-based invalidation等）；(3) 陈旧CDN内容：`vercel cache purge --type cdn`；(4) 陈旧Data Cache：`vercel cache invalidate --tag <tag>`；(5) 陈旧构建缓存：`vercel deploy --force --prod`。（来源：https://vercel.com/docs/caching/cdn-cache/debug-cache-issues + https://vercel.com/changelog/runtime-logs-now-show-cache-reasons ）

### 落地计划
- **P1-PERF-CACHE-AUDIT-001**（已存在待办）：用x-vercel-cache头审计首页/文章页/工具页缓存命中率，确认静态页面HIT、识别异常MISS（Vary key denied/Set-Cookie等）。本次学习的知识点1/2/10/15直接用于此任务。
- **P2-PERF-CACHE-HEADERS-001**（新增）：为半静态页面（文章列表/工具列表/分类页）添加显式Cache-Control头`max-age=120, s-maxage=86400`，改善回访用户浏览器缓存。基于知识点13。
- **P2-PERF-CACHE-VARY-AUDIT-001**（新增）：审计全站Vary头，确保无高基数头（Cookie/Referer）导致缓存碎片化。基于知识点2/10。
- 知识点7（ISR按部署隔离）解释了我们高频部署为何缓存命中率可能不高，未来评估ISR转首页时需考虑部署频率。


### [2026-09-24] 高星GitHub开源工具：size-limit与Performance Budget（性能预算）CI自动化防回归

**知识点1：Performance Budget定义与核心价值** — Performance Budget是防止性能回归的硬性限制，可应用于文件大小、资源数量、加载时间等指标。MDN定义为"a limit to prevent regressions"。核心价值：在PR合并前阻止bundle膨胀，而不是上线后才发现性能问题。预算不是目标而是红线——超过就阻止合并。（来源：https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Performance_budgets + https://web.developers.google.cn/articles/your-first-performance-budget）

**知识点2：size-limit工具定位与生态** — size-limit（ai/size-limit，GitHub 7k+ stars）是CLI工具，在CI中检查JS bundle大小是否超过预设限制。支持多种preset：@size-limit/preset-app（应用项目）、@size-limit/preset-small-lib（库项目）。可配置多个文件的独立限制。与bundlesize类似但更活跃维护，是目前最主流的bundle大小CI门禁工具。（来源：https://skillmd.ai/how-to-build/bundle-analyzer-1/ + http://raw.githubusercontent.com/codeminity/ts-platform/HEAD/CONTRIBUTING.md）

**知识点3：size-limit配置方式** — 支持package.json中的"size-limit"字段或独立.size-limit.json/.size-limit.js配置文件。每个条目包含path（文件路径，支持glob如"dist/**/*.js"）和limit（大小限制如"300 KB"）。可配置多个条目分别限制不同chunk。preset-app自动包含时间限制（加载+执行时间）。（来源：https://skillmd.ai/how-to-build/bundle-analyzer-1/ + http://raw.githubusercontent.com/mohitagw15856/pm-claude-skills/main/skills/performance-budget/SKILL.md）

**知识点4：size-limit CI集成与门禁** — 在GitHub Actions中运行`npx size-limit`或`npm run size`，超过限制时exit code非零导致CI失败，PR无法合并。典型流程：PR触发→安装依赖→构建→size-limit检查。可与Lighthouse CI配合形成双重门禁（bundle大小+实际性能指标）。（来源：http://raw.githubusercontent.com/mohitagw15856/pm-claude-skills/main/skills/performance-budget/SKILL.md + http://raw.githubusercontent.com/codeminity/ts-platform/HEAD/CONTRIBUTING.md）

**知识点5：Google推荐的JS预算阈值** — web.dev经典推荐：页面总JS预算125KB（压缩后），页面总大小300KB，第三方请求数10个。2026年更新建议：移动端总JS < 200KB（gzipped），页面总重 < 800KB。Next.js First Load JS per route目标 < 130KB gzipped（对齐2.5秒LCP在中位移动网络的目标）。营销页<100KB，复杂dashboard可<200KB。（来源：https://web.developers.google.cn/articles/use-lighthouse-for-performance-budgets + https://webperfclinic.com/article/performance-budgets-lighthouse-ci-automate-regression-prevention-cicd-pipeline + https://nextjslaunchpad.com/article/nextjs-bundle-analyzer-reduce-javascript-size）

**知识点6：分层预算策略（四层模型）** — 最佳实践是多层预算独立检查：(1)**Total JS** < 200KB gzipped（First Load）；(2)**Per-page JS** < 50KB gzipped（页面特有chunk）；(3)**Single dependency** < 50KB gzipped（任何单个包）；(4)**Increase vs baseline** < 10%（相比上次构建的增幅）。任何一层超限都阻止合并。这比单一总预算更精细，能定位是哪个页面/依赖导致的膨胀。（来源：http://raw.githubusercontent.com/luanrodrigues/ia-frmwrk/master/dev-team/docs/standards/frontend/testing-performance.md + https://webperfclinic.com/article/performance-budgets-lighthouse-ci-automate-regression-prevention-cicd-pipeline）

**知识点7：Lighthouse CI资源预算配置** — Lighthouse CI支持在.lighthouserc.json中配置resourceSizes和resourceCounts预算：`resourceSizes: [{resourceType:"script", budget:200}, {resourceType:"image", budget:400}, {resourceType:"total", budget:800}]`，`resourceCounts: [{resourceType:"third-party", budget:5}]`。我们第90轮已配置.lighthouserc.json（CLS/TBT断言），可进一步添加资源预算断言形成完整性能门禁。（来源：https://webperfclinic.com/article/performance-budgets-lighthouse-ci-automate-regression-prevention-cicd-pipeline + 我们已有的.lighthouserc.json）

**知识点8：预算基线设定方法（渐进式收紧）** — 第一步是建立开发基线（baseline），用当前生产构建的实际指标作为起点，然后逐步收紧。不要一开始就设激进目标（如<100KB），否则CI永远失败。建议流程：先运行构建记录当前First Load JS→设为初始预算→每次优化后收紧5-10%→最终达到Google推荐阈值。预算应随站点演进而调整。（来源：https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Performance_budgets + https://web.developers.google.cn/articles/your-first-performance-budget）

**知识点9：bundle-intelligence等新一代工具** — bundle-intelligence是较新的npm包，支持更丰富的预算类型：initialJs maxSize、totalJs maxSize、singleChunk maxSize，以及智能回归检测（Initial JS增长≥5% vs baseline自动触发警告）。比size-limit更智能（自动baseline对比），但生态较新。可作为size-limit的补充或替代评估。（来源：https://www.npmjs.com/package/bundle-intelligence）

**知识点10：@adobe/sizewatcher PR可视化反馈** — @adobe/sizewatcher是CI工具，自动在GitHub PR中评论bundle大小变化（+/-KB和百分比），早期发现大依赖添加、大二进制文件、构建产物突增。与size-limit的硬门禁互补：size-limit阻止合并（硬失败），sizewatcher提供可视化反馈（软提醒）。两者配合效果最佳。（来源：https://www.npmjs.com/package/@adobe/sizewatcher）

**知识点11：与@next/bundle-analyzer配合的完整工作流** — 完整bundle治理工作流分三步：(1)**开发时**用@next/bundle-analyzer可视化分析（ANALYZE=true npm run build）找出大依赖；(2)**CI中**用size-limit硬门禁防止回归；(3)**PR中**用sizewatcher评论变化提供反馈。三者配合：分析→预防→反馈。我们刚学了bundle-analyzer（P1-PERF-BUNDLE-ANALYZE-001），size-limit是自然下一步，形成闭环。（来源：https://nextjs.org/docs/15/app/guides/package-bundling + 综合分析）

**知识点12：Next.js First Load JS是核心指标** — Next.js构建输出显示每个路由的First Load JS大小（shared chunk + page-specific chunk），这是最重要的bundle指标，直接影响LCP和TTI。构建时注意观察这个数字。目标：我们的SSG内容站点应在100-130KB gzipped范围。如果超过150KB，需要排查是哪个依赖或组件导致的。（来源：https://nextjslaunchpad.com/article/nextjs-bundle-analyzer-reduce-javascript-size + https://nextjs.org/docs/15/app/guides/production-checklist）

**知识点13：gzip vs brotli vs原始大小的口径** — 预算应基于压缩后大小（gzip或brotli），因为这是用户实际下载的大小。size-limit默认显示gzipped大小，Next.js构建输出的First Load JS也是gzipped。注意：Vercel默认使用brotli压缩（比gzip小15-20%），实际用户下载量比构建输出更小。设预算时用gzipped口径更保守。（来源：https://webperfclinic.com/pl/article/optymalizacja-bundle-javascript-2026-tree-shaking-code-splitting-import-mapy + https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Performance_budgets）

**知识点14：第三方脚本单独预算** — 第三方脚本（AdSense/GA4/Umami/Baidu）应单独设预算，因为它们不受我们代码控制但影响性能。建议：third-party JS总量 < 150KB，第三方请求数 < 5个。配合Partytown（刚学，P1-PERF-PARTYTOWN-001）将第三方脚本移到Worker，可显著降低主线程影响但不减少下载量。预算关注下载量，Partytown关注执行位置，两者互补。（来源：https://webperfclinic.com/article/performance-budgets-lighthouse-ci-automate-regression-prevention-cicd-pipeline + 我们的4个第三方脚本现状）

**知识点15：aitoolcrux落地路线图** — 当前状态：已配置Lighthouse CI（含CLS/TBT断言，第90轮），但无bundle大小硬门禁。落地步骤：(1)**P1**安装size-limit+@size-limit/preset-app，先运行构建记录当前First Load JS基线，配置.size-limit.json；(2)**P1**在现有lighthouse-ci.yml或新建ci.yml中添加size-limit检查步骤；(3)**P2**在.lighthouserc.json添加resourceSizes预算（script<200KB/image<400KB/total<800KB/third-party<5）；(4)**P2**安装Import Cost VSCode插件日常监控导入包大小。预期效果：防止未来添加大依赖导致bundle膨胀，配合P1-PERF-BUNDLE-ANALYZE-001（分析）和P1-PERF-DYNAMIC-IMPORT-001（优化）形成"分析→优化→预防"完整bundle治理闭环。（来源：综合分析 + https://nextjs.org/docs/15/app/guides/package-bundling）

**落地计划**：
- 知识点2+3+4(size-limit配置+CI集成) → P1-CI-SIZE-LIMIT-001：安装size-limit+preset-app，基于当前构建基线配置.size-limit.json，在CI中添加bundle大小门禁
- 知识点7(Lighthouse CI资源预算) → P2-CI-RESOURCE-BUDGET-001：在.lighthouserc.json添加resourceSizes和resourceCounts预算断言
- 知识点6(分层预算) → 配置Total JS<200KB + Per-page<50KB + 增幅<10%三层预算
- 知识点11(完整工作流) → 配合P1-PERF-BUNDLE-ANALYZE-001和P1-PERF-DYNAMIC-IMPORT-001形成分析→优化→预防闭环
- 知识点14(第三方预算) → 配合P1-PERF-PARTYTOWN-001，第三方脚本移到Worker后重新评估third-party预算



### [2026-09-24] Next.js性能优化：动态导入(dynamic import)与第三方库代码分割策略深度实战

**知识点1：next/dynamic = React.lazy + Suspense复合封装** — next/dynamic是React.lazy()和Suspense的复合封装，在app和pages目录中行为一致，支持增量迁移。默认情况下Server Components自动进行代码分割，懒加载主要适用于Client Components。next/dynamic比React.lazy更强大，支持ssr:false、loading等专属选项。（来源：https://nextjs.org/docs/15/app/guides/lazy-loading）

**知识点2：两种懒加载方式对比** — Next.js中有两种实现懒加载的方式：(1)使用next/dynamic的动态导入（推荐，功能更全）；(2)使用React.lazy()配合Suspense（标准React方式）。next/dynamic支持ssr:false选项和loading加载状态组件，React.lazy需要手动包裹Suspense。在App Router中优先用next/dynamic。（来源：https://nextjs.org/docs/15/app/guides/lazy-loading + https://nextjscn.org/docs/app/guides/lazy-loading）

**知识点3：import路径必须显式写死** — 在import('path/to/component')中，路径必须是显式字符串，不能是模板字符串或变量。这是因为webpack/Turbopack需要在构建时静态分析动态导入来生成代码分割点。如果路径是动态的，构建工具无法确定分割边界，会导致整个模块被打包。（来源：https://nextjs.org/docs/pages/guides/lazy-loading）

**知识点4：ssr:false选项与SEO影响** — next/dynamic支持{ ssr: false }选项，组件仅在客户端渲染，不参与SSR。适用于依赖window/document的组件（如地图、图表、富文本编辑器、代码高亮）。但ssr:false会导致该组件内容不在初始HTML中，**对SEO有负面影响**，内容型组件不应使用。aitoolcrux的文章内容组件绝对不能用ssr:false。（来源：https://nextjs.org/docs/15/app/guides/lazy-loading）

**知识点5：loading加载状态与CLS防护** — next/dynamic支持{ loading: () => <Skeleton/> }选项，在组件加载时显示加载状态。也可配合Suspense fallback使用。良好的loading状态可减少CLS（Cumulative Layout Shift）——应预留与实际组件相同尺寸的占位符（骨架屏），避免内容突然跳动。这是Core Web Vitals中CLS指标的关键优化手段。（来源：https://nextjs.org/docs/15/app/guides/lazy-loading）

**知识点6：基于路由的自动代码分割** — Next.js默认按路由段(route segment)自动代码分割，每个页面只加载该页面需要的JS。这是App Router的默认行为，无需额外配置。动态导入是在路由级分割基础上进一步细粒度分割组件级代码——将页面内重型组件拆分为独立chunk，用户不交互就不加载。（来源：https://juejin.cn/post/7556867601496539176 + https://legacy.reactjs.org/docs/code-splitting.html）

**知识点7：@next/bundle-analyzer可视化分析** — @next/bundle-analyzer是Next.js官方插件，生成每个包及其依赖大小的交互式可视化报告（treemap）。使用方式：安装后在next.config.mjs中配置withBundleAnalyzer，运行ANALYZE=true npm run build生成报告（自动在浏览器打开）。用于发现大型依赖、决定哪些需要拆分或懒加载，是bundle优化的第一步。（来源：https://nextjs.org/docs/15/app/guides/package-bundling + https://preview.nextjs.org/docs/pages/guides/package-bundling）

**知识点8：next experimental-analyze快速诊断** — Next.js 16新增`next experimental-analyze`命令，使用Turbopack分析应用bundle输出，理解JS/CSS/其他资源的大小和组成。此命令**不产生应用构建**，比完整构建更快，适合快速诊断bundle组成而不等完整SSG构建。对于我们533工具+105文章的全量构建（2-5分钟），这个命令可快速查看bundle。（来源：https://nextjs.org/docs/app/api-reference/cli/next）

**知识点9：第三方库优化三板斧** — 对于大型第三方库优化策略：(1)**optimizePackageImports**（已配置lucide-react/framer-motion）实现tree-shaking只导入使用的导出；(2)**next/dynamic懒加载**仅在特定页面/交互时使用的重型库；(3)**Bundle Analyzer验证**优化效果，确认chunk体积实际减少。三者配合形成"分析→优化→验证"闭环。（来源：https://nextjs.org/docs/15/app/guides/package-bundling + https://pagepro.co/blog/nextjs-performance-optimization-in-9-steps/）

**知识点10：Server Components是减少bundle最有效手段** — Server Components默认不发送JS到客户端，这是减少bundle体积最有效的方式（比任何代码分割都更彻底）。配合动态导入，将重型Client Components用next/dynamic包裹，可实现"默认Server，按需Client"的最优架构。aitoolcrux的大部分内容页面应为Server Components，仅搜索/筛选/CTA追踪/对比工具选择器用Client Components。（来源：https://nextjs.org/docs/15/app/guides/lazy-loading + https://nextjscn.org/docs/app/guides/lazy-loading）

**知识点11：动态导入的Tree Shaking** — Next.js 15+支持动态导入的Tree Shaking：未使用的exports从动态import()中自动移除。这意味着即使动态导入一个大模块，也只会打包实际使用的导出，进一步减少chunk体积。配合命名导入（import { specificFunc }）而非默认导入整个模块，效果更好。（来源：https://nextjs.org/blog）

**知识点12：Turbopack增量构建与文件系统缓存** — Turbopack（Next.js 16默认bundler）支持增量打包（只构建dev server请求的部分）和文件系统缓存（构建产物持久化到磁盘turbopackFileSystemCache）。这加速了开发和构建，但生产bundle优化仍需关注代码分割——Turbopack的生产构建优化与webpack类似，代码分割策略不变。（来源：https://nextjs.org/docs/pages/api-reference/turbopack）

**知识点13：依赖数量与构建内存优化** — 应用依赖越多，构建时内存使用越高。Bundle Analyzer可帮助发现可移除的大型依赖。Next.js 15支持`experimental.webpackMemoryOptimizations`减少构建时内存。对于aitoolcrux，应定期审计package.json，移除未使用的依赖（用depcheck工具），减少构建时间和内存。（来源：https://nextjs.org/docs/15/app/guides/memory-usage）

**知识点14：生产检查清单工具链** — Next.js官方推荐的bundle优化工具链：(1)**Import Cost**(VSCode插件，实时显示导入包大小)；(2)**Package Phobia**(查新依赖的bundle成本，安装前评估)；(3)**Bundle Phobia**(分析依赖增加的bundle大小)；(4)**Webpack Bundle Analyzer**(可视化webpack输出)。这些配合@next/bundle-analyzer形成完整的bundle治理流程：安装前评估→开发时监控→构建后分析。（来源：https://nextjs.org/docs/13/pages/building-your-application/deploying/production-checklist）

**知识点15：aitoolcrux站点落地优先级与路线图** — 当前已做优化：optimizePackageImports(lucide-react/framer-motion)、tools-index.json(排除6个重字段节省78.1%)、content-visibility、AdSense lazyOnload。下一步路线图：(1)**P1**用@next/bundle-analyzer分析当前bundle组成，找出最大的第三方库和chunk；(2)**P1**将重型Client Components（搜索组件、对比工具选择器）用next/dynamic懒加载，设置loading骨架屏防CLS；(3)**P2**评估framer-motion是否可替换为更轻量的CSS动画（motion.div仅用于少量动画）；(4)**P2**对仅在特定页面使用的库（如代码高亮、图表）用动态导入+ssr:false。（来源：综合分析 + https://nextjs.org/docs/15/app/guides/package-bundling）

**落地计划**：
- 知识点7+8(bundle-analyzer + experimental-analyze) → P1-PERF-BUNDLE-ANALYZE-001：安装@next/bundle-analyzer，分析当前bundle组成，输出最大第三方库和chunk报告
- 知识点1+4+5(next/dynamic + ssr:false + loading) → P1-PERF-DYNAMIC-IMPORT-001：将重型Client Components（搜索组件、对比选择器）用next/dynamic懒加载，loading用骨架屏防CLS
- 知识点9(第三方库三板斧) → 评估framer-motion替换为CSS动画，用Bundle Analyzer验证效果
- 知识点10(Server Components优先) → 配合P1-PERF-RSC-AUDIT-001，将非交互组件移除'use client'
- 知识点14(工具链) → 安装Import Cost VSCode插件，日常开发实时监控导入包大小



### [2026-09-24] 高星GitHub开源工具：Partytown第三方脚本离线化与主线程性能优化（Builder.io/Qwik，GitHub 12k+ stars）

**知识点1：Partytown核心定位与原理** — Partytown是Builder.io/Qwik团队维护的懒加载开源库（beta状态，GitHub 12k+ stars），目标是将资源密集型第三方脚本迁移到Web Worker中运行，释放主线程给应用自身代码。与普通Web Worker不同，Partytown允许Worker中的代码**同步访问DOM**，第三方脚本无需修改即可原样运行。核心价值：分析/追踪/广告脚本不再阻塞主线程，直接改善INP和TTI。（来源：https://partytown.qwik.dev/ + https://www.builder.io/blog/the-ultimate-guide-to-optimizing-javascript-for-quick-page-loads）

**知识点2：同步DOM访问的两种通信机制** — Partytown实现Worker同步访问DOM有两种方式：(1)**Service Worker + 同步XHR（默认）**：Worker发同步XHR到SW拦截的URL，SW暂停请求通过postMessage与主线程通信，再用序列化响应完成XHR。每次DOM访问约2ms开销。(2)**Atomics + SharedArrayBuffer（高性能模式）**：需要COOP/COEP安全头，性能更好但配置复杂，会影响跨域资源加载。默认模式兼容性最好，推荐先用默认模式。（来源：https://partytown.qwik.dev/how-does-partytown-work/ + https://webperfclinic.com/fr/article/partytown-2026-scripts-tiers-web-worker-ecommerce）

**知识点3：Next.js官方集成——next/script strategy="worker"** — Next.js官方支持`<Script strategy="worker">`，自动加载Partytown运行时。需在next.config.mjs中启用`experimental: { nextScriptWorkers: true }`标志。将script标签的type改为"text/partytown"即可将脚本迁移到Worker。Next.js 15 App Router中在app/layout.tsx放置worker策略的Script组件。这是Next.js生态中最标准的Partytown集成方式。（来源：https://nextjs.org/docs/app/guides/scripts + https://webperfclinic.com/fr/article/partytown-2026-scripts-tiers-web-worker-ecommerce）

**知识点4：forward配置——全局函数代理** — Partytown的`forward`配置指定需要从主线程代理到Worker的全局函数调用。常见配置：`forward: ["dataLayer.push"]`(GTM), `"gtag"`(GA4), `"fbq"`(Meta Pixel), `"ym"`(Yandex Metrica)。主线程对这些函数的调用会被序列化并转发到Worker中执行。这是确保GTM/GA4等在Worker中正常工作的**关键配置**——不配置forward会导致数据层调用丢失。（来源：https://partytown.qwik.dev/html/ + https://habr.com/ru/articles/1042228/）

**知识点5：resolveUrl代理——CORS与第三方请求** — Partytown的`resolveUrl`配置用于代理缺少CORS头的第三方脚本请求。通过自定义函数将请求重定向到自有代理端点（如`/proxy/gtm?u=...`），解决Worker中跨域请求限制。对于googletagmanager.com等不支持CORS的域名，必须配置代理，否则脚本无法加载。Vercel上可用Edge Function做代理。（来源：https://webperfclinic.com/sv/article/tredjepartsskript-2026-tam-taggar-analytics-chatt-widgets + https://partytown.qwik.dev/）

**知识点6：适用脚本类型与限制** — Partytown最适合**分析/追踪/广告类脚本**（GA4、GTM、Meta Pixel、Umami、AdSense），这些脚本主要做数据上报不直接操作关键UI。**不适合**：需要同步DOM操作的关键交互脚本、需要在主线程立即执行的脚本、依赖document.write的旧脚本。Partytown仍在beta，不保证所有场景都能工作，需逐个脚本验证。（来源：https://partytown.qwik.dev/ + https://www.builder.io/blog/how-we-cut-99-percent-js-with-qwik-and-partytown）

**知识点7：与next/script四种策略对比** — next/script支持4种策略：`beforeInteractive`(关键脚本SSR注入)、`afterInteractive`(默认，hydration后加载)、`lazyOnload`(空闲时加载，我们AdSense已用此策略)、`worker`(Partytown Web Worker，实验性)。性能排序：worker > lazyOnload > afterInteractive > beforeInteractive。worker策略性能最好但配置最复杂，适合非关键第三方脚本。（来源：https://nextjs.org/docs/app/guides/scripts）

**知识点8：INP改善原理与实测效果** — 第三方脚本在主线程执行时创建Long Task(>50ms)，阻塞浏览器响应用户交互，直接恶化INP。Partytown将这些脚本移到Worker后，主线程Long Task数量大幅减少。webperfclinic实测电商站点INP可从400ms+降至200ms以下。对于我们有4个第三方脚本的站点，主线程Long Task减少预期30-50%。（来源：https://webperfclinic.com/fr/article/partytown-2026-scripts-tiers-web-worker-ecommerce + https://dev.to/playfulprogramming/inp-and-partytown-give-the-main-thread-back-to-your-users-o9m）

**知识点9：Facade模式作为互补方案** — 对于YouTube嵌入、聊天widget、地图等重型第三方组件，Facade模式（用轻量级占位符替换，用户交互时才加载真实组件）可节省200-800KB JS。Facade与Partytown**互补**：Facade用于用户可见的交互组件（点击后加载），Partytown用于不可见的分析/追踪脚本（后台Worker运行）。两者结合可最大化第三方脚本优化效果。（来源：https://webperfclinic.com/uk/article/third-party-scripts-optimization-2026）

**知识点10：Server-Side Tagging作为终极方案** — Google Server-Side Tagging(SST)将标签执行从浏览器移到自有云服务器，浏览器只发一个请求到tagging server，由服务器分发到各分析平台。完全消除第三方脚本的浏览器端开销，但需要服务器运维成本（Cloud Run/App Engine）。Partytown是**客户端方案**（零运维），SST是**服务端方案**（需运维），两者可结合：Partytown处理客户端脚本，SST处理服务端分发。（来源：https://webperfclinic.com/vi/article/quan-ly-hieu-suat-script-ben-thu-ba-nam-2026-huong-dan-toan-dien-tu-partytown-den-server-side-tagging + https://developers.google.com/tag-platform/learn/sst-fundamentals/5-sst-setup-analytics）

**知识点11：调试与数据验证方法** — 配置`debug: true`可在控制台查看Partytown内部日志和Worker通信。验证三步：(1)DevTools Performance面板确认第三方脚本不在主线程执行（无Long Task）；(2)Network面板确认脚本通过Worker加载；(3)确认GA4/Umami数据正常上报（Real-time报告有数据）。每次添加新脚本后必须验证数据收集正常，否则分析数据会丢失。（来源：https://partytown.qwik.dev/ + https://habr.com/ru/articles/1042228/）

**知识点12：静态资源复制与Vercel部署** — Partytown需要将运行时文件（partytown.js、partytown-sw.js等~6KB）复制到public目录。Next.js集成时自动处理，但手动集成需用`@builder.io/partytown/utils`的`copyPartytownFiles`函数在构建时复制。Vercel部署时需确保这些文件在静态资源中可访问（/_partytown/路径）。我们的Vercel SSG部署自动支持静态资源。（来源：https://partytown.qwik.dev/）

**知识点13：COOP/COEP头与Atomics高性能模式** — 启用Atomics+SharedArrayBuffer模式需要两个响应头：`Cross-Origin-Opener-Policy: same-origin`和`Cross-Origin-Embedder-Policy: require-corp`。这会影响跨域资源加载（图片/字体/iframe需要crossorigin属性），与我们当前的CSP配置可能冲突。**建议先用默认Service Worker模式**，不需要改安全头，兼容性最好；Atomics模式作为后续优化选项。（来源：https://webperfclinic.com/fr/article/partytown-2026-scripts-tiers-web-worker-ecommerce + https://partytown.qwik.dev/how-does-partytown-work/）

**知识点14：渐进式迁移策略与回滚** — 不要一次性迁移所有脚本。建议：(1)先迁移Umami（最简单，自有分析）验证数据正常；(2)确认Lighthouse INP改善；(3)再迁移GA4；(4)AdSense最后测试（需操作DOM插入广告iframe，兼容性风险最高）；(5)每个脚本迁移后验证24-48小时数据。**回滚方案**：将type从"text/partytown"改回"text/javascript"，移除strategy="worker"即可，1分钟内回滚。（来源：https://webperfclinic.com/ + https://www.builder.io/blog/the-ultimate-guide-to-optimizing-javascript-for-quick-page-loads）

**知识点15：aitoolcrux站点适用性与优先级** — 当前4个第三方脚本：AdSense(lazyOnload)、GA4、Umami、Baidu Analytics。全部是分析/广告类，适合Partytown。**迁移优先级**：Umami(最简单，自有服务) > GA4(forward:["gtag"]) > Baidu(类似GA4) > AdSense(最后，adsbygoogle.js操作DOM插入广告iframe，兼容性风险最高需重点测试)。预期收益：主线程Long Task减少30-50%，INP从当前~200ms降至~150ms以下，Lighthouse Performance分提升2-5分。（来源：综合分析 + https://nextjs.org/docs/app/guides/scripts + https://webperfclinic.com/fr/article/partytown-2026-scripts-tiers-web-worker-ecommerce）

**落地计划**：
- 知识点3+4+7(Next.js集成+forward+策略对比) → P1-PERF-PARTYTOWN-001：启用nextScriptWorkers实验标志，先将Umami脚本迁移到strategy="worker"，配置forward验证数据正常
- 知识点14(渐进式迁移+回滚) → 按Umami→GA4→Baidu→AdSense顺序逐个迁移，每个验证24小时，回滚方案预设
- 知识点8(INP改善) → 迁移前后用Lighthouse CI对比INP和Long Task数量，量化收益
- 知识点5(resolveUrl代理) → 如果GA4/AdSense脚本加载失败，配置Vercel Edge Function代理CORS请求
- 知识点6+15(适用性+AdSense风险) → AdSense最后迁移，先在preview分支测试广告渲染正常



### [2026-09-24] Next.js性能优化：React Server Components(RSC)与Server Actions深度实战

**知识点1：RSC默认服务端渲染零bundle开销** — Next.js App Router中layouts和pages默认是Server Components，在服务器运行，不需要发送JS到客户端渲染，因此不影响客户端JS bundle体积。只有需要交互的组件才标记"use client"变为Client Components。生产检查清单明确建议：默认用Server Components，仅在需要交互时用Client Components。对于aitoolcrux内容型站点，大部分页面应为纯Server Components，仅搜索/筛选/CTA追踪等交互部分用Client Components。（来源：https://nextjs.org/docs/15/app/guides/production-checklist）

**知识点2：RSC Payload紧凑二进制机制** — RSC Payload是渲染后的Server Components树的紧凑二进制表示，包含三部分：(1)Server Components渲染结果；(2)Client Components占位符及其JS文件引用；(3)从Server Component传给Client Component的props。客户端React用RSC Payload更新DOM。这是App Router流式渲染(Streaming)和部分水合(Partial Hydration)的基础——只发送需要的Client Components JS，不发送整个页面JS。（来源：https://nextjs.org/docs/app/getting-started/server-and-client-components）

**知识点3：Server/Client边界与组合规则** — RSC将组件树拆分为server和client两个模块图。Server Components只在服务器运行不发送到浏览器；Client Components发送到客户端。两者在同一棵树中组合，服务器渲染为RSC Payload。关键规则：边界一旦定义，不能在Server Component中import Client Component的同时又在Client Component中import Server Component——只能通过props传递children模式组合。错误的边界划分会导致不必要的JS发送到客户端。（来源：https://nextjs.org/docs/app/guides/server-and-client-boundary）

**知识点4：自动代码分割与懒加载** — Server Components启用按路由段(route segment)自动代码分割，每个路由只加载该段需要的Client Components JS。可进一步用React.lazy()懒加载大型Client Components和第三方库（如图表库、富文本编辑器），减少初始bundle体积。结合next.config.mjs的optimizePackageImports（已配置lucide-react/framer-motion），可进一步优化tree-shaking。（来源：https://nextjs.org/docs/15/app/guides/production-checklist）

**知识点5：Server Actions两种定义方式** — (1)内联在Server Component中：函数体顶部加"use server"指令，仅该函数是Server Action；(2)模块级：文件顶部加"use server"，该文件导出的所有函数都是Server Actions。Server Actions是异步函数，在服务器上执行，可通过form action属性或在Client Component中直接import调用。模块级方式更适合复用和类型安全。（来源：https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations）

**知识点6：渐进增强(Progressive Enhancement)** — Server Components中通过form action调用的Server Actions支持渐进增强：即使JS未加载或加载失败，浏览器原生form提交仍能工作。Client Components中直接调用Server Action则需要JS加载。这是使用form action属性而非onClick事件调用Server Action的关键优势——对SEO爬虫和弱网环境更友好。aitoolcrux的邮件订阅/搜索等表单应优先用form action模式。（来源：https://nextjs.org/docs/app/getting-started/mutating-data）

**知识点7：与缓存和重新验证深度集成** — Server Action执行后可调用revalidatePath(按URL路径失效缓存)或revalidateTag(按缓存标签失效)。revalidateTag支持stale-while-revalidate策略：后续读取获取旧值同时后台刷新数据，Action自身的重渲染不等待新数据。单次网络往返中Next.js可同时返回更新的UI和刷新的数据，无需浏览器刷新。这是传统POST+redirect模式的重大改进。（来源：https://nextjs.org/docs/app/building-your-application/data-fetching/forms-and-mutations + https://preview.nextjs.org/docs/app/guides/server-actions）

**知识点8：revalidatePath vs revalidateTag选择策略** — revalidatePath按URL路径失效缓存，适用于单一路径受影响且标签过度设计时；revalidateTag按标签失效，适用于多个路由共享同一数据源时（如工具详情页和工具列表页都依赖tools.json）。两者都只能在Server Functions和Route Handlers中调用，不能在Client Components或Middleware中调用。aitoolcrux的工具数据更新应用revalidateTag("tools")一次性失效所有依赖工具数据的页面。（来源：https://nextjs.org/docs/app/getting-started/revalidating + https://nextjs.org/docs/15/app/api-reference/functions/revalidatePath）

**知识点9：useActionState管理表单状态** — React 19的useActionState hook（原useFormState）用于管理Server Action的完整状态：const [state, formAction, isPending] = useActionState(action, initialState)。自动跟踪pending状态（isPending）、返回action的执行结果（state）、支持错误处理。与form action属性配合使用，无需手动管理loading/error state。适用于邮件订阅、搜索提交等表单交互。（来源：https://nextjs.org/docs/app/guides/single-page-applications）

**知识点10：useOptimistic乐观更新** — useOptimistic hook在Server Action完成前乐观更新UI，提供即时反馈。配合startTransition使用：startTransition(() => { addOptimistic(action); dispatch(action); })。适用于评论、点赞、收藏、投票等交互，用户感知响应更快。关键是乐观更新必须可回滚——如果Action失败，UI应自动恢复到真实状态。（来源：https://nextjs.org/docs/app/guides/forms + https://nextjs.org/docs/13/app/building-your-application/data-fetching/server-actions-and-mutations）

**知识点11：数据安全：输入验证与未使用Action自动移除** — Server Actions接收的客户端输入（formData、URL参数、headers、searchParams）必须始终验证，因为客户端可轻易修改。推荐使用zod等schema验证库在Action入口验证所有输入。未被应用引用的Server Action在next build时自动移除，不会创建公开端点——这是Tree Shaking在Server Actions上的应用，避免暴露未使用的API。（来源：https://nextjs.org/docs/15/app/guides/data-security）

**知识点12：Server Action重渲染触发条件** — 当Action执行以下操作时，重渲染包含在同一响应中（无需额外网络请求）：(1)调用updateTag或revalidatePath立即使缓存数据失效；(2)调用refresh重新获取当前路由的RSC Payload；(3)通过cookies()变更cookie。如果Action不执行以上操作，完成后不触发重渲染。理解这一点对避免不必要的重渲染和优化性能至关重要。（来源：https://preview.nextjs.org/docs/app/guides/server-actions）

**知识点13：离线支持useOffline(实验性)** — 启用experimental.useOffline配置后，被网络中断打断的Server Action保持pending状态，网络恢复后自动完成提交，用户不会丢失输入。这对移动端弱网环境和地铁/电梯等场景特别有用。配置方式：next.config.mjs中experimental: { useOffline: true }。目前为实验性功能，生产环境需评估稳定性。（来源：https://nextjs.org/docs/app/guides/forms）

**知识点14：Next.js 15 "use cache"指令** — Next.js 15引入"use cache"实验性指令，用于缓存Server Action或Route Handler的返回结果。支持两种缓存策略：full（完全缓存，直到手动失效）和stale-while-revalidate（返回旧值同时后台刷新）。平台支持：Node.js和Docker容器支持，Static export不支持。可大幅减少重复计算和数据库查询，适用于不常变更的数据查询Action。（来源：https://nextjs.org/docs/15/app/api-reference/directives/use-cache）

**知识点15：Prefetch与RSC Payload导航优化** — Next.js App Router中Link组件默认prefetch视口内目标路由的RSC Payload。结合Server Components，prefetch只获取紧凑的RSC Payload（二进制），不加载完整HTML，导航时客户端用RSC Payload快速更新DOM。生产环境中prefetch默认启用，可通过prefetch={false}关闭特定链接。对于工具列表页的533个工具链接，应评估prefetch对带宽的影响，可能需要对非首屏链接关闭prefetch。（来源：https://nextjs.org/docs/15/app/guides/production-checklist）

**落地计划**：
- 知识点1+3+4(RSC默认+边界+代码分割) → P1-PERF-RSC-AUDIT-001：审计当前Client Components使用情况，将非交互组件从"use client"改为Server Component，减少bundle体积
- 知识点5+6+9(Server Actions+渐进增强+useActionState) → P1-MONETIZE-003邮件捕获功能：用Server Action + form action + useActionState实现邮件订阅，支持渐进增强
- 知识点7+8(revalidatePath/revalidateTag) → 现有工具数据更新流程：添加revalidateTag("tools")到数据更新Action，一次性失效所有依赖工具数据的页面缓存
- 知识点10(useOptimistic) → CTA按钮交互：点赞/收藏功能用useOptimistic实现乐观更新，提升用户感知速度
- 知识点15(Prefetch) → 工具列表页性能优化：评估533个工具链接的prefetch影响，对非首屏链接设置prefetch={false}



### [2026-09-24] 高星GitHub开源工具：Unlighthouse全站Lighthouse扫描与性能监控（GitHub 3k+ stars）

**知识点1：Unlighthouse vs Lighthouse CLI核心差异** — Unlighthouse单次运行可扫描无限页面(自动URL发现/爬取)，Lighthouse CLI每次只能扫描1个页面(需手动输入URL)。Unlighthouse额外具备：交互式UI、页面缓存、动态采样、内置CI/CD支持。对于533工具页+105文章页的站点，Unlighthouse可一次性全站扫描，Lighthouse CLI需逐个URL手动指定。（来源：https://unlighthouse.dev/integrations/cli）

**知识点2：Unlighthouse vs Lighthouse CI定位互补** — Unlighthouse适合全站审计(自动爬取所有页面，发现长尾问题)，Lighthouse CI适合CI/CD管道(关键页面自动化门禁+历史追踪)。最佳实践：两者结合——Lighthouse CI做PR级4-5个关键页面门禁(error级阻断合并)，Unlighthouse做每周/每月全站扫描(warn级报告长尾页面问题)。（来源：https://unlighthouse.dev/learn-lighthouse/playwright）

**知识点3：快速开始一键全站扫描** — `npx unlighthouse --site https://example.com` 无需配置即可全站扫描。配置文件unlighthouse.config.ts用defineUnlighthouseConfig定义：site(目标URL)、scanner.samples(每页运行次数，默认1，设3更准确)、scanner.throttle(网络节流)、scanner.exclude(排除路径)。（来源：https://unlighthouse.dev/guide/getting-started/installation）

**知识点4：大型站点(50+页面)默认优化配置** — 对于数千页面的大型站点，Unlighthouse提供默认优化：ignoreI18nPages启用(跳过i18n重复页)、maxRoutes设为200(最多扫描200路由)、skipJavascript启用(跳过JS-only页面)、samples设为1(单次运行)、throttling禁用(不模拟慢速网络)、crawler启用(自动爬取)、dynamicSampling设为5(每路由模式采样5个)。避免扫描数千个DOM相似的页面浪费时间。（来源：https://unlighthouse.dev/guide/recipes/large-sites）

**知识点5：CI集成unlighthouse-ci** — `unlighthouse-ci --site <your-site>` 在CI中无头运行，支持--reporter选项输出json/csv/lighthouseServer格式。可上传报告到自建LHCI Server(--lhci-host + --lhci-build-token)。支持assertions配置性能预算，扫描后批量检查所有页面是否达标。CI环境需Node 18+和Chrome。（来源：https://unlighthouse.dev/guide/guides/generating-static-reports）

**知识点6：动态采样(Dynamic Sampling)** — 对于路由模式相似的页面(如/blog/[slug]有105篇、/tools/[slug]有533个)，Unlighthouse自动采样少量代表性页面而非扫描全部，大幅减少扫描时间。dynamicSampling默认值为5(每个路由模式采样5个页面)。可配置为更高值以增加覆盖率，或设为0禁用采样扫描全部。（来源：https://unlighthouse.dev/guide/recipes/large-sites）

**知识点7：Puppeteer集群与并发控制** — puppeteerClusterOptions.maxConcurrency控制并发浏览器实例数，默认为CPU核心数。调试时设maxConcurrency:1配合headless:false和slowMo:100可观察扫描过程。认证场景必须maxConcurrency:1避免多实例登录态冲突。CI环境中可设为2-4平衡速度和资源。（来源：https://unlighthouse.dev/guide/guides/authentication）

**知识点8：认证页面扫描** — 支持通过cookies、localStorage token或自定义headers进行认证扫描。React/Vue/Angular应用存在localStorage中的token可通过配置注入。调试认证时用headless:false观察登录流程，确认认证成功后再切回headless:true。对于我们的公开站点无需认证，但后台管理页如需扫描可配置。（来源：https://unlighthouse.dev/guide/guides/authentication）

**知识点9：报告生成与静态站点** — 可生成静态报告站点(类似Lighthouse报告查看器)，支持CI artifact上传保留30天。reporter选项包括json(机器可读)、csv(表格)、lighthouseServer(上传自建Server)。静态报告可部署到Vercel/Netlify供团队查看历史趋势。CI artifact路径为.lighthouseci目录。（来源：https://unlighthouse.dev/guide/guides/generating-static-reports）

**知识点10：与Playwright集成对比** — Unlighthouse底层使用Puppeteer，适合纯静态/SSR页面全站扫描。对于需要登录、点击、表单填写的复杂交互页面，Playwright+Lighthouse直接集成更灵活(可自定义页面交互后再审计)。选择标准：内容型站点用Unlighthouse，交互型应用用Playwright+Lighthouse。（来源：https://unlighthouse.dev/learn-lighthouse/playwright）

**知识点11：内置页面缓存机制** — Unlighthouse内置页面缓存，重复扫描时自动跳过未变更页面，大幅加快迭代速度。CI环境中可配置缓存目录持久化(actions/cache)，跨workflow run复用缓存。这是Lighthouse CLI不具备的能力，也是Unlighthouse适合频繁扫描的关键优势。（来源：https://unlighthouse.dev/integrations/cli）

**知识点12：路由排除与包含配置** — scanner.exclude支持glob模式排除路径(如/admin/*、/api/*、/_next/*)，也可用include只扫描特定路径。对于aitoolcrux站点，应排除/api/*和/_next/*，聚焦/tools/*、/blog/*、/compare、/category/*等内容页。exclude优先级高于include。（来源：https://unlighthouse.dev/guide/getting-started/installation）

**知识点13：GitHub Actions完整工作流** — 典型流程：checkout → setup-node(Node 18+) → npm ci → npm run build → npm start(后台运行) → wait-on等待服务器就绪 → unlighthouse-ci --site http://localhost:3000 --reporter json。LHCI 0.15.x需要Node 18+，Ubuntu runner预装Chrome在/usr/bin/google-chrome。也可直接扫描已部署的生产URL无需本地构建。（来源：https://unlighthouse.dev/learn-lighthouse/lighthouse-ci/github-actions）

**知识点14：全站性能预算断言** — Unlighthouse CI支持与Lighthouse CI相同的断言格式，可在unlighthouse.config.ts中配置assertions：categories:performance/minScore(整体性能分)、largest-contentful-paint/maxNumericValue(LCP阈值)、cumulative-layout-shift/maxNumericValue(CLS阈值)。全站扫描后可批量检查所有页面是否达标，输出不达标页面清单。这是发现长尾页面性能问题的关键能力。（来源：https://unlighthouse.dev/learn-lighthouse/lighthouse-ci/budgets）

**知识点15：与Lighthouse CI互补的双层策略** — 第一层(PR门禁)：Lighthouse CI扫描4-5个关键页面(首页/工具页/文章页/compare页)，error级断言(CWV指标)阻断性能退化合并。第二层(全站健康度)：Unlighthouse每周/每月全站扫描(动态采样+排除非内容页)，warn级断言输出报告，发现长尾页面(如冷门工具详情页)的性能问题。两层结合既保证关键页面质量，又覆盖全站健康度。（来源：https://unlighthouse.dev/learn-lighthouse/playwright + https://webperfclinic.com/article/performance-budgets-lighthouse-ci-automate-regression-prevention-cicd-pipeline）

**落地计划**：
- 知识点2+15(双层策略) → 新增P2任务：添加Unlighthouse每周全站扫描workflow，与现有Lighthouse CI(关键页面门禁)互补
- 知识点4+6+12(大型站点配置+动态采样+路由排除) → Unlighthouse配置：maxRoutes:200, dynamicSampling:5, exclude:["/api/*","/_next/*"], samples:1, throttle:false
- 知识点5+9+14(CI集成+报告+断言) → unlighthouse-ci --reporter json + assertions配置performance minScore:0.7 + LCP maxNumericValue:4000(warn级，全站不阻断)
- 知识点11(缓存) → CI中配置actions/cache持久化.lighthouseci缓存目录
- 知识点13(GitHub Actions) → 新建.github/workflows/unlighthouse-weekly.yml，每周日运行，扫描生产站https://www.aitoolcrux.com



### [2026-09-24] 高星GitHub开源工具：Lighthouse CI与性能预算(Performance Budget)自动化实战（GitHub 6.5k+ stars）

**知识点1：Lighthouse CI三大核心能力** — Collect(运行Lighthouse审计，可配置设备模拟/网络节流/运行次数)、Assert(对比预算阈值，违规则构建失败)、Upload(存储报告用于历史对比，支持临时公开存储/自建Server/本地文件系统)。三者构成完整的CI性能回归防护链。（来源：https://webperfclinic.com/article/performance-budgets-lighthouse-ci-automate-regression-prevention-cicd-pipeline + https://googlechrome.github.io/lighthouse-ci/docs/getting-started.html）

**知识点2：lighthouserc.json配置结构** — 顶层`ci`对象包含collect、assert、upload、server、wizard五个配置段。collect定义审计URL和运行参数，assert定义断言规则，upload定义报告存储目标。我们项目第85轮已创建.lighthouserc.json，需完善assert段。（来源：https://googlechrome.github.io/lighthouse-ci/docs/configuration.html）

**知识点3：Assert断言preset预设** — `preset: 'lighthouse:recommended'`启用推荐断言集，自动断言常见性能和SEO问题（如图片尺寸、未使用JS、渲染阻塞资源等）。可在此基础上覆盖特定断言。另一preset选项lighthouse:no-pwa排除PWA相关检查。（来源：https://googlechrome.github.io/lighthouse-ci/docs/getting-started.html）

**知识点4：自定义断言格式** — 断言格式为`["error"|"warn"|"off", { minScore: 0.9 }]`（类别分数）或`["error", { maxNumericValue: 2500 }]`（指标数值）。categories:performance/minScore用于整体性能分数，largest-contentful-paint/maxNumericValue用于具体指标数值阈值。（来源：https://googlechrome.github.io/lighthouse-ci/docs/configuration.html + https://www.npmjs.com/package/create-quality-automation）

**知识点5：Performance Budget资源预算** — resource-summary:<resourceType>:(size|count)格式断言资源大小和数量。如`resource-summary:script:size`限制JS总体积，`resource-summary:third-party:count`限制第三方资源数量。资源预算比CLS/TBT更早发现bundle膨胀问题，是性能回归的第一道防线。（来源：https://antigravitylab.net/en/articles/integrations/antigravity-lighthouse-ci-performance-regression-pipeline-guide + https://googlechrome.github.io/lighthouse-ci/docs/configuration.html）

**知识点6：Core Web Vitals断言阈值** — LCP maxNumericValue: 2500ms(良好线)、TBT maxNumericValue: 200-300ms、CLS maxNumericValue: 0.1(良好线)、FCP maxNumericValue: 1800ms。这些阈值与Google web.dev的Core Web Vitals评估标准一致，应设为error级别确保不退化。（来源：https://web.dev/learn-core-web-vitals/ + https://antigravitylab.net/en/articles/integrations/antigravity-lighthouse-ci-performance-regression-pipeline-guide）

**知识点7：Upload目标选项对比** — temporary-public-storage(免费公开存储，GCP Cloud Storage，几天后自动删除，报告链接可粘贴到PR，适合快速上手)、lhci(自建LHCI Server，支持历史趋势仪表盘和构建对比UI)、filesystem(本地文件系统)。生产环境建议自建Server或用temporary-public-storage+CI artifact备份。（来源：https://googlechrome.github.io/lighthouse-ci/docs/configuration.html）

**知识点8：treosh/lighthouse-ci-action GitHub Action** — 社区高星Action封装了LHCI CLI，支持urls参数直接指定审计URL、uploadArtifacts上传报告为CI artifact、temporaryPublicStorage启用临时存储。无需手动安装@lhci/cli。需配合.lighthouserc.json使用断言配置。我们项目第85轮已添加此workflow。（来源：https://github.com/treosh/lighthouse-ci-action）

**知识点9：GitHub Actions工作流完整流程** — 典型流程：checkout(fetch-depth:20用于祖先哈希对比) → setup-node → npm ci → npm run build → npm start(后台运行) → wait-on等待服务器就绪 → 运行LHCI。PR触发时可对比base分支性能，实现PR级性能回归检测。（来源：https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/troubleshooting.md + https://meeplab.com/blog/lighthouse-auditoria-rendimiento-web-movil/）

**知识点10：numberOfRuns减少CI波动** — collect.numberOfRuns设为3-5次取中位数，减少CI环境性能波动导致的误报。大型站点(50+页面)应减少单次审计页面数或拆分到多个并行job，避免CI超时。我们项目533工具+105文章，应只审计关键页面（首页/文章页/工具页/compare页）。（来源：https://unlighthouse.dev/learn-lighthouse/lighthouse-ci/troubleshooting + https://googlechrome.github.io/lighthouse-ci/）

**知识点11：渐进式预算策略** — 不要一开始就设过高阈值。先用preset:lighthouse:recommended获取基线分数，然后设为当前分数的10%更好作为初始预算，逐步收紧。例如当前性能分75，先设minScore:0.7，达到后再提到0.8、0.9。避免CI持续失败导致团队忽略性能检查。（来源：https://unlighthouse.dev/learn-lighthouse/lighthouse-ci/troubleshooting）

**知识点12：LHCI Server自建方案** — 支持sqlite/mysql/postgresql存储，提供历史趋势仪表盘和构建对比UI，可深入对比两次构建间的指标差异。可通过防火墙规则限制内网访问，CI机器需放行。适合需要长期性能监控和趋势分析的团队。Docker一键部署可用。（来源：https://googlechrome.github.io/lighthouse-ci/docs/server.html）

**知识点13：断言优先级分层策略** — 关键Core Web Vitals指标(LCP/CLS/TBT)用error级别(构建失败，强制修复)、次要指标(资源数量/可访问性分数/最佳实践)用warn级别(警告不阻断)、不相关审计(uses-http2/canonical等已知不适用项)用off关闭。分层避免CI噪音。（来源：https://webperfclinic.com/article/performance-budgets-lighthouse-ci-automate-regression-prevention-cicd-pipeline + https://antigravitylab.net/en/articles/integrations/antigravity-lighthouse-ci-performance-regression-pipeline-guide）

**知识点14：设备模拟与网络节流配置** — collect.settings可配置emulatedFormFactor(mobile/desktop/none，默认mobile)、throttlingMethod(simulate/devtools/provide，默认simulate)、throttling(CPU慢化倍数/网络上下行速度)。移动端优先的站点用默认mobile模拟；如需桌面端数据可单独跑一次desktop。（来源：https://github.com/GoogleChrome/lighthouse/blob/main/docs/configuration.md）

**知识点15：与Vercel Preview Deployment集成** — 可在Vercel部署完成后通过Preview Deployment URL运行LHCI，实现PR级性能对比。Vercel GitHub App会在PR中自动添加预览URL，LHCI可直接audit该URL。也可在CI中npm run build后本地运行审计，不依赖Vercel部署完成。（来源：https://github.com/treosh/lighthouse-ci-action + https://vercel.com/docs/deployments）

**落地计划**：
- 知识点2+3+4+6(lighthouserc配置+preset+断言格式+CWV阈值) → 完善项目.lighthouserc.json：添加preset:lighthouse:recommended + LCP/CLS/TBT error级断言 + performance minScore:0.8
- 知识点5+13(资源预算+断言分层) → 添加resource-summary:script:size warn级断言(限制JS体积)，third-party:count warn级断言
- 知识点8+9+10(GitHub Action+工作流+运行次数) → 完善.github/workflows/lighthouse-ci.yml：只审计4个关键页面，numberOfRuns:3，wait-on等待本地服务器
- 知识点11(渐进式预算) → 首次运行获取基线后设初始预算，不追求一步到位
- 知识点15(Vercel集成) → 评估是否改用Vercel Preview URL作为审计目标，替代本地构建



### [2026-09-24] 高星GitHub开源工具：Sentry前端错误监控与性能追踪完整集成方案（GitHub 38k+ stars）

**知识点1：Next.js SDK一键安装** — `npx @sentry/wizard@latest -i nextjs` 自动创建instrumentation.ts、修改next.config.mjs、生成.env.sentry-build-plugin（含auth token）并自动加入.gitignore。无需手动配置。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/）

**知识点2：tracesSampleRate采样率策略** — 开发环境设1.0（全量采集便于调试），生产环境建议0.1（10%采样控制成本）。可用tracesSampler函数按事务名动态采样，例如排除/health检查返回0.0。高流量站点应降低采样率。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/）

**知识点3：Automatic Instrumentation自动插桩** — @sentry/nextjs默认启用BrowserTracing集成，自动监控浏览器页面性能；自动采集API路由和Next.js Data Fetchers（fetch/Server Components）的错误和tracing；App Router streaming模式同样支持自动插桩。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/tracing/instrumentation/automatic-instrumentation/）

**知识点4：tracePropagationTargets分布式追踪** — 控制哪些出站请求携带sentry-trace和baggage headers，默认['localhost', /^\/$/]。必须将后端API域名加入此列表否则前后端分布式追踪断链；不要对第三方分析/广告域名开启（可能导致CORS错误）。（来源：https://docs.sentry.io/platforms/javascript/）

**知识点5：Source Maps生产构建自动上传** — 仅在next build（生产构建）时自动上传source maps，next dev不上传。CI/CD中需设SENTRY_AUTH_TOKEN环境变量。.env.sentry-build-plugin自动被.gitignore忽略。authToken必须保密，绝不能提交到版本控制。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/sourcemaps/）

**知识点6：Source Maps时序铁律** — source maps必须在错误发生之前上传到Sentry，Sentry不会回溯将新上传的source maps应用到之前的错误。因此部署流程必须是：构建上传source maps → 部署新版本 → 用户访问产生错误。可用Sentry在线source map验证工具检查构建是否正确。（来源：https://docs.sentry.dev/platforms/javascript/guides/nextjs/sourcemaps/troubleshooting_js/）

**知识点7：Session Replay双采样率设计** — replaysSessionSampleRate: 0.1（10%会话全量录制实时发送），replaysOnErrorSampleRate: 1.0（出错会话100%录制）。未被采样的会话仅在内存中缓冲最近60秒，出错时才发送缓冲内容。这种设计兼顾成本和调试价值。（来源：https://docs.sentry.io/platforms/javascript/session-replay/）

**知识点8：Session Replay体积与性能开销** — Replay增加约50KB(gzipped) bundle体积。录制在Web Worker中进行数据压缩，不阻塞浏览器UI线程。默认masking（隐藏文本/输入）减少像素数据从而降低网络开销。支持懒加载Replay仅在需要时启动以减小初始bundle。（来源：https://docs.sentry.io/platforms/javascript/guides/solid/session-replay/troubleshooting/ + https://sentry.io/product/session-replay/）

**知识点9：SDK Bundle体积明细(v10)** — @sentry/browser基础包约26KB gzipped；含Tracing约45.54KB；含Tracing+Replay约83.87KB（启用tree-shaking flags后73.74KB）。v8移除ES5 polyfills，v9基线提升到ES2020，减小了转译输出体积。应定期升级SDK以获取体积优化。（来源：https://blog.sentry.io/overdue-for-a-sentry-sdk-upgrade/ + https://newreleases.io/project/npm/@sentry/react/release/10.72.0）

**知识点10：Sentry对网站性能零阻塞** — SDK作为异步非阻塞的错误监听器运行，错误/事件通过sendBeacon或fetch异步发送到Sentry.io，不阻塞主线程渲染。官方明确声明不影响网站性能。对于SSG站点，SDK仅在客户端hydration后加载。（来源：https://sentry.io/for/frontend/）

**知识点11：Filtering事件过滤** — beforeSend回调可在事件发送前修改或丢弃（如过滤已知第三方脚本错误）；beforeSendSpan可修改或丢弃单个span。可过滤掉健康检查、分析请求、机器人流量等不需要的事务，降低数据量和成本。（来源：https://docs.sentry.io/platforms/javascript/configuration/filtering/）

**知识点12：Vercel集成与post-build上传** — Vercel Marketplace有官方Sentry集成，部署时自动上传source maps。Next.js 15.4.1+支持post-build upload模式：所有构建（client/server/edge）完成后单次操作上传全部source maps，比默认的逐构建上传更快。命令：`npx @sentry/wizard@latest -i sourcemaps --saas --coming-from vercel`。（来源：https://vercel.com/marketplace/sentry + https://docs.sentry.io/platforms/javascript/guides/nextjs/manual-setup/webpack-setup/）

**知识点13：Release版本管理** — release名称必须在SDK init的release选项和sourcemaps upload的--release参数中保持一致。推荐用GITHUB_SHA或CI_COMMIT_SHA作为release名。release将错误、source maps和部署关联起来，支持在Sentry UI中按版本对比错误率。（来源：https://docs.sentry.io/platforms/javascript/guides/node/sourcemaps/uploading/uglifyjs.md）

**知识点14：Browser Profiling浏览器端性能分析** — 需服务器在响应头中返回`Document-Policy: js-profiling`。profileSessionSampleRate每会话决定是否profile（初始化时决定一次）。Profile采集浏览器端JS函数级性能数据，可定位具体函数的CPU耗时。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/profiling/browser.md）

**知识点15：Performance Monitoring预建仪表盘** — 开启tracing后自动获得分层仪表盘：前端（Core Web Vitals、事务时长、错误率）、后端（数据库查询、API调用、缓存、队列、crons）、AI监控（LLM调用延迟、token用量）。无需额外配置即可查看端到端性能。（来源：https://docs.sentry.io/product/sentry-basics/performance-monitoring/）

**落地计划**：
- 知识点1+5+12(Sentry安装+Source Maps+Vercel集成) → P1-PERF-RUM-001任务：在项目中接入Sentry，配置Vercel自动上传source maps，SENTRY_AUTH_TOKEN存入Vercel环境变量
- 知识点2+4(采样率+tracePropagationTargets) → 接入时配置生产环境10%采样，将自有API域名加入tracePropagationTargets
- 知识点7+8(Session Replay) → 接入时配置10%会话采样+100%错误采样，评估50KB bundle增加对LCP的影响
- 知识点9(SDK体积) → 接入时启用tree-shaking flags，将Sentry SDK动态导入减少首屏bundle
- 知识点11(Filtering) → 配置beforeSend过滤已知第三方脚本错误（如AdSense、GA4的非关键错误）



### [2026-09-24] Vercel部署优化深度实战

**知识点1：Build Cache机制** — Vercel自动缓存node_modules、.next/cache/**、lockfiles，上限1GB，保留1个月。首次构建cache为空较慢，后续构建复用缓存可显著加速。缓存key基于框架预设和依赖文件。（来源：https://vercel.com/docs/deployments/troubleshoot-a-build）

**知识点2：构建机器分级** — Standard(4 vCPU)、Enhanced(8 vCPU)、Turbo(30 vCPU)、Elastic(自动伸缩4-30 vCPU，新付费团队默认)。CPU密集型构建（打包、类型检查）在更多vCPU上完成更快。Pro/Enterprise可在项目设置中切换。（来源：https://vercel.com/docs/builds/managing-builds）

**知识点3：构建超时45分钟** — 最大构建时间45分钟，超时即失败。优化方式：合并相关API路由为单handler、用动态段替代大量静态路由文件、统一runtime、减少跨函数共享大依赖。（来源：https://vercel.com/kb/guide/troubleshooting-build-error-build-step-did-not-complete-within-45-minutes）

**知识点4：构建内存与OOM** — Hobby/Pro默认8192MB内存。SIGKILL/OOM错误可用NODE_OPTIONS="--max-old-space-size=6144"在构建命令前增加Node堆大小。大JSON文件（如7.86MB tools.json）在构建时全量加载可能触发OOM。（来源：https://vercel.com/kb/guide/troubleshooting-sigkill-out-of-memory-errors）

**知识点5：并发构建与排队** — 团队可启用On-demand Concurrent Builds；项目级并发控制；紧急部署可用Force on-demand；可设置Production优先于Preview，避免生产构建被预览构建阻塞。（来源：https://vercel.com/docs/builds/managing-builds）

**知识点6：Monorepo自动跳过未变更项目** — Vercel自动检测项目文件（含依赖）是否变更，未变更的项目跳过构建部署，不占用并发槽位。配合Turborepo/Nx Remote Cache可进一步节省构建时间。（来源：https://vercel.com/docs/builds）

**知识点7：Function maxDuration配置** — 默认所有计划300秒(5分钟)。Hobby上限300s，Pro/Enterprise上限800s，扩展上限1800s(30分钟)Beta。设置合理的maxDuration可控制计费（按执行时间计费），不必所有函数都给5分钟。（来源：https://vercel.com/docs/functions/configuring-functions/duration）

**知识点8：Edge Runtime限制** — 内存128MB，必须在25秒内开始返回响应，之后可持续流式传输最多300秒；gzip后大小Hobby 1MB/Pro 2MB/Enterprise 4MB；默认全球部署可指定区域。基于V8引擎，不支持全部Node.js API。（来源：https://vercel.com/docs/functions/runtimes/edge/edge-functions.rsc）

**知识点9：Fluid Compute自动伸缩** — 自动优化现有资源再扩容，低延迟应对流量高峰；waitUntil支持请求完成后后台处理（日志、分析）；自动冷启动优化（字节码缓存减少冷启动影响）。（来源：https://vercel.com/docs/fluid-compute）

**知识点10：vercel.json完整配置项** — buildCommand、outputDirectory、framework、functions(按路径配maxDuration/runtime/memory)、headers、redirects、rewrites、cleanUrls、crons、ignoreCommand、regions、images、installCommand。Next.js项目通常不需要vercel.json（自动检测），但安全头和重定向可在此配置。（来源：https://vercel.com/docs/project-configuration/vercel-json）

**知识点11：Prebuilt部署(--prebuilt)** — 在CI(GitHub Actions)中执行构建，仅上传.vercel/output到Vercel。优势：源码隐私（仅输出上传）、部署前可跑测试门禁、避免Vercel重复构建。命令：npx vercel --prebuilt。（来源：https://vercel.com/kb/guide/github-actions-vercel）

**知识点12：Next.js构建时间优化** — getStaticPaths用fallback:true/blocking将页面生成从构建时移到请求时；更新Node.js版本获取运行时性能提升；experimental.optimizePackageImports(lucide-react/framer-motion)减少打包体积；构建中跳过tsc（在CI中单独跑类型检查）。（来源：https://vercel.com/kb/guide/how-do-i-reduce-my-build-time-with-next-js-on-vercel）

**知识点13：Function区域与延迟** — Function区域应与源API/数据库同区域以减少延迟。默认iad1(美东)，可在vercel.json中设regions数组或项目设置中配置。全球流量自动路由到最近区域，但数据存储区域决定后端延迟。（来源：https://vercel.com/docs/production-checklist）

**知识点14：Build Output API与.vc-config.json** — 每个函数目录含.vc-config.json，配置runtime(nodejs22.x)、handler、maxDuration、launcherType、shouldAddHelpers。支持自定义构建管线输出Vercel可部署格式。（来源：https://examples.vercel.com/docs/build-output-api/primitives）

**知识点15：ignoreCommand跳过无关部署** — 在vercel.json或项目设置中配置ignoreCommand，当仅变更docs/README等无关文件时跳过部署，节省构建分钟。示例：git diff HEAD^ HEAD --quiet . ':(exclude)*.md'。（来源：https://vercel.com/docs/project-configuration/vercel-json）

**落地计划**：
- 知识点4(构建内存OOM) → 下一轮评估tools.json 7.86MB在构建时是否全量加载，确认tools-index.json迁移后构建内存是否下降，必要时添加NODE_OPTIONS
- 知识点7(maxDuration) → P1-PERF-RUM-001任务中为API路由设置合理maxDuration（当前默认300s过大）
- 知识点12(Next.js构建优化) → 评估首页工具列表是否可用fallback模式减少构建时间（当前533工具全量SSG）
- 知识点10(vercel.json) → 确认当前安全头配置在next.config.mjs中是否最优，评估是否迁移部分到vercel.json
- 知识点15(ignoreCommand) → 配置ignoreCommand跳过仅文档变更的部署，节省构建时间



## [2026-09-23] HTTP缓存与CDN边缘缓存深度优化（15知识点）

**主题**：Vercel CDN Cache / Cache-Control三级头 / stale-while-revalidate / ISR / Vary头 / 缓存失效 / 静态资源immutable / x-vercel-cache诊断

**来源**：
- Vercel CDN Cache官方文档: https://vercel.com/docs/caching/cdn-cache
- Vercel Cache-Control headers: https://vercel.com/docs/caching/cache-control-headers
- Vercel ISR文档: https://vercel.com/docs/incremental-static-regeneration
- Vercel缓存失效: https://vercel.com/docs/caching/cdn-cache/purge
- Vercel缓存问题诊断: https://vercel.com/docs/caching/cdn-cache/debug-cache-issues
- Next.js缓存与重验证: https://nextjs.org/docs/app/getting-started/caching-and-revalidating
- Next.js ISR指南: https://nextjs.org/docs/app/guides/incremental-static-regeneration
- MDN Cache-Control: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control

### 知识点

1. **Vercel四层缓存架构**：①CDN Cache（全球边缘PoP，存储完整HTTP响应，命中则单数字ms返回，无回源）；②Data Cache（Next.js fetch结果缓存）；③Full Route Cache（ISR页面HTML缓存）；④Router Cache（客户端路由缓存，浏览器内存）。CDN缓存通过Cache-Control头控制，静态文件自动缓存无需配置。（来源：Vercel docs）

2. **三级Cache-Control头分别控制不同层**：`Cache-Control`（浏览器+所有CDN共享）、`CDN-Cache-Control`（Vercel CDN+下游CDN，浏览器不受影响）、`Vercel-CDN-Cache-Control`（仅Vercel CDN，不返回浏览器也不转发下游）。可设不同TTL：浏览器max-age=10、下游CDN s-maxage=60、Vercel CDN s-maxage=3600。（来源：Vercel CDN Cache docs）

3. **s-maxage vs max-age的分工**：`max-age`控制浏览器（私有缓存），`s-maxage`控制共享缓存（CDN）。Vercel CDN缓存Function响应**必须**包含`s-maxage=N`。若只设Cache-Control不设CDN-Cache-Control，Vercel在返回浏览器前会**自动剥离**s-maxage和stale-while-revalidate（避免浏览器误用CDN指令）。（来源：Vercel CDN Cache docs + MDN）

4. **stale-while-revalidate（SWR）核心机制**：CDN缓存过期后仍立即返回旧内容，同时后台异步回源刷新。典型HTML配置：`public, max-age=0, s-maxage=60, stale-while-revalidate=86400`——浏览器不缓存HTML（每次导航拿最新），CDN缓存60s，过期后24h内仍返回旧内容并后台刷新。Chrome/Firefox/Edge浏览器级支持，Safari不支持浏览器级但CDN级支持。（来源：Vercel docs + MDN + webperfclinic）

5. **可缓存响应的硬条件（缺一不可）**：GET/HEAD方法、无Range头、无Authorization请求头、状态码200/404/410/301/302/307/308、响应体≤10MB（流式函数20MB）、**无Set-Cookie响应头**、Cache-Control不含private/no-cache/no-store、无Vary:*、Vary不含高基数头（如Cookie）。任何一条不满足则x-vercel-cache: MISS。（来源：Vercel CDN Cache docs）

6. **Vary头的双刃剑**：Vary将指定请求头加入缓存key，可实现按国家（X-Vercel-IP-Country）/语言（Accept-Language）缓存不同版本。但每个Vary头**指数级增加**缓存条目数。**Vary: Cookie会导致完全不可缓存**——Vercel直接拒绝缓存并在runtime log记录"Vary key denied"。Accept和Accept-Encoding默认已在缓存key中，无需显式声明。（来源：Vercel CDN Cache docs）

7. **静态资源immutable长缓存**：`/_next/static/*`下的内容哈希文件自动获得`public, max-age=31536000, immutable`（1年不可变）。Next.js 16.3新增`/_next/static/immutable/*`专用路径。文件名含内容哈希，新版本自动生成新文件名，旧文件自然失效，**无需手动purge**。不要尝试覆盖此配置。（来源：Vercel blog + community docs）

8. **ISR = SWR的框架级实现**：Next.js ISR在Vercel上自动遵循stale-while-revalidate模式。访问者获得快速缓存响应，Vercel后台按revalidate间隔或on-demand API调用重新生成。**自动请求折叠**：同一未缓存路径的并发请求合并为一次函数调用/区域，保护后端防流量尖峰。**全局一致purge**：revalidate后所有区域300ms内更新，HTML和data payload一起purge保证全页加载和客户端跳转内容一致。（来源：Vercel ISR docs）

9. **缓存失效的四种方式**：①Next.js revalidateTag/revalidatePath/updateTag（框架级，推荐，updateTag仅Server Action立即过期用于read-your-own-writes）；②Vercel @vercel/functions invalidateByTag/dangerouslyDeleteByTag；③CLI `vercel cache purge --type cdn`（全站purge）；④重新部署（静态哈希文件自动失效，但**远程图片缓存不随部署自动失效**）。invalidate=标记过期下次请求刷新，delete=立即删除。（来源：Vercel purge docs + Next.js docs）

10. **x-vercel-cache诊断头**：响应头显示缓存状态：HIT（边缘命中）、MISS（未命中回源）、STALE（返回过期内容同时后台刷新=SWR生效）、BYPASS（绕过缓存）。MISS时检查runtime log中的原因（Vary key denied / Set-Cookie / Authorization等）。调试工具：`vercel httpstat /path`。（来源：Vercel debug-cache-issues docs）

11. **缓存按区域分段+best-effort驱逐**：Vercel CDN按区域（region）分段缓存，不是全局单一缓存实例——同一URL在不同区域可能分别HIT/MISS。最大缓存时间1年（s-maxage/max-age/stale-while-revalidate），但是**best-effort不保证**。频繁请求的资源更可能存活整个TTL，低频请求（如每天1次）可能被区域LRU驱逐。（来源：Vercel CDN Cache docs）

12. **远程图片缓存的特殊性**：Vercel Image Optimization对远程图片的缓存**不随重新部署自动失效**。TTL由源站响应的Cache-Control max-age决定（minimum 60s）。可手动purge所有缓存变换或调整TTL。静态图片（public/目录）缓存跨部署持久化。（来源：Vercel Image Optimization docs）

13. **我们SSG站点的缓存现状评估**：纯SSG页面由Vercel作为静态文件自动缓存，首次请求后缓存至部署生命周期结束（新部署自动切换）。`/_next/static/*`哈希资源immutable 1年。**当前无需手动设置Cache-Control**（静态文件自动处理最优）。若未来引入ISR/动态路由，需用`s-maxage=N + stale-while-revalidate=Z`配置。Set-Cookie会破坏缓存——我们的Umami/GA4都是客户端脚本，不设Set-Cookie，安全。（来源：综合分析）

14. **缓存性能最佳实践清单**：①用版本化URL（内容哈希文件名）从根本上消除失效需求；②HTML页面用SWR（max-age=0, s-maxage=N, stale-while-revalidate=Z）隐藏回源延迟；③监控**按路径分段**的缓存命中率（全局HIT率掩盖局部问题）；④设计源站故障容错（延长stale-while-revalidate期将部分中断变为非事件）；⑤永远不要在可缓存页面设Set-Cookie；⑥避免Vary高基数头。（来源：Vercel docs + 行业最佳实践）

15. **Next.js 15+缓存API重大变化**：fetch默认**不缓存**（Next.js 15改变了force-cache默认），需显式`cache: 'force-cache'`或`next: { revalidate: N }`。revalidateTag新增`profile="max"`参数使用SWR语义（推荐，旧的立即过期行为已弃用）。新增updateTag（仅Server Action内，立即过期，用于read-your-own-writes场景）。新增cacheTag + 'use cache'指令可缓存任意计算（不限于fetch，包括数据库查询、文件操作）。（来源：Next.js caching-and-revalidating docs）

### 落地计划
- **P1-PERF-CACHE-AUDIT-001**：用x-vercel-cache头审计首页/文章页/工具页的缓存命中率，确认静态页面HIT、识别异常MISS
- **P2-PERF-CACHE-IMMUTABLE-001**：确认public/目录下自定义静态资源（如llms.txt、ads.txt）获得合理Cache-Control，必要时在next.config.mjs中为特定路径加immutable头
- **P2-PERF-ISR-EVAL-001**：评估将高频更新页面（如首页工具列表）从纯SSG转为ISR（revalidate=3600）的可行性，平衡新鲜度与构建时间


## [2026-09-23] Next.js Middleware & Edge Runtime 实战优化（15知识点）

**主题**：Next.js Middleware / Vercel Routing Middleware / Edge Runtime / 动态重定向 / 安全头 / 地理定位 / A/B测试

**来源**：
- Next.js官方文档: https://nextjs.org/docs/app/api-reference/file-conventions/middleware
- Next.js proxy (v16+): https://nextjs.org/docs/app/api-reference/file-conventions/proxy
- Vercel Routing Middleware: https://vercel.com/docs/routing-middleware
- Vercel动态重定向+Edge Config: https://vercel.com/kb/guide/dynamic-redirects-with-edge-config-and-next-js-proxy
- Vercel重定向限制: https://vercel.com/kb/guide/how-can-i-increase-the-limit-of-redirects-or-use-dynamic-redirects-on-vercel
- Next.js CSP指南: https://nextjs.org/docs/app/guides/content-security-policy
- Vercel Edge Runtime: https://vercel.com/docs/functions/runtimes/edge

### 知识点

1. **Middleware文件约定与执行时机**：middleware.ts放在项目根目录（与app/同级），导出default函数+可选config对象。在路由渲染之前执行，可修改response（rewrite/redirect/headers/cookies）。Next.js 16重命名为proxy.ts，函数导出从middleware改为proxy。（来源：Next.js docs）

2. **Matcher精确控制**：matcher支持字符串、数组、正则。最佳实践用负向前瞻排除静态文件：`matcher: '/((?!_next/static|_next/image|favicon.ico).*)'`。高级matcher支持has/missing条件（header/cookie/query存在性），可实现"仅对有Authorization头的请求运行"。（来源：Next.js docs）

3. **Edge vs Node.js运行时**：Middleware默认Edge Runtime（Web标准API、近零冷启动、全球边缘分布、仅支持edge兼容npm包）。v15.5+支持`config.runtime='nodejs'`使用完整Node.js API。Next.js 16的proxy仅支持Node.js。Edge适合轻量逻辑（重定向/头/鉴权判断），Node.js适合需要完整API的场景。（来源：Next.js docs + Vercel docs）

4. **NextResponse四种操作**：`redirect()`（3xx跳转，URL改变）、`rewrite()`（内部代理，URL不变但渲染不同页面，SEO友好）、`next()`（继续到下一个处理器）、`json()`（直接返回JSON）。可同时修改request headers和response headers。（来源：Next.js docs）

5. **Redirect vs Rewrite的SEO影响**：redirect返回307/308，浏览器导航到新URL，搜索引擎更新索引；rewrite在内部渲染另一个页面但URL不变，适合个性化内容（A/B测试变体），不会稀释SEO权重。（来源：Vercel docs + Next.js docs）

6. **Edge Config动态重定向**：将重定向规则存在Vercel Edge Config（全球KV存储，读取1-5ms，无速率限制），middleware读取后执行重定向，无需重新部署即可更新规则。大小限制：Hobby 8KB（约80条规则）、Pro 64KB、Enterprise 512KB。超过1000条规则用Bulk Redirects。（来源：Vercel KB）

7. **Vercel重定向2048条限制**：next.config.mjs/vercel.json中的redirects每个部署上限2048条。超过则必须迁移到Routing Middleware。我们当前约50条，远未达限，但Edge Config方案可实现动态更新。（来源：Vercel KB）

8. **Middleware设置安全头+CSP nonce**：可在middleware中设置HSTS/X-Content-Type-Options/Referrer-Policy/Permissions-Policy/CSP。CSP nonce方案：每次请求用`crypto.randomUUID()`生成nonce，注入CSP头和页面。**关键限制：nonce要求每次请求动态生成，会破坏SSG/ISR静态缓存**。我们的SSG站点应使用静态CSP（next.config.mjs中的headers），不要用nonce方案。（来源：Next.js CSP指南）

9. **地理定位头（Vercel自动提供）**：`x-vercel-ip-country`、`x-vercel-ip-country-region`、`x-vercel-ip-city`在请求头中自动可用。可用于语言重定向、区域内容、合规判断。无需额外API调用。（来源：Vercel Routing Middleware docs）

10. **Bot拦截与限流**：可检查User-Agent或Vercel BotID进行bot拦截。限流用Upstash Redis（`@upstash/redis`，edge兼容）。但大规模bot管理应委托给WAF（Cloudflare/Vercel Firewall），不要在middleware中做复杂规则。（来源：Vercel docs + 社区指南）

11. **性能最佳实践**：①用精确matcher排除静态文件，避免每个请求都执行；②最小化网络调用（每个fetch增加延迟）；③避免不必要的async/await和Promise.all；④不要设置Set-Cookie（会使响应不可缓存）；⑤用Vercel Observability监控按路径的调用次数和操作类型。（来源：Vercel docs + 社区最佳实践）

12. **请求硬限制**：最大URL长度14KB、请求体4MB、最多64个header、header总长度16KB。超出会被拒绝。（来源：Vercel Routing Middleware docs）

13. **A/B测试与个性化（零CLS）**：Edge Middleware在CDN缓存之前执行，可对SSG静态页面做个性化。用cookie分配变体，rewrite到变体页面。服务端决策，无布局偏移（zero CLS）。用Edge Config存储feature flag和流量比例。（来源：Vercel Edge Middleware白皮书）

14. **计费模型**：Fluid Compute按计算资源使用量计费，不按调用次数。Edge middleware CPU消耗低（便宜），Node.js middleware按Functions计费。简单重定向/头操作用Edge最划算。（来源：Vercel docs）

15. **我们项目的适用场景评估**：当前SSG站点+next.config.mjs（50条重定向+6个安全头）。Middleware可做：①安全头移到middleware实现按路径差异化（如工具页更宽松CSP允许AdSense）；②Edge Config维护模式开关（无需重新部署）；③geo-based联盟链接/语言提示；④bot流量统计。**不要做**：CSP nonce（破坏SSG）、复杂鉴权（无用户系统）、大规模重定向迁移（未达2048限）。（来源：综合分析）

### 落地计划
- **P1-SEC-MIDDLEWARE-CSP-001**：评估将CSP从头配置移到middleware，实现按路径差异化CSP（工具页允许AdSense/GA4，文章页更严格）
- **P2-OPS-MAINTENANCE-MODE-001**：用Edge Config+middleware实现维护模式开关，无需重新部署即可全站503
- **P2-GEO-AFFILIATE-001**：利用x-vercel-ip-country头，在middleware中为不同地区用户rewrite到区域优化的联盟链接页面


## [2026-09-23] GitHub Actions自动化：安全扫描与依赖审计工作流（Dependabot / CodeQL / Secret Scanning / Push Protection / Dependency Review / Snyk / TruffleHog）

**主题**：供应链安全是前端项目的隐形风险——一个被劫持的npm包或泄露的API Key可以让整个站点沦陷。当前我们已有6个安全头+CSP+action SHA锁定，但代码扫描和依赖审计层尚未完整搭建。公共仓库可免费使用全部GitHub Advanced Security功能。

**知识点1：Dependabot version updates（版本更新自动化）** — 通过.github/dependabot.yml配置。关键字段：package-ecosystem（npm/pip/docker/github-actions等）、directory（依赖文件路径）、schedule.interval（daily/weekly/monthly）、open-pull-requests-limit（默认5，控制同时打开的PR数）、reviewers/assignees/labels、target-branch、groups（分组更新）、ignore（忽略特定包/版本）。自动检测依赖新版本并开PR。公共仓库免费。来源：https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates 、https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates

**知识点2：Dependabot security updates（安全更新）** — 与version updates是两个独立功能。当依赖中发现CVE漏洞时，自动开PR升级到安全版本。安全更新PR不受open-pull-requests-limit限制。可通过dependabot.yml的groups分组安全更新。在仓库Settings > Code security and analysis中启用。公共仓库默认开启。与GitHub Advisory Database联动（实时漏洞数据库）。来源：https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates 、https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates

**知识点3：Dependabot groups（分组更新减少PR噪音）** — 新功能，将相关依赖更新合并到一个PR。groups配置：dependency-type（development/production）或patterns（glob匹配包名）。示例：group所有eslint相关包、所有@types包、所有next.js生态包。大幅减少PR数量（从几十个降到几个），降低审查负担。iteration 83我们已添加Dependabot，应检查是否配置了groups。来源：https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file 、https://docs.github.com/ru/code-security/reference/supply-chain-security/dependabot-options-reference

**知识点4：CodeQL代码扫描（语义级漏洞检测）** — GitHub自研语义代码分析引擎，将代码转换成可查询的数据库。两种设置：default setup（自动检测语言和查询套件，一键启用）和advanced setup（自定义.github/workflows/codeql-analysis.yml）。支持语言：JavaScript/TypeScript、Python、Go、Java、C/C++、C#、Ruby。对解释型语言（JS/TS/Python）无需构建步骤。查询套件：default（security-extended+security-and-quality）、security-extended、security-and-quality。结果以code scanning alerts呈现，分Error/Warning/Note三级。来源：https://docs.github.com/code-security/secure-coding/configuring-code-scanning 、https://docs.github.com/ko/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql

**知识点5：CodeQL workflow触发与配置** — 标准触发：push（main/develop分支）、pull_request（PR时扫描）、schedule（每周cron全量扫描）。workflow步骤：github/codeql-action/init（初始化，指定language）→ 自动构建或手动构建 → github/codeql-action/analyze（分析并上传结果）。对JS/TS项目，init后直接analyze无需build。可通过queries字段添加自定义查询包，通过paths/paths-ignore过滤扫描范围。分析结果上传为SARIF格式，在Security标签页查看。来源：https://docs.github.com/code-security/secure-coding/configuring-code-scanning 、https://learn.microsoft.com/ru-ru/training/modules/security-monitoring-and-governance/11-configure-github-advanced-security-github

**知识点6：Secret Scanning（密钥扫描，事后检测）** — 扫描仓库中硬编码的密钥（API Key、token、密码），支持200+种token类型（GitHub PAT、AWS密钥、Stripe、Slack、Google API Key等）。公共仓库默认启用。在密钥提交后检测到并生成alert（事后检测，不阻止提交）。可通过email/webhook通知。对已泄露密钥需立即轮换（即使已删除，git历史中仍存在）。我们的GitHub PAT曾出现在代码中吗？需用TruffleHog扫描历史确认。来源：https://docs.github.com/en/code-security/getting-started/github-security-features 、https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository

**知识点7：Push Protection（推送保护，事前阻止）** — Secret Scanning的主动版本。在git push过程中实时扫描，检测到密钥时**阻止推送**，用户看到详细错误信息（密钥类型、位置、修复方法）。用户可选择移除密钥后重新push，或填写理由绕过（绕过后生成alert）。公共仓库默认启用。这是防止密钥进入git历史的关键防线——比事后检测重要得多。我们用GitHub API提交（Contents API），push protection也会拦截API提交。来源：https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection 、https://docs.github.com/en/code-security/getting-started/github-security-features

**知识点8：Dependency Review Action（PR依赖审查门禁）** — actions/dependency-review-action，在pull_request时扫描PR中变更的依赖。检查：(a)是否引入已知漏洞版本；(b)许可证是否合规（allow-licenses/deny-licenses）；(c)版本变化（deny-packages）。可配置fail-on-severity（critical/high/moderate/low），达到阈值则阻止合并。轻量级，无需额外账户。与Dependabot互补：Dependabot修已有漏洞，Dependency Review阻止新漏洞引入。来源：https://docs.github.com/en/enterprise-server@3.18/code-security/supply-chain-security/end-to-end-supply-chain/securing-code 、GitHub actions/dependency-review-action README

**知识点9：npm audit（内置依赖审计）** — npm自带命令。`npm audit`扫描package.json和node_modules中的已知漏洞（基于GitHub Advisory Database）。`npm audit fix`自动升级有安全补丁的依赖。`npm audit --json`输出JSON供CI解析。`npm audit --production`只检查生产依赖。局限：只检查npm registry包，无法修复所有漏洞（有些需要breaking change升级），可能有误报，输出噪音大。可作为CI步骤但建议配合Snyk使用。来源：npm官方文档 、https://docs.npmjs.com/cli/commands/npm-audit

**知识点10：Snyk（商业安全平台，免费开源层）** — 综合性安全平台，四大产品：Snyk Open Source（依赖扫描，比npm audit更精准，自动生成fix PR）、Snyk Code（SAST代码扫描，AI辅助）、Snyk Container（容器镜像扫描）、Snyk IaC（基础设施即代码扫描）。GitHub Action：snyk/actions/node@master。开源项目免费。可上传SARIF到GitHub Code Scanning统一视图。策略管理（忽略特定漏洞、设置严重度阈值）。与Dependabot相比，Snyk修复建议更精准、支持更多语言。来源：https://github.com/snyk/actions 、Snyk官方文档

**知识点11：TruffleHog（开源git历史密钥深度扫描，~18k星）** — trufflesecurity/trufflehog，开源秘密扫描器。关键优势：扫描**整个git历史**（不只是当前文件），捕获已提交后删除的密钥。支持1000+种密钥类型。**主动验证**（实际测试密钥是否有效，减少误报）。GitHub Action：trufflesecurity/trufflehog@main。可扫描：git仓库、GitHub组织、S3、GCS、Docker镜像等。对我们：扫描整个ai-tools-review仓库历史，确认是否有PAT/API Key曾被提交过。来源：https://github.com/trufflesecurity/trufflehog 、TruffleHog官方文档

**知识点12：Socket.dev（npm供应链攻击专用扫描器）** — 专注npm生态的安全扫描器。检测：安装脚本（postinstall/preinstall）、遥测行为、维护者变更（新维护者突然发布）、风险权限（网络/文件系统访问）、包混淆攻击。socketdev/action GitHub Action，在PR时阻止添加高风险包。与Snyk/Dependabot的区别：那些查已知CVE，Socket查**供应链攻击行为**（即使没有CVE也能发现恶意包）。对我们的533工具数据生成脚本和前端依赖有价值。来源：https://github.com/SocketDev 、Socket.dev官方文档

**知识点13：安全workflow最佳实践（五层防御）** — (1)依赖层：Dependabot version+security updates（自动修复）+ Dependency Review（阻止新漏洞）；(2)代码层：CodeQL（语义漏洞检测）+ Snyk Code（AI辅助）；(3)密钥层：Secret Scanning（事后检测）+ Push Protection（事前阻止）+ TruffleHog（历史深度扫描）；(4)供应链层：Socket.dev（npm恶意包检测）+ npm audit（基础审计）；(5)Action层：所有action锁定commit SHA（iteration 83已做）+ 最小GITHUB_TOKEN权限（permissions: contents: read）。每周定时全量扫描+PR增量扫描。来源：https://docs.github.com/en/code-security/getting-started/github-security-features 、https://resources.github.com/learn/pathways/security/essentials/enabling-github-advanced-security/

**知识点14：GitHub Advanced Security（GHAS，公共仓库全免费）** — GHAS是付费功能集（私有仓库按席位收费），包含：CodeQL、Secret Scanning、Push Protection、Dependency Review。**公共仓库全部免费**。我们的qxgjz/ai-tools-review是公共仓库，因此所有GHAS功能零成本。启用路径：仓库Settings > Code security and analysis > 逐个启用。Default setup for CodeQL会自动创建workflow，无需手写。来源：https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository 、https://resources.github.com/learn/pathways/security/essentials/enabling-github-advanced-security/

**知识点15：我们的安全现状与升级路径** — 已有：6个安全头（HSTS/CSP/X-Frame/nosniff/Referrer/Permissions，iteration 82/87）、action锁定SHA（iteration 83）、Dependabot（iteration 83添加）、Lighthouse CI（iteration 85）。缺失：(a)CodeQL代码扫描（JS/TS语义漏洞检测）；(b)Dependency Review Action（PR依赖门禁）；(c)Push Protection确认已启用（仓库设置）；(d)TruffleHog历史密钥扫描（确认PAT未泄露到历史）；(e)Dependabot groups配置（减少PR噪音）；(f)npm audit CI步骤。升级优先级：CodeQL default setup（P1，一键启用）> Dependency Review action（P1，加workflow）> TruffleHog历史扫描（P2，一次性+定期）> Dependabot groups优化（P2）> Socket.dev评估（P3）。来源：项目实际状态 + https://docs.github.com/en/code-security/getting-started/github-security-features

**落地计划**：
- 知识点4+5+14 → **新增P1-SEC-CODEQL-001**：启用CodeQL default setup（JS/TS语言），在仓库Settings一键启用，自动创建codeql-analysis.yml，push+PR+每周扫描
- 知识点8 → **新增P1-SEC-DEP-REVIEW-001**：添加actions/dependency-review-action到现有CI workflow，PR时阻止引入critical/high漏洞依赖和不合规许可证
- 知识点11 → **新增P2-SEC-TRUFFLEHOG-001**：添加trufflesecurity/trufflehog GitHub Action，扫描整个git历史确认无PAT/API Key泄露，定期运行
- 知识点3 → **新增P2-SEC-DEPENDABOT-GROUPS-001**：优化dependabot.yml配置groups（eslint家族、@types家族、next.js生态分组），减少PR噪音
- 知识点7+13 → **P1-SEC-PUSH-PROTECT-001**（检查项）：确认仓库Settings中Push Protection已启用，防止API Key通过git push或GitHub API提交泄露


## [2026-09-23] 前端工程化最佳实践：CSS性能优化与渲染加速实战（content-visibility / CSS containment / critical CSS / Tailwind生产优化 / 字体显示 / 动画性能）

**主题**：CSS是渲染性能的隐形杠杆——错误的CSS会触发layout/paint风暴，正确的CSS能让浏览器跳过80%的渲染工作。当前我们用Tailwind v3+next/font+next/image，但长文章页和工具列表页尚未利用content-visibility等现代CSS渲染优化。

**知识点1：content-visibility: auto（离屏内容跳过渲染）** — 最强大的纯CSS渲染优化。浏览器跳过视口外元素的layout和paint工作，进入视口时才渲染。Chrome团队web.dev案例：长页面渲染时间从232ms降到30ms（7.7倍加速）。自动施加layout+paint+style containment。2023年起Baseline广泛可用（Chrome 85+/Firefox 129+/Safari 18+）。对长文章页、工具列表页、评论区效果显著。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/content-visibility 、https://web.developers.google.cn/articles/content-visibility?authuser=1&hl=en

**知识点2：contain-intrinsic-size（防止CLS的必备搭配）** — content-visibility:auto跳过渲染时元素高度为0，滚动进入时突然撑开导致CLS。contain-intrinsic-size指定占位尺寸：`contain-intrinsic-size: auto 500px`——auto表示首次渲染后缓存真实高度，500px是首次估算的fallback。必须与content-visibility配对使用，否则CLS分数会恶化。对高度变化大的内容用较大的估算值，误差比0好。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/contain-intrinsic-size 、https://webperfclinic.com/article/css-content-visibility-rendering-performance-guide

**知识点3：CSS contain属性（四种隔离类型）** — contain标示元素及其内容尽可能独立于文档树其余部分，将layout/style/paint/size计算限制在子树内。四种类型：layout（后代布局不影响外部）、paint（后代不绘制到盒子外）、size（元素尺寸独立于内容，需设显式尺寸否则塌陷）、style（计数器/引号作用域）。简写：`contain: content` = layout+paint（最常用）；`contain: strict` = layout+paint+size（最激进）。所有浏览器自2022年3月支持。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/contain 、https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Using

**知识点4：contain: layout（布局隔离）** — 元素后代的布局变化不影响外部布局。元素成为absolute/fixed后代的containing block。建立新的块格式化上下文（BFC）。典型用途：卡片组件、侧边栏、独立widget——内部布局变化（如内容加载、展开/收起）不会触发整页relayout。对我们的工具卡片和文章段落非常适用。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Using 、https://w3c.github.io/csswg-drafts/css-contain-2/

**知识点5：contain: paint（绘制隔离）** — 后代不会绘制到元素盒子外，类似overflow:hidden但无layout副作用。元素成为containing block。对视口外内容、sticky元素、动画元素有用。确保子元素的box-shadow/overflow不会影响外部绘制。与layout组合（contain:content）是最安全的高性能配置。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/contain 、https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_containment

**知识点6：contain: size（尺寸隔离，最激进）** — 元素尺寸完全独立于内容，必须设置显式width/height否则塌陷为0。性能收益最大但最难正确使用。适用场景：已知精确尺寸的媒体容器、固定高度的广告位、骨架屏。通常不直接用size，而是用content-visibility:auto（浏览器自动管理size containment）。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Using 、https://w3c.github.io/csswg-drafts/css-contain-2/

**知识点7：content-visibility: hidden（保持状态的隐藏）** — 与auto不同，即使在视口内也保持跳过渲染。与display:none的关键区别：hidden保留渲染状态（切换回visible时瞬时恢复），display:none销毁状态（重新渲染）。hidden元素仍占据布局空间（配合contain-intrinsic-size）。适用：标签页内容、模态框、手风琴折叠面板——需要瞬时切换且保留滚动位置/表单状态。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/content-visibility 、https://web.developers.google.cn/articles/content-visibility?authuser=1&hl=en

**知识点8：content-visibility vs display:none本质区别** — display:none：元素从渲染树移除，不占空间，子树状态销毁，恢复时完整重渲染（慢）。content-visibility:hidden：元素保留在渲染树中，占据布局空间，子树渲染状态保留，恢复时瞬时（快）。visibility:hidden：占据空间但不可见，仍触发paint（不跳过渲染工作）。选择：需要保留状态用content-visibility:hidden，需要完全移除用display:none。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/content-visibility 、https://webperfclinic.com/article/css-content-visibility-rendering-performance-guide

**知识点9：Tailwind CSS生产优化（JIT模式）** — Tailwind v3默认JIT（Just-In-Time）模式，只生成实际使用的class，生产CSS通常<10KB gzipped（Netflix全站仅6.5KB）。content配置必须扫描所有模板文件（./app/**/*.{js,ts,jsx,tsx,mdx}）。绝对不要在content中包含CSS文件（导致循环引用）。开发与生产CSS一致，无需purge步骤。我们的tailwind.config.ts应确认content路径完整。来源：https://v3.tailwindcss.com/docs/optimizing-for-production 、https://tailwindcss.com/docs/detecting-classes-in-source-files 、https://v3.tailwindcss.com/docs/content-configuration

**知识点10：Tailwind class检测机制（纯文本扫描）** — Tailwind将源文件当纯文本扫描，不解析AST。动态class名如`text-${color}-500`不会被检测到（不会生成）。必须用完整class名或safelist配置。任意值`text-[#ff0000]`、`w-[calc(100%-2rem)]`可正常生成。条件渲染中使用的完整class名会被检测到。常见坑：拼接class名导致生产环境样式丢失。来源：https://tailwindcss.com/docs/detecting-classes-in-source-files 、https://v3.tailwindcss.com/docs/content-configuration

**知识点11：Critical CSS（关键CSS内联）** — 将首屏above-the-fold CSS内联到<style>标签，其余CSS异步加载，消除渲染阻塞CSS请求。工具：Critical（Addy Osmani）、Penthouse。Next.js自动提取critical CSS并内联（App Router自动处理）。对我们的SSG站点，Next.js已处理，但首屏内容结构影响提取效果——确保首屏组件不依赖延迟加载的样式。来源：https://web.dev/articles/critical-rendering-path 、Next.js官方文档CSS优化

**知识点12：字体显示策略（font-display）** — font-display:swap：立即显示fallback字体，web font加载后交换（FOUT，可能有布局偏移）。font-display:optional：fallback字体，仅当web font在100ms内可用才使用（无交换闪烁，适合性能优先）。Next.js next/font自动自托管字体、预加载、size-adjust匹配fallback字体消除布局偏移。我们已用next/font，确认所有字体都通过next/font加载而非外部<link>。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display 、Next.js next/font官方文档

**知识点13：will-change谨慎使用（内存陷阱）** — `will-change: transform`提示浏览器提前创建合成层，但每个提升的层消耗显存和内存。过度使用（给所有元素加will-change）导致内存暴涨、卡顿。规则：只给确实会动画的元素加，动画结束后移除。替代方案：直接用transform/opacity动画（浏览器自动优化），不需要will-change。对我们的framer-motion动画，检查是否滥用will-change。来源：https://developer.mozilla.org/en-US/docs/Web/CSS/will-change 、web.dev CSS性能指南

**知识点14：CSS动画性能（只动画transform和opacity）** — 只有transform和opacity在合成器线程执行（不触发layout/paint，60fps流畅）。动画width/height/top/left/margin/padding触发layout（昂贵）。动画background/box-shadow/border触发paint（中等）。规则：用transform:translateX()替代left动画，用transform:scale()替代width动画，用opacity替代visibility。framer-motion默认优化但需检查自定义动画。对我们的页面过渡和交互动画适用。来源：https://web.dev/articles/animations-and-performance 、https://developer.mozilla.org/en-US/docs/Web/Performance/CSS_JavaScript_animation_performance

**知识点15：我们的CSS性能现状与升级路径** — 现状：Tailwind v3 JIT（小CSS）、next/font（自动优化）、next/image（AVIF/WebP）。未利用：(a)长文章页（105篇）的below-fold段落可加content-visibility:auto+contain-intrinsic-size；(b)工具列表页（533工具搜索结果）的卡片可加contain:content；(c)framer-motion动画需审计是否有非合成器属性；(d)检查是否有滥用will-change；(e)Lighthouse CI已接入，可追踪CSS相关指标（TBT/CLS）变化。优先级：文章页content-visibility（P1，直接降TBT）> 卡片contain（P2）> 动画审计（P2）。来源：项目实际状态 + https://web.developers.google.cn/articles/content-visibility?authuser=1&hl=en

**落地计划**：
- 知识点1+2 → **新增P1-PERF-CONTENT-VIS-001**：长文章页（app/blog/[slug]/page.tsx）的below-fold内容区块加content-visibility:auto + contain-intrinsic-size:auto 800px，降低TBT和首屏渲染时间
- 知识点3+4 → **新增P2-PERF-CONTAIN-CARDS-001**：工具卡片组件和搜索结果卡片加contain:content（layout+paint），内部布局变化不触发整页relayout
- 知识点14+13 → **新增P2-PERF-ANIM-AUDIT-001**：审计framer-motion和自定义CSS动画，确保只动画transform/opacity，移除滥用的will-change
- 知识点9+10 → **新增P2-PERF-TAILWIND-AUDIT-001**：审计tailwind.config.ts的content路径完整性，检查动态class名拼接问题，确保生产CSS最小化
- 知识点12 → **P1-PERF-FONT-001**（已有，next/font已接入）：确认所有字体通过next/font加载，无外部Google Fonts <link>


## [2026-09-23] SEO工程化：索引覆盖率诊断与修复实战（GSC URL Inspection API / IndexNow / 软404 / 抓取预算 / 索引自动化监控）

**主题**：Google索引覆盖率是内容站流量的天花板——页面写得再好，没被索引就没有流量。当前我们有714个URL在sitemap中，iteration 85已批量提交IndexNow（HTTP 200），但实际Google索引数未知，需要系统化诊断和监控。

**知识点1：GSC URL Inspection API（索引状态诊断）** — POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect，请求体含inspectionUrl和siteUrl，返回UrlInspectionResult对象。核心字段indexingState枚举：INDEXING_ALLOWED（可索引）、BLOCKED_BY_META_TAG（noindex meta）、BLOCKED_BY_HTTP_HEADER（X-Robots-Tag noindex）、BLOCKED_BY_ROBOTS_TXT。还返回crawlState（Crawled/Not crawled）、richResultsResult（结构化数据资格）、mobileUsabilityResult。需要OAuth2 webmasters.readonly scope。可批量检查每个URL是否真的被索引。来源：https://developers.google.com/webmaster-tools/v1/urlInspection.index/UrlInspectionResult 、https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect

**知识点2：Google Indexing API v3（主动通知）** — 与URL Inspection API是两个不同API。POST https://indexing.googleapis.com/v3/urlNotifications:publish，type=URL_UPDATED或URL_DELETED。GET /v3/urlNotifications/metadata?url=查询通知状态。批量最多100 URL/请求。官方适用范围：JobPosting、BroadcastEvent、Livestream结构化数据页面；对普通页面Google不保证快速索引，但提交无害。需要service account JSON密钥（不是PAT）。来源：https://developers.google.com/search/apis/indexing-api/v3/using-api?skip_cache=true 、https://developers.google.com/search/apis/indexing-api/v3/quickstart

**知识点3：IndexNow协议（多搜索引擎即时通知）** — 微软Bing+Yandex发起的开放协议，现支持Amazon Bot、Naver、Seznam.cz、Yep等。两种提交方式：GET单URL（?url=...&key=...）或POST批量（最多10,000 URL/批，JSON body含host/key/urlList）。密钥验证：根目录放{key}.txt文件，或keyLocation参数指定路径。密钥8-128个十六进制字符。我们的key：3f7f80308bcbbd81d91bd93cdc0e1120，文件public/3f7f80308bcbbd81d91bd93cdc0e1120.txt。iteration 85已批量提交714 URL，HTTP 200。来源：https://www.indexnow.org/documentation 、https://www.indexnow.org/faq 、https://www.bing.com/indexnow/getstarted

**知识点4：IndexNow vs Google Indexing API本质区别** — IndexNow：通知Bing/Yandex/Amazon等搜索引擎，不通知Google；无配额限制；简单密钥认证；即时生效。Google Indexing API：只通知Google；官方仅限JobPosting/Event/Livestream结构化数据页面；需要service account；有配额。对普通内容页，Google主要靠sitemap提交+自然爬取，Indexing API效果有限。最佳实践：两者都用——IndexNow覆盖Bing/Yandex，sitemap+GSC覆盖Google。来源：https://www.indexnow.org/faq 、https://developers.google.com/search/apis/indexing-api/v3/using-api?skip_cache=true

**知识点5：Soft 404（软404）** — 服务器返回200 HTTP但页面内容为空/近乎空白/错误信息，Google判定为soft 404不索引。常见原因：robots.txt屏蔽了JS/CSS导致渲染失败、页面资源加载失败、JS执行错误、服务端渲染异常输出占位内容、重定向到首页但保留原URL。修复：缺失页面必须返回真实404/410状态码；确保CSS/JS不被robots.txt屏蔽；修复SSR渲染错误；不要用200+空白页代替404。对我们：需检查是否有工具页/文章页渲染出空白。来源：https://developers.google.com/search/docs/crawling-indexing/http-network-errors?hl=en 、https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors

**知识点6：抓取预算（Crawl Budget）优化** — Google按站点流行度和更新频率分配抓取预算。优化手段：(a)永久删除页面返回404/410（强烈信号不再爬取，比robots.txt屏蔽更有效——被屏蔽URL会长期留在抓取队列）；(b)消除软404；(c)修复重定向链（>3跳浪费预算）；(d)内部链接一致指向规范URL；(e)避免大量重复内容。Google官方：<1000 URL的站点通常不需要担心抓取预算。我们714 URL，预算充足，但软404和重定向链仍需修复。来源：https://developers.google.com/crawling/docs/crawl-budget 、https://developers.google.cn/search/docs/crawling-indexing/large-site-managing-crawl-budget?hl=zh-cn

**知识点7：GSC覆盖率报告四大分类** — Error（因错误未索引：服务器错误、软404、重定向错误）、Valid with warnings（已索引但有问题）、Valid（已索引）、Excluded（主动排除：noindex、canonical指向其他页、robots.txt屏蔽、重复页）。关键指标：已索引页数 / sitemap提交页数 = 索引覆盖率。低于80%需排查。我们需要用index-monitor workflow定期获取这个数据。来源：https://developers.google.com/webmaster-tools/v1/api_reference_index 、GSC Coverage报告官方文档

**知识点8：Canonicalization（规范URL）问题** — Google可能选择与你指定的canonical不同的URL作为规范版本，如果它认为另一个版本更合适。原因：跨URL重复内容、内部链接不一致、HTTP/HTTPS混用、www/非www混用、尾部斜杠不一致。后果：你想索引的URL被Excluded（canonical指向其他页）。修复：每页加self-referencing canonical；301重定向到首选版本（HTTPS+www或无www统一）；内部链接全部指向规范URL；hreflang页之间用正确canonical。来源：https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors 、Google Search Central canonical指南

**知识点9：XML Sitemap最佳实践** — 只包含可索引URL（200状态、无noindex、canonical指向自身）。每个sitemap最多50,000 URL或50MB，超过用sitemap index。提交方式：GSC Sitemaps API、robots.txt加Sitemap: https://...指令、GSC UI手动提交。sitemap中的URL不保证全部被索引，但能帮助Google发现URL。我们的sitemap.ts输出714 URL，已排除/blog/tag/*。需定期检查sitemap中是否有返回404/noindex的URL。来源：https://developers.google.com/webmaster-tools/v1/api_reference_index 、Google Search Central sitemap指南

**知识点10：robots.txt最佳实践与陷阱** — 绝对不要屏蔽CSS/JS文件（导致soft 404渲染失败）。Disallow用于真正私有/低价值页面。Allow:指令用于例外（如Disallow /admin/ 但Allow /admin/public/）。文件末尾加Sitemap: https://www.aitoolcrux.com/sitemap.xml。用GSC robots.txt Tester验证。常见错误：Disallow: / 屏蔽全站、屏蔽_next/static/（JS/CSS）、通配符使用不当。我们的robots.txt应允许所有爬取，只屏蔽真正不需要的路径。来源：https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors 、Google Search Central robots.txt指南

**知识点11：JavaScript渲染与索引延迟** — Google用WRS（Web Rendering Service）渲染JS页面，初始爬取获取HTML，渲染爬取在之后（可能延迟数小时到数天）。纯CSR页面关键内容不在初始HTML中，索引更慢。SSG/SSR页面输出完整HTML，索引更快。确保关键内容（标题、正文、结构化数据）在初始HTML中，不只在JS执行后。我们的Next.js SSG（generateStaticParams）输出完整HTML，这是优势。但需确认AdSense/GA脚本不阻塞渲染。来源：https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=fr 、Google Search Central JS SEO指南

**知识点12：IndexNow批量提交响应码** — POST https://api.indexnow.org/indexnow，JSON body {host, key, keyLocation?, urlList}。响应：200 OK（已接受）、202 Accepted（已接受但密钥尚未验证，搜索引擎会爬取key文件验证）、400 Bad Request（格式错误）、403 Forbidden（密钥无效或未验证）、422 Unprocessable Entity（URL不属于指定host）、429 Too Many Requests（频率限制）。密钥验证后后续提交直接200。我们iteration 85提交返回200，说明key已验证。来源：https://www.indexnow.org/faq 、https://www.bing.com/indexnow/getstarted 、http://www.yandex.com/support/webmaster/en/indexnow/reference

**知识点13：URL Inspection API配额限制** — Search Console API配额：URL Inspection 2,000次/天/项目，600次/60秒。Search Analytics 2,000 query units/天。我们714 URL，一次全量检查需714次调用，在日配额内，但需控制QPS（每次间隔>0.1秒）。可写脚本分批检查，输出索引状态报告（已索引/未索引/被noindex/被canonical排除/软404），每周运行一次对比变化。来源：https://developers.google.com/webmaster-tools/v1/api_reference_index 、https://googleapis.github.io/google-api-python-client/docs/dyn/searchconsole_v1.urlInspection.index.html

**知识点14：noindex vs robots.txt屏蔽的关键区别** — noindex meta/X-Robots-Tag：页面被爬取但不索引，随时间推移不再传递PageRank。robots.txt Disallow：页面完全不被爬取，但如果有外部链接指向它，仍可能出现在搜索结果中（无描述，只有URL）——因为Google没爬取就没看到noindex。要从索引中移除页面：用noindex（让Google爬取并看到noindex指令），不要用robots.txt屏蔽（屏蔽后Google无法看到noindex，页面可能残留索引）。这是常见错误。来源：https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors 、Google Search Central noindex指南

**知识点15：我们的索引现状与升级路径** — 现状：714 URL在sitemap，iteration 85批量提交IndexNow（HTTP 200），index-monitor workflow每周运行GSC API查收录数。未知：实际Google索引数、各URL索引状态、是否有软404/canonical问题。升级路径：(a)最高优先级：写脚本用URL Inspection API批量检查714 URL索引状态，输出未索引URL清单及原因；(b)修复软404（检查工具页/文章页是否有空白渲染）；(c)验证所有页面self-referencing canonical一致；(d)检查robots.txt不屏蔽CSS/JS；(e)建立每周索引状态diff监控（新增索引/丢失索引/新出现未索引）；(f)对未索引的高价值页面手动提交GSC"请求编入索引"。来源：项目实际状态 + https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect

**落地计划**：
- 知识点1+13 → **新增P1-INDEX-INSPECT-001**：写Python脚本用GSC URL Inspection API批量检查714 URL索引状态，输出未索引URL清单及原因（noindex/canonical/soft404/blocked），每周运行
- 知识点5+14 → **新增P1-INDEX-SOFT404-001**：排查并修复软404页面——检查所有工具页/文章页/分类页是否返回空白内容，确保缺失页面返回真实404
- 知识点8+9 → **新增P2-INDEX-CANONICAL-001**：验证所有页面self-referencing canonical一致性，修复内部链接指向非规范URL的问题
- 知识点10 → **新增P2-INDEX-ROBOTS-001**：审计robots.txt，确保不屏蔽_next/static/（CSS/JS），添加Sitemap指令，用GSC Tester验证
- 知识点15 → **新增P1-INDEX-MONITOR-002**：建立每周索引状态diff监控（URL Inspection API全量扫描+对比上周），发现丢失索引的页面立即告警


## [2026-09-23] GitHub Actions自动化：高级模式与最佳实践（Reusable Workflows / Matrix / Concurrency / OIDC / Artifact / Cache）

**主题**：GitHub Actions从基础CI/CD升级到高级模式——可复用工作流、矩阵构建、并发控制、OIDC无密钥认证、制品管理、缓存策略、Monorepo优化。当前我们有3个workflow（uptime-monitor/index-monitor/lighthouse-ci），均为基础模式，可应用高级模式优化。

**知识点1：Reusable Workflows（可复用工作流）** — 用`on: workflow_call`定义可被其他workflow调用的工作流，支持inputs/outputs/secrets传递。调用方用`jobs.<job_id>.uses: owner/repo/.github/workflows/file.yml@ref`。与composite action的区别：reusable workflow是完整job级复用（含runs-on、权限、超时），composite action是step级复用。可与matrix组合（matrix调用reusable workflow传入不同inputs）。最佳实践：将通用setup（Python/Node安装+缓存）抽为reusable workflow，避免每个workflow重复写。来源：https://docs.github.com/en/actions/how-tos/sharing-automations/reusing-workflows

**知识点2：Matrix Builds（矩阵构建）** — `strategy.matrix`定义变量组合，自动创建多个并行job运行。支持`include`（添加特定组合）和`exclude`（排除特定组合）。`fail-fast: true`（默认）时一个matrix job失败则取消所有其他job；设为false可让所有组合跑完。`max-parallel`限制最大并发数。典型用途：多Node版本测试、多OS测试、多浏览器E2E。对我们的用途：lighthouse-ci可用matrix同时跑desktop和mobile preset。来源：https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions 、https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python

**知识点3：Concurrency Control（并发控制）** — `concurrency.group`确保同一组内最多1个运行中+1个等待中。`cancel-in-progress: true`会取消同组正在运行的旧job，只保留最新的。典型用法：`concurrency: group: ci-${{ github.ref }}, cancel-in-progress: true`——同一分支推送时取消旧的CI运行，节省分钟数。部署场景：`group: deployment, cancel-in-progress: false`——确保部署串行不重叠。对我们：uptime-monitor每10分钟运行一次，若上次未完成应跳过而非并发。来源：https://docs.github.com/en/actions/tutorials/deploying-with-github-actions 、https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

**知识点4：Deployment Environments（部署环境）** — `jobs.<job_id>.environment: production`将job关联到GitHub环境。环境可配置protection rules：required reviewers（手动审批）、wait timer（延迟N分钟）、deployment branch（只允许特定分支部署）。每次部署会在GitHub UI生成deployment记录（含状态、关联commit、审批人）。环境级secrets只在引用该环境的job中可用。对我们：如果未来加自动部署workflow，可用environment+manual approval防止误部署。来源：https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments

**知识点5：OIDC Federated Authentication（无密钥云认证）** — `permissions: id-token: write`让GitHub OIDC provider签发JWT，云服务商（AWS/GCP/Azure）验证JWT后颁发短期临时token，完全替代长期secret。JWT包含sub（repo:owner/repo:ref:refs/heads/main）、aud、iss等claims，云端trust policy可精确限制哪个repo/branch/环境能assume role。npm trusted publishing也用OIDC（无需npm token）。对我们：当前用GitHub PAT（长期密钥）提交代码，OIDC不适用GitHub API，但如果未来部署到AWS/GCP必须用OIDC。来源：https://docs.github.com/en/actions/reference/security/oidc 、https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers

**知识点6：Artifacts v4（制品管理）** — `actions/upload-artifact@v4`将构建产物打包为单个zip（内存中组装+流式上传+checksum校验），比v3的多文件上传快很多。`actions/download-artifact@v4`在后续job下载。制品默认保留90天（可配置retention-days），公共仓库免费。关键区别：artifact是"这次构建产出了什么"（dist/测试报告/覆盖率），在job间传递；cache是"依赖安装结果"（node_modules），跨workflow run复用。对我们：lighthouse-ci可上传HTML报告为artifact，失败时可下载查看。来源：https://github.blog/2024-02-12-get-started-with-v4-of-github-actions-artifacts/ 、https://blog.csdn.net/diandianxiyu/article/details/161273835

**知识点7：Cache策略（actions/cache@v4）** — 缓存依赖目录（~/.npm、node_modules、~/.cache/pip），key用`${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}`——lockfile变化时自动失效。`restore-keys`提供前缀匹配回退（如`${{ runner.os }}-node-`），即使精确key未命中也能恢复部分缓存。每仓库10GB配额，超出后LRU淘汰；7天无访问自动清除。缓存命中时near-instant恢复，miss时在job结束时自动保存。对我们：Python workflow可缓存pip包，Node workflow可缓存~/.npm。来源：https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows 、https://env.dev/guides/github-actions-guide

**知识点8：Cache vs Artifact的本质区别** — Cache：跨workflow run复用（同一分支多次push），用于依赖安装结果，有配额和过期策略，命中不命中是正常的。Artifact：同一workflow run内job间传递（build job→deploy job），用于构建产物，必须可靠下载，有保留期。不要把构建产物塞进cache（cache可能被evict导致下游job失败），也不要把依赖塞进artifact（每次run都重新上传下载浪费时间）。来源：https://blog.csdn.net/diandianxiyu/article/details/161273835 、https://www.wasilzafar.com/pages/series/software-engineering/deep-dive-github-actions-05-data-sharing-optimization.html

**知识点9：Monorepo CI优化** — 大Monorepo不应每次push跑全部测试。方案：(a)`paths-filter` action检测变更文件路径，只运行受影响包的测试；(b)Nx/Turborepo的`affected`命令（基于依赖图计算哪些包受影响）；(c)pnpm workspace + `--filter`。缓存策略：缓存各包的dist和.tsbuildinfo（TypeScript增量编译信息），key包含源码hash。对我们：当前是单包Next.js项目不适用，但如果未来拆Monorepo需用这些模式。来源：https://blog.dominicrodemer.com/github-actions-optimization-and-performance/ 、https://www.warpbuild.com/blog/github-actions-monorepo-guide

**知识点10：Workflow Permissions（最小权限原则）** — `permissions:`可在workflow级或job级设置GITHUB_TOKEN的scope（contents: read/write, issues: read, pull-requests: write, id-token: write等）。默认GITHUB_TOKEN对public仓库是read-all，对private是write-all。最佳实践：workflow级设`permissions: contents: read`，需要写的job单独覆盖（如`permissions: contents: write`用于提交代码）。不要用`permissions: write-all`——一个被注入的step就能改代码、删release、改环境。对我们：提交代码的job需要contents: write，其他job只需read。来源：https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions 、http://raw.githubusercontent.com/github/awesome-copilot/main/instructions/github-actions-ci-cd-best-practices.instructions.md

**知识点11：Secrets管理三层体系** — (1)Repository secrets：单仓库可用，最常用；(2)Organization secrets：组织内多仓库共享，可设可见性（all repos/private repos/selected repos）；(3)Environment secrets：只在引用特定environment的job中可用，配合deployment protection rules。Secrets在log中自动mask（`***`），但如果secret被echo到变量再输出可能绕过mask——永远不要`echo $SECRET`。Secrets不能在`if:`条件中直接使用（安全限制）。对我们：GitHub PAT存在repo secret，告警邮箱可存organization secret。来源：https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

**知识点12：Composite Actions vs Reusable Workflows选择** — Composite action（`using: composite`）：step级复用，可在同一job内多次调用，不能设runs-on/timeout/permissions，适合"安装依赖+配置环境"类步骤集合。Reusable workflow：job级复用，完整job定义（含runs-on、权限、超时、并发），适合"完整测试流程""完整部署流程"。经验法则：如果复用单元需要独立的runner环境或权限，用reusable workflow；如果只是几步操作的组合，用composite action。对我们：Python环境安装（setup-python+pip cache+依赖安装）可抽为composite action。来源：https://docs.github.com/en/actions/how-tos/sharing-automations/reusing-workflows

**知识点13：Conditional Execution（条件执行）** — `if:`表达式控制step/job是否运行，可用`needs.<job_id>.outputs`、`github.event_name`、`success()/failure()/always()/cancelled()`等函数。`needs`定义job依赖关系，默认只有上游全部success才运行下游。`if: always()`即使上游失败也运行（用于清理/上传报告）。`if: failure()`只在上游失败时运行（用于告警）。`continue-on-error: true`让job失败不阻断后续。对我们：uptime-monitor失败时可触发发邮件step（`if: failure()`）。来源：https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

**知识点14：Timeout与重试策略** — `timeout-minutes`在job级设置最大运行时间（默认360分钟=6小时），防止挂起job浪费分钟数。建议CI job设15-30分钟，部署job设60分钟。step级无原生retry，需用`nick-fields/retry` action或shell循环实现。`continue-on-error: true`标记实验性job（失败不影响整体状态）。对我们：uptime-monitor的Python脚本应设timeout-minutes: 5，防止网络挂起占着runner。来源：https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions 、http://raw.githubusercontent.com/github/awesome-copilot/main/instructions/github-actions-ci-cd-best-practices.instructions.md

**知识点15：我们的Workflows现状与升级路径** — 当前3个workflow：(1)uptime-monitor.yml（每10分钟Python curl，已修复httpx→urllib）；(2)index-monitor.yml（每周一GSC API）；(3)lighthouse-ci.yml（每周一Lighthouse）。升级机会：(a)所有workflow加`concurrency`防止并发重叠；(b)抽composite action复用Python setup+pip cache；(c)lighthouse-ci加matrix（desktop+mobile）+upload-artifact保存HTML报告；(d)uptime-monitor加`if: failure()`发邮件告警step；(e)所有第三方action锁定commit SHA（iteration 83已做actions/checkout和setup-python）；(f)加`timeout-minutes`防止挂起。来源：项目实际workflow文件 + https://docs.github.com/en/actions/how-tos/sharing-automations/reusing-workflows

**落地计划**：
- 知识点3+14 → **新增P2-CI-CONCURRENCY-001**：为所有3个workflow添加concurrency控制（cancel-in-progress: true for CI, false for monitor）和timeout-minutes
- 知识点2+6 → **新增P2-CI-LIGHTHOUSE-MATRIX-001**：lighthouse-ci加matrix（desktop+mobile preset），用upload-artifact@v4保存HTML报告
- 知识点12+7 → **新增P2-CI-COMPOSITE-SETUP-001**：创建composite action复用Python setup+pip cache，uptime-monitor和index-monitor共用
- 知识点13 → **新增P2-CI-UPTIME-ALERT-001**：uptime-monitor失败时触发`if: failure()`发邮件告警step（当前只curl不告警）
- 知识点10 → **P1-CI-PIN-001**（已有，iteration 83完成）：第三方action锁定commit SHA已完成，后续新workflow继续遵守


## [2026-09-23] 高星GitHub开源工具：Web性能监控与RUM（真实用户监控）工具链深度对比

**主题**：RUM（Real User Monitoring）采集真实用户的Core Web Vitals数据，与实验室数据（Lighthouse）互补。当前我们已有Umami+GA4+WebVitalsReporter(仅console.log)，关键缺口是生产环境CWV数据未上报。

**知识点1：web-vitals库（Google官方）** — GitHub GoogleChrome/web-vitals，~8k星，~1KB gzip。提供onLCP/onINP/onCLS/onFCP/onTTFB回调。标准build（'web-vitals'）只报告指标值；attribution build（'web-vitals/attribution'）额外提供interactionTargetElement/inputDelay/processingDuration/presentationDelay/longAnimationFrameEntries/loadState。v4.x是当前稳定版。用法：import {onINP} from 'web-vitals/attribution'; onINP(metric => sendToAnalytics(metric))。来源：https://www.npmjs.com/package/web-vitals 、https://codelabs.developers.google.com/measuring-inp?hl=en

**知识点2：web-vitals上报最佳实践：navigator.sendBeacon** — 用navigator.sendBeacon(url, JSON.stringify(metric))而非fetch上报，因为sendBeacon在页面unload时仍能可靠发送（浏览器保证完成），异步非阻塞，数据量限制<64KB。也可在visibilitychange事件中批量上报。GA4集成：gtag('event', 'web_vitals', {metric_id, metric_value, metric_target})作为自定义事件。自建端点：POST /api/rum，后端存BigQuery/PostgreSQL。来源：https://codelabs.developers.google.com/codelabs/web-vitals-google-analytics-bigquery 、https://blog.redlinesoft.net/posts/core-web-vitals-diagnosing-performance-2026/

**知识点3：Sentry前端性能监控** — GitHub getsentry/sentry-javascript SDK ~7.6k星，Sentry主仓库39k+星。SDK v8.x默认启用INP采集（enableInp: true）。自动采集LCP/INP/CLS/FCP/TTFB，与错误追踪、Session Replay、分布式追踪联动。从指标到根因的完整链路：Web Vitals模块→trace waterfall→session replay→code profiling。Next.js专用SDK @sentry/nextjs自动instrumentation。免费版5000 errors/月，性能监控需付费plan。来源：https://sentry.io/solutions/real-user-monitoring-rum/ 、https://docs.sentry.io/platforms/javascript/guides/nextjs/tracing/instrumentation/automatic-instrumentation/

**知识点4：Sentry Session Replay** — 录制用户会话（DOM快照+控制台日志+网络请求+鼠标移动），与错误和性能指标关联。可在INP慢的交互时回看用户实际操作。隐私保护：默认mask所有文本和输入框，可配置mask/block/unmask选择器。SDK v8+默认集成。对内容站价值：诊断"用户点击CTA无响应""菜单打不开"类难以复现的问题。采样率建议：生产环境10-30%采样，避免数据量过大。来源：https://sentry.io/for/frontend/ 、https://geekflare.com/guides/frontend-error-monitoring-tools/

**知识点5：OpenReplay（开源Session Replay）** — GitHub openreplay/openreplay，~12.1k星（2026年6月）。开源Session Replay平台，可完全自托管。录制DOM变化、网络请求、控制台、鼠标移动、滚动。与Sentry Replay相比：完全自托管、数据不出服务器、无事件量限制、MIT/Elastic双授权。插件系统：可集成Redux/Vuex/NgRx状态、Fetch/XHR、GraphQL。缺点：需维护基础设施（PostgreSQL+MinIO+Redis），初始搭建成本高。来源：https://temps.sh/blog/privacy-first-analytics-and-session-replay-platforms-2026 、https://posthog.com/blog/best-open-source-analytics-tools

**知识点6：Plausible Analytics** — GitHub plausible/analytics，~24k星。AGPL-3.0许可，轻量级脚本<1KB，无cookie，GDPR合规无需cookie横幅。自托管需PostgreSQL+ClickHouse双数据库，内存~1.8GB。云版$9/月起无免费层。特点：实时仪表盘、UTM追踪、目标转化、出口链接追踪。自托管版不支持session replay和funnel（云版独有）。高流量性能优秀（ClickHouse列存储），适合>10M事件/月。来源：https://openpanel.dev/articles/self-hosted-web-analytics 、https://use-apify.com/blog/plausible-vs-umami-2026

**知识点7：Umami Analytics（我们已在用）** — GitHub umami-software/umami，~35k星（最高星开源analytics）。MIT许可（最宽松），Node.js+Next.js+PostgreSQL单数据库，内存~400MB。脚本~2KB。多站点、事件追踪、自定义事件。免费云版（有限额）。我们的website ID: 7d417a27-1151-407a-9bbb-ef8dd10189a2。缺点：无funnel、无session replay、高流量(>10M事件/月)时PostgreSQL性能瓶颈。v2.x 2025年中成熟稳定。来源：https://haloy.dev/blog/self-hosted-analytics-compared 、https://phpwebthings.org/plausible-vs-umami-vs-ackee-2026/

**知识点8：PostHog（全功能产品分析）** — GitHub PostHog/posthog，~22k星。全功能平台：产品分析+session replay+feature flag+A/B测试+web analytics。核心MIT，高级功能ELv2。自托管需Kafka+PostgreSQL+Redis+ClickHouse（重基础设施）。云版免费1M事件/月。对内容站功能过剩，但如果未来做SaaS产品/工具交互功能可考虑。与Umami/Plausible的区别：PostHog是产品分析（用户行为路径），Umami/Plausible是web analytics（页面浏览统计）。来源：https://posthog.com/blog/best-open-source-analytics-tools 、https://dev.to/enfernandes/self-hosted-analytics-in-2026-ditch-ga4-for-umami-plausible-or-posthog-28n9

**知识点9：Lighthouse CI（实验室数据）** — GoogleChrome/lighthouse-ci，~6.5k星。在CI中运行Lighthouse，支持性能预算断言（assertions）、历史趋势对比、上传到Lighthouse CI Server。我们已在iteration 85添加.lighthouserc.json（desktop preset）和.github/workflows/lighthouse-ci.yml（每周一运行）。assertions可设性能/可访问性/SEO/最佳实践分数阈值，低于阈值CI失败。与RUM互补：Lighthouse是受控环境实验室数据，RUM是真实用户数据。来源：https://github.com/GoogleChrome/lighthouse-ci 、https://web.dev/articles/lighthouse-ci

**知识点10：Sitespeed.io（完整性能监控链）** — GitHub sitespeedio/sitespeed.io，~4.8k星。完整网站性能监控工具链：Browsertime（浏览器计时）+ Coach（性能建议）+ PageXray（资源分析）+ Graphite/InfluxDB（时序存储）+ Grafana（仪表盘）。Docker一键运行，可监控多URL性能趋势。比Lighthouse更全面：第三方请求分析、DNS/TCP/SSL计时、视频录制、CPU/内存采集。适合持续性能监控，但基础设施较重（需时序数据库+Grafana）。来源：https://github.com/sitespeedio/sitespeed.io 、https://cssauthor.com/best-frontend-performance-monitoring-tools/

**知识点11：RUM vs 实验室数据的互补关系** — 实验室数据（Lighthouse/PageSpeed Insights/WebPageTest）：受控环境、可复现、调试方便，但不代表真实用户（固定设备/网络/无广告拦截器）。RUM（web-vitals/Sentry/Umami）：真实设备/网络/用户行为，但调试困难（需attribution定位）。最佳实践：两者结合——Lighthouse CI在PR时防止性能退化（回归测试），RUM在生产中发现真实用户遇到的问题（长尾设备/弱网）。CrUX（Chrome User Experience Report）是Google的RUM数据集，PageSpeed Insights的"真实用户数据"即来自CrUX，覆盖Chrome用户。来源：https://web.dev/articles/why-lab-data-doesnt-match-field-data 、https://sentry.io/solutions/real-user-monitoring-rum/

**知识点12：Core Web Vitals阈值与p75百分位** — 所有CWV指标以p75（第75百分位数）为评判标准：LCP≤2.5s好，>4s差；INP≤200ms好，>500ms差；CLS≤0.1好，>0.25差。p75意味着75%的用户体验达到该值以下。绝对不要用平均值（mean）——平均值会被极端值严重扭曲（一个10秒的LCP会拉高整体均值）。RUM采集时保留原始数据，在后端/数据仓库计算p75。Google Search Console的CWV报告也是p75。来源：https://web.dev/articles/defining-core-web-vitals-thresholds 、https://web.dev/articles/vitals

**知识点13：INP RUM采集特殊考虑** — INP报告所有交互中最差的那个（或接近最差，忽略极端离群值），不是平均值。onINP回调在页面生命周期中可能多次触发（每次有更差的交互时更新metric.value）。attribution build的interactionTarget可能为null（交互元素已被移除，或事件持续时间低于浏览器最小报告阈值）。loadState字段指示交互发生时页面加载状态（'loading'/'dom-ready'/'complete'）——启动期INP问题通常loadState='loading'，说明页面还在水合时用户已开始交互。来源：https://web.dev/articles/optimize-fid?hl=zh-cn 、https://webperfclinic.com/da/article/rum-med-web-vitals-js-2026-feltdata-guide

**知识点14：隐私合规与RUM** — GDPR/CCPA要求：不采集个人身份信息(PII)。web-vitals默认不采集PII（只采集指标值和CSS选择器）。Sentry/OpenReplay必须配置mask选项避免录制敏感信息（密码、信用卡、个人数据）——Sentry默认mask所有文本，OpenReplay需手动配置。无cookie分析（Plausible/Umami）无需cookie横幅。CSP头必须允许RUM端点域名（我们的CSP已允许analytics.umami.is和googletagmanager/google-analytics）。如果添加Sentry需在CSP中加sentry.io。来源：https://sentry.io/for/frontend/ 、https://openpanel.dev/articles/self-hosted-web-analytics

**知识点15：我们的RUM现状与升级路径** — 当前：Umami（页面浏览+自定义事件）+ GA4（页面浏览+事件）+ WebVitalsReporter（仅console.log打印LCP/INP/CLS，未上报到任何后端）。关键缺口：生产环境无法收集真实用户CWV数据，只能依赖Lighthouse实验室数据和GSC的CrUX汇总数据（延迟28天）。升级路径：(a)最高优先级：WebVitalsReporter改为attribution build+sendBeacon上报到GA4自定义事件（零成本，利用已有GA4）；(b)中期：评估Sentry（错误追踪+INP归因+session replay，免费版够用）或OpenReplay（自托管replay）；(c)Lighthouse CI已在CI中运行（每周一）。来源：项目实际状态 + https://codelabs.developers.google.com/codelabs/web-vitals-google-analytics-bigquery

**落地计划**：
- 知识点1+2+13 → **P1-PERF-INP-001**（已有）：升级WebVitalsReporter到attribution build，用sendBeacon上报INP/LCP/CLS到GA4自定义事件，包含interactionTarget/inputDelay/processingDuration/presentationDelay/loadState
- 知识点12+15 → **新增P1-PERF-RUM-001**：搭建生产环境RUM数据采集闭环——WebVitalsReporter上报GA4，在GA4中创建CWV仪表板（p75 LCP/INP/CLS按页面分组），每周review最差的5个页面
- 知识点3+4 → **新增P2-MONITOR-SENTRY-001**：评估Sentry免费版接入——错误追踪+INP归因+session replay（10%采样），需在CSP加sentry.io，需npm install @sentry/nextjs
- 知识点5 → **新增P2-MONITOR-OPENREPLAY-001**：评估OpenReplay自托管session replay可行性（Docker部署，与Sentry对比成本/隐私/维护），作为Sentry的开源替代方案


## [2026-09-23] Core Web Vitals INP深度优化实战（Interaction to Next Paint）

**主题**：INP于2024年3月正式替代FID成为Core Web Vital，测量用户交互到下一次绘制的延迟。好阈值≤200ms(p75)，需改善200-500ms，差>500ms。

**知识点1：INP三阶段分解** — INP = input delay（输入延迟，其他代码阻塞主线程）+ processing duration（事件处理器执行+虚拟DOM diff+状态更新）+ presentation delay（浏览器布局/绘制延迟）。优化必须针对具体阶段，不能笼统说"减少JS"。来源：https://web.dev/articles/optimize-fid?hl=zh-cn

**知识点2：INP的关键误解** — INP不要求200ms内完成全部渲染，只要求浏览器有机会paint。如果先await fetch再阻塞主线程1秒，INP可能完美（因为await期间浏览器已paint）。关键是"给浏览器机会响应用户输入"，而非"200ms内做完所有事"。来源：https://vercel.com/blog/demystifying-inp-new-tools-and-actionable-insights

**知识点3：长任务(>50ms)是INP头号敌人** — 主线程被超过50ms的任务占据时，用户交互的input delay会飙升。解决方案是分片(chunking)：将大循环/大计算拆成小片段，每片之间让出主线程。来源：https://web.developers.google.cn/articles/top-cwv

**知识点4：scheduler.yield() 新API** — Chrome 115+支持的scheduler.yield()比setTimeout(0)更优，它让浏览器在分片之间优先处理高优先级任务（如用户输入、动画帧）。Firefox/Safari需polyfill。用法：for循环中每N次迭代后await scheduler.yield()。来源：https://web.dev/articles/optimize-fid?hl=zh-cn

**知识点5：React startTransition/useTransition** — React 18+的startTransition将状态更新标记为非紧急，React可以中断渲染以响应用户输入。这是React/Next.js应用优化INP的首选方案，适用于搜索筛选、标签切换、列表过滤等会触发大量重渲染的交互。来源：https://www.toolsku.com/en/blog/nextjs-app-router-performance-2026/

**知识点6：Vercel await-interaction-response模式** — 先设置即时反馈状态（loading/selected高亮），await interactionResponse()（内部requestAnimationFrame+setTimeout 0，平均延迟8ms），再执行昂贵操作。确保用户在1帧内得到确认，昂贵操作在paint后执行。npm包：await-interaction-response。来源：https://vercel.com/blog/demystifying-inp-new-tools-and-actionable-insights

**知识点7：web-vitals attribution build** — 从'web-vitals/attribution'导入onINP（而非'web-vitals'），可获得attribution对象：interactionTargetElement（被点击的DOM元素）、interactionType（pointer/keyboard）、inputDelay、processingDuration、presentationDelay、processedEventEntries、longAnimationFrameEntries。这是定位慢交互的关键数据。来源：https://codelabs.developers.google.com/measuring-inp?hl=en

**知识点8：Long Animation Frames (LoAF) API** — Chrome 123+，PerformanceObserver type='long-animation-frame'，捕获超过50ms的动画帧，包含scripts数组（每个脚本的duration/invoker/functionName/sourceURL）。与INP归因联动，可精确定位是哪段脚本导致了慢交互。来源：https://developer.chrome.google.cn/docs/web-platform/long-animation-frames

**知识点9：第三方JS是INP常见元凶** — analytics、广告、A/B测试、聊天组件在主线程执行长任务。解决方案：(a)延迟加载第三方脚本（next/script strategy='lazyOnload'）；(b)联系供应商修复（Vercel团队曾联系Heap修复）；(c)使用partytown将第三方脚本移到Web Worker。来源：https://vercel.com/blog/demystifying-inp-new-tools-and-actionable-insights

**知识点10：浏览器渲染阶段优化** — CSS containment（contain: layout style paint）限制重排范围；虚拟列表减少实际DOM大小；动画只改opacity/transform走GPU合成层（不触发布局）；内联SVG替换为<img src>减少DOM节点数。浏览器布局算法是O(n)，DOM越大重排越慢。来源：https://vercel.com/blog/demystifying-inp-new-tools-and-actionable-insights

**知识点11：React重渲染优化** — React.memo/useMemo/useCallback减少虚拟DOM diff；不可变context/props值避免子树不必要重渲染；缩小'use client'边界，尽量用Server Components（RSC不发送JS到客户端，从根源减少主线程工作）。来源：https://tomodahinata.com/blog/core-web-vitals-nextjs-inp-lcp-cls-optimization-guide

**知识点12：INP测量工具链** — (a)Chrome DevTools Performance面板Interactions track，开启CPU throttling 4x模拟移动设备；(b)web-vitals库RUM真实用户监控；(c)Vercel Speed Insights显示慢交互的CSS selector；(d)PageSpeed Insights实验室数据。注意：CPU throttling下第一次交互可能异常慢，忽略即可再点一次。来源：https://vercel.com/blog/demystifying-inp-new-tools-and-actionable-insights

**知识点13：页面启动期INP问题** — 页面还在"热身"（解析/编译/执行JS、水合）时用户开始交互，input delay特别高。解决方案：减少初始JS bundle、路由级代码分割、动态导入重组件（next/dynamic）、SSG/SSR减少客户端水合时间、preload关键资源。来源：https://pagevitals.com/academy/interaction-to-next-paint/

**知识点14：事件处理器优化** — 避免在click handler中同步执行重计算/重渲染；先给即时视觉反馈再做重活；debounce高频事件（scroll/resize/input/keydown）；避免强制同步布局（forced synchronous layout/layout thrashing）——即在同帧内交替读写DOM样式。来源：https://opsblu.com/blog/understanding-inp-interaction-to-next-paint-guide

**知识点15：QuintoAndar案例：INP降低80%转化提升36%** — 巴西房产平台QuintoAndar通过RUM监控+async/defer第三方脚本+代码分割，将INP降低80%，转化同比提升36%。证明INP优化直接影响商业指标，不是纯技术指标。来源：https://web.developers.google.cn/case-studies/quintoandar-inp

**落地计划**：
- 知识点7+8+12 → **P1-PERF-INP-001**：升级WebVitalsReporter到web-vitals/attribution build，采集interactionTarget/inputDelay/processingDuration/presentationDelay，上报到GA4自定义维度
- 知识点5+6 → **新增P1-PERF-INP-003**：搜索页(SearchBox)和筛选交互应用startTransition，避免大列表重渲染阻塞输入
- 知识点9 → **新增P2-PERF-INP-004**：审计第三方脚本（GA4/Umami/AdSense/Baidu）加载策略，确认全部使用lazyOnload，评估partytown可行性
- 知识点14 → **P2-PERF-INP-001**：高频事件处理器（搜索input、移动端菜单）加debounce，避免layout thrashing
- 知识点13 → **P1-PERF-SUSPENSE-001**：非关键博客/工具页数据用Suspense包裹，静态HTML shell先发送，减少启动期主线程阻塞


[2026-09-23] 高星GitHub开源工具：前端自动化测试工具链（Playwright + Vitest + React Testing Library + MSW）

知识点1：Playwright——Microsoft开源的E2E测试框架（GitHub microsoft/playwright，超65k星）。支持Chromium/Firefox/WebKit三大引擎，核心优势是自动等待和重试能力（auto-waiting + retry-ability）。内置trace viewer（时间旅行调试）、codegen（录制生成测试）、network interception（网络拦截）。官方最佳实践：使用locators而非CSS选择器，使用web-first assertions，使用Playwright Tooling，跨浏览器测试，保持依赖更新，在CI运行，lint测试代码。（来源：https://playwright.dev/docs/best-practices 、https://devblogs.microsoft.com/blog/the-complete-playwright-end-to-end-story-tools-ai-and-real-world-workflows）

知识点2：Playwright Locators——定位元素的首选方式，自带自动等待和重试。查询优先级：role locator（page.getByRole('button', {name: 'Submit'})）> text locator（getByText）> placeholder/label/alt text > test id（getByTestId）。getByRole最推荐，因为它查询可访问性树，同时验证可访问性。避免使用脆弱的CSS类选择器（如.btn-primary-123）和XPath——类名变化会导致测试失败，而用户不关心类名。（来源：https://playwright.dev/docs/best-practices 、http://raw.githubusercontent.com/Hack23/euparliamentmonitor/HEAD/e2e/README.md）

知识点3：Playwright Web-First Assertions——expect(locator).toHaveText()/toBeVisible()/toBeEnabled()/toHaveAttribute()等断言会自动等待条件满足，超时默认5秒。与传统assert（立即断言，不等待）不同，web-first assertions会重试直到条件满足或超时。这消除了手动sleep/waitForSelector的需要。关键原则：不要在断言前手动等待，让web-first assertions处理等待。反模式：await page.waitForTimeout(3000)——固定等待既慢又不稳定。（来源：https://playwright.dev/docs/best-practices 、https://playwright.dev/docs/test-assertions）

知识点4：Playwright Trace Viewer——录制测试执行的完整轨迹（DOM快照、网络请求、控制台日志、截图、视频、source位置）。配置选项：trace: 'on-first-retry'（仅在第一次重试时录制，平衡性能和可调试性，官方推荐）、'retain-on-failure'（失败时保留）、'on'（全部录制，最慢）、'off'。测试失败后用npx playwright show-trace trace.zip打开，可时间旅行查看每个步骤的DOM状态和网络请求。比单独的截图/视频更强大——可查看失败时刻的完整DOM和console错误。（来源：https://devblogs.microsoft.com/blog/the-complete-playwright-end-to-end-story-tools-ai-and-real-world-workflows 、https://playwright.dev/docs/trace-viewer）

知识点5：Playwright认证与多角色——storageState API可保存登录状态（cookies + localStorage + sessionStorage），在多个测试间复用，避免每个测试重新登录。支持多角色测试（admin用户和普通用户同时操作，测试权限隔离和实时协作）。标准流程：globalSetup中登录并保存storageState到playwright/.auth/user.json，test.use({ storageState: 'playwright/.auth/user.json' })加载。敏感信息（用户名/密码）用环境变量或GitHub Secrets，不硬编码。.auth/目录应加入.gitignore。（来源：https://playwright.dev/docs/auth 、https://learn.microsoft.com/en-us/power-platform/developer/playwright-samples/cicd）

知识点6：Vitest——Vite原生的单元测试框架（GitHub vitest-dev/vitest，超13k星）。与Vite配置共享（transform、resolve、plugins、alias），启动极快（ESM原生、按需编译、HMR支持）。兼容Jest API（describe/test/it/expect/vi.fn/vi.mock/vi.spyOn/beforeEach/afterEach），可从Jest渐进迁移。支持happy-dom（更快）或jsdom作为DOM环境。Vitest 5.0已发布（2026-09-16），增强browser mode（真实浏览器中运行测试）、component testing、workspace monorepo支持、workspace继承。（来源：https://vitest.dev/guide/features 、https://main.vitest.dev/blog/vitest-5 、https://v3.vitest.dev/guide/mocking）

知识点7：Vitest Mocking最佳实践——vi.fn()创建mock函数，vi.mock()模拟模块（自动hoisted，在所有import前执行，因此不能引用外部变量除非用vi.hoisted），vi.spyOn()监视现有方法。关键：每个测试后清除/重置mock（mockClear清除调用记录、mockReset清除+重置实现、mockRestore恢复原始实现），避免mock状态在测试间泄漏。对于HTTP请求，Vitest官方推荐使用MSW而非直接mock fetch——MSW拦截网络层，测试代码不变，更贴近真实行为。不要过度mock：只mock慢的/非确定性的依赖（网络、文件系统、数据库、当前日期、随机数），纯逻辑不要mock。（来源：https://vitest.dev/guide/mocking 、https://main.vitest.dev/guide/learn/testing-in-practice 、https://cn.vitest.dev/guide/mocking/requests.html）

知识点8：React Testing Library——测试React组件的标准库（GitHub testing-library/react-testing-library，超19k星）。核心哲学：测试用户看到的行为，而非实现细节——不直接测试state、不测试props传递、不测试内部方法、不查询组件实例。查询优先级：getByRole > getByLabelText > getByPlaceholderText > getByText > getByDisplayValue > getByAltText > getByTitle > getByTestId。所有helper（render/fireEvent/waitFor）自动包裹在React act()中，确保React状态更新完成后再断言，避免"not wrapped in act()"警告。（来源：https://testing-library.com/docs/queries/about/ 、https://testing-library.com/docs/react-testing-library/setup/ 、https://legacy.reactjs.org/docs/testing-recipes.html）

知识点9：user-event vs fireEvent——@testing-library/user-event是推荐的用户交互模拟库，v14是完全重写版本。user-event模拟真实浏览器完整事件序列（如打字：focus→keydown→keypress→input→change→keyup），而fireEvent只dispatch单个合成事件（fireEvent.change只触发change）。必须在测试顶部调用const user = userEvent.setup()获取初始化实例，然后await每个交互（await user.type(input, 'hello')、await user.click(button)）。差异不是表面的——fireEvent.change(input)不会触发focus和完整键盘事件，可能遗漏依赖focus状态的bug。新项目统一用user-event，不用fireEvent。（来源：https://techoral.com/react/react-testing-library.html 、https://scrimba.com/articles/how-to-test-react-apps-2026/ 、https://testing-library.com/docs/user-event/intro）

知识点10：MSW（Mock Service Worker）——API mocking库（GitHub mswjs/msw，超17k星），通过Service Worker（浏览器环境）或Node.js undici interceptor（测试环境）拦截网络请求。MSW 2.0使用新API：http.get(url, resolver)/http.post()/HttpResponse.json(data)替代旧的rest.get()/res(ctx.json())。支持REST和GraphQL（graphql.query('OperationName', resolver)按operation name匹配而非URL）。标准测试生命周期：beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))、afterEach(() => server.resetHandlers())、afterAll(() => server.close())。onUnhandledRequest: 'error'确保未mock的请求报错，防止测试意外调用真实API。（来源：https://qaskills.sh/blog/msw-mock-service-worker-guide 、https://qaskills.sh/blog/msw-api-mocking-guide 、https://cn.vitest.dev/guide/mocking/requests.html）

知识点11：测试金字塔——Mike Cohn提出的经典模型：单元测试（最多，最快，毫秒级，测试纯函数和组件隔离逻辑）> 集成测试（中等，测试组件组合和API交互）> E2E测试（最少，最慢，秒级，测试完整用户流程）。原始比例约70/20/10。常见反模式：冰淇淋蛋筒（E2E最多，单元测试最少）——维护成本极高、运行慢、失败原因不明确（是UI bug？API bug？网络问题？测试环境问题？）。对于Next.js SSG内容站：单元测试工具函数（slug生成、日期格式化、schema构建、CTA链接构建）、集成测试关键组件（CTA按钮、FAQ schema渲染、对比表格）、E2E测试关键用户流程（首页加载→工具详情→点击CTA）。（来源：https://main.vitest.dev/guide/learn/testing-in-practice 、https://testing-library.com/docs/react-testing-library/faq）

知识点12：测试覆盖率的正确使用——覆盖率是健康指标不是目标。100%行覆盖率不代表测试质量好（可能只测试了无意义的getter/setter和默认渲染）。关注关键路径覆盖率：用户核心流程、错误处理、边界条件。可用Istanbul/Cobertura格式在CI中设置阈值（如vitest run --coverage --lines 80 --functions 85）。但不要为了覆盖率数字写低价值测试——"测试通过但什么都没验证"比没有测试更危险（给人虚假信心）。对于内容站：优先覆盖schema生成（SEO关键，错误会导致搜索展示异常）、路由参数处理、重定向逻辑、CTA链接生成（affiliate链接错误直接影响收入）。（来源：https://vitest.dev/guide/features 、https://main.vitest.dev/guide/learn/testing-in-practice）

知识点13：CI/CD中的测试策略——分层执行：PR触发快速测试（单元+集成，目标<5分钟），main分支合并触发完整测试（含E2E冒烟），定时任务运行全量E2E（如每小时或每天）。Playwright在CI中用sharding并行（npx playwright test --shard=1/4），Microsoft Playwright Testing服务最多50个并行worker。测试失败时必须上传artifact（trace.zip、截图、视频、JUnit XML报告）便于调试。Vitest在CI中用vitest run（非watch模式）+ --reporter=junit生成JUnit XML。关键原则：测试必须确定性——不依赖外部API（用MSW）、不依赖当前时间（vi.mock Date或vi.setSystemTime）、不依赖随机数（vi.mock Math.random）、测试间不共享状态。（来源：https://learn.microsoft.com/en-us/power-platform/developer/playwright-samples/cicd 、https://learn.microsoft.com/zh-cn/azure/playwright-testing/quickstart-run-end-to-end-tests 、https://vitest.dev/guide/features）

知识点14：Next.js App Router测试特殊考虑——Server Components不能在jsdom中直接渲染（它们运行在服务器上，依赖Node.js环境），需要用Vercel的nextjs-builder（Vitest插件）或单独测试数据获取逻辑。Client Components可用React Testing Library + Vitest + jsdom正常测试。API Routes（Route Handlers）可用Vitest + MSW测试请求/响应。E2E测试（Playwright）是测试Next.js完整页面（含Server Components渲染、metadata注入、schema输出）的最可靠方式——启动next start或next dev，Playwright访问真实URL。对于SSG页面，可测试构建后的静态HTML（next build && next start）。metadata/schema生成函数是纯函数（输入数据输出JSON-LD），非常适合单元测试，且是SEO关键路径。（来源：https://main.vitest.dev/guide/browser/component-testing.html 、https://vitest.fr/react/ 、https://testing-library.com/docs/react-testing-library/faq）

知识点15：测试数据管理与fixtures——使用工厂函数（如@faker-js/faker生成随机但真实的数据，或fishery定义工厂）生成测试数据，而非硬编码大段JSON。每个测试独立（不共享可变状态），用beforeEach重置fixture。MSW handlers可按测试覆盖（server.use(http.get(url, resolver))）测试不同场景（成功/空数据/404/500/超时/分页）。快照测试（expect(component).toMatchSnapshot()）适合稳定的UI组件（如按钮、徽章），但对频繁变化的内容要谨慎——大量快照更新会导致"快照疲劳"（开发者无脑更新快照而不检查差异）。对于内容站：posts.json/tools.json的小子集可作为fixture，测试渲染逻辑而非真实数据（真实数据会变化导致测试不稳定）。（来源：https://vitest.dev/guide/mocking 、https://main.vitest.dev/guide/learn/testing-in-practice 、http://raw.githubusercontent.com/aiskillstore/marketplace/main/skills/curiouslearner/mock-server/SKILL.md）

落地计划：
- P2-TEST-UNIT-001（新增）: 为关键工具函数添加Vitest单元测试。具体任务：(1)npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom；(2)配置vitest.config.ts（environment: 'jsdom', globals: true, setupFiles）；(3)为schema生成函数（FAQSchema/BreadcrumbSchema/OrganizationSchema/ProductSchema）写单元测试，验证输出JSON-LD结构正确；(4)为slug生成、日期格式化、CTA链接构建函数写测试；(5)在package.json添加"test": "vitest run"和"test:watch": "vitest"脚本；(6)目标：关键工具函数覆盖率>80%。
- P2-TEST-E2E-001（新增）: 添加Playwright E2E测试关键用户流程。具体任务：(1)npm install -D @playwright/test；(2)npx playwright install chromium；(3)配置playwright.config.ts（baseURL: 'http://localhost:3000', trace: 'on-first-retry', timeout: 30000）；(4)写3个E2E测试：首页加载返回200+关键元素可见、工具详情页CTA按钮跳转到工具官方域名（非Google搜索）、文章页FAQ schema在HTML中存在；(5)添加.github/workflows/playwright.yml（PR触发，npm ci && next build && next start & playwright test）；(6)失败时上传trace artifact。
- P2-TEST-MSW-001（新增）: 集成MSW mock API请求用于集成测试。具体任务：(1)npm install -D msw；(2)配置src/mocks/server.ts（setupServer + 基础handlers）和src/mocks/handlers.ts；(3)在vitest.setup.ts中集成MSW生命周期（beforeAll listen/afterEach resetHandlers/afterAll close）；(4)设置onUnhandledRequest: 'error'防止意外真实API调用；(5)为依赖外部API的组件（如GSC数据展示、工具价格获取、搜索功能）写集成测试，用MSW模拟不同响应（成功/空数据/错误）；(6)handlers按模块组织，便于复用和维护。



[2026-09-23] 高星GitHub开源工具：前端可访问性（a11y）自动化测试工具链（axe-core + eslint-plugin-jsx-a11y + jest-axe + pa11y + Lighthouse）

知识点1：axe-core——行业标准可访问性测试引擎，由Deque Systems开发维护，开源（GitHub dequelabs/axe-core，超5k星）。运行在任何浏览器环境中，是Lighthouse、axe DevTools、可访问性linter等大多数工具的基础。测试WCAG 2.0/2.1/2.2成功标准，提供可操作的开发者友好结果和修复建议。核心优势：零误报保证（zero false positive guarantee）——axe-core报告的违规都是真实的，不需要人工验证是否为误报。（来源：https://qaskills.sh/blog/accessibility-testing-automation-guide 、https://accessibility.deque.com/hubfs/Fact%20Sheets/axe-DevTools-for-Web.pdf）

知识点2：axe-core规则分类——规则分为三类：(1)wcag2a/wcag2aa/wcag21a/wcag21aa/wcag22a/wcag22aa——对应WCAG各版本各级别；(2)best-practice——Deque推荐的超越正式标准的最佳实践（可启用/禁用，增强可访问性但非正式标准要求）；(3)experimental——仍在开发中可能产生误报的实验规则。可通过runOptions.tags指定只测试特定标签，如{tags: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}。（来源：https://docs.deque.com/developer-hub/2/en/dh-api-reference/ 、https://docs.deque.com/devtools-for-web/4/en/wa-best-practices/）

知识点3：eslint-plugin-jsx-a11y——ESLint插件，对JSX元素进行静态AST检查，在编码阶段发现可访问性问题。GitHub jsx-eslint/eslint-plugin-jsx-a11y（超3k星）。React官方文档推荐。关键规则：alt-text（图片必须有alt）、anchor-is-valid（锚点必须有效）、click-events-have-key-events（可点击元素必须有键盘事件）、no-static-element-interactions（静态元素不应有交互）、aria-props（ARIA属性有效性）、label-has-associated-control（label必须关联控件）。Create React App默认激活子集规则。（来源：https://legacy.reactjs.org/docs/accessibility.html 、http://raw.githubusercontent.com/aiskillstore/marketplace/main/skills/doyajin174/accessibility-wcag/SKILL.md）

知识点4：jest-axe——Jest测试框架的axe-core封装，在单元测试/组件测试中运行可访问性检查。用法：import { axe, toHaveNoViolations } from 'jest-axe'; expect.extend(toHaveNoViolations); render(<Component />); const results = await axe(container); expect(results).toHaveNoViolations()。可在CI中阻止有可访问性违规的PR合并。适合组件级测试，但不能替代端到端测试（动态内容、交互后状态、路由切换后的DOM）。可与@testing-library/react配合使用。（来源：http://raw.githubusercontent.com/wshobson/commands/main/tools/accessibility-audit.md 、http://raw.githubusercontent.com/github/awesome-copilot/main/agents/accessibility.agent.md）

知识点5：pa11y——命令行可访问性测试工具，基于axe-core和HTML_CodeSniffer。GitHub pa11y/pa11y（超4k星）。支持爬取多个页面、生成HTML/JSON/CSV报告、配置阈值（如只允许N个违规）、CI集成（--exit-code在有违规时返回非零退出码）。用法：npx pa11y http://localhost:3000 --reporter html > report.html。pa11y-ci可批量测试sitemap中的所有URL，适合全站审计。可配置--threshold设置允许的违规数上限。（来源：https://raw.githubusercontent.com/github/awesome-copilot/main/agents/accessibility.agent.md 、http://raw.githubusercontent.com/proffesor-for-testing/agentic-qe/main/.claude/skills/accessibility-testing/SKILL.md）

知识点6：Lighthouse可访问性审计——Lighthouse内置可访问性类别，底层使用axe-core引擎。运行axe检查的子集，按加权影响评分0-100（基于axe用户影响评估：critical=10, serious=5, moderate=2, minor=1）。与性能审计不同，可访问性审计是通过/失败二元的——部分通过不得分（如部分按钮有标签部分没有，整个审计失败）。90-100为良好，50-89需改进，0-49严重。重要：100分不等于WCAG合规——自动化工具只能覆盖约30%的WCAG标准，其余需要人工测试。（来源：https://developer.chrome.google.cn/docs/lighthouse/accessibility/scoring 、https://kindatechnical.com/web-development/lesson-100-accessibility-testing-tools-axe-lighthouse-and-automated-ci-checks.html 、https://wsc.us.org/tool-lighthouse）

知识点7：@axe-core/cli——axe-core的命令行接口，可直接对URL运行完整axe测试（比Lighthouse的子集更全面）。用法：npx @axe-core/cli http://localhost:3000 --exit。支持--tags指定WCAG级别（如--tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa）、--rules指定规则、--reporter输出格式、--timeout设置超时。--exit在有违规时返回非零退出码，适合CI。比Lighthouse更严格，因为运行全部axe规则而非Lighthouse选择的子集。（来源：https://www.allaccessible.org/es/blog/website-accessibility-audit-guide-wcag-template 、https://raw.githubusercontent.com/github/awesome-copilot/main/agents/accessibility.agent.md）

知识点8：WCAG 2.2——W3C于2023年10月5日发布为正式推荐标准（W3C Recommendation），2024年12月12日更新。相比WCAG 2.1新增9个成功标准。核心新增AA级：2.4.11 Focus Not Obscured (Minimum)——焦点指示器不能被完全遮挡；2.5.7 Dragging Movements——拖拽操作必须有非拖拽替代（如点击）；2.5.8 Target Size (Minimum)——目标尺寸最小24×24 CSS像素；3.3.8 Accessible Authentication (Minimum)——认知功能测试（如拼图/记忆）不应作为唯一验证手段。新增A级：3.2.6 Consistent Help、3.3.7 Redundant Entry。（来源：https://www.w3.org/TR/WCAG/ 、https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ ）

知识点9：WCAG POUR四原则——所有可访问性标准基于四大原则：Perceivable（可感知）——信息和UI组件必须以用户可感知的方式呈现（文本替代、时间媒体、适应性、可区分）；Operable（可操作）——UI组件和导航必须可操作（键盘可访问、足够时间、癫痫预防、可导航）；Understandable（可理解）——信息和操作必须可理解（可读、可预测、输入辅助）；Robust（健壮）——内容必须能被各种用户代理（包括辅助技术）可靠解析。自动化工具主要覆盖Perceivable和部分Operable，Understandable和Robust需人工评估。（来源：http://raw.githubusercontent.com/msitarzewski/agency-agents/main/testing/testing-accessibility-auditor.md 、https://www.w3.org/TR/WCAG/）

知识点10：自动化测试的局限性——自动化可访问性工具只能检测约30%的WCAG违规。无法自动检测的包括：键盘陷阱、焦点顺序逻辑合理性、屏幕阅读器朗读质量、颜色对比度在渐变/图片上的实际效果、替代文本的质量（只能检测有无，不能判断是否合适/准确）、页面标题的描述性、链接文本的上下文意义、认知可访问性、语言清晰度。因此必须结合人工测试：键盘-only导航测试（Tab/Shift+Tab/Enter/Space/Esc）、屏幕阅读器测试（NVDA/JAWS/VoiceOver/TalkBack）、缩放测试（200%/400%无横向滚动）、减少动画测试。（来源：https://kindatechnical.com/web-development/lesson-100-accessibility-testing-tools-axe-lighthouse-and-automated-ci-checks.html 、https://raw.githubusercontent.com/github/awesome-copilot/main/agents/accessibility.agent.md）

知识点11：CI/CD集成三层防御模式——(1)编码阶段——eslint-plugin-jsx-a11y在IDE和pre-commit hook中实时反馈，最便宜最快的反馈环；(2)测试阶段——jest-axe在组件单元测试中检查，pa11y/@axe-core/cli在E2E中检查关键页面；(3)部署阶段——Lighthouse CI在每次部署后审计，axe DevTools Linter GitHub Action在PR上评论具体违规。Deque的Axe Developer Hub GitHub Action可阻止包含可访问性错误的commit/PR。关键策略：设置合理阈值，从warn开始逐步收紧到error，避免一开始就block所有PR导致团队抵触。（来源：https://docs.deque.com/developer-hub/2/en/dh-github-action/ 、https://docs.deque.com/linter/4.0.0/en/axe-linter-github-action/）

知识点12：焦点管理与键盘可访问性——WCAG 2.1 Success Criterion 2.1.1 (Keyboard, Level A)要求所有功能可通过键盘操作。常见问题：div/span上绑定onClick但无tabIndex和键盘事件（eslint-plugin-jsx-a11y的click-events-have-key-events规则检测）、模态框打开后焦点未移入、关闭后焦点未返回触发元素、路由切换后焦点未更新到新页面、焦点指示器被CSS outline:none移除且无替代样式。WCAG 2.2新增2.4.11 Focus Not Obscured要求焦点指示器不被粘性header/footer完全遮挡（至少部分可见）。（来源：https://www.w3.org/TR/WCAG/ 、http://raw.githubusercontent.com/aiskillstore/marketplace/main/skills/doyajin174/accessibility-wcag/SKILL.md）

知识点13：颜色对比度——WCAG 1.4.3 Contrast (Minimum, AA)：普通文本对比度≥4.5:1，大文本（≥18pt/24px常规或≥14pt/18.66px粗体）≥3:1。WCAG 1.4.11 Non-text Contrast (AA)：UI组件和图形对象对比度≥3:1。axe-core的color-contrast规则自动检测纯色背景，但在渐变背景、半透明叠加、图片上的文本时可能不准确（需人工验证）。工具无法检测：文本在图片上的实际对比度、hover/focus状态的对比度变化、禁用状态的对比度（WCAG豁免）。Next.js/Tailwind项目应使用可访问性友好的配色令牌（如Tailwind的默认配色大多满足AA）。（来源：https://compendium.koder.dev/hci/pt/06-accessibility-and-standards/ 、https://www.w3.org/TR/WCAG/）

知识点14：ARIA使用五大规则——第一规则：如果可以使用原生HTML元素实现，就不要用ARIA（如用<button>而非<div role="button">，原生元素自带键盘支持和语义）。第二规则：不要改变原生元素的语义（如不要给<button>加role="link"）。第三规则：所有ARIA控件必须可键盘操作（role="tab"/"menu"/"dialog"等需完整键盘交互模式）。第四规则：不要使用role="presentation"或aria-hidden="true"在可聚焦元素上（会导致键盘用户聚焦到不可见元素）。第五规则：交互元素必须有可访问名称（accessible name，通过文本内容、aria-label、aria-labelledby）。eslint-plugin-jsx-a11y的aria-props/aria-proptypes/role-has-required-aria-props规则检测常见ARIA错误。（来源：https://legacy.reactjs.org/docs/accessibility.html 、http://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/a11y-audit/skills/a11y-audit/SKILL.md）

知识点15：可访问性与SEO/性能的协同——可访问性改进通常同时改善SEO和性能：语义化HTML（header/nav/main/article/section）帮助搜索引擎理解页面结构同时帮助屏幕阅读器导航；alt文本帮助图片SEO同时帮助视障用户；键盘可访问性改善移动端触摸体验；足够的颜色对比度改善强光下和老年用户可读性；焦点指示器改善所有用户的导航体验；label关联改善表单转化率。Lighthouse的可访问性分数和SEO分数有正相关。Next.js的<Image>组件自动生成width/height避免CLS，同时应确保alt属性非空（装饰性图片用alt=""，axe-core的aria-hidden或presentation角色可标记装饰元素）。（来源：https://wsc.us.org/tool-lighthouse 、https://www.pandauxstudio.com/article/accessibility-as-strategy）

落地计划：
- P2-A11Y-LINT-001（新增）: 集成eslint-plugin-jsx-a11y到项目ESLint配置。具体任务：(1)npm install --save-dev eslint-plugin-jsx-a11y；(2)在.eslintrc中extends添加plugin:jsx-a11y/recommended；(3)启用关键规则：alt-text/anchor-is-valid/click-events-have-key-events/no-static-element-interactions/label-has-associated-control；(4)在pre-commit hook中运行；(5)从warn级别开始，逐步修复后收紧到error。
- P2-A11Y-LIGHTHOUSE-001（新增）: 在现有Lighthouse CI中添加可访问性断言。具体任务：(1)在.lighthouserc.json中添加accessibility>=0.9断言（当前已有performance/accessibility/best-practices/seo>=0.9，确认accessibility阈值已设置）；(2)在lighthouse-ci.yml workflow中确认审计3个关键页面的可访问性；(3)设置阈值从warn开始，逐步修复后收紧到error；(4)定期审查Lighthouse CI报告中的可访问性违规。
- P2-A11Y-SEMANTIC-001（新增）: 修复关键页面的语义化HTML和可访问性问题。具体任务：(1)首页确保有<main> landmark、<h1>唯一、图片alt文本非空（装饰性用alt=""）；(2)工具详情页CTA按钮用<button>而非div、焦点指示器可见（不删除outline）、目标尺寸≥24px；(3)文章页标题层级正确（h1→h2→h3不跳级）、图片有描述性alt；(4)对比页表格有<th>和scope属性；(5)所有交互元素可键盘操作。



[2026-09-23] 前端工程化：Next.js App Router错误处理与加载状态最佳实践（error.tsx + loading.tsx + not-found + catchError）

知识点1：error.tsx文件约定——在路由段中添加error.tsx文件创建React Error Boundary，捕获该段及其子段（page、nested layout、loading、not-found）中未捕获的异常，显示fallback UI。error.tsx必须是Client Component（'use client'）。生产环境中Server Component的错误会被剥离具体细节以避免泄露敏感信息（只保留通用消息和digest）。（来源：https://nextjs.org/docs/app/getting-started/error-handling 、https://nextjs.org/docs/app/api-reference/file-conventions/error）

知识点2：error.tsx不捕获同层layout错误——error boundary在组件层级中包裹page和nested layouts，但不包裹同层的layout.tsx或template.tsx。同层layout中的错误会冒泡到父级的error boundary。因此根layout的错误无法被app/error.tsx捕获，需要global-error.tsx处理。这是最常见的误解之一。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/error 、https://react.codeguides.io/nextjs-routing/loading-error/）

知识点3：global-error.tsx——处理根layout或根template中的错误（最后一道防线）。必须定义自己的<html>和<body>标签，因为它在激活时替换整个根layout/template。global-error.tsx只在生产环境激活，开发环境显示错误覆盖层（dev overlay）。应包含基本的错误信息和"返回首页"链接，因为此时导航栏和footer都不可用。（来源：https://nextjs.org/docs/app/getting-started/error-handling 、https://paulund.co.uk/notebook/nextjs/error-and-not-found-pages-in-the-app-router）

知识点4：error组件props——error.tsx导出的组件接收两个props：error（Error对象，含message和digest）和reset（函数，重置错误状态并重新渲染，不重新fetch）。Next.js 16.3起新增retry()函数（重新fetch并重新渲染error boundary的子组件，成功后fallback被替换），大多数情况应使用retry()而非reset()。retry在16.2为unstable_retry，16.3稳定。（来源：https://preview.nextjs.org/docs/app/api-reference/file-conventions/error 、https://nextjs.org/blog/next-16-3-preview）

知识点5：loading.tsx文件约定——在路由段中添加loading.tsx自动创建Suspense boundary包裹page内容（底层生成<Suspense fallback={<Loading />}><Page /></Suspense>），显示即时加载状态。loading UI作为静态文件的一部分预先渲染并首先发送，动态内容随后从服务器流式传输。在初始加载和每次后续导航到该段时都显示。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/loading 、https://react.codeguides.io/nextjs-routing/loading-error/）

知识点6：骨架屏最佳实践——好的骨架屏应：(1)匹配所替换内容的布局（相同高度、宽度、间距）；(2)避免布局偏移（真实内容替换时不应跳动，即CLS=0）；(3)使用微妙动画（轻柔pulse或shimmer，不分散注意力）；(4)尊重prefers-reduced-motion（减少动画偏好）。骨架屏减少感知加载时间，给用户布局预览。任何UI添加到loading.tsx都会作为静态文件的一部分嵌入并首先发送。（来源：https://nextjs.org/learn/dashboard-app/streaming 、https://rebeccamdeprey.com/blog/rsc-streaming-suspense）

知识点7：Suspense粒度控制——loading.tsx为整个路由段创建一个Suspense boundary，但更细粒度的控制是在page.tsx中用<Suspense fallback={<Skeleton />}>包裹单个异步组件。多个兄弟组件各自包裹Suspense时，它们独立流式渲染，不互相阻塞（无瀑布）。例如Stats组件200ms返回、Posts组件1200ms返回，页面立即渲染标题，200ms时替换stats骨架，1200ms时替换posts骨架。（来源：https://nextjs.org/docs/app/guides/streaming 、https://nerdleveltech.com/nextjs-16-streaming-suspense-use-cache-tutorial）

知识点8：流式传输中的错误处理——如果组件在流式传输开始后抛出错误，最近的error.tsx boundary捕获它并在失败组件的位置渲染错误UI，页面其余部分保持完整（只有出错的section被替换）。但因为HTTP状态码200已随第一个chunk发送，无法更改为500——这是流式传输的已知限制。爬虫和机器人（bots/crawlers）会等待完整渲染而非流式接收。（来源：https://nextjs.org/docs/app/guides/streaming 、https://nextjs.org/docs/app/getting-started/fetching-data）

知识点9：not-found.tsx与notFound()——notFound()函数（来自next/navigation）用于数据不存在的情况（404），不是错误。调用后Next.js停止渲染当前页面并显示404 UI。not-found.tsx在路由段级别工作，仅在显式调用notFound()时触发（不会自动捕获不匹配URL）。global-not-found.js用于整个应用的404（URL不匹配任何路由时），Next.js跳过渲染直接返回此全局页面。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/not-found 、https://www.honeybadger.io/blog/next-js-error-handling/）

知识点10：嵌套error boundaries最佳实践——将error.tsx放在尽可能小的路由段中，隔离失败到最小范围。例如app/tools/[slug]/error.tsx只捕获工具详情页的错误，不影响首页或其他工具页。父级error boundary捕获子级未处理的错误。如果希望错误冒泡到父级error boundary，可以在渲染error组件时throw。（来源：https://nextjs.org/docs/app/getting-started/error-handling 、https://dev.to/anas_sheikh_2/error-handling-in-nextjs-15-errortsx-notfound-and-the-patterns-i-actually-use-ceh）

知识点11：Next.js 16.2 catchError（16.3稳定）——catchError()函数提供组件级别的细粒度错误边界控制，不绑定到路由段（不像error.tsx只能按路由段）。创建自定义error boundary：定义fallback函数接收props和ErrorInfo（含error和retry），导出catchError(ErrorFallback)。框架感知：redirect()和notFound()等API通过抛出特殊错误工作，catchError无缝处理它们不被意外捕获。客户端导航时错误状态自动清除。（来源：https://nextjs.org/docs/app/api-reference/functions/catchError 、https://nextjs.org/blog/next-16-2 、https://certificates.dev/blog/error-handling-in-nextjs-with-catcherror）

知识点12：retry() vs reset()——retry()（16.3稳定）重新fetch并重新渲染error boundary的子组件，成功后fallback被替换为重新渲染的结果。reset()清除错误状态并重新渲染但不重新fetch内容。大多数情况应使用retry()，只有特定原因需要清除错误状态不重新fetch时才用reset()。服务器错误在不修复根本原因的情况下retry可能再次失败，应在retry按钮旁提示用户"如果问题持续请稍后再试"。（来源：https://nextjs.org/docs/app/api-reference/functions/catchError 、https://preview.nextjs.org/docs/app/api-reference/file-conventions/error）

知识点13：Server Actions中的try/catch——在Server Actions中用try/catch优雅处理错误，不要让异常冒泡到error boundary。注意redirect()和notFound()通过抛出特殊错误（NEXT_REDIRECT/NEXT_NOT_FOUND）工作，不要在catch块中吞掉它们（应重新抛出或不在包含这些调用的代码外层用catch）。Next.js官方dashboard教程推荐此模式：try { await action() } catch (e) { if (isRedirectError(e)) throw e; ... }。（来源：https://nextjs.org/learn/dashboard-app/error-handling 、https://nextjs.org/docs/app/getting-started/error-handling）

知识点14：PPR/动态渲染中的try/catch陷阱——不要将选择动态渲染的Next.js API（如cookies()、headers()、searchParams）包裹在try/catch中，否则会触发"Static Bail Out Caught"（ppr-caught-error）错误。如果必须包裹，确保重新抛出原始错误让Next.js捕获，或在try/catch前插入unstable_noStore()显式选择动态渲染。这是PPR/Cache Components场景下的常见坑。（来源：https://nextjs.org/docs/messages/ppr-caught-error ）

知识点15：错误监控与日志——生产环境中Server Component错误被剥离细节，但error.digest属性可用于关联服务器端日志。应在error.tsx中记录错误（console.error或发送到Sentry等监控服务），包含error.message和error.digest。global-error.tsx中也应记录根layout错误。错误日志是调试生产问题的关键，因为用户只看到通用错误UI。建议同时记录：错误消息、digest、当前URL、用户代理、时间戳。（来源：https://nextjs.org/docs/app/getting-started/error-handling 、https://reactdevelopers.org/docs/nextjs-patterns/error-handling/）

落地计划：
- P2-PERF-LOADING-001: 为关键路由段添加loading.tsx骨架屏。具体任务：(1)app/tools/[slug]/loading.tsx——工具详情页骨架（匹配工具卡片布局：标题占位+评分占位+截图占位+CTA按钮占位）；(2)app/blog/[slug]/loading.tsx——文章页骨架（标题+元信息+正文段落占位）；(3)app/compare/loading.tsx——对比页骨架（表格行占位）；(4)确保骨架屏匹配真实布局避免CLS；(5)尊重prefers-reduced-motion。
- P2-ERROR-BOUNDARY-001（新增）: 添加error.tsx和global-error.tsx完善错误处理。具体任务：(1)app/tools/[slug]/error.tsx——工具详情页错误UI+retry按钮；(2)app/blog/[slug]/error.tsx——文章页错误UI；(3)app/global-error.tsx——根layout错误最后防线（含html/body标签+返回首页链接）；(4)错误日志记录（error.digest关联服务器日志）。
- P2-ERROR-NOTFOUND-001（新增）: 完善not-found处理。具体任务：(1)app/tools/[slug]/page.tsx中工具不存在时调用notFound()；(2)app/blog/[slug]/page.tsx中文章不存在时调用notFound()；(3)app/not-found.tsx自定义404页面（匹配站点设计风格）；(4)app/global-not-found.tsx全局404兜底。



[2026-09-23] SEO工程化：E-E-A-T与FTC联盟披露最佳实践（Trust为核心 + 清晰显著披露 + 作者署名信号）

知识点1：E-E-A-T四支柱定义——Experience（经验）、Expertise（专业）、Authoritativeness（权威）、Trustworthiness（可信）。来自Google Search Quality Rater Guidelines（2025年9月11日更新，182页）。Trust是最重要的支柱，低Trust会限制质量评分，无论专业度多高。其他三个支柱都对Trust有贡献，但内容不需要同时具备所有四个。（来源：https://developers.google.cn/search/docs/fundamentals/creating-helpful-content 、https://www.voctos.com/blog/eeat-seo-guide/）

知识点2：Experience（第一E）是2022年12月15日新增的，是最难被AI复制的信号。评估内容创作者是否对主题有第一手亲身参与。关键信号：原始照片、测试时长、失败案例、具体日期和环境。2025年9月更新进一步提升了第一手Experience的权重，展示真实经验和专业的网站在更新后排名上升。（来源：https://www.bestseo.sg/blog/eeat-seo-2026/ 、https://www.jsonhouse.com/posts/eeat-ai-content-2026/）

知识点3：Expertise（专业度）——内容创作者是否有知识、技能或资质来准确覆盖主题。Google从内容深度（浅层表面 vs 深入逻辑框架和体系化干货）、引用数据/行业案例/参考资料的可核查性、是否区分事实与观点等维度评估。对于AI工具评测站，专业度体现在：是否实际使用过工具、是否有量化评测数据、是否对比了多个工具的优劣。（来源：https://thestacc.com/blog/eeat-google-quality-guide/ 、https://www.iesdouyin.com/share/video/7648588428241571123）

知识点4：Authoritativeness（权威性）——创作者或网站是否被公认为该主题的首选来源。关键信号：外部引用和反向链接、行业认可、被其他权威站点引用、社交媒体影响力、作者在领域内的声誉。权威性是"他人对你的评价"，不是自我宣称。对于新站，权威性需要通过持续产出高质量内容、获取行业引用和建立作者个人品牌来积累。（来源：https://theguidex.com/insights/google-quality-rater-guidelines 、https://clickraven.com/google-eat/）

知识点5：Trustworthiness（可信度）——用户是否可以信赖内容、网站和背后的企业。这是最重要的支柱。关键信号：清晰的作者署名、关于页面、联系信息、客户服务、隐私政策、联盟披露、内容准确性、更正记录、安全的网站（HTTPS）、透明的商业模式。对于联盟评测站，联盟披露是Trust的核心组成部分——不披露联盟关系会被认为是不可信的。（来源：https://developers.google.cn/search/docs/fundamentals/creating-helpful-content 、https://www.imarkinfotech.com/e-e-a-t-explained-ultimate-guide-googles-quality-standards/）

知识点6：E-E-A-T不是直接排名因素，但塑造Google算法训练的信号。Google的自动化系统根据许多因素提高优质内容排名，E-E-A-T是确定内容是否有用的综合因素框架。人类质量评分员的评估结果用于训练Google的算法，因此E-E-A-T信号会间接影响排名。E-E-A-T信号与AI答案引擎引用内容的标准高度重叠——AI系统在选择引用源时也评估相同的信任信号。（来源：https://ppc.land/e-e-a-t/ 、https://www.voctos.com/blog/eeat-seo-guide/）

知识点7：YMYL（Your Money or Your Life）内容——涉及财务、健康、安全、公民等主题的内容，E-E-A-T要求更严格。AI工具评测/推荐站虽然不是传统YMYL，但涉及消费决策和金钱支出（用户可能基于评测购买付费工具），Google会以较高标准评估Trust。评测站需要特别注意：评测方法透明、数据来源可核查、联盟关系披露、作者专业背景清晰。（来源：https://theguidex.com/insights/google-quality-rater-guidelines 、https://www.bestseo.sg/blog/eeat-seo-2026/）

知识点8：FTC 16 CFR Part 255（代言和推荐指南）——当背书者与产品卖家之间存在可能实质影响背书权重或可信度的联系（且受众不会合理预期该联系）时，必须清晰显著地披露。物质联系包括商业、家庭或个人关系，包括金钱支付或免费/折扣产品（包括与背书产品无关的免费产品）。广告主对通过背书做出的虚假或未经证实的陈述、或未能披露物质联系承担责任；背书者也可能对其在背书过程中做出的陈述承担责任。（来源：https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 、https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides）

知识点9：FTC披露要求"清晰显著"（clear and conspicuous）——2023年更新明确披露必须是"不可避免的"。四要素：(1)位置——在第一个联盟链接上方或旁边，不在底部、不在hover提示中；(2)格式——无需滚动即可看到，字体大小与正文相当，对比度足够，不用浅色小字；(3)语言——简单直白，不用法律术语，如"我们可能通过此链接赚取佣金"；(4)移动端——在手机上同样可见（桌面above the fold在手机上可能滑出视野，需单独检查）。（来源：https://bestautomationtools.ai/guides/ftc-affiliate-disclosure/ 、https://earnifyhub.com/blog/affiliate/ftc-affiliate-disclosure-requirements-2026）

知识点10：披露位置最佳实践——博客文章：在标题或第一段之后，第一个联盟链接之前；产品评测：在评测顶部与推荐一起可见，每个联盟链接附近重复简短提示；对比页：在对比表格上方加披露作为表格标题，每个"Visit site"/"Check price"按钮附近加简短提示；粘性CTA栏：如果粘性栏先显示联盟链接，披露也必须在粘性栏中。超过2000字的长文应在内容中重复披露。（来源：https://gohomoney.com/affiliate-link-rules/ 、https://www.affiliatenewsreview.com/disclosure-placement-and-timing.html 、https://earnetics.com/affiliate-disclosures-done-right-examples-copy-paste-snippets/）

知识点11：仅在footer或独立披露页面放置披露是不够的——FTC明确指出：把披露埋在About Us页面、标签不清的超链接或服务条款协议中是不够的。放在评测下方或零售商链接下方让读者滚动后才能看到也不够。独立披露页面可以作为补充（提供更详细的说明），但不能替代页面内的即时披露。2026年FTC对违规的罚款可达每次违规51,744美元。（来源：https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides 、https://internetmoneypro.com/blog/affiliate-marketing-disclosure）

知识点12：Google E-E-A-T作者署名信号——Google Search Central明确建议添加准确的作者信息，如内容署名（byline）。署名应链接到作者的更多信息页面，提供背景和写作领域。如果访问者能一目了然地知道谁创作了内容，就可能与E-E-A-T概念一致。2026年2月1日Google在Search Central文档中新增了Authors部分，表明作者透明度是直接的质量考量因素。Google信任经过验证的实体，不仅仅是页面——作者必须被识别为与组织实体和特定主题领域相关联的个人实体，其内容才能获得完整的E-E-A-T权重。（来源：https://developers.google.com/search/docs/fundamentals/creating-helpful-content?id=49 、https://redot.global/blog/eeat-authority-google-ai-trust-signals/）

知识点13：作者页面最佳实践——创建真实的作者页面，包含相关专业背景、头像、LinkedIn链接、在本站发布的作品列表。为需要专业知识的文章添加审核者（reviewer）行并命名审核者。将文章分配给合适的作者（健康文章归营销通才会引发黄旗）。作者简介链接到全站一致的个人资料页面，使同一人可以积累可信度轨迹。Article结构化数据中author字段应指向Person实体（包含name、url、sameAs）。（来源：https://keytomic.com/blog/eeat-google 、https://developers.google.com/search/docs/appearance/structured-data/article）

知识点14：日期更新信号——dateModified必须反映真实的内容更改，Google明确警告不要只更新发布日期而不改变内容（"更新发布日期而不更改内容是Google明确警告的做法之一"）。新鲜日期需要反映新鲜内容。schema中的dateModified字段必须与真实编辑匹配。对于评测站，定期重新测试工具并更新评测内容和日期是强Experience信号——表明评测不是一次性的，而是持续验证的。NAP（名称、地址、电话）在网站和外部来源间的一致性也是信任信号，不一致暗示未维护或可能的欺诈业务。（来源：https://www.reporteroutreach.com/blog/eeat-checklist 、https://developers.google.com/search/docs/appearance/structured-data/article）

知识点15：AI生成内容的E-E-A-T——2025年9月Quality Rater Guidelines更新收紧了对AI生成内容的Trust评估。AI内容需要人类编辑、事实核查和第一手经验补充。关键策略：AI辅助研究+人类第一手测试+原始截图+具体数据+作者署名+审核流程。纯AI生成无人类验证的内容在Experience和Trust维度会被扣分。对于AI工具评测站，最有效的E-E-A-T策略是：AI辅助撰写框架，但所有评测数据、截图、优缺点分析必须来自人类实际使用，文章末尾标注"由XX编辑审核，最后更新于XX日期"。（来源：https://www.jsonhouse.com/posts/eeat-ai-content-2026/ 、https://www.bestseo.sg/blog/eeat-seo-2026/）

落地计划：
- P1-SCHEMA-DISCLOSURE: 在所有工具详情页CTA附近添加"May earn commission"联盟披露。具体任务：(1)在app/tools/[slug]/page.tsx的CTA按钮组上方添加简短披露行（"We may earn a commission when you click our links. This doesn't affect our reviews."）；(2)在app/compare/page.tsx对比表格上方添加披露；(3)确保披露above the fold且移动端可见；(4)创建全局AffiliateDisclosure组件复用。
- P1-MONETIZE-DISCLOSURE-001: 验证FTC联盟披露在所有含联盟链接页面可见。具体任务：(1)检查工具详情页、文章页、对比页、首页、分类页是否都有披露；(2)确保披露在第一个联盟链接之前（不是只在footer）；(3)移动端验证可见性；(4)检查披露语言是否清晰直白（不用法律术语）；(5)创建全站统一的披露标准。
- P1-E-E-A-T-AUTHOR-001（新增）: 完善作者署名和作者页面E-E-A-T信号。具体任务：(1)确保所有105篇文章有byline链接到作者页面；(2)作者页面添加专业背景、头像、社交链接、作品列表；(3)Article schema中author字段指向Person实体（含name/url/sameAs）；(4)所有文章添加dateModified字段（与真实编辑匹配）；(5)首页和关于页添加编辑/审核流程说明。



[2026-09-23] Next.js 15/16新特性与升级要点（Turbopack稳定 + Cache Components + React Compiler + 缓存语义变更）

知识点1：Next.js 15 缓存语义破坏性变更——fetch请求、GET Route Handlers和客户端导航默认不再缓存（Next.js 14及之前默认缓存）。升级后必须显式标注缓存策略：fetch(url, { cache: "force-cache" }) 或用 unstable_cache，否则所有数据请求变为动态渲染，TTFB和构建时间会显著上升。这是14→15升级最大的坑。（来源：https://nextjs.org/blog/next-15 、https://nextjs.org/blog/next-15-rc）

知识点2：Next.js 15 异步Request APIs破坏性变更——request()、headers()、cookies() 从同步变为异步函数，必须用 await 调用。所有直接调用 headers().get("x") 的代码必须改为 (await headers()).get("x")。@next/codemod 可自动迁移大部分。（来源：https://nextjs.org/blog/next-15 ）

知识点3：Next.js 15 React 19支持——App Router使用React 19 RC，Pages Router保留React 18向后兼容。React 19带来Actions、use() hook、useOptimistic、useActionState、ref作为prop、Document Metadata等新特性。hydration错误信息改善，更易定位。（来源：https://nextjs.org/blog/next-15 、https://react.dev/blog/2025/10/07/react-compiler-1）

知识点4：Next.js 15 Turbopack Dev稳定——开发服务器Turbopack达到稳定，Fast Refresh比Webpack快5-10倍。需用 next dev --turbo 启用（15中仍需flag，16中变为默认）。生产构建Turbopack在15.5中为beta，16中稳定。（来源：https://nextjs.org/blog/next-15 、https://nextjs.org/docs/app/api-reference/turbopack）

知识点5：Next.js 15 Partial Prerendering (PPR) 增量可用——通过 next.config.js 设置 experimental.ppr = "incremental"，在具体路由段导出 export const experimental_ppr = true 启用。PPR结合静态shell和动态内容：构建时生成静态HTML shell，请求时立即发送shell，动态部分通过Suspense流式渲染。（来源：https://nextjs.org/docs/15/app/getting-started/partial-prerendering 、https://nextjs.org/docs/15/app/api-reference/config/next-config-js/ppr）

知识点6：Next.js 16 Turbopack全面稳定——Turbopack在开发和生产构建中均达到稳定，成为所有新项目的默认bundler。生产构建比Webpack快2-5倍，Fast Refresh快5-10倍。15.3+版本中已有50%开发会话和20%生产构建使用Turbopack。升级后无需 --turbo flag，自动启用。（来源：https://nextjs.org/blog/next-16 、https://nextjs.org/docs/app/guides/upgrading/version-16）

知识点7：Next.js 16 Cache Components稳定——Cache Components是PPR的演进版，通过 "use cache" 指令和 cacheLife() 函数在单一路由中混合静态、缓存和动态内容。启用方式：next.config.js 中 cacheComponents: true。PPR成为App Router默认行为，experimental.ppr flag和experimental_ppr路由配置已被移除。静态HTML shell可直接从CDN提供，无需回源服务器，直接导航即时加载。（来源：https://nextjs.org/docs/app/getting-started/cache-components 、https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents）

知识点8：Next.js 16 React Compiler支持稳定——React Compiler 1.0已发布，Next.js 16内置稳定支持。React Compiler在构建时自动优化组件渲染，通过自动memoization减少不必要的重渲染，无需手动写useMemo/useCallback。配置选项 reactCompiler 从experimental提升为stable，但默认不启用（因构建时间会增加）。Next.js用SWC自定义优化，只对需要的文件应用Compiler而非全量。（来源：https://nextjs.org/blog/next-16 、https://nextjs.org/docs/app/api-reference/config/next-config-js/reactCompiler 、https://react.dev/learn/react-compiler/introduction）

知识点9：Next.js 16 Turbopack文件系统缓存（beta）——将编译器产物持久化到磁盘，跨运行复用，大幅提升大型应用的启动和编译时间。16.1中 next dev 的文件系统缓存稳定并默认开启；16.3中 next build 的持久化缓存也默认启用。（来源：https://nextjs.org/blog/next-16-1 、https://preview.nextjs.org/blog/next-16-3-turbopack）

知识点10：Next.js 16.2 新特性——Server Fast Refresh（细粒度服务端热重载，改Server Component只重渲染受影响部分）、Web Worker Origin（增加WASM库在Workers中的支持）、Subresource Integrity（JavaScript文件SRI支持）、Tree Shaking of Dynamic Imports（动态import()中未使用的导出被移除）。（来源：https://nextjs.org/blog/next-16-2-turbopack）

知识点11：Next.js 16.3 Rust版React Compiler——React Compiler之前通过Babel在Node.js中运行，16.3的实验性Rust版本直接在Turbopack内部运行，避免生成和重新解析代码的额外开销。启用方式：reactCompiler: { rust: true }。其他16.3特性：import.meta.glob（Vite兼容glob导入）、更少prefetch请求（链接触发更小payload）、静态资产更好缓存（不可变资产可跨部署复用）、自定义error boundaries（重新获取失败数据恢复服务端错误）。（来源：https://nextjs.org/blog/next-16-3）

知识点12：Cache Components迁移路径——从PPR迁移到Cache Components：(1) 移除 next.config 中的 experimental.ppr；(2) 移除路由段中的 export const experimental_ppr；(3) 启用 cacheComponents: true；(4) 将 dynamic/revalidate/fetchCache 路由配置替换为 "use cache" 指令和 cacheLife()；(5) 用 revalidateTag() 替代旧的标签缓存方式。@next/codemod 可自动处理大部分迁移。（来源：https://nextjs.org/docs/app/guides/migrating-to-cache-components 、https://nextjs.org/docs/app/guides/upgrading/version-16）

知识点13：升级路径 14.2.5 → 15 → 16——分两步升级降低风险：第一步14→15重点处理缓存语义变更（所有fetch需显式cache策略）和异步APIs（headers/cookies/request加await）；第二步15→16重点处理Turbopack默认（移除webpack特定配置）、PPR→Cache Components迁移、React Compiler评估。每步后跑完整tsc + build + 线上冒烟测试。@next/codemod CLI可自动化大部分代码变更。（来源：https://nextjs.org/docs/app/guides/upgrading/version-16 、https://nextjs.org/blog/next-15）

知识点14：Vercel部署PPR/Cache Components要求——PPR/Cache Components需要平台支持静态HTML shell + postponedState blob。Vercel完全支持：构建时为每个PPR路由生成静态shell和postponedState，请求时shell立即从CDN发送，动态部分流式渲染。ISR与Cache Components结合可为未包含在构建中的URL提供即时首次访问（App Shell + 参数特定预渲染）。（来源：https://nextjs.org/docs/app/guides/ppr-platform-guide 、https://preview.nextjs.org/docs/app/guides/incremental-static-regeneration-cache-components）

知识点15：Next.js 16破坏性变更清单——(1) 移除 experimental.dynamicIO（重命名为cacheComponents）；(2) 移除 experimental.ppr 和 experimental_ppr 路由配置（并入Cache Components）；(3) 移除自动 scroll-behavior: smooth（需手动加 data-scroll-behavior="smooth" 到HTML文档）；(4) Turbopack变为默认bundler（webpack仍可用但需显式配置）；(5) Node.js最低版本要求提升。升级前必须逐项检查。（来源：https://nextjs.org/blog/next-16 、https://nextjs.org/docs/app/guides/upgrading/version-16）

落地计划：
- P2-UPGRADE-NEXT16-001：评估Next.js 16升级可行性。具体任务：(a) 检查当前package.json依赖与Next.js 16兼容性（next 14.2.5 → 16需升级react/react-dom到19）；(b) 审计所有fetch调用，标注缓存策略（15起默认不缓存，工具页/文章页数据需显式force-cache）；(c) 检查headers()/cookies()/request()调用是否需加await；(d) 跑@next/codemod自动迁移；(e) 评估Turbopack默认对构建配置的影响。
- P2-PERF-CACHE-COMPONENTS-001（新增）：升级后启用Cache Components优化工具页/文章页。具体任务：(a) next.config.mjs加cacheComponents: true；(b) 工具详情页用"use cache" + cacheLife(86400)缓存工具数据，静态shell即时发送，动态部分流式渲染；(c) 文章页同样启用；(d) 验证LCP/TTFB改善。
- P2-PERF-REACT-COMPILER-001（新增）：升级后启用React Compiler自动memoization。具体任务：(a) next.config.mjs加reactCompiler: true（先评估构建时间影响）；(b) 重点优化重型客户端组件（搜索弹窗/筛选面板/compare工具选择）；(c) 验证INP改善和重渲染减少；(d) 如构建时间可接受则保留，否则用reactCompiler.target限定只对特定目录应用。



[2026-09-23] Bundle体积优化与代码分割最佳实践（@next/bundle-analyzer + next/dynamic + Tree Shaking + optimizePackageImports + next/script + CSS优化）

知识点1：@next/bundle-analyzer 是 Next.js 官方 bundle 可视化分析工具，安装后在 next.config.js 中用 withBundleAnalyzer 包裹配置，运行 ANALYZE=true next build 生成 treemap 可视化报告，展示每个包及其依赖的体积占比。用于定位大型依赖、决定是否拆分或懒加载。辅助工具：Import Cost（VSCode插件实时显示导入体积）、Package Phobia、Bundle Phobia、bundlejs。（来源：https://nextjs.org/docs/app/guides/package-bundling 、https://nextjs.org/docs/app/guides/production-checklist）

知识点2：Next.js 16+ 内置 `next experimental-analyze` 命令，基于 Turbopack 分析 bundle 输出（JS/CSS/其他资产），不需要完整构建即可了解 bundle 组成和大小。比 @next/bundle-analyzer 更快，适合 CI 中快速检查。（来源：https://nextjs.org/docs/app/api-reference/cli/next.md）

知识点3：App Router Server Components 实现自动路由级代码分割——每个路由段（route segment）的 Server Components 自动分割为独立 chunk，页面初始加载只包含当前路由所需代码，不需要手动配置。这是 App Router 相比 Pages Router 的核心性能优势之一。客户端组件（"use client"）仍会被打包进客户端 bundle，因此应尽量多用 Server Components。（来源：https://nextjs.org/docs/app/guides/production-checklist 、https://nextjs.org/docs/app/guides/lazy-loading）

知识点4：next/dynamic 是 React.lazy() + Suspense 的封装，用于懒加载客户端组件和第三方库。关键选项：ssr:false（禁用服务端渲染，适合纯客户端组件如图表/地图）、loading（加载占位组件）。典型场景：重型 Modal、富文本编辑器、图表库（recharts/chart.js）、代码高亮器——这些组件不在首屏渲染路径中，懒加载可显著减少初始 JS。（来源：https://nextjs.org/docs/app/guides/lazy-loading 、https://www.codevup.com/posts/nextjs-bundle-optimization-guide/）

知识点5：Tree Shaking 生效的前提是依赖必须使用 ES Modules（import/export）。CommonJS 模块（require/module.exports）是运行时解析的，bundler 无法静态分析哪些导出被使用，会全量包含进 bundle。选择依赖时优先选提供 ESM 构建的包；如果某个依赖只有 CJS 版本，考虑用 optimizePackageImports 或手动 deep import（import Button from 'lib/Button' 而非 import { Button } from 'lib'）。（来源：https://www.codevup.com/posts/nextjs-bundle-optimization-guide/ 、https://sujeit.pro/articles/frontend-engineering/web-performance-optimization/web-performance-javascript-optimization）

知识点6：package.json 的 sideEffects 字段告诉 bundler 该包的哪些文件有副作用（执行顶层代码如 polyfill 注入、CSS import）。声明 "sideEffects": false 表示无副作用，bundler 可更激进地 tree shake 未使用的导出。如果包有 CSS import 或全局副作用，应精确列出文件路径如 "sideEffects": ["*.css"]。这是库作者优化包体积的关键配置。（来源：https://webperfclinic.com/pl/article/optymalizacja-bundle-javascript-2026-tree-shaking-code-splitting-import-maps）

知识点7：optimizePackageImports 是 Next.js 13.5+ 引入的实验特性（next.config.js 的 experimental.optimizePackageImports 数组），针对导出数百/数千模块的大包（如 lucide-react、framer-motion、date-fns、lodash-es），自动只加载实际使用的模块，同时保留命名导入的便利写法。Vercel 官方博客数据：对 lucide-react 等图标库可减少 70%+ 导入体积。当前项目 next.config.mjs 已配置 lucide-react 和 framer-motion。（来源：https://nextjs.org/docs/app/guides/package-bundling 、https://vercel.com/blog/how-we-optimized-package-imports-in-next-js）

知识点8：Barrel files（index.ts 集中 re-export）会破坏 tree shaking——当从 index.ts 导入单个组件时，bundler 可能将 index.ts 中所有 re-export 的模块都包含进来，因为无法确定哪些有副作用。在开发模式下 tree shaking 不执行（dev server 不做生产优化），问题只在生产构建中暴露。解决方案：避免深层 barrel 文件、直接从具体文件导入、或在 package.json 中正确配置 sideEffects。（来源：https://dev.to/childrentime/barrel-files-why-indexts-re-exports-hurt-tree-shaking-nextjs-dev-memory-and-tsc-2026-3kpm）

知识点9：next/script 组件提供四种加载策略控制第三方脚本优先级：beforeInteractive（关键脚本如 bot 检测/同意管理，在水合前注入初始 HTML）、afterInteractive（默认，页面可交互后立即加载，适合 GA/GTM）、lazyOnload（浏览器空闲时加载，适合非关键分析/广告）、worker（Partytown 将脚本移到 Web Worker，适合完全不阻塞主线程的第三方脚本）。正确选择策略可显著改善 INP。（来源：https://nextjs.org/docs/app/guides/scripts 、https://www.patterns.dev/posts/third-party）

知识点10：第三方脚本 "import on interaction" 模式——聊天组件、反馈表单、支持工具等非首屏必需的脚本，只在用户实际交互（点击/悬停/滚动到视口）时才加载。最快的脚本是从不加载的脚本。实现方式：显示轻量占位符，用户点击后动态注入 script 标签或动态 import() 加载组件。对 INP 改善极大，因为脚本永远不占用主线程。（来源：https://www.codeava.com/blog/third-party-scripts-inp-optimization 、https://webperfclinic.com/pl/article/optymalizacja-skryptow-zewnetrznych-2026-partytown-web-workers-inp）

知识点11：CSS Purge（未使用样式清除）——Tailwind CSS 未 purge 时构建可达 3-4MB，配置 content 字段扫描 HTML/JS/模板文件后生产构建通常 <10KB（gzip后）。PurgeCSS 原理：扫描内容文件中出现的 CSS 类名，移除未出现的选择器。注意：动态生成的类名（如 `text-${color}-500`）无法被静态扫描，需用 safelist 或完整类名映射。（来源：https://v1.tailwindcss.com/docs/controlling-file-size 、https://cssawwwards.com/blog/css-performance-optimization-guide-2026）

知识点12：Critical CSS 内联——提取 above-the-fold（首屏可见区域）渲染所需的最小 CSS 集合，直接内联到 HTML <head> 中，浏览器无需等待外部样式heet即可立即绘制。14KB 规则：TCP 初始拥塞窗口约 14KB，内联 CSS 控制在此大小内可在第一个 TCP 包中传输完成。工具：Critical、Penthouse、Critters（Next.js 插件）。非关键 CSS 异步加载（media="print" onload="this.media='all'" 技巧）。（来源：https://webperfclinic.com/article/eliminate-render-blocking-css-critical-css-extraction-async-loading-guide 、https://www.javascriptroom.com/css-mastery/practical-approaches-to-optimize-css-performance/）

知识点13：路由级代码分割（Route-based code splitting）——每个路由独立 chunk，用户访问某 URL 时只下载该路由代码而非全站。在 12 页 React 应用测试中，路由级分割使初始 bundle 减少 28%，LCP 从 4.2s 降到 2.9s。Next.js App Router 的 Server Components 自动实现路由级分割；Pages Router 的每个 pages/ 文件也自动分割。SPA 需手动用 React.lazy + Suspense 包裹路由组件。（来源：https://web.developers.google.cn/learn/performance/code-split-javascript 、https://dev.to/kui_luo/how-to-reduce-your-javascript-bundle-size-by-70-in-10-steps-3j1g）

知识点14：组件级代码分割（Component-level code splitting）——将重型、低频使用的 UI 元素（Modal 对话框、富文本编辑器、图表库、日期选择器、代码高亮器）组织到独立 chunk，仅在需要时加载。与路由级分割互补：路由分割解决跨页面的代码隔离，组件分割解决单页面内的按需加载。判断标准：组件初始渲染不可见 + 体积 >20KB gzip + 用户交互后才需要 → 应该懒加载。（来源：https://kindatechnical.com/web-development/javascript-performance-code-splitting-tree-shaking-bundle-analysis.html 、https://webperfclinic.com/hu/article/javascript-bundle-optimalizalas-2026-tree-shaking-code-splitting-dinamikus-import）

知识点15：Bundle size 持续监控——在 CI 中集成 bundlewatch 或 size-limit，当 PR 引入的依赖使 bundle 超过阈值时自动阻止合并。配置示例：size-limit 设置每个路由 <130KB（Next.js 16 推荐目标）、总 bundle <300KB。配合 Lighthouse CI 的 total-byte-weight 断言（当前项目 .lighthouserc.json 已设 <3MB）形成多层防护。开发者本地用 Import Cost 插件实时感知每个 import 的体积代价。（来源：https://nextjslaunchpad.com/article/nextjs-bundle-analyzer-reduce-javascript-size 、https://nextjs.org/docs/app/guides/production-checklist）

落地计划：
- P2-PERF-BUNDLE-ANALYZE-001：运行 @next/bundle-analyzer 分析当前生产 bundle，输出 treemap 报告，定位 Top 10 最大依赖（重点检查 framer-motion、lucide-react、react-dom、next 等），评估哪些可替换为更轻量替代或 deep import。具体任务：(a) ANALYZE=true npm run build 生成报告 (b) 记录每个路由的 First Load JS (c) 标记 >50KB 的第三方依赖为优化候选。
- P2-PERF-DYNAMIC-IMPORT-001：对重型客户端组件使用 next/dynamic 懒加载。具体任务：(a) 审计 app/ 下所有 "use client" 组件 (b) 识别首屏不可见的重型组件（搜索弹窗、筛选面板、对比工具、Modal）(c) 用 next/dynamic({ ssr: false, loading: <Skeleton/> }) 包裹 (d) 验证 tsc 通过 + 线上 LCP 改善。
- P2-PERF-SCRIPT-STRATEGY-001：审计 layout.tsx 中所有第三方脚本（GA4、Umami、AdSense、Baidu、Impact），将非关键脚本改为 lazyOnload 策略。具体任务：(a) 列出 layout.tsx 中所有 <Script> 和 <script> (b) 分类：beforeInteractive（无）/afterInteractive（GA4/Umami）/lazyOnload（AdSense/Baidu/Impact）(c) 将 AdSense 和 Baidu 改为 lazyOnload (d) 验证广告仍正常展示 + INP 改善。



[2026-09-23] Monorepo与Turborepo/Nx最佳实践（pnpm workspaces + 任务缓存 + Changesets版本管理 + 依赖边界）

知识点1：Monorepo 标准目录结构——apps/* 放可部署应用（Next.js web、API server、docs站、admin后台），packages/* 放共享库（ui组件、utils工具、database client、config配置）。铁律：apps 只能 import packages/*，packages 永远不能 import apps/*，保持单向依赖边界。可选 tools/ 放脚本和代码生成器，infra/ 放 Terraform/Docker，不被应用运行时代码 import。Nx 官方称之为 grouped layout。（来源：https://nx.dev/docs/kb/folder-structure 、https://palakorn.com/blog/monorepo-strategy-pnpm-turbo-nx/）

知识点2：pnpm workspaces 是 Monorepo 的包管理基础设施。根目录必须有 pnpm-workspace.yaml，用 packages 字段定义 glob 模式（如 "apps/*", "packages/*"）。workspace:* 协议将本地包符号链接到 node_modules 而非从 npm 下载，发布时自动替换为真实 semver。pnpm 硬链接+内容寻址存储比 npm/yarn 节省 50%+ 磁盘空间，安装速度快 2-3 倍。（来源：https://pnpm.io/zh/workspaces 、https://pnpm.io/es/settings）

知识点3：pnpm Catalogs（pnpm 10+ 新特性）——在 pnpm-workspace.yaml 的 catalog 字段统一声明第三方依赖版本号（如 react: ^19.0.0），各包的 package.json 中用 "react": "catalog:" 引用。好处：全仓库版本单一来源，升级只需改一处，避免版本碎片化和幽灵依赖。catalog 条目也可指向 workspace:^ 范围。（来源：https://pnpm.io/ru/catalogs 、https://pnpm.io/10.x/settings）

知识点4：Turborepo 核心能力三件套：(1) 任务管道调度（task pipeline）——turbo.json 中用 dependsOn 声明任务间依赖（如 build 依赖 ^build 即先构建依赖包），自动拓扑排序+并行化无依赖任务；(2) 内容寻址缓存（content-addressable cache）——基于源文件 hash、配置、环境变量计算任务指纹，命中则跳过执行直接恢复产物；(3) 远程缓存（Remote Cache）——跨机器/CI 共享缓存。（来源：https://turborepo.dev/docs/index.md 、https://turborepo.dev/）

知识点5：Turborepo 缓存指纹计算——每个任务的 hash 输入包括：源文件内容、任务配置（turbo.json）、依赖包版本、环境变量（env 字段声明的）、全局文件。hash 命中后恢复文件产物（outputs 字段声明的目录如 dist/、.next/）和终端输出（stdout/stderr 原样回放，包括 Windows 兼容）。--cache local:rw,remote:rw 控制读写哪些缓存源，--force 跳过缓存，--dry=json 预演不执行。（来源：https://turborepo.dev/docs/reference/run 、https://turborepo.dev/docs/reference/configuration）

知识点6：Turborepo Remote Cache——Vercel 提供的托管缓存服务，Vercel 账号自动启用，turbo login 授权后 CI 和本地共享同一缓存。核心价值：CI 中跑过的构建，开发者本地直接命中缓存，反之亦然，"CI 永远不需要重复做相同工作"。也可自托管——Turborepo 开放了 remote-cache-spec 协议（MIT），可用任意对象存储+简单 HTTP 服务器实现。（来源：https://vercel.com/docs/monorepos/remote-caching 、https://turborepo.dev/api/remote-cache-spec）

知识点7：Turborepo 2.8 新特性——Git worktrees 共享本地缓存。AI agent 并行工作时常用 git worktree 同时检出多个分支，但每个 worktree 原本有独立缓存实例导致缓存丢失。2.8 起同一仓库的所有 worktree 共享同一个本地缓存，大幅提升多 agent 协作效率。这对我们多窗口/多 agent 并行开发模式有直接参考价值。（来源：https://turborepo.dev/blog/2-8）

知识点8：Nx 核心能力——项目图（project graph，分析 package.json 依赖和 tsconfig paths 构建全仓库依赖关系）+ 任务图（task graph，从项目图派生执行计划）+ 计算缓存（computation caching，与 Turborepo 类似但更精细）+ affected 命令（只跑变更影响的项目）。Nx 比 Turborepo 更重，提供 100+ 官方插件（React/Next/Node/Vite/Jest等）、代码生成器（nx g）、依赖边界强制等企业级功能。GitHub 24k+ stars。（来源：https://nx.dev/docs/concepts/mental-model 、https://nx.dev/concepts/mental-model）

知识点9：Nx affected 命令——nx affected:build / affected:test / affected:lint 通过 git diff 计算哪些项目的源文件变更了，只运行这些项目及其依赖项目的任务。对于大型 monorepo（50+ 包），一次小改动可能只影响 2-3 个项目，CI 时间从全量 30 分钟降到 2 分钟。结合 remote caching，未变更项目直接缓存命中零耗时。（来源：https://nx.dev/docs/concepts/ci-concepts/building-blocks-fast-ci ）

知识点10：Nx vs Turborepo 选型对比——两者都做任务调度+缓存，但定位不同：Turborepo 轻量（~一个 turbo.json 配置）、上手快、与 Vercel 深度集成，适合中小团队和已有项目渐进式引入；Nx 更重但功能全（插件生态、代码生成、依赖边界强制、可视化项目图 nx graph），适合大型企业级 monorepo。缓存精度上 Nx 默认配置更少误报缓存命中（false positives），Turborepo 对注册任务默认启用缓存需用 cache: false 退出 dev 等不可缓存任务。（来源：https://nx.dev/docs/guides/comparisons/nx-vs-turborepo）

知识点11：Changesets 是 Monorepo 版本管理与发布的事实标准（GitHub 8k+ stars，由 Atlassian 维护）。工作流：开发者运行 pnpm changeset 选择受影响包+semver级别（patch/minor/major）+写描述，生成 .changeset/ 下一个 markdown 文件随 PR 提交；发布时 changeset version 消费所有 changeset，自动升级版本号+更新依赖该包的下游包+生成 CHANGELOG.md；changeset publish 发布到 npm，跳过未变更的包。（来源：https://github.com/changesets/changesets 、https://pnpm.io/using-changesets）

知识点12：Changesets GitHub Action 实现全自动发布——PR 合并到 main 后，changesets/action 自动创建或更新 "Version Packages" PR（包含版本升级和 CHANGELOG）；维护者合并该 PR 后，action 自动运行 changeset publish 发布到 npm（支持 npm provenance）+ 创建 GitHub Release + git tag。实现"写 changeset → 合并 → 自动发布"的零手动发布流程。（来源：https://github.com/changesets/action 、http://raw.githubusercontent.com/RemyFevry/fil/HEAD/.changeset/README.md）

知识点13：Monorepo 依赖边界强制——用 ESLint 插件（eslint-plugin-boundaries 或 Nx 内置的 @nx/enforce-module-boundaries）在代码层面强制架构规则：apps 不能 import 其他 apps、packages 不能 import apps、深层路径禁止（只能通过 package.json exports 字段公开的入口 import）。违反规则直接 lint 报错，防止架构腐化。配合 TypeScript paths 映射 @scope/package 名称。（来源：https://nx.dev/docs/kb/folder-structure 、https://palakorn.com/blog/monorepo-strategy-pnpm-turbo-nx/）

知识点14：Monorepo TypeScript 配置模式——根 tsconfig.base.json 定义通用 compilerOptions（strict、target、moduleResolution等），每个包的 tsconfig.json 用 extends 继承根配置并覆盖 paths。paths 字段将 @aitoolcrux/ui 映射到 packages/ui/src。使用 TypeScript Project References（references 字段）实现增量编译和跨包类型检查，tsc --build 只重建变更的包。共享配置本身也可作为一个 packages/tsconfig 包发布。（来源：https://www.pkgpulse.com/guides/how-to-set-up-monorepo-turborepo-2026 、https://lenkastudio.com/blog/how-to-build-typescript-monorepo-turborepo-2026）

知识点15：Monorepo CI 优化三板斧——(1) Affected 过滤：Nx affected 或 Turbo --filter 只运行变更影响的项目，避免全量构建；(2) Remote Cache：跨任务/跨机器/跨 CI run 共享构建产物，相同输入永不重复执行；(3) 并行化+矩阵：无依赖任务并行执行，大任务可拆分为 matrix build。三者叠加效果：50+ 包的 monorepo CI 从 45 分钟降到 3-5 分钟。缓存命中率是核心 KPI——成熟团队可达 80%+。（来源：https://nx.dev/docs/concepts/ci-concepts/building-blocks-fast-ci 、https://turborepo.dev/docs/index.md）

落地计划：
- P2-ENG-MONOREPO-001：评估将 ai-tools-review（主站）+ open-seo-local（SEO审计工具）+ context_manager（上下文生成）整合为 pnpm workspace monorepo 的可行性。当前三个项目分散在不同目录，共享配置（tsconfig、eslint、tailwind）重复。具体任务：(a) 分析三个项目的依赖重叠度；(b) 设计 apps/web + packages/config + packages/seo-tools 结构；(c) 评估迁移成本和 Vercel monorepo 部署配置。
- P2-ENG-TURBO-CACHE-001：引入 Turborepo 加速 GitHub Actions CI。当前 lighthouse-ci.yml 和其他 workflow 每次全量 npm install + build，无缓存。具体任务：(a) 根目录添加 turbo.json 定义 build/lint/typecheck 任务管道；(b) CI 中启用 Vercel Remote Cache（--cache-dir + TURBO_TOKEN）；(c) 用 turbo run build --filter=...[origin/main] 只构建变更包。
- P2-ENG-CHANGESETS-001：引入 Changesets 管理版本和 CHANGELOG。当前直接 commit main 无版本号无 CHANGELOG。具体任务：(a) pnpm add -Dw @changesets/cli + pnpm changeset init；(b) 添加 .github/workflows/release.yml 使用 changesets/action 自动创建 Version Packages PR；(c) 约定每个功能 PR 必须带 changeset 文件。



[2026-09-23] 监控告警与可观测性工具体系（Uptime Kuma / Sentry / Grafana LGTM / OpenTelemetry / Vercel Speed Insights）

知识点1：Uptime Kuma 是最流行的自托管 uptime 监控工具，MIT 协议，84k+ GitHub stars，Node.js 技术栈。支持 HTTP/HTTPS、TCP、Ping、DNS、Docker容器、SSL证书过期、关键字检测、gRPC、Push 等 10+ 监控类型，监控间隔最短 20 秒（企业级粒度）。一行 Docker 命令部署，内置美观状态页，无需额外组件。（来源：https://uptimekuma.org/ 、https://github.com/louislam/uptime-kuma）

知识点2：Uptime Kuma 支持 90+ 通知渠道，包括 Telegram、Discord、Slack、Email(SMTP)、钉钉、飞书、企业微信、Webhook、Gotify、Pushover、PagerDuty、ntfy 等。支持多用户角色权限、HTTPS(Let's Encrypt)、IPv6、多状态页映射到不同域名。核心局限：单点监控——如果运行 Uptime Kuma 的服务器宕机，告警也会停止；SaaS 方案（Better Stack、Freshping）从全球分布式节点检测。（来源：https://uptimekuma.io/uptime-kuma-features/ 、https://ossalt.com/blog/uptime-kuma-self-hosted-monitoring-homelab-2026）

知识点3：Sentry 是前端错误追踪+性能监控的行业标准，支持 JavaScript/React/Next.js/Vue/Angular 等所有主流框架。核心能力：错误聚合与堆栈追踪、分布式 tracing（前端→API→DB 全链路）、Session Replay（类视频用户会话回放）、Profiling（CPU 函数级耗时）、Application Metrics（自定义 counters/gauges/distributions）、User Feedback widget。Next.js 专用 SDK @sentry/nextjs 支持 App Router 和 Pages Router。（来源：https://docs.sentry.io/platforms/javascript/guides/nextjs/ 、https://sentry.io/for/frontend/）

知识点4：Sentry 性能监控配置关键参数：tracesSampleRate 开发环境 1.0（全量采样）、生产环境 0.1（10%采样控制成本）；tracePropagationTargets 控制哪些 URL 启用分布式 tracing（正则匹配）；browserTracingIntegration() 启用浏览器端自动 tracing；replaysSessionSampleRate 和 replaysOnErrorSampleRate 控制 Session Replay 采样率。Sentry 自动生成前端 Core Web Vitals、transaction duration、error rate 仪表盘。（来源：https://docs.sentry.io/product/sentry-basics/performance-monitoring/ 、https://docs.sentry.dev/platforms/javascript/guides/nextjs/manual-setup/）

知识点5：Sentry 2026 新特性：Application Metrics（默认启用，Sentry.metrics.count/gauge/distribution，每个 metric 与 trace 关联，可从峰值直接跳转到相关 trace 和 error）；Logs（enableLogs: true，结构化日志与错误和 trace 并排显示）；AI 监控（LLM call latency、token usage）。错误监控从"捕获异常"演进为"全信号可观测平台"。（来源：https://docs.sentry.io/product/sentry-basics/ 、https://docs.sentry.io/product/）

知识点6：Grafana LGTM 栈是开源可组合可观测性栈：Loki（日志，水平扩展多租户日志聚合，AGPLv3）、Grafana（仪表盘与可视化，查询任意数据源）、Tempo（分布式追踪，仅需对象存储，接入 Jaeger/Zipkin/OpenTelemetry 协议）、Mimir（指标，Prometheus 兼容的长期存储）、Pyroscope（持续 profiling，CPU/内存函数级分析）。设计理念：开放标准（OTel、Prometheus）、无锁定、每个组件可独立替换。（来源：https://grafana.com/about/grafana-stack/ 、https://grafana.com/oss/）

知识点7：Grafana docker-otel-lgtm 是单个 Docker 镜像，预装 OpenTelemetry Collector + Prometheus + Loki + Tempo + Grafana，用于开发/演示/测试环境一键启动可观测性后端。OTel Collector 监听 4317(gRPC) 和 4318(HTTP) 端口，自动转发 metrics→Prometheus、spans→Tempo、logs→Loki。生产环境应使用 Grafana Cloud 或独立部署各组件。（来源：https://grafana.com/docs/opentelemetry/docker-lgtm/ 、https://grafana.com/blog/2024/03/13/an-opentelemetry-backend-in-a-docker-image-introducing-grafana/otel-lgtm/）

知识点8：Loki 的核心设计区别于 ELK：不索引日志内容，只索引每条日志流的标签（与 Prometheus 相同的数据模型），因此存储成本极低、水平扩展容易。查询时用 LogQL（类 PromQL）按标签过滤后再做内容搜索。适合海量日志的低成本长期存储，但不适合需要全文检索的场景。（来源：https://grafana.com/oss/loki/ 、https://grafana.com/blog/2025/07/08/observability-in-under-5-seconds-reflecting-on-a-year-of-grafana/otel-lgtm/）

知识点9：Tempo 是 Grafana 出品的分布式追踪后端，成本高效——仅需对象存储（S3/GCS/Azure Blob）即可运行，无需 Elasticsearch 或 Cassandra 等重型索引。深度集成 Grafana、Prometheus、Loki：可从日志中的 traceID 直接跳转到 Tempo trace，也可从 trace 中的 span 跳转到相关日志。支持从指标（exemplar）到 trace 的跳转。（来源：https://grafana.com/oss/tempo/ 、https://grafana.com/products/cloud/features/）

知识点10：OpenTelemetry 浏览器端埋点需要 @opentelemetry/sdk-trace-web（WebTracerProvider）+ @opentelemetry/instrumentation-document-load（自动采集页面加载 trace）+ ZoneContextManager（上下文传播）。OTLP HTTP exporter 发送到 collector 4318 端口。元包 @opentelemetry/auto-instrumentations-web 一键包含所有浏览器自动埋点库。浏览器端 OpenTelemetry 目前 Traces 稳定、Metrics 稳定、Logs 仍在发展中。（来源：https://opentelemetry.io/docs/languages/js/getting-started/browser/ 、https://opentelemetry.io/docs/languages/js/instrumentation/）

知识点11：OpenTelemetry 浏览器端部署两个必踩坑：(1) CSP——必须在 connect-src 中加入 OTel collector 端点，否则浏览器会阻止上报请求；(2) CORS——如果网站和 collector 跨域，collector 必须配置正确的 CORS 响应头（Access-Control-Allow-Origin），否则浏览器拦截。这两个是 OTel 浏览器埋点"数据发不出去"的最常见原因。（来源：https://opentelemetry.io/docs/instrumentation/js/exporters/ 、https://opentelemetry.io/fr/docs/languages/js/exporters/）

知识点12：Vercel Speed Insights 是 Vercel 官方 RUM（真实用户监控），基于 Core Web Vitals，所有套餐可用（含免费版 10k events/月）。启用后自动注入 /_vercel/speed-insights/* 路由收集数据，无需手动埋点。提供按页面、设备、国家、连接速度细分的性能仪表盘。与 Vercel Web Analytics（用户行为分析）互补：Speed Insights 看性能，Web Analytics 看流量。（来源：https://vercel.com/docs/speed-insights 、https://vercel.com/docs/speed-insights/quickstart）

知识点13：Vercel Speed Insights 监控指标：LCP（最大内容绘制）、FCP（首次内容绘制）、TBT（总阻塞时间，目标 <800ms）、TTFB（首字节时间，目标 <800ms）、CLS（累积布局偏移）。与 Lighthouse 实验室数据不同，Speed Insights 是 field data（真实用户数据），反映实际用户在各种设备/网络条件下的体验。（来源：https://vercel.com/docs/speed-insights/metrics ）

知识点14：Field data（RUM/真实用户监控）vs Lab data（实验室测试）的本质区别：Field data 来自真实访客的实际使用（CrUX 数据集、Google Core Web Vitals 评估完全基于 field data），捕捉设备能力、网络速度、地理位置、浏览行为的差异；Lab data 来自受控环境（Lighthouse、WebPageTest），可复现但不代表真实用户。优化决策应以 field data 为主、lab data 为辅。（来源：https://vercel.com/kb/guide/how-to-improve-core-web-vitals ）

知识点15：前端监控体系分层架构（从外到内）：(1) Uptime 层——Uptime Kuma/GitHub Actions，检测站点是否可达（20s-10min 间隔）；(2) 错误追踪层——Sentry，捕获 JS 异常和 API 错误；(3) RUM 性能层——web-vitals（自建）或 Vercel Speed Insights（官方），采集真实用户 Core Web Vitals；(4) 行为分析层——GA4/Umami/Plausible，用户行为与转化；(5) 基础设施层——Grafana LGTM/Prometheus，服务器指标/日志/trace；(6) 标准化层——OpenTelemetry，统一埋点协议，避免供应商锁定。（来源：综合 https://grafana.com/about/grafana-stack/ + https://sentry.io/for/frontend/ + https://vercel.com/docs/speed-insights + https://uptimekuma.org/）

落地计划：
- P2-PERF-SPEEDINSIGHTS-001：接入 Vercel Speed Insights（@vercel/speed-insights），获得官方 RUM 可视化面板，与现有自建 web-vitals RUM 互补（现有上报到 GA4，Speed Insights 提供按页面/设备/国家细分）。具体任务：npm install @vercel/speed-insights，在 layout.tsx 导入并渲染 <SpeedInsights />，Vercel 项目设置中启用 Speed Insights tab。
- P2-MONITOR-SENTRY-001：接入 Sentry Next.js SDK 做前端错误追踪+Session Replay，当前网站无任何 JS 错误监控。具体任务：npm install @sentry/nextjs，npx @sentry/wizard@latest -i nextjs，配置 tracesSampleRate=0.1（生产），启用 Session Replay（replaysOnErrorSampleRate=1.0），DSN 存入 Vercel Environment Variable 不硬编码。
- P2-MONITOR-UPTIME-KUMA-001：评估用 Uptime Kuma 替代现有 GitHub Actions uptime-monitor.yml（当前 10 分钟间隔，Uptime Kuma 可 20 秒间隔+90+通知渠道+SSL证书监控）。具体任务：Docker 部署 Uptime Kuma 到自有 VPS，配置 aitoolcrux.com HTTP 监控（20s间隔），配置 Telegram/Email 告警，SSL 证书到期前 30 天提醒。
- P2-OBSERVABILITY-OTEL-001（长期）：规划 OpenTelemetry 标准化埋点，统一前端 trace/metrics/logs 协议，为未来接入 Grafana LGTM 栈或任何 OTel 兼容后端做准备。当前优先级低，先完成 Sentry + Speed Insights。



---

### [2026-09-22] Vercel 部署优化完整指南（Build Cache + ISR + Edge + 冷启动）

**知识点1：Vercel Build Cache 自动缓存 node_modules 和 .next/cache**
Vercel 自动在每次部署间缓存 `node_modules/**` 和框架缓存目录（`.next/cache`、`.astro/` 等）。首次构建缓存为空所以较慢，后续构建命中缓存可大幅提速。缓存上限 1GB/项目，保留 1 个月，LRU 淘汰。（来源：https://vercel.com/docs/deployments/troubleshoot-a-build）

**知识点2：Build Cache Key 由项目配置和依赖决定，改 package.json 会失效**
缓存 key 基于项目配置（framework、build command、install command）和依赖锁文件（package-lock.json/yarn.lock/pnpm-lock.yaml）派生。修改 package.json 或锁文件会导致缓存未命中，需要完整重新安装依赖。不要在构建脚本中动态生成非必要文件，以免意外失效缓存。（来源：https://vercel.com/docs/deployments/troubleshoot-a-build + https://aitoolsguidebook.com/en/articles/vercel-build-exceeded-time-limit/）

**知识点3：ISR（增量静态再生）无需全量重建即可更新静态页面**
ISR 允许在构建后创建或更新静态页面，不需要重建整个站点。对于大量内容页面（如我们 533 个工具页 + 105 篇文章），ISR 可以避免 `next build` 时间过长。App Router 中通过 `export const revalidate = 86400` 启用，Pages Router 中通过 `getStaticProps` 返回 `revalidate`。（来源：https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration + https://vercel.com/docs/incremental-static-regeneration）

**知识点4：ISR 自动设置 Cache-Control: s-maxage + stale-while-revalidate**
启用 ISR 后，Vercel 自动为页面设置 `Cache-Control: s-maxage=<revalidate>, stale-while-revalidate` 响应头。这意味着 CDN 边缘缓存页面，过期后后台异步重新生成（stale-while-revalidate），用户始终获得快速响应。纯 SSG 页面则设置 `Cache-Control: s-maxage=31536000, stale-while-revalidate`。（来源：https://nextjs.org/docs/14/app/building-your-application/deploying + https://vercel.com/docs/incremental-static-regeneration）

**知识点5：On-demand ISR 精确失效：revalidatePath() 和 revalidateTag()**
除了时间驱动的 revalidate，Next.js 支持按需精确失效：`revalidatePath('/tools/midjourney')` 失效单个路径，`revalidateTag('tools')` 失效所有标记了该 tag 的 fetch 数据。可通过 API Route + secret 环境变量触发，用于 CMS 内容更新后即时刷新页面。（来源：https://vercel.com/docs/incremental-static-regeneration/quickstart + https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration）

**知识点6：Data Cache（App Router）自动启用，与 ISR 和 CDN Cache 三层协同**
Vercel 上 App Router 项目自动启用 Data Cache，在 ISR 之外额外缓存 segment 级别的 fetch 数据。三层缓存协同：完全静态页用 ISR，动态 fetch 用 Data Cache，最终输出用 CDN Cache。`unstable_cache()` 可缓存非 fetch 的数据（如数据库查询、文件读取）。（来源：https://vercel.com/docs/runtime-cache/data-cache）

**知识点7：Turborepo Remote Caching 跨团队共享构建缓存**
Turborepo Remote Caching 自动在整个 Vercel 团队间共享构建产物（build output + logs），避免在不同 CI 机器上重复编译/测试。对于 monorepo，配合 `turbo run build` 可实现 50x 加速（未变更的包直接命中缓存）。非 monorepo 项目也可受益于 Remote Caching 的 CI 缓存复用。（来源：https://vercel.com/docs/monorepos/remote-caching + https://vercel.com/academy/production-monorepos/deploy-web-app）

**知识点8：Serverless 函数冷启动优化：控制函数体积 + Edge Runtime**
Vercel Serverless 函数冷启动时间与函数体积直接相关。优化方法：(a) 使用 `@next/bundle-analyzer` 分析包体积，移除重型依赖；(b) 对低延迟要求的路由使用 Edge Runtime（`export const runtime = 'edge'`），冷启动 <50ms vs Serverless 200-500ms；(c) 动态导入重型组件（`next/dynamic`）减少初始包体积。（来源：https://github.com/jeremylongshore/claude-code-plugins-plus-skills Vercel Performance Tuning）

**知识点9：Vercel 构建超时限制：Hobby 45 分钟，Pro 无硬性限制但建议 <10 分钟**
Vercel Hobby 计划构建超时为 45 分钟，超过会被取消。Pro 计划虽然没有硬性超时，但构建时间过长会影响开发速度和部署频率。对于大型 SSG 项目（如我们 533 工具页全量静态生成），建议使用 ISR 减少构建时页面数量，或使用 `fallback: 'blocking'` 按需生成。（来源：https://aitoolsguidebook.com/en/articles/vercel-build-exceeded-time-limit/）

**知识点10：Vercel Analytics 真实用户性能监控，识别部署后性能回归**
Vercel Analytics 提供真实用户监控（RUM），包括 Web Vitals（LCP/INP/CLS）和自定义事件。每次部署后可对比新旧版本的性能数据，识别部署引入的性能回归。Speed Insights 提供按页面、设备、地区的性能细分。（来源：https://vercel.com/docs/analytics）

**知识点11：环境变量管理：分环境 + Secret 保护 + 构建时 vs 运行时**
Vercel 环境变量分 Development/Preview/Production 三个环境。敏感数据（API Key、Token）应标记为 Secret（不显示在 Dashboard）。`NEXT_PUBLIC_` 前缀的变量在构建时内联到客户端 bundle，非前缀变量仅在服务器端可用。不要在客户端代码中引用非 `NEXT_PUBLIC_` 变量。（来源：https://vercel.com/docs/projects/environment-variables）

**知识点12：Vercel Deployment Hooks 自动化触发部署**
Vercel 支持 Deployment Hooks（部署钩子），通过唯一 URL 触发特定分支的部署。可用于 CMS 内容更新后自动触发重新部署，或外部 CI/CD 流水线完成后触发 Vercel 部署。每个 Hook 可配置为部署特定分支。（来源：https://vercel.com/docs/deployments/git#deploy-hooks）

**知识点13：Preview Deployments 每个 PR 自动生成预览环境**
Vercel 自动为每个 Git PR 生成唯一的 Preview Deployment URL（`project-git-branch.vercel.app`），可用于在合并前预览和测试。Preview 环境使用 Preview 环境变量，与 Production 隔离。Checks 可集成 Lighthouse、Bundle Analyzer 等自动化检查，在 PR 上显示通过/失败状态。（来源：https://vercel.com/docs/deployments/preview-deployments）

**知识点14：Vercel Edge Network 全球 CDN，静态资源自动边缘缓存**
Vercel 部署在全球 Edge Network（100+ 节点），静态资源（JS/CSS/图片）自动从最近的边缘节点提供，延迟 <50ms。静态页面通过 ISR/SSG 也在边缘缓存。动态路由（SSR/Serverless）执行在最近的 Serverless 区域，可配置 `regions` 优化延迟。（来源：https://vercel.com/docs/edge-network/overview）

**知识点15：AIToolCrux 项目 Vercel 优化落地清单**
我们项目当前纯 SSG（533 工具页 + 105 文章页全量构建），构建时间可能较长。优化方向：(a) 工具详情页和文章页加 `export const revalidate = 86400`（ISR 24小时），减少构建时页面数量（对应 state.json 中 P2-PERF-ISR-TOOLS-001/P2-PERF-ISR-POSTS-001）；(b) 优化 tools.json 7.86MB 加载（对应 P2-PERF-TOOLSJSON-OPTIMIZE-001）；(c) 确认 Vercel Build Cache 正常命中（检查部署日志中的 "Using build cache"）；(d) 配置 Vercel Analytics 监控每次部署后的 Web Vitals 变化；(e) 不要在构建脚本中动态生成文件以免失效 Build Cache。（来源：综合以上 Vercel + Next.js 官方文档）

**落地计划**：
- 知识点3+4（ISR）→ 下次迭代执行 P2-PERF-ISR-TOOLS-001（工具页加 revalidate=86400）和 P2-PERF-ISR-POSTS-001（文章页加 revalidate=86400）
- 知识点2（Build Cache Key）→ 下次部署后检查 Vercel 部署日志确认 Build Cache 命中，避免在构建脚本中动态生成文件
- 知识点10（Vercel Analytics）→ 下次迭代确认 Vercel Analytics 是否已启用，如未启用则在 Vercel Dashboard 开启
- 知识点15（tools.json 优化）→ 下次迭代执行 P2-PERF-TOOLSJSON-OPTIMIZE-001，分析 7.86MB tools.json 的加载优化方案


[2026-09-22] SEO工程化——结构化数据完整类型体系与2026 Google Rich Results最新政策（Organization/Website/Article/SoftwareApplication/ItemList/SiteNavigationElement + 2026政策更新）

知识点1：Organization结构化数据——添加到首页，帮助Google理解组织信息并在搜索结果中消歧。必需属性：name（组织名称）、url（官网URL）、logo（logo图片URL，必须是绝对URL，推荐112x112px以上，JPG/PNG/GIF，最大512KB）。推荐属性：sameAs（社交媒体链接数组，如Product Hunt/Twitter/LinkedIn/GitHub）、contactPoint（联系信息）、iso6523/naics（后台消歧用的行业编码）。影响视觉元素：logo显示在品牌知识面板中。我们项目首页应该加Organization schema（name: AIToolCrux, url: https://www.aitoolcrux.com, logo: /logo.png绝对URL, sameAs: [Product Hunt页面等]）。来源：https://developers.google.com/search/docs/appearance/structured-data/organization

知识点2：Website结构化数据与sitelinks search box已废弃——Website类型描述整个网站，必需属性：name、url。过去常用Website+SearchAction实现sitelinks search box（品牌词搜索结果中显示站内搜索框，用户可直接在搜索结果中搜索站内内容）。但**Google在2024年11月29日正式移除sitelinks search box功能**（官方文档已删除，nositelinkssearchbox规则已归档），原因是该功能在搜索结果中不再可用。所以现在加SearchAction到Website schema完全没有效果。Website schema仍可加name/url/publisher帮助Google理解网站主体，但不再有搜索框富摘要。我们项目不需要加SearchAction。来源：https://developers.google.com/search/updates#august-2021

知识点3：2026 Google结构化数据政策重大更新汇总——(a) 2024年11月移除sitelinks search box（Website+SearchAction不再有效）；(b) 2026年1月移除Practice Problem结构化数据支持（Search Console增强功能报告/Rich Result Test/搜索外观过滤器均不再支持Practice Problem类型，Search Console API延续到2026年1月后也移除）；(c) 2026年7月14日新增review snippet指南（与aggregateRating政策一致，ratingCount/reviewCount必须匹配页面真实可见用户评论，我们项目第80轮已移除违规aggregateRating）；(d) 2026年7月更新llms.txt指南（Google官方声明llms.txt不影响搜索排名）；(e) 2026年8月更新favicon文档和site reputation政策。结构化数据类型在持续淘汰，需要定期检查Google搜索中心更新日志（https://developers.google.com/search/updates）。来源：https://developers.google.com/search/updates

知识点4：Article结构化数据——用于新闻/博客/体育文章页面（我们项目105篇博客文章完美匹配）。必需属性：headline（标题，≤110字符，Google会截断超过110字符的标题，建议≤90字符）、image（至少1张图片，推荐1200x675或更大，多张时Google选最合适的，图片必须是页面实际显示的）、datePublished（ISO 8601格式，如2026-09-22T00:00:00+08:00）、author（Person或Organization，Person类型必须有name属性）。推荐属性：dateModified（更新日期，我们项目文章有publishedAt但需确认是否有dateModified字段）、publisher（Organization，需含logo，Google新闻要求）、mainEntityOfPage（页面URL，通常是canonical URL）。Article schema影响：标题文本显示、大图缩略图、Google新闻收录、Google助理引用。我们项目105篇博客文章应该加Article schema。来源：https://developers.google.com/search/docs/appearance/structured-data/article

知识点5：SoftwareApplication结构化数据——用于软件应用页面（我们项目533个工具详情页完美匹配，这是最大的结构化数据缺口）。必需属性：name（应用名称）、offers.price（价格，免费应用设"0"，需搭配offers.priceCurrency如"USD"）。推荐属性：applicationCategory（应用类别，如"DeveloperApplication"/"DesignApplication"/"BusinessApplication"/"MultimediaApplication"，我们工具有category字段可映射到Schema.org应用类别）、operatingSystem（如"Web"/"Windows"/"macOS"/"Linux"/"iOS"/"Android"，我们工具大多是Web应用）、description（应用描述，应与页面可见描述一致）、aggregateRating（**注意：2026年7月新review snippet指南要求ratingCount/reviewCount必须匹配页面真实可见用户评论，我们项目只有编辑评测ratingCount=1，已在第80轮移除aggregateRating，不要重新添加**）、offers（价格详情/免费试用/订阅模式，可含availability: "https://schema.org/Free"）。SoftwareApplication schema可以让工具详情页在搜索结果中显示价格、类别、操作系统等富摘要。来源：https://developers.google.com/search/docs/appearance/structured-data/software-app

知识点6：BreadcrumbList结构化数据2026最新——已学过（第二轮），补充：必需至少2个ListItem，每个ListItem需position（从1开始递增）、name（面包屑名称，显示给用户的文本）、item（URL，必须是绝对URL）。Google在桌面和移动端所有区域/语言支持面包屑富摘要。面包屑显示在搜索结果标题上方，替代传统URL显示。我们项目Schema.tsx已有BreadcrumbSchema，ComparisonSchema中还有第二处BreadcrumbList（需审计是否重复输出，重复的结构化数据可能导致Google忽略）。注意：面包屑路径必须与页面实际导航一致，不能为了SEO虚构路径（如工具页面包屑应该是Home > Tools > Tool Name，不能是Home > Category > Tool Name如果页面导航不是这样）。来源：https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

知识点7：ItemList/Carousel结构化数据——用于页面上的项目列表（如/tools工具列表页、/category分类页、"最佳AI工具"文章中的工具列表）。Carousel富摘要在搜索结果中显示为可横向滑动的项目卡片。必需属性：itemListElement（ListItem数组），每个ListItem需position（从1开始）、name（项目名称）、item（URL或Thing对象）。**关键规则：列表中所有项目必须是同一类型**（如都是SoftwareApplication，不能混合SoftwareApplication和Article，违反此规则Carousel会被忽略）。Carousel必须与Recipe/Course/Restaurant/Movie/Course等特定类型结合使用才能产生Carousel富摘要，通用ItemList本身不直接产生Carousel（但ItemList仍帮助Google理解页面列表结构）。我们项目/tools列表页和分类页可以加ItemList（SoftwareApplication类型列表），但需要确认是否符合Carousel条件（Google对Carousel的类型支持有限）。来源：https://developers.google.com/search/docs/appearance/structured-data/carousel

知识点8：通用结构化数据指南（Google sd-policies）——所有结构化数据必须遵守：(a) 内容必须对用户可见（不能标记用户看不到的内容，这是最常见的违规原因，如隐藏的评分或价格）；(b) 不能标记误导性内容（如虚假评分、虚假价格、与页面无关的实体）；(c) 不能标记违法/成人/仇恨内容；(d) 结构化数据必须准确反映页面内容（如Article的headline必须与页面<title>一致）；(e) 图片必须是页面上实际显示的图片，不能用库存图或不相关图；(f) 违反指南会导致手动操作（manual action），该页面的结构化数据会被Google忽略（但页面本身仍可出现在搜索结果中，只是没有富摘要）；(g) 不要在结构化数据中包含无关的实体（如在工具页标记Article）。我们项目第80轮移除aggregateRating就是因为违反了"ratingCount必须匹配页面真实可见用户评论"规则。来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies

知识点9：结构化数据格式与放置最佳实践——Google支持JSON-LD（推荐）、Microdata、RDFa三种格式，**JSON-LD是Google明确推荐的格式**（放在<script type="application/ld+json">中，可放在<head>或<body>，不影响页面渲染，易于维护）。可以在一个页面放多个<script type="application/ld+json">块（如Article+BreadcrumbList+Organization分别放不同块），也可以合并为一个JSON数组（[{...Article...}, {...BreadcrumbList...}]）。Next.js中推荐用组件渲染<script type="application/ld+json" dangerouslySetInnerHTML={{__html: JSON.stringify(schema)}} />，或在generateMetadata中输出。不要用next/script加载结构化数据（它是数据不是脚本，直接用<script>标签即可）。我们项目Schema.tsx用JSON-LD格式，正确。来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies

知识点10：结构化数据验证工具链——(a) Google Rich Results Test（https://search.google.com/test/rich-results）：检测页面是否有资格获得富摘要，显示具体类型、错误、警告，支持URL输入和代码片段输入；(b) Google Search Console→增强功能报告：显示已索引页面的结构化数据错误/警告/有效数量，按类型分类（如Article/Breadcrumb/FAQ），点击可查看具体页面错误；(c) Schema.org Validator（https://validator.schema.org/）：验证Schema.org语法正确性（不检查Google特定富摘要要求，比Rich Results Test更严格的语法检查）；(d) Chrome扩展：Structured Data Testing Tool替代品（如Schema.org Validator扩展）。验证流程：开发时用Rich Results Test代码片段验证→部署后用Rich Results Test URL验证→定期检查Search Console增强功能报告→发现错误及时修复。我们项目应该定期检查Search Console的增强功能报告（当前可能显示Article类型缺失、SoftwareApplication缺失等）。来源：https://developers.google.com/search/docs/appearance/structured-data

知识点11：SiteNavigationElement结构化数据——描述网站导航菜单结构。属性：name（导航项名称，如"Tools"/"Blog"/"Categories"/"About"）、url（导航项链接URL）、position（导航项位置，从1开始）。放在首页或全站布局中（如footer/header导航）。**重要：SiteNavigationElement不是Google官方支持的富摘要类型**（它不在Google搜索中心支持的结构化数据功能列表中），添加它不会产生特定的搜索结果展示。但Schema.org定义了此类型，Google和其他搜索引擎可能用它理解网站导航结构（辅助爬虫发现页面）。AI爬虫也可能用它理解网站结构。我们项目可以评估是否添加（低优先级），但不要期望它产生富摘要。优先级低于Organization/Article/SoftwareApplication。来源：https://schema.org/SiteNavigationElement

知识点12：FAQPage结构化数据2026最新——已学过（第二轮），补充：Google 2023年8月起FAQ富摘要仅限权威站（YMYL/健康/金融等领域的高权威网站），普通网站FAQPage不再在搜索结果中显示FAQ富摘要。但FAQPage对AI Overview/Perplexity/ChatGPT提取答案仍有重要价值（AI爬虫会优先读取结构化数据中的问答对作为答案来源）。必需属性：mainEntity（Question数组），每个Question需name（问题文本，必须与页面可见的FAQ问题一致）、acceptedAnswer.text（答案文本，必须与页面可见的FAQ答案一致）。我们项目Schema.tsx已有FAQSchema，但审计发现10篇文章中9篇FAQ不足（5篇完全没有FAQ章节，4篇只有1个问题，仅1篇有5个FAQ）。FAQ质量直接影响AI搜索引用率，应该优先补充。来源：https://developers.google.com/search/docs/appearance/structured-data/faqpage

知识点13：结构化数据与AI搜索（AIO/GEO）关联——已学过（AIO/GEO主题），补充与结构化数据的直接关联：AI爬虫（GPTBot/OAI-SearchBot/PerplexityBot/ClaudeBot等12个AI爬虫UA）会读取页面结构化数据来快速理解内容，而不需要解析整个HTML。FAQPage的问答对是AI提取答案的最重要来源（AI直接用Q&A对作为回答）。Article schema的headline/datePublished/author帮助AI理解文章元数据（用于引用时标注来源和日期）。SoftwareApplication的name/description/offers帮助AI理解工具信息（用于工具推荐场景）。Organization的sameAs帮助AI建立实体关联（知识图谱）。虽然Google官方声明llms.txt不影响搜索排名，但结构化数据质量直接影响AI搜索引用率和答案准确性。我们项目应该确保所有关键页面都有准确、完整的结构化数据，这是提升AI搜索可见性的最有效手段之一。来源：https://developers.google.com/search/docs/appearance/structured-data

知识点14：AIToolCrux项目结构化数据现状与缺口审计——当前components/seo/Schema.tsx包含：FAQSchema、BreadcrumbSchema、ComparisonSchema（含第二处BreadcrumbList）。第80轮已移除3处aggregateRating（ComparisonSchema的about数组aggregateRating、mainEntity.itemListElement aggregateRating、ProductSchema死代码aggregateRating）。当前缺口：(a) 首页没有Organization schema（name/logo/url/sameAs）——P1优先级；(b) 105篇博客文章没有Article schema（headline/image/datePublished/author/dateModified/publisher）——P1优先级，影响最大；(c) 533个工具详情页没有SoftwareApplication schema（name/offers/applicationCategory/operatingSystem/description）——P1优先级，影响最大；(d) /tools列表页和分类页没有ItemList——P2优先级；(e) 没有SiteNavigationElement——P3低优先级；(f) ComparisonSchema中可能有重复BreadcrumbList输出需审计——P2；(g) FAQ覆盖不足（9/10篇文章FAQ缺失或不足）——P1。落地优先级：Article > SoftwareApplication > Organization > FAQ补充 > ItemList。来源：项目代码审计 + Google官方文档

知识点15：结构化数据实施路线图与最佳实践——实施步骤：(a) 先在Schema.tsx中添加OrganizationSchema组件（首页用）、ArticleSchema组件（博客文章页用）、SoftwareApplicationSchema组件（工具详情页用）；(b) ArticleSchema从data/posts.json读取title/excerpt/date/author/hasRealScreenshots等字段映射到headline/description/datePublished/author/image；(c) SoftwareApplicationSchema从data/tools.json读取name/description/category/pricing等字段映射到name/description/applicationCategory/offers；(d) 在对应页面的layout或page组件中引入schema组件渲染<script type="application/ld+json">；(e) 部署后用Rich Results Test验证3类页面（首页Organization、文章页Article、工具页SoftwareApplication）；(f) 1周后检查Search Console增强功能报告确认无错误。最佳实践：用JSON-LD格式；每个页面只放相关类型；内容必须与页面可见一致；图片用绝对URL；日期用ISO 8601；不要重新添加aggregateRating；定期检查Google搜索中心更新日志（结构化数据类型持续淘汰）。来源：Google官方文档 + 项目代码审计

落地计划：
- P1-SCHEMA-ARTICLE-001：为105篇博客文章添加Article结构化数据（headline/image/datePublished/author/dateModified），提升Google新闻/AI搜索引用
- P1-SCHEMA-SOFTWAREAPP-001：为533个工具详情页添加SoftwareApplication结构化数据（name/offers/applicationCategory/operatingSystem/description），提升工具页富摘要
- P1-SCHEMA-ORGANIZATION-001：首页添加Organization结构化数据（name/logo/url/sameAs），帮助Google建立品牌实体知识图谱



[2026-09-22] GitHub Actions自动化——自定义Action开发与高级工作流模式（Composite/Docker/JS actions + Reusable workflows + Matrix + Concurrency + workflow_dispatch）

知识点1：三种自定义Action类型——Docker container actions（用Dockerfile封装环境，完全隔离可复现，但只支持Linux runner，首次构建镜像慢2-5分钟）、JavaScript actions（Node.js运行，启动快支持Linux/macOS/Windows，但需Node环境，需@vercel/ncc打包成单文件）、Composite actions（纯YAML组合多个步骤，最简单最轻量，支持跨平台，2021年GA后成为最常用类型）。每种都需要action.yml元数据文件定义inputs/outputs/runs。来源：https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions

知识点2：action.yml元数据语法——name（Action名称，显示在Marketplace）、description（描述）、inputs（输入参数，每个含description/required/default/deprecationMessage）、outputs（输出参数，composite中用value引用steps输出）、runs（执行配置：using: 'composite'|'node20'|'docker'）、branding（icon和color，Marketplace显示）。文件名必须是action.yml或action.yaml，推荐action.yml。Composite action的outputs必须用value显式引用steps输出，不能自动传递。来源：https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax

知识点3：Composite action开发详解——runs.using: "composite"，runs.steps是步骤数组，每个step可以run shell命令或uses其他action（包括嵌套调用其他composite action，但不能递归调用自己）。输入用${{ inputs.input-name }}引用。输出用value: ${{ steps.step-id.outputs.output-name }}。shell默认bash（Linux/macOS），Windows需指定shell: pwsh或cmd。适合封装重复的多步骤流程（如checkout+setup-node+npm ci+缓存），我们项目5个workflow都有重复的setup步骤可以抽取为composite action。来源：https://docs.github.com/es/actions/tutorials/create-actions/create-a-composite-action

知识点4：Docker container action开发——runs.using: "docker"，runs.image指定Dockerfile路径（如'Dockerfile'）或公共镜像（如'docker://alpine:3.19'）。runs.args传递参数给容器ENTRYPOINT，runs.env设置环境变量。Dockerfile中ENTRYPOINT执行脚本，CMD可被args覆盖。只支持Linux runner（不支持macOS/Windows）。优点是环境完全隔离可复现（不依赖runner预装软件），缺点是构建镜像慢（首次2-5分钟）、体积大。适合需要特定系统依赖（如Python+特定C库+CLI工具）的场景。来源：https://docs.github.com/es/actions/sharing-automations/creating-actions/creating-a-docker-container-action

知识点5：JavaScript action开发——runs.using: "node20"（node16已弃用），runs.main指定入口JS文件（如'dist/index.js'）。核心工具包：@actions/core（getInput/setOutput/setFailed/info/warning/error）、@actions/github（Octokit客户端+上下文）、@actions/exec（执行命令获取输出）、@actions/io（文件操作）、@actions/artifact（上传下载artifact）、@actions/cache（缓存）。必须用@vercel/ncc打包成单文件（避免提交node_modules到仓库，ncc build src/index.ts -o dist）。支持Linux/macOS/Windows。适合需要复杂逻辑/API调用的action。来源：https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions

知识点6：自定义Action发布与版本管理——发布到Marketplace需公开仓库+action.yml+README+通过GitHub验证。版本管理用Git tag（v1/v1.0/v1.0.0遵循语义化版本），用户用@v1引用主版本（自动获取v1.x最新patch）。最佳实践：维护v1分支指向最新v1.x tag，发布v2时创建v2分支。破坏性变更升主版本，新功能升次版本，bug修复升patch。我们项目第83轮已将actions/checkout@v4锁定到commit SHA 11d5960a...和setup-python@v5锁定到a26af69b...（比@v4更安全可复现但需Dependabot自动更新）。来源：https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions

知识点7：Reusable workflows（可复用工作流）——不同于custom action（步骤级复用），reusable workflow是job级复用完整工作流。被调用workflow用on: workflow_call定义inputs和outputs（secrets也可定义）。调用方用uses: owner/repo/.github/workflows/workflow.yml@ref引用。可以传secrets（inherit继承调用方所有secrets，或显式列出secrets: env-name）。限制：一个workflow最多调用10个reusable workflow，嵌套不超过4层，被调用的workflow中不能再调用其他reusable workflow（第4层是叶子）。适合跨仓库复用完整CI流程（如标准化的lint+test+build流程）。来源：https://docs.github.com/en/actions/using-workflows/reusing-workflows

知识点8：Matrix strategies（矩阵策略）——strategy.matrix定义变量组合（如os: [ubuntu-latest, macos-latest, windows-latest] × node: [20, 22, 24]），每个组合创建一个并行job（3×3=9个job并行）。fail-fast: false（一个组合失败不取消其他组合，默认true会取消所有正在运行的组合，调试时建议设false）。max-parallel限制最大并发数（免费账户Linux 20并发/macOS 5/Windows 5，超出会排队）。include添加额外组合（不在矩阵笛卡尔积中的特殊组合），exclude排除特定组合（如排除node 20+windows组合）。矩阵变量用${{ matrix.var-name }}引用。适合跨平台/跨版本测试。来源：https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs

知识点9：Concurrency（并发控制）——concurrency.group定义并发组（如ci-${{ github.ref }}按分支分组，或production-deploy按环境分组），concurrency.cancel-in-progress: true取消同组正在运行的旧workflow（PR推送新commit时取消旧的CI运行，节省Actions分钟数）。默认允许多个workflow同时运行（可能导致部署冲突或资源浪费）。deploy环境也可以用concurrency: environment.name确保同一环境只有一个部署。适合：PR的CI（新推送取消旧的）、部署（确保顺序不冲突）。不适合：需要完整运行的定时任务（取消会导致数据不完整）。来源：https://docs.github.com/en/actions/using-jobs/using-concurrency

知识点10：workflow_dispatch手动触发——on: workflow_dispatch允许在Actions页面手动触发workflow（点击Run workflow按钮）。可以定义inputs（输入参数，支持choice下拉选择/string文本/boolean布尔/environment环境类型），触发时在UI中填写参数。inputs.choice提供下拉选择（如environment: [staging, production]，default: staging）。适合：手动部署、手动运行审计/监控、带参数的一次性任务、调试workflow。我们项目的5个workflow都可以加workflow_dispatch方便手动触发（如uptime-monitor手动测试告警、gsc-fetch手动拉取最新数据、index-monitor手动查收录数）。来源：https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch

知识点11：环境与保护规则（environments）——在仓库Settings→Environments中定义环境（如production/staging/dev），可以设置required reviewers（需要指定人员审批才能部署到该环境）、wait timer（等待N分钟后自动部署，如等待30分钟让测试完成）、deployment branch（只允许特定分支部署到该环境，如只允许main部署到production）。Job中用environment: production引用（也可以environment: name: production, url: https://...）。部署时创建deployment事件，GitHub UI中显示部署历史和状态。适合：生产部署需要人工审批、staging自动部署production需审批、部署URL显示在PR中。我们项目Vercel自动部署main分支，可以加environment保护防止意外部署。来源：https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment

知识点12：Job依赖与并行控制——jobs.<job-id>.needs定义依赖（如deploy needs: [build, test]，build和test都完成后才deploy）。needs可以是数组（多依赖并行等待）。默认所有jobs并行运行。needs.<job-id>.outputs可以获取上游job的outputs（需在被依赖job中定义outputs）。if条件控制job/step是否运行（如if: github.ref == 'refs/heads/main'只在main分支运行，if: failure()只在前面失败时运行）。continue-on-error: true允许job失败但不影响workflow整体状态（适合实验性测试如新版本Node兼容性）。timeout-minutes设置job超时（默认360分钟，建议设短如30防止卡死浪费分钟数）。来源：https://docs.github.com/en/actions/using-jobs

知识点13：Artifacts与缓存策略——actions/upload-artifact上传构建产物/测试报告/日志（保留90天，免费账户500MB上限，单文件最大2GB）。actions/download-artifact下载（支持指定name或all）。缓存用actions/cache（key唯一标识如${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}，restore-keys模糊匹配回退如${{ runner.os }}-node-）。缓存大小限制10GB/仓库（超出LRU淘汰最旧缓存）。npm缓存setup-node内置cache: 'npm'自动处理。Next.js缓存：.next/cache单独缓存（key含package-lock和next.config的hash）。我们项目5个workflow都有setup-node cache: 'npm'。来源：https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows

知识点14：Secrets管理最佳实践——Secrets在仓库Settings→Secrets and variables→Actions中设置（组织级Secrets可共享给多仓库，Environment级Secrets只在引用该environment的job中可用更安全）。Secrets不会出现在日志中（GitHub自动屏蔽为***），但如果用echo $SECRET打印会被屏蔽。不要用Secrets存储非敏感配置（用variables，variables可以在日志中显示）。GITHUB_TOKEN是自动生成的临时token（权限由permissions字段控制，默认contents: read+packages: read，需要写权限时显式声明permissions: contents: write）。我们项目的GitHub PAT硬编码在Python脚本中（github_pat_11CLL4GDA...），应该改为GitHub Secrets引用（${{ secrets.GITHUB_PAT }}），避免密钥泄露。来源：https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions

知识点15：AIToolCrux项目GitHub Actions现状与落地建议——当前5个workflow（context-update/gsc-fetch/index-monitor/seo-check/uptime-monitor），第83轮已锁定action版本到commit SHA+加Dependabot每周检查更新。落地优先级：(a) P2：创建composite action .github/actions/setup-env/action.yml（封装checkout+setup-node+npm ci+缓存），5个workflow复用减少重复代码；(b) P2：所有workflow加on: workflow_dispatch手动触发（方便手动测试和调试）；(c) P2：加concurrency控制（PR推送取消旧CI运行，节省Actions分钟数，定时任务不加）；(d) P3：将硬编码PAT改为GitHub Secrets引用（${{ secrets.GITHUB_PAT }}），避免密钥泄露；(e) P3：加timeout-minutes: 30防止workflow卡死浪费分钟数。来源：GitHub官方文档

落地计划：
- P2-CI-COMPOSITE-SETUP-001：创建composite action setup-env（封装checkout+setup-node+npm ci+缓存），5个workflow复用
- P2-CI-WORKFLOW-DISPATCH-001：所有workflow加workflow_dispatch手动触发，方便手动测试和调试
- P3-CI-SECRETS-REFACTOR-001：将硬编码GitHub PAT改为GitHub Secrets引用，加timeout-minutes防止卡死



[2026-09-22] 前端工程化最佳实践——代码质量流水线（ESLint 9 + Prettier 3 + Husky 9 + lint-staged + commitlint + CI集成）

知识点1：2026代码质量标准工具栈——ESLint（代码质量检查）+ Prettier（格式化）+ Husky（Git hooks管理）+ lint-staged（只检查暂存文件）+ commitlint（提交信息规范）是事实标准组合。Next.js 15+官方文档同时支持ESLint和Biome（Rust编写的更快linter+formatter二合一）作为linter选择。来源：https://nextjs.org/docs/app/getting-started/installation

知识点2：ESLint 9 Flat Config格式——ESLint 9默认使用flat config（eslint.config.mjs），替代旧的.eslintrc.*格式。配置是一个数组，每个元素包含files/rules/languageOptions/plugins。import js from '@eslint/js'获取推荐规则，import tseslint from 'typescript-eslint'获取TS规则。旧格式在ESLint 9中已弃用，新项目必须用flat config。来源：https://nextjs.org/docs/app/getting-started/installation

知识点3：ESLint与Prettier职责分离——ESLint负责代码质量（未使用变量、空catch、any类型、hooks依赖数组、console.log），Prettier负责格式（缩进、引号、分号、换行、尾逗号）。用eslint-config-prettier关闭ESLint中与Prettier冲突的格式规则，用eslint-plugin-prettier把Prettier作为ESLint规则运行（可选但不推荐，直接prettier --write更快）。两者不能同时管格式否则会打架。来源：https://www.mervcodes.com/blog/how-to-setup-eslint-prettier-2026/

知识点4：Husky v9+简化配置——npm install -D husky && npx husky init自动创建.husky/目录和pre-commit钩子脚本。package.json加"prepare": "husky"确保npm install后自动安装git hooks（新开发者clone后无需手动配置）。钩子文件是可执行shell脚本（.husky/pre-commit），内容如npx lint-staged。Husky v9不再需要husky install命令，也不需要.huskyrc配置文件。来源：https://reintech.io/blog/husky-lint-staged-pre-commit-hooks-setup

知识点5：lint-staged只检查暂存文件——配置在package.json的"lint-staged"字段或.lintstagedrc文件。按文件类型匹配命令："*.{ts,tsx}": ["eslint --fix", "prettier --write"]，"*.{json,md,css,yaml}": ["prettier --write"]。只对git add的文件运行，速度极快（全项目lint可能几分钟，lint-staged通常<5秒）。--no-stash选项防止自动stash未暂存更改（避免意外丢失工作区修改）。来源：https://www.npmjs.com/package/lint-staged

知识点6：Next.js中lint-staged特殊配置——Next.js的next lint命令需要--file参数指定文件，不能直接用eslint检查单文件。.lintstagedrc.js中配置：module.exports = { '*.{js,jsx,ts,tsx}': (filenames) => filenames.map((f) => `next lint --fix --file ${f}`) }。或者直接用独立eslint（需配置eslint.config.mjs），这样更快更灵活。我们项目当前用next lint（Next.js内置），迁移到独立ESLint flat config可获得更多规则控制。来源：https://nextjs.org/docs/13/app/building-your-application/configuring/eslint

知识点7：commitlint + Conventional Commits——commitlint检查提交信息是否符合Conventional Commits格式（type(scope): description）。@commitlint/config-conventional是标准配置。type包括：feat（新功能→minor版本）、fix（修复→patch版本）、docs（文档）、style（格式）、refactor（重构）、perf（性能）、test（测试）、chore（构建/工具）、ci（CI配置）、revert（回滚）。BREAKING CHANGE在footer或type!后（如feat!）触发major版本。Husky的commit-msg钩子运行npx commitlint --edit $1。来源：https://commitlint.js.org/guides/ci-setup

知识点8：commitlint CI集成——GitHub Actions中验证PR的所有commit：push事件用npx commitlint --last --verbose（验证最后一个commit）；pull_request事件用npx commitlint --from ${{ github.event.pull_request.base.sha }} --to ${{ github.event.pull_request.head.sha }} --verbose（验证PR范围内所有commit）。也可以用--default-config在没有配置文件时使用内置默认配置（@commitlint/config-conventional）。CI中commitlint检查确保即使本地hooks被--no-verify跳过，不合规commit也无法合并。来源：https://commitlint.js.org/guides/ci-setup

知识点9：完整CI质量门禁流水线——GitHub Actions workflow按顺序运行：(1) actions/checkout@v4（锁定commit SHA）；(2) actions/setup-node@v5（cache: 'npm'自动缓存依赖）；(3) npm ci（严格按lockfile安装，比npm install快且可复现）；(4) npm run typecheck（tsc --noEmit，类型检查）；(5) npm run lint（eslint .，代码质量）；(6) npm run format:check（prettier --check .，格式检查）；(7) npm run test（vitest run，单元测试）；(8) npm run build（next build，构建验证）。任何一步失败则CI失败，阻止合并。来源：https://terrierscript.com/frameworks/83/

知识点10：pre-push钩子做最终健康检查——pre-commit只检查暂存文件（快但不全面，可能漏掉未暂存的文件间依赖问题），pre-push钩子运行完整检查（typecheck + lint + test）确保推送的代码是健康的。.husky/pre-push内容：npm run typecheck && npm run lint && npm run test。如果推送紧急可以用git push --no-verify跳过（但CI仍会拦住，所以跳过只是延迟失败）。我们项目通过GitHub API提交不走本地git push，所以pre-push不生效，但CI质量门禁仍然有效。来源：https://reintech.io/blog/husky-lint-staged-pre-commit-hooks-setup

知识点11：Secret扫描防止API Key硬编码——pre-commit中加secretlint（~2k★）扫描API Key/Token/密码/私钥等敏感信息，防止硬编码密钥提交到仓库。配置.secretlintrc.json，规则包括@secretlint/secretlint-rule-preset-recommend（AWS key、GitHub token、私钥、Slack token等）。也可以用gitleaks（~20k★）做更全面的secret扫描和历史扫描。我们项目有GitHub PAT硬编码在临时Python脚本中（虽然脚本在项目外目录），需要注意不要将含密钥的文件提交到仓库。CI中也可以加secret扫描步骤。来源：https://www.npmjs.com/package/lint-staged

知识点12：代码质量工具性能优化——ESLint加--cache缓存结果（.eslintcache），增量检查快3-5倍；Prettier 3.2+内置--cache只格式化变更文件；TypeScript用--incremental生成.tsbuildinfo增量编译（下次编译只检查变更文件）；lint-staged天然只检查暂存文件；CI中actions/cache缓存node_modules（key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}）和.next/cache。大项目（500+源文件）全量lint可能>1分钟，加缓存后<10秒。来源：https://terrierscript.com/frameworks/83/

知识点13：Biome作为ESLint+Prettier替代方案——Biome（~12k★）是Rust编写的一体化工具，集成linter+formatter，比ESLint+Prettier快10-100倍（Rust vs Node.js）。Next.js 15+官方文档同时列出ESLint和Biome作为linter选择。Biome配置biome.json，规则兼容ESLint大部分规则，内置格式化（无需单独Prettier）。适合追求极致速度的项目，但生态和规则覆盖不如ESLint成熟（2026年仍在快速发展，部分ESLint插件规则无对应）。我们项目可以评估迁移但不急于切换，先用ESLint+Prettier标准组合。来源：https://nextjs.org/docs/app/getting-started/installation

知识点14：AIToolCrux项目代码质量现状与落地建议——当前项目有tsconfig.json（strict模式）但无独立ESLint配置（只用Next.js内置next lint）、无Prettier配置、无Husky/lint-staged、无commitlint。我们通过GitHub API直接提交（不走git commit），所以本地hooks不生效，但CI质量门禁仍然有价值。落地优先级：(a) P2：加ESLint flat config + Prettier配置，统一代码风格（当前代码格式不统一，有的文件2空格有的4空格）；(b) P2：加commitlint + CI commit检查（规范commit message格式，当前是自由格式如"fix(seo): P0 batch"，实际已接近conventional但未强制）；(c) P3：加lint-staged + Husky（其他贡献者/本地修改时有用）；(d) P3：加secretlint防止API Key硬编码提交。来源：https://nextjs.org/docs/app/getting-started/installation

知识点15：完整配置文件清单与package.json scripts——需要创建：eslint.config.mjs（ESLint flat config，extends @eslint/js + typescript-eslint + next/core-web-vitals + prettier）、.prettierrc（JSON配置，如semi: true, singleQuote: true, trailingComma: 'es5'）、.prettierignore（忽略.next/、node_modules/、public/）、.husky/pre-commit（npx lint-staged）、.husky/commit-msg（npx commitlint --edit $1）、.lintstagedrc（按文件类型配置命令）、commitlint.config.mjs（export default { extends: ['@commitlint/config-conventional'] }）。package.json scripts："lint": "eslint . --cache"、"lint:fix": "eslint . --cache --fix"、"format": "prettier --write ."、"format:check": "prettier --check ."、"typecheck": "tsc --noEmit"、"check": "npm run format:check && npm run lint && npm run typecheck"、"prepare": "husky"。来源：https://terrierscript.com/frameworks/83/ + https://www.dimitri-dumont.fr/blog/eslint-prettier-automatiser-qualite-code-2026

落地计划：
- P2-CODE-ESLINT-PRETTIER-001：加ESLint 9 flat config + Prettier 3配置，统一代码风格，加npm run lint/format/format:check脚本
- P2-CODE-COMMITLINT-001：加commitlint + Conventional Commits配置，加GitHub Actions CI commit检查，规范commit message格式
- P3-CODE-HUSKY-LINTSTAGED-001：加Husky 9 + lint-staged pre-commit钩子，提交时自动lint+format暂存文件



[2026-09-22] 高星GitHub开源工具——自动化测试工具完整体系（Vitest + Playwright + React Testing Library + MSW + 视觉回归）

知识点1：2026前端测试工具格局已定型——Vitest赢了单元测试（~8M周下载，快速增长），Playwright赢了E2E（~5M），Testing Library仍是React组件测试标准（~10M）。Jest/Cypress仍是legacy选择但新项目默认Vitest+Playwright。三者组合是2026 Next.js项目的事实标准。来源：https://www.pkgpulse.com/guides/state-of-javascript-testing-2026/raw.md

知识点2：Playwright核心优势——多浏览器（Chromium/Firefox/WebKit）单一API，一套测试跑三个浏览器捕获Safari-only bug；真正的并行执行（--shard免费，Cypress需Cloud plan $67+/月）；auto-waiting消除固定sleep（元素可操作才执行）；隔离browser context（每个测试独立session无状态污染）；内置trace调试（失败时录屏+DOM快照+网络请求）；CI dashboard免费（HTML report）。来源：https://nextjs.org/docs/app/guides/testing/playwright

知识点3：Playwright vs Cypress关键差异——Playwright测试在Node进程运行（可访问文件系统/数据库），Cypress在浏览器内运行（限制多）；Playwright支持多tab/多origin/iframe，Cypress历史上限制单origin；Playwright免费并行+免费报告，Cypress Cloud收费；Playwright由Microsoft维护，Cypress由Cypress.io公司维护；2026新项目默认Playwright，已有Cypress项目可渐进迁移。来源：https://gocodelab.com/en/blog/en-playwright-vs-cypress-e2e-guide-ci-parallel-2026

知识点4：Vitest核心优势——基于Vite构建，ESM原生支持，比Jest快5-10倍（无需编译整个bundle）；配置简单（复用vite.config.ts/next.config.mjs的alias和plugin）；内置TypeScript/JSX支持无需babel；watch模式极快（HMR级别的增量测试）；API兼容Jest（describe/it/expect/beforeEach几乎1:1），迁移成本低；Vitest 5.0已于2026-09-15发布。来源：https://vitest.dev/blog/vitest-5.html

知识点5：React Testing Library哲学与查询优先级——测试用户可见行为而非实现细节（不测试state/props/内部函数）；查询优先级：getByRole（首选，可访问性+最稳定）> getByLabelText（表单字段）> getByPlaceholderText > getByText > getByDisplayValue > getByAltText（图片）> getByTitle > querySelector（避免，脆弱）；getBy*在元素不存在时抛错，queryBy*返回null（用于断言不存在），findBy*异步等待元素出现。来源：https://nextjs.org/docs/app/guides/testing/vitest

知识点6：user-event库是Testing Library标准配套——模拟真实用户交互（点击/输入/键盘/表单/hover/drag）；比fireEvent更真实（触发完整事件序列如focus→keydown→keypress→input→keyup→change）；所有交互必须await（异步）；userEvent.setup()配置延迟（delay选项模拟真实输入速度）和指针事件；clear()/type()/selectOptions()/upload()等高级API。来源：https://scrimba.com/articles/how-to-test-react-apps-2026/

知识点7：Next.js App Router测试关键限制——async Server Components不被Vitest支持（Vitest只能测同步Server/Client Components）；async组件（如app/tools/[slug]/page.tsx中的async函数）必须用E2E测试（Playwright）；Client Components可用Vitest+RTL完整测试；工具函数/hooks/纯逻辑可用Vitest纯单元测试；这意味着我们项目大部分页面是async Server Component，E2E测试比单元测试更有价值。来源：https://nextjs.org/docs/app/guides/testing/vitest

知识点8：Playwright Next.js集成配置——create-next-app --example with-playwright快速开始；playwright.config.ts中webServer配置自动启动dev/prod服务器（command: 'npm run start', port: 3000, reuseExistingServer: !process.env.CI）；baseURL: 'http://localhost:3000'；test('...', async ({ page }) => { await page.goto('/'); })；expect(page).toHaveURL('/tools/chatgpt')；expect(page.getByRole('heading', { level: 1 })).toBeVisible()。来源：https://nextjs.org/docs/app/guides/testing/playwright

知识点9：Playwright选择器最佳实践——用语义选择器（getByRole/getByLabelText/getByText）而非CSS class（.btn-primary.large）或nth-child（div > div > button:nth-child(2)），后者在样式/结构变化时易碎；getByRole是首选（同时验证可访问性）；data-testid作为最后手段（无法用语义选择器时，如动态生成的列表项）；避免XPath和模糊文本匹配；locator链式调用（page.getByRole('navigation').getByRole('link', { name: 'Tools' })）提高精度。来源：https://nextjs.org/docs/app/guides/testing/playwright

知识点10：MSW（Mock Service Worker）是网络请求mock标准工具——拦截浏览器和Node中的网络请求，返回预设响应；支持REST和GraphQL；同一套handlers在浏览器端（Service Worker）和Node端（@mswjs/node）通用；Next.js中配合Vitest使用，mock外部API调用避免测试依赖网络；setupServer()在测试文件中启动，beforeAll(() => server.listen())/afterEach(() => server.resetHandlers())/afterAll(() => server.close())；避免在测试中真实调用外部API（慢/不稳定/有副作用）。来源：https://scrimba.com/articles/how-to-test-react-apps-2026/

知识点11：视觉回归测试工具——Playwright内置toHaveScreenshot()做像素级视觉对比（自动生成baseline，CI中对比差异）；Chromatic（Storybook生态，~10k★）做组件级视觉回归+UI审查；BackstopJS（开源，~6.5k★）做全站页面级视觉回归；视觉测试需在固定viewport（如1280x720）和稳定数据下运行；CI中需有baseline更新策略（人工审核或自动更新）；我们项目SSG站点可用Playwright toHaveScreenshot做关键页面视觉回归。来源：https://nextjs.org/docs/app/guides/testing/playwright

知识点12：测试金字塔在Next.js项目中的应用——单元测试（Vitest，~70%，工具函数/纯逻辑/hooks/数据处理）→ 组件测试（Vitest+RTL，~20%，交互组件如CTA按钮/搜索框/筛选器）→ 集成测试（Vitest+RTL+MSW，~5%，多组件协作如工具卡片列表+筛选）→ E2E测试（Playwright，~5%，关键用户旅程如首页→工具列表→工具详情→点击CTA）。我们项目SSG+async Server Component多，E2E测试价值高于单元测试，建议E2E:单元=6:4。来源：https://www.pkgpulse.com/guides/state-of-javascript-testing-2026/raw.md

知识点13：CI中的测试策略——Vitest在CI中用vitest run（非watch模式，跑完退出）；Playwright用--shard=1/4 --shard=2/4等并行分片（GitHub Actions matrix strategy）；actions/upload-artifact保存Playwright trace（playwright-report/和test-results/）供失败调试；测试失败时自动重试（playwright.config.ts中retries: process.env.CI ? 2 : 0）；测试超时配置（timeout: 30000, expect: { timeout: 5000 }）；npm run test:ci = vitest run && playwright test。来源：https://nextjs.org/docs/app/guides/testing/playwright

知识点14：AIToolCrux项目测试落地优先级（当前0测试）——(a) P1：Playwright smoke测试——关键页面返回200（首页/工具列表/工具详情/文章/分类/对比页），防止部署后404；(b) P1：Playwright CTA链接测试——抽样工具页CTA按钮href指向正确官网域名（非搜索页），防止回归；(c) P2：Playwright SEO验证——/blog/tag/*页面有noindex meta，canonical标签正确，title长度≤60；(d) P2：Vitest单元测试——工具数据处理函数（slug生成/分类映射/评分计算/排序逻辑）；(e) P2：GitHub Actions test workflow——PR时自动运行smoke+CTA测试。来源：https://nextjs.org/docs/app/guides/testing

知识点15：测试代码组织与配置——Playwright测试放tests/e2e/目录（*.spec.ts）；Vitest测试放与源文件同目录（utils.test.ts）或__tests__/目录；playwright.config.ts配置webServer/baseURL/reporter: 'html'/projects（多浏览器）；vitest.config.ts配置environment: 'jsdom'/globals: true/setupFiles: './vitest.setup.ts'；package.json scripts: "test": "vitest", "test:e2e": "playwright test", "test:ci": "vitest run && playwright test", "test:ui": "vitest --ui"；.gitignore忽略playwright-report/、test-results/、coverage/。来源：https://nextjs.org/docs/app/guides/testing/vitest + https://nextjs.org/docs/app/guides/testing/playwright

落地计划：
- P1-TEST-SMOKE-001：Playwright smoke测试——关键页面（首页/工具列表/工具详情/文章/分类）返回200，防止部署后404回归
- P1-TEST-CTA-LINKS-001：Playwright CTA链接测试——抽样20个工具页CTA按钮href指向正确官网域名（非Google搜索页），防止CTA回归
- P2-TEST-SEO-VERIFY-001：Playwright SEO验证——/blog/tag/*页面noindex meta、canonical正确、title≤60字符；加GitHub Actions test workflow



[2026-09-22] Next.js App Router 缓存策略深度优化（Data Cache / Full Route Cache / Router Cache / ISR / revalidate / unstable_cache / cache tags）

知识点1：Next.js 四层缓存架构——Request Memoization（单次请求内React内置去重，请求结束即清除）→ Data Cache（持久化，跨请求/跨部署保留，存在服务器或边缘网络）→ Full Route Cache（渲染后的HTML+RSC payload，静态路由构建时缓存）→ Router Cache（客户端内存缓存，页面刷新清除，back/forward导航重用）。来源：https://nextjs.org/docs/app/guides/caching

知识点2：Data Cache 是 fetch() 的默认行为——App Router 中 fetch() 默认 cache: 'force-cache'，响应被持久化到 Data Cache。用 cache: 'no-store' 或 next: { revalidate: 0 } 跳过缓存。非 fetch 的数据（数据库查询）需用 unstable_cache 或 'use cache' 才能进入 Data Cache。来源：https://nextjs.org/docs/app/api-reference/functions/fetch

知识点3：fetch 缓存选项详解——next: { revalidate: 3600 } 设置TTL（秒），过期后首个请求触发后台重新渲染同时返回旧内容（stale-while-revalidate）；next: { tags: ['blog', 'author-123'] } 打标签用于按需失效；cache: 'no-store' 完全跳过缓存（动态渲染）。来源：https://nextjs.org/docs/app/api-reference/functions/fetch

知识点4：Full Route Cache 存储静态渲染路由的渲染结果（HTML + RSC payload + Client Component JS引用 + props）。静态路由在构建时生成并缓存；ISR路由在首次访问后缓存；动态渲染路由（含no-store fetch或dynamic()）完全不缓存。revalidate后Full Route Cache条目失效，下次请求重新渲染。来源：https://nextjs.org/docs/app/guides/caching

知识点5：Router Cache 是客户端内存缓存，存储React Server Component Payload。预取的链接（<Link prefetch>或router.prefetch）自动缓存5分钟（可通过experimental.staleTimes配置）。页面刷新时Router Cache完全清除。back/forward导航时重用缓存（不发请求）。这是唯一完全在客户端的缓存层。来源：https://nextjs.org/docs/app/guides/caching

知识点6：时间驱动 revalidation 两种粒度——页面级 export const revalidate = 3600（该页面所有fetch默认1小时revalidate）；请求级 fetch(url, { next: { revalidate: 3600 } })（单个fetch的TTL）。页面级revalidate是该页面最短的fetch revalidate——如果页面有一个fetch revalidate=60，页面revalidate=3600，则实际60秒就会revalidate。来源：https://nextjs.org/docs/app/getting-started/revalidating

知识点7：按需 revalidation - revalidatePath——在Server Action或Route Handler中调用 revalidatePath('/blog/post-1') 失效特定路径的Data Cache和Full Route Cache。支持 revalidatePath('/blog/[slug]', 'layout') 失效整个layout下所有页面。revalidatePath是粗粒度的，适合整页更新场景。来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration

知识点8：按需 revalidation - revalidateTag——revalidateTag('blog') 失效所有打了 next: { tags: ['blog'] } 的fetch缓存，比revalidatePath更细粒度。stale-while-revalidate语义：失效后首个请求立即返回旧内容，后台刷新。Vercel上tag revalidation传播到所有边缘区域<300ms。推荐用于CMS内容更新（webhook触发）。来源：https://vercel.com/docs/data-cache

知识点9：unstable_cache 用于缓存非fetch数据——数据库查询、复杂计算、第三方SDK调用等。用法：const getCachedUser = unstable_cache(async (id) => db.user.findUnique({where:{id}}), ['user-cache-key'], { revalidate: 3600, tags: ['user'] })。返回Promise，需在Server Component中await。Next.js 15+已被 'use cache' 指令替代但仍兼容。来源：https://nextjs.org/docs/app/getting-started/caching-and-revalidating

知识点10：ISR（Incremental Static Regeneration）结合SSG和SSR优势——构建时静态生成（快、可CDN缓存），运行时按需重新验证（内容可更新无需重新部署）。只需 export const revalidate = 86400 即可启用。Vercel上ISR页面在边缘网络缓存，首次访问miss后回源渲染并缓存，后续访问直接命中边缘缓存。来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration

知识点11：SSG vs ISR vs SSR 决策树——SSG（纯静态 export const dynamic = 'force-static'，永不更新）→ 内容完全不变的页面（关于页、方法论页）；ISR（export const revalidate = N）→ 内容偶尔更新、可接受几分钟到几小时延迟的页面（博客文章、工具详情页、工具列表）；SSR（fetch cache: 'no-store' 或 export const dynamic = 'force-dynamic'）→ 每次请求都需最新数据的页面（用户dashboard、实时价格、搜索结果）。来源：https://nextjs.org/docs/app/guides/caching

知识点12：CDN/边缘缓存响应头——静态页面（无revalidation）：s-maxage=31536000（1年，CDN永久缓存）；ISR页面（时间驱动revalidate）：s-maxage={revalidate}, stale-while-revalidate={expire-revalidate}（默认expire=1年）；动态页面：private, no-store, no-cache, must-revalidate。Vercel自动设置这些头，自托管需在next.config.mjs的headers中配置。来源：https://nextjs.org/docs/app/guides/cdn-caching

知识点13：Next.js 15+ Cache Components 新缓存模型——'use cache' 指令替代 unstable_cache（函数级缓存，自动序列化key）；cacheTag('posts') 替代 next.tags（在'use cache'函数内调用）；revalidateTag(tag, 'max') 支持stale-while-revalidate profile（'max'=立即返回旧内容后台刷新，默认=等待新内容）；'use cache: remote' 用于远程缓存（Redis/Upstash），只缓存指定参数作为cache key提升命中率。来源：https://nextjs.org/docs/app/getting-started/cache-components

知识点14：缓存失效注意事项——revalidateTag/revalidatePath 只失效 Data Cache，不直接失效 Full Route Cache；Full Route Cache 在下次请求时因 Data Cache 失效而自动重新渲染。Router Cache 是客户端缓存，服务端 revalidate 后用户需刷新页面或重新导航才能看到新内容（除非在Client Component中调用 router.refresh()）。部署新版本会自动清除 Data Cache 和 Full Route Cache（除非用了持久化外部缓存）。来源：https://nextjs.org/docs/app/guides/how-revalidation-works

知识点15：AIToolCrux 项目缓存现状与优化方向——当前纯SSG（Vercel部署时533工具页+105文章全量静态生成），内容更新需重新部署。优化方向：(a) 工具详情页加 export const revalidate = 86400（ISR 24小时），允许tools.json更新后自动刷新而无需重新部署；(b) 文章页同样加revalidate；(c) 当前tools.json 7.86MB全量导入导致每个页面bundle大，可用unstable_cache缓存解析结果或按需加载；(d) 如未来接入CMS/webhook，用revalidateTag实现按需更新；(e) 首页工具列表可考虑ISR+stale-while-revalidate平衡新鲜度和性能。来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration + https://vercel.com/docs/data-cache

落地计划：
- P2-PERF-ISR-TOOLS-001：工具详情页加 export const revalidate = 86400（ISR 24小时），允许内容更新自动刷新
- P2-PERF-ISR-POSTS-001：文章页加 export const revalidate = 86400，文章更新后自动revalidate
- P2-PERF-TOOLSJSON-OPTIMIZE-001：优化 tools.json 7.86MB 全量导入——用 unstable_cache 缓存解析或按需分页加载，减小页面bundle



- [2026-09-22] **GSC API 自动化 + 索引优化 2026 完整指南（15 个权威知识点，Google Search Console API 官方 + IndexNow 官方 + Bing Webmaster + Google Search Central）**
  1. **GSC API v1 四大服务**——Search Analytics（查询流量数据：曝光/点击/CTR/平均排名，按 query/page/country/device/searchAppearance/date 维度）、Sitemaps（列出/提交/获取 sitemap 信息/删除 sitemap）、Sites（列出/添加/删除 Search Console 属性）、URL Inspection（检查单个 URL 的索引状态，等价于 GSC 后台的 URL 检查工具，返回索引状态/抓取详情/移动可用性/富摘要资格）。来源：https://developers.google.com/webmaster-tools/v1/api_reference_index
  2. **Search Analytics API 请求格式**——POST `https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query`，body 含 startDate/endDate（YYYY-MM-DD，最多 16 个月范围）、dimensions（可选：query/page/country/device/searchAppearance）、startRow/rowLimit（默认 1000，最大 25000，需分页）、dimensionFilterGroups（过滤条件）、aggregationType（byPage 按页面聚合/byProperty 按属性聚合）、dataState（FINAL 最终数据/PRELIMINARY 初步数据）。siteUrl 格式：URL 前缀属性用 `http://www.example.com/`，域属性用 `sc-domain:example.com`。来源：https://developers.google.com/webmaster-tools/v1/searchanalytics/query
  3. **URL Inspection API 是自动化索引检查的核心**——POST `https://searchconsole.googleapis.com/v1/urlInspection/index:inspect`，body 含 inspectionUrl（要检查的页面 URL）和 siteUrl。返回 UrlInspectionResult 对象，包含：inspectionResultLink（GSC 后台对应链接）、indexStatus（verdict: PASS/PARTIAL/FAIL/FULLY_ON_INDEX、fullyIndexed、indexedState、lastCrawlTime、pageFetchState、robotsTxtState、indexingState、sitemap 列表、referringUrls 外链）、mobileUsability（移动可用性问题 verdict + 具体 issue）、richResultsResult（富摘要资格 verdict + 具体 item）。来源：https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect
  4. **GSC API 认证：OAuth 2.0 不支持 API Key**——需要 OAuth 2.0 认证，scope 为 `https://www.googleapis.com/auth/webmasters.readonly`（只读，查数据）或 `https://www.googleapis.com/auth/webmasters`（读写，提交 sitemap）。API Key 只能访问公开数据，Search Console 数据需要用户授权。服务账号（Service Account）也可使用，但需在 GSC 属性设置中添加服务账号邮箱为"完整权限"用户（不是仅查看）。Python 用 google-api-python-client + google-auth 库。来源：Google Search Console API 官方认证文档
  5. **IndexNow 是什么：Bing 发起的即时索引协议**——由 Microsoft Bing 发起、Yandex 等参与的开放协议，允许网站即时通知搜索引擎 URL 的新增/更新/删除。提交到任意一个参与端点（api.indexnow.org 全局端点、bing.com、yandex.com、amazonbot.amazon、searchadvisor.naver.com、search.seznam.cz、indexnow.yep.com）后，会自动共享给所有 IndexNow 搜索引擎。**Google 不参与 IndexNow**（Google 有自己的 Indexing API，但仅限 JobPosting/BroadcastEvent 两类页面）。来源：https://www.indexnow.org/documentation + https://www.bing.com/indexnow/getstarted
  6. **IndexNow 提交方式：单 URL GET + 批量 POST**——单 URL 提交：GET `https://api.indexnow.org/indexnow?url={url}&key={key}`。批量提交（最多 10000 条/请求，每日无明确上限但不要滥用）：POST `https://api.indexnow.org/indexnow`，Content-Type: application/json; charset=utf-8，body: `{ "host": "www.aitoolcrux.com", "key": "your-key", "keyLocation": "https://www.aitoolcrux.com/key.txt", "urlList": ["url1","url2"] }`。返回 200 = 成功，202 = 已接收待验证，400 = 格式错误，403 = key 验证失败，422 = key 格式无效。来源：https://www.indexnow.org/documentation + https://www.bing.com/indexnow/getstarted
  7. **Google Indexing API 仅限 JobPosting/BroadcastEvent，普通页面不能用**——Google 的 Indexing API（`https://indexing.googleapis.com/v3/urlNotifications:publish`）仅支持 JobPosting（招聘信息）和 BroadcastEvent（直播活动）两类结构化数据页面的即时索引通知。普通页面（如我们的工具评测页、博客文章、分类页）**不能**用 Indexing API 提交，Google 官方明确建议用 sitemap + 自然抓取。这是用户常问"为什么不能直接提交 URL 给 Google"的标准答案。来源：Google Indexing API 官方文档 + Google Search Central 帮助论坛
  8. **sitemap 优化最佳实践**——单个 sitemap 最多 50000 URL 或 50MB（未压缩），超出需用 sitemap index（sitemap of sitemaps，最多 50000 个子 sitemap）。我们项目 533 工具页 + 105 文章 + 分类页 + 对比页 ≈ 700 URL，单 sitemap 足够。sitemap 应只包含可索引（indexable）的 200 页面，**不包含 noindex/301/404 页面**（浪费抓取配额，Google 会降低对 sitemap 的信任度）。`<lastmod>` 应准确反映页面最后修改时间（帮助 Google 决定抓取优先级，不要全部设为构建时间）。Next.js 13+ 用 `app/sitemap.ts` 约定自动生成。来源：Google Search Central sitemap 官方文档 + Next.js sitemap docs
  9. **robots.txt 与抓取预算**——robots.txt 的 `Sitemap:` 指令告诉搜索引擎 sitemap 位置（可放多个，每行一个）。`Crawl-delay` 指令 Google 不支持（用 GSC 后台设置 > 抓取速率替代）。对新站/小站（<1000 页），抓取预算通常不是问题；对大站，应确保：(a) 内部链接结构合理（重要页面点击深度 <3）；(b) 避免重复内容（canonical 指向首选版）；(c) 减少低质量/薄内容页面消耗抓取预算（noindex 或合并）；(d) 服务器响应速度快（Google 给慢站分配更少抓取预算）。来源：Google Search Central robots.txt 官方文档 + 抓取预算指南
  10. **索引覆盖率监控自动化方案**——用 GSC Search Analytics API 按 page 维度查询（dimensions: ["page"]），获取有曝光的页面列表，对比已发布页面总数（533+105+分类+对比 ≈ 700），计算索引覆盖率 = 有曝光页面数 / 总页面数。用 URL Inspection API 批量抽查未被索引的页面，诊断原因（verdict: FAIL → 看 pageFetchState/robotsTxtState/indexingState/referringUrls）。写 GitHub Actions 定时任务每周运行，输出索引覆盖率报告到 iteration_center/gsc-reports/。来源：GSC API 官方文档 + 索引覆盖率最佳实践
  11. **noindex 与 canonical 的正确使用和 sitemap 联动**——noindex（`<meta name="robots" content="noindex,follow">` 或 X-Robots-Tag HTTP 头）阻止页面被索引，但仍可被抓取和传递权重（follow）。canonical（`<link rel="canonical" href="...">`）告诉 Google 哪个是首选版本，用于重复内容（分页、筛选参数页、打印版）。关键联动规则：**被 noindex 的页面不应出现在 sitemap 中**（Google 官方明确说 noindex 页面在 sitemap 中会混淆信号，浪费抓取配额）。我们项目的 /blog/tag/* 薄内容页已加 noindex,follow（OpenSEO 审计修复任务），**必须从 sitemap 中移除这些 156 个 tag 页面**。来源：Google Search Central noindex/canonical 官方文档
  12. **GSC API 限流和配额**——Search Analytics API：每个项目每秒 5 次查询（QPS），每天 2000 次查询。URL Inspection API：每个属性每天 2000 次查询，每分钟 60 次。Sitemaps API：每个属性每天 50 次提交。Sites API：每个项目每天 300 次查询。超出配额返回 429 Too Many Requests，需指数退避重试（exponential backoff：1s→2s→4s→8s，最多 5 次）。对我们项目 ~700 页面，URL Inspection API 每天 2000 次足够全量检查一次（700 次/天）。来源：Google Search Console API 配额文档
  13. **我们项目的 GSC 自动化落地架构**——(a) Python + google-api-python-client 库，OAuth 服务账号认证（在 GSC 属性设置中添加服务账号邮箱为完整权限用户，JSON key 存 GitHub Secrets）；(b) 每周 GitHub Actions 定时任务：Search Analytics API 拉取上周数据（曝光/点击/CTR/排名 by page + by query），与上周对比生成异动报告（曝光下降 >30% 的页面预警）；(c) 每月全量 URL Inspection：检查所有 ~700 页面索引状态，输出未索引页面清单和原因（verdict + pageFetchState + robotsTxtState）；(d) 新文章发布后自动 IndexNow 提交（Bing/Yandex 即时索引）+ Google 靠 sitemap 自然抓取；(e) 所有报告写入 iteration_center/gsc-reports/ 目录，关键指标更新到 state.json。来源：项目架构分析 + GSC API 官方文档
  14. **IndexNow key 验证机制和我们项目的配置检查**——key 是 8-128 字符的十六进制字符串（如 `e1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6`），需在网站根目录放置 `{key}.txt` 文件（如 `https://www.aitoolcrux.com/e1a2b3c4...txt`），文件内容就是 key 本身（纯文本，无 HTML）。搜索引擎收到 IndexNow 提交后，会 HTTP GET 访问这个 key 文件验证提交者拥有该网站。也可以用 `keyLocation` 参数指定 key 文件的非标准位置。我们项目已配置 IndexNow key（在 state.json 中），**需确认 public/{key}.txt 文件存在且内容正确**，否则 IndexNow 提交会返回 403。来源：https://www.indexnow.org/documentation + https://www.bing.com/indexnow/getstarted
  15. **Google 不参与 IndexNow 的替代方案：加速 Google 索引的 5 个方法**——(a) 确保 sitemap 在 robots.txt 中声明（`Sitemap: https://www.aitoolcrux.com/sitemap.xml`）且在 GSC 后台提交（GSC > 站点地图 > 添加新站点地图）；(b) 高权重网站的外链（Google 从外链发现新页面更快，外链也是排名因素）；(c) 内部链接结构合理（新页面从首页/分类页/相关文章可点击到达，点击深度 <3，不要让新页面成为孤立页 orphan page）；(d) 页面质量高（Google 对薄内容/低质量页面抓取/索引优先级低，我们的列表型文章 best-ai-*-tools 无图无结论是薄内容，需改进）；(e) 耐心等待——新站通常需要 2-4 周才能被充分索引，没有"一键提交"捷径，不要相信第三方"快速收录"服务。来源：Google Search Central 索引指南 + Google 官方论坛声明

  **落地计划**：
  - 下次迭代做 **P2-SEO-INDEX-COVERAGE-001**：用 GSC URL Inspection API 全量检查 ~700 页面索引状态，输出未索引页面清单和原因（verdict/pageFetchState/robotsTxtState），这是解决用户"Google 收录"问题的最直接手段
  - 同步做 **P2-SEO-SITEMAP-CLEANUP-001**：清理 sitemap 中的 noindex 页面（156 个 /blog/tag/* 薄内容页），只包含可索引 200 页面，避免 Google 降低对 sitemap 的信任度
  - **P2-SEO-INDEXNOW-VERIFY-001**：确认 IndexNow key 文件存在于 public/ 且内容正确，新文章发布后自动 IndexNow 批量提交（Bing/Yandex 即时索引）


- [2026-09-22] **Next.js Image Optimization + Font Optimization 2026 完整指南（15 个权威知识点，Next.js 官方 docs + Vercel 官方 + web.dev）**
  1. **next/image 四大核心优化**——尺寸优化（自动 WebP/AVIF + srcset，按设备选择最合适尺寸）、视觉稳定（自动防 CLS，需 width/height 或 fill + 容器 aspect-ratio）、更快加载（视口懒加载 + blur-up 占位）、资产灵活（远程图片按需调整大小，即使存储在远程服务器）。来源：https://nextjs.org/docs/app/getting-started/images
  2. **priority 属性对 LCP 图片至关重要**——`priority={true}` 的图片会被预加载（`<link rel="preload">`），自动禁用懒加载。Google 和 Next.js 官方明确要求：任何被检测为 Largest Contentful Paint (LCP) 元素的图片都应该加 priority。可以有多个 priority 图片（不同视口的 LCP 元素不同）。不加 priority 的 LCP 图片会等浏览器发现后才加载，延迟 200-500ms。来源：https://nextjs.org/docs/app/api-reference/components/image + https://nextjs.org/docs/14/app/api-reference/components/image
  3. **sizes 属性是 next/image 最常被忽略的关键配置**——`sizes` 定义图片在不同断点的渲染尺寸，浏览器据此从生成的 srcset 中选择最合适的尺寸。不写 sizes 时，next/image 默认假设图片占满视口宽度（100vw），会加载过大的图片（浪费带宽，LCP 变慢）。正确写法：`sizes="(max-width: 768px) 100vw, 50vw"`。对网格布局中的缩略图尤其重要。来源：https://nextjs.org/docs/app/api-reference/components/image#sizes
  4. **width/height 或 fill 必须二选一，防止 CLS**——next/image 要求提供 width 和 height（渲染尺寸，宽高比需与源图一致），或使用 fill（图片填充父容器，父容器需有 position: relative + aspect-ratio）。不提供尺寸会导致图片加载时布局偏移（CLS）。ESLint 规则 `@next/next/no-img-element` 强制用 next/image 替代原始 `<img>`。来源：https://nextjs.org/docs/app/api-reference/components/image + https://nextjs.org/docs/messages/no-img-element
  5. **remotePatterns 配置远程图片白名单**——next.config 中 `images.remotePatterns` 定义允许的远程图片源（protocol/hostname/port/pathname/search），阻止所有其他远程图片。这是安全措施，防止恶意图片消耗优化资源。我们项目的工具截图如果存在远程 CDN（如 images.unsplash.com、工具官网截图），需要配置对应的 remotePatterns。支持通配符 `**` 匹配子路径。来源：https://nextjs.org/docs/app/getting-started/images + https://preview.nextjs.org/docs/app/getting-started/images
  6. **next/font 自动自托管字体，零外部请求**——`next/font` 模块在构建时下载字体文件（Google Fonts 或本地字体），与其他静态资产一起自托管。用户访问时不发送请求到 Google（隐私 + 性能，减少一个 DNS 解析 + TCP 连接）。CSS `size-adjust` 属性实现零布局偏移（自动计算 fallback 字体 metrics 与自定义字体匹配）。来源：https://nextjs.org/docs/app/getting-started/fonts + https://vercel.com/docs/frameworks/nextjs
  7. **next/font 的 display 策略：swap vs optional**——默认 `display: 'swap'`（先显示 fallback 字体，自定义字体加载后替换，可能有轻微 CLS）。`display: 'optional'` 最小化不可见文本和布局偏移风险（如果字体在极短时间内（~100ms）未加载就一直用 fallback，不交换）。对 LCP 文本元素，用 `optional` 可避免字体交换导致的 LCP 波动；对品牌字体必须显示的用 `swap`。来源：https://nextjs.org/docs/messages/google-font-display + Next.js font API docs
  8. **next/font 的 CSS 变量用法（Tailwind 集成标准方式）**——`next/font/google` 或 `next/font/local` 返回的对象有 `variable` 属性（如 `inter.variable`，值为 `--font-inter`），在 layout.tsx 中加到 `<html>` 或 `<body>` 的 className，然后在 tailwind.config 中 `fontFamily: { sans: ['var(--font-inter)', 'sans-serif'] }`。这是 Next.js + Tailwind 项目的标准字体集成方式，比全局 CSS class 更灵活。来源：https://nextjs.org/docs/app/getting-started/fonts + Next.js Learn Dashboard App
  9. **字体导致 CLS 的三大常见原因（即使使用了 next/font）**——(a) fallback metrics 不匹配：next/font 自动计算但如果自定义字体与 fallback 差异过大仍有偏移，可用 `adjustFontFallback` 微调；(b) 从 CSS `@import` 或 `<link>` 加载 Google Fonts 而不是 next/font loader（绕过了自托管和 metrics 调整）；(c) 客户端 useEffect 在 hydration 后动态切换 font class（导致 hydration 后布局变化）。解决方案：确保所有字体通过 next/font 加载，不要在 useEffect 中切换字体。来源：https://nextjslaunchpad.com/article/nextjs-next-font-google-local-fonts-guide
  10. **AVIF 格式比 WebP 更小但需注意兼容性和编码速度**——Next.js 默认输出 WebP，可在 next.config 中 `images: { formats: ['image/avif', 'image/webp'] }` 启用 AVIF（AVIF 比 WebP 小 20-50%，对照片类截图效果更明显）。AVIF 在 Chrome 85+/Firefox 93+/Safari 16+ 支持，2026 年全球覆盖率 >95%。但 AVIF 编码更慢（优化 API 首次响应时间增加 2-3 倍），Vercel 上有 Edge 缓存所以首次后影响不大。来源：Next.js Image docs + web.dev AVIF 指南
  11. **blur-up 占位：静态图自动，远程图需 blurDataURL**——静态导入的图片（`import logo from './logo.png'`）next/image 自动生成 blur 占位（Plaiceholder 算法，base64 20px 模糊图）。远程图片需要手动提供 `blurDataURL`（base64 编码的极小图，建议用 Plaiceholder/sharp 预生成）或 `placeholder="empty"`（无 blur，加载前空白）。不提供 blurDataURL 的远程图片没有 blur-up 效果，图片加载前会空白闪烁。对我们的工具截图（远程），应该预生成 blurDataURL 或用背景色占位。来源：https://nextjs.org/docs/app/api-reference/components/image
  12. **Vercel Image Optimization 限制和缓存策略**——Vercel 上 next/image 优化自动进行，优化后的图片缓存在 Vercel Edge Network（Cache-Control: public, max-age=31536000, immutable）。Hobby 免费版 1000 次优化/月，Pro 版 5000 次/月，超出后图片仍显示但不优化（回退原图，仍可访问）。我们项目 533 工具页 × 多尺寸截图，需注意优化次数。对已在外部优化过的截图（如工具官网已压缩的图），可用 `unoptimized` 属性跳过 Vercel 优化节省配额。来源：Vercel docs + Next.js Image docs
  13. **我们项目的图片+字体现状审计清单**——(a) 工具详情页主截图是否用 next/image + priority（LCP 元素，不加 priority LCP 延迟 200-500ms）；(b) 文章中的截图是否用 next/image（而不是原始 `<img>` 或 markdown `![]()`）；(c) 远程图片是否配置了 remotePatterns（否则 next/image 会报错拒绝加载）；(d) 是否有图片缺少 width/height 导致 CLS；(e) 字体是否通过 next/font 加载（检查 layout.tsx，是否有 CSS @import url('fonts.googleapis.com')）；(f) LCP 图片是否加了 sizes 属性。来源：项目架构分析 + Next.js 官方 docs
  14. **priority 与 fetchpriority 的区别和配合**——`priority={true}` 在 Next.js 14 中等价于 `<link rel="preload" as="image">` + `fetchpriority="high"`，会在 HTML head 中插入 preload 链接。对非 LCP 但重要的图片（如首屏第二张图、hero 背景图），可以用 `fetchPriority="high"`（Next.js 14.1+ 支持）而不加 priority，避免过多 preload 链接竞争带宽。preload 太多会适得其反（带宽竞争，反而延迟 LCP）。来源：Next.js Image docs + web.dev fetchpriority 指南
  15. **字体子集化（subsetting）大幅减少字体体积**——next/font 对 Google Fonts 自动做 unicode-range 子集化（CSS @font-face 按 unicode-range 分割，浏览器只加载页面用到的字符范围），拉丁字符子集通常只有 20-50KB。对本地字体（next/font/local），next/font 不自动子集化，需要手动用 fonttools（Python）或 subset-font.js 预处理。对中文网站，字体子集化尤其重要（中文字体动辄 5-10MB，子集化后可降到 500KB 以下）。我们是英文站，Google Fonts 自动子集化已足够，但如果引入本地品牌字体需注意。来源：Next.js font docs + Google Fonts CSS API 文档

  **落地计划**：
  - 下次迭代做 **P2-PERF-IMAGE-AUDIT-001**：审计所有图片是否用 next/image + priority（LCP 图片）+ width/height + sizes，远程图是否配置 remotePatterns，这是 LCP 优化的最直接手段
  - 同步做 **P2-PERF-FONT-AUDIT-001**：审计字体是否通过 next/font 加载，检查是否有 CSS @import Google Fonts（绕过自托管导致额外请求 + CLS）
  - **P2-PERF-AVIF-001**：在 next.config 启用 AVIF 格式（images.formats: ['image/avif', 'image/webp']），减少图片体积 20-50%


- [2026-09-22] **Next.js Partial Prerendering (PPR) + Streaming + Suspense 2026 完整指南（15 个权威知识点，Next.js 官方 docs + Vercel 官方 + React 19）**
  1. **PPR 定义：静态 shell + 动态 hole 单路由混合渲染**——Partial Prerendering 在构建时生成静态 HTML shell 和 postponedState blob，请求时立即返回 shell，动态部分通过 Suspense 边界流式传输。消除了"全静态 vs 全动态"的二元选择。shell 之外全是静态内容，Suspense 边界内是动态 hole。来源：https://nextjs.org/docs/app/getting-started/partial-prerendering + https://nextjs.org/docs/app/guides/ppr-platform-guide
  2. **PPR 在 Next.js 16 正式稳定，experimental 标志已移除**——Next.js 16（2025-10-21 发布）中 PPR 正式稳定，`experimental.ppr` 标志已移除。通过 `cacheComponents: true` 在 next.config 启用，内置在 Cache Components 模型中。Next.js 16 应用使用 Cache Components 时部署到 Vercel 自动获得 PPR。来源：https://vercel.com/docs/frameworks/full-stack/nextjs + https://toolchew.com/en/deepdive-static-vs-dynamic-2026/
  3. **我们项目是 Next.js 14.2.5，PPR 仍在 experimental 阶段**——Next.js 14 中 PPR 需要 `experimental: { ppr: 'incremental' }` 在 next.config.mjs 启用，且每个路由段加 `export const experimental_ppr = true`。升级到 Next.js 15/16 后才能用稳定版 PPR。但升级前可以先用 Streaming + Suspense（App Router 默认支持，不需要 PPR 标志）。来源：Next.js 14 官方 docs + https://nextjs.org/docs/app/guides/streaming
  4. **Streaming 是 App Router 默认启用的，不需要 PPR 标志**——Next.js App Router 默认支持流式渲染。用 `<Suspense>` 边界包裹异步组件，fallback UI 先渲染，内容就绪后流式替换。`loading.tsx` 文件自动用 Suspense 包裹整个路由段。Streaming 改善 TTFB 和 FCP，因为浏览器可以在数据还在加载时就开始解析 HTML。来源：https://nextjs.org/docs/app/guides/streaming + https://nextjs.org/docs/app/getting-started/caching
  5. **Suspense 边界是 PPR 的核心机制**——Suspense 边界定义了"静态 shell 在哪里结束，流式传输从哪里开始"。构建时，Suspense 之外的内容被预渲染为静态 HTML，Suspense 之内的内容留下占位符。请求时 shell 立即返回，Suspense 内容并行流式填充。多个兄弟 Suspense 边界可以并行流式传输。来源：https://nextjs.org/docs/app/glossary + https://nextjs.org/docs/app/guides/streaming
  6. **PPR 的 TTFB 性能：静态 shell 20-80ms（p75，Vercel 边缘网络）**——PPR 页面的静态 shell 从 CDN 边缘缓存返回，TTFB p75 在 20-80ms。相比全动态 SSR（TTFB 200-800ms+）有数量级提升。感知加载速度大幅优于全动态页面，且不需要每次请求都付冷启动代价。来源：https://toolchew.com/en/deepdive-static-vs-dynamic-2026/ + https://dev.to/nayankyada/nextjs-in-2026-honest-practitioner-take-on-whats-working-and-what-isnt-4j36
  7. **PPR 与 ISR 的区别：不是替代关系，可结合使用**——ISR（Incremental Static Regeneration）按时间间隔重新生成整页；PPR 提供静态 shell + 动态 hole 即时服务。两者可结合：ISR with Cache Components + Partial Prefetching 让每个路由首次访问即时响应，即使是构建时未包含的 URL。ISR 按需重新验证在 Vercel 上全局传播约 300ms（无需重新部署）。来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration-cache-components + https://www.techtic.com/blog/why-nextjs-15-is-best-for-headless-commerce/
  8. **`use cache` 指令：缓存组件结果到静态 shell**——React 19 的 `use cache` 指令（Next.js Cache Components 模型的一部分）让组件结果被缓存并包含在静态 shell 中，只要其生命周期不太短。即使组件有异步数据获取，只要数据不依赖请求信息（cookies/headers/params），就可以被缓存到 shell。与 Suspense 配合：Suspense 内的组件用 `use cache` 可以被预渲染到 shell。来源：https://nextjs.org/docs/app/getting-started/caching + https://nextjs.org/docs/app/getting-started/cache-components
  9. **PPR 的 postponedState blob 机制**——构建时，PPR 为每个启用路由生成静态 HTML shell + `postponedState` blob（包含动态部分的序列化状态）。请求时，CDN 返回 shell，边缘函数读取 postponedState 并渲染动态部分，通过同一个 HTTP 响应流式传输。PPR 需要平台支持：Vercel 原生支持，其他平台需实现 PPR Platform Guide 中的不同级别（Level 1: 静态 shell + 客户端获取，Level 2: 单请求流式，Level 3: 边缘流式）。来源：https://nextjs.org/docs/app/guides/ppr-platform-guide
  10. **Vercel PPR Observability 仪表盘**——Vercel 仪表盘有 PPR Observability 页面，显示哪些请求在提供静态内容、动态内容或两者混合。用于确认静态 shell 正常工作、发现回退到全动态的路由、查看函数运行时机。这是调试 PPR 性能的关键工具。升级到 Next.js 16 后可使用。来源：https://vercel.com/blog/vercel-supports-next-js-16-3
  11. **Streaming 的 CLS 陷阱：fallback 与内容尺寸不匹配**——当 Suspense fallback 被解析后的内容替换时，如果两者尺寸不同，会导致布局偏移（CLS）。解决方案：设计与内容尺寸匹配的骨架屏（skeleton），在 Suspense 边界外用固定或 min-height 容器预留空间。这与 Core Web Vitals CLS 优化直接相关。来源：https://nextjs.org/docs/app/guides/streaming + Core Web Vitals 学习笔记
  12. **`loading.tsx` vs 手动 Suspense：粒度控制**——`loading.tsx` 自动用 Suspense 包裹整个路由段，适合整页加载状态。但如果只想让页面的某个部分流式加载（如侧边栏、评论区），应该手动用 `<Suspense>` 包裹特定组件，这样静态 shell 包含更多真实内容，TTFB/FCP 更好。最佳实践：把 Suspense 边界尽量下推到具体的异步数据获取组件，而不是整页。来源：https://nextjs.org/docs/app/guides/streaming + https://nextjs.org/docs/app/guides/public-static-pages
  13. **并行流式传输：多个兄弟 Suspense 边界同时渲染**——当多个组件执行异步工作（获取数据、读数据库）时，用各自的 Suspense 边界包裹它们，Next.js 会并行渲染所有动态部分，而不是串行等待。关键：不要把多个异步组件嵌套在同一个 Suspense 中（会变成串行），应该用兄弟 Suspense 边界。来源：https://nextjs.org/docs/app/guides/streaming
  14. **我们项目的 PPR/Streaming 适用性分析**——我们的项目是纯 SSG（533 工具页 + 105 博客文章，全部静态生成），目前没有动态内容（无用户登录、无个性化、无实时数据）。所以 PPR 对我们当前架构**没有直接收益**——全静态已经是最快的渲染模式。但如果未来添加：(a) 实时工具定价/月访问量数据（需要动态获取），(b) 用户个性化推荐，(c) 评论系统，那么 PPR + Streaming 就有价值。当前可以做的是：(a) 审计是否有页面意外变成动态渲染（使用了 cookies()/headers()/searchParams 导致全页动态），(b) 工具页重型组件用 `next/dynamic` 懒加载减少首屏 JS。来源：项目架构分析 + Next.js 官方 docs
  15. **Next.js 16.3 AI 驱动即时导航（2026-09 新特性）**——Next.js 16.3 引入运行时预渲染（runtime prerendering）和浏览器级缓存，通过 AI 编码 agent 自动优化导航路径。Vercel 在 v0 平台上成功部署了自主编码 agent，将缓慢的用户旅程转换为即时过渡，无需大规模客户端数据获取重构。这是 PPR + Cache Components 模型的进一步演进。升级路径：Next.js 14 → 15（React 19 + 缓存变更）→ 16（PPR 稳定 + Turbopack 默认）→ 16.3（AI 导航优化）。来源：https://codeguilds.com/next-js-16-3-revolutionizes-web-performance-with-ai-driven-instant-navigations-and-cache-component-optimizations/

  **落地计划**：
  - 下次迭代做 **P2-PERF-SSG-AUDIT-001**：审计所有页面是否意外使用了 cookies()/headers()/searchParams 导致全页动态渲染（失去 SSG 优势），这是纯静态站最常见的性能回退
  - 同步做 **P2-PERF-NEXTDYNAMIC-001**：工具页重型组件（大 JSON 渲染、对比表格）用 `next/dynamic` 懒加载，减少首屏 JS 体积，改善 INP
  - **P2-UPGRADE-NEXT16-001**：规划升级到 Next.js 16（获得稳定 PPR + Turbopack 默认 + AI 导航优化），但这是大工程，先做兼容性评估再动手


- [2026-09-22] **AI 搜索优化（AIO/GEO）2026 完整指南：llms.txt + AI 爬虫 + GSC API + Indexing API（15 个权威知识点，Google Search Central + Cloudflare + OpenAI + Anthropic）**
  1. **Google 官方明确：llms.txt 不影响搜索排名和 AI Overviews**——2026-05-15 Google AI Optimization Guide 首次声明，2026-07-10 更新 mythbusting 章节，2026-08-31 文档更新再次确认："You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search"。Google Search 完全忽略 llms.txt 用于排名。创建它无害但也无 Google 排名帮助。来源：https://developers.google.com/search/updates?id=5 + https://dev.to/alifar/google-says-llmstxt-does-not-affect-search-or-ai-overviews-what-seo-teams-should-do-2f81
  2. **llms.txt 对非 Google AI 引擎仍有价值**——Perplexity 已在其文档中暴露 llms-full.txt，Anthropic Claude 和 OpenAI 的 agent 会参考 llms.txt 来更高效地爬取站点。没有这个文件，AI agent "可能"花更多时间爬取（may，不是一定找不到）。llms.txt v2 规范（2026-09 发布，基于 137,000 域名分析）允许子路径文件，最具体的文件优先，支持 `.md` 扩展名替换。来源：https://dev.to/angeo/llmstxt-v2-what-the-spec-says-and-what-137000-domains-show-48bh + https://kaizen360.cl/wp-content/uploads/2026/04/Informe_LLM_Search_Agentic_Commerce.pdf
  3. **Google Indexing API 仅限 JobPosting 和 BroadcastEvent(VideoObject) 页面**——这是 Google 的硬性限制。普通内容页面（博客文章、工具评测、分类页）不能用 Indexing API 请求索引。对于普通页面，只能通过 sitemap.xml + 自然爬取，或在 GSC 手动"请求编入索引"。我们的工具评测页不属于这两类，所以 Indexing API 对我们无效。来源：https://developers.google.com/search/apis/indexing-api/v3/quota-pricing?hl=en
  4. **Indexing API 技术细节**——POST 到 `https://indexing.googleapis.com/v3/urlNotifications:publish`，body 为 `{"url": "...", "type": "URL_UPDATED"}`。支持批量请求（batch endpoint `https://indexing.googleapis.com/batch`），但配额按 URL 级别计算（10个URL合并成1个HTTP请求仍算10次配额）。需要 service account JSON key + GSC 财产验证。全部免费。来源：https://developers.google.com/search/apis/indexing-api/v3/using-api?hl=en
  5. **AI 爬虫 User-Agent 完整清单（2026 现行）**——GPTBot（OpenAI 训练爬虫）、OAI-SearchBot（OpenAI 搜索爬虫）、ChatGPT-User（用户在 ChatGPT 中发起浏览）、ClaudeBot（Anthropic 训练爬虫）、Claude-SearchBot（Claude 搜索爬虫）、Claude-User（Anthropic 用户浏览）、PerplexityBot、Perplexity-User、Google-Extended（Google AI 训练，与 Googlebot 完全分开）、Applebot-Extended、Amazonbot、OAI-AdsBot（OpenAI 广告爬虫）。来源：https://capston.ai/robots-txt-for-ai-bots/ + http://raw.githubusercontent.com/kostja94/marketing-skills/main/skills/seo/technical/robots/SKILL.md
  6. **ChatGPT-User 不再尊重 robots.txt（2025年12月重大变更）**——用户在 ChatGPT 中发起的浏览（ChatGPT-User）不再遵守 robots.txt 规则。要阻止它，必须用服务端控制（Cloudflare WAF 规则、IP 拦截），而非 robots.txt。相比之下，Claude-User 仍尊重 robots.txt（这是两者的关键区别）。这意味着如果我们想被 ChatGPT 引用，robots.txt Allow 不够，还需确保 Cloudflare WAF 不拦截 ChatGPT-User 的 IP 段。来源：http://raw.githubusercontent.com/kostja94/marketing-skills/main/skills/seo/technical/robots/SKILL.md + https://blog.cloudflare.com/accountable-mixed-use-ai-crawlers/
  7. **Google-Extended 与 Googlebot 是完全分开的爬虫**——Googlebot 用于搜索排名（必须 Allow），Google-Extended 用于 AI 训练（Gemini 等）。在 robots.txt 中 `Disallow: /` Google-Extended 不会影响 Google 搜索排名，只会阻止内容被用于 AI 训练。Google 还在 GSC 设置中提供了开关来排除站点内容出现在生成式搜索结果（AI Overviews）中。对我们的策略：Allow Googlebot（必须），Allow Google-Extended（希望被 Gemini 引用）。来源：https://blog.cloudflare.com/accountable-mixed-use-ai-crawlers/
  8. **Cloudflare Bot Preference Sync（2026-08 发布）**——Cloudflare 推出 Bot Preference Sync，可根据你在 AI bot 配置中的设置自动更新 robots.txt，无需手动维护静态文件。从免费版到企业版都可用。可针对 Search（搜索引用）和 Agent（AI agent 爬取）两类 bot 分别配置偏好。我们的站点在 Cloudflare 后面，可以考虑启用这个功能来统一管理 AI 爬虫策略。来源：https://blog.cloudflare.com/bot-preference-sync/
  9. **AI 爬虫速率限制建议**——GPTBot 建议 100/min、ChatGPT-User 50/min、Google-Extended 200/min、Applebot-Extended 100/min、ClaudeBot 50/min、PerplexityBot 30/min。注意：robots.txt 的 `Crawl-delay` 指令并非所有 AI 爬虫都支持（Google 爬虫明确不支持 Crawl-delay）。更可靠的速率限制方式是 Cloudflare WAF 速率限制规则（基于 User-Agent + IP）。来源：https://www.tencentcloud.com/techpedia/143900?lang=en
  10. **AEO vs GEO vs SEO 三者区别**——AEO（Answer Engine Optimization）针对问答引擎（Quora、Reddit 引用、论坛）；GEO（Generative Engine Optimization）针对生成式 AI 搜索（ChatGPT、Perplexity、Claude、Google AI Overviews）；SEO 针对传统搜索引擎（Google、Bing 蓝色链接）。GEO 的核心优化手段：内容结构清晰（H2/H3 分段）、有明确的问答格式（FAQ 章节）、有权威引用和数据来源、有结构化数据（FAQPage/HowTo/Review）、有"Quick Answer"段落（AI 最喜欢引用的格式）。来源：https://criticnest.com/how-to-rank-in-ai-overviews/
  11. **Google AI Overviews 实际排名因素（2026 观察）**——Google 官方表示 AI Overviews 使用与传统搜索相同的排名基础（原创有用内容、可爬取、E-E-A-T），不需要特殊标记。但实际 SEO 行业观察发现：有 FAQPage 结构化数据的页面更容易被 AI Overview 引用答案（因为 FAQ 格式天然匹配 AI 的问答提取）；有明确"Quick Answer"或 TL;DR 段落的页面被引用率更高；有 Review 结构化数据且 ratingValue 合理的产品页更容易出现在 AI Overviews 的产品推荐中。来源：https://criticnest.com/how-to-rank-in-ai-overviews/ + https://developers.google.com/search/updates?id=5
  12. **IndexNow 与 Google Indexing API 的关键区别**——IndexNow 是 Microsoft Bing 推出的协议，支持 Bing、Yandex、Seznam、Naver 等搜索引擎，**不支持 Google**。我们项目已配置 IndexNow key，新文章发布后自动提交到 IndexNow。但 Google 不接收 IndexNow 推送，Google 的索引只能通过 sitemap.xml 提交 + 自然爬取，或 GSC 手动请求（普通页面无法用 API）。所以"GEO 自动提交到 Google"这个用户需求，对普通页面只能靠 sitemap.xml 更新频率 + GSC 手动，无法完全自动化。来源：Google Indexing API docs + IndexNow 官方协议文档
  13. **GSC Search Analytics API 可自动化数据拉取**——Google Search Console API（不同于 Indexing API）可以程序化拉取搜索分析数据：点击、曝光、CTR、平均排名、查询词、页面、国家、设备、搜索外观。API 配额：每天 50,000 次请求，每次最多返回 25,000 行。我们项目已有 gsc-ga4-report/ 目录。可以用 GitHub Actions 定时（每周）拉取 GSC 数据到 CSV/JSON，供 OpenSEO 或数据分析使用，无需手动下载。来源：Google Search Console API 官方文档
  14. **OpenAI 广告爬虫 OAI-AdsBot（2026 新爬虫）**——OpenAI 推出 OAI-AdsBot 专门用于广告相关的网页爬取（广告客户验证、落地页质量评估）。OpenAI 帮助中心明确说明：如果 robots.txt 中 Disallow 了 OAI-AdsBot，爬取会立即停止。对于接入了 Impact/AdSense 等联盟广告的我们，应该 Allow OAI-AdsBot 以确保广告联盟平台能正确验证我们的落地页。来源：OpenAI Help Center - Advertiser Guidance for Allowing OpenAI Web Crawlers（2026-09-21）
  15. **我们项目的 AIO/GEO 具体行动清单**——(a) 检查 public/robots.txt 是否显式 Allow GPTBot/OAI-SearchBot/ClaudeBot/PerplexityBot/Google-Extended/OAI-AdsBot（P2-SEO-AI-CRAWLERS-001）；(b) 考虑添加 public/llms.txt（虽然 Google 不用，但 Perplexity/Claude agent 会参考，低成本高收益，列出工具页和博客文章 URL）（P2-SEO-LLMSTXT-001）；(c) 所有新文章确保有 FAQPage 结构化数据（P2-SCHEMA-FAQ-001 已在待办）；(d) 用 GSC Search Analytics API + GitHub Actions 自动化拉取每周数据（P2-SEO-GSC-API-001）；(e) 检查 Cloudflare WAF 规则是否误拦 ChatGPT-User/Claude-User 的 IP 段（用户之前提过"检查 Cloudflare WAF 有没有拦 AI 爬虫"）（P1-SEO-CLOUDFLARE-WAF-001）；(f) 给高流量文章加"Quick Answer"段落提升 AI Overviews 引用率（P2-GEO-QUICKANSWER-001）。

  **落地计划**：
  - 下次迭代优先做 **P1-SEO-CLOUDFLARE-WAF-001**：检查 Cloudflare WAF 是否误拦 AI 爬虫（GPTBot/ChatGPT-User/ClaudeBot/PerplexityBot），这是用户明确要求过的 P0 级需求
  - 同步做 **P2-SEO-AI-CRAWLERS-001**：在 robots.txt 中显式列出所有 AI 爬虫并 Allow，替代当前的 `User-agent: *` 通配
  - **P2-SEO-LLMSTXT-001**：生成 llms.txt 文件（列出所有工具页和博客文章 URL），虽然 Google 不用但对 Perplexity/Claude 有价值


- [2026-09-22] **Core Web Vitals 2026 完整优化指南：LCP + INP + CLS（15 个权威知识点，web.dev + Next.js 官方 + Vercel + MDN）**
  1. **三大 Core Web Vitals 阈值（2026 现行标准）**：LCP（最大内容绘制）良好 <2.5s，需改善 2.5-4s，差 >4s；INP（交互到下一次绘制）良好 <200ms，需改善 200-500ms，差 >500ms；CLS（累积布局偏移）良好 <0.1，需改善 0.1-0.25，差 >0.25。INP 已于 2024 年 3 月正式取代 FID 成为第三大 Core Web Vital。来源：https://web.dev/articles/top-cwv + https://maxtdesign.com/learn/performance/core-web-vitals-2026-blueprint
  2. **LCP 优化核心：LCP 元素通常是首屏大图或文本块**。关键手段：(a) 对 LCP 图片使用 `next/image` 的 `priority` 属性（跳过懒加载，立即加载）；(b) 用 `<link rel="preload" as="image">` 预加载关键资源；(c) 确保首屏内容服务端渲染（SSG/ISR）；(d) 优化 TTFB（CDN 边缘缓存、ISR revalidate）；(e) 对 LCP 元素加 `fetchpriority="high"`。来源：https://nextjs.org/docs/app/guides/production-checklist + https://vercel.com/kb/guide/how-to-improve-core-web-vitals
  3. **INP 优化：三阶段模型（输入延迟→处理时间→呈现延迟）**。INP 测量页面生命周期内所有交互（点击/触摸/键盘），报告最差的一个（忽略异常值）。输入延迟：主线程被长任务阻塞时用户输入排队；处理时间：事件处理函数本身执行慢；呈现延迟：DOM 过大或强制同步布局导致渲染慢。来源：https://vercel.com/kb/guide/how-to-improve-core-web-vitals + https://web.dev/articles/top-cwv
  4. **INP 优化手段：拆分长任务 + 轻量处理函数 + 最小化 DOM**。(a) 任何 >50ms 的 JS 任务都会阻塞主线程，用 `scheduler.yield()`（Chrome 129+）或 `setTimeout(..., 0)` 拆分；(b) 事件处理函数保持 <50ms；(c) 最小化 DOM 节点数减少呈现延迟；(d) 避免强制同步布局（layout thrashing：先读 layout 再写 layout 再读）；(e) CPU 密集型工作移到 Web Worker；(f) React 非紧急状态更新用 `useTransition`。来源：https://freedevtool.org/guides/web-performance-guide + https://qiita.com/tuanphan/items/8f1b05c18aaa67531000
  5. **CLS 优化：预留空间 + 保持内容稳定**。布局偏移发生在浏览器在知道附近元素最终尺寸前就渲染了内容。最常见原因：图片没有显式尺寸、动态加载的广告、注入的 UI（cookie 横幅）。关键手段：(a) 所有图片/视频设置 width/height（next/image 自动处理）；(b) 媒体容器用 CSS `aspect-ratio`；(c) 广告位用 `min-height` 预留空间；(d) 字体用 `font-display: swap` 或 `optional` 防止 FOUT/FOIT 偏移；(e) 不要在加载后在首屏上方插入内容；(f) 动画用 CSS transform 而非改变 layout 的属性。来源：https://botmonster.com/posts/optimize-core-web-vitals-lcp-cls-inp/ + https://web.dev/articles/top-cwv
  6. **Next.js Streaming + Suspense 的 CLS 陷阱**：当 Suspense fallback 被解析后的内容替换时，浏览器会重排页面。如果 fallback 和最终内容尺寸不同，周围布局就会偏移。解决方案：设计与内容尺寸匹配的骨架屏（skeleton），在 Suspense 边界外用固定或 min-height 容器预留空间。来源：https://preview.nextjs.org/docs/app/guides/streaming
  7. **web-vitals 库 + Next.js useReportWebVitals 进行真实用户监控（RUM）**。Next.js 内置 `useReportWebVitals` hook（pages/_app.tsx 或 app layout）可捕获 LCP/FID/CLS/TTFB/FCP/INP。我们的项目已有 WebVitalsReporter 组件，但需确认它是否专门捕获 INP（INP 是 2024 年后新增指标，旧版 web-vitals 库可能不包含）。来源：https://nextjs.org/docs/app/guides/production-checklist + https://nextjs.net.cn/docs/app/building-your-application/optimizing/analytics
  8. **TTFB 是 LCP 的前置指标**：TTFB（首字节时间）差会延迟所有后续指标包括 LCP。Vercel 部署通过边缘网络自动优化 TTFB。ISR（Incremental Static Regeneration）配合 `revalidate` 可大幅改善用户看到内容的时间。Next.js 14+ 的 Partial Prerendering 进一步优化 TTFB/FCP/LCP。我们的项目是 SSG，TTFB 应该已经很好，但工具详情页如果数据量大可能需要 ISR。来源：https://vercel.com/resources/how-vercel-improves-your-websites-search-engine-ranking
  9. **next/image 对 LCP 和 CLS 的双重优化**：next/image 自动：压缩为 WebP/AVIF、视口外图片懒加载、生成响应式尺寸、预留宽高比防止 CLS。对 LCP 首屏大图，必须加 `priority` 属性和 `sizes` 属性。我们的 next.config.mjs 已配置 `formats: ["image/avif", "image/webp"]`，但工具页截图可能仍在用原生 `<img>`（P1-PERF-IMG-001 待办）。来源：https://www.toolsku.com/en/blog/nextjs-app-router-performance-2026/ + Next.js 官方 docs
  10. **next/font 对 CLS 的优化**：next/font（我们项目用的 GeistSans/GeistMono from geist/font）自托管字体并预加载，防止 FOIT（不可见文本闪烁）和 FOUT（无样式文本闪烁），这两种都是 CLS 的常见来源。我们的 layout.tsx 已正确使用 GeistSans 和 GeistMono，CLS 字体偏移风险已消除。来源：https://nextjs.org/docs/app/guides/production-checklist + https://botmonster.com/posts/optimize-core-web-vitals-lcp-cls-inp/
  11. **INP 差的根因通常是 JS 包体积过大**：过多 JS 竞争主线程是 INP 差的 #1 原因。Next.js 默认按路由段代码分割，但重型 Client Components 仍会打包进客户端 bundle。优化手段：`next/dynamic` 懒加载重型组件、Tree Shaking（用 ES module）、替换重型库（moment→dayjs 从 300KB 降到 2KB、lodash→es-toolkit 从 70KB 降到 3KB、axios→原生 fetch）。来源：https://dev.to/rverwey/core-web-vitals-checklist-for-small-business-websites-4ef7 + 我们刚学的 TypeScript/构建优化笔记
  12. **Cookie 横幅/通知栏是 CLS 的隐形杀手**：动态插入到现有内容上方的 UI（cookie 同意横幅、通知条）会把所有内容下推，造成布局偏移。如果横幅在顶部插入，影响分数最大。解决方案：用 `position: fixed` 或 `absolute` 定位横幅（不影响文档流），或在容器上用 `min-height` 预留空间。我们的项目需要检查是否有 cookie 横幅（P2-PERF-CLS-003 待办）。来源：https://dev.to/apogeewatcher/lcp-inp-cls-what-each-core-web-vital-means-and-how-to-fix-it-4oln
  13. **实验室数据 vs 真实用户数据（Field Data）**：Lighthouse 是实验室模拟测试，而 Google 排名用的是 CrUX（Chrome UX Report）的真实用户数据（p75）。必须两者结合看：Lighthouse 找可优化点，GSC Core Web Vitals 报告看真实用户体验。我们的 P2-PERF-INP-003 待办就是检查 GSC CWV 报告的真实 p75 INP。来源：https://nextjs.org/docs/app/guides/production-checklist + https://www.corewebvitals.io/core-web-vitals/ultimate-checklist
  14. **scheduler.yield() 是 INP 优化的新利器**：Chrome 129+ 支持 `scheduler.yield()`，比 `requestIdleCallback` 更有效因为它立即让出主线程给浏览器而不是等空闲时间。对于关键路径上的长任务（如大数据处理、DOM 操作），用 `await scheduler.yield()` 拆分。旧浏览器回退到 `setTimeout(fn, 0)`。来源：https://freedevtool.org/guides/web-performance-guide + https://web.dev/articles/top-cwv
  15. **我们项目的 CWV 具体行动清单**：(a) 确认 WebVitalsReporter 捕获 INP 并上报 p75（P1-PERF-INP-001 升级 attribution build）；(b) 工具页首屏截图加 `fetchpriority="high"`（P1-PERF-LCP-001）；(c) 审计所有原生 `<img>` 标签缺少 width/height 的情况（P2-PERF-CLS-001）；(d) 非紧急 CTA 点击追踪包在 `requestIdleCallback` 中（P1-PERF-INP-002）；(e) 查 GSC CWV 报告真实 p75 INP（P2-PERF-INP-003）；(f) 考虑接入 Vercel Speed Insights 做 RUM 仪表盘（P2-PERF-SPEEDINSIGHTS-001）；(g) 工具页截图从原生 img 迁移到 next/image（P1-PERF-IMG-001）。来源：综合以上 web.dev + Next.js + Vercel 官方文档

  **落地计划**：
  - 下次迭代优先做 P1-PERF-LCP-001：工具页首屏截图加 fetchpriority="high"，直接改善 LCP
  - 同步做 P1-PERF-INP-002：非紧急 CTA 点击追踪包 requestIdleCallback，减少主线程竞争改善 INP
  - P2-PERF-CLS-001：审计原生 <img> 标签缺 width/height，配合 P1-PERF-IMG-001 迁移 next/image 一起做


- [2026-09-22] **前端工程化最佳实践：TypeScript 严格模式 + 代码分割 + Next.js 构建优化（15 个权威知识点，TypeScript 官方 + Next.js 官方）**
  1. **`strict: true` 一次性开启 8 个子选项**：`noImplicitAny`、`strictNullChecks`、`strictFunctionTypes`、`strictBindCallApply`、`strictPropertyInitialization`、`noImplicitThis`、`useUnknownInCatchVariables`、`alwaysStrict`。可单独关闭某一项，但官方建议全开。来源：https://www.typescriptlang.org/tsconfig/ + https://www.typescriptlang.org/docs/handbook/2/basic-types.html
  2. **`noImplicitAny` 是最重要的第一道防线**：当 TypeScript 无法推断类型时，变量默认退化为 `any`，`noImplicitAny` 会把这种隐式 any 标记为错误。这迫使开发者显式声明类型，避免"any 编程"。我们的项目 tsconfig 应确认已开启。来源：https://www.typescriptlang.org/docs/handbook/2/everyday-types.html + https://www.typescriptlang.org/tsconfig/noImplicitAny.html
  3. **`strictNullChecks` 消除"undefined is not a function"类运行时错误**：开启后 `null` 和 `undefined` 有各自独立类型，不能赋值给具体类型变量。访问可能为 null 的属性前必须先做 null check（`if (x !== null)` 或可选链 `x?.prop`）。这是减少生产 bug 最有效的单一选项。来源：https://www.typescriptlang.org/tsconfig/strictNullChecks.html + https://microsoft.github.io/TypeScript-New-Handbook/everything/
  4. **`strictFunctionTypes` 把函数参数从双变(bivariant)改为逆变(contravariant)**：默认（关闭时）TypeScript 对函数参数采用双变检查，这是为了向后兼容 Array 等内置类型，但会放过类型不安全的函数赋值。开启后函数参数严格逆变检查，方法（method syntax）仍保持双变。这能捕获"把接收 string 的函数传给需要 number 的参数"这类错误。来源：https://www.typescriptlang.org/tsconfig/strictFunctionTypes.html
  5. **`noImplicitReturns` 确保函数所有分支一致返回**：如果函数某些代码路径有 return 而其他路径没有（隐式返回 undefined），会报错。这避免了"函数有时返回值有时不返回"导致的调用方 bug。对我们的工具数据处理函数（如筛选/排序/格式化）尤其重要。来源：https://www.typescriptlang.org/tsconfig/noImplicitReturns.html
  6. **`noFallthroughCasesInSwitch` 防止 switch 意外穿透**：switch 中如果 case 没有 break/return/throw 且不是空 case 穿透到下一个，会报错。这是常见的隐蔽 bug 来源（忘记写 break）。来源：https://www.typescriptlang.org/tsconfig/noFallthroughCasesInSwitch.html
  7. **Next.js App Router 默认按路由段自动代码分割**：每个 route segment 生成独立 JS chunk，访问某页面只加载该页面所需代码，不加载全站代码。Server Components 不产生客户端 JS，只有 Client Components（`'use client'`）才会被打包进客户端 bundle。这是 Next.js 性能的基石。来源：https://nextjs.org/docs/15/app/guides/production-checklist + https://preview.nextjs.org/docs/app/glossary
  8. **`next/dynamic` 手动懒加载 Client Components 和第三方库**：`const Chart = dynamic(() => import('@/components/Chart'), { loading: () => <p>Loading...</p>, ssr: false })`。适合重型组件（图表、编辑器、地图）只在需要时加载。`ssr: false` 表示只在客户端渲染（避免 SSR 不兼容的库报错）。注意：`dynamic()` 不能在 React 组件内部调用，必须在模块顶层。来源：https://nextjs.org/docs/15/app/guides/lazy-loading + https://nextjs.org/docs/pages/guides/lazy-loading
  9. **Tree Shaking 自动移除未使用代码**：Next.js 构建时自动 tree-shake，只打包实际 import 并使用的代码。但前提是用 ES module 语法（`import { x } from 'pkg'`）而非 CommonJS（`const pkg = require('pkg')`），且包本身要 sideEffects 友好。对于 lodash 这类库，用 `lodash-es`（ES module 版）或 `import debounce from 'lodash/debounce'` 路径导入，避免打包整个 lodash（~70KB gzip）。来源：https://preview.nextjs.org/docs/app/glossary + https://nextjs.org/docs/15/pages/guides/package-bundling
  10. **`@next/bundle-analyzer` 可视化分析包体积**：在 `next.config.mjs` 里 `const withBundleAnalyzer = require('@next/bundle-analyzer')({ enabled: process.env.ANALYZE === 'true' })`，然后 `ANALYZE=true npm run build` 生成 treemap 报告。能看到每个 chunk 里每个模块占多少字节，找出意外打包的大库（如 moment.js ~300KB 可用 dayjs ~2KB 替代）。来源：https://nextjs.org/docs/15/pages/guides/package-bundling + GitHub vercel/next.js
  11. **Turbopack（Rust 编写）是 Next.js 15 默认开发构建器**：增量计算（函数级缓存，结果持久化到磁盘）+ 懒打包（只打包 dev server 实际请求的模块），大型应用冷启动比 webpack 快 10 倍。生产构建仍用 webpack（Turbopack 生产构建在 Next.js 15 中为 beta）。开发时 `next dev --turbopack` 或在 next.config 里开启。来源：https://nextjs.org/docs/15/app/api-reference/turbopack + https://nextjs.org/blog/turbopack-chunking
  12. **`transpilePackages` 处理 monorepo 和未预编译的外部包**：在 `next.config.mjs` 里 `transpilePackages: ['@myorg/ui', 'some-untranspiled-pkg']`，Next.js 会用 SWC 编译这些包（通常 node_modules 里的包不被编译）。适合 monorepo 内部包或发布时未编译的 ESM 包。来源：https://nextjs.org/docs/15/pages/guides/package-bundling
  13. **第三方库选型对包体积影响巨大**：moment.js(~300KB) → dayjs(~2KB)；lodash(~70KB) → lodash-es 按需导入或 es-toolkit(~3KB)；axios(~30KB) → 原生 fetch（Next.js 18+ 已内置）；markdown-it(~100KB) → 轻量替代。我们的项目应检查 package.json，用 bundle analyzer 确认哪些库占比最大。来源：https://nextjs.org/docs/15/app/guides/production-checklist + bundlephobia.com
  14. **生产构建优化清单（Next.js 官方）**：(a) 尽量用 Server Components（零客户端 JS）；(b) Client Components 用 `next/dynamic` 懒加载重型部分；(c) 图片用 `next/image`（自动压缩/WebP/AVIF/懒加载）；(d) 字体用 `next/font`（自托管+预加载，避免 FOIT）；(e) 路由预取（`<Link>` 自动 prefetch 视口内链接）；(f) 数据缓存（`fetch` 的 `revalidate`/`cache`）；(g) 部署到 Vercel Edge/CDN。来源：https://nextjs.org/docs/15/app/guides/production-checklist
  15. **我们项目的具体落地建议**：(a) 确认 tsconfig.json `strict: true` 已开启，如未开启则逐步迁移（先开 noImplicitAny + strictNullChecks，修完错误再开其他）；(b) 用 `@next/bundle-analyzer` 跑一次分析，找出最大的 3 个客户端 chunk；(c) 检查是否有重型 Client Components 可以改为 Server Component 或用 `next/dynamic` 懒加载（如富文本编辑器、图表组件）；(d) 确认 `next/font` 和 `next/image` 已全站使用；(e) 考虑开发环境开启 Turbopack 加速本地开发。来源：综合以上 TypeScript + Next.js 官方文档

  **落地计划**：
  - 下次迭代检查 tsconfig.json strict 模式开启状态，如未全开则逐步迁移（先开 noImplicitAny + strictNullChecks）→ 任务 P2-TS-STRICT-001
  - 用 @next/bundle-analyzer 跑一次包体积分析，找出最大的 3 个客户端 chunk 和可替代的重型库 → 任务 P2-BUNDLE-ANALYZE-001
  - 检查重型 Client Components（图表/编辑器）是否可用 next/dynamic 懒加载或改为 Server Component → 任务 P2-DYNAMIC-IMPORT-001


- [2026-09-22] **高星 GitHub 开源工具：SEO 审计 + 性能监控完整体系（15 个权威知识点，Google/Microsoft 官方 + 高星项目）**
  1. **Lighthouse（Google 官方，~30k stars）是所有审计的基线**：开源自动化工具，审计 performance/accessibility/SEO/best practices/PWA 五大类。CLI 用法 `npx lighthouse https://example.com --output json --output-path ./report.json`。Chrome DevTools 内置，PageSpeed Insights 也是它的云端版。每个审计都有参考文档解释为什么重要+怎么修。来源：https://developer.chrome.com/docs/lighthouse/overview
  2. **Lighthouse CI（LHCI）防止性能回归**：在 GitHub Actions 里跑 `lhci autorun`，自动收集多次运行的中位数分数，对比基线，如果分数下降超过阈值就 fail build。配置 `.lighthouserc.json`：`ci.assert.lighthouse.performance >= 0.9`。支持上传报告到临时服务器或自建 LHCI server。来源：https://googlechrome.github.io/lighthouse-ci/docs/configuration.html
  3. **webhint（Microsoft，~3.7k stars）是可定制的 linting 工具**：不仅测性能，还测安全、可访问性、常见坑。可作为 VS Code 扩展实时提示，也可 CLI 跑 `npx hint https://example.com`。每个 hint 可单独开启/关闭，适合在 CI 里做代码级检查（而不是 Lighthouse 的页面级）。来源：https://webhint.io/ + GitHub webhintio/hint
  4. **sitespeed.io（~4.7k stars）是完整的性能测试套件**：集成 Lighthouse + WebPageTest + Browsertime + Coach，一次运行拿到 CWV、加载视频、HAR waterfall、改进建议。支持定时运行 + 指标发到 Graphite/InfluxDB + Grafana 看板做长期趋势追踪。Docker 镜像 `docker run sitespeedio/sitespeed.io https://example.com`。适合替代付费 SpeedCurve。来源：https://www.sitespeed.io/
  5. **WebPageTest（行业标准，开源）做多地点/多设备/多网络条件测试**：从全球多个测试节点跑，捕获加载视频、filmstrip、自定义指标、carbon footprint。API 可程序化调用 `https://www.webpagetest.org/runtest.php?url=...&k=API_KEY`。适合验证特定地区的 LCP（比如我们的目标市场美国/欧洲）。来源：https://www.webpagetest.org/
  6. **Unlighthouse（~2.5k stars）全站 Lighthouse 扫描**：`npx unlighthouse --site https://example.com` 自动爬取 sitemap 或站内链接，对每个页面跑 Lighthouse，生成全站报告。比手动逐个 URL 跑 Lighthouse 高效 10 倍。适合我们 533 个工具页 + 105 篇文章的全站性能审计。来源：https://github.com/harlan-zw/unlighthouse
  7. **Pa11y（~4k stars）自动化可访问性测试**：`pa11y https://example.com` 跑 WCAG 2.1 AA 标准，输出具体违规元素+建议。CI 集成 `pa11y-ci` 可配置阈值（如 `--threshold 10` 允许最多 10 个错误）。可访问性是 Google 排名的间接因素（影响跳出率和用户体验），也是法律合规要求。来源：https://pa11y.org/
  8. **webpack-bundle-analyzer + source-map-explorer 做包体积分析**：`webpack-bundle-analyzer`（~13k stars）可视化 webpack bundle 各模块占比树状图。`source-map-explorer`（~3.8k stars）不依赖 webpack，直接分析 source map。Next.js 项目用 `@next/bundle-analyzer` 包，在 `next.config.mjs` 里开启 `ANALYZE=true`。目标：首屏 JS < 200KB（gzip）。来源：GitHub webpack-contrib/webpack-bundle-analyzer + danvk/source-map-explorer
  9. **Lighthouse CI GitHub Action 一键集成**：`treosh/lighthouse-ci-action@v11`（~1.5k stars）在 GitHub Actions 里跑 Lighthouse CI，自动上传报告到 LHCI server 或临时 URL，PR 评论里贴分数对比。配置简单：`- uses: treosh/lighthouse-ci-action@v11 with: { urls: 'https://example.com', uploadArtifacts: true }`。适合我们在 PR 合并前拦截性能退化。来源：GitHub treosh/lighthouse-ci-action
  10. **性能预算（Performance Budget）是 CI 守门的核心**：在 `lighthouserc.json` 里设 `ci.assert.budgets`，指定每个资源类型的最大体积（如 `resourceSizes: [{ resourceType: script, budget: 200 }]` KB）和请求数量（`resourceCounts: [{ resourceType: total, budget: 50 }]`）。超预算直接 fail CI。来源：https://web.dev/articles/performance-budgets-101 + Lighthouse CI docs
  11. **Lab 数据 vs RUM 数据必须结合用**：Lighthouse/WebPageTest 是 Lab 数据（受控环境，单次运行），反映"能做到多好"；web-vitals 库/Speed Insights 是 RUM（Real User Monitoring）数据，反映"真实用户体验"（p75）。Google 排名用 RUM 的 Chrome User Experience Report（CrUX）数据。我们已有 WebVitalsReporter 上报 GA4，下一步用 Lighthouse CI 做 Lab 守门 + RUM 做长期趋势。来源：https://web.dev/articles/how-to-measure-speed
  12. **SEO 专项审计工具：SEO Spider 类**：开源替代 Screaming Frog 的有 `Screaming Frog SEO Spider`（付费但免费版限500URL）、`Beam Us Up`（开源，~1k stars）、`SEO Spider`（Python）。但我们已用 OpenSEO（本地部署）做全站技术 SEO 审计，不需要再引入爬虫工具。OpenSEO 的优势是 D1 数据库持久化 + 问题分类 + 趋势追踪。来源：各项目 GitHub
  13. **结构化数据验证工具**：Google Rich Results Test（官方，验证 schema 是否符合富摘要要求）、Schema.org Validator（官方，验证 schema 语法）、`schema-dts`（~1k stars，TypeScript 类型定义，编译时检查 JSON-LD 类型）。我们已在 Schema.tsx 里手写 JSON-LD，下一步可引入 `schema-dts` 做类型安全。来源：https://search.google.com/test/rich-results + GitHub google/schema-dts
  14. **Broken link checker 工具**：`broken-link-checker`（~1.5k stars）CLI 扫描全站死链，`linkinator`（~1.8k stars，Google 出品）更快更现代，`npx linkinator https://example.com --recurse`。适合定期检查 533 个工具页的外链是否失效（联盟链接失效=收入损失）。可在 GitHub Actions 每周跑一次，输出死链列表。来源：GitHub JustinBeckwith/linkinator
  15. **我们的工具选型建议（结合当前栈）**：(a) 日常 CI 守门 = Lighthouse CI（treosh/lighthouse-ci-action）+ 性能预算；(b) 全站扫描 = Unlighthouse（每月一次，覆盖所有 URL）；(c) 技术 SEO = OpenSEO（已部署本地，D1 数据库）；(d) RUM 趋势 = 已有 WebVitalsReporter → GA4；(e) 死链 = linkinator（每周 CI）；(f) 包体积 = @next/bundle-analyzer（每次大改后手动跑）。不需要全部引入，优先 Lighthouse CI + linkinator。来源：综合以上各工具文档

  **落地计划**：
  - 下次迭代加 Lighthouse CI GitHub Action（treosh/lighthouse-ci-action），对首页/工具页/文章页做性能预算守门 → 任务 P1-CI-LIGHTHOUSE-001
  - 加 linkinator 每周死链扫描 workflow，检查 533 个工具页外链 → 任务 P2-CI-DEADLINKS-001
  - 用 Unlighthouse 做一次全站 Lighthouse 扫描，找出性能最差的 10 个页面优先优化 → 任务 P2-PERF-UNLIGHTHOUSE-001


- [2026-09-22] **Next.js Security Headers + CSP + Middleware 2026 最佳实践（Google/Next.js 官方 docs，15 个权威知识点）**
  1. **6 个必备安全响应头（next.config.mjs headers）**：Strict-Transport-Security (HSTS)、X-Content-Type-Options (nosniff)、X-Frame-Options (SAMEORIGIN/DENY)、Referrer-Policy (strict-origin-when-cross-origin)、Permissions-Policy (camera/microphone/geolocation=())、Content-Security-Policy。在 next.config.mjs 的 `async headers()` 里用 `source: "/:path*"` 应用到所有路由。来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/headers
  2. **HSTS 标准值**：`Strict-Transport-Security: max-age=31536000; includeSubDomains`（1年）。加 `; preload` 前必须先提交到 hstspreload.org，否则不要加。Vercel 平台默认已对自定义域名加 HSTS，但检查确认。来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/headers + LogRocket
  3. **X-Content-Type-Options: nosniff**：防止浏览器 MIME-sniffing 攻击。唯一有效值是 `nosniff`。对用户上传/生成的文件尤其重要。来源：https://www.nextjs.cn/docs/advanced-features/security-headers
  4. **X-Frame-Options 已被 CSP frame-ancestors 取代**：X-Frame-Options: SAMEORIGIN 仍广泛支持，但现代浏览器优先用 CSP `frame-ancestors 'self'`。两者都加最安全（防御纵深）。来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/headers
  5. **Referrer-Policy: strict-origin-when-cross-origin**：同源导航发完整 URL，跨域只发 origin（不带路径/查询参数）。平衡安全和功能（联盟链接追踪需要 referrer）。来源：https://nextjs.org/docs/app/guides/progressive-web-apps
  6. **Permissions-Policy 禁用不需要的 API**：`Permissions-Policy: camera=(), microphone=(), geolocation=(), browsing-topics=()`。明确告诉浏览器本站不使用这些敏感 API，减少攻击面。来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/headers
  7. **CSP 两种配置方式**：(a) 静态 CSP 在 next.config.mjs headers 里（适合 SSG 全站）；(b) 动态 CSP 带 nonce 在 middleware.ts 里生成（每次请求新 nonce，需要动态渲染）。本站是 SSG，优先用静态 CSP。来源：https://nextjs.org/docs/app/guides/content-security-policy
  8. **CSP 基础指令模板**：`default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' blob: data: https:; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; upgrade-insecure-requests;`。Next.js 内联脚本需要 `'unsafe-inline'`（除非用 nonce）。来源：https://nextjs.org/docs/app/guides/content-security-policy
  9. **AdSense 接入需要 CSP 放行 Google 域名**：script-src 加 `https://pagead2.googlesyndication.com`、`https://googleads.g.doubleclick.net`；img-src 加 `https://*.googleusercontent.com`、`https://*.ggpht.com`；frame-src 加 `https://googleads.g.doubleclick.net`、`https://tpc.googlesyndication.com`；connect-src 加 `https://pagead2.googlesyndication.com`。如果 CSP 太严，AdSense 广告不会加载。来源：Google AdSense 帮助 + CSP spec
  10. **nonce + strict-dynamic 是最严格的 CSP 模式**：`script-src 'nonce-${nonce}' 'strict-dynamic'`——每个内联脚本带 nonce，strict-dynamic 自动信任由已信任脚本加载的脚本。但需要 middleware 每次生成 nonce，且会让所有页面变成动态渲染（失去 SSG 优势）。本站 SSG 优先，暂不采用。来源：https://nextjs.org/docs/15/app/guides/content-security-policy + dev.to field notes
  11. **middleware.ts 设置响应头**：`export function middleware(request) { const res = NextResponse.next(); res.headers.set('X-Custom', 'value'); return res; }`。middleware 在 Edge runtime 运行，`crypto.randomUUID()` 可用。注意：middleware 会让匹配的路由变成动态渲染。来源：https://nextjs.org/docs/15/app/api-reference/file-conventions/middleware
  12. **middleware matcher 配置**：在 middleware.ts 里 `export const config = { matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'] }` 排除静态资源和 API 路由，避免不必要的 middleware 执行。来源：https://nextjs.org/docs/15/app/api-reference/file-conventions/middleware
  13. **避免设置过大的响应头**：Next.js 官方警告：避免在 middleware 里设置过大的 header，可能导致 `431 Request Header Fields Too Large` 错误（取决于后端 web 服务器配置）。CSP 字符串很长，注意控制长度。来源：https://nextjs.org/docs/15/app/api-reference/file-conventions/middleware
  14. **Vercel 平台自动加的安全头**：Vercel 对所有部署自动加 `X-DNS-Prefetch-Control: on`、`X-Frame-Options: SAMEORIGIN`（部分情况）。但不要依赖平台默认——在 next.config.mjs 里显式声明所有需要的头，确保跨平台一致。来源：Vercel docs + Next.js production checklist
  15. **用 securityheaders.com 或 Mozilla Observatory 验证**：部署后用 https://securityheaders.com/ 扫描，目标 A 级以上。检查 6 个必备头是否都存在且值正确。CSP 用 Chrome DevTools → Network → 响应头检查，控制台会报 CSP 违规（`Refused to load ... because it violates the following Content Security Policy directive`）。来源：Mozilla Observatory + securityheaders.com

  **落地计划**：
  - 下次迭代在 next.config.mjs 加 6 个安全响应头（HSTS/nosniff/X-Frame-Options/Referrer-Policy/Permissions-Policy）→ 任务 P1-SEC-HEADERS-001
  - AdSense 接入后，在 CSP 里放行 Google 广告域名（pagead2.googlesyndication.com 等）→ 任务 P1-SEC-CSP-ADSENSE-001
  - 部署后用 securityheaders.com 扫描验证 A 级 → 任务 P2-SEC-AUDIT-001


- [2026-09-21] **BreadcrumbList + FAQPage 结构化数据 2026 最佳实践（Google 官方 docs，15 个权威知识点）**
  1. **BreadcrumbList 必填结构**：`@type: BreadcrumbList` + `itemListElement`（ListItem 数组），至少 2 个 ListItem。每个 ListItem 必须有 `position`（整数，从 1 开始）、`name`（可见名称文本）、`item`（URL）。来源：https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
  2. **ListItem 用扁平数组不要嵌套**：Google 推荐扁平 itemListElement，每个元素直接是 `{@type: ListItem, position, name, item}`。不要用 item 里再嵌 @type 的旧写法。来源：Google breadcrumb docs
  3. **item 必须是完整 URL**：`item: "https://www.aitoolcrux.com/tools/midjourney"`，不能是相对路径 `/tools/midjourney`。本站 BreadcrumbSchema 已用模板拼接完整 URL（正确）。来源：Google breadcrumb docs
  4. **position 从 1 开始递增**：position 1 = 首页（根），position 2 = 二级分类，position 3 = 当前页。不能跳号。本站用 `index + 1`（正确）。来源：Google breadcrumb docs
  5. **面包屑必须和页面可见面包屑一致**：JSON-LD 里的 name/URL 必须和页面上用户看到的面包屑导航一一对应。Google 会对比，不一致可能不展示。来源：Google breadcrumb docs
  6. **面包屑替代 URL 路径展示**：Google 搜索结果里显示面包屑（如 Home > AI Tools > Midjourney）替代丑陋的 URL 路径，提升 CTR。这是 BreadcrumbList 的核心价值。来源：Google breadcrumb docs
  7. **data-vocabulary.org 已废弃**：旧的 data-vocabulary.org Breadcrumb schema 不再被支持，必须用 schema.org BreadcrumbList。来源：Google breadcrumb docs
  8. **FAQPage 必填结构**：`@type: FAQPage` + `mainEntity`（Question 数组）。每个 Question 必须有 `name`（问题全文）和 `acceptedAnswer`（Answer 对象）。Answer 必须有 `@type: Answer` 和 `text`（答案全文）。来源：https://developers.google.com/search/docs/appearance/structured-data/faqpage
  9. **每个问题只能有一个 acceptedAnswer**：FAQPage 用 acceptedAnswer（唯一正确答案），不是 suggestedAnswer。多个建议答案用 QAPage（论坛场景），不要混淆。本站 FAQSchema 已用 acceptedAnswer（正确）。来源：Google faqpage docs
  10. **FAQ 内容必须和页面可见 FAQ 一致**：JSON-LD 里的 question/answer 必须和页面上用户看到的 FAQ 板块文字完全匹配。不能在 schema 里写页面上没有的内容。来源：Google faqpage docs
  11. **FAQPage 不能用于 UGC/广告**：Google 明确禁止：(a) 用户论坛/问答社区内容（用 QAPage）；(b) 广告/促销内容；(c) 导航元素伪装成 FAQ。本站 FAQ 是编辑撰写的（正确）。来源：Google faqpage + content guidelines
  12. **Google 2023-08 起 FAQ 富摘要仅限权威站**：Google 从 2023 年 8 月起大幅限制 FAQ 富摘要展示——只有 well-known、权威政府/医疗网站才在搜索结果展示 FAQ 手风琴。普通站点 FAQPage schema 不再出富摘要，但 (a) 仍不有害；(b) 帮助 AI 搜索（ChatGPT/Perplexity/Google AI Overview）提取答案；(c) 帮助 Google 理解页面内容结构。来源：Google Search Central blog 2023-08
  13. **FAQPage 对 AI 搜索（GEO）仍有价值**：虽然传统富摘要没了，但 FAQPage 是 Google AI Overview 和 Perplexity 提取"直接答案"的高优先级信号。答案 text 建议 40-120 词，第一句直接回答。来源：https://aiseojournal.net/schema-markup-complete-structured-data-guide-for-ai-search/
  14. **FAQPage vs QAPage 区别**：FAQPage = 编辑撰写的固定问答（我们的场景）；QAPage = 论坛/社区用户提问、多用户回答（每个问题可有多个 suggestedAnswer）。不要混用。来源：Google qapage docs
  15. **用 Rich Results Test 验证**：部署后用 Google Rich Results Test（https://search.google.com/test/rich-results）检查 Breadcrumb 和 FAQ schema 是否有错误。GSC 会在"富搜索结果"报告里展示 Breadcrumb 的展示次数。来源：Google breadcrumb/faqpage docs

  **落地计划**：
  - 下次迭代检查所有工具页/blog 页是否都正确引入了 BreadcrumbSchema（确保 position 从 1 开始、item 是完整 URL）→ 任务 P2-SCHEMA-BREADCRUMB-001
  - 检查 FAQSchema 的 answer text 是否都在 40-120 词、第一句直接回答（优化 AI 搜索提取率）→ 任务 P2-SCHEMA-FAQ-001
  - 用 Rich Results Test 批量验证 5 个工具页 + 3 个 blog 页的 Breadcrumb 和 FAQ schema 无错误 → 任务 P2-SCHEMA-VALIDATE-001
  - 确认本站 FAQ 是编辑撰写（非 UGC），不会触发 Google FAQPage 滥用政策 → 已确认，无需改动


- [2026-09-21] **Next.js Metadata API：Canonical / Open Graph / Robots / Sitemap 文件约定 + Google canonical 最佳实践（15 个权威知识点）**
  1. **Metadata 两层定义**：(1) Config-based：layout.tsx/page.tsx 里 `export const metadata: Metadata` 或 `generateMetadata()`；(2) File-based：app/opengraph-image.tsx、app/robots.ts、app/sitemap.ts、app/icon.tsx 等文件约定。来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata
  2. **Metadata 合并规则**：同一路由多个 segment 的 metadata 浅合并；嵌套字段（openGraph、robots）在最后定义的 segment 覆盖前面的，不是深合并。所以根 layout 设的 og 默认值会被子页面覆盖。来源：metadata docs
  3. **canonical 用 alternates.canonical**：`alternates: { canonical: '/tools/midjourney' }` 生成 `<link rel="canonical">`；必须用绝对 URL（含 https://www.aitoolcrux.com），Google 官方要求。来源：https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
  4. **自引用 canonical**：每页 canonical 指向自己（self-referencing），这是标准做法；即使是唯一页面也要加，防止参数化 URL 被当成不同页。来源：Semrush canonical guide + Google docs
  5. **Google canonical 信号强弱**：301 重定向 = 强信号；rel=canonical link = 强信号；sitemap 包含 = 弱信号；组合使用效果最好。Google 可能忽略你指定的 canonical 选它认为更好的（URL Inspection 可查 Google 选了哪个）。来源：https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting
  6. **参数化 URL canonical**：`?ref=xxx`、`?utm_source=xxx` 等带参数的 URL，canonical 指向干净 URL（无参数版本）。来源：Google consolidate-duplicate-urls
  7. **robots metadata 对象**：`robots: { index: true, follow: true, googleBot: { 'max-image-preview': 'large', 'max-snippet': -1, 'max-video-preview': -1 } }` 控制索引指令。noindex 页用这个，不要用 robots.txt disallow（disallow 会让 Google 看不到 noindex meta）。来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata
  8. **app/robots.ts 文件约定**：`export default function robots(): MetadataRoute.Robots { return { rules: [...], sitemap: 'https://www.aitoolcrux.com/sitemap.xml', host: '...' } }`。可按 userAgent 分组（如 GPTBot/PerplexityBot 单独 allow）。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots
  9. **app/sitemap.ts 文件约定**：`export default function sitemap(): MetadataRoute.Sitemap { return [{ url, lastModified, changeFrequency, priority }] }`。可动态生成多 sitemap（按 tools/blog 分组），支持返回数组里嵌套 sitemap index。来源：Next.js metadata docs
  10. **openGraph 必须绝对 URL**：`openGraph: { url: 'https://...', images: [{ url: 'https://.../og.png', width: 1200, height: 630 }] }`。OG image 尺寸 1200x630 是 Facebook/Twitter 推荐；Next.js opengraph-image.tsx 可动态生成 OG 图（用 ImageResponse）。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image
  11. **twitter card 类型**：`twitter: { card: 'summary_large_image', title, description, images: [...] }`。summary_large_image 配大图，summary 配小图。来源：Next.js metadata docs
  12. **title 模板**：根 layout 设 `title: { template: '%s | AIToolCrux', default: 'AIToolCrux — ...' }`。子页面 title 用字符串填进 %s；不设 title 的页面用 default。来源：metadata docs
  13. **forbidden() 自动 noindex**：Next.js `forbidden()` 函数会自动注入 `<meta name="robots" content="noindex">`，不需要手动加。来源：https://nextjs.org/docs/app/api-reference/functions/forbidden
  14. **OG image 动态生成**：`opengraph-image.tsx` 里用 `ImageResponse`（next/og）+ JSX 生成图，build 时静态生成或 request 时动态。可按 tool slug 生成个性化 OG 图。来源：Next.js opengraph-image docs
  15. **GSC canonical 排查**：GSC 报 "Duplicate without user-selected canonical" 时，用 URL Inspection 看 Google 选了哪个 canonical；常见原因：(a) 缺 canonical link；(b) canonical 相对 URL；(c) www/non-www、http/https 版本不一致；(d) sitemap 和 canonical 指向不同版本。来源：https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting

  **落地计划**：
  - 下次迭代检查所有工具页/blog 页的 `alternates.canonical` 是否都用了绝对 URL（现在可能是相对路径）→ 任务 P1-SEO-CANON-001
  - 检查 sitemap.ts 是否给每个 URL 带了 lastModified（现在可能没带，影响 GSC 新鲜度判断）→ 任务 P2-SEO-SITEMAP-001
  - 检查根 layout 的 robots metadata 是否设了 googleBot.max-image-preview=large（影响 Google 图片富摘要）→ 任务 P2-SEO-ROBOTS-001
  - 考虑给工具页加动态 opengraph-image.tsx（按 tool slug 生成个性化 OG 图，提升社交分享 CTR）→ GROWTH-OG-IMAGE-001


- [2026-09-21] **Next.js 缓存体系（Data Cache / Full Route Cache / Router Cache / React Cache / PPR / revalidateTag / unstable_cache / use cache，15 个权威知识点）**
  1. **五层缓存模型**：(1) Request Memoization（React.cache，同请求内去重）；(2) Data Cache（fetch/unstable_cache 跨请求持久）；(3) Full Route Cache（build 时静态页 HTML）；(4) Router Cache（浏览器端 RSC payload，30s 默认）；(5) PPR 静态 shell。来源：https://nextjs.org/docs/app/guides/caching
  2. **fetch 默认行为**：App Router 里 fetch 默认被 Data Cache 缓存（永久），除非用 `next: { revalidate: 0 }` 或 `cache: 'no-store'`。来源：https://nextjs.org/docs/app/api-reference/functions/fetch
  3. **next.revalidate 三值**：`false`=永久缓存；`0`=每次请求重新 fetch（动态）；`number`=秒数，ISR 周期。来源：fetch docs
  4. **revalidateTag**：给 fetch 打 `next: { tags: ['tools'] }`，之后 `revalidateTag('tools')` 立即失效所有带这个 tag 的缓存。适合后台改了工具数据后刷新。来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration
  5. **revalidatePath**：按路径失效，`revalidatePath('/tools/llama')`；适合改了某页内容。在 Server Action 或 Route Handler 里调。来源：https://nextjs.org/docs/app/api-reference/functions/revalidatePath
  6. **revalidateTag vs revalidatePath**：tag 是后台刷新（stale-while-revalidate，用户先看旧的）；path 是立即失效（read-your-own-writes）。来源：https://nextjs.org/docs/app/getting-started/revalidating
  7. **unstable_cache**：不是 fetch 的异步函数（如 DB 查询）用 `unstable_cache(fn, keyParts, {tags, revalidate})` 包，结果进 Data Cache。来源：https://nextjs.org/docs/app/guides/caching-without-cache-components
  8. **Router Cache（浏览器端）**：客户端导航时缓存 RSC payload，默认 30s（静态页 5min）；`router.refresh()` 或 Server Action 里 `cookies.set/delete` 会清空。来源：caching docs
  9. **Full Route Cache**：build 时静态生成的 HTML/RSC payload 存在 CDN；用 `dynamic = 'force-dynamic'` 或 `cookies()/headers()` 会 opt-out。来源：caching docs
  10. **ISR 状态码**：`x-nextjs-cache` header 显示 HIT/STALE/MISS/REVALIDATED；STALE 表示先返回旧的后台刷新。来源：ISR docs
  11. **PPR（Partial Prerendering）**：Next.js 16 默认开启，静态 shell + 流式动态内容；不再需要 `experimental.ppr` flag。来源：https://nextjs.org/docs/app/guides/migrating-to-cache-components
  12. **`use cache` 指令**：Next.js 16 Cache Components，函数顶部 `"use cache"` 让结果进 React Cache；配合 `cacheLife('hours')` 设缓存时长。来源：https://nextjs.org/docs/app/getting-started/cache-components
  13. **cacheLife 三阶段**：`{stale, revalidate, expire}`——stale 后后台刷新、revalidate 后可 serve stale、expire 后必须重新生成。来源：https://nextjs.org/docs/15/app/api-reference/functions/cacheLife
  14. **cacheTag / updateTag**：Cache Components 里用 `cacheTag('tools')` 打标签，`updateTag('tools')` 后台刷新；替代旧的 revalidateTag。来源：Next.js glossary
  15. **`export const revalidate` vs `next.revalidate`**：route segment config `export const revalidate = 3600` 是整页 ISR；fetch 级 `next.revalidate` 是单请求缓存。Next.js 16 里 route config 迁到 `cacheLife()`。来源：cache-components docs
  **落地计划**：
  - **P2-PERF-ISR-001**：给 `app/tools/[slug]/page.tsx` 加 `export const revalidate = 86400`（24h ISR），工具数据改了用 `revalidateTag('tools')` 后台刷新；避免每次请求都读 JSON。
  - **P2-PERF-ROUTER-CACHE-001**：检查现有 fetch 调用，确认哪些该缓存（工具列表、文章列表）、哪些不该（实时数据）；用 `next: { revalidate: 86400 }` 显式标注。
  - **P2-SEO-PPR-001**：升级到 Next.js 16 后，PPR 默认开启，检查现有页面是否需要 `loading.tsx` 配合（上一轮已学）；移除 `experimental.ppr` flag。
  交叉验证：Next.js 官方 caching/ISR/fetch/revalidatePath/cacheLife/cache-components/migrating-to-cache-components docs 七方一致。


- [2026-09-21] **Next.js Streaming + Suspense + loading/error/not-found 文件约定（15 个权威知识点）**
  1. **Streaming 两种方式**：(a) 文件级——放 `loading.tsx` 自动包整个 segment 为 Suspense；(b) 组件级——在 page 里手动 `<Suspense fallback={...}>` 包异步组件。来源：https://nextjs.org/docs/app/getting-started/fetching-data
  2. **loading.tsx 本质**：Next.js 自动把整个 segment 包成 `<Suspense>`，fallback 作为静态 shell 先发给浏览器，数据到了再替换。来源：https://nextjs.org/docs/app/api-reference/file-conventions/loading
  3. **loading.tsx 是 client component**：必须加 `"use client"`，因为它要在浏览器端接收 streaming 数据并替换。来源：loading docs
  4. **流式响应的 HTTP 状态码坑**：一旦 Suspense fallback 渲染，服务器必须先 commit `200 OK` 开始发 HTML 流；之后 mid-stream 调 `notFound()` 无法把状态改成 404，只能替换内容。来源：https://nextjs.org/docs/app/guides/streaming
  5. **not-found.tsx 状态码**：非流式响应返回 `404`；流式响应返回 `200`（因为 shell 已经发了）。SEO 上要 404 就别在流式组件里 notFound，要在数据函数里提前判断。来源：https://nextjs.org/docs/app/api-reference/file-conventions/not-found
  6. **notFound() 最佳位置**：在被 `<Suspense>` 包裹的数据访问函数里调，不要在 page 顶层阻塞整个路由；这样 shell 还能显示。来源：https://nextjs.org/docs/app/api-reference/functions/not-found
  7. **error.tsx 错误边界**：放 segment 目录下，必须 `"use client"`，接收 `{error, reset}` props；`reset()` 重新渲染该 segment。来源：https://nextjs.org/docs/app/api-reference/file-conventions/error
  8. **error.tsx 不捕获 root layout 错误**：root layout 抛错要用 `app/global-error.tsx`，且 global-error 必须自己包含 `<html>` 和 `<body>` 标签（因为它替换了 root layout）。来源：error docs
  9. **error.tsx 不捕获 Server Component 抛出的所有错误**：它只捕获 client-side 渲染错误和 server component 渲染时的错误；构建期错误不捕获。来源：Next.js error-handling docs
  10. **`"use cache"` vs Suspense**：需要每次请求新鲜数据的组件不要用 `"use cache"`，要包 `<Suspense>` + fallback；fallback 随 shell 发，异步工作在请求时跑。来源：https://nextjs.org/docs/app/getting-started/caching
  11. **`instant = false` 阻塞路由**：page/layout 里 `export const instant = false` 允许阻塞式渲染（等数据到了再发 HTML），适合 SEO 关键页面。来源：https://nextjs.org/docs/messages/blocking-prerender-dynamic
  12. **Next.js 16.2 reset() 增强**：旧版 `reset()` 只清错误状态重渲染 children；新版 `unstable_retry()` 会调 `router.refresh()` 重新跑 RSC 数据请求。来源：https://nextjs.org/blog/next-16-2
  13. **loading.tsx 嵌套**：子路由的 loading.tsx 只覆盖子 segment，父 segment 的内容（如 layout、导航）保持可见——这是 streaming 的核心 UX 优势。来源：Next.js streaming guide
  14. **Bots/Crawlers 行为**：Next.js 文档明确说 streaming 对 SEO 友好，爬虫能拿到完整 HTML（RSC payload 在 stream 里）；但要 404 状态码必须非流式。来源：fetching-data docs
  15. **静态 shell + 流式数据**：loading.tsx 的 fallback 会被静态预渲染成 shell，这就是为什么用户立刻看到骨架屏而不是白屏——这是 LCP 优化的关键。来源：Next.js streaming guide
  **落地计划**：
  - **P2-PERF-LOADING-001**：给 `app/tools/[slug]/` 和 `app/blog/[slug]/` 加 `loading.tsx`（骨架屏），提升 LCP 感知；给 `app/tools/[slug]/` 加 `error.tsx`（工具不存在时友好提示）。
  - **P2-SEO-NOTFOUND-001**：检查现有 notFound() 调用位置——如果在流式组件里，改成在数据函数里提前判断，确保不存在的工具页返回真正的 404 状态码（不是 200）。
  - **P2-PERF-INSTANT-001**：对 SEO 关键页面（首页、工具列表页）考虑 `export const instant = false` 阻塞渲染，确保爬虫拿到完整 HTML 和正确状态码。
  交叉验证：Next.js 官方 loading/error/not-found/streaming/caching docs + Next.js 16.2 blog + Next.js Learn streaming tutorial 五方一致。


- [2026-09-21] **Next.js Metadata 文件约定（opengraph-image / sitemap.ts / robots.ts / manifest.ts / icon.ts，15 个权威知识点）**
  1. **文件约定核心思想**：在 app 目录里放 `opengraph-image.tsx`、`sitemap.ts`、`robots.ts`、`manifest.ts`、`icon.ts`，Next.js 自动生成对应 meta 标签/路由，不用手写 Route Handler。来源：https://nextjs.org/docs/app/getting-started/project-structure
  2. **opengraph-image.tsx 用法**：`export default function Image()` 返回 `new ImageResponse(<div>...</div>)`，JSX+CSS 渲染 OG 图；放在哪个 segment 就给哪个 segment 加 og:image。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image
  3. **ImageResponse 来源**：`import { ImageResponse } from 'next/og'`（不是 next/server）；基于 Satori，把 JSX 转 PNG。来源：https://nextjs.org/docs/app/api-reference/functions/image-response
  4. **静态 vs 动态**：不依赖 request-time API 时 build 时 SSG 成静态 PNG；用 cookies/headers/searchParams 时变成动态路由。我们要 SSG，就别用这些。来源：opengraph-image docs
  5. **bundle 大小限制 500KB**：JSX+CSS+字体+图片总 bundle 必须 <500KB，超了 build 失败；图片用 readFile 读本地文件 base64 注入。来源：https://nextjs.org/docs/app/api-reference/functions/image-response
  6. **字体只支持 ttf/otf/woff**：不支持 woff2/ttc；用 ttf/otf 最快。OG 图里别用系统字体，要 readFile 读字体文件传 `fonts` 参数。来源：同上
  7. **文件大小限制**：静态图片文件 opengraph-image ≤8MB，twitter-image ≤5MB，超了 build 失败。来源：opengraph-image docs
  8. **sitemap.ts**：`export default function sitemap(): MetadataRoute.Sitemap { return [{url, lastModified, changeFrequency, priority}] }`；自动输出 `/sitemap.xml`；默认缓存，除非用 request-time API。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
  9. **sitemap.ts 动态分段**：可以在子目录放 `app/tools/[slug]/sitemap.ts` 生成子 sitemap，Next.js 自动在根 sitemap 里列 `<sitemap>` 索引。适合我们 533 工具页拆 sitemap。来源：同上
  10. **robots.ts**：`export default function robots(): MetadataRoute.Robots { return { rules: {...}, sitemap: '...', host: '...' } }`；自动输出 `/robots.txt`。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots
  11. **manifest.ts**：`export default function manifest(): MetadataRoute.Manifest { return { name, short_name, icons, theme_color, display } }`；自动输出 `/manifest.webmanifest`，PWA 用。来源：Next.js docs
  12. **icon.ts / apple-icon.ts**：放 `app/icon.ts` 自动生成 favicon，`app/apple-icon.ts` 生成 iOS 主屏图标；不用在 metadata 里手动写 icons。来源：project-structure docs
  13. **generateImageMetadata**：一个 segment 要多张 OG 图时用，返回数组 `[{id, alt, size, contentType}]`，default function 接收 `{params, id}`。Next.js 16 里 params 和 id 都是 Promise。来源：https://nextjs.org/docs/app/guides/upgrading/version-16
  14. **和 metadata.openGraph.images 的关系**：文件约定优先级高于 metadata 里写的 openGraph.images；用了 opengraph-image.tsx 就可以删掉 metadata 里的 openGraph.images 字段。来源：Next.js metadata docs
  15. **Vercel 上运行时**：app router + Node runtime 或 Edge runtime 都支持 ImageResponse；pages router 只支持 Edge runtime。我们是 app router SSG，build 时生成，零运行时成本。来源：https://vercel.com/docs/og-image-generation
  **落地计划**：
  - **P2-PERF-OG-IMAGE-001**（已在 state.json）：把 `app/tools/[slug]/opengraph-image.tsx` 新建，用 ImageResponse 渲染工具名+评分+logo，替换现在 metadata 里写的 `/api/og?title=...`（那个是运行时重定向，慢）。注意 bundle <500KB、字体用 ttf、别用 request-time API 保持 SSG。
  - **P2-SEO-SITEMAP-SPLIT-001**：把现在的单 sitemap.ts 拆成根 sitemap + `app/tools/sitemap.ts` + `app/blog/sitemap.ts`，每个 <50k URL，避免单 sitemap 过大。
  - **P2-SEO-ROBOTS-001**：把现在的 public/robots.txt 迁成 app/robots.ts，动态读站点 URL，避免硬编码。
  交叉验证：Next.js 官方 opengraph-image/sitemap/robots/image-response docs + Vercel OG Image Generation docs + Next.js 16 upgrade guide 四方一致。


- [2026-09-21] **GSC Search Analytics API 完整体系（查询参数/维度/配额/分页，15 个权威知识点）**
  1. **端点**：`POST https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query`，OAuth2 或 Service Account 鉴权。来源：https://developers.google.com/webmaster-tools/v1/searchanalytics/query
  2. **必需字段**：`startDate` / `endDate`（YYYY-MM-DD，PST 时区），范围最长 16 个月（数据保留窗口）。来源：https://searchconsole.googleapis.com/$discovery/rest?version=v1
  3. **可用 dimensions**：`date`、`query`、`page`、`country`、`device`、`searchAppearance`、`hour`。多维度组合时按顺序 group by。来源：https://developers.google.com/webmaster-tools/v1/searchanalytics/
  4. **指标字段**：每行返回 `clicks`、`impressions`、`ctr`、`position`；按 clicks 降序，相同 clicks 任意排序。来源：同上
  5. **rowLimit**：默认 1000，最大 25,000；用 `startRow` 分页（默认 0）。来源：https://developers.google.cn/webmaster-tools/v1/searchanalytics/query?hl=zh-cn
  6. **数据上限**：每天每个 searchType 最多返回 50,000 行（按 clicks 排序）；查不到就缩小日期范围或加 filter。来源：https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data
  7. **dimensionFilterGroups**：结构是 `[{groupType: "and"|"or", filters: [{dimension, operator, expression}]}]`；跨 group 是 AND，group 内 filters 按 groupType。来源：https://developers.google.com/webmaster-tools/v1/searchanalytics/query
  8. **filter operators**：`equals`、`notEquals`、`contains`、`notContains`、`includingRegex`、`excludingRegex`。来源：同上
  9. **searchType**：`web`（默认）、`image`、`video`、`news`、`discover`、`googleNews`；不同类型数据分开查。来源：https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data
  10. **aggregationType**：`auto`（默认）、`byPage`、`byProperty`；查 URL 级数据必须 `byPage`。来源：同上
  11. **配额**：每 site 1,200 QPM，每 user 1,200 QPM，每 project 30M QPD / 40k QPM。来源：https://developers.google.com/webmaster-tools/limits
  12. **和 URL Inspection API 区别**：Search Analytics 是聚合历史数据（clicks/impressions/position）；URL Inspection 是单页实时索引状态（索引状态、最后抓取、结构化数据错误）。前者量大用于趋势，后者单页精确诊断（2000 QPD/property）。
  13. **Service Account 鉴权**：用 GCP 服务账号 JSON，把它的邮箱加到 GSC 用户列表（Resource Owners 级别），就不用 OAuth 交互登录——适合 GitHub Actions 定时跑。来源：Google 官方文档
  14. **常见坑**：(a) 数据有 2-3 天延迟，不要查昨天；(b) `page` 维度返回完整 URL 带协议和 trailing slash，做对比前要 normalize；(c) 隐私阈值：点击/曝光太少的 query/page 会被 Google 隐藏（不是 0）。来源：GSC docs
  15. **最佳查询模式**：每周一跑一次 `dimensions=["page"], rowLimit=25000, startDate=上周日, endDate=昨天`，落库对比周环比；每月跑一次 `dimensions=["query","page"]` 找高曝光低 CTR 的页面做 Title/meta 优化。
  **落地计划**：
  - 我们现有 GSC 数据抓取 workflow 已经在跑；下次迭代时按第 15 条把查询拆成「周趋势」+「月 query 报告」两个 job，输出到 `gsc-ga4-report/`。
  - 用第 10 条 `aggregationType: byPage` 确认现有脚本查 URL 级数据时没漏这个参数。
  - 用第 14 条 normalize URL（去 trailing slash），避免同一页面因 trailing slash 被拆成两行。
  交叉验证：Google 官方 searchanalytics query docs + discovery rest schema + how-tos/all-your-data + usage limits 四方一致。


- [2026-09-21] **Vercel Speed Insights 完整体系（RUM + RES + Intake API，15 个权威知识点）**
  1. **Vercel Speed Insights 是什么**：Vercel 官方 RUM 产品，自动采集真实用户的 LCP/INP/CLS，免费套餐 10,000 events/team/30 天。来源：https://vercel.com/docs/speed-insights + https://vercel.com/changelog/speed-insights-free-tier
  2. **和 web-vitals npm 包的区别**：`web-vitals`（Google）是你自己采集后上报到 GA4/自建后端；Speed Insights 是 Vercel 托管 dashboard，不用自己建表，但数据在 Vercel 控制台。我们已部署 web-vitals → GA4，两者可并存（一个看趋势一个看 Vercel 面板）。来源：https://vercel.com/docs/speed-insights
  3. **接入方式**：`npm i @vercel/speed-insights`，在 root layout 里 `<SpeedInsights />`（Next.js App Router 是 `import { SpeedInsights } from '@vercel/speed-insights/next'`）。来源：https://vercel.com/docs/speed-insights/quickstart
  4. **自动注入脚本**：包会往页面注入一个 `<script>`，浏览器原生 PerformanceObserver API 采集指标，上报到 `/_vercel/speed-insights/*` 第一方端点（不是第三方域名，不影响隐私/CLS）。来源：https://vercel.com/docs/speed-insights/quickstart
  5. **三个指标目标值**：LCP ≤ 2.5s、INP ≤ 200ms、CLS ≤ 0.1，和 Google Core Web Vitals 官方阈值一致。来源：https://vercel.com/docs/speed-insights/metrics
  6. **INP 语义**：用户交互到下一帧渲染完成的时间；用户离开页面时聚合所有交互取最坏值；bot 访问不算 INP（没交互）。来源：https://vercel.com/kb/guide/optimizing-core-web-vitals-in-2024
  7. **Real Experience Score (RES)**：Speed Insights 独有综合分，把 LCP/INP/CLS 按权重合成一个 0-100 的分数，dashboard 主视图直接看。来源：https://vercel.com/docs/speed-insights
  8. **分路由/分地区/分设备切片**：dashboard 可以按 URL 路径、Country、Device Type（mobile/desktop）拆分，直接定位哪个慢。来源：同上
  9. **Intake API**：如果你想自己把数据拉出来进数据仓库，`POST /_vercel/speed-insights/event`，需要 `process.env.VERCEL_ANALYTICS_ID`（build 时自动注入）。来源：https://vercel.com/docs/speed-insights/api
  10. **减少 events 用量**：可以用 `<SpeedInsights sampleRate={0.1} />` 采样率 10%，免费套餐 10k events 够用。来源：https://vercel.com/docs/speed-insights/managing-usage
  11. **和 Vercel Web Analytics 的区别**：Speed Insights 只看性能指标；Web Analytics 看访问量/来源/页面浏览。两个包独立，都装也不冲突。来源：https://vercel.com/docs/analytics/quickstart
  12. **本地开发不采**：`npm run dev` 时 Speed Insights 默认不上报（避免污染数据）；要测本地可以设 `DEBUG` 或手动 query param。来源：quickstart docs
  13. **SSG 静态站也能用**：我们是 Next.js SSG（Vercel 部署），Speed Insights 不依赖 Server Actions/动态路由，静态 HTML 一样注入 script 采集。来源：https://vercel.com/docs/frameworks/full-stack/nextjs
  14. **隐私合规**：第一方域名上报，cookie-free，不存 PII；GDPR/CCPA 不需要额外 consent banner（但要在隐私政策里写一句）。来源：https://examples.vercel.com/docs/speed-insights/privacy-policy
  15. **和 CrUX 的区别**：Chrome UX Report 是浏览器汇总的匿名数据，按 origin 聚合，粒度粗（28 天窗口）；Speed Insights 是你自己的真实访客，分页面/分地区，粒度细，能看到改造前后对比。来源：Vercel docs
  **落地计划**：
  - 下一轮 P1-PERF-IMG-001（工具页截图迁 next/image）上线后，在 root layout 加 `<SpeedInsights sampleRate={0.2} />`，跑一周看工具页 LCP 中位数变化，对比改造前后。
  - 如果免费 10k events 不够（533 工具页 × 日 UV），保持 20% 采样率即可，不升级付费。
  - 和现有 web-vitals → GA4 上报并存：GA4 看长期趋势，Vercel dashboard 看分路由切片定位慢页面。
  交叉验证：Vercel Speed Insights 官方 docs（overview/quickstart/metrics/api/privacy）+ free-tier changelog + web.dev CWV 阈值 三方一致。


- [2026-09-21] **Next.js Metadata API 深度体系（App Router，15 个权威知识点）**
  1. **root layout 必须设 `metadataBase`**：所有 OG image / canonical 用相对路径时，Next.js 用 `metadataBase` 拼成绝对 URL；不设会导致 OG 图 404。来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata
  2. **title template 继承**：root `title.template = '%s | AIToolCrux'`，子页面只写 `title: "Perplexity Review"`，自动拼成 `Perplexity Review | AIToolCrux`；想覆盖整段就用 `title.absolute`。来源：https://nextjs.org/learn/dashboard-app/adding-metadata
  3. **static vs dynamic**：build 时已知用 `export const metadata`；依赖 params/fetch 用 `export async function generateMetadata({ params })`。Next.js 15+ `params` 是 Promise，必须 `await`。来源：https://nextjs.org/docs/app/getting-started/metadata-and-og-images
  4. **`generateMetadata` 第二参数 `parent`**：可以 `const prev = await parent` 继承父级 OG images，避免重复定义。来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata
  5. **canonical 用 `alternates.canonical`**：不要手写 `<link rel="canonical">`；`alternates: { canonical: '/tools/perplexity' }` 自动输出绝对 URL（基于 metadataBase）。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata
  6. **noindex 用 `robots` 字段**：`robots: { index: false, follow: true }` 输出 `<meta name="robots" content="noindex,follow">`；不要用 `robots.txt` 禁爬（那是控制抓取，不是控制索引）。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots
  7. **OG image 两种方式**：(a) `openGraph.images: ['/og.png']` 静态图；(b) 文件约定 `app/tools/[slug]/opengraph-image.tsx` 用 `ImageResponse` 动态生成，build 时 SSG 成静态 PNG。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image
  8. **`generateImageMetadata`**：一个 opengraph-image.tsx 里 `export function generateImageMetadata()` 返回多张图（不同尺寸/语言），不用建多个文件。来源：同上
  9. **`viewport` 单独导出**：Next.js 14+ viewport/themeColor 从 metadata 拆出，用 `export const viewport = { themeColor: '#000' }`，不要塞 metadata 里。来源：https://nextjs.org/docs/app/api-reference/functions/generate-viewport
  10. **`blocking-prerender-metadata-runtime` 报错**：generateMetadata 里用了 `cookies()`/`headers()`/`searchParams` 等动态 API 又想 SSG，会报这个错；修法：要么改 static metadata，要么 `await connection()` 标 dynamic。来源：https://nextjs.org/docs/messages/blocking-prerender-metadata-runtime
  11. **vercel.app 预览域名要 noindex**：用 `X-Robots-Tag: noindex` header（在 vercel.json 或 middleware），避免预览域名和生产域名重复内容。来源：https://vercel.com/guides/avoid-duplicate-content-with-vercel-app-urls
  12. **JSON-LD 不要塞进 metadata**：metadata 只管 `<head>` 标准 meta；结构化数据用 `<script type="application/ld+json">` 直接在 page 里渲染（我们现在就是这么做的，正确）。来源：Next.js docs
  13. **`openGraph.type`**：文章页用 `type: 'article'`，工具页用 `type: 'website'`；Facebook/LinkedIn 解析靠这个。来源：Next.js metadata docs
  14. **`twitter.card`**：默认 `summary`；大图用 `summary_large_image`，配合 `twitter.images`。来源：同上
  15. **sitemap.ts 和 robots.ts 是文件约定**：`app/sitemap.ts` export default function 返回 `MetadataRoute.Sitemap`；`app/robots.ts` 返回 `MetadataRoute.Robots`。Next.js 自动生成 `/sitemap.xml` 和 `/robots.txt`，不要手写静态文件。来源：https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots
  **落地计划**：
  - 下一轮 P1-SCHEMA-DISCLOSURE 时，顺手检查 root `app/layout.tsx` 的 `metadataBase` 是否设成 `https://www.aitoolcrux.com`（没设的话 OG 图会坏）。
  - 下一轮给 `/blog/tag/*` 加 noindex 时，用 `robots: { index: false, follow: true }`（我们已经做了，确认写法和官方一致）。
  - 未来给工具详情页做动态 OG 图时，用 `app/tools/[slug]/opengraph-image.tsx` + `ImageResponse`，不要在 metadata 里手写 `/api/og?title=...`（那个是 client-side 重定向，SSG 不友好）。
  交叉验证：Next.js 官方 metadata docs + generate-metadata API ref + opengraph-image docs + Vercel duplicate-content guide + Next.js learn SEO 五方一致。




---

### [2026-09-22] 高星GitHub开源工具——前端安全扫描与依赖漏洞审计工具体系

**知识点1：Snyk——商业级开发者安全平台，SCA+SAST+容器+IaC全覆盖**
Snyk 是最主流的开发者安全平台，核心能力：SCA（软件成分分析，扫描依赖漏洞）、SAST（静态代码安全扫描）、容器扫描、IaC 扫描。最大亮点是一键升级 PR（自动将有漏洞的依赖升级到安全版本），IDE 插件实时提示。免费版有限制，付费版按团队规模计费。适合以开源依赖风险为主、需要自动化修复的团队。（来源：https://www.getastra.com/blog/security-audit/code-security-scan-tools + https://www.stackinsight.net/snyk-vs-semgrep-comparison/）

**知识点2：Trivy——开源全能漏洞扫描器，单CLI二进制覆盖SCA+容器+IaC+K8s+SBOM**
Trivy 是 Aqua Security 开源的漏洞扫描器（Apache 2.0），单二进制文件无需安装依赖。扫描目标包括：文件系统/依赖库（SCA）、容器镜像、IaC（Terraform/CloudFormation）、Kubernetes 集群、SBOM 生成。速度快，离线漏洞数据库，完全免费。2026年对比测试中 Trivy 检出 78 个 CVE vs Snyk 65 个。适合 CI/CD 流水线集成和自托管场景。（来源：https://shattered.io/de/trivy-vs-snyk-2026/ + https://dev.to/rahulxsingh/snyk-vs-trivy-commercial-security-platform-vs-open-source-scanner-2026-5e4b）

**知识点3：Semgrep——快速SAST静态代码分析，YAML自定义规则，社区版免费商用**
Semgrep 是安全聚焦的 SAST 工具，CI 中位扫描时间约 10 秒，支持 30+ 语言。核心优势：(a) 用 YAML 编写自定义规则，无需 AST 知识；(b) 误报率低，精确的模式匹配；(c) Community Edition 免费用于商业用途。2026年更新：Claude Code 和 Cursor Hooks 可直接从 Semgrep Registry 拉取自定义规则。Semgrep 侧重源码安全，依赖扫描能力有限（Snyk 在 SCA 方面更强）。（来源：https://www.getastra.com/blog/security-audit/best-ci-cd-security-tools + https://chatforest.com/reviews/code-security-mcp-servers/）

**知识点4：Dependabot——GitHub 原生依赖监控与自动更新，已配置在我们项目**
Dependabot 是 GitHub 原生功能，自动监控依赖并生成安全警报和版本更新 PR。我们项目已配置 .github/dependabot.yml（每周一检查 github-actions 更新）。关键限制：Dependabot 仅对使用语义化版本标签的 action 创建漏洞警报，不支持非 semver 引用。Dependabot security updates 自动为有漏洞的依赖创建升级 PR。对于 npm 依赖也可配置 version updates。（来源：https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions + https://docs.github.com/en/actions/reference/secure-use-reference）

**知识点5：npm audit——内置但误报率高，audit-ci 用于CI强制阻断**
`npm audit` 是 npm 内置的依赖漏洞扫描，但通常报告 50-300 个漏洞，其中绝大多数在传递依赖（transitive dependencies）中而非直接依赖。推荐策略：直接依赖 0 个 critical CVE，传递依赖 critical 每月审查。`audit-ci` 是 npm 包，可在 CI 中按严重级别（moderate/high/critical）阻断构建，比裸 npm audit 更实用。注意：npm audit 的漏洞数据来自 GitHub Advisory Database。（来源：https://ayinedjimi-consultants.fr/articles/trivy-scanner-vulnerabilites-cloud-native + https://www.aicodingguild.com/blog/free-security-scanning-tools-you-should-run-today）

**知识点6：Gitleaks / TruffleHog——Git 历史密钥扫描，防止硬编码凭证泄露**
Gitleaks（~15k★）和 TruffleHog（~15k★）是专门扫描 Git 仓库历史中硬编码密钥（API Key、Token、密码）的工具。Gitleaks 用 Go 编写，速度快，支持 pre-commit hook 和 CI 集成。TruffleHog 支持更多数据源（Git、S3、GCS、Docker 等）和密钥验证（主动测试密钥是否有效）。最佳实践：(a) pre-commit hook 本地拦截；(b) CI 扫描阻断；(c) GitHub Secret Scanning + Push Protection 服务端兜底。（来源：https://www.aicodingguild.com/blog/free-security-scanning-tools-you-should-run-today）

**知识点7：OWASP ZAP——运行时Web漏洞扫描（DAST），自动化渗透测试**
OWASP ZAP（Zed Attack Proxy，~14k★）是开源的 Web 应用安全扫描器，属于 DAST（动态应用安全测试），在运行时扫描漏洞（SQL注入、XSS、CSRF、路径遍历等）。支持自动化扫描（baseline scan 2分钟快速扫描、full scan 深度扫描）和 API 扫描。可集成到 CI/CD 中作为质量门。对于我们的静态站点，ZAP 主要扫描表单和 API 端点，价值相对有限，但对于有用户交互的页面仍有意义。（来源：https://www.aicodingguild.com/blog/free-security-scanning-tools-you-should-run-today）

**知识点8：eslint-plugin-security——ESLint 安全规则插件，实时检测XSS/注入**
eslint-plugin-security 是 ESLint 插件，在编码时实时检测 JavaScript/TypeScript 中的安全问题：XSS（innerHTML、document.write）、代码注入（eval、Function 构造函数）、不安全的正则表达式、硬编码密码等。优点：零额外工具，集成到现有 ESLint 流程，开发时即时反馈。缺点：规则覆盖有限，不能替代专业 SAST 工具。我们项目当前未配置此插件，可作为低成本安全加固第一步。（来源：https://www.aicodingguild.com/blog/free-security-scanning-tools-you-should-run-today）

**知识点9：OSV-Scanner——Google 开源漏洞数据库，多语言生态覆盖**
OSV-Scanner 是 Google 开源的漏洞扫描工具，基于 OSV.dev 数据库（聚合 GitHub Advisory、PyPI、npm、Go、Rust、Maven 等生态的漏洞数据）。特点：(a) 漏洞数据准确，每个漏洞有唯一 OSV ID；(b) 支持 Go、Python、Rust、JavaScript 等生态；(c) 开源免费，可集成到 CI。与 npm audit 相比，OSV 的数据质量更高、误报更少。（来源：https://devopsil.com/articles/2026-03-22-dependency-scanning-ci-pipeline）

**知识点10：GitHub Secret Scanning + Push Protection——服务端密钥泄露防护**
GitHub Secret Scanning 自动扫描仓库中的已知密钥模式（AWS、Google、GitHub、Slack 等 200+ 提供商），发现后通知提供商和仓库管理员。Push Protection 更进一步：在推送时实时阻断包含已知密钥的提交，从源头防止泄露。我们项目应确认这两项功能是否已启用（仓库 Settings → Code security → Secret scanning）。对于我们硬编码在 workflow 中的 GitHub PAT，应迁移到 GitHub Secrets 引用（对应 state.json 中 P3-CI-SECRETS-REFACTOR-001）。（来源：https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions）

**知识点11：CodeQL——GitHub 语义代码分析引擎，深度SAST**
CodeQL 是 GitHub 收购的语义代码分析引擎，将代码视为数据，用查询语言（QL）发现漏洞模式。支持 JavaScript/TypeScript、Python、Go、Java、C/C++、C#、Ruby 等语言。特点：(a) 语义级分析，能发现跨文件、跨函数的复杂漏洞链；(b) 内置大量安全查询（XSS、SQL注入、命令注入等）；(c) 开源仓库免费使用。对于我们的 Next.js 项目，CodeQL 可发现不安全的数据流（如用户输入直接传入危险 API）。可通过 GitHub Actions 的 github/codeql-action 集成。（来源：https://chatforest.com/reviews/code-security-mcp-servers/）

**知识点12：Dependency Review Action——GitHub 原生PR依赖审查，阻断有漏洞的依赖引入**
dependency-review-action 是 GitHub 官方 Action，在 PR 时扫描变更的依赖，如果引入了有已知漏洞的依赖则阻断 PR。与 Dependabot 的区别：Dependabot 监控已有依赖并生成警报/升级 PR，Dependency Review Action 在引入新依赖时实时阻断。配置简单：在 workflow 中添加 `uses: actions/dependency-review-action@v4`。对于我们频繁更新依赖的项目，这是低成本高价值的安全门。（来源：http://raw.githubusercontent.com/github/awesome-copilot/main/instructions/github-actions-ci-cd-best-practices.instructions.md）

**知识点13：Shift-Left Security——安全左移原则，SAST作为PR检查是最高ROI**
Shift-Left Security（安全左移）是指在开发流程早期（编码、PR 阶段）发现和修复安全问题，而不是等到部署后或生产环境。最高 ROI 的实践：(a) SAST 作为 PR 检查（Semgrep/CodeQL），在合并前阻断漏洞；(b) pre-commit hook 本地密钥扫描（Gitleaks）；(c) 依赖审查作为 PR 检查（Dependency Review Action）；(d) ESLint 安全插件实时反馈。研究表明，在编码阶段修复漏洞的成本是生产环境的 1/100。我们项目当前安全左移几乎为零，应优先添加 ESLint security plugin 和 Dependency Review Action。（来源：https://www.getastra.com/blog/security-audit/best-ci-cd-security-tools）

**知识点14：CI/CD 安全工具链七层模型——现代流水线必备安全控制**
现代 CI/CD 流水线应包含七层安全控制：(1) SCA（软件成分分析，扫描依赖漏洞）——Snyk/Trivy/OSV-Scanner；(2) SAST（静态应用安全测试）——Semgrep/CodeQL/SonarQube；(3) Secret Scanning（密钥扫描）——Gitleaks/GitHub Secret Scanning；(4) Container Scanning（容器扫描）——Trivy/Grype；(5) IaC Scanning（基础设施即代码扫描）——Trivy/Checkov；(6) DAST（动态应用安全测试）——OWASP ZAP；(7) SBOM（软件物料清单）——Trivy/CycloneDX。对于我们的纯前端静态站点，优先级：SCA > Secret Scanning > SAST > DAST，容器/IaC/SBOM 优先级低。（来源：https://www.getastra.com/blog/security-audit/best-ci-cd-security-tools + https://devopsil.com/articles/2026-03-22-dependency-scanning-ci-pipeline）

**知识点15：AIToolCrux 项目安全工具落地清单（按优先级）**
我们项目当前安全工具：Dependabot（已配置 github-actions 更新）、GitHub Secret Scanning（待确认是否启用）。缺失的高优先级安全措施：(a) P2-SEC-ESLINT-SECURITY-001：添加 eslint-plugin-security 到 ESLint 配置，零成本实时检测 XSS/注入；(b) P2-SEC-DEPENDENCY-REVIEW-001：添加 dependency-review-action 到 CI，PR 时阻断有漏洞的新依赖；(c) P2-SEC-GITLEAKS-001：添加 Gitleaks pre-commit hook 和 CI 扫描，防止硬编码密钥；(d) P3-SEC-TRIVY-001：添加 Trivy 到 CI 每周扫描依赖漏洞（替代 npm audit 的高误报）；(e) P3-CI-SECRETS-REFACTOR-001：将 workflow 中硬编码的 GitHub PAT 改为 ${{ secrets.GITHUB_PAT }} 引用。AdSense 接入后安全更重要（CSP 配置对应 P1-SEC-CSP-ADSENSE-001）。（来源：综合以上 GitHub Docs + Snyk + Trivy + Semgrep 官方文档）

**落地计划**：
- 知识点8（eslint-plugin-security）→ 下次迭代执行 P2-SEC-ESLINT-SECURITY-001，添加 eslint-plugin-security 到项目 ESLint 配置
- 知识点12（Dependency Review Action）→ 下次迭代执行 P2-SEC-DEPENDENCY-REVIEW-001，在 CI workflow 中添加 dependency-review-action
- 知识点6（Gitleaks）→ 下次迭代执行 P2-SEC-GITLEAKS-001，添加 Gitleaks pre-commit hook 和 CI 扫描
- 知识点10（GitHub Secret Scanning + Push Protection）→ 下次迭代确认仓库是否已启用，未启用则在 Settings 中开启
- 知识点2（Trivy）→ 下次迭代执行 P3-SEC-TRIVY-001，添加 Trivy 到 CI 每周扫描
## 待补充

- [2026-09-21] **Next.js 16 Middleware → Proxy 迁移 + Vercel Edge Runtime 完整体系（15 个权威知识点）**
  1. **Next.js 16 重大变更**：`middleware.ts` 已 deprecated，重命名为 `proxy.ts`；export 从 `middleware` 改为 `proxy`。来源：https://nextjs.org/docs/app/api-reference/file-conventions/proxy
  2. Next.js 16 的 proxy.ts **只跑 Node.js runtime**，不再跑 Edge runtime；Edge 行为迁移到 Routing Middleware（Vercel 平台层）。来源：https://vercel.com/docs/routing-middleware/getting-started
  3. Next.js 15.5+ middleware 支持 `config.runtime = 'nodejs'` 切换到 Node runtime；默认仍是 edge。来源：https://nextjs.org/docs/15/app/api-reference/file-conventions/middleware
  4. Edge Runtime 限制：不支持 Node.js `fs`/`net`/`child_process`；只支持 Web API（fetch/Request/Response）。来源：https://examples.vercel.com/docs/functions/runtimes/edge
  5. Middleware matcher 必须排除静态资源：`'/((?!_next/static|_next/image|favicon.ico).*)'`，否则每个图片请求都触发 Middleware，浪费冷启动。来源：https://vercel.com/docs/routing-middleware/api
  6. Middleware 超时：Edge runtime 默认 30s（Vercel Hobby）/ 更长在 Pro；超过直接 504。来源：Vercel docs
  7. Middleware 适合做：redirects、URL rewrites、cookie/header 注入、A/B 测试、Edge Config 动态重定向；不适合做：重计算、数据库查询、大对象处理。来源：Next.js middleware docs
  8. Edge Config：Vercel 边缘低延迟 KV 存储，`import { get } from '@vercel/edge-config'` 在 proxy 里读动态重定向规则，不用重新部署。来源：https://vercel.com/kb/guide/dynamic-redirects-with-edge-config-and-next-js-proxy
  9. Middleware Upgrade Guide：之前用 Middleware 转发 header 到外部 API，现在改用 Edge API Routes（`pages/api/proxy.ts` + `runtime: 'edge'`）。来源：https://nextjs.org/docs/messages/middleware-upgrade-guide
  10. CORS：在 Middleware 里读 `Origin` header 判断白名单，注入 `Access-Control-Allow-Origin`；不要在每个 Route Handler 重复写。来源：https://vercel.com/kb/guide/how-to-enable-cors
  11. Middleware 不能访问文件系统；要做 301 重定向表，用 Edge Config 或 DB，不要 `fs.readFileSync`。
  12. 对我们项目：5 个 blog tag 301 到 category 的重定向，如果未来频繁加，可以放 Edge Config；现在硬编码在 next.config.mjs redirects 即可（next.config redirects 在 Edge 层执行，零冷启动）。
  13. proxy.ts 在 Next.js 16 是 Node runtime，意味着可以用 Prisma/Redis 等 Node 库；但冷启动比 Edge 慢 100-200ms。来源：Next.js proxy docs
  14. 不要在 Middleware 里做 SEO 重定向（如 /old-slug → /new-slug）；这类静态重定向放 next.config.mjs redirects，Vercel 边缘直接 301，零函数调用成本。
  15. 调试 Middleware：在 Vercel Dashboard 的 Functions 日志里看；本地用 `next dev` 配合 `next/middleware` 的 console.log。
  **落地计划**：下一轮 Next.js 16 升级评估（P2-PERF-PPR-001）时，把现有 `middleware.ts`（如果有）迁移到 `proxy.ts`；5 个 blog tag 301 继续放 next.config.mjs redirects（不用 Edge Config，避免新增依赖）。交叉验证：Next.js proxy/middleware docs + Vercel Routing Middleware docs + middleware-upgrade-guide + Edge Runtime docs 四方一致。


## 待补充

- [2026-09-21] **GitHub Actions 自定义 Action 开发完整体系（Composite vs JavaScript vs Docker，15 个权威知识点）**
  1. 三种 Action 类型：Composite（YAML 串 step）、JavaScript（Node 脚本）、Docker（容器）。优先 Composite 因为无依赖、跨平台快。来源：https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions
  2. Action 必须在仓库 `.github/actions/<name>/action.yml`（或 action.yaml），不能放其他位置。来源：https://learn.microsoft.com/zh-cn/training/modules/create-custom-github-actions/create-custom-github-action
  3. action.yml 必填：name, description, runs.using（'composite' / 'node20' / 'docker'）。来源：metadata-syntax 文档
  4. Composite action 的 runs.using 是 'composite'，每个 step 用 `shell: bash`（Windows runner 必须显式声明 shell，否则默认 pwsh 语法不同）。来源：https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action
  5. Composite action 里 `$GITHUB_OUTPUT` 写输出：`echo "key=value" >> $GITHUB_OUTPUT`；读取用 `${{ steps.<id>.outputs.key }}`。来源：metadata-syntax 文档
  6. inputs 在 action.yml 里声明，用 `${{ inputs.<name> }}` 引用；required + default + description 三字段。来源：同上
  7. JavaScript action 用 `@actions/core` + `@actions/github` 工具包；官方模板 `actions/javascript-action` 和 `actions/typescript-action` 一键初始化（含 lint/test）。来源：https://docs.github.com/en/enterprise-server@3.9/actions/creating-actions/creating-a-javascript-action
  8. JavaScript action 必须 commit `node_modules/`（不能只 commit dist/，因为 runner 不跑 npm install）；或用 `@vercel/ncc` 打包成单文件 dist/index.js。来源：Microsoft Learn
  9. Composite action 不支持 `if: always()` 跨 step 状态判断；要在 job 层做。来源：GitHub composite action 文档
  10. action.yml 里 `branding.icon` + `branding.color` 可选，让 Action 在 Marketplace 有图标。来源：metadata-syntax 文档
  11. 复用方式：同仓库直接 `uses: ./.github/actions/my-action`；跨仓库 `uses: owner/repo/.github/actions/my-action@v1`（必须打 tag）。来源：GitHub composite action 文档
  12. pin SHA：生产 Action 必须 `uses: owner/repo/.github/actions/my-action@<full-sha>`，不能用 `@v1`，避免上游被篡改。来源：GitHub 官方 security hardening
  13. Composite action 不能在 step 之间共享 env 除了 `$GITHUB_ENV`；写 `echo "KEY=value" >> $GITHUB_ENV`。来源：GitHub metadata-syntax
  14. 调试：在 workflow 里 `ACTIONS_STEP_DEBUG=true` secret 开启 step 级 debug 日志。来源：GitHub Actions docs
  15. 不要在 Composite action 里硬编码 secret；通过 `${{ inputs.github-token }}` 或 `${{ secrets.GITHUB_TOKEN }}` 显式传入。来源：GitHub security hardening
  **落地计划**：下一轮把 `uptime-monitor.yml` 和 `index-monitor.yml` 里重复的"checkout + setup-node + npm ci"三步抽成 `.github/actions/setup-node/action.yml`（Composite），所有 workflow 复用；同时把 Action pin 到 full SHA（配合 P1-CI-PIN-001）。交叉验证：GitHub metadata-syntax + composite action tutorial + JavaScript action tutorial + Microsoft Learn 四方一致。


## 待补充

- [2026-09-21] **Next.js Server Actions + Route Handler 触发按需再验证完整体系（15 个权威知识点）**
  1. `revalidatePath('/path')` 在 Server Action 或 Route Handler 里调用，会同时失效 Data Cache 和 Full Route Cache。来源：https://nextjs.org/docs/app/guides/caching
  2. `revalidateTag('tag', 'max')` 是 SWR 语义：立即返回旧内容，后台刷新；Next.js 16 起第二个参数 cacheLife profile 必填。来源：https://nextjs.org/docs/app/guides/server-actions
  3. Route Handler 方式：`app/api/revalidate/route.ts` 写 `import { revalidatePath } from 'next/cache'`，外部脚本 POST 这个端点即可触发再验证。来源：https://nextjs.org/docs/app/api-reference/functions/revalidatePath
  4. 推荐用 secret token 保护 revalidate 端点：URL 带 `?secret=xxx`，环境变量存 token，不暴露。来源：Next.js revalidating guide
  5. `revalidatePath('/', 'layout')` 第二个参数 layout 会再验证该 layout 下所有子路由（适合改全局组件如 footer）。来源：Next.js revalidatePath API
  6. Server Action 必须 `'use server'` 声明；Route Handler 不需要。来源：https://nextjs.org/docs/app/guides/server-actions
  7. revalidatePath 后 `redirect()` 或 `revalidateTag` 后 `revalidatePath` 可以链式调用。
  8. 后台再验证失败不回滚：保留旧数据，不会让用户看到错误页。来源：https://nextjs.org/docs/app/getting-started/caching-and-revalidating
  9. 对 SSG 静态导出（output: 'export'）不支持 revalidatePath/revalidateTag；必须在 Vercel Node runtime 或 Edge runtime 才能用。我们项目是 Vercel SSG 但非 static export，支持。来源：https://nextjs.org/docs/app/guides/self-hosting
  10. 触发方式三选一：① Server Action（表单提交后自动）② Route Handler（外部脚本 POST）③ Webhook（CMS 更新）。我们用 ②。
  11. 不要在客户端组件直接 import 'next/cache'；revalidate 函数只能在 server 层调用。
  12. ISR 首次访问（deferred）慢 1-3 秒；revalidatePath 后下一个请求就是 deferred regeneration。来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration
  13. 对 533 工具页：改一个工具只需 `revalidatePath('/tools/' + slug)`，不用全量重建。
  14. 对博客列表：发新文章后 `revalidatePath('/blog')` 和 `revalidatePath('/blog/' + newSlug)`。
  15. 对 sitemap：sitemap.ts 本身也是缓存的；改了 URL 列表后要 `revalidatePath('/sitemap.xml', 'layout')`。
  **落地计划**：下一轮建 `app/api/revalidate/route.ts`，支持 POST `/api/revalidate?secret=xxx&path=/tools/perplexity`；数据脚本改 tools.json 后 curl 这个端点，替代每次全量 GitHub commit + Vercel 重建。同时给 sitemap.ts 改动后加 `revalidatePath('/sitemap.xml')`。交叉验证：Next.js revalidatePath API + caching guide + server-actions guide + self-hosting guide 四方一致。


## 待补充

- [2026-09-21] **Google Review Snippet / AggregateRating 2026 政策与 SoftwareApplication schema 完整体系（15 个权威知识点）**
  1. 2026-07-24 新增政策：禁止 fake reviews 和未披露的 incentivized reviews，违规会被 manual action 直接摘掉星级。来源：https://developers.google.com/search/docs/appearance/structured-data/review-snippet ；https://ppc.land/google-bans-undisclosed-incentivized-reviews-sites-face-manual-action/
  2. Review snippet 2026 仍被 Google 支持（GSC 六个活跃监控类型之一），不是已废弃 schema。来源：https://developers.google.com/search/docs/appearance/structured-data/review-snippet
  3. self-serving reviews 政策：被评 entity 在自己网站上评自己，不 eligible 星级（Organization/LocalBusiness 评自己不行）。来源：https://www.greadme.com/blog/schemas/what-is-review-schema-complete-guide
  4. SoftwareApplication 支持 aggregateRating 和 review，必须同时给 ratingValue 和 ratingCount。来源：https://developers.google.com/search/docs/appearance/structured-data/software-app
  5. 评分必须可见在页面上（marked up but not shown on page = 不 eligible）。来源：https://jsonschemaapp.com/blog/review-schema-google-star-ratings/
  6. ratingValue 必须在 bestRating 和 worstRating 之间；推荐 bestRating=10 worstRating=1 或 bestRating=5 worstRating=1。来源：Review snippet 文档
  7. 嵌套规则：不要同时在 itemReviewed.name 和父级 name 重复指向同一被评物（2026-08 新增 clarification）。来源：https://developers.google.com/search/updates?id=2
  8. 缺失 required properties = 不 eligible（completeness 原则）。来源：https://developers.google.com/search/docs/appearance/structured-data/sd-policies
  9. 导入 G2/Trustpilot 等第三方评分是合法的（user-sourced ratings），但必须标注来源。
  10. 单篇 review 必须有 review.author 和 review.reviewRating；aggregateRating 可省略单条 review 的 reviewRating 但必须有平均评分。来源：Review snippet 文档
  11. review 内容必须是真实用户/编辑测试结果，不能是 marketing copy；否则触发 manual action。
  12. 对 AI 工具站：我们的评分是编辑团队亲测评分，属于 editorial review，不是 fake；但必须：① 评分可见在页面上 ② 不要在 schema 里写 ratingCount=10000 这种编造数字 ③ bestRating/worstRating 显式声明。
  13. 联盟披露：我们全局 AffiliateDisclosure 条已经满足 "disclosed incentivized reviews" 的披露要求；但每个工具页 CTA 附近最好也有一句 "We may earn commission"（P1-SCHEMA-DISCLOSURE）。
  14. 2026 年 7 月 Google 移除了多种结构化数据富结果支持，但 Review snippet 保留；FAQPage 星标富结果 2023 年已下线，只保留 FAQPage 用于 AI/GEO。
  15. 验证工具：Google Rich Results Test（https://search.google.com/test/rich-results）必须对每个工具页跑一次，确认 aggregateRating 被识别。
  **落地计划**：下一轮 P0-SCHEMA-001b 执行：① 确认 app/tools/[slug]/page.tsx 里 aggregateRating 的 ratingCount 是真实数字（我们编辑团队评测数，不是爬来的假数据）② 显式写 bestRating=10 worstRating=1（P1-SCHEMA-002）③ 评分数字必须在页面上可见 ④ 每个工具页 CTA 附近加 "May earn commission" 小字（P1-SCHEMA-DISCLOSURE）⑤ 用 Rich Results Test 抽 5 个工具页验证。交叉验证：Google 官方 review-snippet + software-app + sd-policies + Google updates changelog 四方一致。


## 待补充

- [2026-09-21] **Next.js/Vercel CDN 缓存头 + ISR 按需再验证完整体系（15 个权威知识点）**
  1. 静态页（无 revalidate）：Next.js 自动发 `s-maxage=31536000`（一年），Vercel Edge 永久缓存。来源：https://nextjs.org/docs/app/guides/cdn-caching
  2. ISR 页（time-based）：自动发 `s-maxage={revalidate}, stale-while-revalidate={expire-revalidate}`；默认 expire=1 年。来源：同上
  3. `revalidateTag('tag', 'max')` 用 SWR 语义：立刻返回旧内容，后台刷新；适合博客/目录页这种可容忍短暂延迟的场景。来源：https://preview.nextjs.org/docs/app/getting-started/revalidating
  4. Next.js 16 起 `revalidateTag` 第二个参数**必填** cacheLife profile：'max' / 'hours' / 'days' 或自定义对象。来源：https://nextjs.org/blog/next-16
  5. `revalidatePath('/path')` 是硬再验证：下一个请求**等待**新内容生成（blocking），适合刚发布/删除内容时立刻生效。来源：https://nextjs.org/docs/app/building-your-application/caching
  6. `revalidateTag` vs `revalidatePath`：前者 SWR 不阻塞，后者 blocking；发布新文章用 revalidatePath，数据小更新用 revalidateTag。来源：https://preview.nextjs.org/docs/app/guides/migrating-to-cache-components
  7. fetch 层缓存：`fetch(url, { next: { revalidate: 60 } })` 控制 Data Cache  lifetime；`revalidate: false` = 永久缓存。来源：https://preview.nextjs.org/docs/app/api-reference/functions/fetch
  8. Vercel Edge Network 识别的 Cache-Control 指令：s-maxage / stale-while-revalidate / stale-if-error / proxy-revalidate；max-age 只控浏览器不控 CDN。来源：https://examples.vercel.com/docs/cdn-cache
  9. Cache Components（Next.js 15+ 稳定）：`<CacheComponents>` 包裹静态+动态混合；用 `cacheTag` 打标 + `updateTag` 在 Server Action 里即时失效。来源：https://nextjs.org/docs/app/getting-started/cache-components
  10. 后台再验证失败不回滚：如果后台 fetch 出错，Data Cache 保留旧数据，不会让用户看到错误页。来源：https://nextjs.org/docs/app/building-your-application/caching
  11. 全量 SSG 构建后 714 个页面都是 s-maxage=31536000；要改内容必须走 revalidateTag/revalidatePath，等 CDN 边缘刷新才生效（不是改完立刻全网生效）。来源：Next.js cdn-caching guide
  12. Vercel Image Optimization 缓存独立于页面缓存：图片 URL 变换后 CDN 单独缓存，页面改了图片 URL 自动出新缓存。来源：https://vercel.com/docs/image-optimization
  13. 自定义 Cache-Control：在 Route Handler 里直接 `Response.json(..., { headers: { 'Cache-Control': 's-maxage=60' }})` 覆盖默认。来源：Vercel CDN cache 文档
  14. ISR 首次访问（deferred）：构建时没生成的页面，第一个请求触发 on-demand regeneration，会慢 1-3 秒；后续命中缓存。这就是为什么 /tools/[slug] 偶尔慢。来源：https://nextjs.org/docs/app/guides/incremental-static-regeneration
  15. 对 533 工具页这种规模：建议给工具页加 `export const revalidate = 86400`（24h），比全量 SSG 永久缓存更安全；发布新工具时用 `revalidateTag('tools')` 后台刷新。来源：综合 Next.js ISR 指南
  **落地计划**：下一轮 P1-PERF-IMG-001 改 next/image 时，顺便给 /tools/[slug] 加 `export const revalidate = 86400`；数据脚本改 tools.json 后调用 `revalidateTag('tools')`（需要 API Route 或 Server Action 触发），不要每次都全量重新部署。交叉验证：Next.js 官方 cdn-caching + ISR + Next.js 16 blog + Vercel CDN cache 四方一致。


## 待补充

- [2026-09-21] **Google Search Console URL Inspection API 完整体系（15 个权威知识点）**
  1. 配额：每 property 2000 QPD / 600 QPM；每 Developer Console 项目 10M QPD / 15K QPM。来源：https://developers.google.com/webmaster-tools/limits
  2. 端点：POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect，body 必须含 inspectionUrl、siteUrl（与 GSC property 一致）、可选 languageCode。来源：https://developers.google.com/webmaster-tools/v1/api_reference_index
  3. 授权 scope：webmasters 或 webmasters.readonly；service account 必须在 GSC property 里被加为 User。来源：https://developers.google.cn/webmaster-tools/v1/urlInspection.index/inspect
  4. 响应核心字段 inspectionResult.indexStatusResult.verdict 枚举 PASS / FAIL / PARTIAL。来源：https://developers.google.com/search/blog/2022/01/url-inspection-api
  5. coverageState 是 Google 给出的精确原因：Indexed not submitted in sitemap / Excluded noindex / Duplicate without user-selected canonical / Crawled currently not indexed。按这个字段分组才知道该修什么。
  6. robotsTxtState ALLOWED/DISALLOWED；indexingState INDEXING_ALLOWED/BLOCKED。区分 robots 挡还是 meta noindex 挡。来源：https://developers.google.com/webmaster-tools/v1/urlInspection.index/UrlInspectionResult
  7. pageFetchState：SUCCESSFUL/NOT_FOUND/DENIED/INVALID_URL/BLOCKED_ROBOTSTXT/SOFT_404。
  8. lastCrawlTime：Google 上次抓取时间；>30 天没抓说明内链/sitemap 权重低。
  9. googleCanonical vs userCanonical：不一致就是 canonical 冲突。
  10. mobileUsabilityResult：text too small / clickable elements too close / content wider than screen。
  11. richResultsResult：结构化数据校验，对应富媒体报告；可批量验证 SoftwareApplication/FAQPage schema。
  12. inspectionResultLink：GSC UI 里的检视报告链接。
  13. 采样策略：2000 QPD 配额下只抽 50 个关键 URL（首页+10工具+10文章+10分类+20长尾），每周跑一次。
  14. 区分 URL Inspection API（读数据 2000 QPD）和 Indexing API（写/提交 URL 默认 200 QPD，仅 JobPosting/BroadcastEvent 合法）。来源：https://developers.google.com/search/apis/indexing-api/v3/quota-pricing
  15. site: 给总数，URL Inspection API 给单页精确原因；批量修 404/noindex/canonical 必须用后者。
  **落地计划**：下一轮 P1-INDEX-001 按本条 2/3/4/5/13 写 Python 脚本，service account 加到 GSC，POST inspect 50 个关键 URL，按 coverageState 分组输出 CSV；发现 Excluded noindex 的页面对照 /blog/tag/* 是否故意 noindex；Crawled currently not indexed 的页面补内链+IndexNow。交叉验证：Google 官方 blog + API limits + OpenAPI spec 三方一致。


## 待补充

- [2026-09-21] **Next.js / Vercel 图片优化完整体系（15 个权威知识点）**
  1. next/image 默认 quality=75（1-100 整数），越低体积越小但锐度下降；不要盲目设 100。来源：https://nextjs.org/docs/app/api-reference/components/image
  2. Next.js 16 起 `images.qualities` 默认从"全部允许"收紧为 `[75]`；要支持多质量需在 next.config 显式声明白名单。来源：https://preview.nextjs.org/docs/app/guides/upgrading/version-16
  3. Vercel Image Optimization 对变换后的图片做边缘缓存，同一 URL+尺寸+质量只付一次变换成本，后续请求命中 CDN。来源：https://examples.vercel.com/docs/image-optimization
  4. `formats` 默认 `['image/webp']`；再加 AVIF 会让每个图片产生两份变换+缓存条目，成本翻倍。成本优先时保持默认 WebP，不要盲目加 AVIF。来源：https://vercel.com/kb/guide/reduce-image-optimization-costs-on-vercel
  5. Vercel 源图最大 8192×8192 px；源格式仅支持 jpeg/png/webp/avif，其他格式会报错。来源：https://vercel.com/docs/image-optimization/limits-and-pricing
  6. `images.remotePatterns` 必须按 host 白名单配置，支持 protocol/hostname/port/pathname/search 五字段；漏配会直接报 next-image-unconfigured-host。来源：https://nextjs.org/docs/messages/next-image-unconfigured-host
  7. `sizes` prop 必须和真实 CSS 布局匹配——这是 #1 图片选错尺寸 bug；浏览器用 sizes × DPR 选 srcset 候选，不匹配会拉 4-6 倍大的图。来源：web.dev / https://sushi.dev/blog/building-responsive-images-the-complete-srcset-sizes-guide
  8. LCP 图片必须 `fetchPriority="high"` 且**绝对不能** loading="lazy"；lazy 会把 hero 排到 idle 队列，LCP 直接慢 20-30%。来源：web.dev / https://www.w3tweaks.com/html/responsive-images-modern-formats-avif-webp-picture-srcset-sizes
  9. 首屏以下图片用 `loading="lazy"`（next/image 默认），配合 width/height 或 aspect-ratio 盒子预留空间防 CLS。来源：https://nextjs.org/docs/app/getting-started/images
  10. 远程图片必须显式传 width/height（Next 构建期拿不到远程文件尺寸），可选 blurDataURL 做模糊占位。来源：https://nextjs.org/docs/app/getting-started/images
  11. AVIF 历史安全风险：2026-08 libheif RCE CVE，Vercel 曾临时关闭 AVIF 解码；新接入图片管线要关注 libvips/libheif 版本。来源：https://vercel.com/blog/reproducing-disclosing-and-fixing-the-libheif-vulnerability-with-hacktron-and-the-maintainers
  12. srcset+sizes 的浏览器选择算法：先用 sizes 规则算渲染宽度 W，乘 DPR 得需要像素 P，再从 srcset 选 ≥P 的最小候选。来源：https://renderlog.in/blog/srcset-sizes-responsive-images-explained
  13. next.config 的 `deviceSizes`/`imageSizes` 控制生成的断点档位；P1-PERF-IMG-002 计划把 deviceSizes 收到 [480,640,750,828,1080]，去掉 1920/2048/3840 等未用档位以减少变换缓存项。来源：https://nextjs.org/docs/app/api-reference/components/image
  14. SVG/图标类图片用 `unoptimized` prop 跳过 Vercel 图片 CPU 成本（SVG 本身已是矢量，不需要再变换）；这正是 P2-PERF-SVG-001 的依据。来源：https://vercel.com/kb/guide/reduce-image-optimization-costs-on-vercel
  15. LCP 图片按真实渲染尺寸压缩——一张 4K hero 渲染成 1280×720 就是浪费 90% 字节；WebP/AVIF quality 75 与人眼无差。来源：web.dev / https://hidekazu-konishi.com/entry/web_performance_checklist_core_web_vitals
  **落地计划**：下一轮 P1-PERF-IMG-001（工具详情页截图迁 next/image + sizes）按本条 7/8/9/10 执行——list 卡片用 `sizes='(max-width:768px) 100vw, 400px'`，detail hero 用 `sizes='(max-width:768px) 100vw, 800px'` + `fetchPriority="high"`，不 lazy；P1-PERF-IMG-002 同步把 deviceSizes 收窄；P2-PERF-SVG-001 给 SVG icon 加 unoptimized。交叉验证：Next.js 官方文档 + Vercel KB + web.dev 三方一致。


- [2026-09-18] **学到：content-visibility: auto (CSS Containment Module Level 2)** — web.dev/Chrome团队官方性能优化技巧。对首屏以下的内容（Alternatives、Similar Tools、Compare等section）设置`content-visibility: auto`，浏览器会跳过渲染离屏内容，直到用户滚动到附近。配合`contain-intrinsic-size: auto 400px`预留空间防止CLS。实测对长列表/长文章页面LCP改善20-50%。来源：https://web.dev/articles/content-visibility。已落地：在app/tools/[slug]/page.tsx的4个below-fold section上加了cv-auto类，globals.css定义了.cv-auto工具类。下次可用到：Blog文章页的FAQ和Related Posts section、Category页的ToolList后半部分。

- [2026-09-18] **踩坑：Vercel SSG部署700+页面需要3-5分钟才能全量上线** — 提交commit后90秒检查，cv-auto还没出现在HTML里；等了270秒（4.5分钟）才确认8个cv-auto类出现在/tools/chatgpt上。经验：SSG全量构建比ISR慢，验证线上时至少等3分钟再查，不要90秒就判定部署失败。
- [2026-09-18 14:41] Blog post dual H1 root cause: markdown content starts with '# Title' AND template renders its own <h1>. Fix: downgrade markdown # to ## in posts.json.
- [2026-09-18 14:41] Vercel SSG rebuild delay: after committing data files, live site may show old content for 3-5 minutes while 700+ pages rebuild.
- [2026-09-18 14:41] GitHub Trees API 5-step flow works reliably from China without git push.

- [2026-09-17] **Google Title 重写最新数据（Q1 2025 研究）**：John McAlpin 研究显示 Google 现在重写 76% 的 title（2023 年是 61%），平均删除 2.71 个词，只保留 35% 原内容。来源：Search Engine Land https://searchengineland.com/guide/title-tag ；Google 官方 https://developers.google.com/search/docs/appearance/title-link 。验证通过：两个独立来源一致。能否用上：能——我们刚把 7 篇高曝光文章 title 重写到 ≤60 字符，正是为了对抗 Google 截断/重写。
- [2026-09-17] **Title 分隔符选择：dash 优于 pipe**：Zyppy/Cyrus Shepard 研究，用 " - " 分隔被 Google 替换率仅 19.7%，用 " | " 被移除率 41%。来源：https://launchcodex.com/blog/seo-geo-ai/google-ai-headline-rewrites/ 引 Zyppy 研究。验证通过。能否用上：能——下次重写 title 时把 " | AIToolCrux" 改成 " - AIToolCrux"，降低被重写概率。
- [2026-09-17] **Title 最佳公式**：`[主关键词前置] - [独特价值/数字] [可选品牌]`，约 12 词 / 600 像素。数字和方括号标签（[2026]、[Tested]、[Free]）有真实价值时 Google 会保留；空洞的 [Best Ever] 会被忽略。来源：Search Engine Journal + onwardSEO + aitoolsguidebook.com。验证通过：3 个独立来源一致。能否用上：下一轮 P1-QA-001 给 46 篇文章补 Quick Answer 时，同步检查 title 是否符合此公式。
- [2026-09-17] **Vercel CDN 部署延迟再次确认**：GitHub 提交后等 80 秒验证，title 仍是旧的；等 140 秒（再 60 秒）后才全部生效。这是第二次确认此规律。下次提交后直接等 120 秒再验证，不要 80 秒就判失败。
- [2026-09-17] **P0-COMPARE-001 实际已完成**：/compare/page.tsx 第 268-277 行已有 Quick Answer 蓝色卡片，280-312 行已有 Key Takeaways 四宫格。教训：认领任务前先 Read 对应代码确认现状，不要凭 state.json 里 "pending" 状态就动手改，避免重复添加。
- [2026-09-17] **PowerShell Invoke-WebRequest 不自动跟随 308 重定向**：验证页面时如果 URL 末尾斜杠不一致可能踩坑。用 `-UseBasicParsing -TimeoutSec 20` 并加 `-Headers @{"Cache-Control"="no-cache"}` 可避免 CDN 缓存拿到旧 HTML。
- [2026-09-17] **批量改 posts.json 前必备份**：本轮备份到 `iteration_center/backup/posts_20260917_010634.json.bak`。7 篇文章 title/excerpt 一次性改完，脚本内置 assert 校验（title≤60、excerpt 120-165），改完回读验证才写盘。

- [2026-09-17] **Google Featured Snippets 官方规范（answer-first + 问题式H2）**：Google官方文档要求精选摘要页面"答案在第一句"（answer-first rule），用问题式H2标题（如"## Quick Answer"、"## What is X?"）帮助Google识别，FAQPage schema提升被选中概率。来源：Google官方 https://developers.google.com/search/docs/appearance/featured-snippets ；交叉验证 mlopez.ca 2025 指南。验证通过：两个独立来源一致。能否用上：能——本轮把4篇文章的"## TL;DR: The Short Version"改成"## Quick Answer"标准h2，正是为了让Google更容易提取精选摘要。
- [2026-09-17] **审计脚本误报教训**：本轮审计报告说12篇缺Quick Answer，实际其中4篇（note-taking/design/email/translation）用"## TL;DR: The Short Version"h2 + 内联"**Quick Answer:**"bold文字，内容存在但标题不标准。教训：批量扫描H2时，除了找标准标题，还要检查"TL;DR"、"Short Version"、"Bottom Line"等同义标题；改前先看内容确认是真缺还是只是标题不同。
- [2026-09-17] **web-vitals RUM监控部署完成**：创建components/analytics/WebVitalsReporter.tsx（'use client'组件），在useEffect中动态import web-vitals，调用onLCP/onINP/onCLS/onFCP/onTTFB，通过gtag上报到GA4作为non_interaction事件（避免污染跳出率），同时存localStorage供本地调试。在layout.tsx的</body>前加<WebVitalsReporter />。commit c8613756。教训：PowerShell的字符串.Replace()中反引号n(
)在双引号外会被当字面量写入文件，需要先.Replace('`n', "
")修复。验证：tsc 0错误，3页面全200。
- [2026-09-17] **web-vitals官方最佳实践（RUM）**：web-vitals库(web.dev官方)动态import仅~1KB gzipped，在Next.js App Router中用use client组件+useEffect加载不影响SSR。GA4事件名直接用LCP/INP/CLS，value参数：CLS乘1000取整，其他直接round。来源：https://web-vitals.dev/ + https://nextjs.org/docs/app/building-your-application/optimizing/analytics 。验证通过。能否用上：已用上。
- [2026-09-18] 博客文章content内嵌h1导致双H1：12篇AI生成文章content里含h1标签，博客模板line 345已有一个h1渲染标题。修复：正则h1->h2。教训：AI生成内容要检查HTML层级。
- [2026-09-18] 重复URL先验证重定向：chatgpt-vs-claude短URL已自动308重定向到长URL，无需加canonical。教训：发现重复URL先线上验证。
- [2026-09-18] generateMetadata description自动处理：>160截断加...，<120追加Expert analysis by AIToolCrux。来源：Next.js Metadata API官方文档。写excerpt直接120-160字符。
- [2026-09-18] **Next.js title.template最佳实践（官方）**：Next.js App Router支持根layout设置`title.template: '%s | AIToolCrux'`，子页面只需传`title: "Page Name"`，Next自动拼接品牌后缀。当前工具页手动拼接title字符串，未来可重构为title对象模式。来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata 。验证通过。
- [2026-09-18] **长工具名title截断教训**：工具页title原逻辑name截断35字符导致总长69字符。改为截断27字符后总长61字符。后缀固定约33字符，所以name阈值=60-33=27。教训：计算title长度要把后缀算进去。
- [2026-09-18] **P0-001重复Review JSON-LD已是历史问题**：线上验证工具页只有1个Review schema+1个FAQSchema+1个BreadcrumbSchema，无重复。教训：认领任务前先线上验证现状。

- [2026-09-18] **Next.js PPR/Cache Components官方动态**：Next.js 16移除experimental.ppr标志，PPR正式成为Cache Components默认渲染模型。每个路由拆成build时预渲染static shell（CDN直接服务，首屏秒开）+请求时streaming动态部分。来源：nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents + nextjs.org/docs/app/guides/migrating-to-cache-components（2026-09-07更新）。验证通过：两个官方文档一致。能否用上：短期不能（项目在Next.js 14.2.5且已转全SSG省Vercel额度）；长期升级Next.js 16时PPR可让静态壳+动态数据并存，不需要全量ISR。
- [2026-09-18] **2026 Core Web Vitals阈值确认**：LCP≤2.5s、INP≤200ms、CLS≤0.1，均按75分位（28天真实用户数据）评估。INP 2024年3月替代FID，测所有交互响应而非仅首次。来源：developers.google.com/search/docs/appearance/core-web-vitals（官方）+多个2026行业博客交叉验证。验证通过。能否用上：能——已有WebVitalsReporter上报GA4，下次性能优化按这三个阈值和75分位对标，不要只看中位数。
- [2026-09-18] **批量Title截断脚本要点**：文章title格式为`{main} | AIToolCrux`（后缀12字符），main部分阈值=48字符。截断时按冒号拆分head/tail，保留head完整，tail在budget内按词边界截断（rfind空格），不要硬切词。本轮82篇从61-91字符批量修到44-60字符。教训：先确认blog页是否已有自动截断逻辑（line 76 slice(0,57)+...），如果数据里已<=60则自动截断不触发。
- [2026-09-19] **INP完整优化指南（15要点）**：(1)INP替代FID测所有交互,Good<=200ms;(2)三阶段:Input Delay+Processing+Presentation;(3)长任务>50ms是最大杀手;(4)scheduler.yield()(Chrome115+)拆分长任务;(5)搜索框debounce 500-1000ms;(6)requestAnimationFrame+setTimeout(0)做postPaint polyfill;(7)LoAF API诊断;(8)事件回调不做昂贵同步操作;(9)DOM<1500节点;(10)避免layout thrashing;(11)content-visibility:auto跳过屏外渲染;(12)非关键JS lazy load;(13)preconnect关键第三方;(14)本站风险:/search过滤533工具+/category卡片渲染+/ranking排序;(15)落地:下次P0-MOBILE-001给/search加debounce(300ms),给/category加content-visibility:auto。来源:Google Codelabs+SitePoint+DebugBear。验证通过:4来源一致。

## [2026-09-19] AI Tool Directory Site Architecture & GEO Best Practices

**Source:** popularaitools.ai starter kit, webrepublic GEO checklist, aiso.blog AI search checklist, thesaasdir.com 2026 directory comparison

**Key learnings (10 points):**

1. **Hub-and-spoke internal linking is the #1 ranking driver** for AI tool directories. Every tool detail page must have 5 mandatory internal links: parent category, 2 sibling tools, 1 comparison page, 1 alternatives page. This is the single biggest structural difference between directories that rank and those that don't.

2. **Category pages need ItemList schema** where each item references the tool's canonical URL. This helps Google understand the relationship between category and tool pages.

3. **GEO (Generative Engine Optimization) requires content in initial HTML.** LLMs (GPTBot, ClaudeBot, PerplexityBot) don't execute JavaScript. Core content (H1, main text, links, FAQ) must be in server-rendered HTML source. SSG already satisfies this.

4. **Clear heading hierarchy is critical for AI search.** Exactly one H1 per page, logical H2/H3 structure, no headings used for visual styling. AI models parse headings to understand page structure.

5. **Chunk-level answers (Quick Answer blocks) get cited by AI search.** A 2-3 sentence direct answer at the top of the page, in a distinct block, is what Perplexity/ChatGPT extracts. Our new best-for pages have this.

6. **FAQPage schema with real on-page FAQ content** is still one of the highest ROI rich results. No hidden FAQ content — it must match visible content.

7. **Category depth matters:** Futurepedia has 54 categories, Toolify has thousands. Moving from 17 to 100+ subcategories (our P2 task) directly increases long-tail coverage.

8. **Scenario/audience pages ("Best AI tools for X")** are a proven traffic driver — these target high-intent long-tail keywords that generic category pages miss. Our new /best-for/ pages fill this gap.

9. **Daily new product tracking** keeps content fresh and catches trending keywords early. Product Hunt + HN monitoring with automatic short pages is the standard approach.

10. **E-E-A-T signals matter for AI search:** author bylines, review dates, hands-on testing details, and "tested & reviewed" badges all increase citation probability by LLMs.

**Actionable items for next iteration:**
- P0: Implement 5 mandatory internal links per tool page (hub-and-spoke)
- P1: Add ItemList schema to category listing pages
- P1: Add Quick Answer block to top 20 blog posts (GEO optimization)
- P2: Expand subcategories from 17 to 100+



- [2026-09-19] **GitHub Trees API ref update returns 404 on this repo** — Steps 1-5 (blob/tree/commit creation) succeed, but PATCH /git/ref/heads/main returns 404 even with force=true. The Contents API (PUT /repos/{owner}/{repo}/contents/{path}) works as a reliable fallback for committing individual files. Use it when Trees API ref update fails. Source: personal experience.
- [2026-09-19] **Title length optimization formula**: Tool title = '{name} Review 2026: {score}/10 | AIToolCrux'. Fixed overhead = 35 chars. To stay <=60, truncate name to 24 chars (24 + ellipsis). Verified: GitHub Copilot title = 47 chars.
- [2026-09-19] **Meta description word-boundary truncation**: Use lastIndexOf(' ') to avoid cutting mid-word. Min threshold 120 chars to avoid over-truncating short names. Strip trailing punctuation before adding ellipsis.

---

## [2026-09-20] 学习主题：Next.js Partial Prerendering (PPR) + INP优化（requestIdleCallback）

**来源（官方/权威）：**
- https://nextjs.org/docs/app/getting-started/partial-prerendering
- https://nextjs.org/blog/next-15-rc
- https://web.dev/articles/optimize-input-delay

**15个知识点：**
1. PPR把页面拆成静态shell（build时生成）+ 动态部分（request时streaming）
2. 静态shell立即从CDN返回，LCP不依赖动态数据
3. 动态部分用<Suspense>包裹，fallback即skeleton
4. Next.js 15里PPR通过`experimental.ppr: 'incremental'`或单路由`export const experimental_ppr = true`启用
5. 旧的`use cache` API实现了PPR，实验性ppr标志已移除
6. PPR不等于SSG——静态shell是预渲染，但动态部分仍需请求
7. PPR不等于ISR——它不按时间revalidate，而是流式渲染
8. 对于完全静态内容（如我们的533个工具页），PPR没有收益，SSG更省Vercel额度
9. PPR适合有少量动态内容的页面（如个性化推荐、实时库存）
10. requestIdleCallback允许浏览器在空闲时段执行非紧急任务，不阻塞关键交互
11. INP关注的是从用户交互到下一帧渲染的延迟；任何在click handler里的同步代码都会增加INP
12. 点击打开新标签页(target="_blank")的跟踪代码，必须defer——浏览器已经开始导航了，跟踪慢不影响用户
13. requestIdleCallback的fallback是setTimeout(0)，但requestIdleCallback更智能（只在空闲时执行）
14. requestIdleCallback的options.timeout设1500ms，确保跟踪不会被无限推迟
15. Vercel Analytics的va.track本身是异步的，但dispatchEvent是同步的——两者都defer才安全

**落地计划（下次迭代）：**
- P1-PERF-INP-001：升级WebVitalsReporter到attribution build（看具体哪个组件贡献INP）
- P1-PERF-SUSPENSE-001：在/blog和/tools列表页用Suspense包裹非关键数据（如Related Tools）
- 暂不启用PPR——我们是纯SSG站，Vercel带宽有限，PPR会引入请求时渲染

---

## [2026-09-20] 学习主题：GitHub Actions 依赖与构建缓存（actions/cache + setup-node cache + Next.js .next/cache）

**来源（官方/权威）：**
- https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/caching-dependencies-to-speed-up-workflows
- https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
- https://nextjs.org/docs/14/pages/building-your-application/deploying/ci-build-caching
- https://github.com/actions/setup-node (official README)

**15个知识点：**
1. actions/cache@v4 在workflow run之间缓存文件，避免重复下载npm包和重复编译（来源：GitHub Docs）
2. 缓存key必须用hashFiles('**/package-lock.json')——依赖变更时自动失效，用旧缓存会导致版本错误（来源：GitHub Docs）
3. 不要直接缓存node_modules，要缓存~/.npm（npm tarball缓存目录）——node_modules跨Node版本会坏，~/.npm是环境无关的（来源：GitHub Docs examples）
4. actions/setup-node有内置cache: 'npm'选项，自动处理~/.npm缓存，比手写actions/cache更简单（来源：setup-node README）
5. Next.js官方建议同时缓存~/.npm和.next/cache——.next/cache包含webpack编译缓存，二次构建快2-5倍（来源：nextjs.org CI build caching）
6. .next/cache的key应该同时hash package-lock.json和源码文件（*.ts/*.tsx）——源码变更时让webpack缓存失效（来源：Next.js docs）
7. restore-keys用于部分匹配——精确key没命中时，回退到同前缀的旧缓存，比如先命中任何上一次构建的缓存（来源：GitHub Docs）
8. 缓存命中后可以用if: steps.cache-npm.outputs.cache-hit != 'true'跳过npm install（来源：GitHub Docs）
9. 每个仓库缓存总量上限10GB，单条缓存7天TTL自动清除——不要缓存超大目录（来源：GitHub Docs）
10. 来自fork的PR对缓存只读（安全限制），不会写入新缓存（来源：GitHub Docs）
11. 多个cache步骤可以共存——一个缓存npm依赖，一个缓存.next/cache，互不干扰（来源：Next.js docs示例）
12. pnpm用户用setup-node的cache: 'pnpm'，它自动执行pnpm store path并缓存store（来源：setup-node README）
13. 缓存是per-repository的，不同branch共享同一缓存命名空间——所以key要包含runner.os避免Linux/macOS缓存串（来源：GitHub Docs）
14. 我们目前5个workflow都没有加缓存——gsc-fetch/context-update只装pip包（python缓存另说），但如果有Next.js build workflow应该加（来源：本次学习）
15. actions/cache的post步骤默认只在job成功时保存缓存（post-if: success()）——失败的构建不会污染缓存（来源：actions/cache README）

**落地计划（下次迭代）：**
- GHACT-CACHE-002：给Next.js build workflow加actions/cache@v4，缓存~/.npm + .next/cache，key含package-lock.json hash
- 如果当前没有build workflow（Vercel自动部署），则给gsc-fetch/context-update的python步骤加pip cache（actions/cache缓存~/.cache/pip）
- 下次写新workflow时，优先用setup-node的cache: 'npm'而不是手写actions/cache

---

## [2026-09-20] 学习主题：Next.js 图片与字体优化（next/image + next/font）

**来源（官方/权威）：**
- https://nextjs.org/docs/app/api-reference/components/image
- https://nextjs.org/docs/app/getting-started/images
- https://nextjs.org/docs/app/getting-started/fonts
- https://nextjs.org/docs/app/api-reference/components/font
- https://vercel.com/docs/conformance/rules/NEXTJS_USE_NEXT_FONT

**15个知识点：**
1. next/image 自动做四件事：WebP/AVIF转换、响应式srcset、视口外懒加载、CLS预防（固定宽高比）（来源：nextjs.org images）
2. **LCP图片必须加`priority`**——默认lazy会延迟加载LCP，加priority自动注入preload标签（来源：nextjs.org image docs）
3. 用`fill`模式时必须写`sizes` prop——告诉浏览器从srcset选哪个尺寸，不写默认100vw会加载过大图（来源：nextjs.org image API）
4. `quality` prop默认75，降到70可减体积约15%，肉眼几乎无差（来源：nextjs.org image API）
5. `placeholder="blur"` + `blurDataURL` 实现blur-up效果，感知加载更快（来源：nextjs.org image docs）
6. `fill`模式要求父元素position:relative且有明确尺寸（来源：nextjs.org image API）
7. next/font在build时下载Google Fonts并自托管——不发外部请求给Google，无FOUT，隐私更好（来源：nextjs.org fonts）
8. next/font必须指定`subsets: ['latin']`——只加载需要的字符子集，不加载全字库（来源：nextjs.org fonts）
9. next/font的`display: 'swap'`是最佳实践——文字立即可见，字体加载后替换，避免FOIT（来源：nextjs.org font API）
10. next/font的CSS variable可配合Tailwind使用，实现全局字体切换（来源：nextjs.org fonts）
11. next.config里`deviceSizes`控制全屏图生成的宽度数组，`imageSizes`控制小图——精简数组减少冗余变体（来源：nextjs.org image config）
12. 外部远程图（如第三方截图）必须在next.config的`images.remotePatterns`里配置域名白名单，否则报错（来源：nextjs.org image docs）
13. SVG图必须加`unoptimized` prop——next/image对SVG优化会出问题（来源：nextjs.org image docs）
14. Next.js 16中`priority`已废弃，改用`preload` prop（我们用14.2.5不受影响，但升级时要注意）（来源：nextjs.org blog）
15. Vercel Conformance规则NEXTJS_USE_NEXT_FONT：禁止用link标签加载Google Fonts，必须用next/font（来源：vercel.com docs）

**落地计划（下次迭代）：**
- P1-PERF-IMG-001：把工具页截图从原生img迁移到next/image，加priority(LCP图)、quality=70、sizes、placeholder=blur
- P2-PERF-SVG-001：SVG图标组件加unoptimized prop，省Vercel图片优化CPU
- P2-PERF-CONFIG-001：精简next.config的deviceSizes/imageSizes数组，减少冗余图片变体
- 检查layout.tsx是否用next/font自托管字体，不用外部Google Fonts link


---

## [2026-09-20] 学习主题：结构化数据 2026 最佳实践（Google Rich Results + SoftwareApplication + Review 政策更新）

**来源（官方/权威）：**
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies/
- https://developers.google.com/search/docs/appearance/structured-data/software-app
- https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- https://developers.google.com/search/docs/appearance/structured-data/article
- https://developers.google.com/search/docs/appearance/structured-data/faqpage
- https://developers.google.com/search/updates （2026年5月FAQ弃用公告、2026年7月Review政策更新）
- https://www.seo-kreativ.de/en/blog/faq-rich-results-discontinued/ （交叉验证FAQ弃用时间线）
- https://ppc.land/manual-actions/ （交叉验证2026年7月Review政策更新）

**15个知识点：**
1. **FAQ富摘要已于2026年5月7日全面下线**——Google不再在搜索结果展示FAQ富摘要；Rich Results Test于2026年6月移除FAQ支持；Search Console API于2026年8月移除FAQ支持。FAQPage schema本身不被禁止，仍可写（对AI搜索/GEO有帮助），但不要再指望它带来星级富摘要（来源：Google FAQ page docs + changelog 2026-05）
2. **SoftwareApplication必填字段**：`name`、`image`、以及`offers`/`aggregateRating`/`review`三者至少其一。付费应用必须写`offers.priceCurrency`（来源：Google Software app docs）
3. **免费应用的offers写法**：`"offers": {"@type": "Offer", "price": "0"}`——price是字符串不是数字，priceCurrency可省略（来源：Google Software app docs）
4. **AggregateRating必填**：`ratingValue` + `ratingCount`/`reviewCount`至少其一。`bestRating`/`worstRating`推荐（来源：Google Review snippet docs）
5. **【政策红线】结构化数据里的评分必须和页面上真实可见的评分一致**——如果页面上没有展示127条真实用户评价，就不能写ratingCount=127；这是2026年7月24日Review政策更新明确禁止的，会触发人工处置直接摘掉星级（来源：Google sd-policies + ppc.land 2026-07政策更新）
6. **【政策红线】虚假评价和未披露的有偿评价会被人工处置**——2026年7月24日起Google明确把fake reviews和undisclosed incentivized reviews列为结构化数据违规，2025年Google已屏蔽/删除2.92亿条违规评价（来源：Google changelog 2026-07-24 + ppc.land）
7. **结构化数据人工处置只影响富摘要展示资格，不影响自然排名**——如果因为schema问题被manual action，页面照样能排名，只是没有星级/富摘要（来源：Google sd-policies docs）
8. **Article schema推荐字段**：`headline`（≤110字符）、`image`（ImageObject，至少1920x1080）、`datePublished`、`dateModified`、`author`（Person/Organization）、`publisher`（含logo）（来源：Google Article docs）
9. **dateModified强烈推荐**——告诉Google内容更新时间，帮助时效性排名；博客文章每次更新都要刷新（来源：Google Article docs）
10. **BreadcrumbList用ItemList嵌套ListElement**：每个item必须有`position`（1,2,3...）、`name`、`item`（URL）。不要用扁平的ItemList（来源：Google Breadcrumb docs交叉验证）
11. **所有结构化数据必须反映页面可见内容**——不能写页面上不存在的评价、价格、评分；Google明确说"如果标记了多条评价，必须包含用户在页面上能看到的所有评价"（来源：Google sd-policies 2026-09-16更新）
12. **SoftwareApplication推荐字段**：`applicationCategory`（如"DesignApplication"）、`operatingSystem`、`description`、`screenshot`、`softwareVersion`（来源：Google Software app docs）
13. **ratingValue用点号不用逗号**——小数必须用`.`分隔，用`,`会导致解析错误（来源：greadme.com Review schema guide，交叉验证Google parser行为）
14. **Google spam policies现在也适用于Google AI Overviews/生成式AI回答**——结构化数据作弊不仅影响传统搜索，也影响AI答案里的引用（来源：Google changelog 2026-08-31 "spam policies apply to generative AI responses"）
15. **JSON-LD script必须是`<script type="application/ld+json">`**——不要用microdata或RDFa；Next.js里用`<script dangerouslySetInnerHTML={{__html: JSON.stringify(data)}} />`（来源：Google sd-policies + Next.js App Router metadata实践交叉验证）

**落地计划（下次迭代）：**
- P1-VERIFY-001：用Google Rich Results Test验证5个工具页的SoftwareApplication schema——重点查：有没有ratingCount/reviewCount、ratingValue是不是数字字符串、offers.price是不是"0"或带priceCurrency
- P0-SCHEMA-001：审计533个工具页的AggregateRating——如果页面上没有真实用户评价展示，把aggregateRating字段从schema里删掉或改成review（基于我们自己的评测），避免2026年7月政策红线
- P2-FAQ-001：FAQPage schema保留（对AI搜索/GEO有用），但不要再把它当成Google富摘要优化点；下次GSC FAQ报告里的"问题"不用急着修
- P1-ARTICLE-001：检查105篇博客文章的Article schema——补dateModified、确保author是"AIToolCrux Research Team" Organization、image至少1920x1080
- P2-BREADCRUMB-001：抽查工具页BreadcrumbList结构，确认position字段从1开始且连续


---

## [2026-09-20] 学习主题：Core Web Vitals 2026 完整指南（LCP + INP + CLS + TTFB）

**来源（官方/权威）：**
- https://web.dev/metrics/lcp （Google官方 LCP 指南）
- https://web.dev/metrics/inp （Google官方 INP 指南）
- https://web.dev/metrics/cls （Google官方 CLS 指南）
- https://web.dev/articles/optimize-cls （Google官方 CLS 优化）
- https://web.developers.google.cn/articles/top-cwv （Google官方"提高CWV最有效方法"）
- https://www.corewebvitals.io/core-web-vitals/interaction-to-next-paint/ （交叉验证 INP 三阶段）
- https://blog.sentry.io/what-is-inp/ （交叉验证 yieldToMain / Web Workers）
- https://www.seo-kreativ.de/en/blog/core-web-vitals-optimizing/ （交叉验证阈值表）

**15个知识点：**
1. **2026年CWV阈值（按75分位真实用户）**：LCP ≤2.5s（差>4.0s）、INP ≤200ms（差>500ms）、CLS ≤0.1（差>0.25）。不是平均值，是75分位——意味着最慢的25%用户决定是否达标（来源：web.dev metrics + seo-kreativ交叉验证）
2. **INP 2024年3月正式替换 FID**——FID只测第一次交互的延迟，INP测整次会话里所有交互（点击/输入/滚动）的最差值。一个只在第一次交互快、后面卡的站点会过FID但挂INP（来源：web.dev INP + anhtu.dev交叉验证）
3. **INP三阶段**：input delay（事件分发到回调）+ processing time（回调执行）+ presentation delay（下一帧绘制）。任一阶段慢都会拉低INP，要系统优化（来源：corewebvitals.io INP指南）
4. **长任务（>50ms）是INP头号杀手**——浏览器主线程单线程，>50ms的任务阻塞交互响应。用`await scheduler.yield()`（或yieldToMain polyfill）在大循环里主动让出主线程，让浏览器先画帧（来源：web.dev top-cwv + SitePoint 2026 INP指南）
5. **事件处理器要debounce/throttle**——scroll/resize/input/keydown这些高频事件，每次都跑大计算会直接拖垮INP；用lodash.debounce或手写leading/trailing throttle（来源：Sentry INP指南 + corewebvitals.io）
6. **重计算移到Web Worker**——排序/筛选/解析JSON这种CPU密集活，放Worker里跑，主线程只管UI；Next.js里可用`workerize`或动态import worker（来源：Sentry INP指南）
7. **TTFB是LCP的地基**——Google官方"good"线≤800ms，但要做到LCP<2.5s，TTFB实际目标应该是200-400ms。TTFB慢=所有后续优化都被封顶（来源：web.dev LCP + overthetopseo交叉验证）
8. **LCP元素通常是hero图或H1文本**——先用Chrome DevTools Performance面板的Web Vitals overlay定位LCP元素，再针对性优化；不要盲目优化所有图（来源：freedevtool + clarigital交叉验证）
9. **LCP图片必须preload + fetchpriority="high"**：`<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">`放在<head>，让浏览器在HTML解析到<img>之前就开始下载（来源：freedevtool LCP指南 + web.dev交叉验证）
10. **图片用WebP/AVIF**——比JPEG小30-50%；Next.js的next/image自动做格式协商，但LCP图要手动加priority（来源：ankitseo + web.dev交叉验证）
11. **CLS头号原因：图片没设width/height**——从2020年起主流浏览器用width/height属性自动算aspect-ratio预留空间；next/image自动处理，原生<img>必须写死width/height或CSS aspect-ratio（来源：web.dev optimize-cls + framerwebsites交叉验证）
12. **字体引起的CLS：用size-adjust/ascent-override**——给fallback字体加CSS Fonts Level 4的`size-adjust`和`ascent-override`，让fallback和web font的metrics尽量接近，字体替换时文字不跳动（来源：hidekazu-konishi web performance checklist）
13. **首屏动态插入的元素会造成CLS**——广告/embed/cookie banner/通知条，必须预留占位空间（min-height），不要在加载后突然插入（来源：aria.nanocorp CLS指南 + web.dev交叉验证）
14. **RUM用web-vitals库**——Google官方~1KB的`web-vitals` npm包，真实上报LCP/INP/CLS到自建端点或GA4；实验室Lighthouse只代表你自己机器，不代表75分位真实用户（来源：web.dev + Sentry交叉验证）
15. **移动桌面要分开看**——Google Search Console按设备分组报CWV；移动端通常比桌面差，因为CPU/网络更弱；优化时优先移动端（来源：web.dev + visiblytics交叉验证）

**落地计划（下次迭代）：**
- P1-PERF-RUM-001：装`web-vitals` npm包，在layout.tsx加Reporter组件，先console.log积累7天真实用户LCP/INP/CLS数据
- P1-PERF-LCP-001：用Chrome DevTools定位首页/blog页的LCP元素，给hero图加`fetchpriority="high"`和preload
- P2-PERF-CLS-001：审计原生<img>标签，确保都有width/height（next/image自动覆盖，重点查自定义组件里的裸img）
- P2-PERF-INP-001：查事件处理器，筛选/搜索/分页这种交互加debounce，大循环里加yieldToMain
- P2-PERF-TTFB-001：用PageSpeed Insights测首页TTFB，确认Vercel边缘缓存是否命中（SSG应该<200ms）


---

## [2026-09-20] 学习主题：GitHub Actions 安全加固与定时任务最佳实践（2026）

**来源（官方/权威）：**
- https://docs.github.com/en/actions/reference/security/secure-use （GitHub官方 secure-use 参考）
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions （GitHub官方 hardening 指南）
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax （GitHub官方 workflow 语法）
- https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration （GitHub官方限额）
- https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows （GitHub官方 reusable workflows）
- https://github.blog/changelog/2026-07-30-reference-same-repository-actions-with-self-repository-syntax/ （2026-07 新语法）
- https://blogs.eclipse.org/post/mika%C3%ABl-barbero/stop-trusting-mutable-references... （Trivy 供应链事件 SHA pin 交叉验证）
- https://safeguard.sh/resources/blog/github-actions-supply-chain-security （2026 hardening guide 交叉验证）
- https://en.ittrip.xyz/windows/troubleshooting/actions-schedule-not-running （定时任务自动禁用规则交叉验证）

**15个知识点：**
1. **GITHUB_TOKEN 默认必须 read-only**——仓库级 Settings → Actions → General → Workflow permissions 设为 Read;每个 job 按需 elevate（contents: write、issues: write 等）。老仓库默认 read-write，被攻破的 action 能直接推代码/建 release（来源：GitHub secure-use + safeguard.sh交叉验证）
2. **第三方 action 必须 pin 到完整 commit SHA，不能用 tag**——Trivy 事件证明 tag 可被移动（攻击者控制上游仓库后改 tag 指向恶意 commit）。写法：`uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`。用 Dependabot 自动升级 SHA（来源：Eclipse Foundation Trivy post + GitHub hardening guide）
3. **不要把事件上下文直接拼进 run:**——`run: echo ${{ github.event.issue.title }}` 是注入漏洞，PR 标题里写 `"; rm -rf /"` 就能执行。必须用 `env:` 传值：`env: TITLE: ${{ github.event.issue.title }}` + `run: echo "$TITLE"`（来源：GitHub secure-use + wasilzafar交叉验证）
4. **OIDC 代替长云凭证**——不要把 AWS/GCP 密钥塞 Secrets；用 GitHub OIDC token 临时换云凭证，用完即弃。OIDC trust policy 要限制到 specific repo + branch（来源：GitHub hardening + wasilzafar）
5. **pull_request_target + checkout fork = 高危组合**——fork PR 能拿到 secrets，除非你完全不 checkout fork 代码。本项目是私有仓库不涉及，但如果开公开 PR 要警惕（来源：GitHub secure-use + CSA AI Actions report）
6. **Composite action vs Reusable workflow 区别**——composite action 把多个 step 打包成一个 step（在 caller job 里跑）；reusable workflow 是完整 workflow（在 caller 的 job 级别用 `jobs.<id>.uses` 调用，有独立 secrets/env）。多个 workflow 共享步骤用 composite，跨仓库用 reusable（来源：GitHub docs reusing-workflows）
7. **【2026-07 新语法】self-repository 引用**——`uses: $/.github/actions/my-action` 自动解析到当前仓库当前 commit，不用 checkout，不用写 owner/repo@SHA（来源：GitHub changelog 2026-07-30）
8. **定时任务 cron 默认 UTC，2026 起支持 IANA timezone**——`on.schedule.cron` + 顶层 `timezone: "Asia/Shanghai"`。最短间隔 5 分钟。定时任务跑的是 default branch 上最新 commit（来源：GitHub workflow syntax 2026-09更新）
9. **【坑】公开仓库定时任务 60 天无活动自动禁用**——GitHub 会自动 disable 长时间没跑的 scheduled workflow，需要去 Actions 页面手动 re-enable。私有仓库不受此限制（来源：IT trip 2026-09 + GitHub docs）
10. **API 限额：每仓库每小时 1000 次 GitHub API 请求**——workflow 里频繁调 GitHub API 会超限导致 job 失败。用 `gh api` 时分页缓存，或用 GITHUB_TOKEN 走 graphql 减少次数（来源：GitHub usage limits）
11. **Dependabot 必须开**——`dependabot.yml` 里配 `package-ecosystem: "github-actions"`，自动 PR 升级 action SHA（来源：GitHub hardening + wasilzafar）
12. **production 部署要 environment protection rules**——Settings → Environments → production 配 required reviewers，手动 approve 才部署；限制只能从 main branch 部署（来源：GitHub hardening + safeguard.sh）
13. **workflow_dispatch 手动触发时 inputs 要校验**——不要直接把 input 当 shell 变量用；同样走 env:（来源：GitHub secure-use）
14. **并发控制 concurrency**——同一个 workflow 不要重叠跑：`concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: false }`。定时任务重叠会浪费 minutes（来源：GitHub workflow syntax）
15. **不要在日志里 echo secret**——GitHub 自动 mask `GITHUB_TOKEN`，但自定义 secret 如果被 echo 到 stdout 会泄露；用 `::add-mask::` 或 `echo "::debug::"` 时小心（来源：GitHub secure-use + CSA report）

**落地计划（下次迭代）：**
- P1-CI-001：审查现有 .github/workflows/ 所有 yml，确保每个 job 显式声明 permissions（不要依赖仓库默认 read-write）
- P1-CI-002：把所有 `uses: owner/action@vX` 改成 pin 到完整 commit SHA；配 Dependabot 自动升级
- P2-CI-003：检查 gsc-fetch/context-update 等 workflow 有没有把 github.event 上下文直接拼进 run:，改成 env: 传值
- P2-CI-004：给定时任务 workflow 加 concurrency 块，防止重叠跑
- P2-CI-005：如果以后开公开仓库，记得 60 天无活动会自动 disable 定时任务


---

## [2026-09-20] 学习主题：GEO（AI 搜索优化）与 llms.txt 2026 完整指南

**来源（官方/权威）：**
- https://llmstxt.studio/blog/llmstxt-and-geo （llms.txt 规范：H1 + blockquote + H2 sections + markdown links）
- https://www.llms-txt-generator.de/blog/llms-txt-2026-ki-crawler-steuern-fuer-sichtbarkeit （llms-full.txt 用法）
- https://capston.ai/robots-txt-for-ai-bots/ （AI crawler UA 完整清单）
- https://landkit.pro/free-tools/ai-crawler-reference/ （AI crawler UA 交叉验证表）
- https://alicelabs.ai/en/insights/ai-crawler-management （search-time vs training bot 策略）
- https://digicore101.com/knowledge/how-to-get-cited-by-ai-geo-seo （Perplexity/Google AI Overviews 引用信号对比）
- https://crawlraven.com/blog/how-to-rank-in-chatgpt （Perplexity Sonar 偏好）
- https://aithinkerlab.com/generative-engine-optimization-2026/ （GEO 内容技巧：+40%/+115% 数据）
- https://nivaalabs.com/generative-engine-optimization-geo-2026... （第三方引用 6.5x、ChatGPT referral +206%）

**15个知识点：**
1. **llms.txt 规范**：第一行 `# 站点名`（唯一 H1），紧接着 `> 一句话描述` blockquote，然后用 `## 分类` H2 分组，每条 `- [链接文字](URL)` markdown 链接列关键页面。不是给人看的 sitemap，是给 AI 看的"意义摘要"（来源：llmstxt.studio）
2. **llms.txt vs robots.txt vs sitemap.xml**：robots.txt 管"能不能爬"，sitemap.xml 管"有哪些 URL"，llms.txt 管"这站是什么、重点是什么"。三者互补，不互相替代（来源：腾讯云 GEO 文章 + llmstxt.studio）
3. **llms-full.txt**：llms.txt 是精选摘要，llms-full.txt 是全站完整内容给 AI 全量抓取用；大站点建议 llms.txt 列精选 + llms-full.txt 做全量索引（来源：llms-txt-generator.de 2026）
4. **AI 爬虫 UA 分类**：训练型（GPTBot、ClaudeBot、CCBot、Google-Extended）只用于训练；搜索型（OAI-SearchBot、Claude-SearchBot、PerplexityBot、ChatGPT-User、Perplexity-User、Claude-User）用于实时回答引用。策略：放开搜索型，选择性 block 训练型（来源：capston.ai + landkit.pro 交叉验证）
5. **robots.txt 是自愿遵守**——AI 爬虫不一定 100% 遵守；要硬拦截得在 CDN/WAF 层按 UA 或 IP 段封。本项目 Vercel 层可配（来源：alicelabs.ai）
6. **Perplexity Sonar 偏好**：①新鲜度是第一排名因子（每周更新内容被引率高）；②显式 inline 引用 + 数据表格 + 来源链接；③FAQ 问答结构直接抽取；④PerplexityBot 不执行 JS，必须 SSG/SSR 直出 HTML（本项目已 SSG，天然符合）（来源：crawlraven + linksurge.jp 交叉验证）
7. **Google AI Overviews 偏好**：传统 SEO 权威性 + E-E-A-T + featured snippet 资格；结构化数据（FAQ/Article）重要；和 Google top-10 相关性 ~78%（来源：digicore101）
8. **Perplexity 和 Google top-10 相关性 91%**——传统 SEO 做对了，Perplexity 引用覆盖 90%；GEO 不是重写 SEO，是在 SEO 基础上加 AI 友好层（来源：digicore101）
9. **GEO 内容技巧（论文实测数据）**：①加具体数字/百分比/日期 → 可见度 +40%；②加可信第三方直接引语 → citation magnet；③加 inline 来源引用 → 第 5 名站点可见度 +115.1%（来源：aithinkerlab GEO 2026 论文综述）
10. **第三方引用比自有域名强 6.5x**——品牌被第三方权威源（Gartner/Forrester/政府数据/行业媒体）提到，比自己网站说"我最好"更可能被 AI 引用。要做外链和媒体提及，不是只优化站内（来源：nivaalabs GEO 2026）
11. **ChatGPT 外溢 referral 2025 年涨 206%**——AI 回答里的引用链接直接带来流量；GEO 不是玄学，是有实际 referral 的（来源：nivaalabs / Semrush 2026-04 数据）
12. **引用磁铁类型**：命名研究机构（Gartner/Forrester/McKinsey）、命名行业工具带公开数据（Semrush/Ahrefs）、政府/机构数据、带具体日期的命名出版物（"Forbes 2026年1月报道"）、一手原始数据（来源：yangsweb GEO 指南）
13. **AI Discovery Files 规范（2026）**：10 个文件分 3 层——Essential：llms.txt（Markdown 身份）、ai.txt（纯文本使用权限）；Recommended：identity.json 等；Advanced 更多。llms.txt 只是第一层（来源：WordPress.org AI Discovery Files 插件文档）
14. **FAQ 结构直接被抽取**——Perplexity/Claude 把显式 Q&A 对直接抽进回答；文章里用 `## FAQ` + `### Q: ...` + 直接回答，比长段落更容易被引用（来源：linksurge.jp + crawlraven 交叉验证）
15. **不要把 AI 爬虫全 block**——全 block GPTBot/ClaudeBot 只影响训练归属，不影响实时引用；要 block 的是训练型（GPTBot/ClaudeBot/CCBot），放开搜索型（OAI-SearchBot/PerplexityBot/Claude-SearchBot）才能被实时回答引用（来源：alicelabs.ai + williamspurlock 交叉验证）

**落地计划（下次迭代）：**
- P1-GEO-001：审 public/llms.txt，按规范补全：H1 站名 + > 一句话描述 + ## 分类（reviews/compare/blog/tools）+ 每类列 5-10 个关键 URL
- P1-GEO-002：审 public/robots.txt，显式加 AI 爬虫 UA：OAI-SearchBot/Claude-SearchBot/PerplexityBot/ChatGPT-User/Claude-User/Perplexity-User 都 Allow；训练型 GPTBot/ClaudeBot/CCBot 默认 Allow（要被训练）
- P2-GEO-003：给每篇 blog 文章加 `## FAQ` 章节（3-5 个 Q&A 对，直接回答句），符合 Perplexity 抽取偏好
- P2-GEO-004：文章正文里加具体数字（定价、月访问量、准确率百分比）+ inline 来源链接，符合 +40%/+115% 数据
- P2-GEO-005：考虑加 public/llms-full.txt，做全站精选内容索引


---

## [2026-09-20] 学习主题：Schema.org Review/AggregateRating 与 Google 2026-07 政策合规

**来源（官方/权威）：**
- https://developers.google.com/search/docs/appearance/structured-data/review-snippet （Google 官方 Review snippet 文档，2026-09-08 更新）
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies/ （Google 结构化数据通用政策，2026-07-10 更新）
- https://ppc.land/google-bans-undisclosed-incentivized-reviews-sites-face-manual-action/ （2026-07-24 Google 新规）
- https://kompozy.io/guides/google-review-snippet-guidelines-fake-incentivized-reviews （2026 政策解读）
- https://www.greadme.com/blog/schemas/what-is-review-schema-complete-guide （Required properties 交叉验证）
- https://developers.google.com/search/docs/appearance/structured-data/faqpage （FAQ rich results 2026-05-07 废弃）

**15个知识点：**
1. **Review snippet 必填属性**：itemReviewed（被评价对象，必须有 @type 和 name）、ratingValue（数字，小数点用 `.` 不用 `,`）、ratingCount 或 reviewCount 至少一个（整数）。bestRating 省略默认 5，worstRating 省略默认 1（来源：Google 官方 + greadme 交叉验证）
2. **Google 支持的可评价类型**：Product、Recipe、SoftwareApplication、Movie、LocalBusiness、Book、Event、Question、Course、Episode、Game、MediaObject、CreativeWorkSeason 等。工具站用 SoftwareApplication 合法（来源：Google 官方文档）
3. **2026-07-24 新规（关键）**：Google 在 Review snippet 指南加了一行——"不要在页面或结构化数据中包含虚假评价或未披露利益关系的激励评价"。违规会触发 manual action，直接摘掉星级 rich result（来源：ppc.land + kompozy 交叉验证）
4. **结构化数据必须匹配页面可见内容**：如果你标了 127 个 review，用户在页面上必须真的能看到 127 个 review。标了 4.3 分但页面显示 4.7，会被判误导。手动加了 127 个结构化 review 但页面只显示 3 个 = 违规（来源：Google 通用政策 sd-policies）
5. **AggregateRating 必须代表"一群评价者"的总分**，不是单个编辑的分数。这对工具评测站是红线：如果 AIToolCrux 的评分是编辑团队自己打的，没有真实用户评价，直接加 AggregateRating 可能不被显示星级，甚至被判违规（来源：Google 官方 + seotopsecret 交叉验证）
6. **自测/自评（self-serving review）风险**：如果网站本身就是评价作者，Google 要求页面包含多个真实用户/评价者的 review。单个编辑打 8.5/10 这种，即使标了 schema，Google 也可能不显示星级（来源：Google 官方 review snippet 文档）
7. **FAQ rich results 2026-05-07 已废弃**：Google 不再在搜索结果显示 FAQ 手风琴式富结果，Rich Results Test 6 月移除支持，Search Console API 8 月移除。但 FAQ schema 仍保留对 AI/GEO 的价值（Perplexity/Claude 抽取）（来源：Google 官方 faqpage 文档）
8. **AI Overviews 也受垃圾政策约束**：2026-09 Google 更新明确，spam policy 同样适用于 AI Overviews 回答——虚假结构化数据不仅摘星级，还可能影响 AI 回答中的呈现（来源：Google Search updates 2026-09-12）
9. **Manual action 后果**：结构化数据问题触发 manual action 后，页面失去所有 rich result 资格，需要在 Search Console 提交复核请求才能恢复。比普通排名下滑严重得多（来源：Google sd-policies）
10. **激励评价披露要求**：如果评价是通过返利/免费产品/折扣换来的，必须在页面上"清晰且显著地披露"（clear and conspicuous disclosure）。affiliate 站尤其要注意——我们的 /affiliate-disclosure 页面是对的，但每个工具页也要在评价附近明确说"我们可能从通过链接注册获得佣金"（来源：ppc.land + wpconsults 交叉验证）
11. **价格和库存要动态**：Google 建议 offer.price、offer.availability 用动态数据，不要硬编码。价格变了没改 schema 会被判过期/误导（来源：schema-validator.com + Google 官方）
12. **SoftwareApplication 推荐字段**：@type=SoftwareApplication、name、description、applicationCategory（如 "DeveloperApplication"、"BusinessApplication"）、operatingSystem、offers（price/priceCurrency/availability）、aggregateRating。可选 fileSize、storageRequirements 等（来源：Google 官方 + thatdevpro 交叉验证）
13. **ratingValue 范围**：必须和 bestRating/worstRating 一致。如果 bestRating=10，ratingValue=8.5 合法；如果 bestRating=5，ratingValue=8.5 就不合法。我们工具站用 1-10 分制，schema 里必须显式写 bestRating: 10, worstRating: 1（来源：Google 官方 review-snippet 文档）
14. **BreadcrumbList 独立于 Review snippet**：面包屑用 BreadcrumbList schema，position 从 1 开始，item 是完整 URL。和工具评分 schema 分开，不冲突（来源：Google 官方 + seotopsecret）
15. **不要为了星级而 schema**：如果没有真实用户评价，宁可不加 AggregateRating，也不要加了被 Google 判违规。替代方案：用 Article/Review schema 标我们自己的评测文章（review 是我们写的，itemReviewed 是工具），但不加 aggregateRating——这样不会触发"自评分"违规，同时保留评测文章被 Google 理解为 review 的能力（来源：综合 Google 官方 + 2026 政策解读）

**落地计划（下次迭代 P0-SCHEMA-001 直接用）：**
- P0-SCHEMA-001：审 533 工具页的 AggregateRating schema。如果评分是编辑团队打的、没有真实用户评价，**直接移除 aggregateRating 字段**，避免 2026-07 新规 manual action 风险。保留 SoftwareApplication + offers + name + description，不保留 aggregateRating。
- P0-SCHEMA-001b：保留我们自己的单篇评测 review schema（review 是我们写的，itemReviewed=工具），但 reviewRating.ratingValue 和页面上的分数一致，不要加 aggregateRating。
- P1-SCHEMA-DISCLOSURE：每个工具页 CTA 按钮附近加一句"May earn commission"，和 /affiliate-disclosure 呼应，满足激励披露要求。
- P1-SCHEMA-002：ratingValue 范围检查——所有 bestRating 设为 10、worstRating 设为 1，确保 1-10 分制和 schema 一致。
- P2-SCHEMA-003：如果未来要加真实用户评价系统（评论区），再恢复 aggregateRating，那时才符合"一群评价者"要求。


---

## [2026-09-20] 学习主题：Next.js Image/Font 优化与 LCP 实战（P1-PERF-IMG-001 直接落地）

**来源（官方/权威）：**
- https://nextjs.org/docs/app/getting-started/images （Next.js 官方图片文档，2026-08-25）
- https://nextjs.org/docs/app/api-reference/components/image （next/image API reference）
- https://nextjs.org/docs/app/getting-started/fonts （next/font 官方文档，2026-05-27）
- https://web.dev/articles/top-cwv （web.dev 官方 Core Web Vitals 指南）
- https://www.corewebvitals.io/core-web-vitals/largest-contentful-paint/ （fetchpriority 案例：Google Flights LCP -700ms）
- https://dev.to/ahmed_mahmoud360/nextimage-in-nextjs-16-field-notes-on-lcp （Next.js 16 field notes，2026-09-13）

**15个知识点：**
1. **next/image 四大自动优化**：自动按设备尺寸裁剪（WebP/AVIF）、自动防布局偏移（CLS=0）、默认 lazy load、远程图片按需 resize（来源：Next.js 官方）
2. **🚨 sizes prop 是最容易写错的**：一个 400px 宽的卡片如果不写 sizes，浏览器会按 100vw 下载 3840px 原图，带宽翻倍。正确写法 `sizes="(max-width: 768px) 100vw, 400px"`（来源：dev.to field notes + Next.js 官方交叉验证）
3. **priority prop 只用于 LCP 图**：priority = 关闭 lazy load + 自动加 `<link rel="preload">`。一张页面只给最可能成为 LCP 的那张图加，给多张图加 priority 会互相抢带宽，反而拖慢 LCP（来源：Next.js 官方 + dev.to FAQ 交叉验证）
4. **fetchpriority="high"**：原生 HTML 属性，告诉浏览器这张图要优先下载。Google Flights 只加了这个属性，LCP 降了 700ms。next/image 的 priority 内部就是做这个（来源：corewebvitals.io 案例）
5. **Next.js 16 next/image v4 默认 AVIF**：AVIF 比 WebP 再小 20% 左右，自动协商格式。老浏览器自动 fallback（来源：dev.to/jsmanifest 2026-09-07）
6. **🚨 Next.js 不放大图片**：原图只有 400px，放到 800px 容器里会模糊，不会自动 upscale。工具截图要上传足够大的原图（至少 2x DPR，800px 卡片传 1600px 原图）（来源：dev.to FAQ）
7. **next/font 自动自托管**：build 时把 Google Fonts 下载到本地，和静态资源一起 self-host，消除外部 DNS/TLS 请求。中国用户访问 Google Fonts 慢的问题直接消失（来源：Next.js 官方）
8. **next/font 自动 fallback 字体度量匹配**：自动生成 size-adjust、ascent-override、descent-override、line-gap-override，让 fallback 字体和实际字体尺寸一致，font swap 时零 CLS（来源：Next.js 官方 + fontfyi 交叉验证）
9. **display: 'swap' 配置**：next/font 里 `display: 'swap'` 让文本立即用 fallback 显示，字体加载完再 swap，消除 FOIT（不可见文本）（来源：Next.js 官方）
10. **placeholder="blur"**：本地图片自动生成模糊占位图（blur-up），LCP 之前先看到模糊轮廓，感知速度快。远程图片要自己传 blurDataURL（来源：Next.js 官方）
11. **loading="lazy" 默认值**：除了 priority 的图，其他都默认 lazy。不要再手写 loading="lazy"，会冗余（来源：Next.js 官方）
12. **decoding="async"**：非关键图片建议加 `decoding="async"`，图片解码不阻塞主线程，INP 更好（来源：webperfclinic 2026）
13. **deviceSizes 配置**：next.config.mjs 里默认 deviceSizes=[640,750,828,1080,1200,1920,2048,3840]。我们工具站卡片都小（最大 400px），可以把 deviceSizes 改成 [480, 640, 750, 828, 1080]，省掉大尺寸变体（来源：Next.js 官方 image config + P2-PERF-CONFIG-001 已做）
14. **unoptimized prop 用于 SVG**：SVG 图标走 next/image 会消耗 Vercel image optimization CPU，直接 `unoptimized` 跳过。我们 P2-PERF-SVG-001 就是这个（来源：Next.js 官方 image API）
15. **LCP 优化顺序**：① 找 LCP 元素（Chrome DevTools Performance）② 给它加 priority + fetchpriority=high ③ 确保 sizes 正确 ④ 确保图片格式 AVIF/WebP ⑤ 预连接 CDN。不要一上来就换图床，先做这 5 步（来源：web.dev 官方 + corewebvitals 交叉验证）

**落地计划（下次迭代直接用）：**
- **P1-PERF-IMG-001**：工具页截图迁移 next/image。每张卡片图加正确 sizes：列表卡片 `sizes="(max-width: 768px) 100vw, 400px"`，工具详情页 hero `sizes="(max-width: 768px) 100vw, 800px"`。只给详情页 hero 截图加 priority，其他 lazy。
- **P1-PERF-LCP-001**：首页/工具详情页 LCP 元素（hero 截图或主图）加 priority + fetchpriority="high"。
- **P2-PERF-SVG-001**：所有 SVG 图标组件加 `unoptimized`。
- **P2-PERF-CLS-001**：检查所有 <img> 有没有 width/height，没有的补上；next/image 自动有 width/height，迁移后 CLS 自然降。
- **P1-PERF-IMG-002（新）**：确认 next.config.mjs deviceSizes 改成 [480,640,750,828,1080]，去掉 1920/2048/3840 这些我们用不到的大尺寸。


---

## [2026-09-20] 学习主题：GSC Indexing API / URL Inspection API / IndexNow / Sitemap 监控完整指南

**来源（官方/权威）：**
- https://developers.google.com/webmaster-tools/limits （Google 官方 API 配额文档）
- https://developers.google.com/search/apis/indexing-api/v3/using-api （Google Indexing API 官方文档，2026-07-17）
- https://developers.google.com/search/apis/indexing-api/v3/quota-pricing （Indexing API 配额）
- https://www.indexnow.org/documentation （IndexNow 官方文档）
- https://www.indexnow.org/faq （IndexNow FAQ）
- https://www.screamingfrog.co.uk/seo-spider/tutorials/how-to-automate-the-url-inspection-api/ （Screaming Frog 权威教程，2026-09-13）
- https://www.sitemapr.com/blog/gsc-sitemap-status-decoded （GSC sitemap 状态解读，2026-05-07）

**15个知识点：**
1. **URL Inspection API 配额**：每 property 2000 QPD（每天2000次）、600 QPM（每分钟600次）；每 project 10M QPD。用途是抽样检查，不是全站逐页查——Google 认为"有些 URL 不被索引是正常的"（来源：Google 官方 limits + Screaming Frog 交叉验证）
2. **🚨 Google Indexing API 只支持 JobPosting / BroadcastEvent**：官方明确说只用于有 JobPosting 或 BroadcastEvent 结构化数据的页面。用它提交普通博客/工具页是 off-label——可能触发爬取但不保证索引，不要依赖（来源：Google 官方 using-api 文档 + seoautomationclub 交叉验证）
3. **Indexing API 默认配额**：每 project 每天 200 次 publish 请求（URL_UPDATED + URL_DELETED 合计），太平洋时间午夜重置。需要更多要申请审批（来源：Google 官方 quota-pricing）
4. **Indexing API 批量**：一次 HTTP multipart 请求最多合并 100 个 URL。不要用多账号绕配额（来源：Google 官方 using-api）
5. **IndexNow 不是 Google 的**：IndexNow 是 Microsoft（Bing/Yandex/Seznam）技术，Google 不直接用。但 IndexNow 提交会共享给所有支持的引擎。我们的 IndexNow key 主要帮 Bing 收录，不是 Google（来源：indexnow.org 官方 + rampify 交叉验证）
6. **IndexNow 批量**：单次 POST 最多 10,000 个 URL，无官方频率限制，但建议：同一 URL 至少间隔 5 分钟再提交、只在内容真的变了才提交、不要重复提交没变的 URL（来源：indexnow.org/faq + ecomexperts 交叉验证）
7. **IndexNow key 文件**：必须在网站根目录放一个 `<key>.txt` 纯文本文件，内容就是 key 本身。403/429 错误多半是 key 文件没放对或格式错（来源：indexnow.org/documentation）
8. **Sitemap 不是魔法子弹**：Google 主要靠内部链接和爬取发现 URL，sitemap 只是辅助。"Couldn't fetch" 有时是 Google 后端 backlog 积压，不一定是我们的问题——等几周可能自己变好（来源：Google 官方帮助论坛 + sitemapr 交叉验证）
9. **"Crawled – currently not indexed" = 质量判决**：Google 爬了但决定不收，常见原因：内容太薄（<300 词）、和站内其他页重复、模板化页面（tag 归档、faceted nav）。我们的 156 个 /blog/tag/ 薄内容页正好命中这个（来源：sitemapr + dev.to 交叉验证）
10. **"Discovered – currently not indexed" = 爬取预算/优先级问题**：Google 知道 URL 存在但还没爬，通常是新站/大站爬取预算不足。解决：加强内链、提交 IndexNow（Bing）、等（来源：sitemapr）
11. **Sitemap 大小限制**：单个 sitemap 最多 50,000 个 URL 或 50MB（压缩后），超过必须用 sitemap index 拆分。我们 700+ URL 远没到，但要注意别无限加（来源：Google 官方 sitemap 文档）
12. **Noindex + sitemap 冲突**：URL 在 sitemap 里但页面有 noindex，Google 不会索引。这是自相矛盾的信号。我们给 /blog/tag/ 加 noindex 后，必须同时从 sitemap 里排除这些 URL（来源：sitemapfixer + searchconsoletools 交叉验证）
13. **GSC sitemap 状态速查**：
   - "Couldn't fetch"：robots.txt 拦了 / 路径错 / manual action
   - "Success, discovered=0"：XML 格式错 / BOM / 相对路径 / http-https 不匹配
   - "Success, discovered count 远低于真实"：sitemap 超 50,000 被截断
   - "Success, count 对但 Pages 报告空"：URL 不是 canonical / 返回 404 / 跨 property（来源：aitoolsguidebook + sitemapr 交叉验证）
14. **URL Inspection API 返回字段**：verdict（PASS/PARTIAL/FAIL）、indexStatusResult（isIndexable、robotsTxtState、canonicalLink、richResults）。适合抽样 50-100 个关键 URL 查索引状态，不是全站 700 个（来源：Google 官方 OpenAPI + Screaming Frog）
15. **新站索引节奏**：新站 700 页面被 Google 全索引需要 2-6 个月，急不来。我们能做的：① 内链铺满 ② sitemap 提交 ③ IndexNow 帮 Bing ④ 内容质量（不薄不重复）⑤ 不要反复提交没变的 URL。"为什么不收录" 多半是内容薄/重复，不是技术问题（来源：综合 Google 官方 + sitemapr）

**落地计划（下次迭代直接用）：**
- P1-INDEX-001：用 URL Inspection API 抽样 50 个关键 URL（首页 + 10 个工具页 + 10 篇文章 + 10 个分类），不超 2000 QPD 配额。不做全站 700 个。
- P1-INDEX-002：给 /blog/tag/ 加 noindex 后，同步从 sitemap.ts 排除 /blog/tag/*，避免 noindex+sitemap 矛盾信号。
- P1-INDEX-003：IndexNow 只在新文章发布/工具页更新时提交，不重复提交旧 URL；确认根目录有 <key>.txt 文件。
- P2-INDEX-004：不要用 Google Indexing API 提交普通文章页（off-label）。Google 收录靠内链+sitemap+时间。
- P2-INDEX-005：监控 GSC "Crawled – currently not indexed" 数量，如果 tag 页多了就扩写 tag 页内容或直接 noindex+sitemap 排除。


---

## [2026-09-20] 学习主题：GitHub Actions 自动化最佳实践（缓存/定时/并发/Secrets）

**来源（官方/权威）：**
- https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching （GitHub 官方缓存文档，2026-09-10）
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax （GitHub 官方 workflow 语法，2026-09-19）
- https://docs.github.com/en/actions/reference/limits （GitHub 官方 Actions 限制）
- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions （官方安全加固）
- https://softwaretestpilot.com/blog/automation-testing/github-actions-schedule-cron-guide-2026 （2026 cron 实战指南）

**15个知识点：**
1. **setup-node@v4 自动缓存**：`actions/setup-node@v4` 加 `cache: 'npm'` 就自动缓存 ~/.npm，不需要手写 actions/cache。pnpm/yarn 也支持 `cache: 'pnpm'/'yarn'`（来源：GitHub 官方 Node.js 构建文档）
2. **手写 actions/cache@v4 结构**：`key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}` + `restore-keys:` 前缀用于部分匹配（来源：GitHub 官方 dependency-caching）
3. **缓存 key 必须含 lockfile hash**：用 `hashFiles('**/package-lock.json')` 而不是固定字符串，依赖变了缓存自动失效，不会用到旧依赖（来源：GitHub 官方）
4. **🚨 定时任务默认 UTC**：`on.schedule.cron` 默认按 UTC 解释。新版 GitHub Actions 支持 `timezone: 'Asia/Shanghai'` 字段（IANA 时区），不用自己换算（来源：GitHub 官方 workflow-syntax）
5. **最短间隔 5 分钟**：cron 不能比 5 分钟更频繁。我们的 uptime-monitor 10 分钟触发合规（来源：GitHub 官方）
6. **🚨 定时任务跑在默认分支最新 commit**：scheduled workflow 总是跑 main 分支最新代码，不是触发那一刻的 commit。改 workflow 本身必须 merge 到 main 才生效（来源：GitHub 官方）
7. **🚨 60 天无 commit 静默停用**：仓库 60 天没有新 commit，定时 workflow 会被 GitHub 静默禁用，需要手动去 Actions 页启用。这是我们之前收到"workflow 不跑"邮件的常见原因（来源：softwaretestpilot + GitHub 官方）
8. **无内置 jitter**：多个 cron 同时触发会撞在一起。我们的定时任务要错开分钟数（如 01:15/03:15/05:15），不要都在整点（来源：softwaretestpilot 2026）
9. **timeout-minutes 默认 360（6小时）**：长任务要显式设 `timeout-minutes: 30` 防止卡死。我们的审计脚本如果跑超过 30 分钟要单独设（来源：GitHub 官方 workflow-syntax）
10. **🚨 concurrency 并发控制**：`concurrency: { group: monitor, cancel-in-progress: true }` 防止上一轮没跑完下一轮又启动。定时监控任务必须加，否则会叠跑（来源：GitHub 官方 workflow-syntax）
11. **Job matrix 最大 256 jobs/run**：自动化测试矩阵别超 256（来源：GitHub 官方 limits）
12. **Free 并发 20 jobs**：免费账户同时最多 20 个 job 在跑，多了排队（来源：GitHub 官方 limits）
13. **Secrets 绝不硬编码**：YAML 里用 `${{ secrets.QQ_EMAIL_AUTH }}`，不要写死。泄露的 secret 立刻 rotate（来源：GitHub 官方 security-hardening）
14. **Self-hosted runner 队列超时**：job 排队超 24 小时会失败；runner 60 秒没接单会 re-queue。我们用 GitHub-hosted runner 不涉及（来源：GitHub 官方 self-hosted runners）
15. **Workflow 队列上限**：每仓库 10 秒内最多 500 个 workflow run 排队，超过直接 fail。我们定时任务频率低不会撞（来源：GitHub 官方 limits）

**落地计划（下次迭代直接用）：**
- P1-CI-001：给所有 .github/workflows/*.yml 加 `concurrency: { group: ${{ github.workflow }}, cancel-in-progress: true }`，防止定时任务叠跑。
- P1-CI-002：检查 uptime-monitor.yml / index-monitor.yml 有没有 `timeout-minutes`，没有就加 `timeout-minutes: 5`。
- P1-CI-003：给 setup-node 步骤加 `cache: 'npm'`，去掉手写 actions/cache（如果有的话），简化 YAML。
- P2-CI-004：确认所有 cron 表达式用 `timezone: 'Asia/Shanghai'`，不用自己 UTC 换算。
- P2-CI-005：在 iteration_log 里记录"60 天无 commit 会静默禁用 workflow"，提醒下次超过 60 天没发版时去 Actions 页手动启用。


---

## [2026-09-20] 学习主题：Core Web Vitals 2026 完整指南（LCP/INP/CLS 阈值与优化）

**来源（官方/权威）：**
- https://web.developers.google.cn/articles/defining-core-web-vitals-thresholds （Google web.dev 官方阈值定义）
- https://developers.google.com/search/docs/appearance/core-web-vitals （Google Search 官方 CWV 文档，2025-12-18）
- https://codelabs.developers.google.cn/understanding-inp （Google 官方 INP Codelab，2026-03-28）
- https://web.developers.google.cn/articles/optimize-cls （Google 官方 CLS 优化）
- https://www.corewebvitals.io/core-web-vitals/cumulative-layout-shift/fix-and-identify （corewebvitals.io 权威）
- https://peoplearegeek.com/inp-optimization-2026/ （INP 实战案例，2026-06-05）

**15个知识点：**
1. **CWV 2026 阈值（p75 分位）**：
   - LCP：≤2.5s 良好 / 2.5-4s 需改进 / >4s 差
   - INP：≤200ms 良好 / 200-500ms 需改进 / >500ms 差
   - CLS：≤0.1 良好 / 0.1-0.25 需改进 / >0.25 差
   （来源：Google 官方阈值文档 + developers.google.com 交叉验证）
2. **INP 2024年3月替代 FID**：INP 测量页面上所有交互（点击/输入/按键），取最差的那次；FID 只测第一次交互。INP 更严格（来源：Google 官方 + pauld.fr 交叉验证）
3. **INP = input delay + processing + presentation**：input delay（主线程被占住时用户点击排队）通常占大头。不是你的 event handler 慢，而是主线程正在跑别的长任务（来源：Google Codelab 官方）
4. **🚨 长任务 >50ms 阻塞主线程**：如果用户在长任务执行期间点击，input delay 直接跳到几百 ms。优化 INP 本质是优化主线程空闲度（来源：Google Codelab + scaled2c 交叉验证）
5. **拆分长任务**：`scheduler.yield()`（Chrome 115+）或 `setTimeout(fn, 0)` 把大同步函数切成小块，每块之间让浏览器响应输入。这是 INP 优化最有效的单一手段（来源：peoplearegeek 实战 + scaled2c 交叉验证）
6. **LoAF（Long Animation Frames API）**：新诊断 API，能精确告诉你哪段 JS 在交互期间导致了 jank。Chrome DevTools 已集成（来源：webperfclinic 2026）
7. **测量用 web-vitals.js**：`npm i web-vitals`，`onINP()/onLCP()/onCLS()` 回调上报到 RUM。不要只靠 Lighthouse 实验室数据（来源：Google 官方 + dev.to 交叉验证）
8. **CLS = 意外布局偏移**：只算用户没交互时的元素移动。用户主动滚动/点击导致的移动不算（来源：Google 官方 optimize-cls）
9. **🚨 CLS 第一修复**：所有 img/video/iframe 必须设 width 和 height 属性。现代浏览器用这俩属性自动算 aspect-ratio 预留空间（来源：Google 官方 + corewebvitals.io 交叉验证）
10. **CSS aspect-ratio**：动态内容占位（如广告位、骨架屏）用 `aspect-ratio: 16/9` 预留，不要不设高度（来源：Google 官方）
11. **font-display 对 CLS 的影响**：
    - `swap`：先显示 fallback 字体，字体加载后替换 = 可见 reflow，CLS 高
    - `block`：文字隐藏最多 3 秒，然后替换 = 中等 CLS
    - `optional`：字体已缓存才用，否则一直用 fallback = **零 CLS**（推荐用于次要字体）
    （来源：wicked-seo + web.dev 交叉验证）
12. **🚨 动态插入内容到现有内容上方 = CLS 杀手**：通知条、cookie 横幅、广告 banner 不要动态插入把现有内容往下推。要么预留固定高度容器，要么用 `position: fixed` 悬浮（来源：Google 官方 optimize-cls）
13. **LCP 元素识别**：LCP 通常是最大的图片（hero 图）或最大的标题块。用 DevTools Performance 面板找 LCP 元素，只优化那一个，不要全站瞎优化（来源：Google 官方）
14. **content-visibility: auto**：首屏外的 section 加这个属性，浏览器渲染时跳过它们，LCP 更快。滚到附近再渲染（来源：dev.to 交叉验证）
15. **CWV 排名影响**：CWV 是 Google 搜索排名因素之一，但不是唯一。内容质量、反向链接、相关性更重要。CWV 差会"拖后腿"，CWV 好不会"直接排上去"（来源：Google Search 官方 + ankitseo 交叉验证）

**落地计划（下次迭代直接用）：**
- P1-PERF-INP-001：在 layout.tsx 加 web-vitals.js 上报（onINP/onLCP/onCLS），数据打到 Umami 或自建 endpoint，不再只靠 Lighthouse。
- P1-PERF-CLS-002：审计所有 img 标签缺 width/height 的，批量补上；next/image 迁移后自动解决。
- P2-PERF-FONT-001：检查 next/font 配置，次要字体用 `display: 'swap'` 配合 `adjustFontFallback: true`（Next.js 默认开），关键字体接受小 CLS。
- P2-PERF-CLS-003：检查 cookie 横幅/通知条是否动态插入把内容往下推，改成固定高度预留或 fixed 悬浮。
- P2-PERF-LCP-002：在首页/工具详情页用 DevTools 找 LCP 元素，针对性加 priority+fetchpriority=high（对应之前 P1-PERF-LCP-001）。


---

## [2026-09-26] Next.js Metadata API与Canonical标签最佳实践（12知识点）

**学习背景**：第102轮修复了3个缺少canonical的页面（subcategory/top-ai-tools-by-traffic/submit），系统学习Metadata API确保后续不再遗漏。

**知识点1：Next.js有两种Metadata定义方式——静态metadata对象和动态generateMetadata函数**。固定页面（首页、about）用`export const metadata: Metadata = {...}`；动态路由（blog/[slug]、tools/[slug]、subcategory/[slug]）必须用`export async function generateMetadata({ params })`，因为标题/描述/canonical都依赖params。两者不能同时在同一文件使用。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata）

**知识点2：canonical必须放在alternates.canonical字段中，不能放在metadata顶层**。正确写法：`alternates: { canonical: "https://www.aitoolcrux.com/subcategory/voice-generators" }`。Next.js会自动渲染为`<link rel="canonical" href="..."/>`。写在顶层不会被识别。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata + https://nextjs.org/docs/app/building-your-application/optimizing/metadata）

**知识点3：Client Component不能直接export metadata——必须通过layout.tsx或父Server Component提供**。submit/page.tsx是"use client"组件，无法export metadata。解决方案：在同目录创建layout.tsx（Server Component），在其中export metadata，children渲染client组件。这是Next.js App Router的标准模式。（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata + https://nextjs.org/learn/dashboard-app/adding-metadata）

**知识点4：Metadata沿路由段继承和合并——layout的metadata会被子page的metadata合并，子级优先**。app/layout.tsx定义的metadataBase和默认title会被所有页面继承。子页面可以覆盖title/description/canonical等字段。如果子页面不设canonical，不会继承父级的canonical（canonical是页面级的，必须每页单独设置）。（来源：https://nextjs.org/docs/app/building-your-application/optimizing/metadata）

**知识点5：Google要求canonical使用绝对URL（含https://+域名），不能用相对路径**。正确：`https://www.aitoolcrux.com/tools/midjourney`；错误：`/tools/midjourney`。Next.js的metadataBase可以设置基础URL，然后canonical写相对路径会自动拼接，但显式写绝对URL更安全。（来源：https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls + https://getviralseo.com/articles/canonical-tags-and-canonicalization-the-complete-seo-guide-for-2026）

**知识点6：canonical指向的页面必须返回200且可索引（不能是noindex/404/重定向）**。如果canonical指向一个noindex页面或404，Google会忽略该canonical标签。submit页面设置了noindex+canonical指向自己——这是合理的（告诉Google这是规范URL但不要索引）。（来源：https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls + https://lafactory.online/canonical-tags-duplicate-content-seo-guide/）

**知识点7：同一页面不能有多个canonical标签——Google会全部忽略**。常见原因：插件冲突、layout和page都设了canonical、SSR和CSR各渲染一个。Next.js的Metadata API会自动去重，但如果用了第三方SEO插件（如next-seo）同时手动写metadata，可能产生重复。AIToolCrux只用原生Metadata API，无此风险。（来源：https://screpy.com/blog/how-to-fix-duplicate-content-with-canonical-tags/ + https://www.overthetopseo.com/canonical-tags-definitive-guide-duplicate-content/）

**知识点8：generateMetadata中使用fetch会触发动态渲染（blocking-prerender-metadata-runtime警告）**。如果generateMetadata里fetch了外部数据，Next.js无法在构建时预渲染该页面。解决方案：用generateStaticParams预生成所有params，或从本地JSON导入数据（AIToolCrux的做法——从data/*.json导入，不触发动态渲染）。（来源：https://nextjs.org/docs/messages/blocking-prerender-metadata-runtime）

**知识点9：noindex页面的canonical应指向自己，不要指向其他可索引页面**。常见错误：给noindex页面设置canonical指向首页，这会告诉Google"这个页面的规范版本是首页"，导致该页面内容被合并到首页。正确做法：noindex页面的canonical指向自己，robots设为{ index: false, follow: true }。（来源：https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls + https://surferseo.com/blog/canonical-tags-in-seo/）

**知识点10：sitemap.xml中的URL应与canonical一致——非canonical URL不应出现在sitemap中**。如果sitemap包含了canonical指向其他页面的URL，Google会困惑。AIToolCrux的sitemap.ts应确保只输出每个页面的规范URL。（来源：https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls + https://www.overthetopseo.com/canonical-tags-duplicate-content-guide/）

**知识点11：内部链接应使用canonical URL——不要链接到带参数或旧格式的URL**。如果内链指向`/blog/category/writing`（已301重定向到`/blog/category/ai-writing`），虽然重定向会传递权重，但增加了跳转延迟。最佳实践：内链直接用最终canonical URL。（来源：https://screpy.com/blog/how-to-fix-duplicate-content-with-canonical-tags/ + https://getviralseo.com/articles/canonical-tags-and-canonicalization-the-complete-seo-guide-for-2026）

**知识点12：Metadata字段速查表——AIToolCrux每页应包含的最小SEO元数据**：title（≤60字符）、description（≤155字符）、alternates.canonical（绝对URL）、openGraph（title/description/type/image）、robots（默认index/follow，submit等页面设noindex）。工具页和文章页还应加JSON-LD结构化数据（但FAQPage已在2026年5月弃用）。（来源：https://nextjs.org/docs/app/api-reference/functions/generate-metadata + 综合Google Search Central文档）

**落地计划（下次迭代执行）**：
1. 知识点3（Client Component metadata模式）→ 任务P1-SEO-METADATA-AUDIT：扫描所有"use client"的page.tsx，检查是否有对应layout.tsx提供metadata，缺失的补建
2. 知识点4+7（metadata继承+重复canonical检查）→ 任务P1-SEO-CANONICAL-AUDIT：用脚本扫描所有29个page.tsx+layout.tsx，确认每页恰好一个canonical，无重复无遗漏
3. 知识点10（sitemap与canonical一致性）→ 任务P1-SEO-SITEMAP-CANONICAL：检查app/sitemap.ts输出的URL是否全部为canonical URL，排除noindex页面
4. 知识点11（内链用canonical URL）→ 任务P1-SEO-INTERNAL-LINKS-CLEAN：扫描文章content中的内链，替换为重定向前的旧URL为最终canonical URL
5. 知识点12（metadata最小集）→ 任务P1-SEO-METADATA-COMPLETENESS：写脚本检查每页是否都有title+description+canonical+OG，缺失的列出清单批量补全


---

## [2026-09-26] Next.js Streaming SSR与Suspense边界深度实战（12知识点）

**学习背景**：AIToolCrux为纯SSG站点，部分页面（工具列表、搜索、对比）数据量大，首屏渲染慢。系统学习Streaming+Suspense评估是否可改善感知性能。

**知识点1：Streaming是服务器逐步发送HTML片段的技术，不需要等整页渲染完成**。传统SSR：服务器等所有数据fetch+组件渲染完成后一次性发送HTML。Streaming：服务器先发静态shell（header/nav/loading骨架），数据就绪的组件逐个以HTML chunk流式发送，客户端逐步替换。核心收益：TTFB更快、LCP改善、用户感知速度提升。（来源：https://nextjs.org/docs/app/guides/streaming + https://nextjs.org/docs/app/getting-started/fetching-data）

**知识点2：loading.tsx是页面级Streaming的约定文件，自动包裹page.tsx在Suspense边界中**。在路由段目录创建loading.tsx，Next.js自动将其作为该段page的fallback。用户导航到该路由时，立即显示loading UI，页面内容流式加载完成后自动替换。loading.tsx嵌套在layout内，不会替换layout内容。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/loading + https://nextjs.org/learn/dashboard-app/streaming）

**知识点3：Suspense边界提供组件级细粒度Streaming控制，比loading.tsx更灵活**。`import { Suspense } from "react"`，将异步组件包裹在`<Suspense fallback={<Skeleton />}>`中。边界外的内容立即渲染，边界内的组件数据就绪后流式注入。可在同一页面放置多个独立Suspense边界，各自独立加载互不阻塞。（来源：https://nextjs.org/docs/app/guides/streaming + https://react.dev/reference/react/Suspense）

**知识点4：多个Suspense边界并行流式渲染，按数据就绪顺序逐个显示**。如果页面有3个异步组件（文章列表、热门工具、分类导航），各自包裹独立Suspense后，哪个数据先返回就先显示哪个，不会被最慢的那个阻塞。这比loading.tsx整页loading更优——用户可以先看到部分内容。（来源：https://nextjs.org/docs/app/guides/streaming + https://react.dev/reference/react-dom/server/renderToReadableStream）

**知识点5：Selective Hydration（选择性水合）是Streaming的配套机制——React优先水合用户交互的组件**。Streaming发送HTML后，React在客户端按优先级水合：用户正在点击/交互的组件优先水合，其他组件后台水合。这确保页面可交互时间（TTI）不受非关键组件阻塞。Next.js App Router默认启用。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/loading + https://react.dev/reference/react/Suspense）

**知识点6：Streaming对SSG站点的影响——SSG在构建时预渲染完整HTML，Streaming主要影响动态路由和导航**。AIToolCrux当前为纯SSG（构建时生成所有页面HTML），首屏加载不受Streaming影响（HTML已完整）。Streaming主要改善：①客户端导航时的loading体验（路由切换不白屏）②动态路由（如搜索结果页）的首字节时间。对纯SSG页面，loading.tsx改善的是路由间导航体验而非首屏。（来源：https://nextjs.org/docs/app/getting-started/fetching-data + https://nextjs.org/docs/app/guides/building）

**知识点7：Bots和爬虫访问时，Next.js会等待完整渲染后再发送HTML，而非流式发送**。Next.js检测到User-Agent为爬虫（Googlebot等）时，会等待所有Suspense边界resolve后发送完整HTML，确保爬虫拿到完整内容。这意味着Streaming不会影响SEO——爬虫看到的是完整页面。这是Next.js内置的行为，无需额外配置。（来源：https://nextjs.org/docs/app/getting-started/fetching-data + https://nextjs.org/docs/app/guides/streaming）

**知识点8：error.tsx与loading.tsx配对使用——Streaming过程中组件报错时显示error UI而非白屏**。error.tsx必须是Client Component（"use client"），自动包裹子路由段在错误边界中。当Suspense内的异步组件渲染失败时，显示error.tsx的fallback。最佳实践：每个有loading.tsx的路由段都配error.tsx，提供retry按钮。（来源：https://nextjs.org/docs/app/api-reference/file-conventions/error + https://nextjs.org/learn/dashboard-app/error-handling）

**知识点9：Async Server Component可以直接在Suspense中使用，不需要useEffect**。Server Component中可以`async function MyComponent() { const data = await fetchData(); return ... }`，包裹在Suspense中后，Next.js自动处理数据fetch+流式渲染。这是App Router的核心优势——数据获取和渲染统一在Server端，不需要客户端loading state管理。（来源：https://nextjs.org/docs/app/guides/streaming + https://react.dev/reference/rsc/server-components）

**知识点10：Streaming与PPR（Partial Prerendering）的关系——Suspense边界是PPR的静态/动态分界线**。PPR在构建时预渲染静态shell（Suspense边界外的内容），请求时动态渲染Suspense边界内的内容并流式注入。Suspense边界定义了"静态部分结束、动态部分开始"的位置。AIToolCrux若启用PPR，工具页的header/sidebar静态预渲染，工具详情数据动态流式加载。（来源：https://nextjs.org/docs/app/glossary + https://nextjs.org/docs/app/getting-started/cache-components）

**知识点11：use() API可在Client Component中读取Promise，配合Suspense实现客户端流式数据**。`import { use } from "react"`，`const data = use(promise)`会在Promise resolve前Suspend。与Server端启动fetch、Client端use()读取的模式配合，实现"服务器启动请求→流式HTML→客户端读取结果"。适用于需要客户端交互但数据可在Server端预取的场景。（来源：https://react.dev/reference/react/use + https://react.dev/reference/rsc/server-components）

**知识点12：AIToolCrux适用场景评估——当前SSG架构下Streaming的实际收益有限，优先改善路由导航loading**。当前533个工具页+107篇文章均为SSG，首屏HTML完整。Streaming的收益场景：①为/blog、/tools列表页添加loading.tsx，路由切换时显示骨架屏而非白屏 ②搜索页（/search）改为动态路由+Suspense，搜索结果流式加载 ③对比页（/compare）多工具数据并行Suspense。不建议为已SSG的详情页改动态渲染——会丧失SSG的SEO和性能优势。（来源：综合Next.js Streaming指南+AIToolCrux架构分析）

**落地计划（下次迭代执行）**：
1. 知识点2+8（loading.tsx+error.tsx）→ 任务P1-PERF-LOADING-SKELETON：为/blog、/tools、/category列表页创建loading.tsx骨架屏和error.tsx错误边界，改善路由导航体验
2. 知识点3+4（多Suspense并行）→ 任务P1-PERF-SEARCH-STREAMING：将/search页面改为动态路由，搜索结果用Suspense包裹，输入框和筛选器立即显示，结果流式加载
3. 知识点6+12（SSG与Streaming权衡）→ 任务P1-PERF-ARCHITECTURE-REVIEW：评估哪些页面适合从SSG改为PPR/动态，制定迁移优先级（搜索页>对比页>列表页>详情页保持SSG）
4. 知识点7（爬虫完整HTML）→ 验证任务：确认所有动态路由页面的爬虫访问返回完整HTML，用Googlebot User-Agent测试
5. 知识点10（PPR与Suspense边界）→ 任务P2-PERF-PPR-ENABLE：在next.config中启用experimental.ppr，为工具详情页定义Suspense边界（静态shell+动态评分区域）
