# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
for c in ['cursor-vs-windsurf-2026','best-ai-coding-tools-beginners','best-ai-tools-for-beginners-2026','what-is-an-ai-agent','best-ai-agents-2026','ai-agent-vs-chatbot-2026','midjourney-v7-vs-flux-2026','best-ai-image-generators-2026','midjourney-v7-vs-dall-e-3-2026','suno-vs-udio','best-ai-video-generators-2026','best-ai-voice-changers-content-creators']:
    print(c, '->', 'EXISTS' if c in slugs else 'FREE')
