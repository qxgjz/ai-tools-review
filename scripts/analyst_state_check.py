# -*- coding: utf-8 -*-
"""检查 state.json 现状：上轮产出是否在位、各系列待办计数"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
d = json.load(open(SP, encoding='utf-8'))
nf = d.get('next_iteration_focus', [])
print('focus:', len(nf), '| last_update:', d.get('last_update'))
print('last_commit:', d.get('last_commit'))
print('current_iteration:', d.get('current_iteration'))

# 上轮产出系列
series = {
    'CTR-20261025': ('CTR-BLOG-OPENAI-ASTRA-20261025', 'CTR-QUERY-CODING-COMPARISON-20261025', 'CTR-QUERY-MIDJOURNEY-20261025'),
    'CA-20261025': ('CA-ART-GENERATORS-20261025', 'CA-ECOMMERCE-20261025', 'CA-FITNESS-20261025', 'CA-LEGAL-20261025', 'CA-TEACHERS-20261025'),
    'KW-20261025-r25': ('KW-ART-GENERATORS-20261025', 'KW-LEGAL-20261025', 'KW-ECOMMERCE-20261025', 'KW-SPREADSHEET-20261025', 'KW-SQL-20261025', 'KW-PRESENTATION-20261025', 'KW-PARAPHRASING-20261025', 'KW-DESIGN-GENERATORS-20261025'),
    'KW-20261025-merged': ('KW-SEO-TOOLS-20261025', 'KW-TRANSCRIPTION-20261025', 'KW-NOTE-TAKING-20261025', 'KW-STOCK-TRADING-20261025', 'KW-NO-CODE-20261025', 'KW-VIDEO-ENHANCER-20261025', 'KW-FINANCE-20261025', 'KW-STUDENTS-20261025'),
}
idx = {i.get('id'): i for i in nf}
for name, ids in series.items():
    present = [i for i in ids if i in idx]
    print(f'{name}: {len(present)}/{len(ids)} present ->', present)

# 分析师相关计数
pend = [i for i in nf if i.get('status') == 'pending']
print('\npending total:', len(pend))
from collections import Counter
src = Counter((i.get('source') or '')[:35] for i in pend)
print('pending by source:')
for s, c in src.most_common(12):
    print('  ', c, s)

# 最近的 completed
comp = [i for i in nf if i.get('status') == 'completed' and '2026-10-25' in (i.get('completed_at') or '')]
print('\ncompleted on 10-25:', len(comp))
for i in comp[-8:]:
    print('  ', i.get('id'), '|', (i.get('completed_at') or '')[:19])
