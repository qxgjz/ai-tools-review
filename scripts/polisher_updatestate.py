"""Update state.json with this polisher run."""
import json, os
from datetime import datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
os.chdir(ROOT)

s = json.load(open("iteration_center/state.json", "r", encoding="utf-8"))

# Add a completed task record
new_task = {
    "id": "POLISH-2026-10-09-R1",
    "priority": "P1",
    "title": "打磨师首轮：优化3篇最低分文章至>=70分",
    "description": "优化 midjourney-v7-vs-flux-2026 (23→100), chatgpt-vs-claude-2026-comparison (28→90), claude-37-vs-gpt4o (28→100)",
    "status": "completed",
    "assigned_to": ["polisher"],
    "completed_at": "2026-10-09T13:25:00+08:00",
    "result": "3/3 articles passed zens-ink content_qc >=70. Also discovered batch_zensink_final.py bug: strips HTML before scoring, causing false negatives across 133/145 articles.",
    "log": "window_logs/polisher_2026-10-09.md"
}

if "completed_tasks" not in s:
    s["completed_tasks"] = []
s["completed_tasks"].insert(0, new_task)

# Add a P1 todo to fix the scoring script bug
bug_task = {
    "id": "P1-TOOL-ZENSINK-MD2HTML-001",
    "priority": "P1",
    "title": "修复 batch_zensink_final.py：写.html而非.md，避免HTML剥标签导致误判",
    "description": "当前脚本把所有HTML标签剥掉再写.md，zens-ink对.md用markdown解析器，导致h2/link/frontmatter全丢失，133/145篇被误判不及格。改为写.html让zens-ink走HTML解析器直接读原始标签。",
    "status": "pending",
    "assigned_to": ["polisher"],
    "created_at": "2026-10-09T13:25:00+08:00"
}
if "next_iteration_focus" not in s:
    s["next_iteration_focus"] = []
# dedupe by id
existing_ids = {t.get("id") for t in s["next_iteration_focus"] if isinstance(t, dict)}
if bug_task["id"] not in existing_ids:
    s["next_iteration_focus"].insert(0, bug_task)

s["last_updated"] = "2026-10-09T13:25:00+08:00"

with open("iteration_center/state.json", "w", encoding="utf-8") as f:
    json.dump(s, f, ensure_ascii=False, indent=2)

print("state.json updated.")
print(f"  completed_tasks: {len(s['completed_tasks'])}")
print(f"  next_iteration_focus: {len(s['next_iteration_focus'])}")
