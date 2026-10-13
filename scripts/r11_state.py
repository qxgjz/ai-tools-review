import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
s.setdefault('completed_tasks',[]).insert(0,{
    'id':'POLISH-2026-10-13-R11','priority':'P1',
    'title':'R11: HTML->MD fix 3 articles (60->100)',
    'status':'completed','assigned_to':['polisher'],
    'result':'ai-tools-for-beginners 60->100, ai-tools-review-guide 60->100, ai-tools-selection-guide 60->100'
})
json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('state updated')
