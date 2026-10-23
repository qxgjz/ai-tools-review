# -*- coding: utf-8 -*-
import io,json,os,re,tempfile
from pathlib import Path
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
from zens_ink import content_qc
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
tmp=Path(tempfile.mkdtemp(prefix='r28_'))
rows=[]
for p in posts:
    content=p.get('content','')
    if not content or len(content)<100:
        rows.append((-1,p.get('slug'),['empty'])); continue
    t=re.sub(r'<[^>]+>','',content); t=re.sub(r'&nbsp;',' ',t); t=re.sub(r'&amp;','&',t)
    f=tmp/(p['slug'][:50]+'.md'); f.write_text(f"# {p.get('title','')[:60]}\n\n{t}",encoding='utf-8')
    try:
        dr=content_qc.check_draft(f)
        fails=[c['check'] for c in dr.get('checks',[]) if not c.get('pass',False)]
        rows.append((dr.get('score',0),p['slug'],fails))
    except Exception as e:
        rows.append((-2,p['slug'],[str(e)[:80]]))
rows.sort(key=lambda r:r[0])
low=[r for r in rows if 0<=r[0]<70]
print('TOTAL',len(rows),'LOW<70',len(low))
for s,sl,fails in rows[:18]:
    print(s,sl,'|',', '.join(fails)[:120])
