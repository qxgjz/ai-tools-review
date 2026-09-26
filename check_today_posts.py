import json

posts = json.load(open('data/posts.json', 'r', encoding='utf-8'))
today = [p for p in posts if p.get('date', '').startswith('2026-09-16')]
print(f'今天(9月16日)发布的文章: {len(today)}篇')
for p in today[:20]:
    print(f'  - {p["slug"]}')
