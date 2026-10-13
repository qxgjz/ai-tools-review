# -*- coding: utf-8 -*-
import io, json, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
print('total posts:', len(posts))
for slug in ['clearscope-alternatives','gemini_38_flash_review','dify-vs-langchain-2026']:
    hit = next((p for p in posts if p.get('slug') == slug), None)
    print('===', slug, '| title:', hit.get('title') if hit else 'NOT FOUND')
print()
for c in ['best-ai-agents-2026','what-is-an-ai-agent','ai-agent-vs-chatbot-2026','how-to-build-an-ai-agent','best-ai-tools-for-beginners-2026','best-ai-coding-tools-beginners','cursor-vs-windsurf-2026','cursor_ai_review','claude-vs-gemini-2026-comparison','chatgpt-vs-claude-2026-comparison','best-ai-video-generators-2026','suno-alternatives','midjourney-v7-review-2026','best-ai-image-generators-2026','gemini-vs-chatgpt-2026','quillbot-alternatives','otter-ai-alternatives','motion-ai-alternatives','runway-alternatives','synthesia-vs-heygen','writesonic-alternatives','lovable-vs-boltnew','beautiful-ai-alternatives','sudowrite-alternatives','agenta-ai-review-2026']:
    print(c, '->', 'EXISTS' if c in slugs else 'FREE')
