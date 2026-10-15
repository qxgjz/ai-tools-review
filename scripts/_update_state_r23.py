import json, io, sys
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = 'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
items = d['next_iteration_focus']
new = [
    {
        'id': 'GEO-PAGED-TITLE-20261015',
        'task': 'GEO审计发现：authors分页页 title 超长（68字符）需截断',
        'title': 'Authors分页页 title 截断至52字符',
        'priority': 'P1',
        'status': 'completed',
        'assigned_to': ['window1', '架构师'],
        'source': 'geo_audit_2026-10-15',
        'created_at': now,
        'completed_at': now,
        'completion_note': 'app/authors/[slug]/page/[page]/page.tsx metadata title改为"AIToolCrux Editorial Team - AI Tool Reviews (Page N)"=52字符；本地审计 title_long 2->0；commit c046bde'
    },
    {
        'id': 'GEO-OG-STUB-20261015',
        'task': 'GEO审计发现：/og/ stub页 title过短22+无meta+无schema',
        'title': '/og/ stub 页 metadata 补全（title/description/noindex/JSON-LD）',
        'priority': 'P1',
        'status': 'completed',
        'assigned_to': ['window1', '架构师'],
        'source': 'geo_audit_2026-10-15',
        'created_at': now,
        'completed_at': now,
        'completion_note': 'public/og/index.html 加完整title(47字符)+meta description+robots noindex+CollectionPage JSON-LD；本地审计 no_meta 1->0、no_schema 1->0；commit c046bde'
    },
]
ids = {x.get('id') for x in items}
for n in new:
    if n['id'] not in ids:
        items.append(n)
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('added:', len([n for n in new if n['id'] not in ids]))
