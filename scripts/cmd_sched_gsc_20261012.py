# -*- coding: utf-8 -*-
"""2026-10-12 每日调度：报告P0/P1覆盖检查 + GSC目标进度"""
import json, os, glob

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])
all_text = " ".join((t.get("task", "") + " " + t.get("id", "")) for t in nf).lower()

# 报告关键问题关键词覆盖检查
checks = {
    "GA4 Bot过滤/新加坡Bot": ["ga4-bot", "bot", "新加坡"],
    "CTR优化(title/meta)": ["ctr", "title", "meta"],
    "转化追踪/Key Events": ["key event", "转化追踪", "affiliate_link_click"],
    "断链/404修复": ["404", "断链", "redirect", "301"],
    "H1缺失": ["h1"],
    "薄内容分类页": ["薄内容", "thin"],
    "收录/索引(10 URL验证)": ["url verify", "收录", "网址检查"],
    "外链5-15域名": ["backlink-15", "外链"],
    "Reddit社区增长": ["reddit"],
    "pSEO去重": ["pseo", "去重"],
    "GEO三要素": ["geo-three", "geo"],
    "Answer-First": ["answer-first"],
}
print("=== 报告P0/P1 → 待办覆盖检查 ===")
missing = []
for label, kws in checks.items():
    hit = any(k in all_text for k in kws)
    flag = "✅已覆盖" if hit else "❌缺失"
    print(f"  {label}: {flag}")
    if not hit:
        missing.append(label)

print(f"\n缺失项: {missing}")

# GSC 目标进度：找最新 live_pull
gsc_dir = os.path.join(ROOT, "gsc-ga4-report")
pulls = sorted(glob.glob(os.path.join(gsc_dir, "live_pull_*.json")), reverse=True)
print(f"\n=== GSC 最新文件 ===")
if pulls:
    latest = pulls[0]
    print(f"  {os.path.basename(latest)}")
    with open(latest, encoding="utf-8") as f:
        g = json.load(f)
    # 尝试取关键字段
    def dig(obj, keys, default="?"):
        for k in keys:
            if isinstance(obj, dict) and k in obj:
                return obj[k]
        return default
    print(f"  keys: {list(g.keys())[:20] if isinstance(g, dict) else type(g)}")
    # 常见字段
    for k in ["total_impressions", "impressions", "total_clicks", "clicks", "ctr", "avg_position", "summary"]:
        v = dig(g, [k])
        if v != "?":
            print(f"  {k}: {v}")
