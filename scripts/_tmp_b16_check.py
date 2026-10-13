# -*- coding: utf-8 -*-
import io, json, re, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
slugs = set(p['slug'] for p in posts)
files = ['2026-10-11-claude-vs-gemini-2026-comparison_REWRITE.md',
         '2026-10-11-gemini-vs-chatgpt-2026_REWRITE.md',
         '2026-10-11-elevenlabs-v2-review-2026_REWRITE.md']
for fn in files:
    s = io.open(os.path.join(base, 'content_drafts', fn), encoding='utf-8').read()
    print('===', fn)
    print('  FAQ count:', s.count('## Frequently Asked Questions'))
    print('  H2 count:', len(re.findall(r'^## ', s, re.M)))
    imgs = re.findall(r'!\[[^\]]*\]\((/screenshots/[^)]+)\)', s)
    for im in imgs:
        exists = os.path.exists(base + r'\public' + im)
        print('  img:', im, '| exists:', exists)
    ints = re.findall(r'\]\((/blog/[\w-]+/)\)', s)
    for link in ints:
        slug = link.split('/')[-2]
        print('  int:', link, '| in posts:', slug in slugs)
    print('  has BLUF:', s.startswith('# '))
    print('  --- present:', '---' in s)
