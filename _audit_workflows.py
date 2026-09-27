import subprocess
import urllib.request
import json
from datetime import datetime, timedelta

# Get token
result = subprocess.run(
    ["git", "credential", "fill"],
    input=b"protocol=https\nhost=github.com\n\n",
    capture_output=True
)
creds = {}
for line in result.stdout.decode().strip().split("\n"):
    if "=" in line:
        k, v = line.split("=", 1)
        creds[k] = v
token = creds.get("password", "")

repo = "qxgjz/ai-tools-review"
headers = {
    "User-Agent": "commander",
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Get all workflow runs from last 7 days
since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
all_runs = []
page = 1
while True:
    url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}&created=%3E{since}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    runs = data.get("workflow_runs", [])
    if not runs:
        break
    all_runs.extend(runs)
    if len(runs) < 100:
        break
    page += 1
    if page > 5:
        break

# Group by workflow name, get latest status
workflows = {}
for run in all_runs:
    name = run["name"]
    if name not in workflows:
        workflows[name] = {"latest": None, "failures": 0, "total": 0, "events": set()}
    workflows[name]["total"] += 1
    workflows[name]["events"].add(run["event"])
    if run["conclusion"] == "failure":
        workflows[name]["failures"] += 1
    if workflows[name]["latest"] is None or run["created_at"] > workflows[name]["latest"]["created_at"]:
        workflows[name]["latest"] = run

print(f"Total runs in last 7 days: {len(all_runs)}")
print(f"Distinct workflows: {len(workflows)}")
print()
print(f"{'Workflow':<35} {'Latest':<10} {'Fails/Total':<12} {'Events'}")
print("-" * 80)
for name in sorted(workflows.keys()):
    w = workflows[name]
    latest = w["latest"]
    status = latest["conclusion"] or latest["status"]
    events = ",".join(sorted(w["events"]))
    print(f"{name:<35} {status:<10} {w['failures']}/{w['total']:<10} {events}")
