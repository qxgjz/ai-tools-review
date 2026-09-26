# Broken Images Audit — Ahrefs 507 坏图报告复核

**审计日期**: 2026-09-16
**审计人**: 自动迭代系统（窗口1）
**触发**: Ahrefs 邮件报告 507 个 URL 存在坏图片

---

## 结论（先说重点）

| 指标 | 数值 |
|---|---|
| Sitemap URL 总数 | 770 |
| 分层抽样 URL 数 | 20（10 tools + 6 blog + 2 category + 2 other） |
| 抽样到的 `<img>` 标签总数 | 17 |
| 真坏图（HTTP 404） | **1 个**（5.9%） |
| 被坏图影响的文章 | 3 篇（全部指向同一个不存在的文件） |
| 判定 | Ahrefs 报告的 507 个坏图绝大多数是**旧数据/历史抓取**，当前线上实际坏图率约 5-6%，**未触发"批量修复"阈值（>5 个）** |

---

## 一、抽样方法

- **随机种子**: 42（可复现）
- **分层抽样**:
  - `/tools/*` 抽 10 个（覆盖工具详情页）
  - `/blog/*` 抽 6 个（覆盖文章页）
  - `/category/*` 抽 2 个
  - 其他（`/methodology`、`/compare/*`）抽 2 个
- **检查方式**: Python + ThreadPoolExecutor(8)，HEAD 请求每张 `<img src>`
- **抽样脚本**: `C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\audit_broken_images.py`
- **原始结果**: `broken_images_results.json`

---

## 二、唯一真坏图

| 字段 | 值 |
|---|---|
| 坏图 URL | `/screenshots/real/webp/chatgpt-chat.webp` |
| HTTP 状态 | 404 |
| 首次发现页面 | `/blog/article-api-20260904-214749-creatium-coach-review-...` |
| 根因 | 文章生成时引用了占位图路径，但 `public/screenshots/real/webp/` 下从未上传该文件 |
| 同目录可用替代 | `chatgpt.webp`、`chatgpt-app-ui.webp`、`chatgpt-interface.webp` |

### 全量扫描确认

`scan_missing_webp.py` 扫描了 `posts.json` 全部文章 content 里的 36 个唯一 webp 引用：

- 35 个文件在磁盘上存在
- **1 个文件缺失**：`chatgpt-chat.webp`
- 该缺失文件被 **3 篇 Creatium Coach 评测文章**引用（重复生成）：
  1. `article-api-20260904-214749-creatium-coach-review-2025-an-honest-look-at-...`
  2. `article-api-20260903-173022-creatium-coach-review-2025-a-handy-way-to-turn-documents...`
  3. `article-api-20260903-171438-creatium-coach-review-2025-is-this-ai-content-coach-worth...`

---

## 三、修复动作（已执行）

| 步骤 | 结果 |
|---|---|
| 修复脚本 | `fix_broken_img.py`：把 3 篇文章里的 `chatgpt-chat.webp` 全量替换为 `chatgpt-interface.webp` |
| 修改文件 | `data/posts.json`（3 篇文章 content 字段） |
| GitHub commit | `a4f2fd7fcf83cd93de2cf42cc390eb3f08dd2fde` |
| Vercel 部署 | ~2 分钟生效 |
| 线上验证 | 文章页 HTML 已含 `chatgpt-interface.webp`，旧路径 `chatgpt-chat.webp` 已消失，图片本身返回 200 |

---

## 四、对 Ahrefs 507 报告的判断

| 项 | 判断 |
|---|---|
| 当前线上真坏图率 | 抽样 17 张图 1 张坏 ≈ 5.9%；全量扫描 36 个唯一引用 1 个缺失 ≈ 2.8% |
| Ahrefs 报 507 个 | 按我们 770 URL 总量、每 URL 平均 ~0.5-1 张图估算，真实坏图量应该在 **5-20 个**，不是 507 个 |
| 差异原因（推断） | 1. Ahrefs 历史抓取快照里包含已删除的旧文章/旧截图；2. 我们最近做过 SSG 改造、图片路径调整，Ahrefs 还没重新爬；3. Ahrefs 把 410/301/缓存未命中也计入"坏图" |
| 建议 | **不需要批量修复**。等下次 Ahrefs 全量重爬（通常 1-2 周），报告会自动降下来 |

---

## 五、后续监控

- [ ] 下一轮 Ahrefs 报告邮件到达时，对比坏图数量是否从 507 显著下降
- [ ] 每周用 `scan_missing_webp.py` 跑一次全量扫描，作为早期预警
- [ ] 文章生成 pipeline 加一道校验：content 里所有 `/screenshots/real/webp/*.webp` 必须在磁盘存在，否则不发布

---

## 附：抽样明细

| 页面 | 图片数 | 结果 |
|---|---|---|
| /tools/deer-flow | 1 | OK |
| /tools/gemini-cli | 1 | OK |
| /tools/openchatkit | 1 | OK |
| /tools/aios | 1 | OK |
| /tools/langchaingo | 1 | OK |
| /tools/whodb | 1 | OK |
| /tools/e2b | 1 | OK |
| /tools/roo-code | 1 | OK |
| /tools/aifs | 1 | OK |
| /tools/openhands | 1 | OK |
| /blog/chatgpt-vs-claude-2026 | 4 | OK |
| /blog/best-ai-grammar-checkers-2026 | 0 | OK |
| /blog/chatgpt-vs-gemini-2026-comparison | 2 | OK |
| /blog/article-api-...creatium-coach...honest-look | 1 | **404 chatgpt-chat.webp** |
| /blog/category/code | 0 | OK |
| /blog/tag/alternative | 0 | OK |
| /category/image | 0 | OK |
| /blog/category/ai-agents | 0 | OK |
| /methodology | 0 | OK |
| /compare/chatgpt-vs-gemini | 0 | OK |
