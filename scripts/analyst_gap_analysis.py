# -*- coding: utf-8 -*-
"""职责A：futurepedia 75 分类 vs 本地 blog 覆盖 → 内容缺口"""
import json, os, glob, re

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
cache = json.load(open(os.path.join(P, 'iteration_center', 'competitor_sitemap_cache.json'), encoding='utf-8'))
fp_cats = cache['sites']['futurepedia']['categories']
print('futurepedia categories (%d):' % len(fp_cats))
for c in fp_cats:
    print('  ', c)

# 本地 blog slugs (out/blog + content_drafts)
local_slugs = set()
for d in glob.glob(os.path.join(P, 'out', 'blog', '*')):
    if os.path.isdir(d):
        local_slugs.add(os.path.basename(d).lower().replace('-', ' '))
for f in glob.glob(os.path.join(P, 'content_drafts', '**', '*.md'), recursive=True):
    b = os.path.basename(f).lower().replace('-', ' ')
    local_slugs.add(b)

def covered(cat):
    c = cat.replace('-', ' ').strip()
    for s in local_slugs:
        if c in s:
            return True
    return False

print('\n=== 内容缺口（futurepedia 有分类，本地 blog 无对应文章）===')
gaps = [c for c in fp_cats if not covered(c)]
print('gaps:', len(gaps))
for g in gaps:
    print('  GAP:', g)
