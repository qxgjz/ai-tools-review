import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
close={'P1-CTR-12WORDS-20261020':
 'R21 live GSC(09-13~10-10) only 7 pos5-15 zero-click signals, not 12. Restored 3 lost ugly-URL 301s (171438/173022 creatium->creatium-coach-review-2025/, 173210 elevenlabs->elevenlabs-review-2026/); adobe-firefly(pos5.2/26impr) already optimized 58c/154c; ai-tools-comparison already 58c/148c; midjourney/voice-changer queries=1impr noise, no action. 3 low articles synthesia/tabnine/writesonic 75->100.'}
n=0
for t in s['next_iteration_focus']:
    if t.get('id') in close and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']='2026-10-20'; t['close_note']=close[t['id']]; n+=1
s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-20-R21','priority':'P1','status':'completed','assigned_to':['window5','打磨师'],
 'title':'R21: CTR-12WORDS verified+301 restored; synthesia/tabnine/writesonic 75->100',
 'result':'3 ugly-URL 301 restored; firefly/comparison already optimized; 3 low articles to 100'})
json.dump(s,open('iteration_center/state.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',n)
for t in s['next_iteration_focus']:
    if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in str(t.get('assigned_to','')).lower()):
        print('LEFT',t.get('priority'),t.get('id'))
