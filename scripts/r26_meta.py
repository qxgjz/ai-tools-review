# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
items=posts if isinstance(posts,list) else posts.get('posts',posts)
want=['adobe-firefly-review-2026','ai-coding-tools-comparison-2026','astra','astra-review']
for p in items:
    slug=p.get('slug','')
    if any(w in slug for w in want):
        t=p.get('title',''); ex=p.get('excerpt') or p.get('description','')
        print('SLUG',slug)
        print('  title(%d):'%len(t),repr(t))
        print('  excerpt(%d):'%len(ex),repr(ex[:180]))
        print()
# also search astra in any field
print('=== astra field search ===')
for p in items:
    blob=json.dumps(p,ensure_ascii=False).lower()
    if 'astra' in blob:
        print('MATCH slug=',p.get('slug'),'| title=',p.get('title','')[:70])
