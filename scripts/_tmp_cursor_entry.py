# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
for p in posts:
    if p.get('slug') == 'cursor-vs-windsurf-2026':
        print(json.dumps(p, ensure_ascii=False, indent=1)[:1500])
        break
