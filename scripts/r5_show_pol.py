import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
for t in s.get('next_iteration_focus',[]):
    assigned = t.get('assigned_to',[])
    if isinstance(assigned, str): assigned = [assigned]
    is_pol = any('window5' in str(a) or '打磨师' in str(a) or 'polisher' in str(a).lower() for a in assigned)
    if is_pol and t.get('status')=='pending':
        print(json.dumps(t, ensure_ascii=False, indent=2))
        print('---')
