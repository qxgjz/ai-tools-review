# -*- coding: utf-8 -*-
"""分析师 r27：标记 P0 完成 + 阻塞复查 + CTR 分析（从 live_pull + 新报告实读）"""
import json, os, glob
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
SP = os.path.join(P, 'iteration_center', 'state.json')
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
d = json.load(open(SP, encoding='utf-8'))
nf = d['next_iteration_focus']
idx = {i.get('id'): i for i in nf}

# ① P0 完成
p0 = idx.get('P0-GSC-INDEXED-ZERO-REPORT-20261025')
if p0 and p0.get('status') == 'pending':
    p0['status'] = 'completed'
    p0['completed_at'] = now
    p0['evidence'] = 'gsc_indexed_baseline_20261025.md 已产出：总URL 905 / indexed 477 (52.8%) / not_indexed 428 (discovered_not_indexed 400 为最大类)；纠正收录=0 误判（sitemap API 口径 bug + 301/308 重定向链）'
    print('P0 completed:', p0['id'])

# ② 阻塞复查（保持 pending + note）
for tid, note in [
    ('P1-GEO-BASELINE-AUDIT-20261013', '2026-10-25 21:06 复查：需浏览器跑 ChatGPT Search/Perplexity/AIO，本机无 GUI 会话，保持 pending'),
    ('P1-TOOL-ELMO-20261017', '2026-10-25 21:06 复查：需 Docker 本机不可用，已被 P0-GEO-ELMO-TRACKER 承接，保持 pending'),
]:
    i = idx.get(tid)
    if i:
        i['status_note_' + '20261025_2106'] = note
        print('note appended:', tid)

# ③ CTR 分析：读新报告 2026-09-24_2026-10-23.md 的页面/查询段
rep = os.path.join(P, 'gsc-ga4-report', '2026-09-24_2026-10-23.md')
content = open(rep, encoding='utf-8').read()
print('--- report excerpt (first 80 lines) ---')
for ln in content.splitlines()[:80]:
    print(ln)

d['next_iteration_focus'] = nf
json.dump(d, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('focus:', len(nf))
