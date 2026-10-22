# -*- coding: utf-8 -*-
import io,json,os,re,tempfile
from pathlib import Path
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
from zens_ink import content_qc
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
CFG=['best-free-ai-tools-for-students-2026','how-to-get-chatgpt-free-2026','jasper-vs-copy-ai-2026-comparison','best-ai-chatbots-2026','best-ai-crm-tools-2026','best-ai-note-taking-tools-2026','best-ai-legal-tools-2026','best-ai-seo-tools-2026','cursor-vs-github-copilot-2026-comparison']
tmp=Path(tempfile.mkdtemp(prefix='r27v_'))
for p in posts:
    if p['slug'] not in CFG: continue
    t=re.sub(r'<[^>]+>','',p['content']); t=re.sub(r'&nbsp;',' ',t); t=re.sub(r'&amp;','&',t)
    f=tmp/(p['slug'][:50]+'.md'); f.write_text(f"# {p.get('title','')[:60]}\n\n{t}",encoding='utf-8')
    dr=content_qc.check_draft(f)
    fails=[c['check'] for c in dr['checks'] if not c.get('pass',False)]
    print(dr.get('score'),p['slug'],'|',', '.join(fails))
