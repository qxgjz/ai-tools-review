# -*- coding: utf-8 -*-
# 指挥官调度：待办完成率统计 + 报告问题校验
import json, os, glob, re, datetime

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sp = os.path.join(base, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    data = json.load(f)

focus = data.get('next_iteration_focus', [])
archived = data.get('archived_todos', [])

# 状态统计
from collections import Counter
status_cnt = Counter(str(t.get('status', 'unknown')) for t in focus)
prio_cnt = Counter(str(t.get('priority', 'unknown')) for t in focus)

# 按窗口统计 pending
win_cnt = Counter()
for t in focus:
    if str(t.get('status')) != 'completed':
        a = t.get('assigned_to', [])
        if isinstance(a, list):
            for w in a:
                win_cnt[str(w)] += 1
        else:
            win_cnt[str(a)] += 1

pending = status_cnt.get('pending', 0) + status_cnt.get('in_progress', 0)
completed = status_cnt.get('completed', 0)
total = pending + completed
rate = completed / total * 100 if total else 0

print('=== 待办统计 ===')
print('总待办(active):', len(focus))
print('状态分布:', dict(status_cnt))
print('优先级分布:', dict(prio_cnt))
print('pending:', pending, 'completed:', completed, '完成率: {:.1f}%'.format(rate))
print()
print('=== 各窗口pending数量 ===')
for w, c in win_cnt.most_common():
    print('  {}: {}'.format(w, c))
print()
print('archived累计:', len(archived))

# completed 待办列表（待清理）
print()
print('=== 待清理 completed 列表 ===')
comp_list = [t for t in focus if str(t.get('status')) == 'completed']
for t in comp_list:
    print('  [{}] {} | {}'.format(t.get('id','?'), t.get('task','')[:60], t.get('assigned_to')))
print('completed条数:', len(comp_list))

# 报告文件 P0/P1 校验
print()
print('=== 报告问题校验 ===')
report_files = ['audit_findings.md', 'index_monitor.md', 'content_originality_audit.md',
                'cloudflare_realtime_data.md', 'monetization_opportunities.md',
                'keyword_opportunities.md', 'pain_points.md', 'backlink_opportunities.md',
                'competitor_analysis_2026-10-09.md', 'ux_audit.md', 'performance.md',
                'gsc_latest_data.md', 'ga4_latest_data.md', 'health_report.md']
ic = os.path.join(base, 'iteration_center')
existing_tasks = ' '.join(str(t.get('task','')) + ' ' + str(t.get('id','')) for t in focus)
found_issues = []
for rf in report_files:
    p = os.path.join(ic, rf)
    if not os.path.exists(p):
        continue
    mtime = os.path.getmtime(p)
    mt = datetime.datetime.fromtimestamp(mtime).strftime('%m-%d %H:%M')
    with open(p, encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    for line in txt.splitlines():
        if re.search(r'\[?(P0|P1)\]?', line) and len(line) > 15:
            if re.search(r'待办|需|应|必须|修复|问题|故障|缺失|风险|异常|错误|优化|失败', line):
                found_issues.append((rf, mt, line.strip()[:130]))

print('报告文件P0/P1行动项候选:')
seen = set()
cnt_issues = 0
for rf, mt, line in found_issues[:60]:
    key = line[:40]
    if key in seen:
        continue
    seen.add(key)
    cnt_issues += 1
    print('  [{} {}] {}'.format(rf, mt, line))
print('去重后候选:', cnt_issues)

# window_logs 检查
print()
print('=== window_logs 最近文件 ===')
wl = os.path.join(base, 'window_logs')
if os.path.isdir(wl):
    files = sorted(glob.glob(os.path.join(wl, '*')), key=os.path.getmtime, reverse=True)
    for fp in files[:15]:
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%m-%d %H:%M')
        print('  [{}] {}'.format(mt, os.path.basename(fp)))
else:
    print('  无 window_logs 目录')
