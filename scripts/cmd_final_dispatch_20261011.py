# -*- coding: utf-8 -*-
"""最终调度动作：补ux待办 + 更新30天目标进度到学习笔记"""
import json, os, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
LEARN = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"
NOW = "2026-10-11T14:50:00"

# ---------- 1. 补 ux 待办（ux 当前 0 条，闲置） ----------
with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.setdefault("next_iteration_focus", [])
existing_ids = {t.get("id") for t in nf}
if "P1-UX-PERF-MONITOR-001" not in existing_ids:
    nf.append({
        "id": "P1-UX-PERF-MONITOR-001",
        "status": "pending",
        "priority": "P1",
        "assigned_to": ["ux", "体验官"],
        "task": "全站性能巡检并更新 health_report：实测首页/排行页/Blog页 TTFB与体积，复查工具页>500KB清单（与P0-PERF-PAGESIZE-001配合做验收验证），输出Core Web Vitals基线",
        "source": "commander_dispatch_2026-10-11",
        "created_at": NOW,
    })
    print("已补 ux 待办 P1-UX-PERF-MONITOR-001")
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# ---------- 2. 更新 30 天目标进度到学习笔记 ----------
with open(LEARN, encoding="utf-8") as f:
    text = f.read()

goal_block = """## 30天目标进度（2026-10-11 14:50 更新）
| 目标 | 基线 | 当前 | 进度 | 状态 |
|------|------|------|------|------|
| A. GSC曝光 | 2095 | 48（新资源10-02~10-08窗口） | 2.3%（vs新资源窗口）/ 旧资源基线2095 | 🔴 差距巨大 |
| B. 日均UV | 5 | GA4 1830 sessions但96%Bot污染，真实UV不可靠 | 无法评估 | 🔴 需用户切新property 549695344 |
| C. 联盟收入 | $0 | 无联盟数据 | 0% | 🔴 未开始 |

**本轮调度结论（2026-10-11）**：
- 完成率：清理前 9.5%（pending 67/completed 7）→ 清理后 active 76 全 pending
- 线上验证：3篇CTR优化全部真完成（openai_astra/adobe-firefly/creatium-coach-review-2025 均200+新标题上线），此前疑假完成为URL验证方法错误
- 新增待办9条：P0-PERF-SLASH-001（无尾斜杠308→404）、P1-SOP-SLUG-001（日志写真实slug）、audit_findings补录7条
- 负载：window2=34(P0=14) 创作家=33 最重，ux=0 已补活
"""
# 替换旧的30天目标区块（如果有），否则追加
import re
if "## 30天目标进度" in text:
    text = re.sub(r"## 30天目标进度.*?(?=\n## |\Z)", goal_block + "\n", text, flags=re.S)
else:
    text = text.rstrip() + "\n\n" + goal_block

with open(LEARN, "w", encoding="utf-8") as f:
    f.write(text)
print("30天目标进度已写入学习笔记")
print("全部调度动作完成")
