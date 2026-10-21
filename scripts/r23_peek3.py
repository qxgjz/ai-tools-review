# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts={p['slug']:p for p in json.load(io.open('data/posts.json',encoding='utf-8'))}
for slug in ['stable-diffusion-review-2026','best-ai-audio-tools-2026','replit-review-2026']:
    c=posts[slug]['content']
    print('\n======',slug,'len',len(c),'======')
    print(c[:1200].replace('\n',' | '))
    print(' internal md links:',re.findall(r'\]\((/[^)]+)\)',c[:30000]))
