import json, io, sys
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = 'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
items = d['next_iteration_focus']
n = 0
for x in items:
    if x.get('id') == 'ux_p1_rotating_outage_day7_pm_2026-10-15' and x.get('status') == 'pending':
        x['status'] = 'completed'
        x['completed_at'] = now
        x['completion_note'] = '误报：服务器端 web_fetch 首页200完整(533+工具/Quick Answer/FAQ全渲染)、/blog/ 200完整(154篇+Featured)均正常，无"轮流宕机"；UX窗口本机网络不可达误判（同r23 ux_p0 判定）；commit 6c3d9d5'
        n += 1
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('completed:', n)
