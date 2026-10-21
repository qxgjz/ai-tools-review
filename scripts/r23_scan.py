# -*- coding: utf-8 -*-
import io,json,subprocess,sys,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
rows=[]
for p in posts:
    c=p.get('content','')
    if not c: continue
    tmp=base+r'\scripts\_tmp_r23scan_'+p['slug'].replace('/','_')+'.md'
    io.open(tmp,'w',encoding='utf-8').write(c[:30000])
    out=subprocess.run([sys.executable,'-m','zens_ink.content_qc',tmp,'--format','json'],capture_output=True,text=True,encoding='utf-8')
    try:
        res=json.loads(out.stdout); r=res[0] if isinstance(res,list) else res
        rows.append((r['score'],p['slug']))
    except Exception:
        rows.append((-1,p['slug']))
rows.sort()
print('TOTAL',len(rows),'LOW<70:',sum(1 for s,_ in rows if s<70))
for s,slug in rows[:12]:
    print(s,slug)
