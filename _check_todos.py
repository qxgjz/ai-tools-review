import json, os

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
state = json.load(open(os.path.join(base, "iteration_center", "state.json"), "r", encoding="utf-8"))
nif = state.get("next_iteration_focus", [])

# Check structure of first few items
print("=== 前3条待办完整结构 ===")
for t in nif[:3]:
    print(json.dumps(t, ensure_ascii=False, indent=2)[:500])
    print("---")

# List active P0/P1 with whatever title field exists
active = [t for t in nif if t.get("status") in ("pending", "in_progress")]
print(f"\n=== 活跃待办 {len(active)} 条 ===")
for t in active:
    title = t.get("task") or t.get("title") or t.get("description") or t.get("name") or "???"
    title = str(title)[:100]
    print(f"  [{t.get('priority','?')}][{t.get('assigned_to','?')}][{t.get('status','?')}] {title}")
