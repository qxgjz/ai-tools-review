# -*- coding: utf-8 -*-
import json, time

p = r"iteration_center\state.json"
d = json.load(open(p, encoding="utf-8"))
nf = d["next_iteration_focus"]
new_items = [
    {
        "id": "GSC-QUOTA-RERUN-20261012",
        "priority": "P1",
        "assigned_to": ["analyst"],
        "status": "pending",
        "source": "gsc_batch_check_20261012",
        "task": "GSC网址检查每日配额2026-10-12已耗尽（页面弹窗超出配额）。2026-10-13配额重置后用修复版脚本重跑40个unknown URL：python scripts/gsc_batch_check.py。脚本已修复：输入框必须用input.Ax4B8，且每次输入前必须cdp.send(ws,Page.bringToFront)把页面带到前台，否则dispatchKeyEvent事件被丢弃导致value为空。重跑完成后对照url_index_check_batch_0_67_20261012_202338.json汇总最终收录状态，404/noindex/redirect坏URL清单派给架构师修复。",
    },
    {
        "id": "GSC-BADURL-FIX-VERIFY-20261012",
        "priority": "P1",
        "assigned_to": ["架构师"],
        "status": "pending",
        "source": "gsc_batch_check_20261012",
        "task": "已确认的坏URL需修复并提交IndexNow：redirect_error(3个)=/category/chat、/category/code、/tools/gemini；redirect(1个)=/tools/chatgpt；discovered_not_indexed(4个)=/category/memory、/category/observability、/tools/claude、/tools/exa。检查线上是否有重定向链(301/302/canonical)，修复后重新请求编入索引。",
    },
]
existing = {it.get("id") or "" for it in nf}
added = 0
for it in new_items:
    if it["id"] not in existing:
        nf.append(it)
        added += 1
d["next_iteration_focus"] = nf
d["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added:", added, "total:", len(nf))
