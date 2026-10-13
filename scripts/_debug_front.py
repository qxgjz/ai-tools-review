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

# 1) 把标签页带到前台（CDP 层）
print("bringToFront:", cdp.send(ws, "Page.bringToFront", {}))
time.sleep(1)

# 2) focus+select+直接键入（不清空）
url = "https://www.aitoolcrux.com/category/code"
r = cdp.eval_js(ws, "(()=>{const i=document.querySelector('input.Ax4B8');if(!i)return 'NO_INPUT';i.focus();i.select();return 'OK'})()")
print("focus:", r)
def key_code(ch):
    if ch.isalpha(): return "Key" + ch.upper()
    if ch.isdigit(): return "Digit" + ch
    return {"/": "Slash", ":": "Semicolon", ".": "Period", "-": "Minus", "_": "Minus"}.get(ch, "")
for ch in url:
    cdp.send(ws, "Input.dispatchKeyEvent", {"type":"keyDown","text":ch,"key":ch,"code":key_code(ch),"unmodifiedText":ch,"windowsVirtualKeyCode":0,"nativeVirtualKeyCode":0})
    cdp.send(ws, "Input.dispatchKeyEvent", {"type":"keyUp","key":ch,"code":key_code(ch),"windowsVirtualKeyCode":0,"nativeVirtualKeyCode":0})
time.sleep(0.5)
val = cdp.eval_js(ws, "document.querySelector('input.Ax4B8') ? document.querySelector('input.Ax4B8').value : ''") or ""
print("键入后 value:", val[:60])
if url not in val:
    # 3) 若仍失败，用 Input.insertText 兜底（现在页面前台了）
    print("insertText 兜底:", cdp.insert_text(ws, url))
    time.sleep(0.5)
    val = cdp.eval_js(ws, "document.querySelector('input.Ax4B8') ? document.querySelector('input.Ax4B8').value : ''") or ""
    print("兜底后 value:", val[:60])
cdp.press_enter(ws)
for s in (2, 4, 6):
    time.sleep(s)
    text = cdp.eval_js(ws, "document.body.innerText") or ""
    print(f"[+{s}s] 含code={'category/code' in text}, 已收录={'网址已收录' in text}, 未编入={'网页未编入索引' in text}")
ws.close()
