# -*- coding: utf-8 -*-
"""指挥官每日调度：清理空待办 + 补录状态更新催办 + 记录经验"""
import json, os, datetime

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p = os.path.join(base, 'iteration_center', 'state.json')
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = '2026-10-09'

# 1) 清理空待办（task为空）
before = len(focus)
focus = [t for t in focus if str(t.get('task', '')).strip()]
removed = before - len(focus)

# 2) 补录P0催办：窗口干活必须更新state.json状态（今天9个日志但0 completed）
new_todos = [
    {
        "task": "🔴P0状态更新铁律：今天（10-09）各窗口有日志产出但state.json完成率仍0%——所有窗口完成任务后必须立即把state.json对应待办status改为completed，禁止只写日志不更新状态。窗口2/创作家/打磨师/体验官/分析师本周起每次执行完必须同步state.json。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["all_windows"],
        "source": "commander_daily_schedule_2026-10-09",
        "created_at": today
    },
    {
        "task": "6条关键词P0文章（best ai agents 2026/ai agent vs chatbot/how to build an ai agent/best ai comparison tools/best ai voice changer/suno alternatives 2026）已在state.json标记open（创作家认领中），必须在3天内完成并标记completed，完成后用zens-ink content_qc验证分数>=70。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window5", "创作家"],
        "source": "commander_daily_schedule_2026-10-09",
        "created_at": today
    },
    {
        "task": "收录P0-2（IndexNow批量提交Top50无曝光工具页）已挂3天未执行，架构师窗口本周内必须执行submit_indexnow_daily.py并标记completed，这是收录上不去的最大瓶颈（397页已发现未索引）。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1", "架构师"],
        "source": "commander_daily_schedule_2026-10-09",
        "created_at": today
    }
]
focus = new_todos + focus
d['next_iteration_focus'] = focus

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('清理空待办:', removed, '条')
print('补录P0待办:', len(new_todos), '条')
print('当前待办总数:', len(focus))

# 3) 更新commander_learning.md关键数据表
lp = r'C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md'
txt = open(lp, encoding='utf-8').read()

new_data_rows = """| 文章总数 | 146 | 2026-10-09 |
| 工具总数 | 533 | 2026-10-09 |
| 真实截图数 | 119（public/screenshots递归统计） | 2026-10-09 |
| 待办总数 | 41（P0:18, P1:23；0 completed，完成率0%→已补录3条P0催办） | 2026-10-09 |
| 待办完成率 | 0%（窗口干活不更新状态=最大问题） | 2026-10-09 |
| 迭代轮次 | 62（completed） | 2026-10-09 |"""

# 替换旧数据行（从文章总数到迭代轮次附近）
import re
txt = re.sub(r'\| 文章总数 \|.*?\n\| 工具总数 \|.*?\n\| 真实截图数 \|.*?\n\| 待办总数 \|.*?\n\| 待办完成率 \|.*?\n\| 迭代轮次 \|.*?\n', new_data_rows + '\n', txt, flags=re.S)

open(lp, 'w', encoding='utf-8').write(txt)
print('commander_learning.md 关键数据已更新')
