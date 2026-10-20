# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
for slug in ['synthesia-review-2026','tabnine-review-2026','writesonic-review-2026']:
    p=next(x for x in posts if x['slug']==slug)
    tmp=base+r'\scripts\_tmp_r22_'+slug+'.md'
    io.open(tmp,'w',encoding='utf-8').write(p['content'][:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    try:
        res=json.loads(out.stdout)
        r=res[0] if isinstance(res,list) else res
        print('\n===',slug,'score=',r.get('score'))
        for c in r.get('checks',[]):
            if not c.get('pass'): print('  FAIL',c.get('check'),'|',str(c.get('detail',''))[:120])
    except Exception as e:
        print(slug,'PARSE FAIL',e,out.stdout[:300],out.stderr[:300])
