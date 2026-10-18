import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
rows=[]
for t in s.get('next_iteration_focus',[]):
    a=str(t.get('assigned_to','')).lower()
    if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in a):
        rows.append(t)
rows.sort(key=lambda x:{'P0':0,'P1':1,'P2':2}.get(x.get('priority'),3))
print('PENDING polisher:',len(rows))
for t in rows:
    print('---')
    print('ID:',t.get('id'),'|',t.get('priority'),'| rank',t.get('rank'),'| ctr',t.get('ctr'),'| impr',t.get('impressions'))
    print('TASK:',str(t.get('task',''))[:300])
