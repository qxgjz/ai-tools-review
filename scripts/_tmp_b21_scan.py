# -*- coding: utf-8 -*-
import io, json, re, subprocess, sys, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
already_rewritten = ['claude-vs-gemini-2026-comparison','gemini-vs-chatgpt-2026','elevenlabs-v2-review-2026','cursor_ai_review','midjourney-v7-review-2026','suno-alternatives','lovable-vs-boltnew','beautiful-ai-alternatives','sudowrite-alternatives','clearscope-alternatives','gemini_38_flash_review','dify-vs-langchain-2026','suno-review-2026','elevenlabs-review-2026','dify_ai_review','synthesia-vs-heygen','motion-ai-alternatives','quillbot-alternatives','runway-alternatives','writesonic-alternatives','otter-ai-alternatives','chatgpt-vs-claude-2026-comparison','claude-37-vs-gpt4o','midjourney-v7-vs-flux-2026']
cands = []
for p in posts:
    slug = p.get('slug', '')
    wc = p.get('wordCount') or 0
    if wc and wc < 2000 and slug not in already_rewritten:
        cands.append((slug, wc, (p.get('title') or '')[:70]))
cands.sort(key=lambda x: x[1])
print('low wordCount candidates (<2000, not yet rewritten):', len(cands))
for c in cands[:40]:
    print(c)
