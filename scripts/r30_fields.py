# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
def clean(s):
    s=re.sub(r'<[^>]+>','',s or ''); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
by={p['slug']:p for p in posts}
for sl in ['perplexity-review-2026','suno-alternatives','chatgpt-vs-claude-2026-comparison','best-ai-productivity-tools-2026']:
    p=by[sl]; c=p['content']
    print('====',sl,'| title=',p.get('title','')[:70])
    print('  QA:',clean(p.get('quickAnswer',''))[:200])
    print('  affil:',(p.get('affiliateLinks') or [])[:4])
    print('  H2s:',re.findall(r'^## (.+)$',c,re.M)[:8])
# 5th candidate: no TLDR, high value, has table
print('\n--- candidates no TLDR ---')
cand=[p['slug'] for p in posts if '## TL;DR' not in p['content'] and p['content'].count('|')>=8 and len(p['content'])>8000]
print(cand[:25])
# affiliate distribution
aff=[(p['slug'],len(p.get('affiliateLinks') or [])) for p in posts if p.get('affiliateLinks')]
print('\nposts with affiliateLinks:',len(aff))
for x in sorted(aff,key=lambda x:-x[1])[:15]: print(' ',x)
