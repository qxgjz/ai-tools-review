# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-13"
NOW = datetime.now().isoformat(timespec="seconds")

state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))

topics = [
    {
        "id": f"COMP-{TODAY.replace('-','')}-01",
        "task": "竞品 futurepedia 有 ai-detection 分类（1 个分类页），我们 0 篇。建议写: Best AI Detectors 2026: Tested for Accuracy & False Positives, slug: /blog/best-ai-detectors-2026, SERP竞争度=High",
        "assigned_to": ["window2", "创作家"],
        "priority": "P1",
        "status": "pending",
        "source": "competitor_analysis_2026-10-13",
        "data_verified": True,
        "competitor_count": 1,
        "our_count": 0,
        "competitor": "futurepedia.io",
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-02",
        "task": "竞品 futurepedia 有 prompt-generators 分类（1 个分类页），我们 0 篇。建议写: Best Prompt Generators 2026: Free vs Paid Compared, slug: /blog/best-prompt-generators-2026, SERP竞争度=Medium",
        "assigned_to": ["window2", "创作家"],
        "priority": "P1",
        "status": "pending",
        "source": "competitor_analysis_2026-10-13",
        "data_verified": True,
        "competitor_count": 1,
        "our_count": 0,
        "competitor": "futurepedia.io",
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-03",
        "task": "竞品 futurepedia 有 no-code 分类（1 个分类页）+ topai.tools 有相关内容，我们 0 篇。建议写: Best No-Code AI Tools 2026: Build Apps Without Coding, slug: /blog/best-no-code-ai-tools-2026, SERP竞争度=Medium",
        "assigned_to": ["window2", "创作家"],
        "priority": "P1",
        "status": "pending",
        "source": "competitor_analysis_2026-10-13",
        "data_verified": True,
        "competitor_count": 2,
        "our_count": 0,
        "competitor": "futurepedia.io + topai.tools",
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-04",
        "task": "竞品 futurepedia 有 transcriber 分类（1 个分类页），我们 0 篇。建议写: Best AI Transcription Tools 2026: Tested for Accuracy, slug: /blog/best-ai-transcription-tools-2026, SERP竞争度=High",
        "assigned_to": ["window2", "创作家"],
        "priority": "P2",
        "status": "pending",
        "source": "competitor_analysis_2026-10-13",
        "data_verified": True,
        "competitor_count": 1,
        "our_count": 0,
        "competitor": "futurepedia.io",
        "created_at": NOW,
    },
    {
        "id": f"COMP-{TODAY.replace('-','')}-05",
        "task": "竞品 futurepedia 有 stock-trading 分类（1 个分类页），我们 0 篇。建议写: AI Stock Trading Bots 2026: What Actually Works (With Risk Warnings), slug: /blog/best-ai-stock-trading-bots-2026, SERP竞争度=High",
        "assigned_to": ["window2", "创作家"],
        "priority": "P2",
        "status": "pending",
        "source": "competitor_analysis_2026-10-13",
        "data_verified": True,
        "competitor_count": 1,
        "our_count": 0,
        "competitor": "futurepedia.io",
        "created_at": NOW,
    },
]

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
print(f"Total todos: {len(state['next_iteration_focus'])}")
