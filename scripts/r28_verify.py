# -*- coding: utf-8 -*-
import io,json,os,re,tempfile
from pathlib import Path
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
from zens_ink import content_qc
SEL=['openai_astra_review','best-ai-voice-changers-2026','adobe-firefly-review-2026','ai-tools-for-beginners-2026','ai-coding-tools-comparison-2026','ai-tools-review-guide-2026','ai-tools-comparison-2026','best-ai-agents-2026-ranked-reviewed','jasper-vs-copy-ai-2026-comparison','cursor-vs-github-copilot-2026-comparison','chatgpt-vs-gemini-2026-comparison','canva-ai-vs-adobe-firefly-2026-comparison','best-ai-chatbots-2026','best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','best-ai-writing-tools-2026','midjourney-free-trial-2026','how-to-get-chatgpt-free-2026']
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
tmp=Path(tempfile.mkdtemp(prefix='r28v_'))
bad=[]
for s in SEL:
    p=by[s]; c=p['content']
    has_tldr='## TL;DR' in c
    has_tbl=c.count('|')>=8
    t=re.sub(r'<[^>]+>','',c); t=re.sub(r'&nbsp;',' ',t); t=re.sub(r'&amp;','&',t)
    f=tmp/(s[:50]+'.md'); f.write_text(f"# {p.get('title','')[:60]}\n\n{t}",encoding='utf-8')
    dr=content_qc.check_draft(f)
    flag='OK' if (has_tldr and has_tbl and dr['score']>=70) else 'FAIL'
    if flag=='FAIL': bad.append(s)
    print(f"{dr['score']:>3} tldr={int(has_tldr)} tbl={int(has_tbl)} {flag} {s}")
print('BAD',bad)
