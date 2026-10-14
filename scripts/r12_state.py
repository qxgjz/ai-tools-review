import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
s.setdefault('completed_tasks',[]).insert(0,{
    'id':'POLISH-2026-10-14-R12','priority':'P1',
    'title':'R12: HTML->MD fix 3 articles (60->100)',
    'status':'completed','assigned_to':['polisher'],
    'result':'best-free-ai-tools 60->100, best-free-ai-tools-youtube 60->100 (excerpt added), best-paid-ai-tools 60->100'
})
json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('state updated')
