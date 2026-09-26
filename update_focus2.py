"""Add new actionable items to next_iteration_focus if not present."""
import json

path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"
with open(path, "r", encoding="utf-8") as f:
    state = json.load(f)

new_items = [
    {
        "id": "P2-PERF-FONT-001",
        "source": "learning: next/font optimization 2026-09-20",
        "title": "Verify layout.tsx uses next/font self-hosted, not external Google Fonts link",
        "how_to": "Check app/layout.tsx. If it uses <link> to fonts.googleapis.com, replace with next/font/google (e.g. Inter/Geist). Specify subsets:['latin'], display:'swap'. Eliminates external DNS lookup and FOUT.",
        "priority": "P2"
    },
]

existing = {item.get("id") if isinstance(item, dict) else None for item in state.get("next_iteration_focus", [])}
added = 0
for item in new_items:
    if item["id"] not in existing:
        state["next_iteration_focus"].append(item)
        added += 1

with open(path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"Added {added}. Total: {len(state['next_iteration_focus'])}")
