# Cloudflare Bot Traffic Analysis — 2026-10-17 (architect r28)

## 背景（commander_cf_probe_2026-10-17, P0 CF-20261017-001）

确认 2026-10-03 有 893 GA4 sessions 为 headless 采集器扫站：
- CF 当日请求 15,428；GA4 仅记 893 sessions，engaged 仅 7.4%（真人 engaged 通常 40%+）
- CF 侧每日 8k-23k 请求，只有 ~100 能进 GA4

## 数据（Cloudflare GraphQL httpRequests1dGroups，2026-10-17 实时拉取）

| 日期 | requests | pageViews | uniques | pageView/request 比 |
|---|---|---|---|---|
| 2026-10-03 | 15,428 | 4,557 | 3,185 | 29.5% |
| 2026-10-04 | 12,688 | 2,288 | 2,615 | 18.0% |
| 2026-10-05 | 16,023 | 3,187 | 2,831 | 19.9% |
| 2026-10-06 | 8,991 | 1,620 | 2,262 | 18.0% |
| 2026-10-07 | 8,739 | 1,903 | 2,082 | 21.8% |
| 2026-10-08 | 11,739 | 4,219 | 2,971 | 35.9% |
| 2026-10-09 | 19,277 | 6,566 | 4,742 | 34.1% |
| 2026-10-10 | 18,296 | 5,941 | 3,988 | 33.0% |

## bot_traffic_pct 计算（多口径，写入 state.json）

- 口径A（GA4 engaged，commander 采用）：100% - 7.4% = **92.6%** 非 engaged（机器/无效流量）
- 口径B（CF 非页面请求）：100% - 4557/15428 = **70.5%** 请求非页面资源（JS/CSS/图片/API/爬虫）
- 口径C（CF→GA4 转化）：15,428 CF 请求 vs 893 GA4 sessions → 仅 5.8% 请求产生 GA4 session

**state.json bot_traffic_pct = 92.6**（口径A，GA4 engaged 反向；附口径B/C 在 note）

## 点名具体爬虫（阻塞项，如实记录）

- 当前 CF token（cfut_4svOam...）权限：`httpRequests1dGroups` 基础 Analytics 可用（date/sum/uniq），
  **无 httpRequestsAdaptiveGroups 维度权限**（clientRequestUserAgent/clientRequestPath/clientCountry 全 unknown field），
  **无 Logpush 权限**（zones/{zone}/logpush/jobs → 403）。
- 因此无法通过现有 token 拿到 UA/路径明细点名 GPTBot/CCBot/Amazonbot 等具体爬虫。
- **行动项（需指挥官/用户）**：
  1. 在 Cloudflare Dashboard 开启 Logpush（HTTP 请求日志，免费，目的地 R2/S3）后提供目的地信息；或
  2. 提供 Zone Analytics 全权限 API token（权限含 Analytics:Read + Logpush:Edit）；或
  3. Dashboard → Analytics → HTTP requests → 手动导出 UA Top 列表。

## 已落地动作（r28）

- P1 CF-20261017-002：robots.ts 增加 CCBot（Common Crawl，高消耗采集）/PetalBot/SeznamBot/YisouSpider/facebookexternalhit/ia_archiver（archive.org）等采集爬虫 Disallow，保留全部 AI 搜索 bot 允许（GEO 不倒退）——见 commit。
- P1 GA4-20261017-003：修复 GA4 page_view 埋点缺失（send_page_view:false 且无手动 pageview → landing page (not set)），新增路由级 page_view 事件带 page_location——见 commit。

## 数据来源

- Cloudflare GraphQL API（httpRequests1dGroups，2026-10-17 拉取）
- GA4 engaged 数据来自 commander_cf_probe_2026-10-17 的 cf_evidence
