# -*- coding: utf-8 -*-
"""2026-10-12 周走查：state归档统计（修正版）"""
import json, os
from collections import Counter

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
IC = os.path.join(ROOT, "iteration_center")
with open(os.path.join(IC, "state.json"), encoding="utf-8") as f:
    state = json.load(f)

arch = state.get("archived_todos", [])
# 兼容字符串元素
week_arch = []
for t in arch:
    if isinstance(t, dict):
        ts = str(t.get("archived_at", t.get("completed_at", "")))
        if ts.startswith("2026-10") and ts[:10] >= "2026-10-06":
            week_arch.append(t)

print("archived累计:", len(arch))
print("本周(10/6后)归档:", len(week_arch))
for t in week_arch[-20:]:
    print(f"  - {t.get('id')} | {t.get('priority')} | {str(t.get('archived_at', t.get('completed_at', '?')))[:10]} | {str(t.get('task'))[:70]}")

nf = state.get("next_iteration_focus", [])
print("\nactive:", len(nf))
print("状态:", dict(Counter(t.get("status") for t in nf)))
print("优先级:", dict(Counter(t.get("priority") for t in nf)))

# 数据源统计
src = Counter(str(t.get("source", "?"))[:40] for t in nf)
print("\n待办来源TOP:", dict(src.most_common(8)))
