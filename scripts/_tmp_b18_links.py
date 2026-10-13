# -*- coding: utf-8 -*-
import io, re, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
for slug in ['lovable-vs-boltnew', 'beautiful-ai-alternatives', 'sudowrite-alternatives']:
    s = io.open(base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md', encoding='utf-8').read()
    il = re.findall(r'\[[^\]]+\]\(/blog/([^/]+)/\)', s)
    bad = [x for x in il if x not in slugs]
    imgs = re.findall(r'!\[[^\]]*\]\((/screenshots/real/webp/[^)]+)\)', s)
    ext = re.findall(r'\]\((https?://[^)]+)\)', s)
    ext = [x for x in ext if '/blog/' not in x]
    print('===', slug, '| internal:', il, '| bad:', bad, '| imgs:', imgs, '| ext:', ext)
