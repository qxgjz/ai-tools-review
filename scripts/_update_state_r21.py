import json, io, sys
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

p = 'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
items = d['next_iteration_focus']
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# 本轮已完成的技术修复（本地审计 r21 验证）
done_map = {
    'GEO-OG-NOINDEX-20261014': 'robots.ts 通用+全部AI爬虫规则 disallow 追加 /og/（OG图片API静态产物stub页，禁索引防AI爬虫浪费抓取配额）。产物title_long 26→0、meta_long 6→0、title_short 4→3。commit 待push。',
    'GEO-BESTFOR-META-20261014': 'best-for/[audience] generateMetadata 加 title≤60/desc≤155 截断，3 页（content-creators/startups/students）title 超长修复。',
    'GEO-TRAFFIC-META-20261014': 'top-ai-tools-by-traffic metadata 规范化：title 加品牌后缀 28→37 字符、description 170→~150 字符（<160）。',
}

# 新增待办（审计发现）
new_todos = [
    {
        'id': 'AUTHORS-PAGE-SIZE-20261014',
        'task': 'authors 页体积优化',
        'title': 'authors/aitoolcrux-editorial-team 页 665.7KB（RSC payload 389KB 为 164 张文章卡 JSX 结构）需分页/懒加载优化，目标 <400KB',
        'priority': 'P1',
        'status': 'pending',
        'assigned_to': ['window1', '架构师'],
        'source': 'seo_audit_local_20261014',
        'created_at': now,
        'note': '数据字段精简已完成（map 只保留 slug/title/excerpt/date/readingTime/category），但 Next.js RSC 序列化结构占大头，需列表分页或只渲染部分+客户端加载更多',
    },
    {
        'id': 'TITLE-SHORT-20261014',
        'task': '辅助页 title 加长',
        'title': '/sitemap/（20字符）、/search/（28字符，noindex 页）title 过短；/search/ 无需处理（已 noindex），/sitemap/ 可加长',
        'priority': 'P2',
        'status': 'pending',
        'assigned_to': ['window1', '架构师'],
        'source': 'seo_audit_local_20261014',
        'created_at': now,
    },
]

ids = {x.get('id') for x in items}
updated = 0
for k, n in done_map.items():
    if k in ids:
        for x in items:
            if x.get('id') == k and x.get('status') == 'pending':
                x['status'] = 'completed'
                x['completed_at'] = now
                x['completion_note'] = n
                updated += 1
    else:
        items.append({
            'id': k,
            'task': k,
            'title': n[:80],
            'priority': 'P1',
            'status': 'completed',
            'assigned_to': ['window1', '架构师'],
            'source': 'geo_audit_20261014',
            'created_at': now,
            'completed_at': now,
            'completion_note': n,
        })
        updated += 1

added = 0
for t in new_todos:
    if t['id'] not in ids:
        items.append(t)
        added += 1

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

from collections import Counter
c = Counter(x.get('priority') for x in items if x.get('status') == 'pending')
mine = [x for x in items if x.get('status') == 'pending' and ('window1' in x.get('assigned_to', []) or '架构师' in x.get('assigned_to', []))]
print('completed:', updated, '| added:', added, '| 架构师pending:', len(mine), '| 全局pending:', sum(c.values()), dict(c))
