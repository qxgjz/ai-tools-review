# -*- coding: utf-8 -*-
"""验证策略A：每个URL新开inspect标签页 + 原生setter注入"""
import sys, time
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

INSPECT_URL = "https://search.google.com/search-console/inspect?resource_id=sc-domain%3Aaitoolcrux.com"

def check_one(url, timeout=25):
    r = cdp.open_tab(INSPECT_URL)
    tab_id = r.get("id")
    time.sleep(7)
    tab = next((t for t in cdp.list_tabs() if t.get("id") == tab_id), None)
    if not tab:
        return "no_tab"
    ws = cdp.connect(tab["webSocketDebuggerUrl"])
    js = ("(()=>{const input=document.querySelector('input.yNVtPc');if(!input)return 'NO_INPUT';"
          "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
          "setter.call(input,'" + url + "');"
          "input.dispatchEvent(new Event('input',{bubbles:true}));"
          "input.dispatchEvent(new Event('change',{bubbles:true}));return 'OK'})()")
    r2 = cdp.eval_js(ws, js)
    status = "unknown"
    for i in range(timeout):
        time.sleep(1)
        text = cdp.eval_js(ws, "document.body.innerText") or ""
        href = cdp.eval_js(ws, "location.href") or ""
        if "inspect" not in href:
            status = "jumped_overview"
            break
        if url in text:
            if "网址已收录到 Google" in text: status = "indexed"; break
            if "未找到 (404)" in text: status = "404"; break
            if "网页未编入索引" in text:
                status = "not_indexed"; break
            if "重复网页" in text: status = "duplicate"; break
            if "noindex" in text.lower(): status = "noindex"; break
            if "重定向" in text: status = "redirect"; break
    ws.close()
    # 关闭标签页
    try:
        cdp._http("GET", "/json/close/{}".format(tab_id))
    except Exception:
        pass
    return status

for u in ["https://www.aitoolcrux.com/category/chat",
          "https://www.aitoolcrux.com/category/code",
          "https://www.aitoolcrux.com/category/video"]:
    s = check_one(u)
    print(u, "=>", s)
