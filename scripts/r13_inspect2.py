import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['adobe-firefly-review-2026','creatium-coach-review-2025','elevenlabs-review-2026']:
    p = next((x for x in posts if x['slug']==slug), None)
    if p:
        print(f"=== {slug} ===")
        print(f"  title: {p.get('title','')} ({len(p.get('title',''))}c)")
        print(f"  excerpt: {p.get('excerpt','')[:160]} ({len(p.get('excerpt',''))}c)")
        print(f"  metaDescription: {p.get('metaDescription','')[:160]} ({len(p.get('metaDescription',''))}c)")
        print()
