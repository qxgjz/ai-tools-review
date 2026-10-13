# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
print('total posts:', len(posts))
slugs = [p.get('slug') for p in posts]
cands = ['runway-vs-pika-2026', 'claude-alternatives-2026', 'elevenlabs-vs-playht-2026',
         'cursor-vs-github-copilot-2026', 'midjourney-alternatives-2026', 'suno-alternatives-2026',
         'chatgpt-alternatives-2026', 'best-paid-ai-tools-worth-buying-2026', 'notion-ai-vs-salesforce-2026',
         'jasper-ai-alternative-2026', 'midjourney-v7-vs-dall-e-3-2026', 'how-to-get-chatgpt-free-2026']
for c in cands:
    p = next((x for x in posts if x.get('slug') == c), None)
    if p:
        wc = p.get('wordCount', '?')
        has_qa = 'Quick Answer' in (p.get('content') or '')[:2000]
        print(c, '| wordCount:', wc, '| date:', p.get('date'), '| quickAnswer:', has_qa)
    else:
        print(c, '| NOT IN POSTS')
