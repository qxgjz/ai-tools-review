# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
pend=[t for t in s.get('next_iteration_focus',[]) if t.get('status')=='pending' and any('window5' in str(a) or '打磨师' in str(a) for a in (t.get('assigned_to') or []))]
print('PENDING',len(pend))
for t in pend:
    print('===',t.get('id'),'|',t.get('priority'))
    print('  ',str(t.get('task'))[:220])
