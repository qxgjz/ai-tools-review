import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
SLUGS = ['openai_astra_review','adobe-firefly-review-2026']
creatium = [p for p in posts if 'creatium' in p['slug'].lower()]
print('creatium matches:', [p['slug'] for p in creatium])
if creatium: SLUGS.append(creatium[0]['slug'])

for slug in SLUGS:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(f'{slug}: NOT FOUND'); continue
    print(f"\n=== {slug} ===")
    print(f"title ({len(p['title'])}c): {p['title']}")
    print(f"meta ({len(p.get('excerpt',''))}c): {p.get('excerpt','')}")
