# -*- coding: utf-8 -*-
import io, json, os
from PIL import Image
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
src = base + r'\content_drafts\screenshots\batch22'
dst = base + r'\public\screenshots\real\webp'
for name in ['runway-home', 'runway-pricing', 'pika-pricing', 'hailuo-home']:
    p = os.path.join(src, name + '.png')
    im = Image.open(p).convert('RGB')
    out = os.path.join(dst, name + '.webp')
    im.save(out, 'WEBP', quality=82)
    print(name + '.webp', os.path.getsize(out), 'bytes')

posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p.get('slug') for p in posts)
# new slugs created in this batch (will exist after posts.json update)
new_slugs = {'ai-video-generator-credits-burn-fast-2026', 'ai-tools-not-worth-the-money-2026'}
check = ['best-ai-video-generators-2026', 'runway-vs-pika-2026', 'best-paid-ai-tools-worth-buying-2026',
         'midjourney-alternatives-2026', 'suno-alternatives-2026', 'cursor_ai_review', 'devin-ai-review',
         'midjourney-v7-review-2026', 'elevenlabs-review-2026', 'elevenlabs-vs-playht-2026', 'cursor-vs-github-copilot-2026',
         'ai-video-generator-credits-burn-fast-2026', 'ai-tools-not-worth-the-money-2026']
for c in check:
    ok = c in slugs or c in new_slugs
    print('OK' if ok else 'MISS', c)
