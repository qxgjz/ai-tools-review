# -*- coding: utf-8 -*-
import json, datetime

path = r"iteration_center\state.json"
d = json.load(open(path, encoding="utf-8"))
nf = d.get("next_iteration_focus", [])
archived = d.get("archived_todos", [])
if not isinstance(archived, list):
    archived = []

# ---- 1) 清理 completed：6条移入 archived；GSC-BADURL-FIX-VERIFY 假完成嫌疑 → 重开 pending ----
keep = []
moved = []
for x in nf:
    if x.get("status") == "completed":
        if x.get("id") == "GSC-BADURL-FIX-VERIFY-20261012":
            # 索引监控 10-12 20:23 实测：/tools/gemini、/tools/chatgpt、/category/chat、/category/code 仍 redirect_error/redirect
            x["status"] = "pending"
            x["note"] = "假完成嫌疑：10-12 索引监控实测 4 个 redirect 坏 URL 仍在线上，需重新修复并验证（用 gsc_batch_check.py 复核）"
            keep.append(x)
        else:
            x["status"] = "archived"
            x["archived_at"] = "2026-10-12 22:00"
            archived.append(x)
            moved.append(x.get("id"))
        continue
    keep.append(x)

# ---- 2) 补录 P0 催办（完成率 6.4% < 50%） ----
def exists(prefix):
    for x in keep:
        if str(x.get("id","")).startswith(prefix):
            return True
    return False

new_todos = []
if not exists("P0-URGE-CREATOR"):
    new_todos.append({
        "id": "P0-URGE-CREATOR-20261012",
        "assigned_to": "创作家",
        "priority": "P0",
        "status": "pending",
        "task": "加快批量修复进度：创作家当前 39 条 pending（关键词/痛点/竞品选题堆积），要求每次执行消化≥5条，全部完成后逐条标记 completed 并写日志；24小时内完成率需≥50%",
        "source": "commander_daily_schedule_20261012"
    })
if not exists("P0-URGE-GROWTH"):
    new_todos.append({
        "id": "P0-URGE-GROWTH-20261012",
        "assigned_to": "window2",
        "priority": "P0",
        "status": "pending",
        "task": "加快批量修复进度：window2 增长黑客当前 38 条 pending（外链/目录/社区待办），要求每次执行消化≥5条，逐条标记 completed；外链目标从 4/15 向 15 推进",
        "source": "commander_daily_schedule_20261012"
    })
if not exists("P0-FAKE-FIX-ARCHITECT"):
    new_todos.append({
        "id": "P0-FAKE-FIX-ARCHITECT-20261012",
        "assigned_to": "架构师",
        "priority": "P0",
        "status": "pending",
        "task": "假完成整改：GSC-BADURL-FIX-VERIFY 标记 completed 但线上 /tools/gemini /tools/chatgpt /category/chat /category/code 仍为 redirect_error/redirect。立即修复 301/canonical 链，用 gsc_batch_check.py 实测复核通过后方可标记完成",
        "source": "commander_daily_schedule_20261012"
    })
new_ids = [t["id"] for t in new_todos]
keep = new_todos + keep

# ---- 3) 排序：P0 在前，其次 P1，再次 P2；同优先级按 id ----
prio = {"P0":0, "P1":1, "P2":2}
keep.sort(key=lambda x: (prio.get(x.get("priority","P2"),2), str(x.get("id",""))))

d["next_iteration_focus"] = keep
d["archived_todos"] = archived
d["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 输出统计
from collections import Counter
st = Counter(x.get("status","?") for x in keep)
print("moved to archived:", moved)
print("reopened:", ["GSC-BADURL-FIX-VERIFY-20261012"])
print("added:", new_ids)
print("after -> next_iteration_focus:", len(keep), dict(st))
print("archived total:", len(archived))
