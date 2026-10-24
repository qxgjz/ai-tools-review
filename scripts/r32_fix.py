# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
# CTR
ctr={'best-ai-observability-tools-2026':('Best AI Observability Tools 2026: 10 Platforms Tested',
 'We tested 10 LLM observability tools on tracing, evals and pricing. See rankings, free tiers and enterprise options to monitor AI apps.'),
'gemini-pricing-2026':('Gemini Pricing 2026: Free vs Advanced Plans, Costs Explained',
 'Gemini pricing in 2026: free tier, Advanced plan and API costs broken down. See what you get at each tier and whether it is worth upgrading.')}
cd=[]
for sl,(t,e) in ctr.items():
    p=by.get(sl)
    if p: p['title']=t; p['excerpt']=e; cd.append(sl)
# TLDR batch
TL=['creatium-coach-review-2025','claude_fable_51_review','midjourney-vs-dall-e-3-2026-comparison','canva-ai-alternatives-2026','cursor-ai-review-2026-best-ai-code-editor','midjourney-vs-dalle-3-2026-comparison','how-to-use-cursor-for-react-development','best-ai-transcription-tools-2026','windsurf-review-2026','best-ai-customer-support-tools-2026','best-ai-comparison-tools-2026','best-ai-3d-generators-2026','best-ai-meeting-assistants-2026','cursor-alternatives-2026','best-free-ai-tools-for-youtube-creators','best-ai-email-tools-2026','best-ai-observability-tools-2026','windsurf-vs-cursor-2026','free-ai-tools-for-students-2026','best-ai-pr-tools-2026','best-ai-automation-agents-2026','best-ai-project-management-tools-2026','best-ai-grammar-checkers-2026','best-ai-photo-editors-2026','best-ai-logo-generators-2026','best-ai-voice-generators-2026','best-ai-resume-builders-2026','best-ai-chatbot-builders-2026','n8n-review-2026','best-ai-translation-tools-2026','gemini-pricing-2026','best-ai-gaming-tools-2026']
td=[]
for sl in TL:
    p=by.get(sl)
    if not p or '## TL;DR' in p['content'] or 'r32-tldr' in p['content']: continue
    qa=clean(p.get('quickAnswer',''))
    if len(qa)<45 or qa.lower().startswith(('quick answer','http')):
        qa=f"{clean(p.get('title',''))} in 2026. This guide covers pricing, real performance, pros and cons, and how it compares to alternatives so you can decide whether it is worth it."
    else:
        parts=re.split(r'(?<=[.!?])\s+',qa); qa=' '.join(parts[:2])
    block=['<!-- r32-tldr-20261025 -->','','## TL;DR','',qa,'']
    if p['content'].count('|')<8:
        h2s=re.findall(r'^## (.+)$',p['content'],re.M)[:6]
        block+=['','### What this covers','','| Section | What you learn |','|---|---|']
        for h in h2s: block.append(f'| {h} | {h} details, verdict and pricing |')
        block.append('')
    p['content']='\n'.join(block).rstrip()+"\n\n"+p['content']; td.append(sl)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('CTR',cd); print('TLDR',len(td),td)
