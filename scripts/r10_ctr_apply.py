import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

NEW = {
    'adobe-firefly-review-2026': {
        'title': 'Adobe Firefly Review 2026: Is It Worth the Free Tier?',
        'excerpt': 'We tested Adobe Firefly for 2 weeks. Is the free tier worth it vs Midjourney? Pricing, commercial license, pros/cons, and honest verdict.'
    },
    'creatium-coach-review-2025': {
        'title': 'Creatium Coach Review 2026: Is the $99/mo Plan Worth It?',
        'excerpt': 'Is Creatium Coach worth $99/mo? We tested it for 2 weeks: features, pricing, pros/cons, and who should buy this AI content coach.'
    },
    'openai_astra_review': {
        'title': 'OpenAI Astra Review 2026: 40 Tasks, Is $200/mo Worth It?',
        'excerpt': 'We tested OpenAI Astra on 40 real coding tasks. Is the $200/mo plan worth it vs Cursor? Honest pros, cons, pricing, and verdict.'
    },
    'best-ai-voice-changers-2026': {
        'title': 'Best AI Voice Changers 2026: We Tested 7 for 10 Days',
        'excerpt': 'We tested 7 AI voice changers over 10 days. Voicemod wins real-time, ElevenLabs wins quality. See which fits your Discord, podcast, or videos.'
    },
    'elevenlabs-review-2026': {
        'title': 'ElevenLabs Review 2026: Best AI Voice Generator & Cloning?',
        'excerpt': 'ElevenLabs review after 2 weeks: is the $5 Starter plan worth it? Pricing, voice quality, cloning, and how it compares to PlayHT.'
    },
}

for slug, meta in NEW.items():
    p = next(x for x in posts if x['slug']==slug)
    p['title'] = meta['title']
    p['excerpt'] = meta['excerpt']
    tlen = len(meta['title']); mlen = len(meta['excerpt'])
    ok = (50 <= tlen <= 60) and (120 <= mlen <= 155)
    print(f"{slug}: title={tlen}c meta={mlen}c {'OK' if ok else 'FAIL'}")
    if not ok:
        print(f"  title: {meta['title']}")
        print(f"  meta:  {meta['excerpt']}")

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
