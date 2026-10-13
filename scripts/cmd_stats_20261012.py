# -*- coding: utf-8 -*-
"""2026-10-12 指挥官早间调度：待办完成率统计"""
import json, os, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)

nf = state["next_iteration_focus"]
arch = state.get("archived_todos", [])
print(f"=== state.json @ {datetime.datetime.now()} ===")
print(f"active总数: {len(nf)}")
print(f"archived累计: {len(arch)}")

from collections import Counter
status_cnt = Counter(t.get("status") for t in nf)
prio_cnt = Counter(t.get("priority") for t in nf)
print(f"状态分布: {dict(status_cnt)}")
print(f"优先级分布: {dict(prio_cnt)}")

# 按窗口统计pending
pending_by_win = Counter()
for t in nf:
    if t.get("status") == "pending" or t.get("status") == "in_progress":
        a = t.get("assigned_to")
        if isinstance(a, list):
            for w in a:
                pending_by_win[str(w)] += 1
        elif isinstance(a, str):
            pending_by_win[a] += 1
print(f"\n各窗口pending/in_progress: {dict(pending_by_win.most_common())}")

# completed 明细
completed = [t for t in nf if t.get("status") == "completed"]
print(f"\ncompleted待办数: {len(completed)}")
for t in completed:
    print(f"  - {t.get('id')} | {t.get('priority')} | {t.get('assigned_to')} | {t.get('completed_at', t.get('updated_at', '?'))} | {str(t.get('task'))[:80]}")

# 完成率
total = len(nf)
done = status_cnt.get("completed", 0)
active_cnt = total - done
rate = done / total * 100 if total else 0
print(f"\n完成率: {rate:.1f}% (pending+in_progress={active_cnt} / completed={done} / total={total})")
