# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts={p['slug']:p for p in json.load(io.open('data/posts.json',encoding='utf-8'))}
for slug in ['best-ai-image-generators-2026','midjourney-v7-vs-dall-e-3-ecommerce','notion-ai-vs-obsidian-ai']:
    p=posts[slug]; c=p['content']
    tmp=base+r'\scripts\_tmp_r24d_'+slug+'.md'
    io.open(tmp,'w',encoding='utf-8').write(c[:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    print('\n===',slug,'score=',r['score'])
    for ch in r['checks']:
        if not ch['pass']: print(' FAIL',ch['weight'],ch['check'],'|',str(ch.get('note',''))[:90])
    head=c[:30000]
    print(' md-outbound=',re.findall(r'\]\((https?://[^)]+)\)',head)[:4])
    print(' md-internal=',re.findall(r'\]\((/[^)]+)\)',head)[:4])
    print(' BLUF=',bool(re.search(r'(TL;DR|tl;dr|Bottom line|In short:|Key takeaway)',head[:3000])),'FAQ=',('Frequently Asked' in head or 'FAQPage' in head))
    print(' mdH2=',len(re.findall(r'(?m)^#{1,2}\s+',head)),'q=',[h for h in re.findall(r'(?m)^#{1,3}\s+(.+)$',head) if h.strip().endswith('?')][:2])
    print(' HEAD>>',c[:400].replace('\n',' | '))
