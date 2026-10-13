# -*- coding: utf-8 -*-
"""指挥官 2026-10-11 14:43 调度：清理completed + 补录待办 + 更新数据"""
import json, os, datetime, glob, collections

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
NOW = "2026-10-11T14:43:00"

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)

nf = state.setdefault("next_iteration_focus", [])
arch = state.setdefault("archived_todos", [])
existing_ids = {t.get("id") for t in nf}
existing_tasks_lower = {str(t.get("task","")).lower() for t in nf}

# ---------- 1. 清理 completed（7条，全部经线上验证为真完成） ----------
completed_ids = [
    "CTR-20261010-2100",   # openai_astra 新标题已上线(200)
    "CTR-20261010-2101",   # adobe-firefly 新标题已上线(200)
    "P0-CTR-001",          # creatium 真实slug 200 验证为真完成
    "P0-PERF-001",         # 首页实测恢复 0.73s/465KB/200
    "P0-GEO-002",          # GEO 整改（早前已验证）
    "CTR-20261011-000",    # CTR 标题优化
    "ux_p0_partial_recovery_72h_2026-10-11",  # 性能自愈验证完成
    "tech_faq_extract_2026-10-11",            # FAQ 提取
]
moved = []
for t in nf[:]:
    if t.get("id") in completed_ids and t.get("status") == "completed":
        t["archived_at"] = NOW
        t["archive_reason"] = "dispatch_cleanup_2026-10-11:线上验证真完成"
        arch.append(t)
        nf.remove(t)
        moved.append(t.get("id"))

# ---------- 2. 补录待办（audit_findings 未覆盖的 P0/P1 + 本轮验证新发现） ----------
def add(tid, task, prio, assign, source, detail=""):
    if tid in existing_ids:
        return False
    nf.append({
        "id": tid, "status": "pending", "priority": prio,
        "assigned_to": assign, "task": task, "source": source,
        "created_at": NOW, "detail": detail,
    })
    existing_ids.add(tid)
    return True

added = []
# 2.1 本轮线上验证新发现：无尾斜杠URL 308→404（真实流量损失风险）
if add("P0-PERF-SLASH-001",
       "修复无尾斜杠文章URL重定向异常：实测 /blog/openai_astra_review(无尾斜杠) 返回308后最终404，需确保301/308正确指向带尾斜杠URL，避免GSC已收录无尾斜杠URL流量损失",
       "P0", ["window1", "架构师"], "commander_verify_2026-10-11",
       "实测: openai_astra_review 无尾斜杠 308->404; 带尾斜杠 200 正常"):
    added.append("P0-PERF-SLASH-001")

# 2.2 SOP：窗口日志必须写真实slug
if add("P1-SOP-SLUG-001",
       "打磨师日志与state.json中的文章URL必须使用真实slug（creatium真实slug=creatium-coach-review-2025，不是creatium-coach-review），防止指挥官/其他窗口验证误判404",
       "P1", ["window5", "打磨师"], "commander_verify_2026-10-11"):
    added.append("P1-SOP-SLUG-001")

# 2.3 audit_findings 高频 P0/P1 检查补录
audit_candidates = [
    ("P1-CONTENT-FAQ-001", "6篇best-ai-*-tools列表文补FAQ+H2+结论（audit_findings P1）", "P1", ["创作家"], "audit_findings_2026-10-11"),
    ("P0-STRUCT-REDIRECT-001", "8组blog category双slug重复title需301合并（audit_findings P0）", "P0", ["window1", "架构师"], "audit_findings_2026-10-11"),
    ("P1-SEO-RICH-001", "SoftwareApplication schema补AggregateRating评分结构化数据（audit_findings P1）", "P1", ["window1", "架构师"], "audit_findings_2026-10-11"),
    ("P0-PERF-PAGESIZE-001", "约100个工具页>500KB（最大2.6MB）需图片压缩/懒加载优化（audit_findings P0）", "P0", ["window1", "架构师"], "audit_findings_2026-10-11"),
    ("P1-DATA-TOOLSJSON-001", "tools.json 8MB+解析失败，需拆分或增量加载（audit_findings P1）", "P1", ["window1", "架构师"], "audit_findings_2026-10-11"),
    ("P0-INDEX-NOINDEX-001", "215个页面noindex需排查（audit_findings P0）", "P0", ["window1", "架构师"], "audit_findings_2026-10-11"),
    ("P0-INDEX-404-001", "7个404页面需修复或301（audit_findings P0）", "P0", ["window1", "架构师"], "audit_findings_2026-10-11"),
]
for tid, task, prio, assign, source in audit_candidates:
    if add(tid, task, prio, assign, source):
        added.append(tid)

# ---------- 3. 更新关键数据 ----------
try:
    posts = json.load(open(os.path.join(ROOT, "data", "posts.json"), encoding="utf-8"))
    n_posts = len(posts) if isinstance(posts, list) else len(posts.get("posts", []))
except Exception as e:
    n_posts = f"err:{e}"
try:
    tools = json.load(open(os.path.join(ROOT, "data", "tools.json"), encoding="utf-8"))
    n_tools = len(tools) if isinstance(tools, list) else len(tools.get("tools", []))
except Exception as e:
    n_tools = f"err:{e}"
try:
    shots = glob.glob(os.path.join(ROOT, "public", "screenshots", "**", "*"), recursive=True)
    n_shots = sum(1 for s in shots if os.path.isfile(s))
except Exception as e:
    n_shots = f"err:{e}"
iter_no = state.get("iteration", 0)

# ---------- 4. 统计输出 ----------
pending = sum(1 for t in nf if t.get("status") == "pending")
inprog = sum(1 for t in nf if t.get("status") == "in_progress")
comp = sum(1 for t in nf if t.get("status") == "completed")
by_win = collections.Counter(t.get("assigned_to")[0] if isinstance(t.get("assigned_to"), list) else str(t.get("assigned_to")) for t in nf if t.get("status") != "completed")
by_prio = collections.Counter(t.get("priority") for t in nf)

with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("=== 清理结果 ===")
print("moved_to_archived:", len(moved), moved)
print("added_todos:", len(added), added)
print("=== state.json 最新 ===")
print("active:", len(nf), "pending:", pending, "in_progress:", inprog, "completed:", comp)
print("priority:", dict(by_prio))
print("pending_by_window:", dict(by_win))
print("iteration:", iter_no)
print("=== 网站关键数据 ===")
print("posts:", n_posts, "| tools:", n_tools, "| screenshots:", n_shots)
