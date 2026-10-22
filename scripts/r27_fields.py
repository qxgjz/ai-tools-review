# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
p=[x for x in posts if x.get('slug')=='suno-alternatives-2026'][0]
print('KEYS:',list(p.keys()))
for k in ['title','excerpt','description','date','publishedAt','updatedAt','updated']:
    if k in p: print(k,'=',repr(str(p[k])[:120]))
print('--- content head 600 ---')
print(p['content'][:600])
