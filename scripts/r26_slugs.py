# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
slugs=sorted(p['slug'] for p in posts)
import re
for kw in ['beginner','non-technical','suno','music','no-code','voice-changer','image-generator','chatbot','dify']:
    hits=[s for s in slugs if kw in s]
    print(kw,'->',hits[:6])
