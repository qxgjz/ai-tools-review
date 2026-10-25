# -*- coding: utf-8 -*-
"""读取分析师5条待办完整内容 + 最新 live_pull 概览"""
import json, glob, os

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
d = json.load(open(os.path.join(P, 'iteration_center', 'state.json'), encoding='utf-8'))
nf = {i.get('id'): i for i in d.get('next_iteration_focus', [])}
todos = ['CMD-20261024-002', 'P1-GEO-BASELINE-AUDIT-20261013', 'P1-TOOL-ELMO-20261017',
         'P1-AUTOCHAIN-CHECK-20261025', 'P2-INDEX-MONITOR-1026-20261025']
for tid in todos:
    i = nf.get(tid)
    if i:
        print('='*100)
        print(tid, '|', i.get('priority'), '| status:', i.get('status'))
        print('task:', i.get('task'))
        print('extra:', {k: v for k, v in i.items() if k not in ('id','task','status','priority','assigned_to')})

# 最新 live_pull
lp = sorted(glob.glob(os.path.join(P, 'gsc-ga4-report', 'live_pull_*.json')), key=os.path.getmtime)
latest = lp[-1]
print('='*100)
print('LATEST live_pull:', os.path.basename(latest))
data = json.load(open(latest, encoding='utf-8'))
print('keys:', list(data.keys())[:20] if isinstance(data, dict) else type(data))
