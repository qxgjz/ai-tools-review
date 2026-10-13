# -*- coding: utf-8 -*-
import io, json, time, urllib.request, urllib.error
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = keys.get('github_pat') or keys.get('github_token') or ''
if not pat:
    for k, v in keys.items():
        if isinstance(v, str) and 'ghp_' in v:
            pat = v
            break
print('pat found:', bool(pat))
if not pat:
    raise SystemExit('no github pat')
# find run for commit 684c6de
url = 'https://api.github.com/repos/qxgjz/ai-tools-review/actions/runs?per_page=5&event=push'
req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + pat, 'Accept': 'application/vnd.github+json', 'User-Agent': 'aitoolcrux'})
runs = json.load(urllib.request.urlopen(req, timeout=30))
for run in runs.get('workflow_runs', [])[:5]:
    print(run['head_sha'][:7], run['name'], run['status'], run['conclusion'], run['id'])
