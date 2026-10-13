# -*- coding: utf-8 -*-
"""指挥官：写入视觉质感/设计系统P0待办（解决AI廉价感）"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = datetime.date.today().isoformat()

new_todos = [
    {
        "task": "设计P0-1: 建立设计系统tokens（tailwind.config.ts）：①换掉默认蓝，用品牌色【靛紫 #6d28d9 主色 + 背景三层 #fafaf9/#f5f5f4/#e7e5e4 + 边框 #e7e5e4 + 深色 #0f172a】；②字体标题加Space Grotesk或Manrope；③统一圆角12px、双层阴影、间距8pt网格。改完跑npx tsc --noEmit提交部署。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1"],
        "source": "commander_design_system_20261009",
        "created_at": today
    },
    {
        "task": "设计P0-2: 重做首页（app/page.tsx）hero区和工具卡片组件，消除AI廉价感：①hero用克制的渐变+玻璃拟态（backdrop-blur只限hero）；②卡片靠1px边框分层，不用大模糊阴影；③大留白section padding 96px；④所有图标统一lucide。改完提交部署并截图对比前后。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1"],
        "source": "commander_design_system_20261009",
        "created_at": today
    },
    {
        "task": "设计P1-1: 体验官制定并执行《视觉质感审计清单》（对照AI廉价感检查项：默认蓝/彩虹渐变/超大圆角/卡片等大/无留白/图标混乱/多余动效），对首页+工具页+文章页三类页面逐一审计，问题写入audit_findings.md并标P0/P1。",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window6", "体验官", "ux"],
        "source": "commander_design_system_20261009",
        "created_at": today
    },
    {
        "task": "设计P1-2: 工具页/文章页应用新设计系统：工具页评分卡+文章页阅读排版（标题层级/正文行距1.75/段落间距24px/代码与表格样式）统一为高级感模板，Top10流量工具页先改。",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window1", "window6"],
        "source": "commander_design_system_20261009",
        "created_at": today
    },
]

existing_tasks = {str(t.get('task', ''))[:60] for t in focus}
added = 0
for nt in new_todos:
    if str(nt['task'])[:60] not in existing_tasks:
        focus.insert(0, nt)
        existing_tasks.add(str(nt['task'])[:60])
        added += 1

d['next_iteration_focus'] = focus
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('新增设计待办: %d 条' % added)
print('当前待办总数: %d 条' % len(focus))
print()
print('--- 新增清单 ---')
for t in new_todos:
    print('[%s] %s | %s' % (t['priority'], t['status'], t['task'][:100]))
