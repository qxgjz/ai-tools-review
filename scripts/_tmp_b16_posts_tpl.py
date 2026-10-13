# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
for slug in ['midjourney-v7-vs-flux-2026','cursor-vs-windsurf-2026']:
    for p in posts:
        if p.get('slug') == slug:
            print('===', slug)
            print('title:', p.get('title'))
            print('keys:', list(p.keys()))
            c = p.get('content') or ''
            print('content head 300:', c[:300].replace('\n', ' | '))
            print('content len:', len(c))
            print()
