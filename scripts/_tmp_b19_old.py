# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
for slug in ['clearscope-alternatives','gemini_38_flash_review','dify-vs-langchain-2026']:
    hit = next(p for p in posts if p.get('slug') == slug)
    c = hit.get('content') or ''
    print('=====', slug, '| len:', len(c))
    print(c[:500].replace('\n', ' | '))
    print()
