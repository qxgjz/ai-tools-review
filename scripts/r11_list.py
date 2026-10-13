import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
tasks = s.get('next_iteration_focus',[])
mine = [t for t in tasks if t.get('status')=='pending' and ('window5' in str(t.get('assigned_to','')) or '打磨师' in str(t.get('assigned_to','')) or 'polisher' in str(t.get('assigned_to','')).lower())]
print(f'pending polisher tasks: {len(mine)}')
for t in mine:
    tid = t.get('id','?')
    pri = t.get('priority','?')
    task = str(t.get('task', t.get('title','')))[:100]
    print(f'  [{pri}] {tid}: {task}')
