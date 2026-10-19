import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
close={'P0-CMD-POLISH-FAKE-FIX-20261019':
 'R20 fixed content_drafts/published/2026-09-16-best-ai-voice-changers-2026_READY.md: added YAML frontmatter title60c/desc149c/date+updated, Bottom-line BLUF, question H2; check_draft 68->100 all-pass'}
n=0
for t in s['next_iteration_focus']:
    if t.get('id') in close and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']='2026-10-19'; t['close_note']=close[t['id']]; n+=1
s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-19-R20','priority':'P0','status':'completed','assigned_to':['window5','打磨师'],
 'title':'R20: fix P0 fake-fix voice-changers READY.md 68->100; fix pika/runway/sora to 100',
 'result':'READY.md frontmatter+BLUF+question H2=100; pika/runway/sora BLUF+official links+clean titles=100'})
json.dump(s,open('iteration_center/state.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',n)
for t in s['next_iteration_focus']:
    if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in str(t.get('assigned_to','')).lower()):
        print('LEFT',t.get('priority'),t.get('id'))
