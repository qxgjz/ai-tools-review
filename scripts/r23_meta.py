# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
slugs=['dify_ai_review','stable-diffusion-review-2026','cursor_ai_review','gemini_38_flash_review',
'adobe-firefly-review-2026','ai-coding-tools-comparison-2026','best-ai-voice-changers-2026']
by={p['slug']:p for p in posts}
for s in slugs:
    p=by.get(s)
    if not p:
        # fuzzy
        cand=[x['slug'] for x in posts if s.replace('-','').replace('_','') in x['slug'].replace('-','').replace('_','')]
        print('MISSING',s,'candidates=',cand[:5]);continue
    t=p.get('title','');e=p.get('excerpt') or p.get('description','')
    print(f"\n### {s}\nT[{len(t)}] {t}\nE[{len(e)}] {e}")
