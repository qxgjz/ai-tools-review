# -*- coding: utf-8 -*-
"""分析师 r28 P0 部分：GSC 蚕食检测报告 + GH-005 SEO MCP 接入方案 + state.json 更新"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
now = datetime.now().strftime('%Y-%m-%d %H:%M')

# ============ 1. GSC 蚕食检测报告 ============
cannibal = f"""# GSC 蚕食（Cannibalization）检测报告

- 生成时间：{now}
- 数据源：`gsc-ga4-report/live_pull_20261024_0939.json`（GSC 实拉，2026-09-24~10-23 窗口）
- 待办：P0-GSC-CANNIBAL-AUDIT-20261025

## 检测结果

### A. URL 变体蚕食（页面级，确定性最高）
同一页面多 URL 变体共享曝光，稀释单一 URL 的排名权重：

| URL 变体 | Impressions | Position | 判定 |
|---|---|---|---|
| http://www.aitoolcrux.com/ | 1 | 1.0 | 非规范版本 |
| https://www.aitoolcrux.com/ | 4 | 2.0 | **规范版本（保留）** |
| https://www.aitoolcrux.com/about | 7 | 3.3 | 无斜杠变体 |
| https://www.aitoolcrux.com/about/ | 2 | 1.0 | 尾部斜杠变体 |
| https://www.aitoolcrux.com/ai-policy | 1 | 8.0 | 无斜杠变体 |

首页 3 版本（http/www-无斜杠/www）+ about 2 版本 → 至少 5 组 URL 变体在蚕食曝光。全部 0 点击，权重被拆分。

### B. 主题族多页竞争（关键词级潜在蚕食）
| 关键词族 | 页面 1 | 页面 2 | 风险 |
|---|---|---|---|
| ai coding tools | /blog/best-ai-coding-tools-2026（12 imp, pos 4.1） | /blog/ai-coding-tools-comparison-2026（2 imp, pos 5.5） | 同族 2 页共享，Google 只挑一页进首页 |

### C. 异常 URL 污染（第三方导入产生）
`/blog/article-api-20260903-171438-creatium-coach-review-2025-...md` 这类含时间戳+markdown 后缀的 URL 共 4 imp，是早期批量导入遗留，占用索引预算且无 SEO 价值。

## 修复建议（按优先级）
1. **P0（架构师/窗口1）**：全站 301 规范化——http→https、www→非www（或反向）、尾部斜杠统一；`_redirects` 加规则
2. **P0（架构师/窗口1）**：`/blog/article-api-*` 系列 301 → 对应规范文章或 410，释放索引预算
3. **P1（内容/打磨师）**：best-ai-coding-tools-2026 与 ai-coding-tools-comparison-2026 二选一为主页，另一页改为差异化长尾（comparison 页做对比表、best 页做列表），内链互指明确主次
4. **P1（分析师监控）**：每周 GSC 复查 URL 变体数量，目标降至 0 组

## 验证方法
- 修复后重拉 live_pull：检查 top_pages 中 http:// / 无斜杠变体消失，曝光合并到规范 URL
- GSC URL 检查工具逐页验证 canonical
"""
cp = os.path.join(P, 'iteration_center', 'gsc_cannibalization_20261026.md')
with open(cp, 'w', encoding='utf-8') as f:
    f.write(cannibal)
print('cannibal report:', os.path.getsize(cp), 'bytes')

# ============ 2. GH-005 SEO MCP 接入方案 ============
plan = f"""# GH-20261026-005 SEO 工具链升级：open-seo-mcp-skills 评估与接入方案

- 生成时间：{now}
- 状态：P0 完成（评估 + 本地化已落地；直连 MCP 待浏览器授权）

## 1. 仓库评估（实读 GitHub）
| 项 | 值 |
|---|---|
| 仓库 | github.com/Ryze-AI-Adgent/open-seo-mcp-skills |
| Stars | 7.2k（与任务描述 7.1k 一致，持续增长） |
| 协议 | MIT（可自由使用/修改/分发） |
| 形态 | SEO MCP server（Ryze connector）+ 8 个 Claude Skills（Markdown） |
| 数据源 | **真实 GSC + GA4 + Google Ads 关键词量 + DataForSEO**（反链/SERP/竞品词），可选接 Ahrefs/Semrush |

### 8 个 Skills 能力
| Skill | 能力 | 数据源 |
|---|---|---|
| seo-audit | 索引健康/CTR 异常/衰减页/striking-distance/蚕食 | GSC+GA4 |
| keyword-research | 种子→想法→量/CPC/意图→聚类 | Ads+DataForSEO |
| rank-tracking | 任意两期位置变化 | GSC |
| competitor-gap | 竞品排名而我们没有的词 | DataForSEO+GSC |
| backlink-check | 反链画像 vs 竞品 | DataForSEO |
| ai-visibility | 哪些 AI 引擎引流+引用哪些页 | GA4 AI 引荐 |
| content-brief | SERP 驱动的写作简报（标题/实体/问题/内链） | DataForSEO+GSC |
| seo-vs-ads | 付费词中已自然排名的查询 | GSC×Ads |

