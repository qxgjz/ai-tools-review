# GSC/GA4 数据日报（2026-10-26，r28）

## GSC 实拉（fetch_gsc 实跑，窗口 2026-09-24~10-23）
- **Clicks 0 | Impressions 167 | CTR 0% | AvgPos 14.13**（环比持平，数据稳定无恢复）
- Top page 曝光：/blog/best-ai-coding-tools-2026（12 imp, pos 4.1）；首页变体合计 5 imp
- 查询级：全 0 点击，长尾异常词为主（ai-native ide adoption metrics / copilot pricing 组合词等）

## 关键发现（本轮）
1. **URL 变体蚕食（P0 修复待办已建）**：首页 3 版本（http/www/无斜杠）+ /about 2 版本 + ai-policy 无斜杠 → 曝光被拆 5 组；`_redirects` 需 301 规范化
2. **同族蚕食**：best-ai-coding-tools-2026（12 imp）vs ai-coding-tools-comparison-2026（2 imp）→ 需分主次
3. **article-api 异常 URL**：4 imp 占索引预算，建议 301/410
4. **收录基线维持**：477/905=52.8%（gsc_indexed_baseline_20261025.md），无新变化

## 待办统计
- 执行完成 3 条；新写入 19 条（CTR3+CA5+KW8+蚕食修复3）
- focus=249；pending=246→249 区间；分析师专属 pending=2（阻塞）

## 下周监控点
- URL 变体数量（规范化后应为 0 组）
- coding-tools 族点击恢复
- SEO MCP 授权后 AI 可见性基线（解锁 GEO-BASELINE）
# GSC/GA4 数据日报（2026-10-26 r29，09:00 档）

## GSC
- Clicks 0 | Impressions 167 | CTR 0% | AvgPos 14.13（窗口 2026-09-24~10-23，与 r28 同数据，环比持平）
- 无新拉数据；上次拉取 2026-10-26 00:2x（r28）

## 关键发现（本轮）
1. **关键词量验证（P0 完成）**：48 候选词 12 词实搜 → 9 High/3 Medium/0 Low；"停止无效长尾量产"判断成立；5 词入选有量清单（legal/gift/churn/travel/fun）
2. CTR 无新命中（数据窗口未变），补开 ai-policy(8.0)/首页(2.0) 2 条
3. 竞品缺口本轮全 High（marketing/sales/search-engine）→ 内容策略转向差异化/GEO
4. 收录基线 477/905=52.8% 维持

## 待办
- 完成 1（P0 量验证）；新写入 14；focus=276→290 区间；分析师 pending=2（阻塞）


---

# r30 追加（2026-10-26 15:06 · 15:00 档 · 新 GSC 窗口实拉）

## GSC（fetch_gsc.py 实拉，窗口 2026-09-25~10-24）
| 指标 | r29(09-24~10-23) | r30(09-25~10-24) | 变化 |
|---|---|---|---|
| Clicks | 0 | 0 | = |
| Impressions | 167 | **171** | **+4** |
| CTR | 0% | 0% | = |
| AvgPos | 14.13 | **14.29** | **-0.16（略降）** |

### 新曝光页面（本窗口新增）
- /about/ 6 imp pos3.3（新变体）、/alternatives/cursor-alternatives 2 imp pos1.0、/blog/best-ai-meeting-assistants-2026 1 imp pos9.0、/blog/best-ai-observability-tools-2026 2 imp pos9.5、/blog/best-ai-productivity-tools-2026 2 imp pos10.5、bondai 查询 2 imp pos89.5
- **3 个新 5-15 位 CTR 命中**（meeting/observability/productivity 全 0%）→ 已开 CTR 待办给打磨师

### 关键发现
1. education 词 SERP Medium → 新 P0（KW-VOLUME-CONFIRMED-EDUCATION）
2. 蚕食持续：/about vs /about/（7+6 imp）、首页变体（1+7 imp）、article-api 异常 URL 5 imp——r28 修复待办（CANONICAL-REDIRECT-AUDIT/ARTICLE-API-URL-CLEAN）仍 pending，建议指挥官催架构师
3. MOBILE 4 imp pos6.5：移动端有位置但 0 点击，与桌面一致
4. 收录基线 477/905=52.8% 维持
