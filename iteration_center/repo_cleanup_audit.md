# Repo Cleanup Audit — 2026-09-16

**仓库**: qxgjz/ai-tools-review
**GitHub tree**: 483 entries
**本地仓库大小（排除 node_modules/.next/.git）**: 94.9 MB
**本地 .next build cache**: 1,220 MB（gitignored，不影响 repo）

---

## 一、可安全删（GitHub 上，无代码引用）

| 文件 | 大小 | 理由 |
|---|---|---|
| 根目录 40 个一次性 .py 脚本（check_*.py / fix_*.py / generate_*.py / add_*.py / analyze_*.py / dedupe-tools.py 等） | 170 KB | 已 grep 全仓 app/components/lib/scripts/package.json，0 引用；workflow 用的是 `.github/scripts/*.py`，不是根目录这些 |
| `data/ai-tools-461.json` | 243 KB | 旧版中间数据，已被 `data/tools.json`（8MB，533 个工具）取代；0 引用 |
| `top50_urls_for_gsc.txt` | ~5 KB | 一次性导出 |
| `daily_urls_for_gsc.txt` | ~5 KB | 一次性导出 |
| `iteration_center/seo_audit_20260916.md` | 5 KB | 一次性审计快照；`seo_check_latest.md` 由 workflow 持续覆盖更新，保留 |

**小计可释放 GitHub 体积**: ~430 KB（很小，但消除噪音）

---

## 二、谨慎删（下次再处理）

| 文件/目录 | 大小 | 为什么谨慎 |
|---|---|---|
| `prompts/` 目录（15 个 JSON） | ~80 KB | SEO 系统提示词库，本地自动化可能仍在引用，不删 |
| `iteration_center/iteration_log.json` | 94 KB | 迭代日志，历史记录，保留 |
| `iteration_center/state.json` | 18 KB | 状态机，保留 |
| `scripts/generate-pdf-guide.py` | 16 KB | lead magnet PDF 生成脚本，可能还会用 |
| `gsc-ga4-report/` | 2 文件 | GSC 报告，workflow 持续写入，保留 |

---

## 三、不能删

- `data/tools.json` (8MB) / `data/posts.json` (5MB) / `data/comparisons.json` / `data/alternatives.json` / `data/subcategories.json` / `data/traffic-ranking.json`
- `app/` (89) / `components/` (59) / `lib/` (5) / `types/` (2)
- `public/` (221 文件，含截图和静态资源)
- `scripts/` (8 文件，package.json `update` 脚本依赖)
- `.github/` (workflows + .github/scripts/)
- 所有配置文件：package.json / package-lock.json / next.config.mjs / tailwind.config.ts / postcss.config.mjs / tsconfig.json / vercel.json / .gitignore

---

## 四、本地垃圾（不在 GitHub，删了不影响线上，但释放本地磁盘）

| 路径 | 大小 | 说明 |
|---|---|---|
| `data/posts.json.bak_internal_links` | 4.0 MB | 9/13 旧备份，3 天前 |
| `data/posts.json.bak_iter30` | 4.1 MB | 9/13 旧备份 |
| `data/posts.json.bak_typography` | 4.0 MB | 9/13 旧备份 |
| `iteration_center/backup/posts_2026-09-16.json` | 4.5 MB | 今日备份，按规则保留 30 天 |
| `iteration_center/backup/tools_2026-09-16.json` | 8.0 MB | 今日备份，保留 |
| `content_drafts/screenshots/batch7/videos/dify.mp4` | 26 MB | 草稿视频，未被任何文章引用 |
| `content_drafts/screenshots/batch{5,6,7,10,10_v2}/` | ~39 MB | 草稿截图，已发布的文章用的是 public/screenshots/ 下的 webp |
| `.next/` | 1,220 MB | build cache，gitignored |

---

## 五、执行动作

1. 删除 GitHub 上：40 个根 .py + ai-tools-461.json + 2 个 txt + seo_audit_20260916.md
2. 删除本地：3 个 posts.json.bak_*（12 MB，9/13 旧备份）
3. 保留：今日 backup、content_drafts、prompts、scripts/
4. tsc --noEmit
5. GitHub Trees API 提交（在 tree 里把这些 path 的 sha 设为 null）
6. 等 60 秒部署
7. 抽查 5 个关键页面 200
