# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
gsc=['openai_astra_review','best-ai-voice-changers-2026','adobe-firefly-review-2026','ai-tools-for-beginners-2026','ai-coding-tools-comparison-2026','ai-tools-review-guide-2026','ai-tools-comparison-2026','best-ai-agents-2026-ranked-reviewed']
by={p['slug']:p for p in posts}
for s in gsc:
    p=by.get(s)
    if not p: print('MISSING',s); continue
    c=p['content']
    has_tldr='TL;DR' in c or 'TLDR' in c or 'tldr' in c
    has_table='|' in c and c.count('|')>=8
    print('====',s,'tldr=',has_tldr,'table=',has_table,'wc=',len(re.findall(r'[A-Za-z]+',c)))
    print(' QA:',str(p.get('quickAnswer'))[:150])
    print(' KT:',json.dumps(p.get('keyTakeaways'),ensure_ascii=False)[:220])
    # first existing table header line
    tl=[ln for ln in c.splitlines() if ln.strip().startswith('|')][:2]
    print(' TBL:',tl)
