# 原子操作手册（工具链版 v2.0）

> **核心铁律：能用脚本/API自动化的，AI绝不手动操作。AI只做需要判断、创作、决策的部分。**
> 所有脚本在 `scripts/seo_toolkit/`，调用方式见 `scripts/seo_toolkit/README.md`

---

## 一、关键词挖掘（全自动脚本）

**AI要做的：选种子词 + 判断哪些P0词值得写**
**脚本做的：扩展词、SERP分析、竞争度计算、意图判断、PAA提取、写待办**

```bash
# 调用脚本（从state.json的P0大品牌词列表中选seed）
python scripts/seo_toolkit/keyword_pipeline.py --seed "Claude" --count 15
```

**脚本输出**：`iteration_center/keyword_pipeline.md`
- 优先级排序表（P0/P1/P2 + KD + 低DR站数 + 意图 + 内容类型 + PAA数量）
- P0词详情（含PAA问题、相关搜索）
- 自动写入state.json待办（assigned_to=窗口3）

**AI判断**：从P0词中选1-2个最值得写的，传给写作任务

---

## 二、竞品分析（全自动脚本）

**AI要做的：选搜索词 + 判断哪个竞品结构最值得借鉴**
**脚本做的：找竞品、批量抓取H1/H2/H3/表格/字数、提取共性模板**

```bash
python scripts/seo_toolkit/competitor_pipeline.py --keyword "Claude vs ChatGPT" --count 3
```

**脚本输出**：
- `iteration_center/competitor_templates.md`（高频H2、高频表格列名、平均字数、推荐结构）
- `iteration_center/competitor_analysis/{domain}.json`（每个竞品详细结构）

**AI判断**：综合竞品结构，确定本文的H2大纲

---

## 三、用户痛点挖掘（全自动脚本）

**AI要做的：选关键词 + 判断哪些痛点最痛**
**脚本做的：搜索Reddit帖子、抓取帖子内容和高赞评论、搜索G2评论、提取PAA、分类痛点**

```bash
python scripts/seo_toolkit/painpoint_pipeline.py --keyword "Claude"
```

**脚本输出**：`iteration_center/user_painpoints/{keyword}_summary.md`
- 核心痛点（按频率排序，每种痛点附Reddit帖子例子）
- Google PAA问题（直接用作FAQ）
- 高赞Reddit帖子详情
- G2/Capterra评论线索

**AI判断**：把最痛的3个痛点融入文章的Quick Answer和Key Takeaways

---

## 四、内容Brief生成（AI创作）

**AI要做的：整合前三步输出，生成Brief**
**输入**：keyword_pipeline.md + competitor_templates.md + user_painpoints/

**Brief模板（AI必须严格按此生成）**：
```
# Brief: {关键词}
- 目标关键词: {keyword}
- 内容类型: {对比页/评测页/替代方案页/场景列表页}
- 标题: {数字}+{年份}+{明确利益点}，<60字符
- Meta description: 150字，含CTA
- Quick Answer: 280-320字符，直接给结论
- Key Takeaways: 3-5条
- H2大纲: {参考竞品高频H2，8-10个}
- 必须包含: 对比表、分场景推荐、Who Should Look Elsewhere、How We Tested、FAQ≥5、定价计算、缺点
- 内链目标: 3篇相关文章slug
- 联盟链接: 2个（对比表+Final Verdict）
- 截图需求: 3张（首页/功能/定价）
```

---

## 五、文章写作（AI创作）

**AI要做的：按Brief写正文，逐节达到字数要求**
**硬规则**：
- 总字数2500-4000词
- 100%英文，无中文
- 每节有具体数字、具体例子，不写空话
- 每个推荐工具至少列2个缺点
- 定价有真实成本计算（月费×12）
- FAQ用PAA问题，每个回答50-80词
- 用Python写入posts.json（禁止手动编辑JSON）

**写入posts.json的Python代码**：
```python
import json
with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)
posts.append({
    "slug": "...", "title": "...", "content": "...",
    "quickAnswer": "...", "keyTakeaways": [...],
    "internalLinks": [...], "affiliateLinks": [...],
    "publishedAt": "2026-09-28", "hasRealScreenshots": True
})
with open("data/posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
```

---

## 六、截图获取（全自动脚本）

**AI要做的：确认工具官网URL**
**脚本做的：Playwright批量截3张图（首页/定价/功能），自动WebP优化**

```bash
python scripts/seo_toolkit/screenshot_bot.py --url https://claude.ai --tool claude
```

**脚本输出**：`public/screenshots/claude/homepage.webp`、`pricing.webp`、`features.webp`

**AI验证**：检查3张图都存在且<300KB，失败则手动补充

---

## 七、质量门检查（全自动脚本）

