# -*- coding: utf-8 -*-
import io,json,os,subprocess
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
# git sync
def g(args):
    return subprocess.run(['git']+args,capture_output=True,text=True,encoding='utf-8',errors='replace')
print('HEAD',g(['rev-parse','HEAD']).stdout.strip())
print('ORIGIN',g(['rev-parse','origin/main']).stdout.strip())
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
mine=[]
for t in s['next_iteration_focus']:
    a=t.get('assigned_to') or []
    if any(x in a for x in ['window5','打磨师']) and t.get('status')=='pending':
        mine.append(t)
order={'P0':0,'P1':1,'P2':2}
mine.sort(key=lambda t:order.get(t.get('priority','P9'),9))
print('\n=== MINE pending',len(mine),'===')
for t in mine:
    cid=t.get('id','')
    flag='CTR' if 'CTR' in cid.upper() or 'CTR' in str(t.get('task','')).upper() else ''
    print(f"[{t.get('priority')}] {cid} {flag} :: {str(t.get('task',''))[:110]}")
