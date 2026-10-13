# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

# 复用带 id 的检查页
tab = None
for t in cdp.list_tabs():
    if "search-console/inspect" in t.get("url", "") and "id=" in t.get("url", ""):
        tab = t
        break
print("控制页:", tab["url"] if tab else None)
if not tab:
    sys.exit(1)
ws = cdp.connect(tab["webSocketDebuggerUrl"])

def set_url(ws, url):
    js = ("(()=>{const input=document.querySelector('input.yNVtPc');if(!input)return 'NO_INPUT';"
          "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
          "setter.call(input,'');"
          "input.dispatchEvent(new Event('input',{bubbles:true}));"
          "setter.call(input,'" + url + "');"
          "input.dispatchEvent(new Event('input',{bubbles:true}));"
          "input.dispatchEvent(new Event('change',{bubbles:true}));"
          "return 'OK: value='+input.value})()")
    return cdp.eval_js(ws, js)

print("set:", set_url(ws, "https://www.aitoolcrux.com/category/chat"))
for s in (2, 4, 8):
    time.sleep(s)
    href = cdp.eval_js(ws, "location.href")
    print(f"[+{s}s] href={href}")
text = cdp.eval_js(ws, "document.body.innerText") or ""
idx = text.find("category/chat")
print("category/chat 位置:", idx)
if idx >= 0:
    print(text[max(0, idx-150):idx+400])
else:
    # 打印输入框附近与按钮
    print("文本前1200:", text[:1200])
ws.close()
