# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
print('=== pending polisher/window5 ===')
for t in s['next_iteration_focus']:
    a=str(t.get('assigned_to','')).lower()
    if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in a or 'polish' in a):
        print(t.get('priority'),'|',t.get('id'),'|',t.get('title',t.get('task',''))[:70])
print('=== ALL pending P0 ===')
for t in s['next_iteration_focus']:
    if t.get('status')=='pending' and t.get('priority')=='P0':
        print(t.get('priority'),'|',t.get('id'),'|',t.get('title',t.get('task',''))[:70],'|',t.get('assigned_to'))
