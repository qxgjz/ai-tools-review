# -*- coding: utf-8 -*-
import json, os
BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
s = json.load(open(os.path.join(BASE, "iteration_center", "state.json"), "r", encoding="utf-8"))

print("=== state.json key fields ===")
for k in ["last_updated","last_analytics_run","gsc_latest_clicks","gsc_latest_impressions","ga4_api_status","analytics_provider"]:
    print(f"  {k}: {s.get(k)}")
ct = s.get("current_todo", [])
print(f"  current_todo: list[{len(ct)}]")
for t in ct:
    if isinstance(t, dict):
        print(f"    - {t.get('id','?')}: {str(t.get('title','?'))[:80]}")

print("\n=== my 3 items from 15:00 still present? ===")
my_ids = ["P0-TRAFFIC-CLIFF-20260924-001","P1-GA4-REBUILD-001","P1-QUERY-FILTER-RULE-001"]
focus = s.get("next_iteration_focus", [])
print(f"  next_iteration_focus total: {len(focus)}")
for mid in my_ids:
    found = [x for x in focus if isinstance(x,dict) and x.get("id")==mid]
    if found:
        f = found[0]
        print(f"  [OK] {mid}: status={f.get('status')}, assigned={f.get('assigned_to')}")
    else:
        print(f"  [MISSING] {mid}")

print("\n=== last 5 items in focus (what other windows added) ===")
for item in focus[-5:]:
    if isinstance(item, dict):
        print(f"  {item.get('priority','?')} {item.get('id','?')}: {str(item.get('title','?'))[:90]}")
