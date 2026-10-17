# claude-seo 工具评估报告（P1-TOOL-CLAUDE-SEO-20261017）

**日期**: 2026-10-17 (r29)
**评估人**: 架构师窗口
**仓库**: AgriciDaniel/claude-seo（GitHub 实测：19.1k stars / 2.8k forks / MIT，383 commits）

## 一、工具事实（web_fetch GitHub 实测，非转述）

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/AgriciDaniel/claude-seo |
| 定位 | Claude Code 开源 SEO 审计插件（26 sub-skills + 19 sub-agents 并行） |
| 覆盖域 | technical SEO / E-E-A-T / Schema.org / GEO·AEO / agent readiness（Lighthouse Agentic Browsing、WebMCP、llms.txt）/ backlinks / local / e-commerce / international |
| 核心卖点 | ①AI-search first（对齐 Google AI Optimization Guide，问题式可引用性评分）②并行审计（全站审计分钟级）③**可证伪建议**：每条建议含 第一性观察+依赖关系+失败检查方式+先行指标 |
| 安装 | install.ps1 / install.sh（Claude Code plugin marketplace），Python 3.10+ |
| 许可 | MIT（免费本地） |
| 私有镜像 | AI-Marketing-Hub/claude-seo（会员 early access） |

## 二、本环境可行性核查（实测）

| 前置条件 | 实测结果 | 结论 |
|---|---|---|
| Claude Code CLI | `Get-Command claude` → **未安装** | ❌ 无法执行 ①安装+②/ seo audit |
| Anthropic 账号/登录态 | 本环境无 | ❌ 安装/运行 Claude Code 需账号（含付费 API 额度） |
| Python 3.10+ | 已有 | ✅ |
| 站点访问 | 线上 www.aitoolcrux.com 可达（服务器端） | ✅ |

**结论**：①安装、②跑 /seo audit 两项**阻塞**——依赖 Claude Code CLI + Anthropic 登录态，架构师窗口无此凭据，非代码可解决。需指挥官决定：提供 Claude Code 环境（或用户在自有 Claude Code 中安装并跑一次审计后回传结果）。

## 三、可落地产出（本轮完成）

### 3.1 「4 项可证伪检查」验收方法论 → 固化为本项目验收模板

借鉴 claude-seo 方法论（每条建议必须含 4 项），本项目所有窗口的"完成声明"验收标准模板：

| # | 检查项 | 含义 | AIToolCrux 落点示例 |
|---|---|---|---|
| 1 | **第一性观察** | 建议基于什么可复现的原始事实 | 线上 HTML 实测：`<h1>` 缺失（curl 页面原文）而非"应该加 h1" |
| 2 | **依赖关系** | 该修复依赖哪些前置条件/顺序 | 先补 h1 才谈 heading 层级；schema 修复依赖对应组件存在 |
| 3 | **失败检查方式** | 怎么知道它失败了（可证伪） | 重跑 `seo_audit_full.py` 该项仍 fail；或线上抓 HTML 无该 schema |
| 4 | **先行指标** | 成功后先出现什么可测信号 | GSC 该 URL 首次进入 coverage；或 Search Console 结构化数据项出现 |

**落盘**：本模板写入 `iteration_center/SEARCH_VALIDATION_TEMPLATE.md`，供指挥官验收各窗口"完成"声明（替代只信窗口日志）。

### 3.2 与 OpenSEO（SaaS）对比

| 维度 | claude-seo（本地开源） | OpenSEO（SaaS） |
|---|---|---|
| 成本 | 免费（MIT），仅需 Claude Code 订阅 | 付费额度（项目已有订阅） |
| 覆盖 | 26 sub-skills + 19 agents（含 GEO/AEO/agent-readiness） | 技术/内容/链接/结构化数据（SaaS 面板） |
| 数据源 | Google 官方指南 + 本机抓取 + 可选扩展 | 云抓取 + API |
| 并行 | 17 agents 并行，分钟级全站 | 队列式 |
| 可证伪 | 内置（每条建议 4 项检查） | 面板评分，无统一证伪模板 |
| 前置 | Claude Code + Anthropic 账号 | 无（已接入） |
| 结论 | **可作为 OpenSEO 付费额度的免费替代补充**，但需先解决 Claude Code 环境；当前 OpenSEO 额度继续作为主审计通道 |

## 四、行动项

1. **待指挥官**：决定是否提供 Claude Code 环境/账号（接入 claude-seo 的硬前置）。
2. **已完成**：可证伪验收模板落盘 SEARCH_VALIDATION_TEMPLATE.md，指挥官验收各窗口时可启用。
3. **本项目已有替代通道**（无需外部工具）：`real_geo_aeo_audit.py`（GEO/AEO）、`iteration_center/seo_audit_full.py`（40+ 规则）、`npx lighthouse`（CWV/a11y/SEO）、OpenSEO SaaS —— claude-seo 的价值主要在"全站并行 + 可证伪输出格式"，模板已吸收其方法论。
