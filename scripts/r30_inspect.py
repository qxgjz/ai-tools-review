# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
pend=[t for t in s.get('next_iteration_focus',[]) if t.get('status')=='pending' and any('window5' in str(a) or '打磨师' in str(a) for a in (t.get('assigned_to') or []))]
print('PENDING',len(pend))
for t in pend:
    print('===',t.get('id'),'|',t.get('priority'),'|',t.get('assigned_to'))
    print('  ',str(t.get('task'))[:400])
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
print('\n--- TLDR gap slugs ---')
for sl in ['perplexity-review-2026','suno-alternatives','chatgpt-vs-claude-2026-comparison','best-ai-productivity-tools-2026']:
    p=by.get(sl)
    if not p: print(sl,'MISSING in posts.json'); continue
    c=p.get('content','')
    print(sl,'| TLDR?',('## TL;DR' in c),'| table?',c.count('|')>=8,'| len',len(c))
