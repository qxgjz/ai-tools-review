#!/usr/bin/env python3
"""
GA4 Data Fetcher (CI version)
Fetches Google Analytics 4 data for aitoolcrux.com (property 556518278).
Uses service account JSON from GOOGLE_SERVICE_ACCOUNT_JSON env var.
Outputs report to gsc-ga4-report/ directory.
Runs in GitHub Actions (US node, no proxy needed).
"""
import json
import os
import sys
import time
import requests
import jwt
from datetime import datetime, timedelta, timezone

PROPERTY_ID = "556518278"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
OUTPUT_DIR = os.path.join(os.environ.get("GITHUB_WORKSPACE", "."), "gsc-ga4-report")

# No proxy in CI; local runs should set HTTPS_PROXY if needed
PROXY = None
if not os.environ.get("GITHUB_ACTIONS"):
    proxy_url = os.environ.get("HTTPS_PROXY", "http://127.0.0.1:7890")
    PROXY = {"http": proxy_url, "https": proxy_url}


def get_token():
    cred_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if cred_json:
        cred_data = json.loads(cred_json)
    else:
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
    r.raise_for_status()
    return r.json()["access_token"]


def ga4_run_report(token, body):
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport"
    r = requests.post(url, headers={"Authorization": f"Bearer {token}"}, json=body, proxies=PROXY, timeout=60)
    if r.status_code != 200:
        print(f"GA4 API error {r.status_code}: {r.text[:500]}")
    r.raise_for_status()
    return r.json()


def rows_to_dicts(resp):
    """Convert GA4 response rows to list of dicts with metric names."""
    if not resp.get("rows"):
        return []
    headers = [h["name"] for h in resp.get("dimensionHeaders", [])]
    metric_names = [m["name"] for m in resp.get("metricHeaders", [])]
    out = []
    for row in resp["rows"]:
        d = {}
        for i, v in enumerate(row.get("dimensionValues", [])):
            d[headers[i]] = v["value"]
        for i, v in enumerate(row.get("metricValues", [])):
            d[metric_names[i]] = v["value"]
        out.append(d)
    return out


def main():
    print("Fetching GA4 data...")
    token = get_token()

    end_date = datetime.now(timezone.utc).date() - timedelta(days=2)
    start_date = end_date - timedelta(days=27)

    # --- Overview: 28d totals ---
    overview_body = {
        "dateRanges": [{"startDate": start_date.isoformat(), "endDate": end_date.isoformat()}],
        "metrics": [
            {"name": "sessions"},
            {"name": "totalUsers"},
            {"name": "newUsers"},
            {"name": "engagedSessions"},
            {"name": "engagementRate"},
            {"name": "averageSessionDuration"},
            {"name": "screenPageViews"},
            {"name": "keyEvents"},
        ],
    }
    overview = ga4_run_report(token, overview_body)
    ov = rows_to_dicts(overview)

    # --- Daily trend: 28d by date ---
    daily_body = {
        "dateRanges": [{"startDate": start_date.isoformat(), "endDate": end_date.isoformat()}],
        "dimensions": [{"name": "date"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "totalUsers"},
            {"name": "engagedSessions"},
            {"name": "keyEvents"},
        ],
        "orderBys": [{"dimension": {"dimensionName": "date", "orderType": "ASCENDING"}}],
    }
    daily_resp = ga4_run_report(token, daily_body)
    daily = rows_to_dicts(daily_resp)

    # --- Top landing pages ---
    landing_body = {
        "dateRanges": [{"startDate": start_date.isoformat(), "endDate": end_date.isoformat()}],
        "dimensions": [{"name": "landingPage"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "engagedSessions"},
            {"name": "engagementRate"},
        ],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 15,
    }
    landing_resp = ga4_run_report(token, landing_body)
    landing = rows_to_dicts(landing_resp)

    # --- Traffic source breakdown ---
    source_body = {
        "dateRanges": [{"startDate": start_date.isoformat(), "endDate": end_date.isoformat()}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}],
        "metrics": [{"name": "sessions"}, {"name": "engagedSessions"}, {"name": "keyEvents"}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 10,
    }
    source_resp = ga4_run_report(token, source_body)
    source = rows_to_dicts(source_resp)

    # --- Save raw JSON ---
    raw = {
        "property_id": PROPERTY_ID,
        "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overview": ov,
        "daily": daily,
        "landing_pages": landing,
        "channels": source,
    }
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    raw_path = os.path.join(OUTPUT_DIR, f"ga4_live_{ts}.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)

    # --- Build markdown report ---
    def g(rows, key, default="0"):
        return rows[0].get(key, default) if rows else default

    sessions = g(ov, "sessions")
    users = g(ov, "totalUsers")
    engaged = g(ov, "engagedSessions")
    eng_rate = g(ov, "engagementRate")
    avg_dur = g(ov, "averageSessionDuration")
    pageviews = g(ov, "screenPageViews")
    key_events = g(ov, "keyEvents")

    # format engagement rate (0.079 -> 7.9%)
    try:
        eng_rate_pct = f"{float(eng_rate)*100:.1f}%"
    except ValueError:
        eng_rate_pct = eng_rate
    try:
        avg_dur_s = f"{float(avg_dur):.1f}s"
    except ValueError:
        avg_dur_s = avg_dur

    report = f"""# GA4 Report: aitoolcrux.com (property {PROPERTY_ID})

Period: {start_date} to {end_date}
Generated: {datetime.now(timezone.utc).isoformat()}

## Summary

| Metric | Value |
|--------|-------|
| Sessions | {sessions} |
| Total Users | {users} |
| Engaged Sessions | {engaged} |
| Engagement Rate | {eng_rate_pct} |
| Avg Session Duration | {avg_dur_s} |
| Screen Page Views | {pageviews} |
| Key Events | {key_events} |

## Daily Trend

| Date | Sessions | Users | Engaged | Key Events |
|------|----------|-------|---------|------------|
"""
    for r in daily:
        report += f"| {r.get('date','')} | {r.get('sessions','0')} | {r.get('totalUsers','0')} | {r.get('engagedSessions','0')} | {r.get('keyEvents','0')} |\n"

    report += "\n## Top Landing Pages\n\n| Page | Sessions | Engaged | Engagement Rate |\n|------|----------|---------|-----------------|\n"
    for r in landing:
        er = r.get("engagementRate", "0")
        try:
            er = f"{float(er)*100:.1f}%"
        except ValueError:
            pass
        report += f"| {r.get('landingPage','(not set)')} | {r.get('sessions','0')} | {r.get('engagedSessions','0')} | {er} |\n"

    report += "\n## By Channel\n\n| Channel | Sessions | Engaged | Key Events |\n|---------|----------|---------|------------|\n"
    for r in source:
        report += f"| {r.get('sessionDefaultChannelGroup','(not set)')} | {r.get('sessions','0')} | {r.get('engagedSessions','0')} | {r.get('keyEvents','0')} |\n"

    report += f"\n---\n*Generated by ga4-fetch workflow*\n"

    md_path = os.path.join(OUTPUT_DIR, f"ga4_{start_date}_{end_date}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Raw saved: {raw_path}")
    print(f"Report saved: {md_path}")
    print(f"Sessions: {sessions}, Users: {users}, Engaged: {engaged}, KeyEvents: {key_events}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
