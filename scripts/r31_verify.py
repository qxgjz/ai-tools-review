# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
gap=sum(1 for p in posts if '## TL;DR' not in p['content'])
print('TOTAL',len(posts),'WITH TLDR',len(posts)-gap,'GAP',gap)
by={p['slug']:p for p in posts}
for sl in ['ai-coding-tools-comparison-2026','best-ai-comparison-tools-2026','github-copilot-review-2026']:
    p=by[sl]; print(sl,'| title',len(p['title']),repr(p['title']),'| excerpt',len(p['excerpt']))
