# -*- coding: utf-8 -*-
"""职责A：读竞品缓存 + 本地 blog 目录 → 内容缺口清单"""
import json, os, glob

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
cache = json.load(open(os.path.join(P, 'iteration_center', 'competitor_sitemap_cache.json'), encoding='utf-8'))
print('cache keys:', list(cache.keys()))
print('cached_at:', cache.get('cached_at'))
fp = cache.get('futurepedia', {})
if isinstance(fp, dict):
    cats = fp.get('categories', []) or []
    tools = fp.get('tools', []) or []
else:
    cats, tools = fp, []
print('futurepedia categories:', len(cats))
for c in sorted(cats)[:80]:
    print('  ', c)

# 本地 blog slug
blogs = set()
for f in glob.glob(os.path.join(P, 'content_drafts', '**', '*.md'), recursive=True):
    b = os.path.basename(f).lower()
    blogs.add(b)
print('\nLOCAL draft/published files:', len(blogs))
# 本地发布路径 out/blog
out_blogs = set()
for d in glob.glob(os.path.join(P, 'out', 'blog', '*')):
    if os.path.isdir(d):
        out_blogs.add(os.path.basename(d).lower())
print('out/blog slugs:', len(out_blogs))
