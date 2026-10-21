# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
for t in s['next_iteration_focus']:
    if t.get('id','').startswith(('P1-READABILITY-SENTENCE','P1-SCAN-FORMAT','P1-LLM-ANSWER')):
        print('OK',t['id'],t['priority'],t['assigned_to'],t['status'])
p=r'C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md'
txt=io.open(p,encoding='utf-8').read()
print('learning tail marker present:', '2026-10-22 可读性' in txt, '| points=', txt.count('| ')>=0)
print('last 120 chars:',repr(txt[-120:]))
