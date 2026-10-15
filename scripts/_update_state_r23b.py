import json, io, sys
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = 'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
items = d['next_iteration_focus']
targets = {
    'ux_p0_severe_degradation_day7_2026-10-15': {
        'status': 'completed', 'completed_at': now,
        'completion_note': '误报：服务器端 web_fetch 首页200完整/Blog 200(154篇)/404正常，无TTFB 12s故障；UX窗口本机网络不可达（同r21 ux_p0_all_pages_timeout 判定）；commit 7f6b321'
    },
    'GEO-BESTFOR-META-FIX-20261015': {
        'status': 'completed', 'completed_at': now,
        'completion_note': 'best-for 3页 metaTitle 源串改短（&实体转义致raw超60根因）：content-creators 59/startups 56/students 58 raw（unescape 55/52/54）；本地out核验≤60；commit 7f6b321'
    },
    'GEO-BESTFOR-META-20261014': {
        'status': 'completed', 'completed_at': now,
        'completion_note': '同GEO-BESTFOR-META-FIX-20261015：best-for generateMetadata title 截断根因修复（&amp;转义后超60，改源串≤60）；commit 7f6b321'
    },
}
n = 0
for x in items:
    if x.get('id') in targets and x.get('status') == 'pending':
        for k, v in targets[x['id']].items():
            x[k] = v
        n += 1
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('completed:', n)
