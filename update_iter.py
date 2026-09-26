"""Update iteration_log.json and state.json"""
import json
from datetime import datetime

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Update iteration_log.json (it's a list)
log_path = PROJECT + r"\iteration_center\iteration_log.json"
with open(log_path, "r", encoding="utf-8") as f:
    log = json.load(f)

new_entry = {
    "round": 59,
    "timestamp": now,
    "actions": [
        "Published 10 [READY] drafts from content_drafts/ to data/posts.json (91->101 posts)",
        "Fixed tool page schema: worstRating changed from '0' to '1' in Review rating",
        "Verified aggregateRating already present in itemReviewed SoftwareApplication",
        "Confirmed TypeScript compilation passes",
        "Committed via GitHub API (commit 5d92a6a)",
        "Verified all 10 new articles return 200/308 on live site",
        "Verified schema fix (worstRating=1) live on /tools/chatgpt"
    ],
    "files_changed": [
        "data/posts.json (added 10 new articles)",
        "app/tools/[slug]/page.tsx (worstRating fix)"
    ],
    "verified": True
}

if isinstance(log, list):
    log.insert(0, new_entry)
    log = log[:50]
elif isinstance(log, dict):
    if "iterations" not in log:
        log["iterations"] = []
    log["iterations"].insert(0, new_entry)
    log["iterations"] = log["iterations"][:50]
    log["last_updated"] = now

with open(log_path, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

# Update state.json
state_path = PROJECT + r"\iteration_center\state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["current_round"] = 59
state["last_updated"] = now
state["last_action"] = "Published 10 drafts + schema worstRating fix"
state["latest_commit"] = "5d92a6abe255b43d0bc65135ec0d9c9287a86f6c"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("State and log updated.")
print(f"Round: {state['current_round']}")
