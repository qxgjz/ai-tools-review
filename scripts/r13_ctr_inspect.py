import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
tasks = s.get('next_iteration_focus',[])
for t in tasks:
    tid = t.get('id','')
    if 'CTR' in tid:
        print('===', tid, '===')
        print(json.dumps(t, ensure_ascii=False, indent=2)[:800])
        print()
