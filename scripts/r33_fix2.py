# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
D={
'dify_ai_review':('Dify AI Review 2026: Build AI Apps Without Coding?',
 'We built 3 real LLM apps in Dify over a week. See pricing, real limits, and how it stacks up vs Coze and LangChain before you commit.'),
'stable-diffusion-review-2026':('Stable Diffusion Review 2026: Free, Fast & Fully Yours?',
 'No GPU at home? We set up Stable Diffusion in 20 minutes. Compare SDXL vs SD 3.5, free cloud tools, and who should skip it.'),
'cursor_ai_review':('Cursor AI Review 2026: I Switched From Copilot (Here\'s Why)',
 'After 90 days coding full-time in Cursor, is the $20 Pro plan worth it vs GitHub Copilot? Honest bugs, speed, and verdict inside.'),
'gemini_38_flash_review':('Gemini 3.8 Flash Review 2026: Cheaper, Faster, Enough?',
 'We ran 50 side-by-side prompts on Gemini 3.8 Flash vs GPT-4o Mini. See real price, latency, and when it beats paid models.'),
'openai_astra_review':('OpenAI Astra Review 2026: Is $200/mo Worth It for Coding?',
 'We tested OpenAI Astra on 40 real coding tasks and compared it against Cursor. See pros, cons, pricing, and who should buy it.'),
'creatium-coach-review-2025':('Creatium Coach Review 2026: Is $99/mo AI Coach Worth It?',
 'We used Creatium Coach for two full weeks. See features, pricing, honest pros and cons, and exactly who should buy this tool.'),
'midjourney-v7-review-2026':('Midjourney v7 Review 2026: Is It the Best MJ Yet? Tested',
 'Midjourney v7 leans more artistic. We ran 30 test prompts on logos, product photos and art. See pros, limits, and pricing details.'),
}
for sl,(t,e) in D.items():
    p=by[sl]; p['title']=t; p['excerpt']=e
    print(sl,'|',len(t),len(e))
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
