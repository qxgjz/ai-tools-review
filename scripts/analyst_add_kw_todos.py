# -*- coding: utf-8 -*-
"""职责B：关键词挖掘待办写入 state.json（3 P0 SERP已验证 + 5 P1）"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
idx = {i.get('id'): i for i in nf}

todos = [
    {'id': 'KW-ART-GENERATORS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P0',
     'task': '基于关键词 [best AI art generators 2026] 写 2000 字新文章，标题建议 [Best AI Art Generators 2026: 8 Tested (Midjourney vs DALL-E 3 vs Adobe Firefly)]，slug 建议 [best-ai-art-generators-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '按用途矩阵（写实=Midjourney/易用=DALL-E 3/Adobe工作流=Firefly/本地控制=SD/开源=FLUX）+ 实测样图对比'},
    {'id': 'KW-LEGAL-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P0',
     'task': '基于关键词 [best AI legal tools 2026] 写 2000 字新文章，标题建议 [Best AI Legal Tools 2026: 8 Tested (Harvey vs Lexis+ AI vs Spellbook)]，slug 建议 [best-ai-legal-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '按律所规模分（大所=Harvey/中台=Lexis+ AI/起草=Spellbook/合同管理=Evisort）+ 合规与幻觉风险视角'},
    {'id': 'KW-ECOMMERCE-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P0',
     'task': '基于关键词 [best AI ecommerce tools 2026] 写 2000 字新文章，标题建议 [Best AI Ecommerce Tools 2026: 9 Tested (Shopify Sidekick vs Gorgias vs Klaviyo)]，slug 建议 [best-ai-ecommerce-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium', 'serp_verified': True,
     'our_angle': '按电商环节分（建站=Shopify Sidekick/客服=Gorgias/邮件=Klaviyo/搜索=Algolia）+ 定价分层'},
    {'id': 'KW-SPREADSHEET-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI spreadsheet tools 2026] 写 2000 字新文章，标题建议 [Best AI Spreadsheet Tools 2026: 8 Tested]，slug 建议 [best-ai-spreadsheet-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium'},
    {'id': 'KW-SQL-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI SQL tools 2026] 写 2000 字新文章，标题建议 [Best AI SQL Tools 2026: 7 Tested]，slug 建议 [best-ai-sql-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium'},
    {'id': 'KW-PRESENTATION-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI presentation tools 2026] 写 2000 字新文章，标题建议 [Best AI Presentation Tools 2026: 9 Tested]，slug 建议 [best-ai-presentation-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High'},
    {'id': 'KW-PARAPHRASING-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI paraphrasing tools 2026] 写 2000 字新文章，标题建议 [Best AI Paraphrasing Tools 2026: 8 Tested]，slug 建议 [best-ai-paraphrasing-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High'},
    {'id': 'KW-DESIGN-GENERATORS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '基于关键词 [best AI design generators 2026] 写 2000 字新文章，标题建议 [Best AI Design Generators 2026: 10 Tested]，slug 建议 [best-ai-design-generators-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium'},
]

added = []
for t in todos:
    if t['id'] not in idx:
        t.update({'status': 'pending', 'created_at': now})
        nf.append(t); idx[t['id']] = t; added.append(t['id'])

d['next_iteration_focus'] = nf
d['last_update'] = now
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('added:', added)
print('focus:', len(nf))
