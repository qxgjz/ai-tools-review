# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
for slug in ['claude-vs-gemini-2026-comparison','gemini-vs-chatgpt-2026','elevenlabs-v2-review-2026']:
    for p in posts:
        if p.get('slug') == slug:
            print('===', slug)
            print(' title:', p.get('title'))
            print(' keys:', list(p.keys()))
            print(' wc:', p.get('wordCount'), '| content head:', (p.get('content') or '')[:200].replace(chr(10),' | '))
            break
    else:
        print('===', slug, 'NOT FOUND')
