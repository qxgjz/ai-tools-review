# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p = base + r'\iteration_center\state.json'
st = json.load(io.open(p, encoding='utf-8'))
st['latest_commit'] = '8b687e9'
for e in st.get('iteration_log', []):
    if e.get('batch') == 'batch18':
        e['git'] = '8b687e9'
        e['online_200'] = 'pending-verify'
io.open(p, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('latest_commit:', st['latest_commit'])
