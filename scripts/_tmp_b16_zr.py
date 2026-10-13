# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
d = json.load(io.open(base + r'\iteration_center\zensink_content_quality_report.json', encoding='utf-8'))
print('type:', type(d))
items = d if isinstance(d, list) else d.get('articles') or d.get('results') or []
print('items:', len(items) if hasattr(items,'__len__') else '?')
if isinstance(d, dict):
    print('keys:', list(d.keys())[:10])
for it in (items if isinstance(items, list) else [])[:60]:
    if isinstance(it, dict):
        print(it.get('slug') or it.get('file') or it.get('title'), '| score:', it.get('score') or it.get('zens_ink_score') or it.get('content_qc'))
