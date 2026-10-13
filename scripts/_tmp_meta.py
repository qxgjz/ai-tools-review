# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
for p in posts:
    if p.get('slug') == 'what-is-an-ai-agent':
        print('status:', p.get('status'))
        print('meta:', json.dumps(p.get('meta'), ensure_ascii=False)[:300])
        break
# also confirm last ids used
ids = sorted(int(p['id'].rsplit('-',1)[1]) for p in posts if p.get('id') and p['id'].rsplit('-',1)[1].isdigit())
print('max id:', ids[-1], '| id count:', len(ids))
