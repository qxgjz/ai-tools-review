# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
for sl in ['ai-coding-tools-comparison-2026','best-ai-comparison-tools-2026']:
    p=by.get(sl)
    if p: print('CTR',sl,'| title=',repr(p.get('title')),'| excerpt=',repr((p.get('excerpt') or '')[:160]))
# ai-policy may not be a post
print('ai-policy post?', 'ai-policy' in by)
# TL;DR gap list
gaps=[(p['slug'],len(p['content']),p.get('title','')[:50]) for p in posts if '## TL;DR' not in p['content']]
print('\nTOTAL',len(posts),'WITH TLDR',len(posts)-len(gaps),'GAP',len(gaps))
for sl,l,t in sorted(gaps,key=lambda x:-x[1])[:40]:
    print(f'{l:7d}  {sl}  | {t}')
