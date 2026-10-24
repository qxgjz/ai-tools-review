# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
def clean(s):
    s=re.sub(r'<[^>]+>','',s or ''); s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
def dom(u):
    d=re.sub(r'^https?://','',u).split('/')[0].replace('www.','')
    return d.split('.')[0].capitalize()
TLDR={
'perplexity-review-2026':('Perplexity is our top-rated AI answer engine for 2026, returning cited answers drawn from the live web rather than a frozen training cutoff. This review covers answer accuracy, the free tier versus Pro pricing, privacy handling, and how it compares with ChatGPT and standard web search.',True),
'suno-alternatives':('Udio is the best overall Suno alternative in 2026 for full-length songs, ElevenLabs Music wins short clips and API work, and Stable Audio is the producer pick. Compare pricing, credit economics and use cases below before you switch off Suno.',False),
'chatgpt-vs-claude-2026-comparison':('ChatGPT leads in ecosystem breadth and multimodal convenience, while Claude leads in long-context accuracy and careful writing. This side-by-side compares coding, pricing, safety and multimodal input so you can choose the right assistant in 2026.',False),
'best-ai-productivity-tools-2026':('Notion AI is our top pick for the best AI productivity tool in 2026, combining notes, docs and lightweight automation in one workspace. Compare the top 10 work assistants on pricing, automation depth and team fit below.',False),
'midjourney-vs-dalle-3-2026':('MidJourney wins on image quality and artistry, while DALL-E 3 wins on ease of use and tight prompt-following. This comparison covers output quality, pricing, style control and which tool suits creators in 2026.',False),
}
AFF=['best-ai-presentation-tools-2026','beautiful-ai-alternatives','sudowrite-alternatives','perplexity-vs-chatgpt-2026','best-ai-music-generators-2026','best-ai-text-to-speech-tools-2026','best-ai-spreadsheet-tools-2026','best-ai-sql-generators-2026','best-ai-summarizer-tools-2026','clearscope-alternatives']
done=[]
for sl,(t,needtbl) in TLDR.items():
    p=by[sl]
    if 'r30-tldr-20261024' in p['content']: continue
    block=['<!-- r30-tldr-20261024 -->','', '## TL;DR', '', t, '']
    if needtbl:
        h2s=re.findall(r'^## (.+)$',p['content'],re.M)[:6]
        block+=['### What this review covers','','| Section | What you will learn |','|---|---|']
        for h in h2s: block.append(f'| {h} | {h} details, pricing and verdict |')
        block.append('')
    p['content']='\n'.join(block).rstrip()+"\n\n"+p['content']; done.append('TLDR:'+sl)
for sl in AFF:
    p=by[sl]
    if 'r30-aff-20261024' in p['content']: continue
    verdict=clean(p.get('quickAnswer','')).replace('Quick Answer:','').strip()
    verdict=verdict.split('. ')[0]+'.' if len(verdict)>120 else verdict
    aff=p.get('affiliateLinks') or []
    links=aff[:3]
    block=['<!-- r30-aff-20261024 -->','', '## Quick Verdict','', verdict, '', '**Get started:**']
    block+= [f'- [{dom(u)}]({u})' for u in links]
    block.append('')
    p['content']='\n'.join(block).rstrip()+"\n\n"+p['content']; done.append('AFF:'+sl)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('done',len(done)); [print(' ',x) for x in done]
