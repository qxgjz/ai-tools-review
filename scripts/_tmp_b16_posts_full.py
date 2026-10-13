# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
for slug in ['claude-vs-gemini-2026-comparison','gemini-vs-chatgpt-2026','elevenlabs-v2-review-2026']:
    for p in posts:
        if p.get('slug') == slug:
            print('===', slug)
            print(json.dumps({k: (v[:300] if isinstance(v, str) and len(v) > 300 else v) for k, v in p.items()}, ensure_ascii=False, indent=1)[:2500])
            print()
