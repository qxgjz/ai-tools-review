# -*- coding: utf-8 -*-
"""2026-10-12 周走查：把学到的新方法写入state.json待办（防只写知识库不写待办）"""
import json, os, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
IC = os.path.join(ROOT, "iteration_center")
STATE = os.path.join(IC, "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)

nf = state.get("next_iteration_focus", [])
existing_ids = {t.get("id") for t in nf}
existing_tasks = {str(t.get("task", "")) for t in nf}
today = "2026-10-12"

new_todos = [
    {
        "id": "P0-PSEO-DEDUP-20261012",
        "task": "pSEO全量去重：对全部533工具页检查H1/导语/FAQ是否差异化（防止重复模板被Google判为重复内容），列表页/工具页模板需保证intro和FAQ按工具动态生成",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1", "架构师"],
        "source": "commander_weekly_review_20261012",
        "created_at": today,
    },
    {
        "id": "P1-GEO-THREE-20261012",
        "task": "GEO三要素落地到新文章：每篇评测至少3个统计数字（带命名来源+年份）+1个专家/用户直接引语（带归属）+内文出处链接（Princeton研究：统计+40%可见性、引用+115%、引语+30-40%）",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window3", "创作家"],
        "source": "commander_weekly_review_20261012",
        "created_at": today,
    },
    {
        "id": "P1-ANSWER-FIRST-20261012",
        "task": "新文章采用Answer-First 40-60字直接答案架构：正文开头/每个H2下先给40-60字直答再展开；打磨师批量打磨时检查AI可提取性（ChatGPT 93%引用来自第三方→评测必须引用真实用户评论/外部数据）",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window5", "打磨师", "window3", "创作家"],
        "source": "commander_weekly_review_20261012",
        "created_at": today,
    },
]

added = 0
for t in new_todos:
    if t["id"] in existing_ids or t["task"] in existing_tasks:
        print(f"跳过已存在: {t['id']}")
        continue
    nf.append(t)
    added += 1

state["next_iteration_focus"] = nf
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"新增待办: {added} 条")
print(f"active总数: {len(nf)}")
for t in new_todos:
    print(f"  - {t['id']} | {t['priority']} | {t['assigned_to']} | {t['task'][:50]}")
