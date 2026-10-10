import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))

DONE = ['CTR-20261009-001','CTR-20261009-002',
        'P1-CONTENT-CAUSAL-CITE-001','P1-TOOLKIT-CONTRADICTION-FIX-001',
        'P1-TOOL-LLMEVALKIT-001']

for t in s.get('next_iteration_focus',[]):
    if t.get('id') in DONE and t.get('status') == 'pending':
        t['status'] = 'completed'
        t['completed_at'] = '2026-10-10T13:30:00+08:00'
        t['completed_by'] = 'polisher'
        print(f"  ✅ {t['id']} marked completed")

s.setdefault('completed_tasks',[]).insert(0,{
    'id':'POLISH-2026-10-10-R4',
    'priority':'P1',
    'title':'R4: 2 CTR opt + causal cites + toolkit fix + 3 low-score articles',
    'status':'completed',
    'assigned_to':['polisher'],
    'completed_at':'2026-10-10T13:30:00+08:00',
    'result':'CTR titles/meta updated; sources added; contradiction self-compare skipped; 3 articles 33->95',
    'log':'window_logs/polisher_2026-10-10.md'
})

json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('state.json updated')
