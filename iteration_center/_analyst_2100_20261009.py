# -*- coding: utf-8 -*-
"""分析师窗口 21:00 班次 - 2026-10-09
增量执行：自 15:00 以来无新 GSC 报告落地，网络到 Google 不通，
不重复分析，只记录状态、更新时间戳、写增量日志。
"""
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-09"
NOW = datetime.now().isoformat(timespec="seconds")

# ========== 1. 追加简短的 audit_findings（只记增量） ==========
audit_path = os.path.join(BASE, "iteration_center", "audit_findings.md")
addendum = f"""

### 21:00 班次增量复查 - {TODAY}

**与 15:00 班次对比**：
- GSC 报告目录：无新增（最新仍是 2026-09-06_2026-10-05.md，落地于 10/7）
- `.secrets/gsc-service-account.json`：已就位（2385 bytes，9/29 创建）
- 到 `oauth2.googleapis.com:443` 的 TCP 连接：**失败（False）**
- 结论：凭证配置正确，但当前网络环境无法直连 Google API，实时拉取仍被网络阻塞

**15:00 提出的 3 条待办在其他窗口执行后的状态**：
- P0-TRAFFIC-CLIFF-20260924-001：仍 pending，已被 current_todo 拆解为 P0-COMPARE-001 / P0-MOBILE-001 / P0-CTR-001（其他窗口已认领具体动作）
- P1-GA4-REBUILD-001：仍 pending（commander），凭证已下载但未授权到 GSC/GA4 属性
- P1-QUERY-FILTER-RULE-001：仍 pending（analyst 自领）

**本次新增 P2**：
- P2-GOOGLE-NETWORK-BLOCK-001：当前运行环境无法直连 Google API（TCP 443 不通）。在用户本地开启代理/VPN 之前，所有实时 GSC/GA4 拉取尝试都会超时。下次触发时先 Test-NetConnection 探测一次，通则拉实时数据，不通则跳过。
"""

with open(audit_path, "a", encoding="utf-8") as f:
    f.write(addendum)
print(f"[OK] audit_findings appended, size: {os.path.getsize(audit_path)}")

# ========== 2. 更新 state.json 时间戳和网络阻塞记录 ==========
state_path = os.path.join(BASE, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# 备份
backup = state_path + f".backup_2100_{TODAY.replace('-','')}"
with open(backup, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

state["last_analytics_run"] = f"{TODAY} 21:00 (SOP cron, network blocked - no live pull)"
state["last_updated"] = NOW

# 追加网络阻塞待办（去重）
focus = state.get("next_iteration_focus", [])
existing_ids = {x.get("id") for x in focus if isinstance(x, dict)}
new_item = {
    "id": "P2-GOOGLE-NETWORK-BLOCK-001",
    "priority": "P2",
    "title": "运行环境无法直连 Google API（TCP 443 不通），需开启代理后才能实时拉 GSC/GA4",
    "assigned_to": ["commander"],
    "status": "pending",
    "created": TODAY,
    "description": "Test-NetConnection oauth2.googleapis.com:443 = False。凭证已就位但网络不通。下次定时任务先探测，通则拉实时数据，不通则用落地报告。",
    "evidence_source": "window_logs/analyst_2026-10-09.md 21:00 section"
}
if new_item["id"] not in existing_ids:
    focus.append(new_item)
    print(f"[OK] added: {new_item['id']}")
else:
    print(f"[SKIP] already exists: {new_item['id']}")

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[OK] state.json updated, focus total: {len(focus)}")

# ========== 3. 追加日志到 window_logs/analyst_2026-10-09.md ==========
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
# 读已有内容
existing = ""
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        existing = f.read()

new_section = f"""

---

## 21:00 班次增量复查 - {NOW}

### 本次做了什么

| 步骤 | 结果 |
|---|---|
| 检查 .secrets/gsc-service-account.json | ✅ 存在（2385 bytes） |
| 检查 gsc-ga4-report 新报告 | ❌ 无新增（仍是 10/7 那份） |
| Test-NetConnection oauth2.googleapis.com:443 | ❌ False（网络不通） |
| 检查 15:00 加的 3 条待办是否还在 | ✅ 全部 pending，未被其他窗口删除 |
| 检查 current_todo 是否覆盖同一问题 | ✅ 已被拆为 P0-COMPARE-001/P0-MOBILE-001/P0-CTR-001 |
| 追加 audit_findings | ✅ +1 段增量记录 |
| 更新 state.json | ✅ last_analytics_run / last_updated / 新增 1 条 P2 |

### 关键观察

1. **不重复 15:00 的分析**——GSC 数据没有新落地，重复写同样的报告是浪费
2. **网络阻塞是新事实**——15:00 沙箱超时是沙箱问题，21:00 真实系统也超时，说明用户当前网络出不去 Google
3. **其他窗口已经在行动**——current_todo 里 6 条 P0/P1 都是针对同一流量危机的具体执行项（UX/CTR/compare/移动端/截图/QA），分析师不需要再报同样问题
4. **P1-QUERY-FILTER-RULE-001 是 analyst 自领**——下次跑关键词分析时要真正落地过滤逻辑，不能只挂 pending

### 下次触发（明天 9:00）建议

1. 先 `Test-NetConnection oauth2.googleapis.com -Port 443`
2. 如果 True：跑 `iteration_center/_test_gsc_live.py` 拉实时数据，更新报告
3. 如果 False：跳过实时拉取，只检查 gsc-ga4-report 是否有新落地文件
4. 重点观察：current_todo 里 P0-COMPARE-001 / P0-MOBILE-001 是否有进展（看其他窗口日志）

---
"""

with open(log_path, "w", encoding="utf-8") as f:
    f.write(existing.rstrip() + new_section)
print(f"[OK] log updated: {log_path}")
print("\n=== 21:00 shift DONE ===")
