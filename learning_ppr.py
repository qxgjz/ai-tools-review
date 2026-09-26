"""Pure learning task: append Next.js PPR/Cache Components knowledge to knowledge_code.md and state.json."""
import json, io

KC = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\knowledge_code.md"
SJ = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"

ENTRY = """
- [2026-09-19] **Next.js Partial Prerendering (PPR) + Cache Components 完整指南 — 权威来源：Next.js官方docs + Vercel官方docs**

  1. **PPR是什么**：Partial Prerendering在同一路由里同时组合静态shell和动态流式内容。build时生成静态HTML shell + 序列化的postponed state blob；请求时shell立即从CDN发出，动态部分流式填充。来源：https://nextjs.org/docs/app/getting-started/partial-prerendering
  2. **Next.js 16把PPR转正**：从实验性 `experimental.ppr` 变成Cache Components默认模型。升级到Next.js 16后删掉旧flag，在next.config里开 `cacheComponents: true`。来源：https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents
  3. **静态shell定义**：在任何async work resolve之前渲染的所有内容 = layouts、navigation、`<Suspense>`的fallback UI。这些在build时prerender，请求时从edge CDN立即发出（~32-65ms TTFB）。来源：https://nextjs.org/docs/app/guides/streaming
  4. **动态holes = `<Suspense>`边界**：依赖request-time数据的组件必须包在`<Suspense>`里，fallback进入静态shell，真正的数据在请求时并行stream进来。多个Suspense边界并行加载。来源：https://nextjs.org/docs/app/getting-started/cache-components
  5. **`use cache`指令**：在组件/函数顶部写 `"use cache"`，输出会被缓存并进入静态shell。适合所有用户共享的数据（如我们的工具列表、分类导航）。来源：https://nextjs.org/docs/app/api-reference/directives/use-cache
  6. **新鲜数据不要use cache**：需要每次请求都新鲜的数据（如个人化推荐），用`<Suspense>`包，不要加use cache。官方明确：async API/db/fetch需要fresh data时，不use cache，包Suspense。来源：https://nextjs.org/docs/app/getting-started/caching
  7. **loading.js自动成为Suspense边界**：Next.js里放一个 `loading.tsx` 文件就自动把整个segment包进`<Suspense>`，它的loading UI就是静态shell的fallback。来源：https://preview.nextjs.org/docs/app/guides/building
  8. **SEO好处**：静态shell是完整HTML，立即发给Googlebot，不需要等JS hydration。这解决了"CSR/SSR内容需要爬虫等JS"的老问题——Googlebot直接看到shell里的所有内容。来源：https://nextjs.org/docs/app/getting-started/caching
  9. **LCP好处**：LCP元素如果在静态shell里（如hero图、H1、产品图），它立即paint，LCP从几百ms降到几十ms。官方数据：把LCP元素放进shell后LCP从~650ms降到65ms。来源：https://nextjs.org/docs/app/guides/streaming
  10. **postponed state是什么**：build时序列化的RSC payload blob，客户端导航时hydrate用。直接访问URL时发HTML shell，客户端内部跳转时用postponed state。来源：https://preview.nextjs.org/docs/app/guides/ppr-platform-guide
  11. **ISR + Cache Components**：即使URL不在generateStaticParams里，第一次访问也能拿到即时shell（App Shell模式），动态内容stream进来。这对我们533个工具页+大量长尾页特别有用。来源：https://preview.nextjs.org/docs/app/guides/incremental-static-regeneration-cache-components
  12. **Vercel官方确认PPR替代Edge SSR**：PPR不阻塞serverless cold start的TTFB，比Edge SSR更省资源。Vercel的frontend cloud直接从edge cache发shell。来源：https://vercel.com/docs/frameworks/full-stack/nextjs
  13. **静态vs动态是光谱不是二元**：Next.js 16的渲染哲学——一个页面可以既有静态shell、又有cached function、又有动态个人化部分。不再需要"全站SSG或全站SSR"的选择。来源：https://nextjs.org/docs/app/guides/rendering-philosophy
  14. **迁移要点**：① 升级Next.js到16 ② next.config开 `cacheComponents: true` ③ 删 `experimental.ppr` flag ④ 检查每个路由有没有Suspense边界/loading.tsx ⑤ fresh数据的组件包Suspense，shared数据加use cache。来源：https://nextjs.org/docs/app/guides/migrating-to-cache-components
  15. **不阻塞主线程**：因为shell是CDN直接发的HTML，不经过serverless function，cold start不影响首屏。这对Vercel免费额度紧张的我们特别友好——shell不消耗ISR reads/serverless invocation。来源：https://vercel.com/resources/how-vercel-improves-your-websites-search-engine-ranking

  **落地计划（下次迭代执行）**：
  - 任务A：评估Next.js 16升级可行性（当前我们是Next.js 14.2.5），查Breaking Changes和我们用的依赖兼容性，出一份升级checklist
  - 任务B：在不升级的前提下，先用现有Next.js 14的Suspense + loading.tsx模式，把/blog/[slug]和/tools/[slug]里的非关键数据（Related Tools、FAQ手风琴）包进Suspense，让首屏HTML立即发出
  - 任务C：把tools.json里的静态工具列表用React.cache（不是use cache，Next.js 14版）包一层，减少重复render
  - 任务D：Lighthouse跑一次，确认我们LCP元素（H1、hero screenshot）已经在首屏HTML里，不需要客户端JS

"""

