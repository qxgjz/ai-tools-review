# -*- coding: utf-8 -*-
import io,json,os,re,tempfile
from pathlib import Path
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
from zens_ink import content_qc
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
tmp=Path(tempfile.mkdtemp(prefix='r27d_'))
rows=[]
for p in posts:
    content=p.get('content','')
    if len(content)<100: continue
    t=re.sub(r'<[^>]+>','',content); t=re.sub(r'&nbsp;',' ',t); t=re.sub(r'&amp;','&',t)
    f=tmp/(p['slug'][:50]+'.md'); f.write_text(f"# {p.get('title','')[:60]}\n\n{t}",encoding='utf-8')
    dr=content_qc.check_draft(f)
    rows.append((dr.get('score',0),p,dr))
rows.sort(key=lambda r:r[0])
for s,p,dr in rows[7:20]:
    fails=[c['check'] for c in dr['checks'] if not c.get('pass',False)]
    ext=re.findall(r'\]\((https?://[^)]+)\)',p['content'])
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])
    print('==',s,p['slug'])
    print('   T:',p['title'])
    print('   FAIL:',', '.join(fails))
    print('   EXT:',ext[:4])
    print('   INT:',il[:3])
