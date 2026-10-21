# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts={p['slug']:p for p in json.load(io.open('data/posts.json',encoding='utf-8'))}
for slug in ['stable-diffusion-review-2026','best-ai-audio-tools-2026','replit-review-2026']:
    p=posts[slug]; c=p['content']
    tmp=base+r'\scripts\_tmp_d_'+slug+'.md'
    io.open(tmp,'w',encoding='utf-8').write(c[:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    print('\n===',slug,'score=',r['score'])
    for ch in r['checks']:
        if not ch['pass']: print(' FAIL',ch['weight'],ch['check'],'|',str(ch.get('note',''))[:80])
    head=c[:30000]
    print(' head outbound=',re.findall(r'\]\((https?://[^)]+)\)',head))
    print(' head BLUF=',bool(re.search(r'(TL;DR|tl;dr|Bottom line|In short:|Key takeaway)',head[:3000])))
    print(' head FAQ=',('Frequently Asked' in head or 'FAQPage' in head))
    print(' H2 count=',len(re.findall(r'(?m)^#{1,2}\s+',head)),'questionH=',[h for h in re.findall(r'(?m)^#{1,3}\s+(.+)$',head) if h.strip().endswith('?')][:2])
