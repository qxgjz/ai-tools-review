# -*- coding: utf-8 -*-
"""分析师 SOP：读 state.json 找分析师 pending 待办"""
import json

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(P, encoding='utf-8'))
nf = d.get('next_iteration_focus', [])
print('focus len:', len(nf), '| last_update:', d.get('last_update'))

analyst = []
for i in nf:
    if i.get('status') != 'pending':
        continue
    a = i.get('assigned_to', '')
    if isinstance(a, list):
        hit = any('分析师' in str(x) for x in a)
    else:
        hit = '分析师' in str(a)
    if hit:
        analyst.append(i)

analyst.sort(key=lambda x: (x.get('priority', 'P2'), x.get('created_at', '')))
print('analyst pending:', len(analyst))
for i in analyst:
    print(i.get('priority'), '|', i.get('id'), '|', (i.get('task') or '')[:100])
