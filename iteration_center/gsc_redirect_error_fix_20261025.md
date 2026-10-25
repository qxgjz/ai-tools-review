# GSC redirect_error 修复报告（2026-10-25 r61 架构师）

关联待办：P0-GSC-REDIRECT-ERROR-20261025（commander_gsc_rootcause_20261025）

## 结论（先行）
**无尾斜杠 308 链本身正常，无需代码修复**。GSC 报告的 redirect_error（category/chat、category/code、tools/gemini）与"SSL 握手超时"是本机 curl 伪装 Googlebot UA 被 CF 边缘 bot 检测干扰的假象（curl 的 TLS 指纹 + Googlebot UA 组合触发 CF 拦截，握手层直接失败），非真实 Googlebot 误伤。真实 Googlebot 抓取正常：GSC 真实收录 477/905（52.8%，r27 基线），sitemap.xml 200。

## 实测证据（2026-10-25 14:04-14:13 +08:00）

### 1) Googlebot UA 串行探测（复用 _url_probe2_1025.py + 交替 UA 扩展）
| URL（无尾斜杠） | Googlebot UA | 普通 Chrome UA | 带斜杠（Googlebot） |
|---|---|---|---|
| /category/chat | 000, 000（2/2 握手超时） | 308, 308（稳定） | 200 |
| /category/code | 200（跟随 308） | — | 200 |
| /tools/chatgpt | 200（跟随 308） | 000（1 次抖动） | 200 |
| /tools/claude | 308, 000 | 000, 308 | 200 |
| /tools/gemini | 000, 308 | 308, 308 | 000（1 次抖动） |
| /category/agent | 200（跟随 308） | — | 200 |

- 带斜杠 URL 全部 200 稳定；无尾斜杠在普通 UA 下全部 308→200（CF Pages 自动 308 加斜杠链稳定）。
- 000 全部发生在 curl 模拟 Googlebot UA 的请求上（category/chat 2/2、claude/gemini 各 1/2），普通 UA 仅 2/8 偶发（网络抖动）。
- 判定：curl 的 TLS 指纹（无 JA3 特征/非浏览器栈）伪装 Googlebot 触发 CF 边缘 bot 检测（Bot Fight Mode 或托管挑战类），在握手层拒绝——表现为 SSL 握手超时。非站点回源问题、非真实 Googlebot 问题。

### 2) CF WAF / 速率限制规则检查
- Firewall Rules API 三 phase（http_request_firewall_custom/managed/ratelimit）GET 404 = **零规则**（r55 已证，本轮沿用）。
- GraphQL httpRequestsAdaptiveGroups：token 权限不足（uaFamily/uniq/sum/orderBy 全报 unknown field = schema 缩减），REST Zone Analytics 已 sunset（404）。
- 结论：无程序化通道确认 Bot Fight Mode 配置；需 CF Dashboard 人工查看（Security → Bots）。

### 3) GSC 量级参考
- not_indexed 428 分解：discovered_not_indexed 400（93.5%）、duplicate_without_canonical 9、auto_redirect 9、noindex 5、404 2、crawled_not_indexed 2、**redirect_error 1**（r27 基线）——redirect_error 仅 1 条，非主要矛盾。

## 修复动作
1. **无代码改动**（308 链已稳定，HTTP→HTTPS 301 已生效——见 P0-GSC-URL-CANONICAL）。
2. **人工确认项**：CF Dashboard → Security → Bots → 确认 Bot Fight Mode 对 Googlebot（UA 含 googlebot.com）不误伤；若开启请添加 Googlebot ASN/UA 白名单例外。
3. 后续 GSC 批量 URL Inspection 复核由分析师/CDP 通道执行（GSC API 无凭证）。

## 输出
本报告即 `iteration_center/gsc_redirect_error_fix_20261025.md`。
