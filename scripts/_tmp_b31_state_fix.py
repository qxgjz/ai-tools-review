# -*- coding: utf-8 -*-
"""batch30/31 state fix: mark git/online/deploy as success after confirmed push + 200 verification"""
import io, json, os

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sp = os.path.join(base, 'iteration_center', 'state.json')
st = json.load(io.open(sp, encoding='utf-8'))

fixed = []
for e in st.get('iteration_log', []):
    b = e.get('batch')
    if b == 'batch30':
        e['git'] = 'pushed: f70961d (remote main == local HEAD 08453b8)'
        e['online_200'] = 'verified: 200 x3 (2026-10-18)'
        e['deploy'] = 'deployed via Cloudflare Pages'
        fixed.append('batch30')
    elif b == 'batch31':
        e['git'] = 'pushed: c7104d5 (remote main == local HEAD 08453b8)'
        e['online_200'] = 'verified: 200 x3 (2026-10-18)'
        e['deploy'] = 'deployed via Cloudflare Pages'
        fixed.append('batch31')

io.open(sp, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('state updated for:', fixed)
