# -*- coding: utf-8 -*-
import io,re,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
for f in ['out/ai-policy/index.html','out/ai-policy/index.txt']:
    if os.path.exists(f):
        raw=io.open(f,encoding='utf-8',errors='replace').read()
        tm=re.search(r'<title>(.*?)</title>',raw,re.S|re.I)
        dm=re.search(r'<meta\s+name="description"\s+content="([^"]*)"',raw,re.I)
        print(f,'\n title=',tm.group(1).strip() if tm else 'NONE',len(tm.group(1).strip()) if tm else 0)
        print(' desc=',dm.group(1) if dm else 'NONE',len(dm.group(1)) if dm else 0)
# source comparison full record
import json
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
p=next(x for x in posts if x['slug']=='ai-coding-tools-comparison-2026')
print('\nCOMPARISON source keys:',{k:v for k,v in p.items() if k in ('title','excerpt','description','slug')})
