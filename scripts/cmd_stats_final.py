# -*- coding: utf-8 -*-
# 1) 验证claude-opus正文(从posts.json) 2) 统计网站关键数据 3) 读最新GSC
import json, os, sys
from pathlib import Path

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(base)
sys.path.insert(0, base)

# 1) claude-opus正文评分
from zens_ink import content_qc
posts = os.path.join(base, 'data', 'posts.json')
with open(posts, encoding='utf-8') as f:
    pdata = json.load(f)
if isinstance(pdata, dict):
    items = pdata.get('posts', pdata)
else:
    items = pdata

found = None
if isinstance(items, list):
    found = next((x for x in items if 'claude-opus-4-vs-gpt-5-2026' in str(x.get('slug', ''))), None)
else:
    found = items.get('claude-opus-4-vs-gpt-5-2026')
if found:
    tmp = os.path.join(base, 'scripts', 'tmp_claude.md')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write('# {}\n\n{}'.format(found.get('title', ''), found.get('content', '')))
    try:
        r = content_qc.check_draft(Path(tmp))
        if isinstance(r, dict):
            print('claude-opus正文 score =', r.get('score') or r.get('total_score') or r.get('quality_score'))
        else:
            print('claude-opus正文 返回:', str(r)[:150])
    except Exception as e:
        print('claude-opus正文 ❌', str(e)[:150])

# 2) 关键数据
print()
print('=== 关键数据统计 ===')
# 文章数
n_posts = len(items) if isinstance(items, list) else len(items.get('posts', {}))
print('文章数:', n_posts)
# 工具数
tools_p = os.path.join(base, 'data', 'tools.json')
if os.path.exists(tools_p):
    with open(tools_p, encoding='utf-8') as f:
        tdata = json.load(f)
    if isinstance(tdata, list):
        print('工具数:', len(tdata))
    elif isinstance(tdata, dict):
        print('工具数:', len(tdata.get('tools', tdata)))
else:
    print('tools.json 不存在')
# 截图数
shot_dir = os.path.join(base, 'public', 'screenshots')
n_shot = 0
if os.path.isdir(shot_dir):
    for dp, dn, fn in os.walk(shot_dir):
        n_shot += len([f for f in fn if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
print('截图数:', n_shot)
# 迭代轮次
sp = os.path.join(base, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    data = json.load(f)
print('archived迭代:', len(data.get('archived_todos', [])))
focus = data.get('next_iteration_focus', [])
print('active待办:', len(focus))
comp = [t for t in focus if t.get('status') == 'completed']
pend = [t for t in focus if t.get('status') != 'completed']
print('active中pending:', len(pend), 'completed:', len(comp))
# 按窗口
import collections
win = collections.Counter()
for t in pend:
    a = t.get('assigned_to')
    if isinstance(a, list):
        a = ','.join(a)
    win[str(a)] += 1
print('按窗口pending:', dict(win))
# 优先级
prio = collections.Counter()
for t in pend:
    prio[t.get('priority', '?')] += 1
print('优先级:', dict(prio))

# 3) 最新GSC文件
print()
print('=== GSC最新文件 ===')
gsc_dir = os.path.join(base, 'gsc-ga4-report')
if os.path.isdir(gsc_dir):
    files = [f for f in os.listdir(gsc_dir) if 'gsc' in f.lower() or 'GSC' in f]
    files.sort()
    print('GSC相关文件:', files[-5:] if files else '无')
else:
    print('gsc-ga4-report 目录不存在')
