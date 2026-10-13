# -*- coding: utf-8 -*-
"""环境准备 v3：native setter 设置 URL + input 事件 + 回车。"""
import sys, time
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

def json_str(s):
    return '"' + s.replace('"', '\\"') + '"'

TEST_URL = "https://www.aitoolcrux.com/category/chat"
INSPECT_URL = "https://search.google.com/search-console/inspect?resource_id=sc-domain%3Aaitoolcrux.com"

tab = None
for t in cdp.list_tabs():
    if "search-console" in t.get("url", "") and "/inspect" in t.get("url", ""):
        tab = t
        break
if not tab:
    r = cdp.open_tab(INSPECT_URL)
    time.sleep(6)
    for t in cdp.list_tabs():
        if t.get("id") == r.get("id"):
            tab = t
            break
if not tab:
    print("无 inspect 标签")
    sys.exit(1)
ws = cdp.connect(tab["webSocketDebuggerUrl"])
print("标签URL:", tab["url"][:110])

cdp.send(ws, "Page.bringToFront", {})
time.sleep(1)

js = (
    "(()=>{const i=document.querySelector('input.Ax4B8');if(!i)return 'NO_INPUT';"
    "const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
    "s.call(i," + json_str(TEST_URL) + ");"
    "i.dispatchEvent(new Event('input',{bubbles:true}));"
    "i.dispatchEvent(new Event('change',{bubbles:true}));"
    "i.focus();"
    "return i.value===" + json_str(TEST_URL) + "?'SET_OK':'SET_FAIL';})()"
)
r = cdp.eval_js(ws, js)
print("设置URL:", r)

cdp.press_enter(ws)
time.sleep(2)

found = False
for i in range(15):
    time.sleep(2)
    txt = cdp.eval_js(ws, "document.body.innerText") or ""
    for k in ["网址已收录到 Google", "重定向错误", "会自动重定向", "未找到 (404)", "已发现 - 尚未编入索引",
              "已抓取 - 尚未编入索引", "被“noindex”", "重复网页", "网页未编入索引"]:
        if k in txt:
            print("命中:", k, "(@%ds)" % ((i + 1) * 2))
            found = True
            break
    if found:
        break
url = cdp.eval_js(ws, "location.href") or ""
print("最终URL:", url[:130])
if not found:
    print("未命中关键词，页面片段:", (cdp.eval_js(ws, "document.body.innerText") or "")[200:600].replace(chr(10), " | "))
ws.close()
