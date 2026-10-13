# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

tab = None
for t in cdp.list_tabs():
    if "search-console/inspect" in t.get("url", "") and "id=" in t.get("url", ""):
        tab = t
        break
ws = cdp.connect(tab["webSocketDebuggerUrl"])
js = """JSON.stringify({
  textareas: Array.from(document.querySelectorAll('textarea')).map(t=>({cls:t.className.slice(0,60), placeholder:t.placeholder, aria:t.getAttribute('aria-label'), rows:t.rows, value:(t.value||'').slice(0,80), readonly:t.readOnly})),
  input2: (()=>{const i=document.querySelector('input.Ax4B8');return i?{placeholder:i.placeholder, aria:i.getAttribute('aria-label'), value:(i.value||'').slice(0,80)}:null})()
})"""
print(cdp.eval_js(ws, js))
ws.close()
