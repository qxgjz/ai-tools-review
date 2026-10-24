# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
def clean(s):
    s=re.sub(r'<[^>]+>','',s or ''); s=re.sub(r'\*\*','',s); s=re.sub(r'!?:?\[?[^\]]*\]\([^)]*\)','',s); s=re.sub(r'\s+',' ',s).strip(); return s
print('== 5th midjourney-vs-dalle-3-2026 ==')
p=by['midjourney-vs-dalle-3-2026']; print('QA:',clean(p.get('quickAnswer',''))[:200]); print('table',p['content'].count('|')>=8)
AFF=['best-ai-presentation-tools-2026','beautiful-ai-alternatives','sudowrite-alternatives','perplexity-vs-chatgpt-2026','best-ai-music-generators-2026','best-ai-text-to-speech-tools-2026','best-ai-spreadsheet-tools-2026','best-ai-sql-generators-2026','best-ai-summarizer-tools-2026','clearscope-alternatives']
for sl in AFF:
    p=by[sl]
    print('====',sl,'| table',p['content'].count('|')>=8,'| alreadyVerdict',('Quick Verdict' in p['content']))
    print('  QA:',clean(p.get('quickAnswer',''))[:160])
    print('  AFF:',p.get('affiliateLinks'))
