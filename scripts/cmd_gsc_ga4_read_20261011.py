# -*- coding: utf-8 -*-
"""读取最新 GA4 + GSC 数据，用于30天目标进度"""
import json, os

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\gsc-ga4-report"

def show(path, name):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    print("=" * 20, name, "=" * 20)
    if isinstance(d, dict):
        print("keys:", list(d.keys()))
        ov = d.get("overview")
        if ov:
            print("overview:", json.dumps(ov, ensure_ascii=False)[:600])
        daily = d.get("daily")
        if daily:
            items = daily if isinstance(daily, list) else list(daily.items())[:5]
            print("daily(前5):", json.dumps(items, ensure_ascii=False)[:800])
        tl = d.get("top_landing")
        if tl:
            print("top_landing(前5):", json.dumps(tl[:5] if isinstance(tl, list) else tl, ensure_ascii=False)[:600])
        tq = d.get("top_queries")
        if tq:
            print("top_queries(前5):", json.dumps(tq[:5] if isinstance(tq, list) else tq, ensure_ascii=False)[:600])
        site = d.get("site")
        if site:
            print("site:", site)

show(os.path.join(ROOT, "ga4_live_20261011_1409.json"), "GA4 LIVE 14:09")
show(os.path.join(ROOT, "live_pull_20261011_1409.json"), "GSC LIVE 14:09")
