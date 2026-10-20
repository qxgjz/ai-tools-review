# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
NEW_T='AI Tools for Beginners 2026: Easy No-Code Starter Guide'
NEW_E='New to AI? Our 2026 beginner guide helps non-technical users pick the easiest AI tools, sign up in minutes, and get real results — no coding required.'
p=next(x for x in posts if x['slug']=='ai-tools-for-beginners-2026')
p['title']=NEW_T; p['excerpt']=NEW_E
json.dump(posts,io.open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('T',len(NEW_T),'E',len(NEW_E))
assert 50<=len(NEW_T)<=60, 'title out of range'
assert 120<=len(NEW_E)<=155, 'excerpt out of range'
print('OK')
