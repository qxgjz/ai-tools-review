# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
SHORT='''<!-- r38-short-20261027 -->
**Quick read**
- Start with the free tier.
- Test the output on your own task.
- Check export options before you pay.
- Compare two tools side by side.
- Cancel if it does not save you time.
'''
for sl in ['best-ai-art-generators-2026','best-ai-audio-generators-2026','best-ai-portrait-generators-2026']:
    p=by[sl]
    if 'r38-short-20261027' in p['content']: continue
    p['content']=SHORT+"\n"+p['content']
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('short added')
