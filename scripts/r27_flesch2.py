# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
def syl(w):
    w=re.sub(r'[^a-z]','',w.lower())
    if not w: return 0
    groups=re.findall(r'[aeiouy]+',w)
    n=len(groups)
    if w.endswith('e'): n-=1
    return max(1,n)
def flesch(t):
    t=re.sub(r'<[^>]+>',' ',t)
    sents=[s for s in re.split(r'[.!?]+',t) if s.strip()]
    words=re.findall(r"[A-Za-z']+",t)
    if not sents or not words: return 0
    sw=len(words)/len(sents)
    sy=sum(syl(w) for w in words)/len(words)
    return 206.835-1.015*sw-84.6*sy
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
CFG=['best-free-ai-tools-for-students-2026','how-to-get-chatgpt-free-2026','jasper-vs-copy-ai-2026-comparison','best-ai-chatbots-2026','best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','cursor-vs-github-copilot-2026-comparison']
for p in posts:
    if p['slug'] not in CFG: continue
    print(round(flesch(p['content']),1),p['slug'])
