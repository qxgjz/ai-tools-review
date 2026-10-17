import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['cursor-vs-github-copilot-2026','dall-e-3-review-2026','figma-ai-review-2026']:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(slug, "NOT FOUND"); continue
    ex = p.get('excerpt','')
    c = p.get('content','')
    print(f"=== {slug} ===")
    print(f"  excerpt {len(ex)}c: {ex[:120]}")
    print(f"  content {len(c)}c, starts: {c[:150]}")
    print()
