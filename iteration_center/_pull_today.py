# -*- coding: utf-8 -*-
"""拉今天 + 昨天的 GA4 数据 - 2026-10-09"""
import os, json
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"

from datetime import datetime, timedelta
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
SA = os.path.join(BASE, ".secrets", "gsc-service-account.json")
PROP = "properties/556518278"

creds = service_account.Credentials.from_service_account_file(
    SA, scopes=["https://www.googleapis.com/auth/analytics.readonly"]
)
data = BetaAnalyticsDataClient(credentials=creds)

today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)
print(f"[today UTC] {today}  [yesterday] {yesterday}")

for label, sd, ed in [("TODAY", str(today), str(today)),
                       ("YESTERDAY", str(yesterday), str(yesterday))]:
    print(f"\n=== {label} ({sd} ~ {ed}) ===")
    req = RunReportRequest(
        property=PROP,
        date_ranges=[DateRange(start_date=sd, end_date=ed)],
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
    if not r.rows:
        print("  [NO DATA]")
        continue
    vals = [m.value for m in r.rows[0].metric_values]
    names = ["sessions","totalUsers","newUsers","engagedSessions","screenPageViews","avgDuration"]
    for n, v in zip(names, vals):
        print(f"  {n}: {v}")

    # landing page 分布
    req2 = RunReportRequest(
        property=PROP,
        date_ranges=[DateRange(start_date=sd, end_date=ed)],
        dimensions=[Dimension(name="landingPage")],
        metrics=[Metric(name="sessions"), Metric(name="engagedSessions")],
        limit=10,
    )
    r2 = data.run_report(req2)
    print(f"  --- landing pages ---")
    for row in r2.rows:
        p = row.dimension_values[0].value
        sess = row.metric_values[0].value
        eng = row.metric_values[1].value
        print(f"  {p:<45} sess={sess} engaged={eng}")

    # 流量来源
    req3 = RunReportRequest(
        property=PROP,
        date_ranges=[DateRange(start_date=sd, end_date=ed)],
        dimensions=[Dimension(name="sessionSource"), Dimension(name="sessionMedium")],
        metrics=[Metric(name="sessions")],
        limit=10,
    )
    r3 = data.run_report(req3)
    print(f"  --- traffic sources ---")
    for row in r3.rows:
        src = row.dimension_values[0].value
        med = row.dimension_values[1].value
        sess = row.metric_values[0].value
        print(f"  {src:<25} {med:<15} sess={sess}")
