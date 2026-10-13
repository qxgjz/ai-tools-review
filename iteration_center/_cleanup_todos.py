# -*- coding: utf-8 -*-
"""指挥官：清理state.json中的空任务待办 + 合并重复待办（只做删除/去重，不改任何任务内容）"""
import json

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
archived = d.get('archived_todos', [])
if not isinstance(archived, list):
    archived = []

before_total = len(focus)
removed_empty = []
removed_dup = []

# 1) 删除 task 为空/空白的待办
keep = []
for t in focus:
    task = t.get('task')
    if task is None or (isinstance(task, str) and task.strip() == ''):
        removed_empty.append(t)
        continue
    keep.append(t)

# 2) 合并重复：按 task 内容归一化分组，保留优先级最高的一条
seen = {}
for t in keep:
    task = str(t.get('task', '')).strip()
    key = task  # 直接按完整task文本去重
    prio = t.get('priority', 'P2')
    if key not in seen:
        seen[key] = t
    else:
        old = seen[key]
        # 保留优先级更高的（P0 > P1 > P2）
        order = {'P0': 0, 'P1': 1, 'P2': 2, '': 3, None: 3}
        if order.get(prio, 3) < order.get(old.get('priority'), 3):
            removed_dup.append(old)
            seen[key] = t
        else:
            removed_dup.append(t)

cleaned = list(seen.values())
after_total = len(cleaned)

d['next_iteration_focus'] = cleaned
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('清理前待办总数: %d' % before_total)
print('删除空任务: %d 条' % len(removed_empty))
print('合并重复: %d 条' % len(removed_dup))
print('清理后待办总数: %d' % after_total)
print('archived_todos: %d 条（未动）' % len(archived))
print()
print('--- 删除的空任务(前10) ---')
for t in removed_empty[:10]:
    print('  [%s] %s | %s' % (t.get('priority',''), t.get('assigned_to',''), t.get('status','')))
print()
print('--- 合并的重复任务(全部) ---')
for t in removed_dup:
    print('  [%s] %s | %s' % (t.get('priority',''), t.get('assigned_to',''), str(t.get('task',''))[:80]))
print()
print('--- 保留的待办(全部) ---')
for i, t in enumerate(cleaned):
    print('%d. [%s] %s | %s | %s' % (i+1, t.get('status',''), t.get('priority',''), str(t.get('assigned_to',''))[:30], str(t.get('task',''))[:90]))
