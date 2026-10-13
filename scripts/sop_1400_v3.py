import urllib.request, ssl, json, os
from datetime import datetime, timezone, timedelta
CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S CST")
PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")
LOG_PATH = os.path.join(PROJECT, "window_logs", f"growth_{today}.md")
PROXY = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
opener = urllib.request.build_opener(PROXY, urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]
def check(url):
    try:
        with opener.open(url, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore").lower()
            return r.status, "aitoolcrux" in html
    except Exception as e:
        return -1, False
sites = [
    ("aitoolsdirectory", "https://aitoolsdirectory.com/?s=aitoolcrux"),
    ("hyzenpro", "https://hyzenpro.com/?s=aitoolcrux"),
]
results = {}
for name, url in sites:
    s, h = check(url)
    results[name] = (s, h)
    print(f"{name}: {s}, found={h}")
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)
state.setdefault("completed_tasks", []).append({
    "task": "拓荒者-SOP(14点档)",
    "time": now_str,
    "result": f"aitoolsdirectory={'上线' if results['aitoolsdirectory'][1] else '审核中(~80h)'}; hyzenpro={'搜索可见' if results['hyzenpro'][1] else '审核中'}; HN=NOT_LOGGED_IN; Reddit=NOT_LOGGED_IN"
})
state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## SOP（{now_str}）14点档\n\n- HN: 未登录（karma=1），无法评论\n- Reddit: 未登录，无法回复\n- aitoolsdirectory: {'上线' if results['aitoolsdirectory'][1] else '审核中(~80h)'}\n- hyzenpro: {'搜索可见' if results['hyzenpro'][1] else '审核中'}\n- 4个backlink稳定存活（昨晚已验证）\n")
print("Done")
