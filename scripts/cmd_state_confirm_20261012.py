# -*- coding: utf-8 -*-
"""2026-10-12 早间：清理后state确认 + 目标进度"""
import json, os

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
with open(STATE, encoding="utf-8") as f:
    state = json.load(f)

nf = state["next_iteration_focus"]
arch = state.get("archived_todos", [])
from collections import Counter
status_cnt = Counter(t.get("status") for t in nf)
prio_cnt = Counter(t.get("priority") for t in nf)
print(f"清理后 active={len(nf)} 状态={dict(status_cnt)} 优先级={dict(prio_cnt)}")
print(f"archived累计={len(arch)}")

pending_by_win = Counter()
for t in nf:
    if t.get("status") in ("pending", "in_progress"):
        a = t.get("assigned_to")
        if isinstance(a, list):
            for w in a: pending_by_win[str(w)] += 1
        elif isinstance(a, str):
            pending_by_win[a] += 1
print(f"各窗口负载: {dict(pending_by_win.most_common())}")

# 检查GA4问题是否已录入
ids = [t.get("id") for t in nf]
print(f"\n当前待办ID样例(前15): {ids[:15]}")
for t in nf:
    task = str(t.get("task", ""))
    if "not set" in task.lower() or "爬虫" in task or "engagement" in task.lower() or "0 engaged" in task:
        print(f"  GA4相关已录入: {t.get('id')} | {task[:80]}")