with io.open(KC, 'r', encoding='utf-8') as f:
    kc = f.read()

marker = "## 待补充\n"
idx = kc.find(marker)
if idx == -1:
    print("[ERR] no 待补充 marker")
else:
    insert_at = idx + len(marker)
    new_kc = kc[:insert_at] + ENTRY + kc[insert_at:]
    with io.open(KC, 'w', encoding='utf-8') as f:
        f.write(new_kc)
    print("[OK] knowledge_code.md appended")

with io.open(SJ, 'r', encoding='utf-8') as f:
    state = json.load(f)

nif = state.get("next_iteration_focus", [])
if not isinstance(nif, list):
    nif = []

new_items = [
    {
        "id": "P2-PERF-PPR-001",
        "source": "learning: Next.js PPR/Cache Components 2026-09-19",
        "title": "Evaluate Next.js 16 upgrade feasibility for PPR/Cache Components",
        "how_to": "Check Next.js 14.2.5 -> 16 Breaking Changes, dependency compatibility (Tailwind, next-seo, all custom components), produce a migration checklist. Don't upgrade until checklist is green.",
        "priority": "P2"
    },
    {
        "id": "P1-PERF-SUSPENSE-001",
        "source": "learning: Next.js PPR/Cache Components 2026-09-19",
        "title": "Wrap non-critical blog/tool page data in Suspense so static HTML shell ships instantly",
        "how_to": "On /blog/[slug] and /tools/[slug], wrap Related Tools list and FAQ accordion in <Suspense fallback={<Skeleton/>}>. Add loading.tsx at blog and tools segment levels if missing. Goal: LCP element (H1 + hero image) in first HTML byte.",
        "priority": "P1"
    },
    {
        "id": "P3-PERF-REACTCACHE-001",
        "source": "learning: Next.js PPR/Cache Components 2026-09-19",
        "title": "Wrap tools.json lookups in React.cache to dedupe renders",
        "how_to": "In Next.js 14, use React.cache() around getToolBySlug()/getCategoryTools() so multiple components in the same request don't re-read and re-process tools.json.",
        "priority": "P3"
    }
]

existing_ids = {item.get("id") for item in nif if isinstance(item, dict)}
added = 0
for item in new_items:
    if item["id"] not in existing_ids:
        nif.append(item)
        added += 1

state["next_iteration_focus"] = nif
with io.open(SJ, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] state.json next_iteration_focus: added {added} new items (total {len(nif)})")
