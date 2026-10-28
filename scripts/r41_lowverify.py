# -*- coding: utf-8 -*-
import io,json,os,re,tempfile
from pathlib import Path
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
from zens_ink import content_qc
SEL=['best-ai-text-generators-2026','best-ai-personal-assistant-2026','best-ai-tools-for-startups-2026']
def syl(w):
    w=re.sub(r'[^a-z]','',w.lower()); n=len(re.findall(r'[aeiouy]+',w))
    if w.endswith('e'): n-=1
    return max(1,n)
def flesch(t):
    s=[x for x in re.split(r'[.!?]+',t) if x.strip()]; w=re.findall(r"[A-Za-z']+",t)
    if not s or not w: return 0
    return 206.835-1.015*len(w)/len(s)-84.6*sum(syl(x) for x in w)/len(w)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
tmp=Path(tempfile.mkdtemp(prefix='r41v_'))
for s in SEL:
    p=by[s]; c=p['content']; t=re.sub(r'<[^>]+>','',c); t=re.sub(r'&nbsp;',' ',t)
    f=tmp/(s[:50]+'.md'); f.write_text(f"# {p.get('title','')[:60]}\n\n{t}",encoding='utf-8')
    dr=content_qc.check_draft(f)
    print(dr['score'],round(flesch(c),1),s)
