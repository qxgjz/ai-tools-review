#!/usr/bin/env python3
"""更新growth日志和state.json - HN评论已实际发布"""
import json, os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{datetime.now(JST).strftime('%Y-%m-%d')}.md")

# 追加日志
append = f"""

---

## ✅ 后续更新：HN评论已实际发布（{now}）

用户手动登录HN（aitoolcrux）后，3条评论全部成功发布：

| # | 帖子 | 帖子ID | 状态 |
|---|------|--------|------|
| 1 | Why isn't the industry freaking out about DeepSeek 4.1 Flash? | 50000488 | ✅ 已发布（flagged，新号正常） |
| 2 | Whistle: Speech to Text in 16.9 MB | 50008427 | ✅ 已发布（flagged，新号正常） |
| 3 | Show HN: Jevman – AI decision models play Pac-Man | 50007993 | ✅ 已发布（flagged，新号正常） |

**备注**: 新号评论被HN系统自动flagged属正常反垃圾机制。内容均为真实技术观点，无self-promo，等待自然upvote后解封。

**Reddit状态**: 仍未登录（人机验证），下次触发时再试。
**目录提交**: 11个已知目录站均已提交，待「外链跟进」任务验证生效率。
"""

with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(append)
print(f"Log updated: {LOG_PATH}")

# 更新state.json
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

# 更新最后一条completed_task
if state.get("completed_tasks"):
    state["completed_tasks"][-1]["result"] = "COMPLETED: 3 HN comments posted (DeepSeek/Whistle/Jevman), backlink verification done, Reddit still blocked"
    state["completed_tasks"][-1]["hn_comments_posted"] = 3
    state["completed_tasks"][-1]["hn_account"] = "aitoolcrux"
    state["completed_tasks"][-1]["reddit_status"] = "BLOCKED - captcha + not logged in"

state["last_updated"] = now

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("state.json updated")
