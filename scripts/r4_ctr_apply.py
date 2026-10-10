import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

NEW_META = {
    'openai_astra_review': {
        'title': 'OpenAI Astra Review 2026: 40 Coding Tasks, Worth $200/mo?',
        'excerpt': 'We tested OpenAI Astra on 40 real coding tasks over 2 weeks. See if it beats Cursor for full-repo refactors — and when $200/mo is worth it.'
    },
    'adobe-firefly-review-2026': {
        'title': 'Adobe Firefly Review 2026: 40+ Photos Edited, Honest Rating',
        'excerpt': 'We edited 40+ photos in Adobe Firefly over 30 days. See our 7.8/10 rating, pricing breakdown, and how it compares to Midjourney in 2026.'
    },
}

for slug, meta in NEW_META.items():
    p = next(x for x in posts if x['slug']==slug)
    old_t, old_e = p['title'], p.get('excerpt','')
    p['title'] = meta['title']
    p['excerpt'] = meta['excerpt']
    print(f"{slug}:")
    print(f"  title: {len(old_t)}->{len(meta['title'])}  {old_t[:50]!r} -> {meta['title']!r}")
    print(f"  meta:  {len(old_e)}->{len(meta['excerpt'])} chars")
    # Verify CTR rules
    assert 50 <= len(meta['title']) <= 60, f"title {len(meta['title'])} not in 50-60"
    assert 120 <= len(meta['excerpt']) <= 155, f"meta {len(meta['excerpt'])} not in 120-155"
    print(f"  ✅ CTR standard met")

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
