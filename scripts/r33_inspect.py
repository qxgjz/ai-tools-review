# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
for sl in ['dify_ai_review','stable-diffusion-review-2026','cursor_ai_review','gemini_38_flash_review','openai_astra_review','creatium-coach-review-2025','midjourney-v7','ai-coding-tools-comparison-2026']:
    p=by.get(sl)
    if p: print(sl,'| t',len(p['title']),repr(p['title']),'| e',len(p.get('excerpt') or ''),repr((p.get('excerpt') or '')[:150]))
    else: print(sl,'NO')
# find midjourney v7
print('\nmidjourney v7 slugs:')
for p in posts:
    if 'midjourney' in p['slug'] and ('v7' in p['slug'] or '7' in p['slug']): print(' ',p['slug'],len(p['title']),p['title'][:60])
