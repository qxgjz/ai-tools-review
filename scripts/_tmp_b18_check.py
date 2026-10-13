# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
for slug in ['lovable-vs-boltnew','beautiful-ai-alternatives','sudowrite-alternatives']:
    hit = next((p for p in posts if p.get('slug') == slug), None)
    if hit:
        c = hit.get('content') or ''
        print('===', slug, '| title:', hit.get('title'))
        print('  len:', len(c), '| keys:', list(hit.keys())[:14])
    else:
        print('===', slug, 'NOT FOUND')
print()
for c in ['cursor-vs-windsurf-2026','best-ai-coding-tools-beginners','best-ai-agents-2026','what-is-an-ai-agent','best-ai-tools-for-beginners-2026','ai-agent-vs-chatbot-2026','best-ai-image-generators-2026','midjourney-v7-review-2026','quillbot-alternatives','chatgpt-vs-claude-2026-comparison','best-ai-video-generators-2026','best-ai-voice-changers-content-creators','suno-alternatives','claude-vs-gemini-2026-comparison']:
    print(c, '->', 'EXISTS' if c in slugs else 'FREE')
