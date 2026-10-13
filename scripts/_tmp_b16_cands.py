# -*- coding: utf-8 -*-
import io, json, glob, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
print('posts total:', len(posts))
# check candidate slugs
cands = ['best-ai-comparison-tools-2026','suno-alternatives-2026','best-ai-video-generators-2026',
         'midjourney-alternatives-2026','perplexity-ai-review-2026','best-ai-image-generators-2026',
         'best-ai-tools-for-beginners-2026','agenta-ai-review-2026','cursor-vs-windsurf-2026',
         'what-is-an-ai-agent','best-ai-agents-2026']
for c in cands:
    print(c, '->', 'EXISTS' if c in slugs else 'FREE')
# find zensink report
for f in glob.glob(base + r'\iteration_center\zensink*.json') + glob.glob(base + r'\*.json'):
    if 'zensink' in f.lower() or 'zens' in f.lower():
        print('report candidate:', f)
