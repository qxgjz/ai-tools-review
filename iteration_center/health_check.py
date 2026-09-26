"""
AIToolCrux Health Check Script
Checks all automated tasks for failures and generates health report.
Saves to: iteration_center/health_check.md
"""
import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

PROJECT = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
REPORT_DIR = PROJECT / "iteration_center"
HEALTH_FILE = REPORT_DIR / "health_check.md"

# Website URLs to check
URLS_TO_CHECK = [
    ("Homepage", "https://www.aitoolcrux.com"),
    ("Blog", "https://www.aitoolcrux.com/blog"),
    ("Tools Ranking", "https://www.aitoolcrux.com/ranking"),
    ("Sitemap", "https://www.aitoolcrux.com/sitemap.xml"),
    ("Robots.txt", "https://www.aitoolcrux.com/robots.txt"),
]

# Expected automated tasks and their indicators
TASKS = {
    "Core Iteration (every 3h)": {
        "indicator": "iteration_center/iteration_log.json",
        "expected_freq_hours": 3,
        "description": "Code modifications, bug fixes, SEO improvements",
    },
    "Daily Operation (02:00)": {
        "indicator": "auto_operation/reports",
        "expected_freq_hours": 24,
        "description": "Article layout check and FAQ improvement",
        "path_override": r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\auto_operation\reports",
    },
    "Context Auto-update (01:00)": {
        "indicator": "AIToolCrux_CONTEXT.md",
        "expected_freq_hours": 24,
        "description": "Updates shared context file for all tasks",
        "path_override": r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\AIToolCrux_CONTEXT.md",
    },
    "GSC/GA4 Report": {
        "indicator": "gsc-ga4-report",
        "expected_freq_hours": 24,
        "description": "Search Console and Analytics data",
    },
}

ALERT_THRESHOLD_HOURS = 48  # Alert if no update in 48 hours
CRITICAL_THRESHOLD_HOURS = 96  # Critical if no update in 96 hours


