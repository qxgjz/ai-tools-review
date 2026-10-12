import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

NEW = {
    'openai_astra_review': {
        'title': 'OpenAI Astra Review: 40 Coding Tasks, Pros, Cons & Verdict',
        'excerpt': 'OpenAI Astra review with 40 real coding tasks tested. See pros, cons, pricing, and how it compares to Cursor — before you pay $200/mo.'
    },
    'adobe-firefly-review-2026': {
        'title': 'Adobe Firefly Review 2026: Pricing, Pros, Cons & Options',
        'excerpt': 'Adobe Firefly review: pricing, pros/cons, commercial use license, and how it compares to Midjourney. Find out if it\'s worth it in 2026.'
    },
    'creatium-coach-review-2025': {
        'title': 'Creatium Coach Review 2026: Pricing & Honest Verdict',
        'excerpt': 'Creatium Coach review: pricing, features, pros/cons, and who should buy it. Is this AI content coach worth the $99/mo asking price?'
    },
}

for slug, meta in NEW.items():
    p = next(x for x in posts if x['slug']==slug)
    p['title'] = meta['title']
    p['excerpt'] = meta['excerpt']
    print(f"{slug}: title={len(meta['title'])}c, meta={len(meta['excerpt'])}c")
    assert 50 <= len(meta['title']) <= 60
    assert 120 <= len(meta['excerpt']) <= 155
    print(f"  ✅ {meta['title']}")

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
