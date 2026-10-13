# -*- coding: utf-8 -*-
import os, datetime

proj = r"iteration_center"

# ---------- 1) index_monitor.md 追加本周报告 ----------
im_path = os.path.join(proj, "index_monitor.md")
im = open(im_path, encoding="utf-8").read()

week_report = """

---

## 2026-10-12 周索引报告

### 基本数据
- **日期：** 2026-10-12（GSC 报告日 2026-10-09，快照拉取 2026-10-12）
- **GSC 已编入页面数：** 477
- **GSC 未编入页面数：** 428（含 discovered_not_indexed 400 / duplicate 9 / auto_redirect 9 / noindex 5 / not_found 2 / redirect_error 1 / crawled_not_indexed 2）
- **GSC 已知 URL 总数：** 905
- **Sitemap URL总数：** 804（上周 752，+52，+6.9%）
- **索引覆盖率（已编入/sitemap）：** 59.3%
- **环比：** 9/18 site: 基线 343 → 现 GSC 官方 477（口径不同：site: 查询 vs GSC 索引报告，仅作方向性参考；估算增长约 +39%）
- **GSC 曝光（10-03~10-09 周）：** 41 次曝光 / 0 点击
- **28天窗口 Top 查询：** best voice changer 2026（点击1）、ai agent（曝光5）

### 68 个重点 URL 批量实测（2026-10-12，AdsPower CDP 直连 GSC 网址检查）
| 状态 | 数量 | 明细 |
|------|-----:|------|
| 已收录 indexed | 20 | midjourney/dall-e-3/windsurf/copy-ai/notion-ai/runway/pika/suno/perplexity/figma-ai/canva-magic/auto-gpt/worldmonitor/llama-index/ragflow/promptfoo/milvus/chroma/faiss/mem0 |
| 已发现未编入 discovered_not_indexed | 4 | /category/memory、/category/observability、/tools/claude、/tools/exa |
| 重定向错误 redirect_error | 3 | /category/chat、/category/code、/tools/gemini |
| 重定向 redirect | 1 | /tools/chatgpt |
| 未知 unknown（配额耗尽） | 40 | 待 2026-10-13 配额重置后重跑 |

### 趋势判断
- ✅ **无连续下降**：GSC 官方已编入 477，较 9 月 site: 估算基线（343-370）方向性增长约 +29%~39%
- ✅ **内容持续扩充**：Sitemap 752→804（+52），博客文章 105→184
- ⚠️ **未编入中 93.5% 为"已发现未编入"（400/428）**：Google 已发现这些 URL 但尚未抓取编入，是当前最大收录杠杆，需 IndexNow 提交 + 内链 + 抓取推动
- ⚠️ **重定向异常 4 个**：/category/chat、/category/code、/tools/gemini（redirect_error）、/tools/chatgpt（redirect），影响对应高价值词收录
- ⚠️ **曝光仍极低**：周曝光 41 次 / 0 点击，覆盖 905 已知 URL 中仅少数获得展示

### Top 10 未收录/异常重要页面
| 优先级 | 页面 | 类型 | 状态 | 建议 |
|--------|------|------|------|------|
| P0 | /tools/gemini | 工具页 | redirect_error | 修复重定向链，检查 301/canonical，修复后 IndexNow 提交 |
| P0 | /tools/chatgpt | 工具页 | redirect | 确认是否规范 301 到唯一 URL，避免被判定重定向异常 |
| P0 | /category/chat | 分类页 | redirect_error | 修复分类重定向，检查面包屑/规范链接 |
| P0 | /category/code | 分类页 | redirect_error | 同上 |
| P1 | /category/memory | 分类页 | discovered_not_indexed | IndexNow 提交 + 从博客页加内链 |
| P1 | /category/observability | 分类页 | discovered_not_indexed | 同上 |
| P1 | /tools/claude | 工具页 | discovered_not_indexed | 同上 |
| P1 | /tools/exa | 工具页 | discovered_not_indexed | 同上 |
| P1 | /tools/midjourney | 工具页 | 无曝光（历史） | 持续监控，确保无 noindex |
| P1 | /tools/elevenlabs | 工具页 | 无曝光（历史） | 持续监控 |

### 优化建议
- **P0**：架构师修复 4 个重定向异常 URL（/tools/gemini、/tools/chatgpt、/category/chat、/category/code），修复后请求编入索引
- **P0**：分析师 2026-10-13 配额重置后重跑 40 个 unknown URL（脚本已修复 bringToFront）
- **P1**：增长黑客对 400 个 discovered_not_indexed 中的高价值页面（工具页 Top50）批量 IndexNow 提交
- **P1**：创作家在已曝光博客文章中加入指向未收录分类页/工具页的内链
- **P2**：持续每周监控，下次监控 2026-10-19

### 数据来源说明
- GSC 已编入/未编入：AdsPower CDP 直连 GSC 索引报告页实测快照（indexing_snapshot_20261012.json）
- Sitemap：线上 https://www.aitoolcrux.com/sitemap.xml 实时统计（804 URL）
- 68 URL 状态：url_index_check_batch_0_67_20261012_202338.json
- GSC 曝光：gsc-ga4-report/live_pull_20261012_2007.json
"""
open(im_path, "w", encoding="utf-8").write(im + week_report)

