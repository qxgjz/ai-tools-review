"""
Update state.json, iteration_log.json, and knowledge_code.md for iteration #71.
"""
import json
from datetime import datetime

today = "2026-09-18"
now_str = f"{today}T20:15:00+08:00"

# 1. Update state.json
with open('iteration_center/state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

state['current_iteration'] = 71
state['current_phase'] = "waiting_for_next_trigger"
state['last_deployment'] = f"{today} (perf: content-visibility:auto on tool pages)"
state['total_iterations_completed'] = 57
state['total_issues_fixed'] = 55
state['total_pages_optimized'] = state.get('total_pages_optimized', 4400) + 533

# Mark P0-MOBILE-001 as in_progress (content-visibility done, Lighthouse check pending)
for todo in state.get('current_todo', []):
    if todo['id'] == 'P0-MOBILE-001':
        todo['status'] = 'in_progress'
        todo['progress'] = 'Content-visibility:auto added to 4 below-the-fold sections on all 533 tool pages (commit ef3b56c1). Touch targets 44x44px and 16px mobile inputs already verified. Pending: Lighthouse mobile run to measure LCP improvement.'
        todo['started_at'] = now_str
        break

# Add completed todo entry
new_completed = {
    "id": "P0-PERF-001",
    "priority": "P0",
    "title": "Add content-visibility:auto to below-the-fold sections on tool pages",
    "source": "INP/performance learning from web.dev",
    "status": "completed",
    "iteration": 71,
    "completed_at": now_str,
    "result": "Added .cv-auto CSS class (content-visibility:auto + contain-intrinsic-size:auto 400px) to Alternatives, Similar Tools, Popular Tools, and Compare sections on all 533 tool detail pages. Expected LCP improvement 20-50% per web.dev data. TypeScript 0 errors. Live verified: cv-auto found 8x on /tools/chatgpt."
}
state.setdefault('completed_todo', []).insert(0, new_completed)

with open('iteration_center/state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("[OK] state.json updated (iteration 71)")

# 2. Update iteration_log.json
with open('iteration_center/iteration_log.json', 'r', encoding='utf-8') as f:
    log = json.load(f)

new_entry = {
    "iteration": 71,
    "timestamp": now_str,
    "task": "Content visibility performance optimization on tool detail pages",
    "changes": [
        "Added .cv-auto CSS utility class in app/globals.css (content-visibility: auto + contain-intrinsic-size: auto 400px)",
        "Applied cv-auto to 4 below-the-fold sections on all 533 tool detail pages (Alternatives, Similar Tools, Popular Tools, Compare)",
        "Audited image alt text: 0 missing out of 17 images across 104 blog posts (already clean)"
    ],
    "files_changed": [
        "app/globals.css",
        "app/tools/[slug]/page.tsx"
    ],
    "commit": "ef3b56c1e6fdb3c2ca16c5e93bfa35596164ecf4",
    "quality_gate": {
        "tsc_passed": True,
        "live_verified": True,
        "pages_200": ["homepage", "/tools/chatgpt", "/blog/chatgpt-vs-claude-2026-comparison"],
        "cv_auto_confirmed": "Found 8x on /tools/chatgpt after 270s deployment wait"
    },
    "next_planned": [
        "Run Lighthouse mobile performance check to measure LCP improvement",
        "P1-INDEX-001: Google indexing check (site: query vs sitemap URLs)",
        "P1-CONTENT-UPDATE-001: Content refresh mechanism for articles >3 months old"
    ]
}

if isinstance(log, list):
    log.insert(0, new_entry)
    # Keep last 20 entries
    log = log[:20]
elif isinstance(log, dict):
    log.setdefault('iterations', []).insert(0, new_entry)

with open('iteration_center/iteration_log.json', 'w', encoding='utf-8') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
print("[OK] iteration_log.json updated")

# 3. Append to knowledge_code.md
knowledge_entry = f"""

## 待补充

- [{today}] **学到：content-visibility: auto (CSS Containment Module Level 2)** — web.dev/Chrome团队官方性能优化技巧。对首屏以下的内容（Alternatives、Similar Tools、Compare等section）设置`content-visibility: auto`，浏览器会跳过渲染离屏内容，直到用户滚动到附近。配合`contain-intrinsic-size: auto 400px`预留空间防止CLS。实测对长列表/长文章页面LCP改善20-50%。来源：https://web.dev/articles/content-visibility。已落地：在app/tools/[slug]/page.tsx的4个below-fold section上加了cv-auto类，globals.css定义了.cv-auto工具类。下次可用到：Blog文章页的FAQ和Related Posts section、Category页的ToolList后半部分。

- [{today}] **踩坑：Vercel SSG部署700+页面需要3-5分钟才能全量上线** — 提交commit后90秒检查，cv-auto还没出现在HTML里；等了270秒（4.5分钟）才确认8个cv-auto类出现在/tools/chatgpt上。经验：SSG全量构建比ISR慢，验证线上时至少等3分钟再查，不要90秒就判定部署失败。
"""

with open('iteration_center/knowledge_code.md', 'r', encoding='utf-8') as f:
    kb = f.read()

if '## 待补充' in kb:
    kb = kb.replace('## 待补充', knowledge_entry.strip())
else:
    kb += '\n' + knowledge_entry

with open('iteration_center/knowledge_code.md', 'w', encoding='utf-8') as f:
    f.write(kb)
print("[OK] knowledge_code.md updated with new learnings")

print("\n[DONE] All state/log files updated for iteration 71")
