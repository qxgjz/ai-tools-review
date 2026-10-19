import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
for t in s['next_iteration_focus']:
    if t.get('id') in ('P0-CMD-POLISH-FAKE-FIX-20261019','P1-ARTICLE-REFRESH-20261019'):
        print('=====',t.get('id'))
        print(json.dumps(t,ensure_ascii=False,indent=2))
