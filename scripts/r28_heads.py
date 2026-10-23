# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
noTbl=['adobe-firefly-review-2026','ai-tools-for-beginners-2026','ai-coding-tools-comparison-2026','ai-tools-review-guide-2026','ai-tools-comparison-2026','best-ai-note-taking-tools-2026']
for s in noTbl:
    c=by[s]['content']
    h2=re.findall(r'^#{2,3}\s+(.+)$',c,re.M)
    scores=re.findall(r'([A-Za-z0-9 .\/+&-]{2,30}?)\s*[:|]\s*([0-9](?:\.[0-9])?/10)',c)
    print('====',s)
    print(' H2:',[h.strip()[:50] for h in h2][:8])
    print(' SCORES:',scores[:6])
