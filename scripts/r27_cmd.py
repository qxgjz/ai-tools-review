# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
for t in s['next_iteration_focus']:
    if t.get('id')=='CMD-POLISHER-BATCH-20261022':
        print(json.dumps(t,ensure_ascii=False,indent=2))