def check_url(url):
    """Check if URL is accessible."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HealthCheck/1.0"})
        start = datetime.now()
        resp = urllib.request.urlopen(req, timeout=15)
        elapsed = (datetime.now() - start).total_seconds()
        return {"status": resp.status, "latency_ms": int(elapsed * 1000), "ok": 200 <= resp.status < 400}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "latency_ms": 0, "ok": False}
    except Exception as e:
        return {"status": 0, "latency_ms": 0, "ok": False, "error": str(e)}


def get_file_mtime(filepath):
    """Get file modification time."""
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime)
    except:
        return None


def check_task_health(task_name, task_info):
    """Check if a task is healthy based on its indicator file."""
    if "path_override" in task_info:
        filepath = task_info["path_override"]
    else:
        filepath = str(PROJECT / task_info["indicator"])

    # For directories, check if any file exists inside
    if os.path.isdir(filepath):
        try:
            files = [f for f in os.listdir(filepath) if not f.startswith('.')]
            if not files:
                return {
                    "status": "NO_DATA",
                    "age_hours": None,
                    "message": f"Directory exists but is empty: {filepath}",
                }
            # Get newest file
            newest = max(
                [os.path.join(filepath, f) for f in files],
                key=os.path.getmtime
            )
            mtime = get_file_mtime(newest)
            newest_file = os.path.basename(newest)
        except:
            mtime = None
            newest_file = None
    else:
        if not os.path.exists(filepath):
            return {
                "status": "MISSING",
                "age_hours": None,
                "message": f"File not found: {filepath}",
            }
        mtime = get_file_mtime(filepath)
        newest_file = os.path.basename(filepath)

    if mtime is None:
        return {"status": "ERROR", "age_hours": None, "message": "Cannot read file time"}

    age_hours = (datetime.now() - mtime).total_seconds() / 3600
    expected = task_info["expected_freq_hours"] * 2  # Allow 2x expected frequency as buffer

    if age_hours > CRITICAL_THRESHOLD_HOURS:
        status = "CRITICAL"
    elif age_hours > ALERT_THRESHOLD_HOURS or age_hours > expected:
        status = "ALERT"
    else:
        status = "HEALTHY"

    return {
        "status": status,
        "age_hours": round(age_hours, 1),
        "last_file": newest_file,
        "last_modified": mtime.strftime("%Y-%m-%d %H:%M"),
        "message": f"Last updated {round(age_hours, 1)}h ago (expected ~{task_info['expected_freq_hours']}h)",
    }


def check_recent_commits():
    """Check recent iteration log for failures."""
    log_path = PROJECT / "iteration_center" / "iteration_log.json"
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            log = json.load(f)
        recent = log[-5:] if isinstance(log, list) else log.get("iterations", [])[-5:]

        failed = []
        for entry in recent:
            result = entry.get("result", "").lower()
            if "fail" in result or "error" in result or "❌" in result:
                failed.append(entry)

        return {
            "total_recent": len(recent),
            "failed": len(failed),
            "healthy": len(failed) == 0,
            "recent_rounds": [e.get("round", "?") for e in recent[-3:]],
        }
    except Exception as e:
        return {"error": str(e)}


def generate_report():
    """Generate the full health check report."""
    now = datetime.now()
    lines = []

    lines.append("# AIToolCrux Health Check Report")
    lines.append(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Check interval:** Automated")
    lines.append("")

    # Section 1: Website Availability
    lines.append("## 1. Website Availability")
    lines.append("")
    lines.append("| Page | URL | Status | Latency |")
    lines.append("|------|-----|--------|---------|")

    website_healthy = True
    for name, url in URLS_TO_CHECK:
        result = check_url(url)
        status_icon = "✅" if result["ok"] else "❌"
        latency = f"{result['latency_ms']}ms" if result["ok"] else "N/A"
        lines.append(f"| {name} | `{url}` | {status_icon} {result['status']} | {latency} |")
        if not result["ok"]:
            website_healthy = False

    lines.append("")

    # Section 2: Automated Tasks Health
    lines.append("## 2. Automated Tasks Health")
    lines.append("")
    lines.append("| Task | Status | Last Updated | Age | Expected |")
    lines.append("|------|--------|-------------|-----|----------|")

    alerts = []
    for task_name, task_info in TASKS.items():
        health = check_task_health(task_name, task_info)
        status = health["status"]
        if status == "HEALTHY":
            icon = "✅"
        elif status == "ALERT":
            icon = "⚠️"
            alerts.append(f"{task_name}: {health['message']}")
        elif status == "CRITICAL":
            icon = "🔴"
            alerts.append(f"CRITICAL - {task_name}: {health['message']}")
        else:
            icon = "❓"

        last_mod = health.get("last_modified", "N/A")
        age = f"{health.get('age_hours', '?')}h"
        expected = f"~{task_info['expected_freq_hours']}h"
        lines.append(f"| {task_name} | {icon} {status} | {last_mod} | {age} | {expected} |")

    lines.append("")

    # Section 3: Recent Iteration Status
    lines.append("## 3. Recent Iteration Status")
    lines.append("")
    commit_check = check_recent_commits()
    if "error" not in commit_check:
        healthy = "✅" if commit_check["healthy"] else "⚠️"
        lines.append(f"- Recent rounds checked: {commit_check.get('recent_rounds', 'N/A')}")
        lines.append(f"- Failed runs: {commit_check['failed']}/{commit_check['total_recent']} {healthy}")
    else:
        lines.append(f"- Error reading iteration log: {commit_check['error']}")
    lines.append("")

    # Section 4: Alerts
    lines.append("## 4. Active Alerts")
    lines.append("")
    if alerts:
        for alert in alerts:
            lines.append(f"- ⚠️ {alert}")
    else:
        lines.append("✅ No active alerts. All systems operational.")
    lines.append("")

    # Section 5: Summary Score
    lines.append("## 5. Summary")
    lines.append("")
    total_issues = len(alerts) + (0 if website_healthy else 1)
    if total_issues == 0:
        score = 9
        summary = "All systems healthy. Website accessible, all automated tasks running on schedule."
    elif total_issues <= 2:
        score = 7
        summary = f"Minor issues detected ({total_issues}). Review alerts above."
    elif total_issues <= 4:
        score = 5
        summary = f"Several issues detected ({total_issues}). Needs attention."
    else:
        score = 3
        summary = f"Multiple critical issues ({total_issues}). Immediate action required."

    lines.append(f"**Health Score:** {score}/10")
    lines.append(f"**Summary:** {summary}")
    lines.append("")
    lines.append("---")
    lines.append(f"*Auto-generated by health_check.py at {now.strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines), score, alerts


if __name__ == "__main__":
    report, score, alerts = generate_report()

    # Ensure directory exists
    os.makedirs(REPORT_DIR, exist_ok=True)

    with open(HEALTH_FILE, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Health check complete. Score: {score}/10")
    print(f"Report saved to: {HEALTH_FILE}")
    if alerts:
        print(f"Alerts ({len(alerts)}):")
        for a in alerts:
            print(f"  - {a}")
    else:
        print("No active alerts.")
