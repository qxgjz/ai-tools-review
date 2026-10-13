# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

tab = None
for t in cdp.list_tabs():
    if "search-console/inspect" in t.get("url", "") and "id=" in t.get("url", ""):
        tab = t
        break
print("控制页:", tab["url"] if tab else None)
ws = cdp.connect(tab["webSocketDebuggerUrl"])
js = """JSON.stringify({
  inputs: Array.from(document.querySelectorAll('input')).map(i=>({cls:i.className.slice(0,50), readonly:i.readOnly, disabled:i.disabled, tabindex:i.tabIndex, value:(i.value||'').slice(0,60)})),
  contentedit: Array.from(document.querySelectorAll('[contenteditable=true]')).map(e=>e.className.slice(0,50)),
  textareas: document.querySelectorAll('textarea').length,
  inputsCount: document.querySelectorAll('input').length
})"""
print(cdp.eval_js(ws, js))
ws.close()
