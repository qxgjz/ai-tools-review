import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
p = next(x for x in posts if x['slug']=='ai-tools-comparison-2026')
for k in ['title','excerpt','metaDescription','metaTitle','description']:
    v = p.get(k)
    if v:
        print(f"{k} ({len(v)}c): {v}")
print("\n--- all keys ---")
print(list(p.keys()))
