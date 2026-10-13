# -*- coding: utf-8 -*-
"""指挥官：设计P0-1升级为完整接入shadcn/ui体系（60k stars高星工具，禁止手写重复组件）"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = datetime.date.today().isoformat()

new_task = {
    "task": "设计P0-1(升级版): 完整接入shadcn/ui体系（https://ui.shadcn.com 60k stars，禁止手写重复组件）。①初始化components.json（npx shadcn init，目录指向components/）；②globals.css按shadcn CSS变量主题体系重写：--background/--foreground/--card/--border/--primary/--radius，把design_standard色板映射进去（背景三层#ffffff/#fafafa/#f4f4f5、强调色#5E6AD2、边框rgba(0,0,0,0.08)、圆角8-12px）；③npx shadcn add按需补组件（input/select/separator/tooltip等页面缺的）；④页面里自写的重复组件（components/layout、components/content等）优先替换为已有shadcn组件（card/button/badge/tabs/table/accordion/progress），不重复造轮子；⑤改完跑npx tsc --noEmit提交部署，截图对比。",
    "priority": "P0",
    "status": "pending",
    "assigned_to": ["window7", "设计师"],
    "source": "commander_design_research_20261009 (shadcn/ui 60k+ stars完整接入)",
    "created_at": today
}

replaced = False
out = []
for t in focus:
    if str(t.get('task','')).startswith('设计P0-1'):
        out.append(new_task)
        replaced = True
    else:
        out.append(t)

if not replaced:
    out.insert(0, new_task)

d['next_iteration_focus'] = out
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('设计P0-1已升级为shadcn/ui完整接入版: %s' % replaced)
print('待办总数:', len(out))
