# -*- coding: utf-8 -*-
import json

state_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = state.get("next_iteration_focus", [])
existing_ids = {t.get("id") for t in todos}

new = {
    "id": "P0-BATCH-CLEAR-2026-10-09-001",
    "task": "待办完成率14.1%远低于50%。创作家(22条)和打磨师(21条)负载最高，本周内各自把pending待办全部批量解决（每次触发至少完成5条，禁止一次只修2-3条），完成后立即在state.json标记completed由指挥官清理。",
    "assigned_to": ["window3", "window5"],
    "priority": "P0",
    "status": "pending",
    "source": "commander-daily-schedule 2026-10-09",
    "created_at": "2026-10-09"
}

if new["id"] not in existing_ids:
    todos.insert(0, new)

state["next_iteration_focus"] = todos
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"新增催办待办: {new['id']}")
print(f"当前 next_iteration_focus: {len(todos)} 条")
