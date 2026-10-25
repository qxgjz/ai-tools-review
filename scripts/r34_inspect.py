# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
for sl in ['ai-coding-tools-comparison-2026','best-ai-meeting-assistants-2026','best-ai-observability-tools-2026','best-ai-productivity-tools-2026']:
    p=by.get(sl)
    if p: print(sl,'| t',len(p['title']),repr(p['title']),'| e',len(p.get('excerpt') or ''),repr((p.get('excerpt') or '')[:160]))
    else: print(sl,'NO')
# article-api ugly slug
print('\narticle-api slugs:')
for p in posts:
    if p['slug'].startswith('article-api'): print(' ',p['slug'][:90])
