# -*- coding: utf-8 -*-
import json
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
print('=== state.json 当前待办中 索引/收录相关 ===')
for t in focus:
    task = str(t.get('task', ''))
    if any(k in task for k in ['索引', '收录', 'sitemap', 'noindex', '404', '重定向', 'canonical', '规范']):
        print('[%s] %s | %s' % (t.get('priority', ''), t.get('status', ''), task[:120]))
print()
print('=== archived 中索引相关处理记录 ===')
arch = d.get('archived_todos', [])
cnt = 0
for t in arch:
    if not isinstance(t, dict):
        continue
    task = str(t.get('task', ''))
    if any(k in task for k in ['索引', '收录', 'sitemap', 'noindex', '404', '重定向', 'canonical', '规范', 'indexnow', 'IndexNow']):
        print('[%s] %s | %s' % (t.get('priority', ''), t.get('archived_at', ''), task[:110]))
        cnt += 1
        if cnt >= 30:
            break
print('共找到 %d 条' % cnt)
