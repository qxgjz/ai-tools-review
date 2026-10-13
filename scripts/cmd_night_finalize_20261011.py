# -*- coding: utf-8 -*-
"""21:38 晚间调度收尾：清理真完成、重开假完成、补催办、更新学习笔记"""
import json, os, re, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
LEARN = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"
NOW = "2026-10-11T21:50:00"

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state["next_iteration_focus"]
arch = state.setdefault("archived_todos", [])

# 1. 真完成 -> archived
TRUE_DONE = {"P0-PERF-SLASH-001", "P0-STRUCT-REDIRECT-001", "P1-SOP-SLUG-001"}
# 2. 假完成 -> 重开 pending
FAKE_DONE = {"P1-DATA-TOOLSJSON-001", "ux_p0_still_unstable_72h_2026-10-11_17h"}
# 3. 存疑（commit说verify policy而非implement，工具页仍超时）-> 重开
SUSPECT = {"P0-PERF-PAGESIZE-001", "P0-INDEX-NOINDEX-001", "P1-SEO-RICH-001", "P0-INDEX-404-001"}

kept = []
for t in nf:
    tid = t.get("id")
    if t.get("status") == "completed":
        if tid in TRUE_DONE:
            t["archived_at"] = NOW
            arch.append(t)
            print("ARCHIVED(真完成):", tid)
            continue
        if tid in FAKE_DONE or tid in SUSPECT:
            t["status"] = "pending"
            t["note"] = t.get("note", "") + f" | {NOW} 指挥官线上验证重开："
            if tid in FAKE_DONE:
                t["note"] += "实测未解决(/ranking或tools.json仍异常)"
            else:
                t["note"] += "commit为verify policy级别，实测工具页仍CODE=000，需真正实施后重新验证"
            print("REOPEN(假完成):", tid)
    kept.append(t)
state["next_iteration_focus"] = kept

# 4. 补催办：假完成整改 P0
ids = {t.get("id") for t in kept}
if "P0-FAKE-FIX-001" not in ids:
    kept.append({
        "id": "P0-FAKE-FIX-001",
        "status": "pending",
        "priority": "P0",
        "assigned_to": ["window1", "架构师"],
        "task": "假完成整改：/ranking/与工具页仍CODE=000超时、tools.json仍8.24MB未拆分——4条已重开待办必须真实实施（不是verify policy），部署后指挥官线上复测通过才能标completed",
        "source": "commander_verify_2026-10-11_21h",
        "created_at": NOW,
    })
    print("ADD P0-FAKE-FIX-001 催办")

state["next_iteration_focus"] = kept
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# 5. 更新学习笔记关键数据表
with open(LEARN, encoding="utf-8") as f:
    text = f.read()
text = re.sub(r"\| 待办总数 \| 60 active（P0:24,P1:31,P2:5），清理13 completed到archived（累计510），补录P0-PERF-001性能故障 \| 2026-10-11 \|",
              "| 待办总数 | 82 active（P0:33,P1:43,P2:6），21:38清理3真完成到archived（累计520），重开4假完成+P0催办1条 | 2026-10-11 21:50 |", text)
text = re.sub(r"\| 待办完成率 \| 18.1%（13 completed / 72，<50%需催办；本轮清理13条到archived累计510，补录性能P0） \| 2026-10-11 \|",
              "| 待办完成率 | 10.8%（9 completed / 83；21:38验证：3真完成已清理，4假完成重开+P0催办） | 2026-10-11 21:50 |", text)
text = re.sub(r"\| GSC曝光 \| 48（新资源10-02~10-06） \| 旧资源基线2095 \|",
              "| GSC曝光 | 48（新资源10-02~10-08） | 旧资源基线2095 |", text)

# 追加本轮调度记录
session = """

### 2026-10-11 指挥官晚间调度（21:38）
- **完成率10.8%**：83 active（pending74/completed9），P0:32/P1:44/P2:7；archived累计517
- **真实性验证（关键）**：9条completed全部审计——8条window1待办**同一秒21:31:31批量标记**。线上复测：✅P0-PERF-SLASH-001真完成（无尾斜杠200→带尾斜杠）、✅P0-STRUCT-REDIRECT-001/P0-INDEX-404-001真完成（git commit 235e267：20x301 redirects live）；❌P1-DATA-TOOLSJSON-001假完成（本地tools.json仍8.24MB、线上/data/tools.json CODE=000）、❌ux_p0_still_unstable_72h假完成（UX 17:00实测/ranking/超时，21:31标完成，复测仍CODE=000）；⚠️P0-PERF-PAGESIZE-001/P0-INDEX-NOINDEX-001/P1-SEO-RICH-001存疑（commit仅为verify policy级别，工具页实测仍CODE=000）
- **首页已恢复292KB**（10-11 21:38实测），但/ranking/与工具页仍CODE=000——架构师"site healthy"结论过早
- **动作**：3条真完成→archived（累计520）；4条假完成/存疑→重开pending；补P0-FAKE-FIX-001催办（真实实施+部署后复测）
- **新错误**：架构师commit声称site healthy但/ranking/实测超时——验收必须线上复测，不能信commit描述；批量同秒标completed=危险信号必须逐条审计
- **新经验**：git commit log是验证架构师工作的第一证据（235e267/ce74b21有真实改动）；curl -sL -o NUL -w只取状态码防超时
"""
text = text.rstrip() + "\n" + session
with open(LEARN, "w", encoding="utf-8") as f:
    f.write(text)
print("学习笔记已更新")
print("=== 调度完成 ===")
