import json, os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")
today = now.strftime("%Y-%m-%d")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LEARNING_PATH = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"

# 15个可落地知识点
takeaways = [
    "90/10规则：90%真实贡献，最多10%产品提及。安全系数取15:1或20:1",
    "25条预热规则：发任何产品前先在目标subreddit做25条无产品评论，零提及",
    "账号年龄<30天且首帖是链接=直接shadowban。先养号2-4周",
    "同一域名24h内发5+ subreddit = spamflag。每个subreddit只发一次",
    "不要跨subreddit cross-post完全相同内容，社区互相看得到",
    "标题公式：[Built/Created/Launched] [what] for [who] — [key benefit]",
    "目标subreddit：r/SaaS(weekly feedback thread)、r/indiehackers、r/startups、r/ChatGPT、r/Entrepreneur",
    "最佳发帖：周二/周三，避开周末",
    "自然提及原则：只在有人问\"有没有XX工具\"时回答，主动推销=ban",
    "透明性：说\"我做了这个评测站\"比假装第三方更安全，mod会查history",
    "优先用subreddit指定的promo thread（r/SaaS有weekly feedback）",
    "Reddit DA=91，帖子在Google排长尾词比自己网站快30-40%（parasite SEO）",
    "自动化监控：设关键词(AI tool review/best AI/AI alternative)，帖子热时(2h内)参与",
    "Alai案例：每天扫描Reddit关键词帖→Slack推送→趁热处理，获88k注册",
    "不要删负面评论，要回应批评。Reddit尊重创始人面对质疑",
]

# 落地到state.json
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

todo = state.setdefault("next_iteration_focus", [])
todos_to_add = [
    {
        "task": "Reddit养号：登录Beautiful_Smoke_2425后，先在r/SaaS/r/ChatGPT/r/Entrepreneur发25条无产品真实评论（2-4周），零提及aitoolcrux",
        "assigned_to": ["window2", "拓荒者"],
        "priority": "P0",
        "source": f"growth_learning_reddit_{today}",
        "detail": "90/10规则，25条预热，账号年龄<30天不发链接"
    },
    {
        "task": "设置Reddit关键词监控：AI tool review / best AI / AI alternative / frustrated AI / waste of money，帖子2h内参与回答",
        "assigned_to": ["window2", "拓荒者"],
        "priority": "P1",
        "source": f"growth_learning_reddit_{today}",
        "detail": "Alai案例88k注册，趁帖子热时介入"
    },
    {
        "task": "在r/SaaS weekly feedback thread自然提及aitoolcrux（透明说\"我做了个AI工具评测站\"），不硬推",
        "assigned_to": ["window2", "拓荒者"],
        "priority": "P1",
        "source": f"growth_learning_reddit_{today}",
        "detail": "用指定promo thread，周二/三发"
    },
]
todo.extend(todos_to_add)

state.setdefault("completed_tasks", []).append({
    "task": "拓荒者-增长学习(Reddit营销)",
    "time": now_str,
    "result": f"学15个知识点，3个落地待办已写入state.json"
})
state["last_updated"] = now_str

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# 写commander_learning.md
learning_md = f"""

## {now_str} — 增长学习：Reddit营销（拓荒者窗口）

**主题**: Reddit for SaaS growth（避免ban的正确打法）
**来源**: replyagent.ai, reddit-radar-marketing.com, remery.ai, avinashvagh.com, mediafa.st, getalai.com, hashmeta.com, foundationinc.co 等10+篇

### 15个核心知识点
"""
for i, t in enumerate(takeaways, 1):
    learning_md += f"{i}. {t}\n"

learning_md += f"""
### 对AIToolCrux的落地动作
1. **P0**: Reddit账号先养号2-4周，25条真实评论零提及，再发任何aitoolcrux链接
2. **P1**: 设关键词监控，帖子2h内参与（Alai案例88k注册的核心打法）
3. **P1**: 用r/SaaS weekly feedback thread自然提及，周二/三发

### 之前踩过的坑
- HN账号karma=1就发评论被spam filter删除 → 同理，Reddit新号直接推必被ban
- 之前一直卡"未登录"，登录后第一件事不是发推广，是贡献价值
"""

os.makedirs(os.path.dirname(LEARNING_PATH), exist_ok=True)
with open(LEARNING_PATH, "a", encoding="utf-8") as f:
    f.write(learning_md)

print(f"Done. 15 takeaways, 3 todos added to state.json")
print(f"Learning saved to: {LEARNING_PATH}")
