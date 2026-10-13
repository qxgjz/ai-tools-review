# -*- coding: utf-8 -*-
import json, os, glob

state_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = state.get("next_iteration_focus", [])
archived = state.get("archived_todos", [])

# 状态统计
from collections import Counter
status_count = Counter(t.get("status", "unknown") for t in todos)
prio_count = Counter(t.get("priority", "?") for t in todos)

# 按窗口统计
window_map = {"window1": "架构师", "architect": "架构师", "window2": "拓荒者", "backlink": "拓荒者",
              "window3": "创作家", "creator": "创作家", "window4": "分析师", "analyst": "分析师",
              "window5": "打磨师", "polisher": "打磨师", "window6": "体验官", "ux": "体验官",
              "all_windows": "全部窗口", "commander": "指挥官"}
win_count = Counter()
for t in todos:
    a = t.get("assigned_to", "")
    if isinstance(a, list):
        a = ",".join(a)
    win_count[window_map.get(a, a)] += 1

completed_todos = [t for t in todos if t.get("status") == "completed"]
pending_todos = [t for t in todos if t.get("status") in ("pending", "in_progress")]

total = len(pending_todos) + len(completed_todos)
rate = round(len(completed_todos) / total * 100, 1) if total else 0

print(f"=== 待办统计 ===")
print(f"next_iteration_focus 总数: {len(todos)}")
print(f"状态分布: {dict(status_count)}")
print(f"优先级分布: {dict(prio_count)}")
print(f"按窗口: {dict(win_count)}")
print(f"完成率: {rate}% (pending {len(pending_todos)} / completed {len(completed_todos)})")
print(f"archived_todos: {len(archived)}")

# 列出completed的待办（待清理）
print(f"\n=== completed待办（待清理到archived）===")
for t in completed_todos:
    print(f"  {t.get('id','?')} | {t.get('assigned_to','?')} | {t.get('task','')[:60]}")

# P0列表
print(f"\n=== P0待办 ===")
for t in sorted(todos, key=lambda x: x.get("priority",""), reverse=True):
    if t.get("priority") == "P0":
        print(f"  {t.get('id','?')} | {t.get('assigned_to','?')} | {t.get('status','?')} | {t.get('task','')[:60]}")
