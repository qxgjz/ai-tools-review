# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
print('total posts:', len(posts))
for slug in ['suno-review-2026', 'elevenlabs-review-2026', 'dify_ai_review']:
    hit = next((p for p in posts if p.get('slug') == slug), None)
    if hit:
        c = hit.get('content') or ''
        print('===', slug, '| title:', hit.get('title'), '| len:', len(c))
        print(c[:300].replace('\n', ' | '))
    else:
        print('===', slug, 'NOT FOUND')
print()
cands = ['suno-alternatives','suno-alternatives-2026','midjourney-v7-review-2026','best-ai-video-generators-2026','best-ai-tools-for-beginners-2026','elevenlabs-v2-review-2026','elevenlabs-vs-playht-2026','best-ai-voice-changers-content-creators','motion-ai-alternatives','synthesia-vs-heygen','dify-vs-langchain-2026','dify-vs-coze-2026-comparison','what-is-an-ai-agent','how-to-build-an-ai-agent','best-ai-agents-2026','ai-agent-vs-chatbot-2026','agenta-ai-review-2026','best-ai-coding-tools-beginners','claude-vs-gemini-2026-comparison','gemini-vs-chatgpt-2026','chatgpt-vs-claude-2026-comparison','cursor-vs-windsurf-2026','cursor_ai_review','best-ai-grammar-checker','quillbot-alternatives','notion-ai-vs-obsidian-2026','runway-alternatives','otter-ai-alternatives','writesonic-alternatives','lovable-vs-boltnew','beautiful-ai-alternatives','sudowrite-alternatives','perplexity-vs-chatgpt-2026','claude-alternatives-2026','chatgpt-alternatives-2026']
for c in cands:
    print(c, '->', 'EXISTS' if c in slugs else 'FREE')
