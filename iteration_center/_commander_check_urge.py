# -*- coding: utf-8 -*-
import json, datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)

todos = data.get('next_iteration_focus', [])

# 1. 检查是否已有"加快批量修复进度"催办
has_urge = any('URGE' in t.get('id', '') or '催' in t.get('title', '') for t in todos)
print('已有催办待办:', has_urge)

# 2. 统计完成率
pending = [t for t in todos if t.get('status') in ('pending', 'in_progress', 'pending_user_action')]
completed = [t for t in todos if t.get('status') == 'completed']
rate = 0 if not completed else round(len(completed) / (len(pending) + len(completed)) * 100, 1)
print(f'完成率: {rate}% (pending {len(pending)} / completed {len(completed)})')

# 3. 按窗口统计今日日志情况（手动检查）
print('今日(10-09)有日志的窗口: 体验官(ux)、分析师(analyst)')
print('无日志窗口: 架构师(window1)、创作家(window2)、打磨师(window3)、拓荒者(window5)')
