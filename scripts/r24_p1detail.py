# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
ids=['LEARN-20261014-01','LEARN-20261014-08','P1-ANSWER-FIRST-20261012','P1-ARTICLE-REFRESH-20261019','P1-DENSITY-REGRESSION-20261021','P1-H1-MISSING-20261012']
for t in s['next_iteration_focus']:
    if t.get('id') in ids and t.get('status')=='pending':
        print('\n###',t['id'],'|',t.get('priority'),'| assigned=',t.get('assigned_to'))
        for k in ('title','detail','task','source','evidence','detail_note','scope'):
            if k in t: print(k+':',str(t[k])[:600])
