# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
d = json.load(io.open(base + r'\iteration_center\zensink_content_quality_report.json', encoding='utf-8'))
print('total:', d.get('total'), 'avg:', d.get('average_score'), 'fail:', d.get('fail_count'))
low = d.get('low_quality_articles') or []
# group by score
from collections import defaultdict
g = defaultdict(list)
for a in low:
    g[a.get('score')].append(a.get('slug'))
for sc in sorted(g, reverse=True):
    print('score', sc, ':', len(g[sc]), g[sc][:20])
