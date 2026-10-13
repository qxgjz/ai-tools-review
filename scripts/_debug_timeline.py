# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

INSPECT_URL = "https://search.google.com/search-console/inspect?resource_id=sc-domain%3Aaitoolcrux.com"
r = cdp.open_tab(INSPECT_URL)
tab_id = r.get("id")
time.sleep(6)
tab = next((t for t in cdp.list_tabs() if t.get("id") == tab_id), None)
print("open后 href:", tab["url"])
ws = cdp.connect(tab["webSocketDebuggerUrl"])

def set_via_event(url):
    js = ("(()=>{const input=document.querySelector('input.yNVtPc');if(!input)return 'NO_INPUT';"
          "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
          "setter.call(input,'" + url + "');"
          "input.dispatchEvent(new Event('input',{bubbles:true}));"
          "input.dispatchEvent(new Event('change',{bubbles:true}));return 'OK'})()")
    return cdp.eval_js(ws, js)

print("set:", set_via_event("https://www.aitoolcrux.com/category/chat"))
for i in range(1, 13):
    time.sleep(1)
    href = cdp.eval_js(ws, "location.href") or ""
    text = cdp.eval_js(ws, "document.body.innerText") or ""
    marks = []
    for kw, name in [("category/chat", "URLchat"), ("category/video", "URLvideo"),
                     ("网址已收录到 Google", "已收录"), ("网页未编入索引", "未编入"),
                     ("未找到 (404)", "404"), ("已发现 - 尚未编入索引", "已发现未编入")]:
        if kw in text:
            marks.append(name)
    # 结果区域摘要
    seg = ""
    for kw in ["网页索引编制", "网页可用性"]:
        p = text.find(kw)
        if p >= 0:
            seg += "[" + kw + "]" + text[p:p+40].replace("\n", " ")[:40]
    print(f"[+{i}s] href尾部={'inspect' if 'inspect' in href else '概述页'}, 命中={marks} {seg}")
ws.close()
