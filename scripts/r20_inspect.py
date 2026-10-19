import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
pend=[]
for t in s.get('next_iteration_focus',[]):
    a=str(t.get('assigned_to','')).lower()
    if t.get('status')=='pending' and ('window5' in a or '打磨' in str(t.get('assigned_to',''))):
        pend.append(t)
print('PENDING count=',len(pend))
for t in pend:
    print('\n###',t.get('id'),'|',t.get('priority'),'|',t.get('status'))
    for k in ('task','source','pos','ctr_pct','impressions','url','page','slug','created_at'):
        if k in t and t[k] is not None: print(f'  {k}: {t[k]}')
