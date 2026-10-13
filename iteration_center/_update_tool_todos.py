# -*- coding: utf-8 -*-
import json, os
state_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = state.get("next_iteration_focus", [])
new_todos = [
    {
        "id": "P0-TOOL-FIX-001",
        "task": "工具链大修复已完成：16/17工具真实可用。各窗口必须真正调用工具执行，禁止回退AI硬写。每次执行前先import验证工具可用。",
        "assigned_to": "all_windows",
        "priority": "P0",
        "status": "pending",
        "source": "commander_tool_audit_2026-10-09",
        "created_at": "2026-10-09"
    },
    {
        "id": "P0-TOOL-CRAWL4AI-001",
        "task": "Crawl4AI因Windows长路径装不上。用trafilatura+requests替代做网页正文提取，JS渲染用playwright。不要在脚本里import crawl4ai。",
        "assigned_to": "architect",
        "priority": "P0",
        "status": "pending",
        "source": "commander_tool_audit_2026-10-09",
        "created_at": "2026-10-09"
    },
    {
        "id": "P1-TOOL-LLMEVALKIT-001",
        "task": "打磨师：用scripts/llmevalkit_toolkit.py对已发布文章做全量幻觉检测+内容评分，<70分的标记重写。context必须用全文，不能用前1/3（已修复误报）。",
        "assigned_to": "polisher",
        "priority": "P1",
        "status": "pending",
        "source": "commander_tool_audit_2026-10-09",
        "created_at": "2026-10-09"
    },
    {
        "id": "P1-TOOL-LIGHTHOUSE-001",
        "task": "体验官：用npx lighthouse对首页+3个工具页做性能/SEO/可访问性审计，输出报告，Performance<70的P0修复。",
        "assigned_to": "ux",
        "priority": "P1",
        "status": "pending",
        "source": "commander_tool_audit_2026-10-09",
        "created_at": "2026-10-09"
    },
    {
        "id": "P1-TOOL-OPENSERP-001",
        "task": "分析师：用openserp批量查询Top50关键词的真实排名（Google），对比GSC数据，找出排名虚高/虚低的页面。",
        "assigned_to": "analyst",
        "priority": "P1",
        "status": "pending",
        "source": "commander_tool_audit_2026-10-09",
        "created_at": "2026-10-09"
    }
]

existing_ids = {t.get("id") for t in todos}
added = 0
for t in new_todos:
    if t["id"] not in existing_ids:
        todos.insert(0, t)
        added += 1

state["next_iteration_focus"] = todos
state["last_tool_audit"] = "2026-10-09"
state["tool_audit_result"] = "18 tools available, 1 unavailable (Crawl4AI, trafilatura替代)"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"已添加 {added} 条待办")
print(f"当前待办总数: {len(todos)}")
