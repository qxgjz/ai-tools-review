# AIToolCrux SEO工具链完整整合手册 v1.2

**最后更新**: 2026-10-08（新增llmevalkit+opengtm+CrewAI+OpenSEO）
**原则**: 现成工具优先，不重复造轮子，实在不行才写胶水代码
**目标**: 6个窗口+指挥官全部用上所有工具，高质量高效率完成SEO工作

---

## ⚠️ 工具真实状态验证（2026-10-08实测）

> 指挥官职责：每次使用工具前必须验证真实状态，禁止凭手册记忆调用。以下为实测结果。

### ✅ 真实可用的工具

| 工具 | 真实版本 | 验证方式 | 用途 |
|------|---------|---------|------|
| **broken-link-checker** | 0.7.8 | `npx broken-link-checker --version` | 断链审计 |
| **zens-ink** | 1.4.10 | `pip install zens-ink`（刚补装） | 关键词竞争度、搜索意图、SEO审计 |
| **Crawl4AI** | ✅ | `import crawl4ai` | AI网页爬虫 |
| **trafilatura** | ✅ | `import trafilatura` | 网页正文提取 |
| **textstat** | ✅ | `import textstat` | 可读性评分 |
| **openserp** | ✅ | `import openserp` | 多引擎SERP |
| **playwright** | ✅ | `import playwright` | 浏览器自动化 |
| **googleapiclient** | ✅ | `import googleapiclient` | GSC/GA4 API |
| **nltk** | ✅ | `import nltk` | 自然语言处理 |
| **tiktoken** | ✅ | `import tiktoken` | token计数 |
| **rank_bm25** | ✅ | `import rank_bm25` | 相关性排序 |
| **courlan** | ✅ | `import courlan` | URL清洗 |
| **Serper API** | ✅ | GitHub Secret已配置 | Google搜索结果API |
| **GSC API** | ✅ | GitHub Actions已验证 | 搜索控制台数据 |
| **Lighthouse** | ✅ | GitHub Actions | 性能/SEO审计 |
| **llmevalkit** | 6.0.2 | `pip install llmevalkit` | 78指标内容评估+幻觉检测+AI内容检测 |
| **opengtm** | 0.1.0 | `pip install opengtm` | 9模块AEO审计+关键词研究（Google Search grounding，无幻觉） |
| **Chroma** | 1.5.9 | `pip install chromadb` | 向量数据库，38条历史经验语义检索 |

### ❌ 手册写了但实际不可用

| 工具 | 手册写的状态 | 真实状态 | 原因 |
|------|------------|---------|------|
| **OpenSEO** | v0.1.9 ✅运行中 localhost:3001 | ❌未运行 | Docker服务未启动，需手动启动 |
| **playwright-stealth** | 2.0.3 ✅ | ❓未验证 | 需确认是否安装 |
| **patchright** | ✅ | ❓未验证 | 需确认是否安装 |

### 🔄 待评估接入的高星GitHub项目（指挥官主动发现）

| 项目 | Stars | 用途 | 评估状态 |
|------|-------|------|---------|
| **OpenClaw** | 310K+ | AI agent框架，有SEO skills | 已被OpenAI收购，接入复杂，暂缓 |
| **Claude SEO** | 4.9K | 26子技能+19agent+34命令 | 方法论可参考，豆包可借鉴其审计流程 |
| **every-app/open-seo** | 4.3K | 自托管SEO栈+MCP server | 有MCP server，AI agent可直接调用，待评估 |
| **SerpBear** | 2K | 排名追踪 | Docker部署，可替代手动排名检查 |
| **SEONaut** | 717 | 技术SEO审计 | Go语言，Docker部署 |
| **marketingskills** | 33.3K | 最大marketing skills集合 | 待评估哪些skill可复用 |
| **CrewAI** | 52.8K | 多Agent协作框架 | ⚠️脚本已就绪，Python 3.14依赖冲突待解决 |
| **OpenSEO** | 20.5K | 完整SEO套件 | 📋部署指南已写，当前阶段不建议部署（资源占用高） |
| **llmevalkit** | - | 78指标AI内容评估 | ✅已接入，scripts/llmevalkit_toolkit.py |
| **opengtm** | - | AEO审计+关键词研究 | ✅已接入，scripts/opengtm_toolkit.py |

---

## 第一部分：完整工具清单（所有资源盘点）

### 1.1 已安装的SEO平台/服务

| 工具 | 版本/状态 | 访问方式 | 用途 | 负责人 |
|------|----------|---------|------|--------|
| **OpenSEO** | v0.1.9 ✅运行中 | http://localhost:3001 | 全站技术审计、排名追踪、关键词研究、反链分析 | 窗口1+窗口4 |
| **Lighthouse** | v13.4.1 ✅全局安装 | CLI `lighthouse <url>` | 页面性能、SEO、可访问性审计 | 窗口1 |
| **Unlighthouse** | ✅GitHub Actions | `.github/workflows/unlighthouse.yml` | 全站Lighthouse批量扫描 | 窗口1 |
| **GitHub Actions** | 16个workflow ✅ | `.github/workflows/` | CI/CD、GSC拉取、监控、测试 | 全部窗口 |

### 1.2 Python SEO工具库（已pip安装）

