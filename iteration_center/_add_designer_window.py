# -*- coding: utf-8 -*-
"""指挥官：新增窗口7=设计师（视觉质感/设计系统），收拢设计待办"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = datetime.date.today().isoformat()

# 1) 新增窗口角色定义（供所有窗口识别）
d['window_roles'] = {
    "window1": "架构师-全栈技术修复",
    "window2": "增长黑客-外链建设",
    "window3": "内容生产",
    "window4": "数据分析师",
    "window5": "创作家-文章写作",
    "window6": "体验官-UX转化优化",
    "window7": "设计师-视觉质感/设计系统/避免AI廉价感",
    "polisher": "打磨师-内容精修",
    "analyst": "分析师-关键词挖掘",
    "拓荒者": "痛点挖掘",
    "指挥官": "战略调度"
}

# 2) 把设计相关待办统一分配给 window7
changed = 0
for t in focus:
    task = str(t.get('task', ''))
    if task.startswith('设计'):
        t['assigned_to'] = ['window7', '设计师']
        t['updated_at'] = today
        changed += 1

d['next_iteration_focus'] = focus
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('设计待办重新分配: %d 条 → window7设计师' % changed)
print('window_roles 已写入: 11个角色')
print()
for t in focus:
    task = str(t.get('task', ''))
    if task.startswith('设计'):
        print('[%s] %s | assigned=%s' % (t.get('priority',''), task[:55], t.get('assigned_to')))
