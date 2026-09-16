# 知识库：代码/工程（窗口1）

> 每次完成任务后更新：学到了什么、犯了什么错、积累了什么经验。
> 目的：不重复踩坑。

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
