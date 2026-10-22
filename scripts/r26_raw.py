# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
for p in posts:
    if p.get('slug')!='ai-tools-for-beginners-2026': continue
    c=p['content'][:30000]
    tmp=base+r'\scripts\_tmp_r26raw.md'
    io.open(tmp,'w',encoding='utf-8').write(c)
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    print('KEYS',list(r.keys()))
    print(json.dumps(r,ensure_ascii=False,indent=1)[:3500])
