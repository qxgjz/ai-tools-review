#!/usr/bin/env python3
"""Index monitor: track Google indexed pages count weekly."""
import json
import os
import sys
from datetime import datetime, timezone

import httpx

SITE_URL = "sc-domain:aitoolcrux.com"
SITE_URL_PREFIX = "https://www.aitoolcrux.com/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
OUTPUT_FILE = os.path.join(
    os.environ.get("GITHUB_WORKSPACE", "."),
    "iteration_center", "index_monitor.md"
)


def get_gsc_service():
    cred_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not cred_json:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON not set")
        return None

    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    cred_data = json.loads(cred_json)
    credentials = service_account.Credentials.from_service_account_info(
        cred_data, scopes=SCOPES
    )
    return build("searchconsole", "v1", credentials=credentials, cache_discovery=False)


def get_gsc_indexed_count(service):
    """Get total indexed URL count from GSC (URL inspection or search analytics)."""
    try:
        # Use search analytics to get total clicks/impressions and page count
        request = {
            "startDate": (datetime.now(timezone.utc).date().replace(day=1)).isoformat(),
            "endDate": datetime.now(timezone.utc).date().isoformat(),
            "dimensions": ["page"],
            "rowLimit": 1000,
        }
        response = service.searchanalytics().query(
            siteUrl=SITE_URL, body=request
        ).execute()

        rows = response.get("rows", [])
        return len(rows), rows
    except Exception as e:
        print(f"GSC query error: {e}")
        # Try with www prefix
        try:
            request["siteUrl"] = SITE_URL_PREFIX
            response = service.searchanalytics().query(
                siteUrl=SITE_URL_PREFIX, body=request
            ).execute()
            rows = response.get("rows", [])
            return len(rows), rows
        except Exception as e2:
            print(f"GSC query error (www): {e2}")
            return -1, []


def get_site_query_estimate():
    """Estimate indexed pages via Bing/DuckDuckGo as fallback."""
    try:
        # DuckDuckGo HTML search as fallback
        r = httpx.get(
            "https://html.duckduckgo.com/html/",
            params={"q": "site:aitoolcrux.com"},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        if r.status_code == 200:
            import re
            m = re.search(r'About ([\d,]+) results', r.text)
            if m:
                return int(m.group(1).replace(",", ""))
        return -1
    except Exception as e:
        print(f"Site query error: {e}")
        return -1


def read_previous_report():
    """Read last line from existing report."""
    if not os.path.exists(OUTPUT_FILE):
        return None
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Find last data row
    for line in reversed(lines):
        if "|" in line and "---" not in line and "日期" not in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3:
                try:
                    return int(parts[1])
                except ValueError:
                    pass
    return None


def main():
    print("=== Index Monitor ===")

    # Get GSC indexed count
    service = get_gsc_service()
    gsc_count = -1
    if service:
        gsc_count, rows = get_gsc_indexed_count(service)
        print(f"GSC active pages this month: {gsc_count}")

    # Get site: query estimate
    site_count = get_site_query_estimate()
    print(f"site:aitoolcrux.com estimate: {site_count}")

    # Read previous
    prev_gsc = read_previous_report()
    change = gsc_count - prev_gsc if (prev_gsc and gsc_count >= 0) else "N/A"

    # Build report line
    today = datetime.now().strftime("%Y-%m-%d")
    note = ""
    if change != "N/A":
        if change > 0:
            note = f"📈 +{change} new indexed"
        elif change < 0:
            note = f"📉 {change} lost"
        else:
            note = "No change"

    line = f"| {today} | {gsc_count} | {site_count} | {change} | {note} |"

    # Write report (create header if new)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    is_new = not os.path.exists(OUTPUT_FILE)

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        if is_new:
            f.write("# Google Index Monitor\n\n")
            f.write("Weekly tracking of indexed pages on aitoolcrux.com.\n\n")
            f.write("| 日期 | GSC收录数 | site:查询数 | 上周变化 | 备注 |\n")
            f.write("|------|-----------|-------------|----------|------|\n")
        f.write(line + "\n")

    print(f"\n✅ Report updated: {OUTPUT_FILE}")
    print(f"   {line}")


if __name__ == "__main__":
    main()
