# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
targets=['suno-alternatives-2026','ai-tools-for-beginners-2026','ai-tools-for-non-technical-users-2026']
for p in posts:
    if p.get('slug') not in targets: continue
    c=p['content']
    tmp=base+r'\scripts\_tmp_r26d2_'+p['slug']+'.md'
    io.open(tmp,'w',encoding='utf-8').write(c[:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    r=json.loads(out.stdout); r=r[0] if isinstance(r,list) else r
    print('====',p['slug'],'score',r['score'])
    for chk in r['checks']:
        if not chk['pass']:
            print('  FAIL w%d'%chk['weight'],chk['check'],'::',chk.get('note',''))
    ext=re.findall(r'\]\((https?://[^)]+)\)',c)
    internal=re.findall(r'\]\((/(?:blog|tools|compare)[^)]*)\)',c)
    print('  EXTERNAL md:',ext)
    print('  INTERNAL md:',internal[:5])
    qh2=re.findall(r'(?m)^#{1,3}\s*(.*\?)\s*$',c)
    print('  QHEADINGS:',qh2[:3])
