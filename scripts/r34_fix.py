# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
D={
'best-ai-meeting-assistants-2026':('Best AI Meeting Assistants 2026: 12 Tested, 5 Win',
 'We tested 12 AI meeting assistants on transcription accuracy, summaries and pricing. See which 5 are worth it in 2026, from Fireflies to Otter.'),
'best-ai-productivity-tools-2026':('Best AI Productivity Tools 2026: 15 We Use Daily',
 'We tested 15 AI productivity tools on Notion, Copilot, Gemini and more. See which 10 actually save hours each week, with pricing and winners.'),
'best-ai-observability-tools-2026':('Best AI Observability Tools 2026: 10 Tested & Ranked',
 'We tested 10 LLM observability tools on tracing, evals and pricing. See rankings, free tiers and enterprise options to monitor your AI apps.'),
'ai-coding-tools-comparison-2026':('AI Coding Tools Comparison 2026: Copilot vs Cursor Wins?',
 'We benchmarked Copilot, Cursor and Tabnine on 50 real coding tasks in 2026. See pricing, setup, and which AI assistant fits your stack.'),
}
for sl,(t,e) in D.items():
    p=by[sl]; p['title']=t; p['excerpt']=e
    print(sl,'|',len(t),len(e))
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
