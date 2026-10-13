#!/usr/bin/env python3
import json, os
from datetime import datetime, timezone, timedelta
JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")
PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")
OPPORTUNITIES = os.path.join(PROJECT, "iteration_center", "backlink_opportunities.md")
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)
state["completed_tasks"].append({
    "task": "拓荒者-外链增长SOP (10-12 22:00)",
    "time": now_str,
    "result": "HN未登录; tooljunction.io客座付费(最低$150)不推荐"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
with open(OPPORTUNITIES, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## tooljunction.io客座评估（{now_str}）\n\n- URL: https://www.tooljunction.io/write-for-us\n- 流量: 100K+ monthly readers\n- **预算: 最低$150-$300（付费客座）**\n- 结论: 不推荐（成本太高）\n")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 外链增长SOP（10-12 22:00，{now_str}）\n\n- HN: 未登录\n- tooljunction: 付费$150+，不推荐\n- 今日总结: hyzenpro提交成功 + 2轮调研 + 2轮跟进\n")
print(f"Done. {now_str}")
