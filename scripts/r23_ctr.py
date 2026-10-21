# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
T='AI Coding Tools Comparison 2026: Copilot, Cursor, Tabnine'
E='Compare the top AI coding tools of 2026 — GitHub Copilot, Cursor, and Tabnine — on features, pricing, and setup. Pick your best AI coding assistant today.'
print('T',len(T),'E',len(E))
p=next(x for x in posts if x['slug']=='ai-coding-tools-comparison-2026')
p['title']=T; p['excerpt']=E
json.dump(posts,io.open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
assert 50<=len(T)<=60
assert 120<=len(E)<=155
print('OK saved')
