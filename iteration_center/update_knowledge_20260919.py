"""Append Next.js Image + Font Optimization knowledge to knowledge_code.md
   and add actionable items to state.json next_iteration_focus."""
import json

KNOWLEDGE_FILE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\knowledge_code.md"
STATE_FILE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"

TODAY = "2026-09-19"

NEW_KNOWLEDGE = """
- [DATE] **Next.js Image Optimization + Font Optimization (App Router) — 权威来源：Next.js官方docs + Vercel官方docs**

  1. **next/image自动优化**：自动转WebP/AVIF格式，按设备尺寸返回正确大小的图，内置懒加载，用width/height防止CLS。来源：https://nextjs.org/docs/app/getting-started/images
  2. **`<img>`原生标签完全绕过Vercel图片优化管线**：直接用`<img>`不会走Next.js Image Optimization，不会自动压缩/转WebP/生成srcset。当前项目工具截图用的是原生`<img>`，这是~100个工具页>500KB的主要原因之一。来源：https://vercel.com/docs/image-optimization
  3. **`priority` prop = LCP图片preload**：首屏LCP图片（如工具页顶部screenshot）必须加`priority`，Next.js会自动加preload link标签，大幅提升LCP。不加的图片默认懒加载。来源：https://nextjs.org/docs/app/api-reference/components/image
  4. **`sizes` prop是关键，不是可选的**：没有`sizes`，浏览器默认按100vw选图，导致手机上下载2x甚至3x大的图。必须按实际渲染宽度设置，如sizes='(max-width: 768px) 100vw, 800px'。来源：https://nextjs.org/docs/app/api-reference/components/image#sizes
  5. **`unoptimized` prop用于SVG/GIF/小图(<1KB)**：对不需要优化的图（如SVG图标），加`unoptimized`跳过Vercel优化CPU，节省构建时间和函数调用。来源：https://nextjs.org/docs/app/api-reference/components/image#unoptimized
  6. **`quality` prop控制压缩质量**：默认75，截图类图片可降到60-70，视觉差异极小但文件体积减30-40%。来源：https://nextjs.org/docs/app/api-reference/components/image#quality
  7. **`fill` prop需要父容器position:relative**：当图片占满父容器时用`fill`，但父元素必须有明确的position:relative和尺寸，否则图片溢出。来源：https://nextjs.org/docs/app/api-reference/components/image#fill
  8. **本地图片（import的）不需要手动写width/height**：Next.js构建时自动检测尺寸。远程图片（在next.config.mjs配置remotePatterns的）必须手动传width/height。来源：https://nextjs.org/docs/app/getting-started/images
  9. **next/font/google自动自托管Google Fonts**：构建时下载字体文件，和静态资源一起serve，浏览器不向fonts.googleapis.com发请求，消除额外RTT，改善FCP/LCP。来源：https://nextjs.org/docs/app/getting-started/fonts
  10. **font-display必须用optional或swap**：Next.js官方警告不要用auto/block/fallback。optional对自定义字体最优（避免FOIT），swap对内容站点可接受。来源：https://nextjs.org/docs/messages/google-font-display
  11. **Variable Fonts推荐**：一个文件覆盖所有字重，不用为每个weight单独加载。来源：https://nextjs.org/docs/app/getting-started/fonts
  12. **next/font用CSS size-adjust实现零布局偏移**：字体文件构建时被调整metric，切换字体时不会导致文字跳动。来源：https://vercel.com/docs/frameworks/nextjs
  13. **next/font在build时内联font-face CSS**：不产生额外字体CSS网络请求，直接内联到HTML中。来源：https://nextjs.org/learn/seo/fonts
  14. **Vercel Image Optimization免费额度**：Pro计划每月有优化图额度。用unoptimized跳过不需要的图，用next.config.mjs的deviceSizes和imageSizes控制生成的尺寸变种，避免浪费。来源：https://vercel.com/docs/image-optimization
  15. **当前项目差距**：(a)工具页screenshot用原生img未优化→应迁到next/image；(b)需确认app/layout.tsx是否用next/font，如果还用link引Google Fonts要迁移；(c)首屏screenshot需加priority；(d)所有图片需加正确sizes。

  **落地计划（下次迭代执行）**：
  - 任务A：把app/tools/[slug]/page.tsx里的原生img截图改为next/image，加priority和sizes='(max-width: 768px) 100vw, 860px'，quality=70
  - 任务B：检查app/layout.tsx是否用next/font，如未用则迁移Inter字体
  - 任务C：SVG图标组件加unoptimized跳过图片优化
  - 任务D：在next.config.mjs配置deviceSizes减少多余的尺寸变种
""".replace("[DATE]", TODAY)

# Read and append to knowledge_code.md
with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if "Next.js Image Optimization + Font Optimization" in content:
    print("[SKIP] Knowledge already exists")
else:
    if "## 待补充" in content:
        content = content.replace("## 待补充\n", "## 待补充\n" + NEW_KNOWLEDGE + "\n")
    else:
        content += "\n\n## 待补充\n" + NEW_KNOWLEDGE + "\n"
    with open(KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] Appended knowledge to knowledge_code.md")

# Update state.json next_iteration_focus
with open(STATE_FILE, 'r', encoding='utf-8') as f:
    state = json.load(f)

new_items = [
    "P1-PERF-IMG-001: Migrate tool page screenshots from raw img to next/image with priority, sizes='(max-width: 768px) 100vw, 860px', quality=70. Expected: reduce ~100 tool pages from >500KB to <200KB, improve LCP.",
    "P1-PERF-FONT-001: Check if app/layout.tsx uses next/font/google; if still using link to Google Fonts, migrate to next/font with display='optional' for zero CLS and no external font requests.",
    "P2-PERF-SVG-001: Add unoptimized prop to all SVG icon components to skip Vercel image optimization CPU cost.",
    "P2-PERF-CONFIG-001: Configure next.config.mjs deviceSizes to avoid unnecessary image size variants (trim to 640/828/1200/1920 for our use case).",
]

existing_focus = state.get("next_iteration_focus", [])
already = any("P1-PERF-IMG-001" in str(item) for item in existing_focus)
if not already:
    state["next_iteration_focus"] = existing_focus + new_items
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    print(f"[OK] Added {len(new_items)} items to next_iteration_focus")
else:
    print("[SKIP] next_iteration_focus already has image optimization items")

print("Done.")
