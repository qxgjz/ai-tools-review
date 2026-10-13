# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-12"
NOW = datetime.now().isoformat(timespec="seconds")

state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))

# 5 个选题（来自 futurepedia sitemap 竞品分析）
topics = [
    {
        "id": f"COMP-{TODAY.replace('-','')}-01",
        "task": "竞品 futurepedia 有 ai-agents 分类，我们 0 篇。建议写: Best AI Agents 2026: Tested & Compared (6维度实测), slug: /blog/best-ai-agents-2026",
        "assigned_to": ["window2", "创作家"],
        "priority": "P0",
        "status": "pending",
        "source": "competitor_gap_futurepedia",
        "competitor_category": "ai-agents",
        "our_count": 0,
        "competitor_count": 1,
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-02",
        "task": "竞品 futurepedia 有 prompt-generators 分类，我们 0 篇。建议写: Best Prompt Generators 2026: Save Time and Get Better AI Output, slug: /blog/best-prompt-generators-2026",
        "assigned_to": ["window2", "创作家"],
        "priority": "P1",
        "status": "pending",
        "source": "competitor_gap_futurepedia",
        "competitor_category": "prompt-generators",
        "our_count": 0,
        "competitor_count": 1,
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-03",
        "task": "竞品 futurepedia 有 ai-detection 分类，我们 0 篇。建议写: AI Detectors That Actually Work in 2026 (Tested with Real Content), slug: /blog/best-ai-detectors-2026",
        "assigned_to": ["window2", "创作家"],
        "priority": "P1",
        "status": "pending",
        "source": "competitor_gap_futurepedia",
        "competitor_category": "ai-detection",
        "our_count": 0,
        "competitor_count": 1,
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-04",
        "task": "竞品 futurepedia 有 code-assistant 分类，我们 0 篇。建议写: AI Coding Tools in 2026: Cursor vs Copilot vs Windsurf Compared, slug: /blog/best-ai-coding-tools-2026",
        "assigned_to": ["window2", "创作家"],
        "priority": "P1",
        "status": "pending",
        "source": "competitor_gap_futurepedia",
        "competitor_category": "code-assistant",
        "our_count": 0,
        "competitor_count": 1,
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-05",
        "task": "竞品 futurepedia 有 no-code 分类，我们 0 篇。建议写: No-Code AI Tools That Actually Work in 2026 (Build Apps Without Coding), slug: /blog/best-no-code-ai-tools-2026",
        "assigned_to": ["window2", "创作家"],
        "priority": "P2",
        "status": "pending",
        "source": "competitor_gap_futurepedia",
        "competitor_category": "no-code",
        "our_count": 0,
        "competitor_count": 1,
        "created_at": NOW,
    },
]

# 去重检查
existing_tasks = [t.get("task", "") for t in state["next_iteration_focus"]]
added = 0
for t in topics:
    if t["task"] in existing_tasks:
        print(f"[SKIP] {t['id']}")
        continue
    state["next_iteration_focus"].append(t)
    added += 1
    print(f"[ADD] {t['id']}: {t['priority']}")

json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nTotal added: {added}")
print(f"Total todos in state.json: {len(state['next_iteration_focus'])}")
