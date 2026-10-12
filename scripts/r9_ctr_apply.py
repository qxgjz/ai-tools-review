import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

NEW = {
    'gemini_38_flash_review': {
        'title': 'Gemini 3.8 Flash Review 2026: Speed, Price & Verdict',
        'excerpt': 'We tested Gemini 3.8 Flash for 2 weeks. Speed, pricing, and honest verdict on whether it beats GPT-4o Mini for your dev stack.'
    },
    'cursor_ai_review': {
        'title': 'Cursor AI Review 2026: Is the $20/mo Plan Worth It?',
        'excerpt': 'Cursor AI review after 3 months of real use. Is the $20/mo Pro plan worth it vs GitHub Copilot? Honest pros, cons, and verdict inside.'
    },
    'stable-diffusion-review-2026': {
        'title': 'Stable Diffusion Review 2026: Best Models & Free Setup',
        'excerpt': 'Complete 2026 Stable Diffusion review: best models (SDXL, SD 3.5), Automatic1111 setup, ComfyUI workflows, and free cloud alternatives.'
    },
    'dify_ai_review': {
        'title': 'Dify AI Review 2026: Best Open-Source AI App Builder?',
        'excerpt': 'Dify AI review: pricing, features, pros/cons, and how it compares to Coze and LangChain. Is it the best open-source LLMOps in 2026?'
    },
    'suno-review-2026': {
        'title': 'Suno AI Review 2026: Is the $10/mo Pro Plan Worth It?',
        'excerpt': 'Suno AI review after 2 weeks of real use. Is the $10/mo Pro plan worth it? Pricing, features, pros/cons, and how it compares to Udio.'
    },
}

for slug, meta in NEW.items():
    p = next(x for x in posts if x['slug']==slug)
    p['title'] = meta['title']
    p['excerpt'] = meta['excerpt']
    tlen = len(meta['title']); mlen = len(meta['excerpt'])
    ok = (50 <= tlen <= 60) and (120 <= mlen <= 155)
    print(f"{slug}: title={tlen}c meta={mlen}c {'✅' if ok else '❌'}")
    if not ok:
        print(f"  title: {meta['title']}")
        print(f"  meta:  {meta['excerpt']}")

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
