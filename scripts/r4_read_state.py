import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
print('keys:', list(s.keys()))
nf = s.get('next_iteration_focus', [])
print(f'\nnext_iteration_focus: {len(nf)} items')
for t in nf:
    assigned = t.get('assigned_to', [])
    if isinstance(assigned, str): assigned = [assigned]
    is_polisher = any('window5' in str(a) or '打磨师' in str(a) or 'polisher' in str(a).lower() for a in assigned)
    status = t.get('status','?')
    mark = '★' if (is_polisher and status=='pending') else ' '
    print(f"  {mark} [{status:>10}] P={t.get('priority','?'):>3}  assigned={assigned}  id={t.get('id','?')}  title={t.get('title','?')[:80]}")
