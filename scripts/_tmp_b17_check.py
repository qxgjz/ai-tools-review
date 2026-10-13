# -*- coding: utf-8 -*-
import io, json, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
for slug in ['cursor_ai_review','midjourney-v7-review-2026','suno-alternatives','openai_astra_review','lovable-vs-boltnew']:
    hit = None
    for p in posts:
        if p.get('slug') == slug:
            hit = p
            break
    if hit:
        c = hit.get('content') or ''
        print('===', slug, '| title:', hit.get('title'))
        print('  keys:', list(hit.keys())[:16])
        print('  content head:', c[:150].replace('\n',' | '), '| len:', len(c))
    else:
        print('===', slug, 'NOT FOUND')
print()
webp_dir = base + r'\public\screenshots\real\webp'
for w in ['cursor-pricing.webp','cursor-homepage.webp','cursor-code-editor.webp','midjourney-pricing.webp','midjourney-gallery.webp','midjourney-docs-sample.webp','suno-music-creator.webp','suno.webp']:
    print(w, '->', os.path.exists(os.path.join(webp_dir, w)))
