# -*- coding: utf-8 -*-
"""GSC 数据分析：CTR 候选(排名5-15且CTR<3%) + 关键词表现 + 趋势"""
import json, os, glob

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
lp = sorted(glob.glob(os.path.join(P, 'gsc-ga4-report', 'live_pull_*.json')), key=os.path.getmtime)
latest = json.load(open(lp[-1], encoding='utf-8'))
print('FILE:', os.path.basename(lp[-1]), '| pulled_at:', latest.get('pulled_at'))
print('daily:', latest.get('daily'))
print('query window:', latest.get('query_window_start'), '->', latest.get('query_window_end'))
print('sitemap_summary:', latest.get('sitemap_summary'))

tq = latest.get('top_queries', [])
tp = latest.get('top_pages', [])
print('\n=== top_queries (%d) ===' % len(tq))
for q in tq[:30]:
    print(q)

print('\n=== top_pages (%d) ===' % len(tp))
for p in tp[:25]:
    print(p)
