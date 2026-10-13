# -*- coding: utf-8 -*-
"""指挥官每日调度：验证待办+统计关键数据"""
import json, os
from collections import Counter

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p = os.path.join(base, 'iteration_center', 'state.json')
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])

# 1. 验证HN登录态/aitoolsdirectory待办是否存在
print('=== 验证增长窗口补录 ===')
hn = [t for t in focus if 'HN' in str(t.get('task','')) or '登录态' in str(t.get('task','')) or 'aitoolsdirectory' in str(t.get('task',''))]
for t in hn:
    print(' - [%s/%s] %s' % (t.get('priority'), t.get('status'), str(t.get('task',''))[:80]))
if not hn:
    print(' ❌ 增长日志声称补录但state.json中未找到！需补录')

# 2. 按窗口统计pending
print()
print('=== 各窗口待办数（pending+open） ===')
win = Counter()
for t in focus:
    if t.get('status') in ('pending', 'open'):
        for a in (t.get('assigned_to') or []):
            win[a] += 1
for w, c in sorted(win.items(), key=lambda x: -x[1]):
    print(' %s: %d' % (w, c))

# 3. 统计文章/工具数
print()
print('=== 关键数据 ===')
for fname, label in [('data/posts.json', '文章数'), ('data/tools.json', '工具数')]:
    fp = os.path.join(base, fname)
    try:
        arr = json.load(open(fp, encoding='utf-8'))
        print(' %s: %d' % (label, len(arr)))
    except Exception as e:
        print(' %s: 读取失败 %s' % (label, str(e)[:60]))

# 4. 截图数（递归）
shot_dir = os.path.join(base, 'public', 'screenshots')
if os.path.isdir(shot_dir):
    n = sum(1 for _, _, fs in os.walk(shot_dir) for f in fs if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')))
    print(' 截图数: %d' % n)
else:
    print(' 截图目录不存在')

# 5. 迭代轮次
print(' 迭代轮次(archived数量):', len(d.get('archived_todos', [])))
print(' ga4_api_status:', str(d.get('ga4_api_status',''))[:80])

# 6. 最新GSC报告
gsc_dir = os.path.join(base, 'gsc-ga4-report')
if os.path.isdir(gsc_dir):
    files = [f for f in os.listdir(gsc_dir) if f.startswith('live_pull') and f.endswith('.json')]
    files.sort()
    if files:
        latest = os.path.join(gsc_dir, files[-1])
        g = json.load(open(latest, encoding='utf-8'))
        print()
        print(' 最新GSC报告:', files[-1])
        print(' 曝光/点击:', g.get('total_impressions'), '/', g.get('total_clicks'))
