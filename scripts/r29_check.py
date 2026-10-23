# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
tldr=[p['slug'] for p in posts if 'r28-tldr-20261023' in p.get('content','')]
low=[p['slug'] for p in posts if 'r28-low-20261023' in p.get('content','')]
print('TLDR markers',len(tldr)); [print(' ',x) for x in tldr]
print('LOW markers',len(low)); [print(' ',x) for x in low]
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
print('completed_tasks has P0:', any(x.get('id')=='P0-GEO-TLDR-TABLE-20261023' for x in s.get('completed_tasks',[])))
