# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
by['best-ai-coding-tools-2026']['title']='Best AI Coding Tools 2026: Cursor vs Copilot, Tested'
by['best-ai-coding-tools-2026']['excerpt']='We tested 8 AI coding assistants for 30 days. Cursor wins for AI-native dev, Copilot for VS Code users, Windsurf for refactoring. See rankings now.'
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
p=by['best-ai-coding-tools-2026']
print(len(p['title']),len(p['excerpt']))
