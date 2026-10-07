"""Mark completed keyword research tasks in state.json"""
import json, os

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

# 13 keyword task IDs to mark complete
completed_ids = [
    "kw_r2_lovable_vs_boltnew",
    "kw_r2_claude37_vs_gpt4o",
    "kw_r2_synthesia_vs_heygen",
    "kw_r3_otter_alternatives",
    "kw_r3_runway_alternatives",
    "kw_r3_gemini_vs_perplexity",
    "kw_r3_beautiful_ai_alternatives",
    "kw_r3_devin_ai_review",
    "kw_r4_sudowrite_alternatives",
    "kw_r4_writesonic_alternatives",
    "kw_r4_motion_ai_alternatives",
    "kw_r4_clearscope_alternatives",
    "kw_r4_quillbot_alternatives",
]

nif = state.get("next_iteration_focus", [])
updated = 0
for task in nif:
    if task.get("id") in completed_ids:
        task["status"] = "completed"
        task["completed_at"] = "2026-09-30"
        task["research_round"] = "round5_2026-09-30"
        updated += 1

with open("iteration_center/state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Count remaining window3 P0
remaining = [t for t in nif if (
    "window3" in str(t.get("assigned_to", "")).lower()
    or "窗口3" in str(t.get("assigned_to", ""))
) and t.get("priority") == "P0" and t.get("status") == "pending"]

print(f"Marked complete: {updated} tasks")
print(f"Remaining window3 P0 pending: {len(remaining)}")
for t in remaining:
    print(f"  - [{t.get('id')}] {t.get('task', t.get('title',''))[:80]}")
