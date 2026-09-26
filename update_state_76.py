"""Update iteration_log.json and state.json after perf fixes."""
import json
from datetime import datetime
from pathlib import Path

base = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center")

# 1. Update iteration_log.json
log_path = base / "iteration_log.json"
log = json.loads(log_path.read_text(encoding="utf-8"))

new_entry = {
    "iteration": 76,
    "date": "2026-09-20",
    "tasks_completed": [
        {
            "id": "P2-PERF-FONT-001",
            "title": "Remove unused Google Fonts preconnect/dns-prefetch in layout.tsx",
            "files_changed": ["app/layout.tsx"],
            "commit": "7a16dc45",
            "result": "Removed preconnect to fonts.gstatic.com and dns-prefetch to fonts.googleapis.com; geist/font self-hosts fonts, so these were unnecessary DNS overhead."
        },
        {
            "id": "P2-PERF-CONFIG-001",
            "title": "Trim deviceSizes and imageSizes in next.config.mjs",
            "files_changed": ["next.config.mjs"],
            "commit": "5be4dacb",
            "result": "deviceSizes 8->6 (dropped 750/2048/3840, added 2560); imageSizes 8->6 (dropped 16/384). Reduces number of generated image variants and build time."
        }
    ],
    "tsc_passed": True,
    "live_verification": {
        "homepage_200": True,
        "blog_post_200": True,
        "tool_page_200": True,
        "font_preconnect_removed": True
    },
    "learnings": "geist/font (next/font/google under the hood) self-hosts font files at build time; preconnect to fonts.gstatic.com is redundant and adds DNS overhead. Trimming deviceSizes from 8 to 6 reduces number of srcset variants and image optimization worker work."
}

# Prepend to list
if isinstance(log, list):
    log.insert(0, new_entry)
elif isinstance(log, dict):
    if "iterations" not in log:
        log["iterations"] = []
    log["iterations"].insert(0, new_entry)

log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
print("iteration_log.json updated")

# 2. Update state.json
state_path = base / "state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["current_iteration"] = 76
state["latest_commit"] = "5be4dacb202609c33c5d51e5b965a622191e895c"

# Mark P2-PERF-FONT-001 and P2-PERF-CONFIG-001 as completed in next_iteration_focus
focus = state.get("next_iteration_focus", [])
new_focus = []
for item in focus:
    if isinstance(item, dict):
        iid = item.get("id", "")
        if iid in ("P2-PERF-FONT-001", "P2-PERF-CONFIG-001"):
            item["status"] = "completed"
            item["completed_at"] = "2026-09-20"
            item["commit"] = state["latest_commit"][:8]
        new_focus.append(item)
    elif isinstance(item, str):
        if "P2-PERF-FONT-001" in item or "P2-PERF-CONFIG-001" in item:
            new_focus.append({"id": item.split(":")[0].strip(), "title": item, "status": "completed", "completed_at": "2026-09-20"})
        else:
            new_focus.append(item)
    else:
        new_focus.append(item)
state["next_iteration_focus"] = new_focus

state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"state.json updated: iteration=76, latest_commit={state['latest_commit'][:8]}")
print("Done.")
