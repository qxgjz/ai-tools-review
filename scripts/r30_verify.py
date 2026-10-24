# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
for sl in ['perplexity-review-2026','suno-alternatives','chatgpt-vs-claude-2026-comparison','best-ai-productivity-tools-2026','midjourney-vs-dalle-3-2026']:
    c=by[sl]['content']; m=re.search(r'## TL;DR\s*(.*?)(?:\n## |\Z)',c,re.S)
    body=re.sub(r'!\[[^\]]*\]\([^)]*\)','',m.group(1)) if m else ''
    body=re.sub(r'\|.*','',body).strip()
    sents=[x for x in re.split(r'(?<=[.!?])\s+',body) if len(x)>15]
    print(sl,'| TLDR句子',len(sents),'| table',c.count('|')>=8,'| r30块','r30-tldr-20261024' in c)
print('--- AFF ---')
for sl in ['best-ai-presentation-tools-2026','clearscope-alternatives','perplexity-vs-chatgpt-2026']:
    c=by[sl]['content']; head=c[:600]
    print(sl,'| verdict在前100字',('Quick Verdict' in c[:300]),'| aff链接数',len(re.findall(r'https?://',head)))
