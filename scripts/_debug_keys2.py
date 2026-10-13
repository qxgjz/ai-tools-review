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

# 聚焦正确的输入框
print("focus:", cdp.eval_js(ws, "(()=>{const i=document.querySelector('input.Ax4B8');if(!i)return 'NO_INPUT';i.focus();i.select();return 'OK'})()"))
time.sleep(0.5)

# 逐字符真实按键
url = "https://www.aitoolcrux.com/category/code"
def key_code(ch):
    if ch.isalpha():
        return "Key" + ch.upper()
    if ch.isdigit():
        return "Digit" + ch
    return {"/": "Slash", ":": "Semicolon", ".": "Period", "-": "Minus", "_": "Minus"}.get(ch, "")
for ch in url:
    cdp.send(ws, "Input.dispatchKeyEvent", {
        "type": "keyDown", "text": ch, "key": ch, "code": key_code(ch),
        "unmodifiedText": ch, "windowsVirtualKeyCode": 0, "nativeVirtualKeyCode": 0,
    })
    cdp.send(ws, "Input.dispatchKeyEvent", {
        "type": "keyUp", "key": ch, "code": key_code(ch),
        "windowsVirtualKeyCode": 0, "nativeVirtualKeyCode": 0,
    })
time.sleep(0.5)
print("键入后value:", cdp.eval_js(ws, "document.querySelector('input.Ax4B8') && document.querySelector('input.Ax4B8').value"))
print("Enter:", cdp.press_enter(ws))
for s in (2, 3, 5):
    time.sleep(s)
    href = cdp.eval_js(ws, "location.href")
    text = cdp.eval_js(ws, "document.body.innerText") or ""
    print(f"[+{s}s] href含inspect={'inspect' in href}, 含code={'category/code' in text}, 含'已收录'={'网址已收录' in text}, 含'未编入'={'网页未编入索引' in text}")
ws.close()
