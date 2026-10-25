# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
D={
'dify_ai_review':('Dify AI Review 2026: Build AI Apps Without Coding?',
 'We built 3 real LLM apps in Dify. See pricing, limits, and how it stacks up vs Coze and LangChain before you commit.'),
'stable-diffusion-review-2026':('Stable Diffusion Review 2026: Free, Fast & Fully Yours?',
 'No GPU? We set up SD in 20 minutes. Compare SDXL vs SD 3.5, free cloud tools, and who should skip it.'),
'cursor_ai_review':('Cursor AI Review 2026: I Switched From Copilot (Here\'s Why)',
 'After 90 days coding in Cursor, is the $20 Pro plan worth it vs Copilot? Honest bugs, speed, and verdict inside.'),
'gemini_38_flash_review':('Gemini 3.8 Flash Review 2026: Cheaper, Faster, Enough?',
 'We ran 50 prompts on Gemini 3.8 Flash vs GPT-4o Mini. See price, latency, and when it beats paid models.'),
'openai_astra_review':('OpenAI Astra Review 2026: Is $200/mo Worth It for Coding?',
 'We tested OpenAI Astra on 40 real coding tasks vs Cursor. See pros, cons, pricing, and who should buy.'),
'creatium-coach-review-2025':('Creatium Coach Review 2026: $99/mo AI Coach, Tested',
 'We used Creatium Coach for 2 weeks. See features, pricing, honest pros and cons, and who should buy it.'),
'midjourney-v7-review-2026':('Midjourney v7 Review 2026: Best MJ Yet? Tested',
 'Midjourney v7 is more artistic. We ran 30 prompts on logos, photos and art. See pros, limits, and pricing.'),
}
ch=[]
for sl,(t,e) in D.items():
    p=by.get(sl)
    if p: p['title']=t; p['excerpt']=e; ch.append((sl,len(t),len(e)))
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
for c in ch: print(c)
