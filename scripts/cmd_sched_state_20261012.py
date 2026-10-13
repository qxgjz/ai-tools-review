# -*- coding: utf-8 -*-
"""2026-10-12 每日调度：统计state.json待办"""
import json, os
from collections import Counter

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)

nf = state.get("next_iteration_focus", [])
archived = state.get("archived_todos", [])

status_cnt = Counter(t.get("status", "unknown") for t in nf)
prio_cnt = Counter(t.get("priority", "?") for t in nf)

# 按窗口统计
win_cnt = Counter()
for t in nf:
    for w in (t.get("assigned_to") or []):
        win_cnt[w] += 1

# 按窗口按优先级
win_prio = {}
for t in nf:
    for w in (t.get("assigned_to") or []):
        win_prio.setdefault(w, Counter())[t.get("priority", "?")] += 1

pending = status_cnt.get("pending", 0)
in_prog = status_cnt.get("in_progress", 0)
completed = status_cnt.get("completed", 0)
total_active = len(nf)
rate = completed / (pending + completed) * 100 if (pending + completed) else 0

print(f"=== state.json 待办统计 ===")
print(f"active总数: {total_active} | pending: {pending} | in_progress: {in_prog} | completed: {completed}")
print(f"完成率: {rate:.1f}%")
print(f"优先级: P0={prio_cnt.get('P0',0)} P1={prio_cnt.get('P1',0)} P2={prio_cnt.get('P2',0)} 其他={prio_cnt.get('?',0)}")
print(f"archived累计: {len(archived)}")
print("\n=== 按窗口（含优先级）===")
for w, c in win_cnt.most_common():
    pc = win_prio.get(w, {})
    print(f"  {w}: {c}条 (P0={pc.get('P0',0)} P1={pc.get('P1',0)} P2={pc.get('P2',0)})")

# 列出completed待办
print("\n=== completed待办 ===")
for t in nf:
    if t.get("status") == "completed":
        print(f"  [{t.get('id')}] {t.get('task','')[:60]}")
