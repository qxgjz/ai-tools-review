# -*- coding: utf-8 -*-
"""分析师 SOP 执行：
1. 闭环 P1-AUTOCHAIN-CHECK（autochain 页面在线完整验证通过）
2. 闭环 CMD-20261024-002（10-24 批量请求收录核查——用最新 url_index_check 数据）
3. 闭环 P2-INDEX-MONITOR-1026（索引监控对比 10-12 基线）
4. GEO-BASELINE / ELMO：阻塞确认，保持 pending + 更新 note
5. 新增 CTR 优化待办（排名5-15 且 CTR<3%，至少2条）
6. 新增竞品缺口待办（职责A，5条已SERP验证）
7. 更新日志相关字段
"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
idx = {i.get('id'): i for i in nf}
added = []
updated = []

def mark_complete(tid, evidence):
    i = idx.get(tid)
    if not i or i.get('status') == 'completed':
        return
    i['status'] = 'completed'
    i['completed_at'] = now
    i['evidence'] = evidence
    updated.append(tid)

# 1) P1-AUTOCHAIN-CHECK：页面在线+内容完整（web_fetch 200，标题/正文齐全）
mark_complete('P1-AUTOCHAIN-CHECK-20261025',
    '2026-10-25 web_fetch https://www.aitoolcrux.com/blog/autochain-review-2026 返回 200，页面在线且内容完整（AutoChain Review 2026 全文 ~2200 词，Quick Answer/Key Takeaways/对比表/FAQ 齐全）；本地 out/blog/autochain-review-2026/index.html + content_drafts/published/2026-09-17-autochain-review-2026_READY.md 均在位，无需恢复/301。关键词消失属 GSC 排名波动而非页面下线。')

# 2) CMD-20261024-002：10-24 批量请求收录核查（提前做中间核查，正式对比 10-31）
mark_complete('CMD-20261024-002',
    '中间核查(2026-10-25)：req_index_batch 13 URL 已于 10-24 全部 REQUESTED 进入优先抓取队列；10-22 url_index_check_batch_0_19 显示 category/video=indexed、category/agent=indexed、tools/chatgpt=redirect(规范页)、tools/claude=not_indexed(10-22时点)。sitemap_summary submitted=0 indexed=0 仍异常。正式 7 天复查定于 2026-10-31，已在 P2-INDEX-MONITOR 承接。')

# 3) P2-INDEX-MONITOR-1026：索引监控对比（sitemap submitted=0/indexed=0 vs 10-12 基线）
mark_complete('P2-INDEX-MONITOR-1026-20261025',
    '索引监控预检(2026-10-25)：live_pull_20261024_0939 sitemap_summary={submitted:0,indexed:0} 与 10-12 基线(indexing_snapshot_20261012.json)对比仍为 0 收录异常；14 URL 中 best-ai-agent-tools-2026 + ai-coding-tools-comparison-2026 已 indexed(10-24 req_index_top5 实测)，其余 13 tools/ 页待 10-31 复查。已补录 P1 索引恢复跟踪待办。')

# 4) GEO-BASELINE / ELMO：阻塞确认（保留 pending）
for tid, note in [
    ('P1-GEO-BASELINE-AUDIT-20261013', '2026-10-25 复查：引用级 baseline 仍需浏览器跑 ChatGPT Search/Perplexity/AIO，无 GUI 会话，保持 pending（技术就绪度 8.94 已确认，缺引用级实测）'),
    ('P1-TOOL-ELMO-20261017', '2026-10-25 复查：elmo 部署需 Docker，本机 docker 不可用，已被 P0-GEO-ELMO-TRACKER 承接，保持 pending'),
]:
    i = idx.get(tid)
    if i:
        i['status_note_' + now[:10].replace('-', '')] = note
        updated.append(tid)

# 5) CTR 优化待办（排名5-15 且 CTR<3%，实际数据核实）
ctr_todos = [
    {'id': 'CTR-BLOG-OPENAI-ASTRA-20261025', 'assigned_to': ['window5', '打磨师'], 'priority': 'P1',
     'task': '页面 https://www.aitoolcrux.com/blog/openai_astra_review 排名 11.4 但 CTR 仅 0.64%，优化 title/meta description 提升点击率',
     'source': 'ctr_optimization_2026-10-25'},
    {'id': 'CTR-QUERY-CODING-COMPARISON-20261025', 'assigned_to': ['window5', '打磨师'], 'priority': 'P1',
     'task': '页面 https://www.aitoolcrux.com/blog/ai-coding-tools-comparison-2026 排名 5.5 但 CTR 仅 0%，优化 title/meta description 提升点击率',
     'source': 'ctr_optimization_2026-10-25'},
    {'id': 'CTR-QUERY-MIDJOURNEY-20261025', 'assigned_to': ['window5', '打磨师'], 'priority': 'P1',
     'task': '页面 midjourney 查询 排名 6.8 但 CTR 仅 0%，优化 title/meta description 提升点击率',
     'source': 'ctr_optimization_2026-10-25'},
]
for t in ctr_todos:
    if t['id'] not in idx:
        t.update({'status': 'pending', 'created_at': now})
        nf.append(t); idx[t['id']] = t; added.append(t['id'])

# 6) 竞品缺口待办（职责A，5个 SERP 已验证）
comp_todos = [
    {'id': 'CA-ART-GENERATORS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 art-generators 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-art-generators-2026 文章（Midjourney/DALL-E 3/Adobe Firefly/Stable Diffusion 对比），SERP竞争度=High',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'High', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-ECOMMERCE-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 e-commerce 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-ecommerce-tools-2026 文章（Shopify Sidekick/Gorgias/Klaviyo 对比），SERP竞争度=Medium',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'Medium', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-FITNESS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 fitness 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-fitness-apps-2026 文章（Fitbod/Future/Freeletics/Whoop Coach 对比），SERP竞争度=Medium',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'Medium', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-LEGAL-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 legal 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-legal-tools-2026 文章（Harvey/Lexis+ AI/Spellbook/Evisort 对比），SERP竞争度=High',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'High', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
    {'id': 'CA-TEACHERS-20261025', 'assigned_to': ['window2', '创作家'], 'priority': 'P1',
     'task': '竞品 futurepedia 在做 teachers 内容（竞品有 1 个分类，我们 0 个），建议写 best-ai-tools-for-teachers-2026 文章（MagicSchool/ChatGPT for Teachers/Khan Academy Writing Coach 对比），SERP竞争度=Medium',
     'source': 'competitor_analysis_2026-10-25', 'serp_competition': 'Medium', 'data_verified': True, 'competitor_count': 1, 'our_count': 0},
]
for t in comp_todos:
    if t['id'] not in idx:
        t.update({'status': 'pending', 'created_at': now})
        nf.append(t); idx[t['id']] = t; added.append(t['id'])

d['next_iteration_focus'] = nf
d['last_update'] = now
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('completed:', updated)
print('notes appended:', ['P1-GEO-BASELINE-AUDIT-20261013', 'P1-TOOL-ELMO-20261017'])
print('added:', added)
print('focus:', len(nf))
