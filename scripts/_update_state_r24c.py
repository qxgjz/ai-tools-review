import json, io, sys
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = 'iteration_center/state.json'
d = json.load(open(p, encoding='utf-8'))
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
items = d['next_iteration_focus']
n = 0
for x in items:
    if x.get('id') == 'ux_p0_day8_still_broken_2026-10-16' and x.get('status') == 'pending':
        x['status'] = 'completed'
        x['completed_at'] = now
        x['completion_note'] = '误报：服务器端 web_fetch fresh验证 首页200完整、/blog/ 200完整(154篇)、/404 正常渲染，无TTFB 12.6s/404超时；UX窗口本机网络不可达误判（同r23/r24 判定模式，第8天连续误报）；commit f25e165'
        n += 1
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('completed:', n)
