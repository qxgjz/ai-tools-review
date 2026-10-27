# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
missing=[]
for p in posts:
    c=p.get('content','') or ''
    if '## TL;DR' not in c and '## TL;DR' not in c.replace('## TL;DR',''):
        missing.append(p['slug'])
print('total',len(posts),'missing TL;DR',len(missing))
print('\n'.join(missing[:20]))
