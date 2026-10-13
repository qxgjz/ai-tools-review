#!/usr/bin/env python3
"""10-12 6点档SOP: hyzenpro提交成功!"""
import json, os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")
ACCOUNTS = os.path.join(PROJECT, "iteration_center", "accounts.md")

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

state["completed_tasks"].append({
    "task": "拓荒者-外链增长SOP (10-12 06:00)",
    "time": now_str,
    "result": "HN未登录; hyzenpro.com提交成功! 7步表单全部完成, 等编辑审核(5个工作日)",
    "hn_status": "NOT-LOGGED-IN",
    "hyzenpro": "SUBMITTED ✅ (7/7 steps: essentials/positioning/pricing/FAQs/media/about you/review)"
})

# 补录backlink跟踪
state["next_iteration_focus"].append({
    "id": f"GROWTH-HYZENPRO-CHECK-{today}",
    "priority": "P1",
    "title": "检查hyzenpro.com是否上线（提交后5个工作日内审核）",
    "description": "提交时间: 2026-10-12 06:xx, 编辑审核, 邮箱840754587@qq.com",
    "assigned_to": "拓荒者",
    "status": "pending",
    "created": now_str
})

state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# accounts.md追加
with open(ACCOUNTS, "a", encoding="utf-8") as f:
    f.write(f"""
## 16. hyzenpro.com
- URL: https://hyzenpro.com/submit-ai-tool/
- 提交时间: {now_str}
- 状态: 已提交，等编辑审核（5个工作日）
- 邮箱: 840754587@qq.com
- 免费，无需登录，编辑审核制
""")

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"""

---

## 外链增长SOP（10-12 06:00，{now_str}）

### 🎉 重大成果：hyzenpro.com提交成功！
- ✅ 7步表单全部完成
- ✅ Name: AIToolCrux
- ✅ Category: AI General Tools
- ✅ Audience: Marketers & Growth
- ✅ Pricing: Freemium/Free
- ✅ 3 FAQs
- ✅ About you: AIToolCrux Team / 840754587@qq.com
- ✅ 点击Submit for review
- ⏳ 等编辑审核（5个工作日内回复）

### 其他
- ❌ HN: 未登录
- ❌ Reddit: 未登录

### 技术总结（hyzenpro表单经验）
- JS设值不触发React验证，必须用bu.type(ref, text)
- tag-input（key features/pros/cons）需要逐个bu.type + submit=True
- starting-price用bu.type(ref, "Free")成功
- 7步表单：essentials → positioning → pricing → FAQs → media(可跳过) → about you → review
""")
print(f"Done. {now_str}")
