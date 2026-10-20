import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
for t in s.get('next_iteration_focus',[]):
    a=str(t.get('assigned_to',''))
    if ('打磨' in a or 'window5' in a.lower()) and t.get('status')=='pending':
        print(t.get('priority'),'|',t.get('id'),'|',t.get('title',t.get('task',''))[:80])
        if t.get('detail'): print('   detail:',str(t.get('detail'))[:300])
        for k in ('pos','ctr_pct','impressions','evidence'):
            if t.get(k): print('   ',k,'=',str(t[k])[:160])
