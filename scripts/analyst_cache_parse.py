# -*- coding: utf-8 -*-
"""职责A：解析 competitor_sitemap_cache.json (sites 结构) + 本地内容 → 缺口"""
import json, os, glob

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
cache = json.load(open(os.path.join(P, 'iteration_center', 'competitor_sitemap_cache.json'), encoding='utf-8'))
print('cached_at:', cache.get('cached_at'))
sites = cache.get('sites', {})
print('sites:', list(sites.keys()))
for name, info in sites.items():
    if isinstance(info, dict):
        print('---', name, '| keys:', list(info.keys())[:10])
        cats = info.get('categories', info.get('ai_tools', []))
        tools = info.get('tools', [])
        print('   categories:', len(cats) if isinstance(cats, (list, dict)) else cats)
        if isinstance(cats, list) and cats:
            print('   first 15:', cats[:15])
        if isinstance(cats, dict):
            ks = list(cats.keys())
            print('   cat keys first 15:', ks[:15])
    else:
        print('---', name, '| type:', type(info), '| len:', len(info) if hasattr(info,'__len__') else '')
        if isinstance(info, list) and info:
            print('   first 10:', info[:10])
