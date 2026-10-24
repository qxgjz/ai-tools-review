# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
for sl in ['best-ai-observability-tools-2026','gemini-cli-review','gemini-cli-2026','best-ai-coding-tools-2026']:
    p=by.get(sl)
    print(sl,'EXISTS' if p else 'NO')
    if p: print('  title',len(p['title']),repr(p['title']),'| excerpt',len(p.get('excerpt') or ''),repr((p.get('excerpt') or '')[:140]))
# find gemini cli-ish
print('\n--- gemini/copilot pricing slugs ---')
for p in posts:
    if 'gemini' in p['slug'] and ('cli' in p['slug'] or 'code' in p['slug']): print(p['slug'])
# next tldr gaps (already have tldr skip)
gaps=[(len(p['content']),p['slug']) for p in posts if '## TL;DR' not in p['content']]
print('\nGAP',len(gaps))
for l,sl in sorted(gaps,reverse=True)[:35]: print(l,sl)
