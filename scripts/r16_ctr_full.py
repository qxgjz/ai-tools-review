import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
for t in s['next_iteration_focus']:
    if str(t.get('id','')).startswith('CTR-20261017'):
        print(json.dumps(t, ensure_ascii=False, indent=1))
        print('-'*60)
