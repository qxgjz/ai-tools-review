# -*- coding: utf-8 -*-
import io, json, time, urllib.request
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = keys.get('github_pat') or keys.get('github_token')
url = 'https://api.github.com/repos/qxgjz/ai-tools-review/actions/runs?per_page=5'
req = urllib.request.Request(url, headers={'Authorization': 'token ' + pat, 'Accept': 'application/vnd.github+json', 'User-Agent': 'aitoolcrux'})
data = json.load(urllib.request.urlopen(req, timeout=30))
for r in data.get('workflow_runs', [])[:5]:
    print(r['id'], '|', r['name'], '|', r['head_sha'][:7], '|', r['status'], '|', r.get('conclusion'))
