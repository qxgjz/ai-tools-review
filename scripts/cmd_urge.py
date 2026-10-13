# -*- coding: utf-8 -*-
# 1) 更新旧的14.1%催办为18.1% 2) 补创作家无日志产出催办
import json, os

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sp = os.path.join(base, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    data = json.load(f)
focus = data.get('next_iteration_focus', [])

# 1) 更新旧催办
old_text = '待办完成率14.1%远低于50%'
new_text = '待办完成率18.1%仍远低于50%'
for t in focus:
    if old_text in str(t.get('task', '')):
        t['task'] = str(t['task']).replace(old_text, new_text).replace('创作家(22条)和打磨师(21条)', '创作家(28条)和打磨师(2条)')
        t['priority'] = 'P0'
        print('✅ 更新旧催办: {}'.format(str(t['task'])[:80]))

# 2) 补创作家催办（无执行日志）
exists = any('创作家' in str(t.get('task', '')) and '无日志' in str(t.get('task', '')) for t in focus)
if not exists:
    focus.append({
        'id': 'P0-W2-URGENT-001',
        'status': 'pending',
        'priority': 'P0',
        'assigned_to': ['window2', '创作家'],
        'task': 'P0-W2-URGENT-001: 创作家28条pending待办但10-09~10-11无任何执行日志（window_logs无创作家新产出）——立即批量执行：每次触发至少完成5条文章写作/改写（现有6条关键词P0文章+批量关键词待办），完成后立即在state.json标记completed，禁止一次只修2-3条',
        'source': 'commander_daily_20261011',
        'created': '2026-10-11'
    })
    print('✅ 已补录创作家催办 P0-W2-URGENT-001')

data['next_iteration_focus'] = focus
with open(sp, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('✅ state.json 已更新，active={}'.format(len(focus)))
