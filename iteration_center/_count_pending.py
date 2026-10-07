import json
with open(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json','r',encoding='utf-8') as f:
    s = json.load(f)
t = s['next_iteration_focus']
w3 = [x for x in t if 'window3' in x.get('assigned_to',[])]
p0 = [x for x in w3 if x.get('priority')=='P0' and x.get('status')=='pending']
p1 = [x for x in w3 if x.get('priority')=='P1' and x.get('status')=='pending']
done = [x for x in w3 if x.get('status')=='completed']
print(f'TOTAL next_iteration_focus: {len(t)}')
print(f'window3 total: {len(w3)} (pending P0={len(p0)}, pending P1={len(p1)}, completed={len(done)})')
kw = [x for x in p0 if x.get('id','').startswith('kw_')]
fix = [x for x in p0 if not x.get('id','').startswith('kw_')]
print(f'\nP0 breakdown: 关键词写作={len(kw)}, 质量修复={len(fix)}')
print('\n=== P0 质量修复 ===')
for x in fix:
    print(f'  - {x.get("id","?")}: {x.get("task", x.get("title","?"))[:70]}')
print('\n=== P0 关键词写作 (by round) ===')
from collections import Counter
rounds = Counter()
for x in kw:
    rid = x.get('id','')
    r = rid.split('_')[1] if '_' in rid else 'other'
    rounds[r] += 1
for r,c in sorted(rounds.items()):
    print(f'  round{r}: {c}个')
