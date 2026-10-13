# -*- coding: utf-8 -*-
"""2026-10-12 每日调度：读GSC最新 + 补录缺失待办"""
import json, os

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
GSC = os.path.join(ROOT, "gsc-ga4-report", "live_pull_20261012_1439.json")
STATE = os.path.join(ROOT, "iteration_center", "state.json")

with open(GSC, encoding="utf-8") as f:
    g = json.load(f)

print(f"=== GSC {g.get('pulled_at','')} ===")
print(f"site: {g.get('site')}")
print(f"查询窗口: {g.get('query_window_start')} ~ {g.get('query_window_end')}")
daily = g.get("daily", [])
if daily:
    tot_imp = sum(d.get("impressions", 0) for d in daily)
    tot_clk = sum(d.get("clicks", 0) for d in daily)
    print(f"daily天数: {len(daily)} | 总曝光: {tot_imp} | 总点击: {tot_clk}")
print("top_queries:", json.dumps(g.get("top_queries", [])[:5], ensure_ascii=False)[:400])
print("top_pages:", json.dumps(g.get("top_pages", [])[:5], ensure_ascii=False)[:400])

# 补录缺失待办
with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])
existing_ids = {t.get("id") for t in nf}
today = "2026-10-12"

new_todos = [
    {
        "id": "P0-CTR-TITLE-BATCH-20261012",
        "task": "CTR批量优化（audit_findings P0-2/P1-1遗留+GSC 10-12 仍有高曝光零点击页）：对GSC top_pages 中排名<=20且CTR<1%的页面批量重写title/meta（含数字+年份+情感词），目标全站CTR 0.45%→1%+；参考best-ai-voice-changers-2026 CTR 2.9%的'best X 2026'格式",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window5", "打磨师"],
        "source": "audit_findings.md",
        "created_at": today,
    },
    {
        "id": "P1-ANALYTICS-KEYEVENT-20261012",
        "task": "转化追踪落地（audit_findings P1-3）：GA4创建affiliate_link_click自定义事件+自定义维度(affiliate_network/offer_id/placement)并标记Key Event；验证联盟链接点击可追踪（GTM或gtag配置）",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window4", "分析师"],
        "source": "audit_findings.md",
        "created_at": today,
    },
    {
        "id": "P1-H1-MISSING-20261012",
        "task": "H1缺失修复（audit_findings 9-27：121页缺H1，含5个article-api-*自动页）：创作家/打磨师批量检查并补H1（每页唯一H1），架构师核查模板层H1输出；同时301处理article-api-*丑陋URL",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["创作家", "window5", "打磨师"],
        "source": "audit_findings.md",
        "created_at": today,
    },
    {
        "id": "P1-THIN-CATEGORY-20261012",
        "task": "薄内容分类页修复（audit_findings 9-27：10个分类页138-148词）：为/blog/category/*和/subcategory/*添加>=300词介绍性文字，或设置noindex（二选一按价值判断）",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window3", "创作家"],
        "source": "audit_findings.md",
        "created_at": today,
    },
]

added = 0
for t in new_todos:
    if t["id"] in existing_ids:
        print(f"跳过已存在: {t['id']}")
        continue
    nf.append(t)
    added += 1
state["next_iteration_focus"] = nf
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"\n补录待办: {added} 条，active总数: {len(nf)}")
