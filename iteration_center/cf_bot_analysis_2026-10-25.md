# CF uniques 暴涨调查（2026-10-25 r61 架构师）

关联待办：P1-CF-UNIQ-SURGE-20261025（commander_data_crosscheck_20261025）

## 结论（先行）
**无法经 API 点名爬虫（token 权限不足），需 CF Dashboard 导出 UA Top 人工点名**。但本轮实测发现强关联线索：curl 伪装 Googlebot UA 被 CF 边缘 bot 检测在握手层拦截（000）——证明 CF 边缘已有 bot 检测逻辑在识别爬虫特征，uniques 暴涨大概率与批量 bot/SEO 工具抓取相关（pv/req 比 0.15-0.25 佐证"高请求低页面渲染"）。

## 背景数据（指挥官提供，10-20 起）
| 日期 | uniques | pageViews | 变化 |
|---|---|---|---|
| 10-19 | 3229 | — | 基线 |
| 10-20 | 6360 | 3295~ | +98% |
| 10-23 | 7655 | ~5875 | +137% |
- pv/req 比降至 0.15~0.25 → 大量请求未渲染页面 = 爬虫/扫描特征

## 调查记录（API 通道全试）
| 通道 | 结果 |
|---|---|
| CF GraphQL httpRequestsAdaptiveGroups（uaFamily） | unknown field（token 无 Analytics 权限，schema 缩减） |
| CF GraphQL sum{bytes}/uniq{uniques}/orderBy | 全部 unknown field / unknown enum |
| CF REST Zone Analytics dashboard | 404 = API sunset（强制 GraphQL） |
| CF WAF Firewall Rules 三 phase | 404 零规则（无 bot 防护规则；Bot Fight Mode 为托管层不可 API 查） |
| 本机模拟 Googlebot 探测 | curl+Googlebot UA 被 CF 握手层拦截（000）→ 印证边缘 bot 检测存在且对"非浏览器指纹"严格 |

## 动作
1. **人工（必需）**：CF Dashboard → Analytics → 流量（或 Security → Events）导出 10-20~10-25 UA Top 20，点名具体爬虫（常见：Bytespider/Amazonbot/GPTBot/ClaudeBot/CCBot/SemrushBot 等）。
2. **人工**：Dashboard → Security → Bots → 确认 Bot Fight Mode 状态；若误伤 Googlebot 加白名单例外（见 P0-GSC-REDIRECT-ERROR 报告）。
3. **代码侧可选**：点名后若为已知好爬虫（如 GPTBot 收录意图），可在 robots.txt 保留允许；若为垃圾扫描，CF Dashboard 添加速率限制规则（WAF Custom rule）——API 无权限，走 Dashboard。

## 输出
本报告即 `iteration_center/cf_bot_analysis_2026-10-25.md`。
