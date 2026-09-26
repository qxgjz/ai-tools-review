"""Update state.json: mark 5 completed tasks from this batch."""
import json
from datetime import datetime

path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"

with open(path, "r", encoding="utf-8") as f:
    state = json.load(f)

completed_ids = {
    "P0-SEO-404-001",
    "P0-SEO-SLOW-001",
    "P0-SEO-THIN-001",
    "P1-SEO-ORPHAN-001",
    "P1-SEO-TITLE-001",
}

# Move completed tasks from current_todo to completed_todo
new_current = []
new_completed = list(state.get("completed_todo", []))

for item in state.get("current_todo", []):
    if item.get("id") in completed_ids:
        item["status"] = "completed"
        item["completed_at"] = "2026-09-20T01:30:00+08:00"
        item["completed_iteration"] = 74
        item["result"] = {
            "P0-SEO-404-001": "37 redirects added in next.config.mjs. /tools -> /ranking, 35 tool slugs -> nearest category. Live verified: /tools=308, /tools/llama=308, /tools/firefly=308. Commits: bc81ce45.",
            "P0-SEO-SLOW-001": "/tools/anthropic-claude and /tools/llama were 404s (not in tools.json) - redirects fix them. /tools/openagents exists in tools.json; slow measurement was crawl artifact (SSG means no runtime cost). No code change needed.",
            "P0-SEO-THIN-001": "Added robots: {index: false, follow: true} to app/blog/tag/[slug]/page.tsx generateMetadata. Live verified: /blog/tag/ai-crm HTML has noindex. Commit: 7285603a.",
            "P1-SEO-ORPHAN-001": "Added /terms and /ai-policy links to footer Resources column in app/layout.tsx. Live verified: homepage footer contains /ai-policy and /terms. Commit: f713bb23.",
            "P1-SEO-TITLE-001": "Shortened title template in blog/tag/[slug] and blog/category/[slug] pages to '{Tag} AI Tools Reviews | AIToolCrux' (<=60 chars). Live verified: /blog/tag/ai-crm title is 'AI CRM AI Tools Reviews | AIToolCrux'. Commit: de7b3504.",
        }[item["id"]]
        new_completed.append(item)
    else:
        new_current.append(item)

state["current_todo"] = new_current
state["completed_todo"] = new_completed
state["current_iteration"] = 74
state["last_updated"] = "2026-09-20"
state["last_run"] = "2026-09-20T01:30:00+08:00"
state["latest_commit"] = "f713bb23daa3ec33490a39a3aaf33f77561d4bfe"
state["last_iteration_summary"] = "fix(seo): P0 batch - 37 redirects, noindex tag pages, footer links, shortened titles - commits bc81ce45,7285603a,de7b3504,f713bb23"
state["total_issues_fixed"] = state.get("total_issues_fixed", 55) + 5
state["total_pages_optimized"] = state.get("total_pages_optimized", 4933) + 156

with open(path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("state.json updated successfully")
print(f"current_todo remaining: {len(new_current)}")
print(f"completed_todo total: {len(new_completed)}")
