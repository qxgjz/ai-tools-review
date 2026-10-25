# GA4 数据真实性分析（2026-10-25 r61 架构师）

关联待办：P0-GA4-TRUTH-AUDIT-20261025（commander_data_crosscheck_20261025）
数据源：`gsc-ga4-report/ga4_2026-09-25_2026-10-22.md`（GA4 28d 报告，实拉）

## 结论（先行）
**GA4 存在显著 bot / 无 referrer 流量污染**，判定非真实用户流量：Direct 98.5%、Engaged 仅 8.3%、会话均长 10.2s、(not set) 落地页 19%、单日尖峰 893、Key Events 0。与 GSC 点击归零（Google 搜索无点击）交叉印证——GA4 的高 Sessions 不是搜索/引荐驱动的真实用户。

## 证据表
| 指标 | 值 | 判定 |
|---|---|---|
| Sessions（28d） | 3581 | 总量被污染放大 |
| Direct 渠道占比 | 3529 / 3581 = 98.5% | 无 referrer 流量主导（bot 特征） |
| Engaged Sessions | 299（8.3%） | 极低粘性 = 非真实用户 |
| Avg Session Duration | 10.2s | 短会话批量行为 |
| (not set) 落地页 | 672（19%） | 直接访问/无页面参数（无法归因） |
| 10-03 单日尖峰 | 893 | 尖峰 = 批量爬虫/扫描事件 |
| Key Events | 0 | 无任何转化行为 |
| GSC 30d Clicks | 0 | Google 搜索零点击，与 GA4 高流量矛盾 → 污染实锤 |

## 根因定位
1. **无 bot 过滤**：GA4 数据流未开启 Google bot 过滤（Google signals/bot filtering），爬虫（含 CF 边缘漏放的 bot、AI 扫描器、SEO 工具）全部计入 Sessions。
2. **无内部流量过滤**：若运营/开发本机访问未排除，也会计入（规模存疑，主因仍是 bot）。
3. **(not set) 672 来源**：无 referrer（直接输入 URL / 书签 / bot 无 referrer 请求）+ 无 UTM 参数 → GA4 归入 (not set)。其中 10-03 尖峰 893 为批量请求特征（同一 IP 段/UA 短时间大量 hit）。

## 动作（代码侧无待办，配置侧需人工）
1. **GA4 后台人工（必需）**：Admin → 数据流（数据流 ID 由 ga4_property_id 定位）→ 数据流详情 → 开启"机器人流量过滤"（Exclude known bots）+ 创建"内部流量"数据流标记排除本机/办公 IP。
2. **可选项**：开启 User-ID/增强型衡量中的"点击次数筛选"（排除 bot 的 hit）。
3. **验证**：开启后 48h 复查 Sessions 应显著下降（预期降至几百量级），Direct 占比回落，此时 GA4 才可作真实转化归因。
4. API 通道不可用：api_keys 无 GA4 Data API token（仅 measurement_id / property_id），无法程序化改数据流设置。

## 遗留说明
- GA4 Key Events 标记（Conversion）仍需后台人工（r60 已记录）。
- UTM 归因（campaign=ai_referral）解决 AI 引荐被归 Direct 的问题——属内容/外链窗口动作（r24 已记录）。

## 输出
本报告即 `gsc-ga4-report/ga4_pollution_analysis_20261025.md`。
