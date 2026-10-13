# -*- coding: utf-8 -*-
import json, collections

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)

todos = data.get('next_iteration_focus', [])
print('=== 待办状态统计 ===')
status_c = collections.Counter(t.get('status', 'none') for t in todos)
for k, v in status_c.items():
    print(f'  {k}: {v}')

print('=== 优先级统计 ===')
prio_c = collections.Counter(t.get('priority', 'none') for t in todos)
for k, v in prio_c.items():
    print(f'  {k}: {v}')

print('=== 各窗口 pending/in_progress 数量（规范窗口名） ===')
win = collections.Counter()
for t in todos:
    if t.get('status') in ('pending', 'in_progress'):
        at = t.get('assigned_to', [])
        if isinstance(at, str):
            at = [at]
        for w in at:
            win[w] += 1
for k, v in win.most_common():
    print(f'  {k}: {v}')

print('=== P0 待办明细 ===')
for t in todos:
    if t.get('priority') == 'P0':
        print(f"  [{t.get('status')}] {t.get('id')} | 分配 {t.get('assigned_to')} | {t.get('title')}")

arch = data.get('archived_todos', [])
print('archived_todos 数量:', len(arch) if isinstance(arch, list) else arch)
