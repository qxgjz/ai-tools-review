import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
nf = s.get('next_iteration_focus', [])
targets = ['CTR-20261009-001','CTR-20261009-002','P0-BATCH-CLEAR-2026-10-09-001',
           'P1-CONTENT-CAUSAL-CITE-001','P1-TOOLKIT-CONTRADICTION-FIX-001','P1-TOOL-LLMEVALKIT-001']
for t in nf:
    if t.get('id') in targets:
        print(json.dumps(t, ensure_ascii=False, indent=2))
        print('---')
