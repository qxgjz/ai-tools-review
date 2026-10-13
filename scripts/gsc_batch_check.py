# -*- coding: utf-8 -*-
"""
gsc_batch_check.py — 通过 AdsPower CDP 在 GSC 网址检查页批量查询 URL 收录状态
用法: python scripts/gsc_batch_check.py <start_idx> <count>
"""
import json
import sys
import time
import re

sys.path.insert(0, "scripts")
import adspower_cdp as cdp

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
INSPECT_URL = "https://search.google.com/search-console/inspect?resource_id=sc-domain%3Aaitoolcrux.com"


def build_url_list():
    with open(PROJECT + r"\data\tools.json", "r", encoding="utf-8") as f:
        tools = json.load(f)
    urls = []
    cats = {}
    for t in tools:
        c = t.get("category", "")
        cats.setdefault(c, []).append(t.get("slug", ""))
    # 先分类页
    for c in cats:
        urls.append("https://www.aitoolcrux.com/category/" + c)
    # 每个分类前 3 个工具页
    for c, slugs in cats.items():
        for s in slugs[:3]:
            urls.append("https://www.aitoolcrux.com/tools/" + s)
    # 去重保序
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def get_control_tab():
    # 优先复用已处于"检查结果视图"的网址检查标签页（带 id= 参数的）
    for t in cdp.list_tabs():
        u = t.get("url", "")
        if "search-console/inspect" in u and "id=" in u:
            return t
    # 没有则新开，并喂入一个已知 URL 让它进入检查结果视图
    r = cdp.open_tab(INSPECT_URL)
    if not r.get("id"):
        return None
    time.sleep(6)
    tab = next((t for t in cdp.list_tabs() if t.get("id") == r["id"]), None)
    if tab:
        ws = cdp.connect(tab["webSocketDebuggerUrl"])
        set_url(ws, "https://www.aitoolcrux.com/category/video")
        time.sleep(9)
        ws.close()
        for t in cdp.list_tabs():
            if t.get("id") == r["id"]:
                return t
    return None


def set_url(ws, url):
    # 正确的 URL 输入框是 input.Ax4B8（aria-label="检查 xxx 中的任何网址"）
    # 关键：GSC 改版后 dispatchKeyEvent 键入不触发检查，改用 native setter + input/change 事件 + 回车
    cdp.send(ws, "Page.bringToFront", {})
    time.sleep(0.8)
    js = ("(()=>{const i=document.querySelector('input.Ax4B8');if(!i)return 'NO_INPUT';"
          "const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
          "s.call(i," + json.dumps(url) + ");"
          "i.dispatchEvent(new Event('input',{bubbles:true}));"
          "i.dispatchEvent(new Event('change',{bubbles:true}));"
          "i.focus();"
          "return i.value===" + json.dumps(url) + "?'OK':'SET_FAIL';})()")
    r = cdp.eval_js(ws, js)
    if r != "OK":
        return r
    cdp.press_enter(ws)
    return "OK"


def get_text(ws):
    return cdp.eval_js(ws, "document.body.innerText") or ""


def classify(text):
    low = text
    if "网址已收录到 Google" in low:
        return "indexed"
    if "未找到 (404)" in low or "未找到(404)" in low:
        return "404"
    if "被“noindex”标记排除" in low or "noindex" in low.lower():
        return "noindex"
    if "网页会自动重定向" in low:
        return "redirect"
    if "重定向错误" in low:
        return "redirect_error"
    if "重复网页" in low:
        return "duplicate"
    if "已抓取 - 尚未编入索引" in low or "已抓取-尚未编入索引" in low:
        return "crawled_not_indexed"
    if "已发现 - 尚未编入索引" in low or "已发现-尚未编入索引" in low:
        return "discovered_not_indexed"
    if "网页未编入索引" in low or "网页未编入索引" in low:
        return "not_indexed"
    return "unknown"


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    urls = build_url_list()
    batch = urls[start:start + count]
    print("URL 总数: {}  本次检查: {} - {} ({})".format(len(urls), start, start + len(batch) - 1, len(batch)))

    tab = get_control_tab()
    if not tab:
        print("无法获取控制标签页")
        return
    print("控制标签页:", tab["url"])
    ws = cdp.connect(tab["webSocketDebuggerUrl"])

    results = []
    for i, url in enumerate(batch):
        # 输入失败则重试一次（重建检查页场景）
        set_ret = set_url(ws, url)
        if set_ret != "OK":
            print("[{}/{}] {} => 输入失败({})，重试一次".format(i + 1, len(batch), url, set_ret))
            time.sleep(2)
            set_ret = set_url(ws, url)
        if set_ret != "OK":
            results.append({"url": url, "status": "input_fail", "detail": set_ret})
            print("[{}/{}] {} => input_fail ({})".format(i + 1, len(batch), url, set_ret))
            continue
        # 等待自动检查完成（轮询，最多 30 秒）
        status = "unknown"
        text = ""
        for _ in range(30):
            time.sleep(1)
            text = get_text(ws)
            if url in text:
                status = classify(text)
                if status != "unknown":
                    break
        results.append({"url": url, "status": status})
        print("[{}/{}] {} => {}".format(i + 1, len(batch), url, status))
        # 关键状态抓取结果片段
        if status in ("404", "noindex", "redirect", "redirect_error", "duplicate"):
            m = re.search(r"(网页未编入索引|网址已收录到 Google)[^\n]{0,80}", text)
            print("   详情:", m.group(0) if m else "-")

    out_path = PROJECT + r"\gsc-ga4-report\url_index_check_batch_{}_{}_{}.json".format(
        start, start + len(batch) - 1, time.strftime("%Y%m%d_%H%M%S"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"start": start, "count": len(batch), "results": results}, f, ensure_ascii=False, indent=2)
    print("已保存:", out_path)

    from collections import Counter
    print("状态分布:", dict(Counter(r["status"] for r in results)))
    ws.close()


if __name__ == "__main__":
    main()
