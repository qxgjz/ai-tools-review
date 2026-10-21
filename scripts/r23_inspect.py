# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
pend=[t for t in s['next_iteration_focus'] if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in str(t.get('assigned_to','')).lower())]
pend.sort(key=lambda t:{'P0':0,'P1':1,'P2':2}.get(str(t.get('priority')),9))
print('PENDING 打磨师:',len(pend))
for t in pend:
    print('\n###',t.get('priority'),t.get('id'),'| assigned=',t.get('assigned_to'))
    print(' title:',t.get('title'))
    print(' detail:',str(t.get('detail',''))[:400])
    for k in ('pos','ctr_pct','impressions','evidence','source'):
        if k in t: print(f'  {k}:',t[k])
