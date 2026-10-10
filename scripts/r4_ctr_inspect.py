import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['openai_astra_review','adobe-firefly-review-2026']:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(f'{slug}: NOT FOUND'); continue
    print(f"\n=== {slug} ===")
    print(f"title ({len(p['title'])} chars): {p['title']}")
    print(f"excerpt ({len(p.get('excerpt',''))} chars): {p.get('excerpt','')}")
    # 看 content 里有没有 H1
    import re
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', p['content'])
    if h1: print(f"H1: {h1.group(1)[:100]}")
