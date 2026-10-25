# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
by['best-ai-meeting-assistants-2026']['title']='Best AI Meeting Assistants 2026: 12 Tested, 5 Worth It'
by['best-ai-productivity-tools-2026']['title']='Best AI Productivity Tools 2026: 15 We Use Every Day'
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
for sl in ['best-ai-meeting-assistants-2026','best-ai-productivity-tools-2026']:
    print(sl,len(by[sl]['title']))
