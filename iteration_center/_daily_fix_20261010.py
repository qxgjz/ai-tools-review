# -*- coding: utf-8 -*-
"""指挥官每日调度：修复assigned_to + 补录缺失待办"""
import json, os

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p = os.path.join(base, 'iteration_center', 'state.json')
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])

# 1. 修复assigned_to为字符串的待办
fixed = 0
for t in focus:
    at = t.get('assigned_to')
    if isinstance(at, str):
        # 如果是完整窗口名，包成数组
        known = ['window1','window2','window3','window4','window5','window6','window7','架构师','分析师','创作家','打磨师','拓荒者','体验官','设计师','polisher','analyst','all_windows','window5','增长']
        if at in known:
            t['assigned_to'] = [at]
            fixed += 1
        elif at.startswith('window'):
            t['assigned_to'] = [at]
            fixed += 1
print('修复assigned_to字符串->数组:', fixed, '条')

# 2. 补录增长窗口缺失待办（增长日志声称写了但没写）
all_text = ' '.join(str(t.get('task','')) for t in focus)
new_todos = []
if 'aitoolsdirectory' not in all_text:
    new_todos.append({
        'task': '跟踪aitoolsdirectory.com审核结果（2026-10-10已提交，表单aitool.paperform.co，等待人工审核，通常几天）：审核通过后确认dofollow外链上线并记录到accounts.md',
        'priority': 'P1',
        'status': 'pending',
        'assigned_to': ['window2'],
        'source': 'backlink_opportunities_20261010',
        'created_at': '2026-10-10'
    })
if '登录态' not in all_text:
    new_todos.append({
        'task': 'HN登录态恢复：aitoolcrux账号(karma=1)登录态丢失，需用户手动在浏览器登录news.ycombinator.com后，window2才能继续评论养号。同时Reddit(Beautiful_Smoke_2425)也需确认登录态',
        'priority': 'P1',
        'status': 'pending',
        'assigned_to': ['window2'],
        'source': 'backlink_opportunities_20261010',
        'created_at': '2026-10-10'
    })
if new_todos:
    focus = new_todos + focus
    d['next_iteration_focus'] = focus
    print('补录待办:', len(new_todos), '条')
    for t in new_todos:
        print(' - [%s] %s' % (t['priority'], t['task'][:60]))
else:
    print('无需补录')

# 3. 看GSC报告结构
gsc_dir = os.path.join(base, 'gsc-ga4-report')
files = [f for f in os.listdir(gsc_dir) if f.startswith('live_pull') and f.endswith('.json')]
files.sort()
if files:
    g = json.load(open(os.path.join(gsc_dir, files[-1]), encoding='utf-8'))
    print()
    print('GSC报告 keys:', list(g.keys())[:15])
    for k in ['impressions','clicks','total_impressions','total_clicks','totalImpressions','totalClicks','totals']:
        if k in g:
            print(' ', k, '=', g[k])

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print()
print('保存完成，待办总数:', len(d['next_iteration_focus']))
