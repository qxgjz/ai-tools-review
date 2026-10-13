# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

r = cdp.open_tab("https://search.google.com/search-console/inspect?resource_id=sc-domain%3Aaitoolcrux.com")
tab_id = r.get("id")
time.sleep(8)
tabs = cdp.list_tabs()
tab = next(t for t in tabs if t.get("id") == tab_id)
print("tab url:", tab["url"])
ws = cdp.connect(tab["webSocketDebuggerUrl"])

def set_url(ws, url):
    js = ("(()=>{const input=document.querySelector('input.yNVtPc');if(!input)return 'NO_INPUT';"
          "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
          "setter.call(input,'" + url + "');"
          "input.dispatchEvent(new Event('input',{bubbles:true}));"
          "input.dispatchEvent(new Event('change',{bubbles:true}));return 'OK'})()")
    return cdp.eval_js(ws, js)

print("set:", set_url(ws, "https://www.aitoolcrux.com/category/code"))
time.sleep(8)
print("页面URL:", cdp.eval_js(ws, "location.href"))
text = cdp.eval_js(ws, "document.body.innerText") or ""
idx = text.find("code")
print("code 出现位置:", idx)
print(text[max(0, idx-300):idx+600] if idx >= 0 else text[:2000])
ws.close()