| 库 | 版本 | 核心能力 | 用途 | 调用示例 |
|----|------|---------|------|---------|
| **zens-ink** | 1.4.8 | 23个模块 | 关键词竞争度、搜索意图、竞品分析、31项SEO审计、内容矩阵、内容QC | `from zens_ink import kd, search_intent, competitor_gap, site_audit, onpage_audit, content_matrix, content_qc, rank_tracker` |
| **Crawl4AI** | 0.9.3 | AI网页爬虫 | 爬取竞品页面、提取结构化内容、异步并发 | `from crawl4ai import AsyncWebCrawler, BrowserConfig` |
| **trafilatura** | 2.2.0 | 网页正文提取 | 从HTML提取纯文本、元数据、作者、日期 | `import trafilatura; text = trafilatura.extract(html)` |
| **textstat** | 0.7.13 | 20+可读性指标 | Flesch、Coleman-Liau、Dale-Chall等可读性评分 | `import textstat; textstat.flesch_reading_ease(text)` |
| **openserp** | 0.2.6 | 多引擎SERP | Google/Bing/DuckDuckGo搜索结果抓取 | `from openserp import OpenSERP` |
| **playwright** | 最新 | 浏览器自动化 | 截图、交互测试、SPA渲染 | `from playwright.sync_api import sync_playwright` |
| **playwright-stealth** | 2.0.3 | 反检测 | 绕过Cloudflare、反爬检测 | `from playwright_stealth import stealth_sync` |
| **patchright** | 1.62.3 | Playwright增强 | 更强的反检测能力 | `from patchright.sync_api import sync_playwright` |
| **google-api-python-client** | 2.200.0 | Google API全套 | GSC Search Console API、YouTube API等 | `from googleapiclient.discovery import build` |
| **google-analytics-data** | 0.23.0 | GA4官方API | 直接拉GA4实时数据 | `from google.analytics.data_v1beta import BetaAnalyticsDataClient` |
| **courlan** | 1.4.0 | URL清理 | URL规范化、去参数、去追踪 | `import courlan` |
| **rank-bm25** | 0.2.2 | BM25算法 | 关键词相关性排序 | `from rank_bm25 import BM25Okapi` |
| **nltk** | 3.10.3 | NLP工具 | 分词、词性标注、命名实体 | `import nltk` |
| **tiktoken** | 0.14.0 | Token计数 | OpenAI token计数、成本估算 | `import tiktoken` |

### 1.3 API服务（已配置）

| API | 状态 | 用途 | 配置位置 | 调用方式 |
|-----|------|------|---------|---------|
| **Serper API** | ✅已配置 | Google SERP搜索、关键词研究 | 环境变量SERPER_API_KEY | `requests.post('https://google.serper.dev/search', headers={'X-API-KEY': key})` |
| ~~DataForSEO API~~ | ❌已废弃（账号无法验证） | ~~关键词研究、排名追踪、反链、域名概览~~ | .env.local | **改用zens-ink + Serper API替代** |
| **Google Search Console** | ✅通过GitHub Actions | 搜索曝光、点击、排名数据 | gsc-fetch.yml workflow | 每日自动拉取到gsc-ga4-report/ |
| **GA4** | ✅服务账号 | 用户行为、流量来源、转化 | 服务账号JSON | google-analytics-data API |
| **Cloudflare** | ✅GraphQL API | 实时流量、请求数、安全事件 | API Token | GraphQL查询 |
| **GitHub API** | ✅PAT | 代码提交、Issue、Actions | GITHUB_PAT环境变量 | REST API |
| **Vercel API** | ✅Token | 部署、项目配置 | VERCEL_TOKEN | REST API |

### 1.4 项目已有Python脚本（200+，按功能分类）

#### 审计类（直接用，不要重写）

| 脚本 | 大小 | 功能 | 用法 |
|------|------|------|------|
| `scripts/quality_audit.py` | 14KB | 文章质量审计（14项加权检查+A-F评级+自动报告） | `python scripts/quality_audit.py` |
| `real_seo_audit.py` | 22KB | 40+规则SEO审计（基于argus+claude-seo方法论） | `python real_seo_audit.py` |
| `real_geo_aeo_audit.py` | 18KB | GEO/AEO审计（AI搜索可见性检查） | `python real_geo_aeo_audit.py` |
| `real_internal_link_audit.py` | 10KB | 内链审计（基于Thibaultbm方法） | `python real_internal_link_audit.py` |
| `seo_technical_check.py` | 9KB | 技术SEO检查 | `python seo_technical_check.py` |
| `iteration_center/seo_audit.py` | 6KB | 全站技术SEO审计 | `python iteration_center/seo_audit.py` |
| `iteration_center/seo_audit_full.py` | 11KB | sitemap驱动版全站审计 | `python iteration_center/seo_audit_full.py` |
| `iteration_center/health_check.py` | 9KB | 网站健康检查 | `python iteration_center/health_check.py` |
| `audit_deep.py` | 2KB | 深度检查（FAQ结构、图片、章节） | `python audit_deep.py` |
| `content_quality_check.py` | 7KB | 内容质量检查 | `python content_quality_check.py` |
| `iteration_center/pre_commit_check.py` | 3KB | 提交前质量检查 | `python iteration_center/pre_commit_check.py` |

#### 关键词类

| 脚本 | 大小 | 功能 | 用法 |
|------|------|------|------|
| `iteration_center/keyword_miner.py` | 10KB | 关键词机会挖掘 | `python iteration_center/keyword_miner.py` |

#### 修复类（按问题选择）

| 脚本 | 大小 | 功能 |
|------|------|------|
| `fix_seo_batch2.py` | 7KB | OpenSEO审计问题批量修复 |
| `fix_seo_issues_iteration6.py` | 10KB | 深度审计SEO问题修复 |
| `fix_p0_issues.py` | 7KB | P0问题修复 |
| `fix_article_structure.py` | 4KB | 文章结构修复 |
| `fix_dual_h1.py` | 1KB | 双H1修复 |
| `fix_og_tags.py` | 2KB | OG标签修复 |
| `fix_schema.py` | 2KB | Schema结构化数据修复 |
| `fix_title_meta_redirects.py` | 4KB | 标题/Meta/重定向修复 |
| `fix_chinese.py` + `fix_chinese2.py` | 4KB | 中文文本修复 |
| `optimize_titles_desc.py` | 5KB | 标题和描述优化 |
| `optimize_ctr_v2.py` | 1KB | CTR优化 |
| `optimize_affiliate_cta.py` | 4KB | 联盟CTA优化 |
| `optimize_performance.py` | 4KB | 性能优化 |

#### 内容生成类

