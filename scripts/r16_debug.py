import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
for t in s['next_iteration_focus']:
    if t.get('id') in ('CTR-20261017-03','CTR-20261017-04','CTR-20261017-05'):
        i = t['task'].find('article-api')
        print(t['id'])
        print(repr(t['task'][i-10:i+180]))
        print()
# title candidates
cands = [
 "Best AI Voice Changers 2026: Real-Time Tools for Streaming & Gaming",
 "Best AI Voice Changers 2026: Real-Time Voice Tools Compared",
 "Best AI Voice Changers 2026: Top Real-Time Tools Tested",
 "Best AI Voice Changers 2026: Real-Time Tools for Gamers",
]
for c in cands: print(len(c),'c',c)
