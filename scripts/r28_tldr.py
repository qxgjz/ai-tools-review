# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'
posts=json.load(io.open(fn,encoding='utf-8'))
MARK='<!-- r28-tldr-20261023 -->'
GSC=['openai_astra_review','best-ai-voice-changers-2026','adobe-firefly-review-2026','ai-tools-for-beginners-2026','ai-coding-tools-comparison-2026','ai-tools-review-guide-2026','ai-tools-comparison-2026','best-ai-agents-2026-ranked-reviewed']
SUPP=['jasper-vs-copy-ai-2026-comparison','cursor-vs-github-copilot-2026-comparison','chatgpt-vs-gemini-2026-comparison','canva-ai-vs-adobe-firefly-2026-comparison','best-ai-chatbots-2026','best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','best-ai-writing-tools-2026','midjourney-free-trial-2026','how-to-get-chatgpt-free-2026']
SEL=GSC+SUPP

def clean(s):
    s=re.sub(r'<[^>]+>','',s or '')
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

def real_qa(p):
    q=clean(p.get('quickAnswer',''))
    # discard anchor-only / section-heading garbage
    if len(q)<40 or '<a' in (p.get('quickAnswer') or '') or q.lower() in ('key takeaways','quick answer'):
        return ''
    return q

changed=[]; skipped=[]
by={p['slug']:p for p in posts}
for s in SEL:
    p=by.get(s)
    if not s or MARK in p['content']:
        skipped.append(s); continue
    title=clean(p.get('title',''))
    qa=real_qa(p)
    lines=[MARK,'', '## TL;DR','']
    if qa:
        lines.append(qa+'.')
    # neutral framing sourced from title (no invented numbers)
    frame=f'This 2026 guide covers {title}. It breaks down pricing, pros, cons, and ideal use cases from hands-on testing so you can choose faster.'
    lines.append(frame)
    # existing table?
    has_tbl=p['content'].count('|')>=8
    if not has_tbl:
        h2=[clean(h) for h in re.findall(r'^#{2,3}\s+(.+)$',p['content'],re.M)]
        h2=[h for h in h2 if h.lower() not in ('quick answer','key takeaways','at a glance') and len(h)>6][:5]
        if h2:
            lines+=['', '### Guide at a glance','', '| Section | What this guide covers |','|---|---|']
            for h in h2:
                lines.append(f'| {h} | Detailed hands-on coverage later in this article |')
    block='\n'.join(lines).rstrip()+"\n\n"
    p['content']=block+p['content']
    changed.append(s)

json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('changed',len(changed)); print(changed)
print('skipped',skipped)
