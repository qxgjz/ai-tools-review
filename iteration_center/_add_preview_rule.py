# -*- coding: utf-8 -*-
"""指挥官：设计待办加入'先本地预览截图确认，再部署'要求"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = datetime.date.today().isoformat()

cnt = 0
for t in focus:
    task = str(t.get('task', ''))
    if task.startswith('设计') and '预览' not in task:
        # 在结尾追加预览确认要求
        t['task'] = task.rstrip('。') + '。🔴部署铁律：改完先 npm run dev 本地起服务截图给用户确认效果，用户说"可以"才 push 上线，未确认禁止部署。'
        t['updated_at'] = today
        cnt += 1

d['next_iteration_focus'] = focus
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('已加入预览确认要求的设计待办: %d 条' % cnt)
for t in focus:
    if str(t.get('task','')).startswith('设计'):
        print('[%s] %s' % (t.get('priority',''), str(t.get('task',''))[:45]))
