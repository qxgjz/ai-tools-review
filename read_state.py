"""Read state.json and print pending P0/P1 tasks."""
import json
from pathlib import Path

p = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json")
with open(p, "r", encoding="utf-8") as f:
    s = json.load(f)

print(f"iteration: {s.get('current_iteration')} / round: {s.get('current_round')}")
print(f"latest_commit: {s.get('latest_commit')}")
print()
print("=== current_todo ===")
for t in s.get("current_todo", []):
    if isinstance(t, dict):
        print(f"  [{t.get('priority')}] {t.get('id')}: {t.get('title')[:60]} | status={t.get('status')}")
print()
print("=== next_iteration_focus (pending, not completed) ===")
for item in s.get("next_iteration_focus", []):
    if isinstance(item, dict):
        print(f"  [{item.get('priority')}] {item.get('id')}: {item.get('title','')[:70]}")
    else:
        print(f"  ? {item[:80]}")
