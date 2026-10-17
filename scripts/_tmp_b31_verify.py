# -*- coding: utf-8 -*-
"""batch31 verify: internal links exist in posts.json, screenshots exist, FAQ count, outbound links"""
import io, json, os, re

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(os.path.join(base, 'data', 'posts.json'), encoding='utf-8'))
slugs = set(p['slug'] for p in posts)

files = ['2026-10-17-ai-tools-hallucinate-least-2026_NEW.md',
         '2026-10-17-ai-writing-tools-match-your-voice-2026_NEW.md',
         '2026-10-17-ai-tools-generous-rate-limits-2026_NEW.md']
for fn in files:
    s = io.open(os.path.join(base, 'content_drafts', fn), encoding='utf-8').read()
    il = re.findall(r'\]\((/blog/([^)]+)/)\)', s)
    ol = re.findall(r'\]\((https?://[^)]+)\)', s)
    imgs = re.findall(r'!\[[^\]]*\]\((/screenshots/[^)]+)\)', s)
    faq = len(re.findall(r'^\*\*[^*]+\?\*\*', s, flags=re.M))
    missing = [sl for _, sl in il if sl not in slugs]
    img_missing = [p for p in imgs if not os.path.exists(os.path.join(base, 'public', p.lstrip('/')))]
    print(fn.split('-')[3])
    print('  internal links:', len(il), '| missing slugs:', missing)
    print('  outbound links:', len(ol), '| urls:', ol[:4])
    print('  screenshots:', imgs, '| missing files:', img_missing)
    print('  FAQ count:', faq)
