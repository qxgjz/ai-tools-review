# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
d=json.load(io.open('gsc-ga4-report/live_pull_20261022_0801.json',encoding='utf-8'))
print(type(d))
if isinstance(d,dict): print('keys',list(d.keys())[:10])
rows=d if isinstance(d,list) else d.get('rows') or d.get('data') or []
print('nrows',len(rows))
for r in rows[:3]: print(json.dumps(r,ensure_ascii=False)[:300])
