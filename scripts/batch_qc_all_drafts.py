# -*- coding: utf-8 -*-
"""全量质检：遍历 content_drafts/*.md，用 LMEvalKit 批量评估，写报告+state.json"""
import os, sys, json, re
from pathlib import Path
from datetime import datetime

ROOT = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from scripts.llmevalkit_toolkit import LMEvalKit

# keyword 映射（从文件名/标题提取主关键词）
KEYWORDS = {
    "midjourney-v7-vs-flux-2026": "Midjourney vs Flux",
    "chatgpt-vs-claude-2026-comparison": "ChatGPT vs Claude",
    "claude-37-vs-gpt4o": "Claude 3.7 vs GPT-4o",
    "n8n-review-2026": "n8n review",
}

# 收集草稿（跳过 _review_report.md）
draft_dir = Path(ROOT) / "content_drafts"
drafts = []
for f in sorted(draft_dir.glob("*.md")):
    if f.name.startswith("_"):
        continue
    # slug = 去掉日期前缀和 _REWRITE/_DRAFT 后缀
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", f.stem)
    slug = re.sub(r"_(REWRITE|DRAFT)$", "", slug)
    drafts.append((f, slug))

print(f"=== 发现 {len(drafts)} 篇草稿 ===")
for f, slug in drafts:
    print(f"  - {f.name}  (slug={slug})")

evaluator = LMEvalKit()
status = evaluator.status()
print(f"\nllmevalkit installed: {status['llmevalkit_installed']}, modules: {status['available_modules']}\n")

results = []
for fpath, slug in drafts:
    text = fpath.read_text(encoding="utf-8")
    kw = KEYWORDS.get(slug, slug)
    print(f"--- 评估 {slug} ({len(text)} chars, kw={kw}) ---")
    try:
        res = evaluator.evaluate_content(text, keyword=kw)
    except Exception as e:
        res = {"score": 0, "error": str(e), "warnings": [f"evaluator error: {e}"]}
    res["slug"] = slug
    res["file"] = fpath.name
    res["keyword"] = kw
    results.append(res)
    print(f"    score={res.get('score')}  halluc={res.get('hallucination_detected')}  ai_prob={res.get('ai_content_probability',0):.1%}")
    for w in res.get("warnings", [])[:5]:
        print(f"      ! {w}")

# 按分数从低到高排序
results.sort(key=lambda r: r.get("score", 0))

# 判定 P0/P1
def classify(r):
    score = r.get("score", 0)
    if score < 70 or r.get("hallucination_detected") or r.get("ai_content_probability", 0) > 0.8:
        return "P0"
    if score < 85:
        return "P1"
    return "PASS"

for r in results:
    r["grade"] = classify(r)

# ===== 写报告 =====
report = []
report.append("# 全量内容质检报告（llmevalkit）\n")
report.append(f"**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**工具**: LMEvalKit 封装（{status['available_modules']} modules, use_llm=False）")
report.append(f"**草稿数**: {len(results)}\n")
report.append("## 一、总览（按分数从低到高）\n")
report.append("| 排名 | 文件 | 关键词 | 综合分 | 幻觉 | AI概率 | 字数 | 判定 |")
report.append("|------|------|--------|--------|------|--------|------|------|")
for i, r in enumerate(results, 1):
    report.append(
        f"| {i} | {r['file'][:45]} | {r.get('keyword','')} | **{r.get('score',0)}** | "
        f"{'是' if r.get('hallucination_detected') else '否'} | "
        f"{r.get('ai_content_probability',0):.1%} | "
        f"{r.get('word_count','?')} | {r['grade']} |"
    )
report.append("")

