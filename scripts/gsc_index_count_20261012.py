# -*- coding: utf-8 -*-
"""GSC 收录统计：Sitemaps API indexed 数 + URL 检查抽样 + 有曝光URL数"""
import json, os, sys

CRED = r"C:\Users\通明街\Downloads\aitoolcrux-automation-2f297efa91fb.json"
SITE = "sc-domain:aitoolcrux.com"
SITE_PLAIN = "https://www.aitoolcrux.com/"

def get_token(cred_path):
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)
    creds.refresh(Request())
    return creds.token

def api_get(path, token):
    import urllib.request
    url = f"https://www.googleapis.com/webmasters/v3{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

token = get_token(CRED)
print("=== 1. Sitemaps（Google 报告的收录数）===")
try:
    sm = api_get(f"/sitemaps/{SITE}", token)
    entries = sm.get("sitemap", [])
    if not entries:
        print("无已提交 sitemap")
    tot_idx = 0
    for e in entries:
        path = e.get("path")
        cont = e.get("contents", [{}])[0]
        sub = cont.get("submitted", 0)
        idx = cont.get("indexed", 0)
        tot_idx += idx
        print(f"  {path} | 提交 {sub} | 收录 {idx} | 最后提交 {e.get('lastSubmitted','')}")
    print(f"  >>> sitemap 报告总收录: {tot_idx}")
except Exception as ex:
    print("  sitemaps 调用失败:", ex)

print("\n=== 2. 有曝光/点击的 URL 数（GSC 认可的有效收录近似）===")
try:
    import urllib.request
    body = json.dumps({
        "startDate": "2026-09-09", "endDate": "2026-10-09",
        "dimensions": ["page"], "rowLimit": 25000
    }).encode()
    req = urllib.request.Request(
        f"https://www.googleapis.com/webmasters/v3/sites/{SITE}/searchAnalytics/query",
        data=body, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        rows = json.loads(r.read().decode("utf-8")).get("rows", [])
    print(f"  28 天窗口有曝光/点击的 URL 数: {len(rows)}")
except Exception as ex:
    print("  searchAnalytics 调用失败:", ex)

print("\n=== 3. URL Inspection 抽样（首页/文章/工具/对比各1个）===")
samples = [
    "https://www.aitoolcrux.com/",
    "https://www.aitoolcrux.com/blog/best-ai-voice-changers-2026",
    "https://www.aitoolcrux.com/tools/ailice",
    "https://www.aitoolcrux.com/alternatives/cursor-alternatives",
]
try:
    for u in samples:
        req = urllib.request.Request(
            f"https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
            data=json.dumps({"inspectionUrl": u, "siteUrl": SITE}).encode(),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode("utf-8"))
            st = d.get("inspectionResult", {}).get("indexStatusResult", {})
            print(f"  {u} | {st.get('coverageState','?')} | {st.get('robotsTxtState','?')} | {st.get('crawledAs','?')} | 上次抓取 {st.get('lastCrawlTime','?')}")
        except urllib.error.HTTPError as he:
            print(f"  {u} | HTTP {he.code}: {he.read().decode()[:200]}")
except Exception as ex:
    print("  URL inspection 失败:", ex)
