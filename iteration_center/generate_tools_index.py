# -*- coding: utf-8 -*-
"""架构师第10轮：从 tools.json 重生成精简版 tools-index.json
列表页（compare/ranking/search/category/best-for/alternatives/subcategory/首页）只读轻字段；
重字段（longDescription/verdict/useCases/keyFeatures/testingDetails 等）仅详情页用全量 tools.json。
裁剪后列表页 JS chunk 从 1.48MB 大幅减小。
"""
import json, os

BASE = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
TOOLS = os.path.join(BASE, 'data', 'tools.json')
OUT = os.path.join(BASE, 'data', 'tools-index.json')

# 列表页实际使用的字段白名单（来自 app/* 的 tool.xxx 引用扫描）
KEEP = [
    'id', 'slug', 'name', 'vendor', 'category', 'description', 'scores',
    'pros', 'cons', 'pricing', 'tags', 'hasFreeTier', 'officialUrl',
    'affiliateUrl', 'bestFor', 'subcategory', 'lastUpdated',
    'overallScore', 'grade', 'screenshot',
]

tools = json.load(open(TOOLS, encoding='utf-8'))
print('tools.json 工具数:', len(tools))

out_list = []
dropped_total = 0
for t in tools:
    slim = {k: t.get(k) for k in KEEP if k in t}
    out_list.append(slim)

old_size = os.path.getsize(OUT) if os.path.exists(OUT) else 0
json.dump(out_list, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
new_size = os.path.getsize(OUT)

# 校验：每个工具关键字段仍在
missing = [t['slug'] for t in out_list if not t.get('name') or not t.get('slug')]
print('缺失 name/slug 的工具:', len(missing))
print('旧大小: %.0fKB -> 新大小: %.0fKB (-%.0f%%)' % (old_size/1024, new_size/1024, (1-new_size/old_size)*100 if old_size else 0))
print('done')
