# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
want=['best-ai-crm-tools-2026','best-ai-project-management-tools-2026','best-ai-note-taking-tools-2026','best-ai-design-tools-2026','best-ai-email-tools-2026','best-ai-transcription-tools-2026','best-ai-chatbots-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','best-ai-video-editors-2026','best-ai-writing-tools-2026','midjourney-vs-dall-e-3-2026-comparison','cursor-vs-github-copilot-2026-comparison','chatgpt-vs-gemini-2026-comparison','canva-ai-vs-adobe-firefly-2026-comparison']
for p in posts:
    if p['slug'] not in want: continue
    urls=re.findall(r'https?://[^\s\)\]\"<>]+',p['content'])
    dom=[]
    for u in urls:
        m=re.match(r'https?://(?:www\.)?([^/]+)',u)
        if m and m.group(1) not in dom: dom.append(m.group(1))
    print('==',p['slug'])
    print('   domains:',dom[:8])
