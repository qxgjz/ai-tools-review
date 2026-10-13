# -*- coding: utf-8 -*-
"""带代理的 GSC 实时拉取 - 2026-10-09"""
import os, json
from datetime import datetime, timedelta
import httplib2
import socks
from google.oauth2 import service_account
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
SA = os.path.join(BASE, ".secrets", "gsc-service-account.json")

PROXY = httplib2.ProxyInfo(
    proxy_type=socks.PROXY_TYPE_HTTP,
    proxy_host="127.0.0.1",
    proxy_port=7890,
)

def make_http():
    return httplib2.Http(proxy_info=PROXY, timeout=30)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
creds = service_account.Credentials.from_service_account_file(SA, scopes=SCOPES)
authed = AuthorizedHttp(creds, http=make_http())

gsc = build("searchconsole", "v1", http=authed, cache_discovery=False)

print("[1] listing sites...")
sites = gsc.sites().list().execute()
entries = sites.get("siteEntry", [])
print(f"    accessible sites: {len(entries)}")
for s in entries:
    print(f"      - {s.get('siteUrl')}  permission={s.get('permissionLevel')}")

if not entries:
    raise SystemExit("no site accessible")

target = entries[0]["siteUrl"]
print(f"\n[2] using site: {target}")

end = datetime.utcnow().date() - timedelta(days=3)
start = end - timedelta(days=6)
print(f"[3] daily trend {start} ~ {end}")

resp = gsc.searchanalytics().query(siteUrl=target, body={
    "startDate": str(start), "endDate": str(end),
    "dimensions": ["date"], "rowLimit": 100,
}).execute()
rows = resp.get("rows", [])
print(f"    {'date':<12}{'clk':>5}{'impr':>7}{'ctr':>8}{'pos':>7}")
for r in rows:
    print(f"    {r['keys'][0]:<12}{r.get('clicks',0):>5}{r.get('impressions',0):>7}{r.get('ctr',0)*100:>7.2f}%{r.get('position',0):>7.1f}")

# 28 天 top queries
qend = datetime.utcnow().date() - timedelta(days=3)
qstart = qend - timedelta(days=27)
print(f"\n[4] top queries {qstart} ~ {qend}")
qresp = gsc.searchanalytics().query(siteUrl=target, body={
    "startDate": str(qstart), "endDate": str(qend),
    "dimensions": ["query"], "rowLimit": 20,
}).execute()
print(f"    {'query':<70}{'clk':>4}{'impr':>6}{'pos':>6}")
for r in qresp.get("rows", []):
    q = r["keys"][0]
    if len(q) > 68: q = q[:65] + "..."
    print(f"    {q:<70}{r.get('clicks',0):>4}{r.get('impressions',0):>6}{r.get('position',0):>6.1f}")

# top pages
print(f"\n[5] top pages {qstart} ~ {qend}")
presp = gsc.searchanalytics().query(siteUrl=target, body={
    "startDate": str(qstart), "endDate": str(qend),
    "dimensions": ["page"], "rowLimit": 15,
}).execute()
for r in presp.get("rows", []):
    p = r["keys"][0].replace("https://www.aitoolcrux.com", "")
    print(f"    {p:<60} clk={r.get('clicks',0)} impr={r.get('impressions',0)} pos={r.get('position',0):.1f}")

# 保存原始 JSON 供后续分析
out = {
    "site": target,
    "daily_start": str(start), "daily_end": str(end),
    "daily": rows,
    "query_window_start": str(qstart), "query_window_end": str(qend),
    "top_queries": qresp.get("rows", []),
    "top_pages": presp.get("rows", []),
    "pulled_at": datetime.now().isoformat(),
}
out_path = os.path.join(BASE, "gsc-ga4-report", f"live_pull_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"\n[OK] raw data saved: {out_path}")
