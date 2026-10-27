# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
EXTRA='''<!-- r38-short4-20261027 -->
**Checklist**
- Clear face?
- Good lighting?
- Realistic skin?
- Fine details?
- No weird hands?
- Consistent style?
- Fast renders?
- Fair pricing?
'''
for sl in ['best-ai-portrait-generators-2026','best-ai-art-generators-2026']:
    p=by[sl]
    if 'r38-short4-20261027' in p['content']: continue
    p['content']=EXTRA+"\n"+p['content']
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('short4 added')
