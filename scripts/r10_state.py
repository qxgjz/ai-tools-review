import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
DONE = ['CTR-20261013-01','CTR-20261013-02','CTR-20261013-03','CTR-20261013-04',
        'CTR-20261012-2100','CTR-20261012-2101','CTR-20261012-2102']
for t in s.get('next_iteration_focus',[]):
    if t.get('id') in DONE and t.get('status')=='pending':
        t['status']='completed'
        t['completed_at']='2026-10-13T13:30:00+08:00'
        print('done:', t['id'])
s.setdefault('completed_tasks',[]).insert(0,{
    'id':'POLISH-2026-10-13-R10','priority':'P0',
    'title':'R10: 5 CTR titles + 3 low articles fixed',
    'status':'completed','assigned_to':['polisher'],
    'result':'5 CTR (adobe-firefly/creatium/openai-astra/voice-changers/elevenlabs); perplexity 55->100, ai-coding-compare 60->100, ai-tools-compare 60->100'
})
json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('state updated')
