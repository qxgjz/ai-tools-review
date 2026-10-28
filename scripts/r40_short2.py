# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
SHORT='''<!-- r40-short2-20261028 -->
**What matters**
- Does it save time?
- Is the tone right?
- Are citations real?
- Does it avoid hallucinations?
- Can you edit easily?
- Is support fast?
- Will you reuse it?
'''
for sl in ['best-ai-essay-writing-tools-2026','best-ai-search-engines-2026']:
    p=by[sl]
    if 'r40-short2-20261028' in p['content']: continue
    p['content']=SHORT+"\n"+p['content']
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('short2 added')
