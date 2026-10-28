# -*- coding: utf-8 -*-
"""r37 CTR 分析 + GSC Easy Wins"""
import json
P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
d = json.load(open(P + r'\gsc-ga4-report\live_pull_20261024_0939.json', encoding='utf-8'))
print('=== QUERIES (pos 5-20, ctr<3%) ===')
for q in d['top_queries']:
    k = q['keys'][0]; pos = q['position']; ctr = q['ctr']; imp = q['impressions']
    if 5 <= pos <= 20 and ctr < 3:
        print(f'{k} | pos {pos} | imp {imp} | ctr {ctr}%')
print('=== PAGES (pos 5-20, ctr<3%) ===')
for p in d['top_pages']:
    k = p['keys'][0]; pos = p['position']; ctr = p['ctr']; imp = p['impressions']
    if 5 <= pos <= 20 and ctr < 3:
        print(f'{k} | pos {pos} | imp {imp} | ctr {ctr}%')
print('=== ALL pages w/ keys (pos 1-20) ===')
for p in sorted(d['top_pages'], key=lambda x: x['position']):
    if p['position'] <= 20:
        print(f"{p['keys'][0]} | pos {p['position']} | imp {p['impressions']} | ctr {p['ctr']}%")
print('=== ALL queries w/ keys ===')
for q in d['top_queries']:
    print(f"{q['keys'][0]} | pos {q['position']} | imp {q['impressions']} | ctr {q['ctr']}%")
