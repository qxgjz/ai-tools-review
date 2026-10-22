# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
want=['best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-chatbots-2026','cursor-vs-github-copilot-2026-comparison']
for p in posts:
    if p['slug'] not in want: continue
    print('====',p['slug'])
    for k in ['affiliateLinks','internalLinks','faq','quickAnswer','keyTakeaways']:
        v=p.get(k)
        print(' ',k,'=',json.dumps(v,ensure_ascii=False)[:400])
