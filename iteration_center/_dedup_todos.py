# -*- coding: utf-8 -*-
"""第二轮：合并近似重复（同一痛点的两个变体，保留P0/更完整的一条）"""
import json

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])

# 近似重复组：核心痛点词 -> 保留规则
groups = [
    'AI工具订阅太贵',
    'AI视频生成credits',
    'ChatGPT/AI写作幻觉',
    'SaaS老板用AI工具',
]

removed = []
kept = []

# 先按组归类
bucket = {}
for t in focus:
    task = str(t.get('task', ''))
    matched = None
    for g in groups:
        if g in task:
            matched = g
            break
    if matched is None:
        kept.append(t)  # 无重复，直接保留
    else:
        bucket.setdefault(matched, []).append(t)

order = {'P0': 0, 'P1': 1, 'P2': 2, '': 3, None: 3}
for g, items in bucket.items():
    if len(items) == 1:
        kept.append(items[0])
        continue
    # 选优先级最高、task文本更完整的一条
    items_sorted = sorted(items, key=lambda x: (order.get(x.get('priority'), 3), -len(str(x.get('task', '')))))
    best = items_sorted[0]
    kept.append(best)
    for t in items_sorted[1:]:
        removed.append(t)

d['next_iteration_focus'] = kept
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('第二轮合并删除: %d 条' % len(removed))
print('合并后待办总数: %d' % len(kept))
print()
print('--- 合并删除的重复(全部) ---')
for t in removed:
    print('  [%s] | %s' % (t.get('priority',''), str(t.get('task',''))[:95]))
print()
print('--- 最终保留待办(全部) ---')
for i, t in enumerate(kept):
    print('%d. [%s] %s | %s | %s' % (i+1, t.get('status',''), t.get('priority',''), str(t.get('assigned_to',''))[:30], str(t.get('task',''))[:95]))
