import json, os, sys

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# state.json
state = json.load(open(os.path.join(base, "iteration_center", "state.json"), "r", encoding="utf-8"))
nif = state.get("next_iteration_focus", [])
active = [t for t in nif if t.get("status") in ("pending", "in_progress")]
completed = [t for t in nif if t.get("status") == "completed"]
p0 = [t for t in active if t.get("priority") == "P0"]
p1 = [t for t in active if t.get("priority") == "P1"]
print(f"=== STATE.JSON ===")
print(f"总待办: {len(nif)}, 活跃: {len(active)}, 已完成: {len(completed)}")
print(f"P0: {len(p0)}, P1: {len(p1)}")
print("--- P0待办 ---")
for t in p0[:15]:
    task = str(t.get("task", ""))[:90]
    who = t.get("assigned_to", "?")
    print(f"  [{who}] {task}")
print("--- 最近5条 ---")
for t in nif[-5:]:
    task = str(t.get("task", ""))[:80]
    print(f"  [{t.get('priority','?')}][{t.get('assigned_to','?')}][{t.get('status','?')}] {task}")

# posts.json
posts = json.load(open(os.path.join(base, "data", "posts.json"), "r", encoding="utf-8"))
print(f"\n=== POSTS ===")
print(f"文章数: {len(posts)}")
if posts:
    dates = sorted([p.get("date", "") for p in posts if p.get("date")], reverse=True)
    if dates:
        print(f"最新文章日期: {dates[0]}")
    for p in posts[-3:]:
        print(f"  - {p.get('title', '')[:60]} ({p.get('date', '')})")

# iteration count
print(f"\n=== ITERATION ===")
print(f"迭代轮次字段: {state.get('iteration_count', state.get('current_iteration', 'N/A'))}")
for k in ["iteration_count", "current_iteration", "round", "total_iterations"]:
    if k in state:
        print(f"  {k} = {state[k]}")