| 脚本 | 大小 | 功能 |
|------|------|------|
| `generate_real_article.py` | 24KB | 生成真实高质量文章（基于ccforseo/content-brief方法） |
| `generate_perplexity_article.py` | 18KB | 生成Perplexity优化文章 |
| `add_faq_to_articles.py` | 12KB | 批量添加FAQ |
| `add_real_experience.py` | 54KB | Top20工具添加真实用户体验 |
| `add_real_experience_top50.py` | 50KB | Top50工具添加真实用户体验 |
| `add_aeo_geo_optimization.py` | 8KB | AEO/GEO优化 |
| `add_aeo_quick_answer.py` | 7KB | 添加Quick Answer |
| `add_aeo_to_alternatives.py` | 6KB | Alternatives页AEO优化 |
| `add_aeo_to_blog.py` | 6KB | 博客页AEO优化 |
| `add_comparison_schema.py` | 6KB | 添加对比Schema |
| `add_experience_sections.py` | 6KB | 添加体验章节 |
| `add_internal_links.py` | 7KB | 添加内链 |
| `add_related_articles.py` | 5KB | 添加相关文章 |
| `add_utm.py` | 4KB | 添加UTM参数 |
| `generate_llms_full.py` | 7KB | 生成llms.txt |
| `generate_missing_screenshots.py` | 12KB | 生成缺失截图 |
| `publish_drafts.py` | 3KB | 发布草稿 |

#### 部署/验证类

| 脚本 | 大小 | 功能 |
|------|------|------|
| `push_via_api.py` | 6KB | 通过GitHub API推送 |
| `push_iteration_1.py` ~ `push_batch5.py` | 2-5KB | 各批次推送 |
| `commit_iteration_4.py` ~ `commit_*.py` | 1-6KB | 各类提交 |
| `verify_iteration_2.py` ~ `verify_*.py` | 1-5KB | 各类验证 |
| `check_deployment.py` | 1KB | 部署检查 |
| `performance_monitor.py` | 7KB | 性能监控 |
| `submit_indexnow_daily.py` | 3KB | IndexNow提交 |
| `geo_submit.py` | 3KB | GEO自动提交 |

#### CI/CD脚本（.github/scripts/）

| 脚本 | 大小 | 功能 |
|------|------|------|
| `fetch_gsc.py` | 5KB | GSC数据拉取（CI版） |
| `seo_check.py` | 6KB | SEO健康检查（CI版） |
| `uptime_check.py` | 5KB | 可用性+内容完整性监控 |
| `index_monitor.py` | 5KB | Google索引页数追踪 |
| `run_diagnosis.py` | 7KB | 网站优化诊断 |
| `generate_summary.py` | 10KB | 生成优化诊断摘要 |
| `generate_context.py` | 6KB | 生成上下文（CI版） |
| `execute_optimizations.py` | 10KB | 自动执行优化 |
| `create_p0_issues.py` | 7KB | 根据诊断创建GitHub Issue |

### 1.5 GitHub高星项目（可安装/参考）

| 项目 | Stars | 功能 | 状态 | 安装方式 |
|------|-------|------|------|---------|
| **OpenSEO** | 20,045 | 开源Semrush/Ahrefs替代 | ✅已安装运行 | Docker/Cloudflare Workers |
| **OpenClaw** | 157K | AI agent for SEO，自动化关键词/竞品/内容/审计 | ⚠️待评估 | pip install openclaw |
| **Claude SEO** | 4,900+ | 18并行AI agent审计，0-100分 | ⚠️待评估 | Claude Code skill |
| **marketingskills** | 33.3K | 最大marketing skills集合（含seo-audit/ai-seo） | ⚠️待评估 | Claude Code skill |
| **SerpBear** | 2,000 | 排名追踪 | ⚠️待评估 | Docker |
| **SEONaut** | 717 | 技术SEO和站点审计 | ⚠️待评估 | Docker |
| **searchstack-aeo** | - | AEO/GEO/SEO监控，22命令，9API | ⚠️待评估 | pip install |
| **answerlint** | - | AEO/GEO审计CLI，12项检查 | ⚠️待评估 | npm install -g answerlint |
| **seo-autopilot** | 1.0.1 | 多租户SEO自动化，50+检测器，GEO审计 | ⚠️待评估 | pip install seo-autopilot |
| **seo-agent** | 0.4.0 | 轻量级技术SEO审计CLI | ⚠️待评估 | pip install seo-agent |

---

## 第二部分：工具链架构（每个环节用什么）

### 2.1 完整SEO工作流 → 工具映射

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AIToolCrux SEO工具链架构                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  【数据采集层】                                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ GSC API      │ │ GA4 API      │ │ Cloudflare   │ │ Serper API   │ │
│  │ (每日自动拉取)│ │ (服务账号)   │ │ (GraphQL)    │ │ (SERP搜索)   │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ │
│                                                                           │
│  【分析审计层】                                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ OpenSEO      │ │ zens-ink     │ │ Lighthouse   │ │ Unlighthouse │ │
│  │ (全站审计)   │ │ (31项检查)   │ │ (性能/SEO)   │ │ (全站扫描)   │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │
│  │ quality_audit │ │ real_seo_    │ │ real_geo_    │                   │
│  │ (文章质量)    │ │ audit(40+规则)│ │ aeo_audit    │                   │
│  └──────────────┘ └──────────────┘ └──────────────┘                   │
│                                                                           │
│  【关键词研究层】                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │
│  │ zens-ink kd  │ │ zens-ink     │ │ keyword_miner│                   │
│  │ (竞争度计算)  │ │ search_intent│ │ (机会挖掘)   │                   │
│  └──────────────┘ └──────────────┘ └──────────────┘                   │
│  ┌──────────────┐ ┌──────────────┐                                    │
│  │ OpenSEO      │ │ Serper API   │                                    │
│  │ (关键词研究)  │ │ (SERP分析)   │                                    │
│  └──────────────┘ └──────────────┘                                    │
│                                                                           │
│  【竞品分析层】                                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │
│  │ Crawl4AI     │ │ trafilatura  │ │ zens-ink     │                   │
│  │ (AI爬虫)     │ │ (正文提取)   │ │ competitor_gap│                  │
│  └──────────────┘ └──────────────┘ └──────────────┘                   │
│                                                                           │
│  【内容生产层】                                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │
│  │ generate_real │ │ textstat     │ │ content_qc   │                   │
│  │ _article      │ │ (可读性)     │ │ (内容QC)     │                   │
│  └──────────────┘ └──────────────┘ └──────────────┘                   │
│  ┌──────────────┐ ┌──────────────┐                                    │
│  │ add_faq/      │ │ add_aeo_*    │                                    │
│  │ add_*系列     │ │ (AEO优化)    │                                    │
│  └──────────────┘ └──────────────┘                                    │
│                                                                           │
│  【发布部署层】                                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │
│  │ GitHub API    │ │ Vercel API   │ │ IndexNow     │                   │
│  │ (提交推送)    │ │ (部署)       │ │ (索引提交)   │                   │
│  └──────────────┘ └──────────────┘ └──────────────┘                   │
│                                                                           │
│  【监控反馈层】                                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │
│  │ GitHub Actions│ │ uptime_check │ │ performance_ │                   │
│  │ (16个workflow)│ │ (可用性监控) │ │ monitor      │                   │
│  └──────────────┘ └──────────────┘ └──────────────┘                   │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 各环节详细工具选择

