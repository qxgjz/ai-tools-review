import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

NEW = {
    'openai_astra_review': {
        'title': 'OpenAI Astra Review 2026: 40 Tasks, Is $200/mo Worth It?',
        'excerpt': "We ran OpenAI Astra on 40 real coding tasks for 2 weeks. Here's the honest verdict — where it beats Cursor, and who should skip it."
    },
    'adobe-firefly-review-2026': {
        'title': "Adobe Firefly Review: I Edited 40+ Photos, Here's the Truth",
        'excerpt': "I edited 40+ photos in Adobe Firefly for 30 days. Is it worth it for commercial work? Pricing, pros/cons, and Midjourney comparison inside."
    },
    'creatium-coach-review-2025': {
        'title': 'Creatium Coach Review: Is This AI Coach Worth $99/mo?',
        'excerpt': "I used Creatium Coach for 2 weeks on real business writing tasks. Honest review of features, pricing, pros/cons, and who should skip it."
    },
}

for slug, meta in NEW.items():
    p = next(x for x in posts if x['slug']==slug)
    ot, oe = p['title'], p.get('excerpt','')
    p['title'] = meta['title']
    p['excerpt'] = meta['excerpt']
    print(f"{slug}:")
    print(f"  title: {len(ot)}->{len(meta['title'])}  {meta['title']}")
    print(f"  meta:  {len(oe)}->{len(meta['excerpt'])}")
    assert 50 <= len(meta['title']) <= 60, f"title {len(meta['title'])} out of range"
    assert 120 <= len(meta['excerpt']) <= 155, f"meta {len(meta['excerpt'])} out of range"
    print(f"  ✅ CTR standard met")

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
