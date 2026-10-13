# -*- coding: utf-8 -*-
import io, re, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
valid = set(p['slug'] for p in posts)
files = ['2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md',
         '2026-10-10-agenta-ai-review-2026_DRAFT.md',
         '2026-10-10-cursor-vs-windsurf-2026_REWRITE.md']
for fn in files:
    s = io.open(base + r'\content_drafts\\' + fn, encoding='utf-8').read()
    ints = re.findall(r'\[[^\]]*\]\((/blog/[^)]+)\)', s)
    bad = []
    for l in ints:
        slug = l.rstrip('/').split('/')[-1]
        if slug not in valid:
            bad.append((slug, l))
    print(fn, '| int count:', len(ints), '| bad:', bad if bad else 'NONE')
