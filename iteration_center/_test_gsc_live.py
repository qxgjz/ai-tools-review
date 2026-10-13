# -*- coding: utf-8 -*-
import json, os, sys
from datetime import datetime, timedelta

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
SA = os.path.join(BASE, ".secrets", "gsc-service-account.json")
print("[1] SA exists:", os.path.exists(SA), "size:", os.path.getsize(SA))

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
creds = service_account.Credentials.from_service_account_file(SA, scopes=SCOPES)
gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

sites = gsc.sites().list().execute()
entries = sites.get("siteEntry", [])
print("[2] accessible sites:", len(entries))
for s in entries:
    print("   -", s.get("siteUrl"), s.get("permissionLevel"))

if not entries:
    print("[BLOCKED] service account not added to any GSC property yet")
    sys.exit(0)

target = entries[0]["siteUrl"]
end = datetime.utcnow().date() - timedelta(days=3)
start = end - timedelta(days=6)
print(f"[3] daily trend {start} ~ {end} on {target}")

resp = gsc.searchanalytics().query(siteUrl=target, body={
    "startDate": str(start), "endDate": str(end),
    "dimensions": ["date"], "rowLimit": 100
}).execute()
rows = resp.get("rows", [])
print(f"    {'date':<12}{'clk':>5}{'impr':>7}{'ctr':>8}{'pos':>7}")
for r in rows:
    print(f"    {r['keys'][0]:<12}{r.get('clicks',0):>5}{r.get('impressions',0):>7}{r.get('ctr',0)*100:>7.2f}%{r.get('position',0):>7.1f}")

qend = datetime.utcnow().date() - timedelta(days=3)
qstart = qend - timedelta(days=27)
print(f"\n[4] top queries {qstart} ~ {qend}")
qresp = gsc.searchanalytics().query(siteUrl=target, body={
    "startDate": str(qstart), "endDate": str(qend),
    "dimensions": ["query"], "rowLimit": 15
}).execute()
for r in qresp.get("rows", []):
    q = r["keys"][0]
    if len(q) > 65: q = q[:62] + "..."
    print(f"    {q:<68} clk={r.get('clicks',0)} impr={r.get('impressions',0)} pos={r.get('position',0):.1f}")

print("\n[OK] GSC live pull verified")
