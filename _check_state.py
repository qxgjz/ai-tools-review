import json
import os

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
state_path = os.path.join(base, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

print("=== TOP LEVEL KEYS ===")
print(list(state.keys()))
print()

# Check iteration
for k in ["iteration", "current_iteration", "round", "iteration_count"]:
    if k in state:
        print(f"iteration key '{k}': {state[k]}")

# Check focus structure
focus = state.get("next_iteration_focus", [])
if focus:
    print(f"\n=== FIRST TASK KEYS ===")
    print(list(focus[0].keys()))
    print(f"\n=== FIRST 3 TASKS ===")
    for t in focus[:3]:
        print(json.dumps(t, ensure_ascii=False, indent=2)[:300])
        print("---")

# Count by status
from collections import Counter
statuses = Counter(t.get("status", "unknown") for t in focus)
print(f"\n=== STATUS COUNTS ===")
print(dict(statuses))

# Count by assigned_to
assigned = Counter(t.get("assigned_to", "unknown") for t in focus if t.get("status") != "completed")
print(f"\n=== ACTIVE BY WINDOW ===")
print(dict(assigned))
