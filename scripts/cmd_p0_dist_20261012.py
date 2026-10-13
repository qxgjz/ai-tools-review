# -*- coding: utf-8 -*-
"""2026-10-12 早间：P0按窗口分布 + 学习笔记关键数据更新"""
import json, os
from collections import Counter

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state["next_iteration_focus"]

p0_by_win = Counter()
for t in nf:
    if t.get("priority") == "P0":
        a = t.get("assigned_to")
        if isinstance(a, list):
            for w in a: p0_by_win[str(w)] += 1
        elif isinstance(a, str):
            p0_by_win[a] += 1
print("P0按窗口分布:", dict(p0_by_win.most_common()))

# 统计是否有窗口P0>10 或 P0=0
all_wins = set()
for t in nf:
    a = t.get("assigned_to")
    if isinstance(a, list): all_wins.update(str(w) for w in a)
    elif isinstance(a, str): all_wins.add(a)
print("\n窗口P0>10:", [w for w, c in p0_by_win.items() if c > 10])
print("有pending但P0=0的窗口:", [w for w in all_wins if p0_by_win.get(w, 0) == 0])
