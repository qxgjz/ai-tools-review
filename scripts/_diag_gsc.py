# -*- coding: utf-8 -*-
"""导航回 index 报告 → 点「网页会自动重定向」和「重复网页」行。"""
import sys, time
sys.path.insert(0, "scripts")
import adspower_cdp as cdp

tab = None
for t in cdp.list_tabs():
    if 'search-console/index' in t.get('url', ''):
        tab = t
        break
ws = cdp.connect(tab['webSocketDebuggerUrl'])
cdp.send(ws, 'Page.bringToFront', {})
time.sleep(1)

def go_list():
    cdp.send(ws, 'Page.navigate', {'url': 'https://search.google.com/search-console/index?resource_id=sc-domain%3Aaitoolcrux.com'})
    time.sleep(5)

def click_row(kw):
    js = ("(()=>{const cands=[...document.querySelectorAll('a,div,span,li,button')].filter(e=>{"
          "  const t=(e.innerText||'').trim();"
          "  return t.indexOf('" + kw + "')>=0 && e.offsetParent!==null && e.children.length<=1;"
          "});"
          "if(cands.length===0)return 'NO';"
          "const el=cands[cands.length-1];el.click();return 'CLICKED:'+el.tagName;})()")
    print('点击', kw, ':', cdp.eval_js(ws, js))
    time.sleep(3)
    txt = cdp.eval_js(ws, 'document.body.innerText') or ''
    idx = txt.find(kw)
    if idx >= 0:
        print('---', kw, '详情 ---')
        print(txt[idx:idx+800].replace('\n', ' | '))
    else:
        print('未找到文本')

go_list()
click_row('网页会自动重定向')
ws.close()
