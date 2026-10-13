# -*- coding: utf-8 -*-
"""指挥官：将设计待办升级为真实调研标准版（来源：shadcn/ui/Linear/Vercel/Stripe/Awwwards解剖）"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = datetime.date.today().isoformat()

# 真实案例提炼的设计标准（来源URL附在source）
standard = {
    'colors': '背景三层：主#ffffff→#fafafa→#f4f4f5（Linear/Vercel分层）；文字层级 rgba(0,0,0,0.90/0.60/0.45)；边框 rgba(0,0,0,0.08) hover 0.12（Vercel shadow-as-border）；强调色不用纯primary用混合色#5E6AD2蓝紫（Linear）/或#6d28d9；状态色：done#10B981/progress#F59E0B/cancel#EF4444/todo#3B82F6',
    'type': '标题Inter Display或Space Grotesk（负字距-0.5~-2.4px，Vercel Geist模式）；正文Inter 16px line-height1.5；显示级80-120px line-height0.9；权重只用400/500/600三级不用700+',
    'space': '8pt网格；section padding 80-120px（Vercel留白哲学）；卡片gap精确16px或24px；bento大卡内部padding更多；max-width 1200px',
    'radius_shadow': '圆角统一8-12px（shadcn默认--radius:0.5rem）；阴影即边框 box-shadow 0 0 0 1px rgba(0,0,0,0.08)；多层阴影栈=边框+悬浮+环境光三层',
    'motion': '时长100ms微反馈/150ms标准/250ms页面过渡（Linear）；easing cubic-bezier(0.16,1,0.3,1)；spotlight hover效果（Linear/Vercel）',
    'bento': '每section最多4-8卡（超过则无重点）；非对称bento 2×2大卡表达"从这里开始"；间隙精确16/24px',
    'trust': 'hero放真实产品UI截图不是插画（designkey：2026顶级SaaS共识）；标题≤12词；logo墙monochrome 40-60%透明度；真实截图+1.2x放大让字可读',
    'noise': '4% SVG噪点 mix-blend-mode:overlay（thegrain：让背景有物质感，AI平涂廉价感解药）',
}

new_todos = [
    {
        "task": "设计P0-1: 按真实调研标准建设计系统tokens（tailwind.config.ts）。色彩：背景三层#ffffff→#fafafa→#f4f4f5、文字rgba(0,0,0,0.90/0.60/0.45)、边框rgba(0,0,0,0.08)/hover 0.12、强调色#5E6AD2蓝紫（Linear）、状态色done#10B981/progress#F59E0B/cancel#EF4444/todo#3B82F6。字体：标题Space Grotesk负字距-0.5~-2.4px、正文Inter 16px行高1.5、权重400/500/600三级。圆角8-12px、阴影即边框、间距8pt网格、section padding 80-120px。改完跑npx tsc --noEmit提交部署。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1"],
        "source": "commander_design_research_20261009 (Linear/Vercel/shadcn真实解剖)",
        "created_at": today
    },
    {
        "task": "设计P0-2: 重做首页hero+工具卡片（app/page.tsx）：①hero用真实工具UI截图（1.2x放大）替代抽象插画（designkey规则）；②标题≤12词；③卡片用1px边框分层+bento非对称布局（2×2大卡为首选推荐），每section 4-8卡；④4%SVG噪点overlay消除AI平涂感；⑤section padding 80-120px大留白。提交部署并截图对比。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1"],
        "source": "commander_design_research_20261009 (Linear/Stripe/Vercel真实解剖)",
        "created_at": today
    },
    {
        "task": "设计P1-1: 体验官按真实标准制定《视觉质感审计清单》并执行：对照①默认蓝/纯primary色（Linear#5E6AD2标准）②无噪点无质感③卡片等大无bento层级④无留白（section<80px）⑤图标不统一⑥动效时长不标准（应100/150/250ms）⑦标题字距未收紧，逐页审计首页/工具页/文章页，输出P0/P1问题到audit_findings.md。",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window6", "体验官", "ux"],
        "source": "commander_design_research_20261009 (thegrain/designkey真实解剖)",
        "created_at": today
    },
    {
        "task": "设计P1-2: 工具页评分卡+文章页排版按标准统一：正文16px行高1.5、标题Inter Display/Space Grotesk、代码块/表格/引用统一样式、工具评分卡用状态色（done绿/progress琥珀）+8-12px圆角+1px边框，Top10流量工具页先改。",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window1", "window6"],
        "source": "commander_design_research_20261009 (Linear/shadcn真实解剖)",
        "created_at": today
    },
]

# 替换旧的4条设计待办（source以commander_design_system开头的）
remaining = []
for t in focus:
    src = str(t.get('source', ''))
    if src.startswith('commander_design_system_'):
        continue
    remaining.append(t)

existing_tasks = {str(t.get('task', ''))[:60] for t in remaining}
added = 0
for nt in new_todos:
    if str(nt['task'])[:60] not in existing_tasks:
        remaining.insert(0, nt)
        existing_tasks.add(str(nt['task'])[:60])
        added += 1

d['next_iteration_focus'] = remaining
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('替换旧设计待办: 4条，新增标准版: %d 条' % added)
print('当前待办总数: %d 条' % len(remaining))
