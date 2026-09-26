"""Update state.json: mark 2 completed tasks, bump iteration to 75."""
import json
from datetime import datetime

path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"

with open(path, "r", encoding="utf-8") as f:
    state = json.load(f)

completed = {
    "P1-PERF-INP-002": "Wrapped AffiliateCTA trackCtaClick in requestIdleCallback (setTimeout 0 fallback). Click→navigation path is no longer blocked by va.track + CustomEvent dispatch. Commit ebae1f4c. Expected: INP improvement on tool pages with affiliate CTAs.",
    "GHACT-CRON-001": "Staggered 4 GitHub Actions cron times off top of hour: context-update 17:17, gsc-fetch 18:23, seo-check 19:11, index-monitor 20:37 UTC. Uptime monitor kept */10. Commits 3386fd9a, c9bca244, 9053c33d, ec20ca73. Expected: reduced queuing delay at top of hour.",
}

new_current = []
new_completed = list(state.get("completed_todo", []))
existing_ids = {t.get("id") for t in new_completed}

# Scan current_todo for matching items; also add new entries if not present
for item in state.get("current_todo", []):
    new_current.append(item)

# Add completed entries
for tid, desc in completed.items():
    if tid in existing_ids:
        continue
    new_completed.append({
        "id": tid,
        "priority": "P1",
        "title": tid,
        "status": "completed",
        "completed_at": "2026-09-20T01:12:00+08:00",
        "completed_iteration": 75,
        "result": desc,
    })

state["current_todo"] = new_current
state["completed_todo"] = new_completed
state["current_iteration"] = 75
state["last_updated"] = "2026-09-20"
state["last_run"] = "2026-09-20T01:12:00+08:00"
state["latest_commit"] = "ec20ca735f4567e03a72c624f8360c2eb60cbd57"
state["last_iteration_summary"] = "P1-PERF-INP-002 (requestIdleCallback for CTA tracking) + GHACT-CRON-001 (staggered cron times). tsc 0 errors. 3 key pages 200."
state["total_issues_fixed"] = state.get("total_issues_fixed", 60) + 2

with open(path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("state.json updated. iteration=75, completed=", len(new_completed))
