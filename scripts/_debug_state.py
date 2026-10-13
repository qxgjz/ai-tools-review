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
print("输入框状态:", cdp.eval_js(ws, """JSON.stringify({
  ax: (()=>{const i=document.querySelector('input.Ax4B8');return i?{disabled:i.disabled, readonly:i.readOnly, value:(i.value||'').slice(0,50), visible:!!(i.offsetWidth||i.offsetHeight)}:null})(),
  ynt: (()=>{const i=document.querySelector('input.yNVtPc');return i?{disabled:i.disabled, readonly:i.readOnly, value:(i.value||'').slice(0,50)}:null})(),
  loading: document.querySelectorAll('[role=progressbar],progress,[class*=loading]').length,
  inputs: document.querySelectorAll('input').length
})"""))
text = cdp.eval_js(ws, "document.body.innerText") or ""
for kw in ["正在检查", "请输入", "发生错误", "重试", "too many", "请求过多", "稍后"]:
    if kw in text:
        p = text.find(kw)
        print("命中[{}]: {}".format(kw, text[max(0,p-80):p+120].replace(chr(10),' ')))
ws.close()
