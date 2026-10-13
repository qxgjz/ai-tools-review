# -*- coding: utf-8 -*-
# 1) 找claude-opus正文文件 2) 清理completed待办到archived 3) 补录性能故障P0
import json, os, glob

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sp = os.path.join(base, 'iteration_center', 'state.json')

# 先找claude正文
print('=== 找claude-opus正文文件 ===')
for pat in ['**/*claude-opus-4-vs-gpt-5-2026*', '**/*claude*opus*4*']:
    for f in glob.glob(os.path.join(base, '**', pat.split('**/',1)[-1] if '**/' in pat else pat), recursive=True):
        if os.path.isfile(f) and f.endswith(('.md', '.json')):
            print(' ', f, os.path.getsize(f))

print()
print('=== 清理completed待办到archived ===')
with open(sp, encoding='utf-8') as f:
    data = json.load(f)
focus = data.get('next_iteration_focus', [])
archived = data.get('archived_todos', [])
if not isinstance(archived, list):
    archived = []

completed = [t for t in focus if t.get('status') == 'completed']
remain = [t for t in focus if t.get('status') != 'completed']
print('completed数量:', len(completed))
for t in completed:
    print('  清理: [{}] {}'.format(t.get('assigned_to'), str(t.get('task'))[:80]))
    # 标记archived原因
    t['archived_at'] = '2026-10-11'
    t['archived_reason'] = 'commander_daily_cleanup'
    archived.append(t)

data['next_iteration_focus'] = remain
data['archived_todos'] = archived

# 补录性能故障P0
perf_task = {
    'id': 'P0-PERF-001',
    'status': 'pending',
    'priority': 'P0',
    'assigned_to': ['window1', '架构师'],
    'task': 'P0-PERF-001: 网站性能故障持续36小时+（UX日志10-10：首页TTFB 4.29s、首页加载15s超时、404页面code=000不可达、Blog TTFB 5.07s）。立即排查Cloudflare Pages部署/资源加载瓶颈，恢复首页+404正常响应，部署后curl验证TTFB<1.5s',
    'source': 'ux_2026-10-10.md',
    'created': '2026-10-11'
}
# 去重检查
exists = any('P0-PERF' in str(t.get('task', '')) for t in remain)
if not exists:
    remain.append(perf_task)
    print('✅ 已补录性能故障P0: P0-PERF-001')
else:
    print('性能故障P0已存在')

with open(sp, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('✅ state.json 已更新: active={}, archived累计={}'.format(len(remain), len(archived)))
