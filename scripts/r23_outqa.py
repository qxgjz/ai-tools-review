# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
for slug in ['synthesia-review-2026','tabnine-review-2026','writesonic-review-2026']:
    f=os.path.join('out','blog',slug,'index.txt')
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',f,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    try:
        res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
    except Exception as e:
        print(slug,'PARSE FAIL',e,out.stdout[:200],out.stderr[:200]);continue
    print('\n===',slug,'score=',r.get('score'))
    for c in r['checks']:
        if not c['pass']: print(' FAIL',c['weight'],c['check'],'|',str(c.get('note',''))[:70])
