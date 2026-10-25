# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
for sl in ['best-ai-coding-tools-2026','best-ai-comparison-tools-2026','github-copilot-pricing','copilot-pricing','github-copilot-pricing-2026']:
    p=by.get(sl)
    if p: print(sl,'| t',len(p['title']),repr(p['title']),'| e',len(p.get('excerpt') or ''),repr((p.get('excerpt') or '')[:160]))
    else: print(sl,'NO')
# find copilot pricing candidates
print('\ncandidates:')
for p in posts:
    if 'copilot' in p['slug'] and 'pricing' in p['slug']: print(' ',p['slug'])
