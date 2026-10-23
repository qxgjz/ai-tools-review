# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
d=json.load(io.open('gsc-ga4-report/live_pull_20261022_0801.json',encoding='utf-8'))
tp=d['top_pages']
print('n=',len(tp)); print(json.dumps(tp[0],ensure_ascii=False,indent=2))
