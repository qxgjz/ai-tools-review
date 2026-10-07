#!/usr/bin/env python3
"""
GSC Data Fetcher (CI + local version)
Fetches Google Search Console search analytics for aitoolcrux.com.
Uses service account JSON from GOOGLE_SERVICE_ACCOUNT_JSON env var or local file.
Outputs report to gsc-ga4-report/ directory.
"""
import json
import os
import sys
import time
import requests
import jwt
from datetime import datetime, timedelta, timezone

SITE_URL = "sc-domain:aitoolcrux.com"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
OUTPUT_DIR = os.path.join(os.environ.get("GITHUB_WORKSPACE", "."), "gsc-ga4-report")

# Local proxy (only used when running locally, not in CI)
PROXY = None
if not os.environ.get("GITHUB_ACTIONS"):
    # Local dev - use proxy if available
    proxy_url = os.environ.get("HTTPS_PROXY", "http://127.0.0.1:7890")
    PROXY = {"http": proxy_url, "https": proxy_url}


def get_token():
    cred_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if cred_json:
        cred_data = json.loads(cred_json)
    else:
        # Local: read from file
        local_path = r"C:\Users\通明街\Downloads\aitoolcrux-automation-2f297efa91fb.json"
        if not os.path.exists(local_path):
            print("ERROR: No service account JSON found")
            sys.exit(1)
        with open(local_path, "r", encoding="utf-8") as f:
            cred_data = json.load(f)

    now = int(time.time())
    payload = {
        "iss": cred_data["client_email"],
        "scope": " ".join(SCOPES),
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now, "exp": now + 3600,
    }
    token = jwt.encode(payload, cred_data["private_key"], algorithm="RS256")
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": token,
    }, proxies=PROXY, timeout=30)
    return r.json()["access_token"]


def gsc_query(token, body):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{SITE_URL}/searchAnalytics/query"
    r = requests.post(url, headers={"Authorization": f"Bearer {token}"}, json=body, proxies=PROXY, timeout=30)
    return r.json()


def main():
    print("Fetching GSC data...")
    token = get_token()

    end_date = datetime.now(timezone.utc).date() - timedelta(days=2)
    start_date = end_date - timedelta(days=29)
    prev_end = start_date - timedelta(days=1)
    prev_start = prev_end - timedelta(days=29)

    base = {"dimensions": [], "rowLimit": 10}

    # Totals
    base["startDate"] = start_date.isoformat()
    base["endDate"] = end_date.isoformat()
    totals = gsc_query(token, base)
    rows = totals.get("rows", [])
    clicks = rows[0]["clicks"] if rows else 0
    impressions = rows[0]["impressions"] if rows else 0
    ctr = rows[0]["ctr"] if rows else 0
    position = rows[0]["position"] if rows else 0

    # Previous period
    base["startDate"] = prev_start.isoformat()
    base["endDate"] = prev_end.isoformat()
    prev = gsc_query(token, base)
    prev_rows = prev.get("rows", [])
    prev_clicks = prev_rows[0]["clicks"] if prev_rows else 0
    prev_impressions = prev_rows[0]["impressions"] if prev_rows else 0

    # Top pages
    base["startDate"] = start_date.isoformat()
    base["endDate"] = end_date.isoformat()
    base["dimensions"] = ["page"]
    base["rowLimit"] = 20
    top_pages = gsc_query(token, base)

    # Top queries
    base["dimensions"] = ["query"]
    top_queries = gsc_query(token, base)

    # By device
    base["dimensions"] = ["device"]
    base["rowLimit"] = 10
    by_device = gsc_query(token, base)

    # Daily trend
    base["dimensions"] = ["date"]
    base["rowLimit"] = 100
    daily = gsc_query(token, base)

    # Build report
    report = f"""# GSC Report: aitoolcrux.com

Period: {start_date} to {end_date}
Generated: {datetime.now(timezone.utc).isoformat()}

## Summary

| Metric | This Period | Previous Period | Change |
|--------|------------|-----------------|--------|
| Clicks | {clicks} | {prev_clicks} | {clicks - prev_clicks:+d} |
| Impressions | {impressions} | {prev_impressions} | {impressions - prev_impressions:+d} |
| CTR | {ctr*100:.2f}% | - | - |
| Avg Position | {position:.2f} | - | - |

## Top Pages

| Page | Clicks | Impressions | CTR | Position |
|------|--------|-------------|-----|----------|
"""
    for r in top_pages.get("rows", []):
        page = r["keys"][0].replace("https://www.aitoolcrux.com", "")
        report += f"| {page} | {r['clicks']} | {r['impressions']} | {r['ctr']*100:.1f}% | {r['position']:.1f} |\n"

    report += "\n## Top Queries\n\n| Query | Clicks | Impressions | CTR | Position |\n|-------|--------|-------------|-----|----------|\n"
    for r in top_queries.get("rows", []):
        report += f"| {r['keys'][0]} | {r['clicks']} | {r['impressions']} | {r['ctr']*100:.1f}% | {r['position']:.1f} |\n"

    report += "\n## By Device\n\n| Device | Clicks | Impressions | Avg Position |\n|--------|--------|-------------|---------------|\n"
    for r in by_device.get("rows", []):
        report += f"| {r['keys'][0]} | {r['clicks']} | {r['impressions']} | {r['position']:.2f} |\n"

    report += "\n## Daily Trend\n\n| Date | Clicks | Impressions |\n|------|--------|-------------|\n"
    for r in daily.get("rows", []):
        report += f"| {r['keys'][0]} | {r['clicks']} | {r['impressions']} |\n"

    report += f"\n---\n*Generated by gsc-fetch workflow*\n"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{start_date}_{end_date}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved: {filepath}")
    print(f"Clicks: {clicks}, Impressions: {impressions}, CTR: {ctr*100:.2f}%, Pos: {position:.2f}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
