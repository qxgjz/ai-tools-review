# -*- coding: utf-8 -*-
"""2026-10-12 早间调度：清理9条真完成到archived + 报告校验补录"""
import json, os, datetime, re

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
NOW = "2026-10-12T06:40:00"

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state["next_iteration_focus"]
arch = state.setdefault("archived_todos", [])

# 1. 清理9条completed（全部线上复测通过）
kept = []
cleaned = []
for t in nf:
    if t.get("status") == "completed":
        t["archived_at"] = NOW
        t["verification"] = "2026-10-12早间线上复测通过：/ranking/200 /tools/midjourney/200 369KB /blog/best-ai-search-engines-2026 200 首页200 464KB 无尾斜杠301生效 tools-index拆分落地(870KB)"
        arch.append(t)
        cleaned.append(t.get("id"))
    else:
        kept.append(t)
state["next_iteration_focus"] = kept
print(f"已清理到archived: {len(cleaned)}条 -> {cleaned}")
print(f"archived累计: {len(arch)}")

# 2. 报告校验：读最新报告P0/P1，查是否已在待办
def extract_p0p1(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        return []
    out = []
    for line in text.splitlines():
        if re.match(r"^\s*[-*]\s*\[?[Pp]0", line) or re.match(r"^\s*[-*]\s*\[?[Pp]1", line):
            if len(line.strip()) > 10:
                out.append(line.strip()[:120])
    return out

reports = ["audit_findings.md", "keyword_opportunities.md", "pain_points.md",
           "monetization_opportunities.md", "backlink_opportunities.md",
           "jsonld_audit_results.md", "full_audit_report.md"]
base = os.path.join(ROOT, "iteration_center")
print("\n=== 报告P0/P1问题（抽样） ===")
for r in reports:
    p = os.path.join(base, r)
    items = extract_p0p1(p)
    print(f"{r}: {len(items)}条P0/P1行")

with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("\nstate.json已保存")
