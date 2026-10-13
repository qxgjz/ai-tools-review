# -*- coding: utf-8 -*-
"""指挥官每日调度：清理completed + 检查报告缺口"""
import json, re, os

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
archived = d.get('archived_todos', [])

# 1. 清理completed
completed_items = [t for t in focus if t.get('status') == 'completed']
pending_items = [t for t in focus if t.get('status') != 'completed']
print('待清理completed:', len(completed_items))
for t in completed_items:
    print(' - ', str(t.get('task',''))[:70])
archived = archived + completed_items
d['next_iteration_focus'] = pending_items
d['archived_todos'] = archived
print('已移入archived, archived总数:', len(archived))

# 2. 检查backlink_opportunities.md报告内容是否已录入待办
report = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\backlink_opportunities.md'
txt = open(report, encoding='utf-8').read()
# 提取可能的关键动作关键词
checks = ['aitoolsdirectory', 'stork.ai', 'submitator', 'tooljunction', 'aitude', 'Reddit', 'Futurepedia']
all_text = ' '.join(str(t.get('task','')) for t in pending_items).lower()
missing = []
for c in checks:
    if c.lower() not in all_text and c.lower() in txt.lower():
        missing.append(c)
print()
print('报告中提到但待办未覆盖的关键词:', missing if missing else '无')

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('state.json已保存, 剩余待办:', len(pending_items))
