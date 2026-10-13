# -*- coding: utf-8 -*-
import json
from collections import Counter

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
pend = [t for t in focus if t.get('status') in ('pending', 'in_progress', 'pending_user_action', 'open')]

def who(t):
    a = t.get('assigned_to')
    return a if isinstance(a, str) else str(a)

print('===== 按窗口分组 =====')
by = {}
for t in pend:
    by.setdefault(who(t), []).append(t)
for k, v in sorted(by.items(), key=lambda x: -len(x[1])):
    print('%s: %d条' % (k, len(v)))

print()
print('===== 按任务类型 =====')
kws = Counter()
for t in pend:
    task = str(t.get('task', ''))
    if '关键词密度' in task:
        kws['关键词密度'] += 1
    elif '幻觉' in task or 'llmeval' in task.lower():
        kws['幻觉检测'] += 1
    elif 'zens' in task.lower() or '评分' in task or '质量' in task:
        kws['内容质量'] += 1
    elif 'CTR' in task or '标题' in task or 'meta' in task.lower():
        kws['CTR/标题'] += 1
    elif 'schema' in task.lower() or 'GEO' in task or 'AEO' in task:
        kws['GEO/AEO'] += 1
    elif '内链' in task or '链接' in task:
        kws['链接'] += 1
    elif '截图' in task:
        kws['截图'] += 1
    elif '外链' in task:
        kws['外链'] += 1
    elif '索引' in task:
        kws['索引'] += 1
    elif '关键词' in task:
        kws['关键词类'] += 1
    else:
        kws['其他'] += 1
for k, v in kws.most_common():
    print('%s: %d条' % (k, v))

print()
print('===== 全部任务预览 =====')
for i, t in enumerate(pend):
    print('[%s] %s | %s | %s' % (t.get('status', ''), t.get('priority', ''), who(t)[:30], str(t.get('task', ''))[:80]))
