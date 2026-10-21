# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
print('keys:',list(s.keys()))
for t in s['next_iteration_focus']:
    if any(k in str(t).lower() for k in ['readab','可读性','flesch','sentence','段落','句子']):
        print(t.get('status'),'|',t.get('id'),'|',t.get('priority'),'|',str(t.get('task',t.get('title','')))[:90])
