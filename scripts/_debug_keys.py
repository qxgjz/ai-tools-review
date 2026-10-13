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

# 1) 用原生 setter 清空（清空 React 通常响应）
cdp.eval_js(ws, ("(()=>{const input=document.querySelector('input.yNVtPc');"
                 "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                 "setter.call(input,'');"
                 "input.dispatchEvent(new Event('input',{bubbles:true}));"
                 "input.focus();return input.value})()"))
time.sleep(0.5)
print("清空后value:", cdp.eval_js(ws, "document.querySelector('input.yNVtPc') && document.querySelector('input.yNVtPc').value"))

# 2) 逐字符真实按键
url = "https://www.aitoolcrux.com/category/code"
for ch in url:
    cdp.send(ws, "Input.dispatchKeyEvent", {
        "type": "keyDown", "text": ch, "key": ch, "code": "Key" + (ch.upper() if ch.isalpha() else ""),
        "unmodifiedText": ch, "windowsVirtualKeyCode": 0, "nativeVirtualKeyCode": 0,
    })
    cdp.send(ws, "Input.dispatchKeyEvent", {
        "type": "keyUp", "key": ch, "code": "Key" + (ch.upper() if ch.isalpha() else ""),
        "windowsVirtualKeyCode": 0, "nativeVirtualKeyCode": 0,
    })
time.sleep(0.5)
print("键入后value:", cdp.eval_js(ws, "document.querySelector('input.yNVtPc') && document.querySelector('input.yNVtPc').value"))

# 3) 回车触发
cdp.press_enter(ws)
for s in (2, 4, 6):
    time.sleep(s)
    href = cdp.eval_js(ws, "location.href")
    text = cdp.eval_js(ws, "document.body.innerText") or ""
    print(f"[+{s}s] href={href}")
    print("   含code:", "category/code" in text, "| 含'已收录':", "网址已收录" in text, "| 含'未编入':", "网页未编入索引" in text)
ws.close()
