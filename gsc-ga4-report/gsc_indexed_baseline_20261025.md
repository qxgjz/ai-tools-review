# GSC 真实收录基线 · 2026-10-25

> **目的**：纠正「收录=0」误判。sitemap API 报 submitted=881/indexed=0 是 GSC 报告口径问题（站点存在 301/308 重定向链时 sitemap indexed 长期显示 0），**真实收录远非 0**。

## 一、基线数据（AdsPower CDP 实抓 GSC 页面，indexing_snapshot_20261012.json）

| 指标 | 数值 | 说明 |
|---|---|---|
| 总 URL（known） | **905** | 站点已知 URL 总数 |
| **真实收录（indexed）** | **477** | 收录率 **52.8%** |
| 未收录（not_indexed） | 428 | 未收录率 47.2% |

## 二、未收录原因分解（428 = 100%）

| 原因 | 数量 | 占比 | 可行动作 |
|---|---|---|---|
| **discovered_not_indexed（已发现未收录）** | **400** | **93.5%** | 最大类：Google 已发现但未入索引，多为低质量/低需求长尾页，需内容质量提升+内部链接强化 |
| duplicate_without_canonical（无规范重复） | 9 | 2.1% | 加 canonical 标签（P1，架构师） |
| auto_redirect（自动重定向） | 9 | 2.1% | 核实重定向链，避免死链（P1） |
| noindex | 5 | 1.2% | 确认是否故意 noindex（默认保留） |
| not_found_404 | 2 | 0.5% | 清理或 301 到有效页（P1） |
| crawled_not_indexed（已抓未收录） | 2 | 0.5% | 内容质量/渲染问题（P1） |
| redirect_error（重定向错误） | 1 | 0.2% | 修复重定向链（P1） |

## 三、周度跟踪基线（首期）

| 周次 | 报告日 | indexed | not_indexed | 收录率 | 数据源 |
|---|---|---|---|---|---|
| W1 | 2026-10-09 | 477 | 428 | 52.8% | indexing_snapshot_20261012（10-12 拉取） |

**跟踪方法**：每周用 AdsPower CDP 拉 GSC 索引覆盖率页 → 更新本表 → 与 sitemap API（易误报 0）交叉验证。目标：收录率周度环比上升，重点压降 discovered_not_indexed（400 条）。

## 四、纠正结论

1. **收录不是零**：真实收录 477/905（52.8%），此前的 indexed=0 为 sitemap API 口径 bug 所致
2. **真正的问题不是收录为零，而是**：
   - discovered_not_indexed 400 条（93.5%）——Google 已发现但认为不值得索引，指向**内容质量/相关性**问题而非技术收录问题
   - GSC 点击归零/曝光低位与收录率关系需重新归因：52.8% 收录下曝光仍低，重点是**查询相关性 + 排名**，而非"未被收录"
3. **P0 杠杆修正**：之前「URL 规范化解决收录=0」的判断需降级；真正的动作是内容质量提升（压降 discovered_not_indexed）+ CTR/Title 优化（已有 5 条 CTR 待办在池）

## 五、本轮动作

- 产出本基线文件（P0-GSC-INDEXED-ZERO-REPORT-20261025 完成）
- 同步更新 audit_findings.md（纠偏收录误判）
- 新增周度跟踪待办：每周重拉索引覆盖率，更新本表
