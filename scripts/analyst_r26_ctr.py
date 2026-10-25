# -*- coding: utf-8 -*-
"""分析师 SOP r26：①阻塞待办复查 ②新增 CTR 优化待办（排名5-15且CTR<3%，本轮5条）"""
import json, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
idx = {i.get('id'): i for i in nf}
added = []
notes = []

# ① 阻塞待办复查（保持 pending + 追加 note）
for tid, note in [
    ('P1-GEO-BASELINE-AUDIT-20261013', '2026-10-25 15:09 复查：引用级 baseline 需浏览器跑 ChatGPT Search/Perplexity/AIO，本机无 GUI 会话；技术就绪度 8.94 已确认，缺引用级实测，保持 pending'),
    ('P1-TOOL-ELMO-20261017', '2026-10-25 15:09 复查：elmo 部署需 Docker，本机 docker 不可用；已被 P0-GEO-ELMO-TRACKER 承接，保持 pending'),
]:
    i = idx.get(tid)
    if i:
        i['status_note_' + '20261025_1509'] = note
        notes.append(tid)

# ② CTR 优化待办：基于 2026-09-24_2026-10-23 新报告（实际读取）
# 命中 5 个页面：排名 5-15 且 CTR<3%
ctr_items = [
    ('https://www.aitoolcrux.com/blog/ai-coding-tools-comparison-2026', '5.5', '0'),
    ('https://www.aitoolcrux.com/blog/article-api-20260904-214749-creatium-coach-review-2025-an-honest-look-at-this-ai-business-coaching-tool-md', '6.0', '0'),
    ('https://www.aitoolcrux.com/blog/best-ai-meeting-assistants-2026', '9.0', '0'),
    ('https://www.aitoolcrux.com/blog/best-ai-observability-tools-2026', '9.5', '0'),
    ('https://www.aitoolcrux.com/blog/best-ai-productivity-tools-2026', '10.5', '0'),
]
for url, pos, ctr in ctr_items:
    slug = url.rstrip('/').split('/')[-1][:40]
    tid = 'CTR-PAGE-' + slug.upper().replace('-', '-')[:36] + '-20261025'
    task = f'页面 {url} 排名 {pos} 但 CTR 仅 {ctr}%，优化 title/meta description 提升点击率'
    if tid not in idx:
        nf.append({'id': tid, 'status': 'pending', 'priority': 'P1',
                   'assigned_to': ['window5', '打磨师'], 'task': task,
                   'source': 'ctr_optimization_2026-10-25', 'created_at': now,
                   'position': float(pos), 'ctr_pct': float(ctr), 'impressions': None})
        idx[tid] = nf[-1]
        added.append(tid)

d['next_iteration_focus'] = nf
d['last_update'] = now
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('notes appended:', notes)
print('ctr todos added:', added)
print('focus:', len(nf))