**AI要做的：修复不达标项，直到15/15通过**
**脚本做的：15项逐项检查，列出具体问题和修复建议**

```bash
python scripts/seo_toolkit/quality_gate.py --slug {文章slug}
```

**15项检查**：
1. 字数2500-4000
2. Quick Answer 280-320字符
3. Key Takeaways≥3
4. 有对比表
5. 有分场景推荐
6. 有Who Should Look Elsewhere
7. 有How We Tested
8. FAQ≥5
9. 定价有真实计算
10. 诚实说缺点
11. 有Last updated
12. 内链≥3
13. 联盟链接≥2
14. 真实截图≥3
15. 100%英文

**不通过→AI修复→重新检查，直到15/15通过才允许发布**

---

## 八、提交发布（全自动脚本）

**AI要做的：确认文章已通过质量门**
**脚本做的：tsc检查+git add+commit+pull rebase+push+Vercel等待+线上验证+state.json更新**

```bash
python scripts/seo_toolkit/publisher.py --slug {文章slug} --message "feat(content): add article"
```

**脚本输出**：
- tsc检查结果
- commit hash
- 线上HTTP 200验证
- state.json待办状态更新

**AI验证**：确认线上页面可访问，内容完整

---

## 九、GSC数据分析（全自动脚本）

**AI要做的：无（全自动）**
**脚本做的：解析最新GSC报告→识别3类问题页面→生成优化建议→写入state.json待办**

```bash
python scripts/seo_toolkit/gsc_pipeline.py
```

**脚本输出**：
- `iteration_center/gsc_analysis_{日期}.md`
- 自动写入state.json待办（高曝光低CTR→窗口1，排名11-20→窗口3）

**3类问题页面**：
1. 高曝光>100但CTR<1% → P0 CTR优化（窗口1）
2. 排名11-20 → P1内容增强（窗口3）
3. 排名1-3但CTR<2% → P0紧急CTR优化（窗口1）

---

## 十、外链建设（半自动化）

**AI要做的：判断哪些目标值得提交，写外联邮件**
**脚本做的：Serper API批量搜索外链目标**

```python
# Python批量搜索外链目标
import requests, json
queries = [
    "AI tools write for us",
    "AI tools submit article",
    "best AI tools list 2026",
    "AI tools resource page",
]
for q in queries:
    resp = requests.post("https://google.serper.dev/search",
        headers={"X-API-KEY": "db3bbe31d1470d3d4358896851c04030d2e76a6e"},
        data=json.dumps({"q": q, "num": 20}))
    # 提取域名，过滤大站，输出到outreach_targets.md
```

**AI操作**：
- 从目标列表选5个最相关的
- 浏览器打开提交表单，填写提交
- Reddit参与：搜索相关帖子，提供有价值的回答（不硬广）

---

## 十一、技术SEO修复（半自动化）

**AI要做的：读state.json的P0待办，判断修复方案**
**脚本做的：Python扫描问题，批量修复**

**以article-api URL修复为例**：
```python
# Python扫描所有自动生成URL
import json, re
with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)
bad = [p for p in posts if re.match(r'article-api-\d+', p.get("slug",""))]
# 批量重命名slug为有意义的slug
for p in bad:
    p["slug"] = re.sub(r'[^a-z0-9]+', '-', p["title"].lower())[:60]
```

**AI操作**：
- 修复后tsc验证
- git提交+线上验证
- 更新state.json待办状态

---

## 十二、联盟链接优化（半自动化）

**AI要做的：判断哪些链接需要更新，申请新联盟**
**脚本做的：Python扫描所有文章的联盟链接，检查有效性**

```python
# Python扫描联盟链接
import json, re
with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)
for p in posts:
    links = re.findall(r'href="([^"]*(?:ref|affiliate|partner)[^"]*)"', p.get("content",""))
    # 检查每个链接是否有效，记录到monetization_audit.md
```

**AI操作**：
- 失效链接替换为有效联盟链接
- 高流量页面优先优化联盟链接位置
- 新联盟申请：写申请邮件，等待审核

---

## 通用规则

1. **脚本优先**：每次触发先看有没有对应脚本，有就调用，没有才手动
2. **AI只做判断和创作**：数据获取、分析、检查、提交全部自动化
3. **失败重试**：脚本失败时查看错误，修复后重试，最多3次
4. **输出可追溯**：所有脚本输出到iteration_center/，AI读取后再行动
5. **质量门不可跳过**：发布前必须15/15通过，脚本退出码非0则禁止发布
6. **JSON用Python**：所有JSON读写用Python，禁止PowerShell ConvertFrom-Json
7. **待办写state.json**：发现问题/新机会自动写state.json，各窗口只读state.json
