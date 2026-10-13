# -*- coding: utf-8 -*-
"""指挥官每日调度：待办完成率统计"""
import json
from collections import Counter

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
archived = d.get('archived_todos', [])

print('=== next_iteration_focus 总数:', len(focus))
st = Counter(t.get('status', '?') for t in focus)
pr = Counter(t.get('priority', '?') for t in focus)
print('状态分布:', dict(st))
print('优先级分布:', dict(pr))

win = Counter()
for t in focus:
    for a in (t.get('assigned_to') or []):
        win[a] += 1
print('按窗口:', dict(win))

completed = st.get('completed', 0)
pending_like = st.get('pending', 0) + st.get('open', 0) + st.get('in_progress', 0)
rate = completed / (completed + pending_like) * 100 if (completed + pending_like) > 0 else 0
print('完成率: %.1f%% (completed=%d, pending+open+in_progress=%d)' % (rate, completed, pending_like))
print()
print('=== archived_todos 总数:', len(archived))
print()
print('=== 前20条待办 ===')
for i, t in enumerate(focus[:20]):
    print('[%d] %s/%s assigned=%s :: %s' % (i, t.get('priority', '?'), t.get('status', '?'), t.get('assigned_to'), str(t.get('task', ''))[:90]))
