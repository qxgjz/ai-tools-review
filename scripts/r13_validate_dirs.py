import json, os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")

# R13目录实际验证结果
results = [
    ("gptbot.io/submit-ai-tool", "❌ $39付费快速通道，跳过"),
    ("bestofai.io/submit", "❌ 需Google登录（用户跳过）"),
    ("ai-hunter.io/submit-a-tool", "❌ SSL证书错误，无法访问"),
    ("insidr.ai/submit-tools", "⚠️ 表单已填（message/link/category），但提交后无success反馈，可能已提交待审"),
    ("tipseason.com/ai-tools/submit-free", "❌ 表单缺website URL字段，需注册登录"),
    ("agentic.ai/submit", "❌ 需vendor account注册，可mailto:hello@agentic.ai"),
]

with open(STATE_PATH, "r", encoding="utf-8") as fh:
    state = json.load(fh)

state.setdefault("completed_tasks", []).append({
    "task": "拓荒者-R13免注册目录实际提交验证",
    "time": now_str,
    "result": "6个目录全部有门槛：gptbot($39付费)/bestofai(Google登录)/ai-hunter(SSL错误)/insidr(已填待确认)/tipseason(缺URL需登录)/agentic(需vendor注册)。无1个真正免注册即时审核。R13'免注册目录'标签需修正。"
})

# 补录待办：发邮件给agentic.ai和insidr确认
todo = state.setdefault("next_iteration_focus", [])
todo.append({
    "task": "发邮件给hello@agentic.ai提交aitoolcrux（mailto方式）；发邮件确认insidr.ai提交是否成功",
    "assigned_to": "拓荒者", "priority": "P1",
    "source": f"r13_dir_validation_{today}"
})

state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as fh:
    json.dump(state, fh, ensure_ascii=False, indent=2)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as fh:
    fh.write(f"""
## 06:00档 R13目录实际提交验证 ({now_str})

| 目录 | 验证结果 |
|------|---------|
""")
    for name, res in results:
        fh.write(f"| {name} | {res} |\n")
    fh.write(f"""
**结论**：R13调研标记的"免注册目录"实际全部有门槛，无1个真正免注册即时审核。
- insidr.ai表单已填写（message/link/category），但无success反馈，待观察是否上线
- agentic.ai可通过mailto:hello@agentic.ai提交
- 其他4个均不适合立即提交
""")

print("Done. state.json and log updated.")
