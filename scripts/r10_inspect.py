import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
SLUGS = [
    'adobe-firefly-review-2026',
    'creatium-coach-review-2025',
    'openai_astra_review',
    'best-ai-voice-changers-2026',
    'elevenlabs-review-2026',
]
for slug in SLUGS:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(f'{slug}: NOT FOUND'); continue
    print(f'\n=== {slug} ===')
    print(f'title ({len(p["title"])}c): {p["title"]}')
    print(f'meta ({len(p.get("excerpt",""))}c): {p.get("excerpt","")[:200]}')
