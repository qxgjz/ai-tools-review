# -*- coding: utf-8 -*-
import json

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)
todos = data.get('next_iteration_focus', [])

print('=== 含GA4/API/凭证关键词的待办 ===')
for t in todos:
    tt = (t.get('title', '') + ' ' + t.get('description', '')).lower()
    if any(k in tt for k in ['ga4', 'api', 'credential', '凭证', 'service account']):
        print(f"  [{t.get('status')}] {t.get('id')} | {t.get('assigned_to')} | {t.get('title')}")

print()
print('=== 含LCP/性能/图片/渲染关键词的待办 ===')
for t in todos:
    tt = (t.get('title', '') + ' ' + t.get('description', '')).lower()
    if any(k in tt for k in ['lcp', 'render', 'image', 'img', 'script', '性能']):
        print(f"  [{t.get('status')}] {t.get('id')} | {t.get('assigned_to')} | {t.get('title')}")
