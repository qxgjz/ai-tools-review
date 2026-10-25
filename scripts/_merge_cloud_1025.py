# -*- coding: utf-8 -*-
"""合并云端快照侧 10-25 产出的待办到本地主项目 state.json（方案A）"""
import json
from datetime import datetime

LOCAL = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

d = json.load(open(LOCAL, encoding='utf-8'))
nf = d['next_iteration_focus']
existing = {i.get('id') for i in nf}

cloud_todos = [
    # 10-25 关键词轮（3 P0，SERP 已验证）
    {'id': 'KW-SEO-TOOLS-20261025', 'status': 'pending', 'priority': 'P0',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI SEO tools 2026] 写 2000 字新文章，标题建议 [Best AI SEO Tools 2026: 10 Tested (Semrush vs Surfer vs Frase) — With GEO/AI-Search Angle]，slug 建议 [best-ai-seo-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '分任务矩阵（Semrush=全站/Ahrefs=外链/Surfer=内容优化）+ GEO 与 AI 搜索可见性差异化（传统 SEO 平台不覆盖 AI 引用）',
     'created_at': now},
    {'id': 'KW-TRANSCRIPTION-20261025', 'status': 'pending', 'priority': 'P0',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI transcription tools 2026] 写 2000 字新文章，标题建议 [Best AI Transcription Tools 2026: 9 Tested (Otter vs Fireflies vs Descript)]，slug 建议 [best-ai-transcription-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '按用例分（会议=Otter/CRM=Fireflies/播客=Descript/企业=Deepgram）+ 实测准确率对比（93.4% vs 98.7%）',
     'created_at': now},
    {'id': 'KW-NOTE-TAKING-20261025', 'status': 'pending', 'priority': 'P0',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI note taking apps 2026] 写 2000 字新文章，标题建议 [Best AI Note-Taking Apps 2026: 10 Compared (Notion AI vs Mem vs NotebookLM)]，slug 建议 [best-ai-note-taking-apps-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'serp_verified': True,
     'our_angle': '按需求分（工作区=Notion/第二大脑=Mem/加密=Reflect/研究=NotebookLM/自托管=Obsidian），定价+加密双矩阵',
     'created_at': now},
    # 10-25 关键词轮（5 P1）
    {'id': 'KW-STOCK-TRADING-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI stock trading tools 2026] 写 2000 字新文章，标题建议 [Best AI Stock Trading Tools 2026: 7 Tested (TrendSpider vs Danelfin vs Trade Ideas)]，slug 建议 [best-ai-stock-trading-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium', 'created_at': now},
    {'id': 'KW-NO-CODE-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI no-code tools 2026] 写 2000 字新文章，标题建议 [Best AI No-Code Tools 2026: 10 Tested (Bubble vs Lovable vs Bolt)]，slug 建议 [best-ai-no-code-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium', 'created_at': now},
    {'id': 'KW-VIDEO-ENHANCER-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI video enhancers 2026] 写 2000 字新文章，标题建议 [Best AI Video Enhancers 2026: 8 Tested (Topaz vs HitPaw vs CapCut)]，slug 建议 [best-ai-video-enhancer-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium', 'created_at': now},
    {'id': 'KW-FINANCE-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI finance tools 2026] 写 2000 字新文章，标题建议 [Best AI Finance Tools 2026: 9 Tested (for budgeting & investing)]，slug 建议 [best-ai-finance-tools-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'Medium', 'created_at': now},
    {'id': 'KW-STUDENTS-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window2', '创作家'],
     'task': '基于关键词 [best AI tools for students 2026] 写 2000 字新文章，标题建议 [Best AI Tools for Students 2026: 12 Picks (Study Stack)]，slug 建议 [best-ai-tools-for-students-2026]',
     'source': 'keyword_mining_2026-10-25', 'serp_competition': 'High', 'created_at': now},
    # 10-25 SOP 轮（3 CTR 页面级）
    {'id': 'CTR-BLOG-OPENAI-ASTRA-WWW-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window5', '打磨师'],
     'task': '页面 https://www.aitoolcrux.com/blog/openai_astra_review 排名 11.4 但 CTR 仅 0.64%，优化 title/meta description 提升点击率',
     'source': 'ctr_optimization_2026-10-25', 'created_at': now},
    {'id': 'CTR-BLOG-MIDJOURNEY-V7-215236-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window5', '打磨师'],
     'task': '页面 midjourney v7 查询 排名 6.8 但 CTR 仅 0%，优化 title/meta description 提升点击率',
     'source': 'ctr_optimization_2026-10-25', 'created_at': now},
    {'id': 'CTR-BLOG-CREATIUM-COACH-173022-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window5', '打磨师'],
     'task': '页面 creatium coach 查询 排名 8.5 但 CTR 仅 0%，优化 title/meta description 提升点击率',
     'source': 'ctr_optimization_2026-10-25', 'created_at': now},
    # 10-25 SOP 轮（1 新发现）
    {'id': 'P1-GSC-QUERY-DATA-GAP-20261025', 'status': 'pending', 'priority': 'P1',
     'assigned_to': ['window1', '窗口1'],
     'task': 'GSC 查询级数据被 -site: 过滤器垃圾查询污染（13/23 为工具生成 site 排除式长查询，干净词仅 10 个）：fetch_gsc 脚本需过滤 -site: 模式查询 + 提高查询维度 rowLimit',
     'source': 'gsc_query_data_gap_2026-10-25', 'created_at': now},
]

added = [t for t in cloud_todos if t['id'] not in existing]
nf.extend(added)
d['next_iteration_focus'] = nf
d['last_update'] = now
json.dump(d, open(LOCAL, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('added:', len(added), '| skipped(dup):', len(cloud_todos) - len(added))
print('focus:', len(nf))
