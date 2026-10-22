# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
# corpus-wide verified domain per tool keyword
want=['best-free-ai-tools-for-students-2026','how-to-get-chatgpt-free-2026','jasper-vs-copy-ai-2026-comparison','best-ai-chatbots-2026','best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','best-ai-writing-tools-2026','cursor-vs-github-copilot-2026-comparison','chatgpt-vs-gemini-2026-comparison','canva-ai-vs-adobe-firefly-2026-comparison']
for p in posts:
    if p['slug'] not in want: continue
    ext=[]
    for u in re.findall(r'https?://(?:www\.)?([^\s\)\]\"/<>]+)',p['content']):
        if u not in ext and 'aitoolcrux.com' not in u: ext.append(u)
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])
    faq=p.get('faq') or []
    print('====',p['slug'])
    print('QA:',str(p.get('quickAnswer',''))[:160])
    print('EXT:',ext[:4])
    print('INT:',il[:3])
    print('KT:',p.get('keyTakeaways'))
    print('FAQn=',len(faq),'| q1:',str(faq[0].get('question',''))[:90] if faq else None)
