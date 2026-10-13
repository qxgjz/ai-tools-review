# -*- coding: utf-8 -*-
import io, json, time, urllib.request
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = ''
for k, v in keys.items():
    if isinstance(v, str) and 'ghp_' in v:
        pat = v
        break
def get(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + pat, 'Accept': 'application/vnd.github+json', 'User-Agent': 'aitoolcrux'})
    return json.load(urllib.request.urlopen(req, timeout=30))
for i in range(20):
    runs = get('https://api.github.com/repos/qxgjz/ai-tools-review/actions/runs?per_page=3&event=push')
    deploy = None
    for run in runs.get('workflow_runs', []):
        if run['name'] == 'Deploy to Cloudflare Pages' and run['head_sha'][:7] == '684c6de':
            deploy = run
            break
    if not deploy:
        print(i, 'deploy run not found yet')
    else:
        print(i, 'status:', deploy['status'], '| conclusion:', deploy['conclusion'])
        if deploy['status'] == 'completed':
            print('FINAL:', deploy['conclusion'])
            break
    time.sleep(30)
