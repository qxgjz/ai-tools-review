# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-13"
NOW = datetime.now().isoformat(timespec="seconds")

state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))

# CTR 优化待办
ctr_todos = [
    {
        "id": f"CTR-{TODAY.replace('-','')}-01",
        "task": "页面 https://www.aitoolcrux.com/blog/adobe-firefly-review-2026 排名 5.2 但 CTR 仅 0.0%（26次曝光），优化 title/meta description 提升点击率",
        "assigned_to": ["window5", "打磨师"],
        "priority": "P0",
        "status": "pending",
        "source": f"ctr_optimization_{TODAY}",
        "url": "https://www.aitoolcrux.com/blog/adobe-firefly-review-2026",
        "position": 5.2,
        "ctr": 0.0,
        "impressions": 26,
        "created_at": NOW,
    },
    {
        "id": f"CTR-{TODAY.replace('-','')}-02",
        "task": "页面 https://www.aitoolcrux.com/blog/article-api-20260903-171438-creatium-coach-review-2025-is-this-ai-content-coach-worth-your-time-md 排名 6.3 但 CTR 仅 0.0%（20次曝光），优化 title/meta description 提升点击率",
        "assigned_to": ["window5", "打磨师"],
        "priority": "P0",
        "status": "pending",
        "source": f"ctr_optimization_{TODAY}",
        "url": "https://www.aitoolcrux.com/blog/article-api-20260903-171438-creatium-coach-review-2025-is-this-ai-content-coach-worth-your-time-md",
        "position": 6.3,
        "ctr": 0.0,
        "impressions": 20,
        "created_at": NOW,
    },
    {
        "id": f"CTR-{TODAY.replace('-','')}-03",
        "task": "页面 https://www.aitoolcrux.com/blog/best-ai-voice-changers-2026 排名 16.5 但 CTR 仅 2.9%（68次曝光），优化 title/meta description 提升点击率",
        "assigned_to": ["window5", "打磨师"],
        "priority": "P1",
        "status": "pending",
        "source": f"ctr_optimization_{TODAY}",
        "url": "https://www.aitoolcrux.com/blog/best-ai-voice-changers-2026",
        "position": 16.5,
        "ctr": 2.9,
        "impressions": 68,
        "created_at": NOW,
    },
    {
        "id": f"CTR-{TODAY.replace('-','')}-04",
        "task": "页面 https://www.aitoolcrux.com/blog/article-api-20260903-173210-elevenlabs-review-2026-is-it-still-the-most-human-like-ai-voice-generator-md 排名 5.6 但 CTR 仅 0.0%（5次曝光），优化 title/meta description 提升点击率",
        "assigned_to": ["window5", "打磨师"],
        "priority": "P1",
        "status": "pending",
        "source": f"ctr_optimization_{TODAY}",
        "url": "https://www.aitoolcrux.com/blog/article-api-20260903-173210-elevenlabs-review-2026-is-it-still-the-most-human-like-ai-voice-generator-md",
        "position": 5.6,
        "ctr": 0.0,
        "impressions": 5,
        "created_at": NOW,
    },
]

existing_tasks = [t.get("task", "") for t in state["next_iteration_focus"]]
added = 0
for t in ctr_todos:
    if t["task"] in existing_tasks:
        print(f"[SKIP] {t['id']}")
        continue
    state["next_iteration_focus"].append(t)
    added += 1
    print(f"[ADD] {t['id']}: {t['priority']} - pos={t['position']} ctr={t['ctr']}%")

json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nTotal added: {added}")
print(f"Total todos: {len(state['next_iteration_focus'])}")
