# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
p=next((x for x in posts if 'beginners' in x['slug']),None)
if p: print(p['slug'],'T',len(p['title']),p['title'],'\nE',len(p.get('excerpt','')),p.get('excerpt',''))
else: print('not in posts.json')
