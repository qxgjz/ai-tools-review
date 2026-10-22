# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
ids=['CTR-ADOBE-FIREFLY-20261021','CTR-AI-CODING-TOOLS-20261021','CTR-AI-POLICY-20261021','CTR-ASTRA-REVIEW-20261022']
for t in s['next_iteration_focus']:
    if t.get('id') in ids:
        print('###',t['id'])
        print('task:',t.get('task'))
        print('source:',t.get('source'),'created:',t.get('created_at'))
        print()