# ---------- 2) audit_findings.md 追加索引异常 ----------
af_path = os.path.join(proj, "audit_findings.md")
af = open(af_path, encoding="utf-8").read()
af_append = """

---

## 索引监控异常发现（2026-10-12 周）

### 异常 1：重定向异常 URL（P0）
- **现象**：GSC 网址检查实测 /category/chat、/category/code、/tools/gemini 为 redirect_error，/tools/chatgpt 为 redirect
- **影响**：这 4 个 URL 无法正常编入索引，其中 /tools/chatgpt、/tools/gemini 是高搜索量头部工具词
- **建议**：架构师检查线上 301/302/canonical 链，确认是规范重定向（如 /tools/gpt-4 → /tools/chatgpt）还是异常循环；修复后 IndexNow 重新提交

### 异常 2：未编入中 93.5% 为"已发现未编入"（400/428）（P0）
- **现象**：GSC 索引报告显示 428 未编入中 400 个为 discovered_not_indexed（已发现、尚未编入）
- **影响**：Google 已发现但未抓取/编入，新站常见但会长期拖累索引覆盖率（59.3%）
- **建议**：优先对高价值工具页 Top50 批量 IndexNow 提交；在已收录页面增加指向这些 URL 的内链；保证页面有独立内容价值（避免 thin content）

### 异常 3：索引覆盖率口径升级（信息）
- **现象**：从 site: 估算（343-370）升级为 GSC 官方索引报告口径（已编入 477）
- **影响**：基准更准确；后续环比一律以 GSC 官方口径为准
- **建议**：下次监控（2026-10-19）直接用 GSC 索引报告页快照
"""
open(af_path, "w", encoding="utf-8").write(af + af_append)

# ---------- 3) todo_from_analysis.md 追加待办建议 ----------
td_path = os.path.join(proj, "todo_from_analysis.md")
td = open(td_path, encoding="utf-8").read()
td_append = """

---

## 索引监控待办建议（2026-10-12）

### P0（架构师）
1. **修复重定向异常 URL**：/category/chat、/category/code、/tools/gemini（redirect_error）、/tools/chatgpt（redirect）。检查 301/302/canonical 链是否规范，修复后提交 IndexNow 请求编入索引。

### P0（分析师）
2. **重跑 40 个 unknown URL**：GSC 网址检查配额 2026-10-12 已耗尽，2026-10-13 配额重置后运行 `python scripts/gsc_batch_check.py`（脚本已修复：输入框用 input.Ax4B8 + 每次输入前 Page.bringToFront）。结果对照 url_index_check_batch_0_67_20261012_202338.json 汇总最终收录状态。

### P1（增长黑客）
3. **批量 IndexNow 提交 discovered_not_indexed 高价值页面**：对 400 个"已发现未编入"中 /tools/ 高价值工具页 Top50 提交 IndexNow。

### P1（创作家）
4. **内链推动未收录页面**：在已有曝光的 /blog/ 文章中，加入指向 /category/memory、/category/observability、/tools/claude、/tools/exa 的自然内链。

### P2（持续）
5. **每周索引监控**：下次 2026-10-19，直接用 GSC 索引报告页快照口径对比。
"""
open(td_path, "w", encoding="utf-8").write(td + td_append)

print("index_monitor.md 已更新:", os.path.getsize(im_path))
print("audit_findings.md 已更新:", os.path.getsize(af_path))
print("todo_from_analysis.md 已更新:", os.path.getsize(td_path))