# 逐篇详情
report.append("## 二、逐篇详情\n")
for i, r in enumerate(results, 1):
    report.append(f"### {i}. {r['slug']}  —  **{r['grade']}** (score={r.get('score',0)})\n")
    report.append(f"- 文件: `{r['file']}`")
    report.append(f"- 关键词: {r.get('keyword','')}")
    report.append(f"- 字数: {r.get('word_count','?')} (chars={r.get('char_count','?')})")
    report.append(f"- 幻觉检测: {'⚠️ 触发' if r.get('hallucination_detected') else '✅ 未触发'}")
    report.append(f"- AI内容概率: {r.get('ai_content_probability',0):.1%}")
    if r.get("keyword_density"):
        report.append(f"- 关键词密度: {r['keyword_density']}")
    # 幻觉各检测器
    hall = r.get("checks", {}).get("hallucination", {})
    if isinstance(hall, dict):
        report.append("\n**幻觉子检测器**:")
        for k, v in hall.items():
            if isinstance(v, dict):
                report.append(f"- {k}: score={v.get('score','?')}  ({v.get('reason','')[:80]})")
    # AI content
    ai = r.get("checks", {}).get("ai_content", {})
    if isinstance(ai, dict):
        report.append(f"\n**AI检测**: {ai}")
    # PII
    pii = r.get("checks", {}).get("pii", {})
    if isinstance(pii, dict):
        report.append(f"**PII**: score={pii.get('score','?')}")
    # warnings
    report.append(f"\n**Warnings ({len(r.get('warnings',[]))})**:")
    for w in r.get("warnings", []):
        report.append(f"- ⚠️ {w}")
    # recommendations
    recs = evaluator.get_rewrite_recommendations(r)
    report.append(f"\n**修复建议**:")
    for rec in recs:
        report.append(f"- {rec}")
    report.append("")

# P0/P1 汇总
p0_list = [r for r in results if r["grade"] == "P0"]
p1_list = [r for r in results if r["grade"] == "P1"]
pass_list = [r for r in results if r["grade"] == "PASS"]

report.append("## 三、P0/P1 汇总\n")
report.append(f"- **P0 必须重写**: {len(p0_list)} 篇 — {', '.join(r['slug'] for r in p0_list) or '无'}")
report.append(f"- **P1 需按建议修改**: {len(p1_list)} 篇 — {', '.join(r['slug'] for r in p1_list) or '无'}")
report.append(f"- **PASS 可发布**: {len(pass_list)} 篇 — {', '.join(r['slug'] for r in pass_list) or '无'}\n")

report_path = Path(ROOT) / "iteration_center" / "hallucination_audit_report.md"
report_path.write_text("\n".join(report), encoding="utf-8")
print(f"\n报告已写: {report_path}")

# ===== 写 state.json =====
state_path = Path(ROOT) / "iteration_center" / "state.json"
state = json.load(open(state_path, "r", encoding="utf-8"))
if "next_iteration_focus" not in state:
    state["next_iteration_focus"] = []

# 清理旧的同 source 项
old = [t for t in state["next_iteration_focus"] if isinstance(t, dict) and t.get("source") == "hallucination_audit_report"]
for t in old:
    state["next_iteration_focus"].remove(t)

# 新增 P0/P1 待办
new_todos = []
for r in p0_list:
    new_todos.append({
        "id": f"QC-P0-{r['slug']}",
        "priority": "P0",
        "title": f"重写 {r['slug']}（score={r.get('score')}, halluc={r.get('hallucination_detected')}, ai_prob={r.get('ai_content_probability',0):.0%}）",
        "description": "；".join(r.get("warnings", [])[:5]),
        "assigned_to": ["内容生产窗口"],
        "source": "hallucination_audit_report",
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    })
for r in p1_list:
    new_todos.append({
        "id": f"QC-P1-{r['slug']}",
        "priority": "P1",
        "title": f"优化 {r['slug']}（score={r.get('score')}，按 recommendations 修改）",
        "description": "；".join(evaluator.get_rewrite_recommendations(r)[:3]),
        "assigned_to": ["内容生产窗口"],
        "source": "hallucination_audit_report",
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    })

# 插入到最前
for t in reversed(new_todos):
    state["next_iteration_focus"].insert(0, t)

state["last_updated"] = datetime.now().isoformat()
json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"state.json 已更新: 新增 {len(new_todos)} 条待办（P0={len(p0_list)}, P1={len(p1_list)}）")

# 保存原始 JSON
raw = Path(ROOT) / "iteration_center" / "_qc_raw_results.json"
json.dump(results, open(raw, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
print(f"原始结果: {raw}")
