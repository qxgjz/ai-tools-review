# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

tab = None
for t in cdp.list_tabs():
    if "search-console/inspect" in t.get("url", "") and "id=" in t.get("url", ""):
        tab = t
        break
print("控制页:", tab["url"] if tab else None)
ws = cdp.connect(tab["webSocketDebuggerUrl"])

print("focus+select:", cdp.focus_and_select(ws, "input.yNVtPc"))
time.sleep(1)
print("当前value:", cdp.eval_js(ws, "document.querySelector('input.yNVtPc') ? document.querySelector('input.yNVtPc').value : 'NO_INPUT'"))
print("insertText:", cdp.insert_text(ws, "https://www.aitoolcrux.com/category/code"))
time.sleep(1)
print("插入后value:", cdp.eval_js(ws, "document.querySelector('input.yNVtPc') ? document.querySelector('input.yNVtPc').value : 'NO_INPUT'"))
print("Enter:", cdp.press_enter(ws))
for s in (2, 4, 6):
    time.sleep(s)
    href = cdp.eval_js(ws, "location.href")
    print(f"[+{s}s] href={href}")
    if "category/code" in (cdp.eval_js(ws, "document.body.innerText") or ""):
        print("  -> 页面文本已包含 category/code")
        break
    else:
        print("  -> 页面文本未包含 category/code")
ws.close()
