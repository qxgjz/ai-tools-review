# -*- coding: utf-8 -*-
"""补录GSC调查发现到state.json待办 (2026-10-24)"""
import json, io, sys, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
focus = d['next_iteration_focus']

new_todos = []
t1 = ('检查Cloudflare防火墙/Bot规则是否误伤Googlebot：GSC显示best-ai-agent-tools-2026为'
      '"Google无法识别此网址"，疑似新加坡IP段Bot清洗规则拦截Googlebot抓取。'
      '1)查CF WAF/Bot管理规则是否排除verified Googlebot；'
      '2)用GSC URL Inspection"测试实际网址"验证抓取返回200+正确内容；'
      '3)若有误伤立即改规则')
if not any('Cloudflare防火墙' in t.get('task', '') or '误伤Googlebot' in t.get('task', '') for t in focus):
    new_todos.append({'id': 'CMD-20261024-001', 'status': 'pending', 'priority': 'P0',
        'assigned_to': 'window1(核心迭代)', 'source': 'commander_diagnosis_20261024_gsc_inspect',
        'task': t1, 'url': 'https://www.aitoolcrux.com/blog/best-ai-agent-tools-2026'})

t2 = ('验证2026-10-24批量请求收录效果：14个URL(13个/tools/工具页+best-ai-agent-tools-2026)'
      '已通过GSC请求编入索引(req_index_batch_20261024.json)，'
      '7天后(2026-10-31)用GSC inspect复查收录状态变化，产出对比报告写入gsc-ga4-report/')
if not any('批量请求收录' in t.get('task', '') and '验证' in t.get('task', '') for t in focus):
    new_todos.append({'id': 'CMD-20261024-002', 'status': 'pending', 'priority': 'P1',
        'assigned_to': 'window4(数据分析)', 'source': 'commander_diagnosis_20261024_gsc_inspect',
        'task': t2, 'url': 'https://www.aitoolcrux.com/gsc-ga4-report/req_index_batch_20261024.json'})

if new_todos:
    focus.extend(new_todos)
    focus.sort(key=lambda x: (0 if x.get('priority') == 'P0' else 1 if x.get('priority') == 'P1' else 2, x.get('id', '')))
    d['next_iteration_focus'] = focus
    d['last_updated'] = now
    d['last_commander_review'] = now
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('added', len(new_todos), 'todos; focus now', len(focus))
else:
    print('no new todos needed; focus', len(focus))