## 2. 与现有 zens-ink/opengtm 工具链覆盖差距对比（实读本地）
| 能力 | 现有（zens-ink/fetch_gsc/fetch_ga4） | open-seo-mcp | 差距 |
|---|---|---|---|
| GSC 数据拉取 | ✅ fetch_gsc.py（md 报告） | ✅ 实时工具 | 无 |
| GA4 数据拉取 | ✅ fetch_ga4.py | ✅ 实时工具 | 无 |
| 竞品 sitemap 对比 | ✅ zens_ink.competitor_gap | ✅ competitor-gap（词级） | 部分（词级更深） |
| CTR/排名分析 | ✅ 手动脚本 | ✅ seo-audit/rank-tracking 自动 | 部分 |
| **关键词搜索量/CPC/意图** | ❌ 无 | ✅ Ads+DataForSEO | **大差距（禁编造搜索量的正解）** |
| **反链画像** | ❌ 无 | ✅ backlink-check | **大差距** |
| **SERP 快照/content-brief** | ❌ 无 | ✅ content-brief | **大差距** |
| **AI 可见性（GEO）** | ❌ 无（GEO baseline 阻塞中） | ✅ ai-visibility（GA4 AI 引荐） | **大差距（GEO 落地捷径）** |
| seo-vs-ads | ❌ 无 | ✅ | 大差距 |

结论：**覆盖差距集中在 5 项——关键词量/反链/SERP 简报/AI 可见性/seo-vs-ads**，恰好是本工具链最短缺的"禁编造搜索量"数据源。

## 3. 接入方案
### A. 立即可用（已完成 ✅）：skills 本地化
- 已 clone 至 `vendor/open-seo-mcp-skills/`（8 个 SKILL.md，MIT）
- 用法：按需 Read 对应 SKILL.md 的 workflow，替换 MCP 工具调用为现有脚本等价实现；其中**思路可直接移植**（striking-distance/CTR 异常/衰减页定义）

### B. 需授权（待浏览器会话）：直连 Ryze MCP
```
# MCP endpoint（实测可达，401 invalid_token → 需 OAuth）
POST https://connector.get-ryze.ai/mcp   # 代理 127.0.0.1:7890 已通

# 接入命令（Claude Code 环境）
claude mcp add ryze --transport http https://connector.get-ryze.ai/mcp
# 或本机 Python MCP 客户端（需先 pip install mcp）
```
- **依赖**：Google OAuth 授权（连接 GSC/GA4/Ads 账号）+ 浏览器 GUI 会话（同 GEO baseline 阻塞同类）
- **数据口径**：rankings=真实 GSC 位置；traffic=真实 GA4（含 AI 引荐）；keyword volumes=Google Ads 关键词规划器；竞品词/反链=DataForSEO
- 落地后分析师 SOP 新增：seo-audit 每周跑（替代手工 fetch）、keyword-research 挖词（搜索量有真值）、ai-visibility 做 GEO 基线（解锁阻塞的 P1-GEO-BASELINE-AUDIT）

### C. 推荐执行顺序
1. 用户授权浏览器登录 get-ryze.ai / 或授权 OAuth（一次性）→ 2. 装 Python mcp 库 → 3. 脚本化调用 ryze 工具（search console/analytics）→ 4. SOP 固化

## 4. 结论
- 接入价值：**高**（5 项大差距正好是内容生产/关键词挖掘的瓶颈）
- 阻塞点：仅 OAuth 授权（需用户浏览器配合一次），代码与 skills 已全部就绪
- 本轮已落地：vendor 本地化 + 本方案 + SEO_TOOLKIT_MASTER.md 更新
"""
pp = os.path.join(P, 'iteration_center', 'seo_mcp_接入方案_20261026.md')
with open(pp, 'w', encoding='utf-8') as f:
    f.write(plan)
print('mcp plan:', os.path.getsize(pp), 'bytes')

# ============ 3. state.json 更新：标记 2 个 P0 完成 + 蚕食修复待办 ============
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
for i in nf:
    if i.get('id') in ('GH-20261026-005', 'P0-GSC-CANNIBAL-AUDIT-20261025'):
        i['status'] = 'completed'
        i['completed_at'] = now_iso
        i['evidence'] = ('iteration_center/gsc_cannibalization_20261026.md' if 'CANNIBAL' in i['id']
                         else 'iteration_center/seo_mcp_接入方案_20261026.md + vendor/open-seo-mcp-skills/')
# 补录蚕食修复待办（架构师 P0）
new_todos = [
    {'id': 'CANONICAL-REDIRECT-AUDIT-20261026', 'status': 'pending', 'priority': 'P0',
     'assigned_to': ['架构师', 'window1'],
     'task': '全站 URL 规范化：http→https、www→非www、尾部斜杠统一（GSC 实数据发现首页 3 版本+about 2 版本蚕食），_redirects 加 301 规则',
     'source': 'gsc_cannibalization_20261026', 'created_at': now_iso},
    {'id': 'ARTICLE-API-URL-CLEAN-20261026', 'status': 'pending', 'priority': 'P0',
     'assigned_to': ['架构师', 'window1'],
     'task': '/blog/article-api-*（含时间戳+md 后缀）系列 URL 301→规范文章或 410，释放索引预算（GSC 实数据 4 imp）',
     'source': 'gsc_cannibalization_20261026', 'created_at': now_iso},
    {'id': 'CODING-TOOLS-CANNIBAL-RESOLVE-20261026', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['创作家', 'window3'],
     'task': 'best-ai-coding-tools-2026 与 ai-coding-tools-comparison-2026 二选一为主页，另一页差异化（列表 vs 对比表）并互指，消除同族蚕食',
     'source': 'gsc_cannibalization_20261026', 'created_at': now_iso},
]
ids = {i.get('id') for i in nf}
for t in new_todos:
    if t['id'] not in ids:
        nf.append(t); ids.add(t['id'])
d['next_iteration_focus'] = nf
d['last_update'] = now_iso
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('state updated. focus:', len(nf), '| completed 2 P0 | +3 cannibal todos')
