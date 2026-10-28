# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
SHORT='''<!-- r40-short3-20261028 -->
**Our verdict**
- Start free.
- Test now.
- Keep the winner.
'''
for sl in ['best-ai-essay-writing-tools-2026','best-ai-search-engines-2026']:
    p=by[sl]
    if 'r40-short3-20261028' in p['content']: continue
    p['content']=SHORT+"\n"+p['content']
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('short3 added')
