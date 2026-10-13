# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
hit = next(p for p in posts if p.get('slug') == 'lovable-vs-boltnew')
for k, v in hit.items():
    if k == 'content':
        print(k, ':', str(v)[:80], '... len', len(v))
    else:
        print(k, ':', json.dumps(v, ensure_ascii=False)[:200])
