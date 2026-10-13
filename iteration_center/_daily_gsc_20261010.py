# -*- coding: utf-8 -*-
"""读取最新GSC报告关键数据"""
import json, os

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
gsc_dir = os.path.join(base, 'gsc-ga4-report')
files = [f for f in os.listdir(gsc_dir) if f.startswith('live_pull') and f.endswith('.json')]
files.sort()
if not files:
    print('无GSC报告')
    exit()

g = json.load(open(os.path.join(gsc_dir, files[-1]), encoding='utf-8'))
print('报告:', files[-1])
print('site:', g.get('site'))
print('窗口:', g.get('query_window_start'), '→', g.get('query_window_end'))

daily = g.get('daily', [])
tot_imp = sum(int(d.get('impressions', 0)) for d in daily)
tot_clk = sum(int(d.get('clicks', 0)) for d in daily)
print('累计曝光:', tot_imp, '点击:', tot_clk)
for d in daily[-7:]:
    print(' ', d)

print()
print('Top queries:')
for q in (g.get('top_queries') or [])[:10]:
    print(' ', q)
print()
print('Top pages:')
for pg in (g.get('top_pages') or [])[:10]:
    print(' ', pg)
