# -*- coding: utf-8 -*-
"""2026-10-12 每日调度：修正版按窗口统计（处理assigned_to为str的情况）+ 列出completed详情"""
import json, os
from collections import Counter

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])

def norm_windows(v):
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        return [x for x in v if isinstance(x, str)]
    return []

win_cnt = Counter()
win_prio = {}
for t in nf:
    for w in norm_windows(t.get("assigned_to")):
        win_cnt[w] += 1
        win_prio.setdefault(w, Counter())[t.get("priority", "?")] += 1

print("=== 按窗口（修正版）===")
for w, c in win_cnt.most_common():
    pc = win_prio.get(w, {})
    print(f"  {w}: {c}条 (P0={pc.get('P0',0)} P1={pc.get('P1',0)} P2={pc.get('P2',0)})")

print("\n=== completed待办详情 ===")
for t in nf:
    if t.get("status") == "completed":
        print(f"[{t.get('id')}] | prio={t.get('priority')} | win={t.get('assigned_to')} | completed_at={t.get('completed_at','?')}")
        print(f"   task: {t.get('task','')[:120]}")
