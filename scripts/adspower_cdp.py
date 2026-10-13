# -*- coding: utf-8 -*-
"""
adspower_cdp.py — 免费连接 AdsPower SunBrowser（无需 API Key）
原理：读取 AdsPower profile 缓存里的 DevToolsActivePort 拿到 CDP 端口，
通过 Chrome DevTools Protocol 直接驱动 AdsPower 内的浏览器，复用其登录态。

用法：
  python adspower_cdp.py tabs                # 列出所有标签页
  python adspower_cdp.py open <url>          # 打开新标签页
  python adspower_cdp.py eval <匹配串> <js>  # 在标题/URL 含匹配串的标签页执行 JS
  python adspower_cdp.py text <匹配串>       # 读取标签页可见文本
"""
import json
import sys
import time
import urllib.parse
import urllib.request

import websocket

PORT_FILE = r"C:\.ADSPOWER_GLOBAL\cache\k1hfuvv6_i786g3\DevToolsActivePort"


def get_port():
    with open(PORT_FILE, "r", encoding="utf-8") as f:
        return int(f.readline().strip())


def _http(method, path):
    port = get_port()
    url = "http://127.0.0.1:{}{}".format(port, path)
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def list_tabs():
    return [t for t in _http("GET", "/json/list") if t.get("type") == "page"]


def open_tab(url):
    return _http("PUT", "/json/new?{}".format(urllib.parse.quote(url, safe="")))


def connect(ws_url):
    # AdsPower 启动 SunBrowser 未带 --remote-allow-origins，CDP 会拒绝第三方 Origin。
    # 用 chrome-devtools:// 官方前端 Origin 或空 Origin 可绕过该校验。
    try:
        ws = websocket.create_connection(
            ws_url, timeout=20,
            header=["Origin: chrome-devtools://devtools"],
        )
    except websocket.WebSocketBadStatusException:
        ws = websocket.create_connection(ws_url, timeout=20, suppress_origin=True)
    return ws


def send(ws, method, params=None, req_id=1):
    ws.send(json.dumps({"id": req_id, "method": method, "params": params or {}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == req_id:
            return resp


def eval_js(ws, js):
    resp = send(ws, "Runtime.evaluate", {"expression": js, "returnByValue": True})
    return resp.get("result", {}).get("result", {}).get("value")


def focus_and_select(ws, selector):
    """聚焦输入框并全选已有内容（为真实键入做准备）"""
    js = ("(()=>{const el=document.querySelector('" + selector + "');"
          "if(!el)return 'NO_EL';el.focus();el.select();return 'OK'})()")
    return eval_js(ws, js)


def insert_text(ws, text):
    """通过 CDP Input.insertText 真实键入文本（触发受控组件正确响应）"""
    resp = send(ws, "Input.insertText", {"text": text})
    return resp.get("error") is None


def press_enter(ws):
    """发送真实 Enter 键"""
    for t in ("keyDown", "keyUp"):
        send(ws, "Input.dispatchKeyEvent", {
            "type": t, "key": "Enter", "code": "Enter",
            "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13,
        })


def type_url(ws, selector, url):
    """完整流程：聚焦 -> 全选清空 -> 真实键入 -> 回车触发查询"""
    r = focus_and_select(ws, selector)
    if r != "OK":
        return r
    insert_text(ws, url)
    press_enter(ws)
    return "OK"


def find_tab(match):
    tabs = list_tabs()
    for t in tabs:
        hay = (t.get("title") or "") + " " + (t.get("url") or "")
        if match in hay:
            return t
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "tabs":
        for t in list_tabs():
            print("[{}] {} => {}".format(t.get("type"), t.get("title"), t.get("url")))
        return

    if cmd == "open":
        url = sys.argv[2]
        r = open_tab(url)
        print("已打开标签页: id={} url={}".format(r.get("id"), r.get("url")))
        return

    if cmd in ("eval", "text"):
        match = sys.argv[2]
        tab = find_tab(match)
        if not tab:
            print("未找到包含 '{}' 的标签页".format(match))
            return
        ws = connect(tab["webSocketDebuggerUrl"])
        if cmd == "eval":
            js = sys.argv[3]
            print(eval_js(ws, js))
        else:
            js = "document.body.innerText"
            text = eval_js(ws, js)
            print((text or "")[:4000])
        ws.close()
        return

    print(__doc__)


if __name__ == "__main__":
    main()
