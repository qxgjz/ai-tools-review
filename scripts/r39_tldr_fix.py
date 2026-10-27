# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
MARK='<!-- r39-tldr-20261027 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
TARGETS=[
'best-paid-ai-tools-worth-buying-2026','dify-vs-langchain-2026','gemini-alternatives-2026',
'cursor-vs-windsurf-2026','notion-ai-vs-obsidian-2026','notion-ai-alternative-2026',
'jasper-ai-alternative-2026','chatgpt-vs-claude-2026','best-ai-slack-bots-2026',
'best-ai-scheduling-tools-2026',
]
done=[]
for sl in TARGETS:
    p=by.get(sl)
    if not p or MARK in p['content']: continue
    qa=clean(p.get('quickAnswer','')).replace('Quick Answer:','').strip()
    if len(qa)<45 or qa.lower().startswith(('quick answer','http','<a')):
        title=clean(p.get('title',''))
        qa=f"{title} compares the top options on pricing, ease of use and output quality so you can pick fast."
    kt=[clean(x) for x in (p.get('keyTakeaways') or []) if clean(x)]
    block=[MARK,'', '## TL;DR','', qa,'']
    if kt:
        block+=['**Key takeaways**']+[f'- {k}' for k in kt[:4]]+['']
    p['content']='\n'.join(block).rstrip()+"\n\n"+p['content']; done.append(sl)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('changed',len(done),done)
