# -*- coding: utf-8 -*-
"""分析师 r27：盘点分析师专属 pending 待办（P0→P1）"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
print('=== focus total:', len(nf))
print('=== last_update:', d.get('last_update'))
print('=== last_commit:', d.get('last_commit'))

# 分析师专属 pending
analyst = [i for i in nf if i.get('status') == 'pending'
           and '分析师' in str(i.get('assigned_to', ''))]
analyst.sort(key=lambda x: (0 if x.get('priority') == 'P0' else 1, x.get('created_at', '')))
print('=== analyst pending:', len(analyst))
for i in analyst:
    print(f"- {i.get('id')} | {i.get('priority')} | {i.get('task', '')[:80]} | created {i.get('created_at','')[:16]}")

# 今日已有 source 分布（避免重复开单）
from collections import Counter
src = Counter(i.get('source', '') for i in nf if i.get('status') == 'pending')
print('=== pending by source (top 20):')
for s, c in src.most_common(20):
    print(f'  {c:3d}  {s}')

# 总 pending
print('=== total pending:', len([i for i in nf if i.get('status') == 'pending']))
