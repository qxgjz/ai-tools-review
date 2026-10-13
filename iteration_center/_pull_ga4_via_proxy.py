# -*- coding: utf-8 -*-
"""GA4 实时拉取 - 2026-10-09"""
import os, json
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"

from datetime import datetime, timedelta
from google.oauth2 import service_account
from google.analytics.admin_v1beta import AnalyticsAdminServiceClient
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
SA = os.path.join(BASE, ".secrets", "gsc-service-account.json")

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/webmasters.readonly",
]
creds = service_account.Credentials.from_service_account_file(SA, scopes=SCOPES)

print("[1] listing GA4 account summaries...")
admin = AnalyticsAdminServiceClient(credentials=creds)
try:
    resp = admin.list_account_summaries({})
    accounts = list(resp)
    print(f"    accessible accounts: {len(accounts)}")
    all_props = []
    for acc in accounts:
        print(f"    account: {acc.account} ({acc.display_name})")
        for p in acc.property_summaries:
            print(f"      property: {p.property} ({p.display_name})")
            all_props.append(p.property)
except Exception as e:
    print(f"    admin list FAIL: {type(e).__name__}: {str(e)[:300]}")
    all_props = []

if not all_props:
    # 直接试 measurement ID 对应的 property（G-7XYFQR3ETF）
    print("\n[!] no properties listed via admin API.")
    print("    可能原因: 服务账号未被加到 GA4 属性的用户列表")
    print("    下一步: GA4 -> 管理 -> 属性访问管理 -> 添加使用者 -> aitoolcrux-bot@aitoolcrux-automation.iam.gserviceaccount.com")
    raise SystemExit(0)

# 明确选 aitoolcrux property（自动发现时第一个是 ToolHub，不是我们要的）
prop = "properties/556518278"
print(f"\n[2] using property: {prop} (aitoolcrux)")

data = BetaAnalyticsDataClient(credentials=creds)
end = datetime.utcnow().date() - timedelta(days=2)
start = end - timedelta(days=27)
print(f"[3] report {start} ~ {end}")

# 总览
req = RunReportRequest(
    property=prop,
    date_ranges=[DateRange(start_date=str(start), end_date=str(end))],
    metrics=[
        Metric(name="sessions"),
        Metric(name="totalUsers"),
        Metric(name="newUsers"),
        Metric(name="engagedSessions"),
        Metric(name="screenPageViews"),
        Metric(name="averageSessionDuration"),
    ],
)
r = data.run_report(req)
print("\n    === 28d overview ===")
if not r.rows:
    print("    [NO DATA] 0 rows returned - GA4 可能没装 gtag 或没流量")
else:
    row = r.rows[0]
    headers = ["sessions", "totalUsers", "newUsers", "engagedSessions", "screenPageViews", "averageSessionDuration"]
    vals = [m.value for m in row.metric_values]
    for h, v in zip(headers, vals):
        print(f"    {h}: {v}")

# 每日趋势
req2 = RunReportRequest(
    property=prop,
    date_ranges=[DateRange(start_date=str(end - timedelta(days=13)), end_date=str(end))],
    dimensions=[Dimension(name="date")],
    metrics=[Metric(name="sessions"), Metric(name="totalUsers"), Metric(name="engagedSessions")],
)
r2 = data.run_report(req2)
print(f"\n    === 14d daily ===")
print(f"    {'date':<12}{'sess':>6}{'users':>7}{'engaged':>8}")
for row in r2.rows:
    d = row.dimension_values[0].value
    d = f"{d[:4]}-{d[4:6]}-{d[6:]}"
    sess = row.metric_values[0].value
    users = row.metric_values[1].value
    eng = row.metric_values[2].value
    print(f"    {d:<12}{sess:>6}{users:>7}{eng:>8}")

# top landing pages
req3 = RunReportRequest(
    property=prop,
    date_ranges=[DateRange(start_date=str(start), end_date=str(end))],
    dimensions=[Dimension(name="landingPage")],
    metrics=[Metric(name="sessions"), Metric(name="engagedSessions")],
    limit=15,
)
r3 = data.run_report(req3)
print(f"\n    === top landing pages (28d) ===")
for row in r3.rows:
    p = row.dimension_values[0].value
    sess = row.metric_values[0].value
    eng = row.metric_values[1].value
    print(f"    {p:<50} sess={sess} engaged={eng}")

# 保存
out = {
    "property": prop,
    "window": f"{start}~{end}",
    "overview": dict(zip(["sessions","totalUsers","newUsers","engagedSessions","screenPageViews","averageSessionDuration"], [m.value for m in r.rows[0].metric_values])) if r.rows else {},
    "daily": [
        {"date": row.dimension_values[0].value,
         "sessions": row.metric_values[0].value,
         "users": row.metric_values[1].value,
         "engaged": row.metric_values[2].value}
        for row in r2.rows
    ],
    "top_landing": [
        {"page": row.dimension_values[0].value,
         "sessions": row.metric_values[0].value,
         "engaged": row.metric_values[1].value}
        for row in r3.rows
    ],
}
out_path = os.path.join(BASE, "gsc-ga4-report", f"ga4_live_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"\n[OK] saved: {out_path}")
