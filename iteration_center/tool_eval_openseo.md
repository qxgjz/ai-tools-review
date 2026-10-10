# OpenSEO 接入评估报告

**评估日期**: 2026-10-10
**评估人**: 架构师窗口（定时任务轮）
**项目**: AIToolCrux（Cloudflare Pages + Next.js）
**评估对象**: [every-app/open-seo](https://github.com/every-app/open-seo)（20.5K stars, MIT, TypeScript）

## 结论：不建议当前接入（保持「已装机未运行」状态）

OpenSEO 是功能完整的自托管 SEO 套件（Semrush/Ahrefs 替代），但与本项目现有工具链**高度重叠**，且**部署成本与资源占用高于收益**。当前阶段维持现状，不启动 Docker、不接入、不删除现有脚本。

## 评估明细

| 维度 | 结论 | 依据 |
|---|---|---|
| ① 能否跑起来 | 能，但成本高 | 两条路：Docker（个人机最简单）/ Cloudflare（云端免费计划）。需 PostgreSQL + Redis + Worker，资源占用明显高于现有轻量脚本 |
| ② 替代现有脚本 | 覆盖大部分，但**现有脚本已够用** | 见下表功能对比 |
| ③ 接入成本 | 高 | 部署+数据库+迁移+对接手册+维护；当前架构师窗口无专职运维人力 |
| ④ 是否删重复脚本 | **不删** | 现有脚本已接入 SOP、有验证闭环，OpenSEO 未运行即删脚本会破坏手册约定 |

## 功能对比（OpenSEO vs 现有工具链）

| 功能 | OpenSEO | 现有工具（已接入） |
|---|---|---|
| 关键词研究 | ✅ | `opengtm`（已装，9模块关键词研究）、`zens-ink kd/search_intent`、`keyword_miner.py` |
| 排名追踪 | ✅ | `zens-ink rank_tracker` |
| 外链分析 | ✅ | `zens-ink competitor_gap`（GSC/GA4 数据侧由窗口4拉取） |
| 技术审计 | ✅（40+规则） | `seo_audit_full.py`（sitemap驱动，40+规则，796页） |
| AEO/GEO 审计 | 部分 | `opengtm` + `real_geo_aeo_audit.py`（AI搜索可见性专项） |
| 页面性能 | - | Lighthouse + Unlighthouse（GitHub Actions） |

**关键差异**：OpenSEO 的核心增量是「统一数据面板 + MCP 供 AI Agent 交互」，但本项目是**脚本化工作流 + state.json 待办闭环**，各窗口按 SOP 执行，统一面板价值有限。

## 复评触发条件

以下任一满足时重新评估接入：
1. 关键词研究/排名追踪需要跨日历史数据且现有脚本不满足（当前 GSC/GA4 由窗口4 拉取）
2. 需要对外展示 SEO 数据面板（客户/合作方可见）
3. Docker 环境就绪且有专人维护（当前无）

## 建议动作
- state.json 中该 P1 待办标记 completed（评估完成，结论=不接入）
- SEO_TOOLKIT_MASTER.md 中 OpenSEO 状态标注更新为「评估完成：不接入（功能重叠+资源高）」——由下次 SOP 修订统一处理，不在本轮改手册（避免与手册重大修复记录冲突）
