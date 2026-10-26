# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
for sl in ['ai-coding-tools-comparison-2026','creatium-coach-review-2025']:
    p=by.get(sl)
    if p: print(sl,'| t',len(p['title']),repr(p['title']),'| e',len(p.get('excerpt') or ''),repr((p.get('excerpt') or '')[:160]))
    else: print(sl,'NO')
print('\ntabbyml slugs:')
for p in posts:
    if 'tabby' in p['slug'].lower(): print(' ',p['slug'],len(p['title']),repr(p['title']))
print('\ncreatium slugs:')
for p in posts:
    if 'creatium' in p['slug'].lower(): print(' ',p['slug'])
