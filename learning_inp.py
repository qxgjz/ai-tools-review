"""Pure learning task: append INP knowledge to knowledge_code.md and add actionable items to state.json."""
import json
import io

KC = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\knowledge_code.md"
SJ = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"

ENTRY = """
- [2026-09-19] **Core Web Vitals: INP (Interaction to Next Paint) 完整优化指南 — 权威来源：Google官方web.dev/Codelabs + React官方docs + Vercel官方blog**

  1. **INP是什么**：INP测量用户交互（点击/点按/键盘）到浏览器下一帧绘制的延迟。2024年3月12日正式替代FID成为第三个Core Web Vital。来源：https://web.dev/articles/inp
  2. **INP阈值（p75真实用户）**：Good ≤200ms；Needs Improvement 200-500ms；Poor >500ms。Google Web Vitals团队数据显示INP从500ms优化到200ms可提升用户参与度22%。来源：https://web.dev/articles/evolving-inp-threshold
  3. **INP测量所有交互，不是只测第一次**：与FID只测首次输入不同，INP跟踪整个页面生命周期的所有click/tap/keyboard事件，报告最差的（p98）。来源：https://codelabs.developers.google.com/understanding-inp
  4. **INP的三个阶段**：① Input Delay（事件被浏览器接收前的排队延迟）② Event Processing Duration（事件处理器执行时间）③ Presentation Delay（浏览器绘制下一帧前的渲染时间）。三个阶段都要优化。来源：https://codelabs.developers.google.com/understanding-inp
  5. **Long Task >50ms是INP头号杀手**：任何阻塞主线程超过50ms的任务都会导致输入排队。优化方法：把长任务切成<50ms的小块，块之间用yield让浏览器绘制。来源：https://web.dev/articles/optimize-inp
  6. **scheduler.yield()（Chromium 115+）**：新API，把控制权交回浏览器立即绘制，然后恢复任务。比setTimeout更精确。降级方案：`if ('scheduler' in window && 'yield' in window.scheduler) window.scheduler.yield(); else new Promise(r => setTimeout(r, 0))`。来源：https://developer.chrome.com/docs/web-platform/scheduler-yield
  7. **React startTransition/useTransition（最重要的React优化）**：把非紧急的state更新包在startTransition里，React会把它们标记为可中断，浏览器优先响应用户输入。Vercel官方blog确认：如果慢操作是由state change引起的，包startTransition往往是最大单点修复。来源：https://react.dev/reference/react/useTransition ; https://vercel.com/blog/demystifying-inp-new-tools-and-actionable-insights
  8. **useDeferredValue**：把昂贵的派生渲染延迟到输入响应之后。适合搜索过滤、长列表渲染等场景——先响应用户输入，再慢慢渲染过滤结果。来源：https://react.dev/reference/react/useDeferredValue
  9. **web-vitals attribution build + LoAF API**：`web-vitals/attribution`构建用Long Animation Frames API精确告诉你哪个script/哪个event listener导致了慢INP，而不是只给一个数字。我们已部署WebVitalsReporter，下次可升级到attribution build拿到具体元凶。来源：https://codelabs.developers.google.com/measuring-inp
  10. **requestIdleCallback推迟非紧急工作**：analytics上报、logging、prefetching、预渲染等可以放到浏览器空闲时做，不阻塞交互。降级用setTimeout。来源：https://web.dev/articles/optimize-inp#defer-non-essential-work
  11. **事件委托减少监听器开销**：在父元素上放一个listener代替给每个子元素放listener，减少input delay。尤其适合我们工具页的Related Tools、Category列表。来源：https://web.dev/articles/optimize-inp#defer-non-essential-work
  12. **保持DOM小、避免强制reflow（layout thrashing）**：Presentation Delay和DOM复杂度正相关。避免read-write-read模式（循环里读offsetWidth再改style），用CSS containment隔离大列表。我们533个工具页每个渲染12个相关工具卡片，DOM不算大但要注意。来源：https://web.dev/articles/optimize-inp#reduce-presentation-delay
  13. **Server Components减少客户端JS**：Client Component越少，hydration越快，input delay越低。我们的SSG已帮大忙，但FAQ手风琴、CTA追踪、Newsletter表单都是'use client'组件，要确保它们是小型leaf组件，不拖累整页hydration。来源：https://nextjs.org/docs/app/building-your-application/rendering/server-components
  14. **Debounce/Throttle输入处理器**：搜索框、slider等不要每次keystroke都跑重活，debounce 100-300ms。来源：https://web.dev/articles/optimize-inp#defer-non-essential-work
  15. **Lighthouse TBT ≠ INP**：Lab工具（Lighthouse）测的是Total Blocking Time，不是真实INP。必须用RUM（web-vitals库）收集真实用户数据。我们已在WebVitalsReporter里onINP上报GA4，下一步要去GSC的Core Web Vitals报告看我们真实p75 INP是多少。来源：https://web.dev/articles/inp#what-is-inp

  **落地计划（下次迭代执行）**：
  - 任务A：把WebVitalsReporter升级到web-vitals/attribution build，拿到具体哪个client component导致慢INP（不改业务代码，只换import路径+加attribution:true）
  - 任务B：检查'use client'组件清单（FAQ手风琴、AffiliateCTA tracking、NewsletterSignup、WebVitalsReporter），把非紧急的trackCtaClick/analytics上报包进requestIdleCallback，不阻塞click事件
  - 任务C：GSC Core Web Vitals报告里查我们真实p75 INP，确认是Good/Needs Improvement/Poor，再决定要不要做startTransition
  - 任务D：Category页和Tools列表的渲染，如果单次渲染>50ms，用React.memo + useDeferredValue优化

"""

# ---- Append to knowledge_code.md ----
with io.open(KC, 'r', encoding='utf-8') as f:
    kc = f.read()

# Insert after the first "## 待补充" heading (the one at line 181)
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

# ---- Update state.json next_iteration_focus ----
with io.open(SJ, 'r', encoding='utf-8') as f:
    state = json.load(f)

# Find or create next_iteration_focus
nif = state.get("next_iteration_focus", [])
if not isinstance(nif, list):
    nif = []

new_items = [
    {
        "id": "P1-PERF-INP-001",
        "source": "learning: INP optimization 2026-09-19",
        "title": "Upgrade WebVitalsReporter to attribution build to identify slow INP sources",
        "how_to": "Change import from 'web-vitals' to 'web-vitals/attribution'; pass attribution:true to onINP/onLCP/onCLS; log attribution to GA4. No business code change.",
        "priority": "P1"
    },
    {
        "id": "P1-PERF-INP-002",
        "source": "learning: INP optimization 2026-09-19",
        "title": "Wrap non-urgent CTA click tracking in requestIdleCallback",
        "how_to": "In components/monetization/AffiliateCTA.tsx trackCtaClick(), defer window.va.track and CustomEvent dispatch via requestIdleCallback (fallback setTimeout 0), so click→new window opens immediately.",
        "priority": "P1"
    },
    {
        "id": "P2-PERF-INP-003",
        "source": "learning: INP optimization 2026-09-19",
        "title": "Check GSC Core Web Vitals report for real p75 INP",
        "how_to": "Read GSC > Core Web Vitals > INP. If Poor (>500ms), profile which pages; if Good, no code change needed.",
        "priority": "P2"
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
