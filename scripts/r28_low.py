# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
want=['best-ai-project-management-tools-2026','best-ai-design-tools-2026','best-ai-email-tools-2026','best-ai-transcription-tools-2026','best-ai-video-editors-2026','midjourney-vs-dall-e-3-2026-comparison','cursor-alternatives-2026','free-ai-tools-for-students-2026','perplexity-alternatives-2026']
by={p['slug']:p for p in posts}
for s in want:
    p=by.get(s)
    if not p: print('MISS',s); continue
    ext=[]
    for u in re.findall(r'https?://(?:www\.)?([^\s\)\]\"/<>]+)',p['content']):
        if u not in ext and 'aitoolcrux.com' not in u: ext.append(u)
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])[:2]
    faq=p.get('faq') or []
    print('====',s)
    print('QA:',re.sub(r'<[^>]+>','',str(p.get('quickAnswer','')))[:160])
    print('EXT:',ext[:3],'| INT:',il,'| FAQn=',len(faq))
    print('KT:',json.dumps(p.get('keyTakeaways'),ensure_ascii=False)[:180])