#### 环节1：数据采集

| 任务 | 首选工具 | 备选工具 | 调用方式 | 输出 |
|------|---------|---------|---------|------|
| GSC数据拉取 | GitHub Actions gsc-fetch.yml | google-api-python-client | 每日自动运行 | gsc-ga4-report/*.md |
| GA4数据分析 | google-analytics-data API | GA4报告文件 | Python脚本 | 真实用户/流量来源/转化 |
| Cloudflare实时数据 | Cloudflare GraphQL API | - | Python脚本 | 实时请求/流量/安全 |
| SERP搜索结果 | Serper API | openserp | `requests.post` | 排名/标题/URL/摘要 |
| 竞品页面爬取 | Crawl4AI | playwright-stealth | `AsyncWebCrawler` | HTML+结构化数据 |
| 网页正文提取 | trafilatura | - | `trafilatura.extract()` | 纯文本+元数据 |

#### 环节2：分析审计

| 任务 | 首选工具 | 备选工具 | 调用方式 | 输出 |
|------|---------|---------|---------|------|
| 全站技术审计 | OpenSEO | zens-ink site_audit | http://localhost:3001 | 988问题分类报告 |
| 40+规则SEO审计 | real_seo_audit.py | seo-agent | `python real_seo_audit.py` | JSON+MD报告 |
| GEO/AEO审计 | real_geo_aeo_audit.py | answerlint | `python real_geo_aeo_audit.py` | AI搜索可见性报告 |
| 内链审计 | real_internal_link_audit.py | zens-ink | `python real_internal_link_audit.py` | 内链结构报告 |
| 文章质量审计 | quality_audit.py | textstat+zens-ink content_qc | `python scripts/quality_audit.py` | 14项评分+A-F评级 |
| 性能审计 | Lighthouse | Unlighthouse | `lighthouse <url>` | 性能/SEO/可访问性评分 |
| 技术SEO检查 | seo_technical_check.py | - | `python seo_technical_check.py` | 技术问题清单 |

#### 环节3：关键词研究

| 任务 | 首选工具 | 备选工具 | 调用方式 | 输出 |
|------|---------|---------|---------|------|
| 关键词竞争度 | zens-ink kd | OpenSEO | `kd.calculate_kd(serp_results)` | KD分数0-100 |
| 搜索意图判断 | zens-ink search_intent | - | `search_intent.classify(keyword)` | informational/commercial/transactional |
| 关键词机会挖掘 | keyword_miner.py | OpenSEO | `python iteration_center/keyword_miner.py` | 机会词清单 |
| SERP分析 | Serper API | openserp | `requests.post` | 前10名结果分析 |
| 竞品内容缺口 | zens-ink competitor_gap | Crawl4AI+trafilatura | `competitor_gap.fetch_sitemap()` | 内容缺口清单 |
| 关键词聚类 | zens-ink content_matrix | rank-bm25 | `content_matrix.generate_matrix()` | 主题矩阵 |

#### 环节4：内容生产

| 任务 | 首选工具 | 备选工具 | 调用方式 | 输出 |
|------|---------|---------|---------|------|
| 文章生成 | generate_real_article.py | AI直接写 | `python generate_real_article.py` | 高质量文章 |
| 可读性检查 | textstat | quality_audit.py | `textstat.flesch_reading_ease()` | 20+指标 |
| 内容QC | zens-ink content_qc | quality_audit.py | `content_qc.check_draft()` | 内容质量评分 |
| FAQ添加 | add_faq_to_articles.py | AI直接写 | `python add_faq_to_articles.py` | 带FAQ的文章 |
| AEO优化 | add_aeo_*.py系列 | - | 对应脚本 | Quick Answer/Key Takeaways |
| 真实体验添加 | add_real_experience*.py | - | 对应脚本 | 真实用户体验章节 |
| 截图生成 | generate_missing_screenshots.py | playwright-stealth | `python generate_missing_screenshots.py` | 工具截图 |
| llms.txt生成 | generate_llms_full.py | - | `python generate_llms_full.py` | llms.txt文件 |

#### 环节5：发布部署

| 任务 | 首选工具 | 备选工具 | 调用方式 | 输出 |
|------|---------|---------|---------|------|
| 代码提交 | GitHub API | git CLI | `push_via_api.py` | commit+push |
| 部署 | Vercel API | GitHub Actions | 自动触发 | 部署完成 |
| 索引提交 | submit_indexnow_daily.py | - | `python submit_indexnow_daily.py` | IndexNow提交 |
| GEO提交 | geo_submit.py | - | `python geo_submit.py` | AI引擎提交 |
| 部署验证 | verify_*.py系列 | - | 对应脚本 | 验证报告 |

#### 环节6：监控反馈

| 任务 | 首选工具 | 备选工具 | 调用方式 | 输出 |
|------|---------|---------|---------|------|
| 可用性监控 | uptime_check.py | GitHub Actions | 每日运行 | 可用性报告 |
| 性能监控 | performance_monitor.py | Lighthouse CI | 定时运行 | 性能趋势 |
| 索引监控 | index_monitor.py | GitHub Actions | 每周运行 | 索引页数趋势 |
| 包大小监控 | bundle-size.yml | - | GitHub Actions | 包大小报告 |
| 安全监控 | codeql.yml + security.yml | - | GitHub Actions | 安全报告 |
| SEO检查 | seo-check.yml | - | GitHub Actions | SEO健康报告 |

---

## 第三部分：6个窗口完整执行手册

### 窗口1：技术SEO修复工程师

**核心职责**: 网站技术SEO问题修复、性能优化、部署验证
**使用工具**: OpenSEO + Lighthouse + zens-ink site_audit + real_seo_audit.py + fix_*.py系列 + GitHub API + Vercel API

#### 每日执行流程（定时任务：0 1,5,13,22 * * *）

**步骤1：运行审计（5分钟）**
```bash
# 1.1 检查OpenSEO最新审计结果
# 访问 http://localhost:3001 查看最新审计报告
# 重点关注：thin-content、heading-order-skip、slow-response、meta-description-too-long

# 1.2 运行real_seo_audit.py（40+规则）
cd C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review
python real_seo_audit.py

# 1.3 运行seo_technical_check.py
python seo_technical_check.py

# 1.4 运行Lighthouse（首页+3个关键页）
lighthouse https://www.aitoolcrux.com --output=json --output-path=lh-home.json
lighthouse https://www.aitoolcrux.com/ranking --output=json --output-path=lh-ranking.json
lighthouse https://www.aitoolcrux.com/blog --output=json --output-path=lh-blog.json
```

**步骤2：分析问题，按优先级排序（3分钟）**
- P0：影响索引/排名的严重问题（noindex错误、404、重定向错误、Schema错误）
- P1：影响用户体验的问题（慢加载、移动端适配、标题过长）
- P2：优化项（内链、图片alt、结构化数据增强）

**步骤3：执行修复（根据问题选择对应脚本）**
```bash
# 按问题类型选择修复脚本：
# - OpenSEO审计问题 → python fix_seo_batch2.py
# - 深度审计问题 → python fix_seo_issues_iteration6.py
# - P0问题 → python fix_p0_issues.py
# - 双H1问题 → python iteration_center/fix_dual_h1.py
# - OG标签问题 → python fix_og_tags.py
# - Schema问题 → python fix_schema.py
# - 标题/Meta问题 → python fix_title_meta_redirects.py
# - 性能问题 → python optimize_performance.py
# - 中文文本问题 → python fix_chinese.py + fix_chinese2.py
```

**步骤4：提交部署（2分钟）**
```bash
# 通过GitHub API提交
python push_via_api.py

# 等待Vercel自动部署（约2-3分钟）
# 验证部署
python verify_deployment.py
```

**步骤5：验证修复效果（3分钟）**
```bash
# 重新运行审计确认问题已修复
python real_seo_audit.py
# 检查对应页面HTTP状态
python check_deployment.py
```

**步骤6：更新state.json（1分钟）**
- 用Python读取iteration_center/state.json
- 将已完成的任务标记为completed
- 添加新发现的问题到next_iteration_focus

---

### 窗口2：外链建设/社区增长专家

**核心职责**: 外链建设、社区推广、品牌提及、合作 outreach
**使用工具**: Serper API + Crawl4AI + trafilatura + zens-ink competitor_gap + Reddit/社区搜索

#### 每日执行流程（定时任务：0 10,16 * * *）

**步骤1：外链机会挖掘（10分钟）**
```python
# 1.1 用Serper API搜索外链机会
import requests
headers = {'X-API-KEY': 'db3bbe31d1470d3d4358896851c04030d2e76a6e'}

# 搜索"AI tools 投稿/guest post"机会
r = requests.post('https://google.serper.dev/search', 
    headers=headers, 
    json={'q': 'AI tools write for us guest post', 'num': 20})

# 搜索"AI工具 推荐/榜单"页面
r2 = requests.post('https://google.serper.dev/search',
    headers=headers,
    json={'q': 'best AI tools list 2026', 'num': 20})

# 搜索Reddit讨论（site:reddit.com）
r3 = requests.post('https://google.serper.dev/search',
    headers=headers,
    json={'q': 'site:reddit.com AI tools recommendation', 'num': 20})

# 1.2 用Crawl4AI爬取目标页面，分析外链机会
from crawl4ai import AsyncWebCrawler
# 爬取竞品的外链来源，找到可复制的链接策略

# 1.3 用zens-ink competitor_gap分析竞品sitemap
from zens_ink import competitor_gap
# 找到竞品有但我们没有的内容类型
```

**步骤2：内容营销/社区推广（15分钟）**
- 在Reddit相关subreddit（r/artificial、r/MachineLearning、r/ChatGPT）找到可参与的讨论
- 在Hacker News、Product Hunt、Indie Hackers找到推广机会
- 撰写有价值的评论（不是硬广），自然提及aitoolcrux.com
- 寻找交叉推广机会（其他AI工具站互换链接）

**步骤3：外链建设执行（20分钟）**
- 给目标网站发送outreach邮件（guest post投稿、资源页收录请求）
- 在可接受的目录站提交网站
- 创建社交媒体资料并链接回网站
- 监控品牌提及（未链接的提及→请求添加链接）

**步骤4：更新state.json和知识库（5分钟）**
- 记录外链建设进展
- 添加新发现的外链机会到待办
- 更新外链知识库

---

### 窗口3：内容生产专家（3个子任务：调研→写作→发布）

**核心职责**: 关键词调研→文章写作→质量检查→发布
**使用工具**: zens-ink(kd/search_intent/competitor_gap) + Serper API + Crawl4AI + trafilatura + textstat + quality_audit.py + generate_real_article.py + add_*.py系列

#### 子任务3a：内容调研（定时任务：0 3 * * *，每天凌晨3点）

**步骤1：关键词挖掘（15分钟）**
```python
import os
os.environ['SERPER_API_KEY'] = 'db3bbe31d1470d3d4358896851c04030d2e76a6e'

# 1.1 从GSC报告中提取高排名低点击词
# 读取 gsc-ga4-report/ 最新文件，找到排名5-20但CTR<1%的词

# 1.2 用zens-ink计算关键词竞争度
from zens_ink import kd, search_intent
# 对每个候选词：
# serp = kd.fetch_serp(keyword)
# kd_score = kd.calculate_kd(serp)
# intent = search_intent.classify(keyword)
# 筛选：KD<40 且 intent=commercial/informational

# 1.3 用keyword_miner.py挖掘机会词
# python iteration_center/keyword_miner.py

# 1.4 用Serper API搜索相关问题（People Also Ask）
# q: "AI tools what/how/why/best"
```

**步骤2：竞品分析（15分钟）**
```python
# 2.1 用zens-ink competitor_gap分析竞品sitemap
from zens_ink import competitor_gap
# gap = competitor_gap.fetch_sitemap('https://www.futurepedia.io/sitemap.xml')
# 找到竞品有但我们没有的内容类型

# 2.2 用Crawl4AI爬取Top3排名页面
from crawl4ai import AsyncWebCrawler
# 爬取目标关键词排名前3的页面

# 2.3 用trafilatura提取正文
import trafilatura
# text = trafilatura.extract(html)
# 分析：字数、结构、FAQ、数据引用、独特角度

# 2.4 用textstat分析竞品可读性
import textstat
# 对比我们的文章和竞品的可读性分数
```

**步骤3：用户痛点挖掘（10分钟）**
```python
# 3.1 用Serper API搜索Reddit讨论
# q: "site:reddit.com AI tool frustration/problem/recommendation"

# 3.2 用Serper API搜索Quora问题
# q: "site:quora.com AI tools"

# 3.3 分析GSC搜索查询中的问题型关键词
# 包含 "what/how/why/can/best/vs" 的查询

# 3.4 整理痛点清单，每个痛点对应一个文章选题
```

**步骤4：生成内容简报（10分钟）**
- 输出：5-10个经过验证的文章选题
- 每个选题包含：目标关键词、KD分数、搜索意图、竞品分析、用户痛点、文章大纲、独特角度
- 写入iteration_center/content_briefs/目录

#### 子任务3b：内容写作（定时任务：0 7 * * *，每天早上7点）

**步骤1：读取内容简报（2分钟）**
- 从iteration_center/content_briefs/读取待写选题
- 按优先级排序（高排名低点击词优先）

**步骤2：文章写作（40分钟，AI直接写）**
- **文章结构标准**（必须包含）：
  1. H1标题（含目标关键词，30-60字符）
  2. Quick Answer（前100字直接回答问题，AEO优化，≤320字符）
  3. Key Takeaways（3-5个要点）
  4. 正文（2000+字，H2/H3层级清晰，不跳级）
  5. How We Tested（真实测试方法论）
  6. FAQ（3-5个问题，含Schema）
  7. 内链（≥3个相关文章/工具页链接）
  8. 外链（≥1个权威来源引用）
  9. 图片（≥1张，含alt文本）

- **写作标准**：
  - 100%英文，针对美国用户
  - 可读性：Flesch Reading Ease ≥ 40
  - 真实数据引用，不编造
  - 独特角度，不与竞品重复
  - 包含具体数字、对比、案例

**步骤3：质量检查（5分钟）**
```bash
# 运行quality_audit.py检查文章质量
python scripts/quality_audit.py
# 检查项：
# - 字数≥2000
# - Quick Answer存在
# - Key Takeaways存在
# - FAQ存在且≥3个
# - How We Tested存在
# - 内链≥3个
# - 图片≥1张
# - Flesch可读性≥40
# - 标题长度30-80
# - 外链≥1个
# 评分<85分的文章必须修改后才能发布
```

**步骤4：AEO/GEO优化（5分钟）**
```bash
# 运行AEO优化脚本
python add_aeo_quick_answer.py  # 添加Quick Answer
python add_aeo_to_blog.py         # 博客页AEO优化
# 确保：
# - 首段≤320字符（AI摘要优化）
# - 包含结构化数据（FAQPage、Article schema）
# - llms.txt已更新
```

#### 子任务3c：内容发布（定时任务：0 11 * * *，每天上午11点）

**步骤1：发布准备（3分钟）**
```bash
# 运行pre_commit_check.py
python iteration_center/pre_commit_check.py
# 检查所有待发布文章是否通过质量门
```

**步骤2：发布文章（5分钟）**
```bash
# 运行publish_drafts.py发布草稿
python publish_drafts.py
# 将[READY]状态的文章写入data/posts.json
```

**步骤3：提交部署（5分钟）**
```bash
# 通过GitHub API提交
python push_via_api.py
# 等待Vercel部署完成
```

**步骤4：索引提交（2分钟）**
```bash
# 运行IndexNow提交
python submit_indexnow_daily.py
# 运行GEO提交
python geo_submit.py
```

**步骤5：验证发布（5分钟）**
```bash
# 验证新文章可访问
python verify_deployment.py
# 检查HTTP 200、标题正确、内容完整
```

---

### 窗口4：数据分析/SEO策略专家

**核心职责**: GSC/GA4数据分析、排名追踪、关键词策略、竞品监控
**使用工具**: GSC API + GA4 API + Cloudflare API + OpenSEO + zens-ink(rank_tracker/content_matrix) + Serper API

#### 每日执行流程（定时任务：0 9,21 * * *，每天9点和21点）

**步骤1：数据拉取（10分钟）**
```python
# 1.1 读取最新GSC报告（GitHub Actions每日自动拉取）
# 读取 gsc-ga4-report/ 最新.md文件
# 关键指标：曝光、点击、CTR、平均排名、Top页面、Top查询

# 1.2 用google-analytics-data API拉GA4实时数据
from google.analytics.data_v1beta import BetaAnalyticsDataClient
# 拉取：真实用户数、流量来源、页面浏览、停留时间、跳出率
# 过滤：排除新加坡Bot（97.5%的流量是Bot）
# 重点关注：Google organic真实用户

# 1.3 用Cloudflare GraphQL API拉实时流量
# 拉取：请求数、独立访客、国家分布、安全事件

# 1.4 检查OpenSEO排名追踪结果
# 访问 http://localhost:3001 查看20+10个关键词的排名变化
```

**步骤2：数据分析（15分钟）**
```python
# 2.1 GSC深度分析
# - 高排名零点击页（排名5-20，CTR<1%）→ 需要优化标题和meta
# - 高曝光低点击查询 → 需要优化SERP展示
# - 排名上升/下降最快的页面 → 分析原因
# - 新获得排名的查询 → 乘胜追击
# - 品牌词vs非品牌词比例

# 2.2 GA4真实用户分析
# - 真实用户来源分布（Google organic/direct/referral/social）
# - 真实用户行为（停留时间、页面/会话、转化率）
# - 高转化页面分析
# - Bot流量过滤（新加坡IP、0秒停留、异常UA）

# 2.3 竞品排名监控
# 用Serper API检查目标关键词的Top10变化
# 监控竞品：futurepedia.io、theresanaiforthat.com、topai.tools等

# 2.4 用zens-ink content_matrix生成主题矩阵
from zens_ink import content_matrix
# 分析我们的内容覆盖度，找到主题缺口
```

**步骤3：生成数据报告（10分钟）**
- 输出：每日数据报告（曝光/点击/CTR/排名/真实用户/转化率）
- 输出：问题清单（需要优化的页面/关键词）
- 输出：机会清单（新关键词/新内容方向）
- 写入iteration_center/data_reports/目录

**步骤4：更新state.json和知识库（5分钟）**
- 将P0/P1问题写入state.json的next_iteration_focus
- 更新SEO知识库（关键词策略、竞品动态、算法变化）
- 给窗口1/窗口3分配具体任务

---

### 窗口5：变现运营专家

**核心职责**: 联盟营销、广告优化、变现模式探索、收入追踪
**使用工具**: 联盟平台API + GA4转化追踪 + Serper API + Crawl4AI

#### 每日执行流程（定时任务：0 14 * * *，每天下午2点）

**步骤1：联盟链接检查（10分钟）**
```python
# 1.1 检查所有联盟链接是否有效
# 扫描data/tools.json中的所有affiliate链接
# 检查HTTP状态、是否跳转正确、UTM参数是否完整

# 1.2 运行add_utm.py确保所有联盟链接有UTM
python add_utm.py

# 1.3 优化联盟CTA
python optimize_affiliate_cta.py
# 检查CTA按钮位置、文案、颜色、转化率
```

**步骤2：变现机会挖掘（15分钟）**
```python
# 2.1 分析高流量页面的变现潜力
# 从GSC报告中找到Top20高曝光页面
# 检查这些页面是否有联盟链接、是否有广告位、是否有付费产品推荐

# 2.2 用Serper API搜索新的联盟计划
# q: "AI tools affiliate program high commission"
# 评估：佣金比例、cookie期限、品牌知名度、转化难度

# 2.3 竞品变现分析
# 用Crawl4AI爬取竞品页面
# 分析竞品的变现方式：联盟/广告/付费会员/数字产品
```

**步骤3：变现优化执行（20分钟）**
- 给高流量页面添加联盟链接（相关产品）
- 优化CTA按钮（A/B测试文案和位置）
- 添加新的联盟计划（替换低佣金的）
- 探索数字产品变现（AI工具模板、教程、电子书）
- 优化广告位布局（不影响用户体验的前提下）

**步骤4：更新state.json和知识库（5分钟）**
- 记录变现优化进展
- 添加新的联盟计划到知识库
- 给窗口3分配内容任务（写推广文章）

---

### 窗口6：UI/UX设计优化专家

**核心职责**: 网站设计优化、用户体验改进、转化率优化、移动端适配
**使用工具**: Lighthouse + Playwright + Crawl4AI + GA4行为数据 + taste-skill

#### 每日执行流程（定时任务：0 15,20 * * *，每天15点和20点）

**步骤1：UX审计（10分钟）**
```bash
# 1.1 运行Lighthouse可访问性审计
lighthouse https://www.aitoolcrux.com --only-categories=accessibility --output=json

# 1.2 用Playwright测试关键页面交互
# - 首页加载时间、首屏渲染
# - 工具卡片点击、筛选、排序
# - 博客列表页、文章页阅读体验
# - 搜索功能
# - 移动端适配（375px宽度）

# 1.3 分析GA4用户行为数据
# - 高跳出率页面
# - 短停留时间页面
# - 用户点击热图（如果有）
# - 转化漏斗分析
```

**步骤2：设计优化（20分钟）**
- 优化首页Hero区域（标题、副标题、CTA按钮）
- 优化工具卡片设计（信息层级、视觉层次、hover效果）
- 优化博客文章排版（字体、行高、段落间距、目录）
- 优化移动端体验（导航、按钮大小、表单）
- 优化配色方案（对比度、品牌一致性）
- 优化页面加载速度（图片懒加载、代码分割）

**步骤3：执行优化（15分钟）**
```bash
# 按问题选择优化脚本：
# - 首页优化 → taste_optimize_hero.py
# - 文章页优化 → taste_optimize_article.py
# - 移动端优化 → taste_optimize_mobile.py
# - 动效优化 → taste_optimize_motion.py
# - 工具卡片优化 → taste_optimize_toolcard.py
# - 博客列表优化 → optimize_blog_list.py
```

**步骤4：验证优化效果（10分钟）**
```bash
# 重新运行Lighthouse确认性能提升
lighthouse https://www.aitoolcrux.com --output=json
# 用Playwright截图对比优化前后
# 验证移动端适配
```

**步骤5：更新state.json和知识库（5分钟）**
- 记录UX优化进展
- 更新设计知识库
- 给窗口1分配技术实现任务

---

## 第四部分：指挥官调度手册

### 指挥官核心职责
- 战略调度（不是监工）
- 发现新机会、分配任务、协调资源
- 学习新工具/新方法，分配给对应窗口
- 数据汇总、日报发送

### 每日执行流程（定时任务：30 7,22 * * *，每天7:30和22:00）

**步骤1：读取学习笔记（2分钟）**
- 读取commander_learning.md
- 提取今日必须避免的错误

**步骤2：批量学习（30分钟）**
- 按轮换方向学习一个完整主题（10-15个知识点）
- 学习方向：多Agent管理/效率工具/自动化运营/SEO-GEO战略/增长黑客/商业变现/AI工作流
- 学完后将可落地的方法写入state.json待办，分配给对应窗口

**步骤3：发现新机会（10分钟）**
- 读取iteration_center/各窗口报告
- 读取state.json当前待办
- 主动思考新方向/新工具/新机会
- 写入对应窗口知识库和state.json待办

**步骤4：协调资源（5分钟）**
- 检查是否有窗口改同一个文件（协调时间错开）
- 检查任务负载均衡
- 给空闲窗口分配任务

**步骤5：更新关键数据（5分钟）**
- 用Python读data/posts.json → 文章数
- 递归统计public/screenshots/ → 截图数
- 用Python读state.json → 迭代轮次
- 读取gsc-ga4-report/最新文件 → GSC数据
- 更新commander_learning.md的「网站关键数据」

**步骤6：复盘+自我进化（5分钟）**
- 复盘各窗口新进展
- 新错误追加到「犯过的错」表格
- 新经验追加到「学到的经验」表格

**步骤7：发邮件（仅晚上22:00那次）**
- 用Python smtplib发送HTML日报到840754587@qq.com
- 内容：今日预警+各窗口进展+关键数据+新知识+新机会+补录待办
- 标题：【指挥官日报】XXXX-XX-XX 自我升级（HTML版）

---

## 第五部分：定时任务更新方案

### 现有18个定时任务更新

| 任务 | cron_job_id | 现有时间 | 更新内容 |
|------|------------|---------|---------|
| 窗口1-技术SEO修复 | 11854724703490 | 0 1,5,13,22 | query改为引用OpenSEO+real_seo_audit.py+fix_*.py |
| 窗口1-技术学习 | 12381700696322 | 每周一6点 | 学习新SEO工具/技术 |
| 窗口2-外链建设 | 11634001739522 | 0 10,16 | query改为引用Serper API+Crawl4AI+competitor_gap |
| 窗口3-内容调研 | 11854264014594 | 0 3 | query改为引用zens-ink kd+search_intent+keyword_miner.py |
| 窗口3-内容写作 | 11845490420482 | 0 7 | query改为引用generate_real_article.py+quality_audit.py+textstat |
| 窗口3-内容发布 | 11909234749186 | 0 11 | query改为引用publish_drafts.py+push_via_api.py+submit_indexnow |
| 窗口3-内容学习 | 12349601570306 | 每周二6点 | 学习内容营销/写作技巧 |
| 窗口4-数据分析 | 11649035337218 | 0 9,21 | query改为引用GSC+GA4+Cloudflare API+OpenSEO排名 |
| 窗口4-数据学习 | 12342382357250 | 每周三6点 | 学习数据分析/SEO策略 |
| 窗口5-变现运营 | 11224965051650 | 0 14 | query改为引用联盟平台API+GA4转化+Crawl4AI |
| 窗口5-变现学习 | 12249915101954 | 每周四6点 | 学习变现模式/联盟营销 |
| 窗口6-UI/UX优化 | 11845518144514 | 0 15,20 | query改为引用Lighthouse+Playwright+taste-skill |
| 窗口6-UX学习 | 12342382360834 | 每周五6点 | 学习UX设计/转化率优化 |
| 指挥官-战略学习 | 12249915177730 | 0 9 | 学习战略级主题 |
| 指挥官-每日调度 | 11909253222146 | 30 7,22 | 调度+复盘+日报 |
| 每周全链路走查 | 11633848417794 | 每周一8点 | 全链路检查 |
| 每周索引监控 | 12342528135938 | 每周一22点 | 索引页数监控 |
| 每周一GSC关键词机会筛选 | 12360047155202 | 每周一21:45 | GSC机会词筛选 |

### 所有定时任务query必须包含的铁律
```
## ⚠️ JSON解析铁律
- 绝对禁止用PowerShell的ConvertFrom-Json解析任何JSON
- 所有JSON必须用Python解析（json.load()）
- 大JSON文件（tools.json 7.86MB）必须用Python，禁止PowerShell

## ⚠️ 工具使用铁律
- 优先使用已有工具，禁止重复造轮子
- 审计用：OpenSEO + real_seo_audit.py + quality_audit.py + Lighthouse
- 关键词用：zens-ink(kd/search_intent) + keyword_miner.py + Serper API
- 爬虫用：Crawl4AI + trafilatura + playwright-stealth
- 修复用：对应fix_*.py脚本
- 部署用：push_via_api.py + Vercel自动部署
- 发现问题必须写入state.json待办（用Python json.load+json.dump）
```

---

## 第六部分：紧急问题处理流程

### P0问题（网站打不开/内容消失/部署失败）
1. 立即用Playwright检查网站状态
2. 检查Vercel部署日志
3. 检查GitHub Actions最近运行
4. 回滚到上一个稳定版本
5. 修复后重新部署
6. 通知用户

### P1问题（排名骤降/流量暴跌/CTR异常）
1. 检查GSC数据变化
2. 检查是否有算法更新
3. 检查竞品变化
4. 分析受影响页面
5. 制定修复计划
6. 分配给对应窗口

### P2问题（性能下降/小bug/内容质量）
1. 记录到state.json待办
2. 按优先级排队修复
3. 分配给对应窗口

---

## 第七部分：质量保证体系

### 文章发布前质量门（必须全部通过）
| 检查项 | 标准 | 工具 |
|--------|------|------|
| 字数 | ≥2000字 | quality_audit.py |
| Quick Answer | 存在且≤320字符 | quality_audit.py |
| Key Takeaways | 存在 | quality_audit.py |
| FAQ | ≥3个 | quality_audit.py |
| How We Tested | 存在 | quality_audit.py |
| 内链 | ≥3个 | quality_audit.py |
| 图片 | ≥1张含alt | quality_audit.py |
| 可读性 | Flesch≥40 | textstat |
| 标题 | 30-80字符 | quality_audit.py |
| 外链 | ≥1个权威来源 | quality_audit.py |
| 综合评分 | ≥85分 | quality_audit.py |

### 部署前验证清单
- [ ] 所有测试通过（GitHub Actions）
- [ ] Lighthouse性能评分≥90
- [ ] 无控制台错误
- [ ] 移动端适配正常
- [ ] 所有链接有效
- [ ] 图片加载正常
- [ ] Schema结构化数据有效

### 每周全链路走查（每周一8点）
1. 运行所有审计脚本
2. 检查所有定时任务执行状态
3. 检查GSC/GA4数据趋势
4. 检查外链增长
5. 检查索引页数
6. 检查部署成功率
7. 生成周报

---

**文档版本**: v1.0
**最后更新**: 2026-09-28
**维护者**: 指挥官
**适用范围**: 6个窗口+指挥官全部定时任务
