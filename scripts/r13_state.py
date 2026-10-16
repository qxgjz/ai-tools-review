import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))

# Mark 3 CTR tasks as completed
ctr_ids = ['CTR-20261014-01','CTR-20261014-02','CTR-20261014-03']
for t in s.get('next_iteration_focus',[]):
    if t.get('id') in ctr_ids and t.get('status')=='pending':
        t['status'] = 'completed'
        t['completed_at'] = '2026-10-16'

s.setdefault('completed_tasks',[]).insert(0,{
    'id':'POLISH-2026-10-16-R13','priority':'P1',
    'title':'R13: 3 CTR tasks closed + HTML->MD fix 3 articles (60->100)',
    'status':'completed','assigned_to':['polisher'],
    'result':'3 CTR closed (1 title already optimized, 2 already 301); canva-ai-alternatives/chatgpt-alternatives/chatgpt-deep-review 60->100'
})
json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('state updated')
