# -*- coding: utf-8 -*-
"""用户画像深度分析 - 2026-10-09"""
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

end = datetime.utcnow().date() - timedelta(days=1)  # 昨天，数据更完整
start = end - timedelta(days=27)
print(f"[window] {start} ~ {end} (28d)")

def run(title, dims, mets, limit=15):
    print(f"\n=== {title} ===")
    req = RunReportRequest(
        property=PROP,
        date_ranges=[DateRange(start_date=str(start), end_date=str(end))],
        dimensions=[Dimension(name=d) for d in dims],
        metrics=[Metric(name=m) for m in mets],
        limit=limit,
    )
    r = data.run_report(req)
    for row in r.rows:
        vals = [d.value for d in row.dimension_values] + [m.value for m in row.metric_values]
        print("  " + " | ".join(vals))
    return r.rows

# 1. 设备类型
run("Device Category", ["deviceCategory"],
    ["sessions","totalUsers","engagedSessions","screenPageViews","averageSessionDuration"])

# 2. 国家
run("Country (top 15)", ["country"],
    ["sessions","totalUsers","engagedSessions"], limit=15)

# 3. 流量来源 + 媒介
run("Traffic Source x Medium", ["sessionSource","sessionMedium"],
    ["sessions","totalUsers","engagedSessions"], limit=20)

# 4. 浏览器
run("Browser", ["browser"],
    ["sessions","engagedSessions"], limit=10)

# 5. 页面浏览深度分布（用 sessions per page view 近似）
run("Page Path (top 20 by pageviews)", ["pagePath"],
    ["screenPageViews","sessions","engagedSessions"], limit=20)

# 6. 新老用户
run("New vs Returning", ["newVsReturning"],
    ["sessions","totalUsers","engagedSessions","averageSessionDuration"])

# 7. 小时分布（看用户活跃时间）
run("Hour of Day", ["hour"],
    ["sessions","engagedSessions"], limit=24)

print("\n[DONE]")
