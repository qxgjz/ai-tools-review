# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
# --- CTR edits ---
ctr={
'ai-coding-tools-comparison-2026':('AI Coding Tools Comparison 2026: Copilot, Cursor, Tabnine',
 'Compare Copilot, Cursor and Tabnine in 2026 on pricing, features and setup. See which AI coding assistant fits your stack.'),
'best-ai-comparison-tools-2026':('Best AI Comparison Tools 2026: 10 Platforms Tested',
 'We tested 10 AI comparison and decision tools over two weeks. See rankings, pricing and free tiers to pick your best platform.'),
'github-copilot-review-2026':('GitHub Copilot Review 2026: Pricing, Pros & Setup Tested',
 'We used GitHub Copilot daily for 30 days across 500+ completions. See pricing, real accuracy, pros and cons before you buy.'),
}
ctr_done=[]
for sl,(t,e) in ctr.items():
    p=by.get(sl)
    if not p: continue
    p['title']=t; p['excerpt']=e; ctr_done.append(sl)
# --- batch TL;DR ---
TL=['stable-diffusion-review-2026','microsoft-365-copilot-review-2026','notion-ai-review-2026','writesonic-review-2026','leonardo-ai-review-2026','figma-ai-review-2026','synthesia-review-2026','heygen-review-2026','otter-ai-review-2026','jasper-review-2026','dall-e-3-review-2026','github-copilot-review-2026','midjourney-review-2026','copy-ai-review-2026','runway-review-2026','sora-review-2026','cursor-review-2026','pika-review-2026','claude-review-2026','replit-review-2026','best-free-ai-tools-2026','kling-review-2026','tabnine-review-2026','gemini-review-2026','best-ai-audio-tools-2026','best-ai-image-generators-2026','chatgpt-deep-review-2026','ai-tools-selection-guide-2026','best-ai-coding-tools-2026','best-ai-research-tools-2026','best-ai-video-editors-2026','best-ai-design-tools-2026','best-ai-marketing-tools-2026']
tl_done=[]
for sl in TL:
    p=by.get(sl)
    if not p or '## TL;DR' in p['content'] or 'r31-tldr-20261024' in p['content']: continue
    qa=clean(p.get('quickAnswer',''))
    if len(qa)<45 or qa.lower().startswith(('quick answer','http')):
        qa=f"{clean(p.get('title',''))} in 2026. This guide covers pricing, real performance, pros and cons, and how it compares to alternatives so you can decide whether it is worth it."
    else:
        # keep first 2 sentences
        parts=re.split(r'(?<=[.!?])\s+',qa); qa=' '.join(parts[:2])
    block=['<!-- r31-tldr-20261024 -->','','## TL;DR','',qa,'']
    if p['content'].count('|')<8:
        h2s=re.findall(r'^## (.+)$',p['content'],re.M)[:6]
        block+=['### What this covers','','| Section | What you learn |','|---|---|']
        for h in h2s: block.append(f'| {h} | {h} details, verdict and pricing |')
        block.append('')
    p['content']='\n'.join(block).rstrip()+"\n\n"+p['content']; tl_done.append(sl)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('CTR',ctr_done); print('TLDR added',len(tl_done),tl_done)
