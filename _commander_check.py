import json
import os

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# Read state.json
state_path = os.path.join(base, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

print("=== STATE.JSON ===")
print(f"iteration: {state.get('iteration', 'N/A')}")
focus = state.get("next_iteration_focus", [])
print(f"next_iteration_focus count: {len(focus)}")
active = [t for t in focus if t.get("status") != "completed"]
completed = [t for t in focus if t.get("status") == "completed"]
print(f"  active: {len(active)}, completed: {len(completed)}")
p0 = [t for t in active if t.get("priority") == "P0"]
p1 = [t for t in active if t.get("priority") == "P1"]
print(f"  P0: {len(p0)}, P1: {len(p1)}")
print()
print("=== ACTIVE P0 TASKS ===")
for t in p0:
    print(f"  [{t.get('assigned_to','?')}] {t.get('task','')[:80]}")
print()
print("=== ACTIVE P1 TASKS (first 10) ===")
for t in p1[:10]:
    print(f"  [{t.get('assigned_to','?')}] {t.get('task','')[:80]}")

# Read posts.json count
posts_path = os.path.join(base, "data", "posts.json")
with open(posts_path, "r", encoding="utf-8") as f:
    posts = json.load(f)
print(f"\n=== POSTS ===")
print(f"Total posts: {len(posts)}")
if posts:
    latest = sorted(posts, key=lambda x: x.get("date", ""), reverse=True)[:3]
    for p in latest:
        print(f"  {p.get('date','?')}: {p.get('title','?')[:60]}")

# Count screenshots
screenshots_dir = os.path.join(base, "public", "screenshots")
webp_count = 0
svg_count = 0
total = 0
for root, dirs, files in os.walk(screenshots_dir):
    for f in files:
        total += 1
        if f.endswith(".webp"):
            webp_count += 1
        elif f.endswith(".svg"):
            svg_count += 1
print(f"\n=== SCREENSHOTS ===")
print(f"Total: {total} (webp: {webp_count}, svg: {svg_count})")
