# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
targets=['suno-alternatives-2026','ai-tools-for-beginners-2026','ai-tools-for-non-technical-users-2026']
for p in posts:
    if p.get('slug') not in targets: continue
    c=p.get('content','')
    tmp=base+r'\scripts\_tmp_r26d_'+p['slug']+'.md'
    io.open(tmp,'w',encoding='utf-8').write(c[:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    print('====',p['slug'],'score',r.get('score'))
    for chk in r.get('checks',[]):
        if not chk.get('passed',True):
            print('  FAIL:',chk.get('name'),'|',str(chk.get('detail',''))[:120])
    # existing md features
    import re
    md_h2=len(re.findall(r'(?m)^#{1,2}\s',c))
    md_links=len(re.findall(r'\]\(https?://',c))
    bluf=bool(re.search(r'(?i)(TL;DR|Bottom line|In short:|Key takeaway)',c[:3000]))
    faq='Frequently Asked' in c or 'FAQ' in c
    print('  mdH2=',md_h2,'mdLinks=',md_links,'BLUF=',bluf,'FAQ=',faq,'len=',len(c))
