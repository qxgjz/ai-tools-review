# -*- coding: utf-8 -*-
"""r33 P0-INDEX-SNAPSHOT-RERUN: 重拉 GSC 索引报告页快照（恢复周度收录跟踪）
输出 gsc-ga4-report/indexing_snapshot_20261027.json + 更新 gsc_indexed_baseline"""
import json, os, sys
from datetime import datetime

CRED = r"C:\Users\通明街\Downloads\aitoolcrux-automation-2f297efa91fb.json"
SITE = "sc-domain:aitoolcrux.com"
SITE_PLAIN = "https://www.aitoolcrux.com/"
START, END = "2026-09-26", "2026-10-25"
P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

def get_token(cred_path):
    # 与 fetch_gsc.py 一致的 jwt+requests 方式（google 库未安装）
    import time, jwt, requests
    with open(cred_path, "r", encoding="utf-8") as f:
        cred_data = json.load(f)
    now = int(time.time())
    payload = {
        "iss": cred_data["client_email"],
        "scope": " ".join(["https://www.googleapis.com/auth/webmasters.readonly"]),
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now, "exp": now + 3600,
    }
    token = jwt.encode(payload, cred_data["private_key"], algorithm="RS256")
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": token,
    }, proxies=PROXY, timeout=30)
    return r.json()["access_token"]

PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

def api_get(path, token, method="GET", body=None):
    import requests
    url = f"https://www.googleapis.com/webmasters/v3{path}"
    r = requests.request(method, url, json=body,
        headers={"Authorization": f"Bearer {token}"}, proxies=PROXY, timeout=40)
    r.raise_for_status()
    return r.json()

token = get_token(CRED)
out = {"pulled_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "site": SITE, "window": f"{START}~{END}"}

# 1. Sitemaps API（Google 报告收录；sitemaps 端点=webmasters/v3/sites/{site}/sitemaps，需具体站点属性+URL编码）
from urllib.parse import quote
SITEMAP_SITE = quote(SITE_PLAIN, safe='')
try:
    sm = api_get(f"/sites/{SITEMAP_SITE}/sitemaps", token)
    entries = sm.get("sitemap", [])
    tot_sub, tot_idx = 0, 0
    sm_rows = []
    for e in entries:
        cont = e.get("contents", [{}])[0]
        sub, idx = cont.get("submitted", 0), cont.get("indexed", 0)
        tot_sub += sub; tot_idx += idx
        sm_rows.append({"path": e.get("path"), "submitted": sub, "indexed": idx})
    out["sitemaps"] = {"submitted": tot_sub, "indexed": tot_idx, "entries": sm_rows}
    print(f"sitemaps: submitted={tot_sub} indexed={tot_idx}")
except Exception as ex:
    out["sitemaps"] = {"error": str(ex)}
    print("sitemaps 失败:", ex)

# 2. searchAnalytics 有曝光 URL 数（有效收录近似）
try:
    body = {"startDate": START, "endDate": END, "dimensions": ["page"], "rowLimit": 25000}
    rows = api_get(f"/sites/{SITE}/searchAnalytics/query", token, method="POST", body=body).get("rows", [])
    out["active_pages"] = len(rows)
    print(f"有曝光 URL: {len(rows)}")
except Exception as ex:
    out["active_pages"] = -1
    print("searchAnalytics 失败:", ex)

# 3. URL Inspection 抽样
samples = [
    "https://www.aitoolcrux.com/",
    "https://www.aitoolcrux.com/blog/best-ai-voice-changers-2026",
    "https://www.aitoolcrux.com/tools/ailice",
    "https://www.aitoolcrux.com/alternatives/cursor-alternatives",
    "https://www.aitoolcrux.com/blog/best-ai-coding-tools-2026",
]
insp = []
try:
    for u in samples:
        try:
            import requests as _rq
            rr = _rq.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                json={"inspectionUrl": u, "siteUrl": SITE_PLAIN},
                headers={"Authorization": f"Bearer {token}"}, proxies=PROXY, timeout=40)
            rr.raise_for_status()
            r = rr.json()
            st = r.get("inspectionResult", {}).get("indexStatusResult", {})
            insp.append({"url": u, "coverageState": st.get("coverageState", "?"),
                         "lastCrawl": st.get("lastCrawlTime", "?")})
            print(f"  {u.split('/')[-1] or 'home'} | {st.get('coverageState','?')}")
        except Exception as e2:
            insp.append({"url": u, "error": str(e2)[:100]})
except Exception as ex:
    print("inspection 失败:", ex)
out["inspection_samples"] = insp

with open(os.path.join(P, "gsc-ga4-report", "indexing_snapshot_20261027.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("snapshot saved")
