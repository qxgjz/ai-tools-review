import json, os, glob

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

nif = state.get("next_iteration_focus", [])
print(f"total todos: {len(nif)}")

p0_w3 = [t for t in nif if (
    "window3" in str(t.get("assigned_to", "")).lower()
    or "窗口3" in str(t.get("assigned_to", ""))
) and t.get("priority") == "P0" and t.get("status") == "pending"]

print(f"window3 P0 pending: {len(p0_w3)}")
for i, t in enumerate(p0_w3):
    tid = t.get("id", "?")
    task = t.get("task", t.get("title", "?"))
    print(f"{i+1}. [{tid}] {task[:100]}")
    print(f"   assigned_to={t.get('assigned_to')}, source={t.get('source','')}")
