# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
import textstat
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
CFG=['best-free-ai-tools-for-students-2026','how-to-get-chatgpt-free-2026','jasper-vs-copy-ai-2026-comparison','best-ai-chatbots-2026','best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','cursor-vs-github-copilot-2026-comparison']
for p in posts:
    if p['slug'] not in CFG: continue
    t=re.sub(r'<[^>]+>','',p['content'])
    f=textstat.flesch_reading_ease(t)
    print(round(f,1),p['slug'])
