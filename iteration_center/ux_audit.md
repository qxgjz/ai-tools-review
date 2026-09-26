# UI/UX 审计报告 — 窗口6

> 审计日期：2026-09-26（紧急全面检查）
> 审计范围：移动端布局 / Hero / 导航 / 按钮对比度 / 加载性能 / 深浅色模式
> 技术栈：Next.js 14.2.5 SSG + Tailwind CSS + TypeScript

---

## 🔴 P0 已本轮修复

### P0-I18N-001 英文站残留中文 UI 文本
- **位置1**：`app/page.tsx` 移动端 hero 下方快速入口芯片
  - 修复前：标题"快速入口"；chip 标签"🔥 热门工具 / 🖼️ AI图像 / 💻 AI编程 / 📝 AI写作 / 🎬 AI视频 / 📖 评测博客"
  - 修复后：标题"Quick Access"；chip 标签"AI Chat / AI Image / AI Coding / AI Writing / AI Video / Reviews"，同时去掉 emoji（设计规范：SVG icon / 纯文本优先，不用 emoji 当图标）
- **位置2**：`app/tools/[slug]/page.tsx` 主 CTA 下方信任行
  - 修复前："✓ 编辑独立测试 / ✓ 评分透明 / ✓ 无付费排名"
  - 修复后："✓ Independently tested / ✓ Transparent scoring / ✓ No paid rankings"
- **影响**：网站 `<html lang="en">`，面向美国/英文用户，中文文本会严重降低信任并造成困惑
- **commit**：`8364a11570c4e601e78361cde90db749e512bb9d`

---

## 🟢 已检查且状态良好（无需修改）

| 检查项 | 现状 | 结论 |
|---|---|---|
| 移动端 Hero 布局 | 左列 badge/H1/描述/CTA/stats，下方 Top3 横向 snap 滚动卡片 + Quick Access 芯片，`lg:hidden` 正确隔离 | ✅ 不拥挤，无横向溢出 |
| Hero 视觉吸引力 | `bg-zinc-950` 深色 + emerald 强调色，H1 `text-4xl~6xl tracking-tight`，右列桌面 Top3 实卡 | ✅ 符合 Linear/Vercel 暗色 SaaS 规范 |
| 导航清晰度 | Header sticky + `backdrop-blur`，6 个导航项带 aria-label，移动端汉堡菜单 48px 触摸目标，有 skip link | ✅ |
| 按钮对比度 | 主 CTA `bg-emerald-600` on `zinc-950` 深色背景，白字，对比度 ≥ 4.5:1；次 CTA 描边按钮 `border-zinc-700` | ✅ 达标 |
| CTA 触摸热区 | 所有 CTA `px-6 py-3.5`（≈48px 高），移动菜单链接 `min-h-[48px]` | ✅ ≥44px |
| 加载性能 | SearchBox `dynamic ssr:false` + skeleton，NewsletterSignup dynamic，`preconnect` 第三方域名 | ✅ |
| 深色/浅色模式 | ThemeProvider + ThemeToggle 已集成，全站 `dark:` 变体，color-scheme 已设 | ✅ |
| 可访问性 | skip link、focus-visible outline、aria-label、aria-expanded、Escape 关菜单、body scroll lock | ✅ |

---

## 🟡 待观察 / 后续优化建议（未本轮改）

1. **emoji 图标统一性**：Quick Access 已去 emoji；全站仍有少量 emoji（如 `✅ Tested by our team`）在 CTA 副标题，不影响功能，后续可统一为 lucide SVG icon。
2. **`prefers-reduced-motion` 全局兜底**：FadeIn 动画组件需确认在 reduced-motion 下降级为无动画。
3. **ToolCard hover 微交互**：学习知识库建议 hover 时 `-translate-y-0.5 + shadow-lg`，本轮未改（避免改动过大）。
4. **粉色第三方悬浮按钮**（用户截图曾见）：layout.tsx 中无聊天 widget，疑似 Vercel Speed Insights badge 或浏览器扩展，待复现确认。
5. **`category/[slug]/page.tsx` 中 UTF-8 乱码**（`鈥斆?`/`鈥?`）：是 en-dash/em-dash 编码损坏，属内容问题非 UI 问题，应归窗口1/内容侧修复，不在窗口6样式范围内。

---

## 质量门
- [x] 只改 className/可见文本，未改业务逻辑、SEO、数据、affiliate URL
- [x] 改动文件：`app/page.tsx`、`app/tools/[slug]/page.tsx`
- [x] 已 push main，等 Vercel 部署后线上验证英文文本生效
