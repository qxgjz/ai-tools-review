# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts={p['slug']:p for p in json.load(io.open('data/posts.json',encoding='utf-8'))}
for slug in ['synthesia-review-2026','tabnine-review-2026','writesonic-review-2026']:
    p=posts[slug]
    tmp=base+r'\scripts\_tmp_r23_'+slug+'.md'
    io.open(tmp,'w',encoding='utf-8').write(p['content'][:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    # shipped-equivalent local index.html: official link present?
    hf=os.path.join('out','blog',slug,'index.html')
    htmllink=''
    if os.path.exists(hf):
        raw=io.open(hf,encoding='utf-8',errors='replace').read()
        m=re.search(r'href="(https?://(?:www\.)?'+re.escape(slug.split('-')[0])+r'[^"]*)"',raw)
        htmllink=m.group(1) if m else 'none'
    print(slug,'b20=',r['score'],'html-official=',htmllink,'wc=',p.get('wordCount'))
